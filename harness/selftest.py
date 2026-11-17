"""Prove the harness and graders measure what they claim, without any model call.

  ~/.cache/codex-practices-lab/venv/bin/python -m harness.selftest
"""

from __future__ import annotations

import json
import shutil
import sys
import uuid

from . import agentsmd, codexrun, workspace
from .config import WORK, cost
from .run import bug_signatures, cells, may_start
from .config import CONDITION_LIST
from .tasks import TASKS

ok = True


def check(cond: bool, label: str, detail: str = "") -> None:
    global ok
    ok &= cond
    print(f"{'OK  ' if cond else 'BAD '} {label}" + (f"  [{detail}]" if detail and not cond else ""))


def fresh(agents: str = "none"):
    repo = WORK / f"selftest-{uuid.uuid4().hex[:6]}"
    return repo, workspace.make_copy(repo, agents)


WORK.mkdir(parents=True, exist_ok=True)

# 1. AGENTS.md variants have the sizes and rule positions the tests depend on
sizes = agentsmd.write_all()
check(sizes["short"][0] < 4096 and sizes["short"][1] is not None, "short AGENTS.md is under 4 KiB and has the rule", str(sizes["short"]))
check(25 * 1024 < sizes["bloated"][0] < agentsmd.LIMIT and sizes["bloated"][1] < 2048,
      "bloated AGENTS.md is short + ~25 KiB, under the 32 KiB limit, rule near the top", str(sizes["bloated"]))
check(sizes["rule_early"][0] > agentsmd.LIMIT and sizes["rule_early"][1] < 2048, "rule_early: file past the limit, rule in the first 2 KiB", str(sizes["rule_early"]))
check(sizes["rule_late"][0] > agentsmd.LIMIT and sizes["rule_late"][1] > agentsmd.LIMIT, "rule_late: rule starts after byte 32768", str(sizes["rule_late"]))
check(abs(sizes["rule_late"][0] - sizes["rule_early"][0]) < 64, "rule_early and rule_late are the same size")
for kind in ("bloated", "rule_early"):
    text = agentsmd.build(kind)
    check(text.count(agentsmd.RULE_MARKER) == 1, f"{kind}: the rule appears exactly once")
check(agentsmd.RULE_MARKER not in agentsmd.filler(40 * 1024), "filler never mentions the rule")

# 2. Every task: the untouched repo fails its hidden tests, the reference passes them and the visible suite;
#    for rule tasks the rule test tells a ShopError solution from a plain ValueError one
for tid, task in TASKS.items():
    repo, base = fresh()
    before = workspace.grade_hidden(repo, tid)
    check(not before["ok"] and not before["error"], f"{tid}: untouched repo fails hidden tests",
          f"{len(before['failed'])} failing, error={before['error']}")
    workspace.apply_edits(repo, task.edits)
    after = workspace.grade_hidden(repo, tid)
    vis = workspace.grade_visible(repo)
    check(after["ok"] and vis["ok"], f"{tid}: reference passes {len(after['passed'])} hidden tests and the visible suite",
          f"failed={after['failed']} error={after['error']} visible={vis}")
    if task.has_rule:
        r_without = workspace.grade_rule(repo, tid)
        workspace.apply_edits(repo, task.rule_edits)
        r_with = workspace.grade_rule(repo, tid)
        still = workspace.grade_hidden(repo, tid)
        check(not r_without["ok"] and r_with["ok"] and still["ok"],
              f"{tid}: rule test fails on ValueError, passes on ShopError", f"{r_without} / {r_with}")
    else:
        check(workspace.grade_rule(repo, tid) is None, f"{tid}: no rule test (not a rule task)")
    shutil.rmtree(repo)

