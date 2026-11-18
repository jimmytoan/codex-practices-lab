"""Derived numbers for the write-up, computed from results/runs.jsonl and the raw per-run events.

  python -m harness.analysis > results/findings-full.md

Every number in the blog post should trace either to results/report-full-*.md or to this file's output.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from statistics import mean, median

from .config import RESULTS

TAGS = {"full-terra": "gpt-6.1-terra", "full-luna": "gpt-6-luna"}
SHORT = {"gpt-6.1-terra": "Terra", "gpt-6-luna": "Luna"}


def load() -> list[dict]:
    rows = [json.loads(l) for l in (RESULTS / "runs.jsonl").read_text().splitlines() if l.strip()]
    return [r for r in rows if r["tag"] in TAGS and r["status"] != "error"]


def commands(r: dict) -> list[str]:
    out = []
    for f in sorted((RESULTS / "raw" / r["run_id"]).glob("events-*.jsonl")):
        for line in f.read_text().splitlines():
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if d.get("type") == "item.completed" and d["item"].get("type") == "command_execution":
                out.append(d["item"]["command"])
    return out


READ_AGENTS = re.compile(r"\b(cat|tail|head|sed|less|nl|awk)\b[^|;&]*AGENTS\.md|rg -n[^|;&]*AGENTS\.md|AGENTS\.md[^|;&]*\|\s*(tail|head|sed)")
OUTSIDE_REPO = re.compile(r"(/Users/AGENTS\.md|/Users/[^/ ]+/AGENTS\.md|\.\./AGENTS\.md|\.cache/[^ ]*/AGENTS\.md)")


def pct(a: float, b: float) -> str:
    return f"{(b / a - 1) * 100:+.0f}%"


def main() -> None:
    rows = load()
    by = defaultdict(list)
    for r in rows:
        by[(r["model"], r["condition"])].append(r)
    out = ["# Derived findings (full run)", "",
           f"Runs: {len(rows)} counted ({', '.join(f'{SHORT[m]} {sum(r['model'] == m for r in rows)}' for m in TAGS.values())}). "
           "Computed by `python -m harness.analysis`.", ""]

    # 1. Each condition against base, same 14 tasks x 3 repeats
    out += ["## 1. Each condition against `base` (all conditions below ran all 14 tasks, 3 times)", "",
            "| Model | Condition | Passed | Median input tokens | vs base | Median output tokens | vs base | Mean cost | vs base | Median wall s | vs base |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]
    for m in TAGS.values():
        base = by[(m, "base")]
        bi, bo = median(r["usage"]["input_tokens"] for r in base), median(r["usage"]["output_tokens"] for r in base)
        bc, bw = mean(r["cost_usd"] for r in base), median(r["wall_s"] for r in base)
        for c in ["base", "agents_none", "agents_bloated", "prompt_oneline", "plan", "effort_low", "effort_high"]:
            rs = by[(m, c)]
            i, o = median(r["usage"]["input_tokens"] for r in rs), median(r["usage"]["output_tokens"] for r in rs)
            cc, w = mean(r["cost_usd"] for r in rs), median(r["wall_s"] for r in rs)
            out.append(f"| {SHORT[m]} | {c} | {sum(r['passed'] for r in rs)}/{len(rs)} | {i:,.0f} | {pct(bi, i)} | {o:,.0f} | {pct(bo, o)} "
                       f"| ${cc:.4f} | {pct(bc, cc)} | {w:.0f} | {pct(bw, w)} |")
    out.append("")

    # 2. Hard tasks only (t11-t14) against base
    out += ["## 2. Same, hard tasks t11-t14 only", "", "| Model | Condition | Passed | Mean cost | vs base | Median wall s |", "|---|---|---|---|---|---|"]
    for m in TAGS.values():
        hard = lambda c: [r for r in by[(m, c)] if r["task"][:3] in ("t11", "t12", "t13", "t14")]  # noqa: E731
        bc = mean(r["cost_usd"] for r in hard("base"))
        for c in ["base", "agents_none", "agents_bloated", "prompt_oneline", "plan", "effort_low", "effort_high"]:
            rs = hard(c)
            out.append(f"| {SHORT[m]} | {c} | {sum(r['passed'] for r in rs)}/{len(rs)} | ${mean(r['cost_usd'] for r in rs):.4f} "
                       f"| {pct(bc, mean(r['cost_usd'] for r in rs))} | {median(r['wall_s'] for r in rs):.0f} |")
    out.append("")

    # 3. Did the agent open AGENTS.md itself?
    out += ["## 3. Commands that touch AGENTS.md", "",
            "`mentions` = any shell command containing `AGENTS.md` (mostly `rg --files -g AGENTS.md`, looking for nested files). "
            "`reads` = a command that prints its content (cat/tail/head/sed/rg -n ... AGENTS.md). "
            "`outside repo` = looked for AGENTS.md above the repo root.", "",
            "| Model | Condition | Runs | mentions | reads | outside repo |", "|---|---|---|---|---|---|"]
    cache = {r["run_id"]: commands(r) for r in rows}
    for m in TAGS.values():
        for c in ["agents_none", "base", "agents_bloated", "rule_early", "rule_late", "prompt_oneline", "plan", "effort_low", "effort_high"]:
            rs = by[(m, c)]
            men = sum(any("AGENTS.md" in x for x in cache[r["run_id"]]) for r in rs)
            rd = sum(any(READ_AGENTS.search(x) for x in cache[r["run_id"]]) for r in rs)
            outside = sum(any(OUTSIDE_REPO.search(x) for x in cache[r["run_id"]]) for r in rs)
            out.append(f"| {SHORT[m]} | {c} | {len(rs)} | {men} | {rd} | {outside} |")
    out.append("")

    # 4. rule_late: reading the file vs following the rule
    out += ["## 4. Rule placed after byte 32,768: read the file itself vs followed the rule", "",
            "| Model | Read AGENTS.md content | Followed | Runs |", "|---|---|---|---|"]
    for m in TAGS.values():
        cross = Counter((any(READ_AGENTS.search(x) for x in cache[r["run_id"]]), r["rule_followed"]) for r in by[(m, "rule_late")])
        for (read, fol), n in sorted(cross.items()):
            out.append(f"| {SHORT[m]} | {read} | {fol} | {n} |")
    examples = [r["run_id"] for r in by[("gpt-6.1-terra", "rule_late")] if r["rule_followed"]]
    out += ["", f"Terra rule_late runs that followed the rule: {', '.join(examples)}", ""]

    # 5. Rule loaded but not followed
    out += ["## 5. Rule in the loaded AGENTS.md but not followed", "", "| Run | Model | Condition | Task | ShopError anywhere in diff | `raise ValueError` lines added |", "|---|---|---|---|---|---|"]
    for r in rows:
        if r["rule_followed"] is False and r["rollout"].get("agents_loaded_has_rule"):
            d = (RESULTS / "raw" / r["run_id"] / "diff.patch").read_text()
            added = len(re.findall(r"^\+\s+raise ValueError", d, re.M))
            out.append(f"| `{r['run_id']}` | {SHORT[r['model']]} | {r['condition']} | {r['task']} | {'ShopError' in d} | {added} |")
    rule_cells = defaultdict(lambda: [0, 0])
    for r in rows:
        if r["rule_followed"] is not None and r["rollout"].get("agents_loaded_has_rule"):
            k = (r["model"], r["task"][:3] == "t01")
            rule_cells[k][0] += r["rule_followed"]
            rule_cells[k][1] += 1
    out += ["", "Rule followed when it was in the loaded text, all conditions:", ""]
    for (m, is_t01), (f, n) in sorted(rule_cells.items()):
        out.append(f"- {SHORT[m]}, {'t01 only' if is_t01 else 'rule tasks other than t01'}: {f}/{n}")
    out.append("")

    # 6. Review
    out += ["## 6. Review: same session vs fresh session", "",
            "| Model | Condition | Runs | Bugs caught | Mean cost | Median wall s | Findings | Findings per run |", "|---|---|---|---|---|---|---|---|"]
    for m in TAGS.values():
        for c in ["review_same_buggy", "review_fresh_buggy", "review_same_clean", "review_fresh_clean"]:
            rs = by[(m, c)]
            caught = sum(len(r["bugs_caught"]) for r in rs) if c.endswith("buggy") else None
            seeded = sum(len(r["bug_signatures"]) for r in rs) if c.endswith("buggy") else None
            nf = sum(len(r["findings"] or []) for r in rs)
            out.append(f"| {SHORT[m]} | {c} | {len(rs)} | {f'{caught}/{seeded}' if caught is not None else '-'} | ${mean(r['cost_usd'] for r in rs):.4f} "
                       f"| {median(r['wall_s'] for r in rs):.0f} | {nf} | {nf / len(rs):.2f} |")
        same = mean(r["cost_usd"] for r in by[(m, "review_same_buggy")] + by[(m, "review_same_clean")])
        fresh = mean(r["cost_usd"] for r in by[(m, "review_fresh_buggy")] + by[(m, "review_fresh_clean")])
        out.append(f"| {SHORT[m]} | same / fresh cost ratio | | | {same / fresh:.2f}x | | | |")
    out += ["", "Findings on the bug-free patches, sorted by keyword (one finding can only land in the first matching group):", "",
            "| Model | Session | Findings | ShopError / ValueError rule | shipping_cost tier bug (pre-existing) | unknown coupon kind (spec silent) | other (hardening beyond the spec) |",
            "|---|---|---|---|---|---|---|"]
    for m in TAGS.values():
        for s in ["same", "fresh"]:
            groups = Counter()
            for r in by[(m, f"review_{s}_clean")]:
                for f in r["findings"] or []:
                    t = f["description"].lower()
                    if "no bugs" in t or "none found" in t:
                        groups["none"] += 1
                    elif "kind" in t and "coupon" in t:
                        groups["kind"] += 1
                    elif "tier" in t or ("boundar" in t and "shipping" in t):
                        groups["tier"] += 1
                    elif "shoperror" in t or "valueerror" in t:
                        groups["rule"] += 1
                    elif False:
                        groups["none"] += 1
                    else:
                        groups["other"] += 1
            total = sum(v for k, v in groups.items() if k != "none")
            out.append(f"| {SHORT[m]} | {s} | {total} | {groups['rule']} | {groups['tier']} | {groups['kind']} | {groups['other']} |")
    out += ["", "Note: the bug-free patches for t11-t14 raise a bare ValueError, which the repo's AGENTS.md forbids, and t10's touches code "
            "next to the pre-existing shipping_cost boundary bug (task t01). Findings in those two groups are correct, not false alarms.", ""]

    # 7. Failures and scope
    out += ["## 7. Failed runs and out-of-scope edits", ""]
    for r in rows:
        if not r["passed"] or r["out_of_scope"]:
            out.append(f"- `{r['run_id']}` {SHORT[r['model']]} {r['condition']} {r['task']}: passed={r['passed']} "
                       f"failed={r['hidden']['failed']} out_of_scope={r['out_of_scope']}")
    out.append("")

    # 8. Totals
    out += ["## 8. Totals", ""]
    for tag, m in TAGS.items():
        rs = [r for r in rows if r["tag"] == tag]
        out.append(f"- {SHORT[m]}: {len(rs)} runs, passed {sum(r['passed'] for r in rs)}, spend ${sum(r['cost_usd'] for r in rs):.2f} upper / "
                   f"${sum(r['cost_usd_low'] for r in rs):.2f} lower, input tokens {sum(r['usage']['input_tokens'] for r in rs):,}, "
                   f"output tokens {sum(r['usage']['output_tokens'] for r in rs):,}, wall {sum(r['wall_s'] for r in rs) / 3600:.1f} h")
    print("\n".join(out))


if __name__ == "__main__":
    main()