# 3. Seeded bugs: each bug alone breaks its own non-empty set of hidden tests, sets do not overlap,
#    and all bugs together break the union
for tid, task in TASKS.items():
    if not task.bugs:
        continue
    sigs = bug_signatures(tid)
    names = list(sigs)
    check(all(sigs[n] for n in names), f"{tid}: every seeded bug breaks at least one hidden test", json.dumps(sigs))
    check(not set(sigs[names[0]]) & set(sigs[names[1]]), f"{tid}: the two bugs break different tests", json.dumps(sigs))
    repo, _ = fresh()
    workspace.apply_edits(repo, task.reference() + [e for b in task.bugs.values() for e in b])
    both = set(workspace.grade_hidden(repo, tid)["failed"])
    check(both == set(sigs[names[0]]) | set(sigs[names[1]]), f"{tid}: both bugs together fail exactly the union",
          f"{sorted(both)}")
    check(workspace.grade_visible(repo)["ok"], f"{tid}: seeded bugs still pass the visible suite (they look done)")
    shutil.rmtree(repo)

# 4. Scope detector
repo, base = fresh()
(repo / "src/shoplib/legacy_pricing.py").write_text("# changed\n")
(repo / "tests/test_new.py").write_text("def test_x():\n    pass\n")
(repo / "src/shoplib/shipping.py").write_text((repo / "src/shoplib/shipping.py").read_text() + "\n")
(repo / "src/shoplib/__pycache__").mkdir(exist_ok=True)
(repo / "src/shoplib/__pycache__/x.pyc").write_text("x")
changed = workspace.changed_files(repo, base)
oos = workspace.out_of_scope(changed, TASKS["t01-shipping-boundary"].scope)
check(oos == ["src/shoplib/legacy_pricing.py"], "out-of-scope detector flags legacy_pricing.py only",
      f"changed={changed} oos={oos}")
workspace.git(repo, "add", "-A")
workspace.git(repo, "commit", "-q", "-m", "agent committed")
check(workspace.changed_files(repo, base) == changed, "changes the agent committed are still counted")
shutil.rmtree(repo)

# 5. Event parser on the recorded probe run (codex-cli 0.169.0, real output)
lines = (codexrun.Path(__file__).parent / "fixtures" / "probe_events.jsonl").read_text().splitlines()
inv = codexrun.parse_events(lines)
check(inv.status == "ok" and inv.thread_id and inv.usage.get("input_tokens") == 56681 and len(inv.commands) == 2,
      "event parser reads thread id, usage and commands from a real run", f"{inv.status} {inv.usage} {len(inv.commands)}")
bad = codexrun.parse_events(lines[:3] + ['{"type": "turn.failed", "error": {"message": "429"}}'])
check(bad.status == "error", "a turn.failed run is an error (excluded and redone by --resume)")
check(codexrun.parse_events(lines[:-1]).status == "error", "a run with no turn.completed is an error")
facts = codexrun.rollout_facts(codexrun.Path(__file__).parent / "fixtures" / "probe_rollout.jsonl")
check(facts["agents_loaded_bytes"] and facts["turns"][0]["effort"] == "low" and facts["turns"][0]["model"] == "gpt-6.1-terra",
      "rollout facts: loaded AGENTS.md size, model and effort", json.dumps(facts)[:300])
check(codexrun.rollout_usage(codexrun.Path(__file__).parent / "fixtures" / "probe_rollout.jsonl", 0)["input_tokens"] == 56681,
      "summed rollout token records match turn.completed (live spend guard sees the same numbers)")

# 6. Cost and the spend cap
u = {"input_tokens": 1_000_000, "cached_input_tokens": 500_000, "cache_write_input_tokens": 250_000, "output_tokens": 100_000}
check(abs(cost("gpt-6.1-terra", u) - (0.25 + 0.025 + 0.625 + 0.5)) < 1e-9, "cost: terra, cache writes at the 12h price")
check(abs(cost("gpt-6.1-terra", u, "write_30m") - (0.25 + 0.025 + 0.3125 + 0.5)) < 1e-9, "cost: terra, cache writes at the 30m price")
check(may_start(4.0, 0.0, 0.75, 5.0) and not may_start(4.3, 0.0, 0.75, 5.0) and not may_start(3.0, 1.5, 0.75, 5.0),
      "cap: a run starts only if spent + in flight + its own kill limit fits")

# 7. The matrix
c = cells(CONDITION_LIST, list(TASKS))
check(len(c) == 140, f"one repeat of the full matrix is 140 runs (got {len(c)})")

print("\nSELF-TEST", "PASSED" if ok else "FAILED")
sys.exit(0 if ok else 1)
