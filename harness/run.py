"""Run the matrix.

  python -m harness.run --tag pilot --cap 5 --conditions base,plan --tasks t01,t07 --repeat 1
  python -m harness.run --tag full --cap 40 --repeat 3 --resume

One record per run is appended to results/runs.jsonl. --resume skips cells this tag already has (runs that
ended in a provider/harness error do not count, so they are redone). --cap is a hard limit on the tag's
total upper-bound spend: a run starts only if spend so far plus --run-cap fits under it, and every run is
killed if its own spend passes --run-cap, so the tag can never exceed --cap.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from . import codexrun, workspace
from .config import CONDITION_LIST, CONDITIONS_BY_NAME, CODEX, RESULTS, ROOT, WORK, Condition, cost
from .tasks import RULE_TASKS, SEEDED_TASKS, TASKS

RUNS = RESULTS / "runs.jsonl"
LOCK = threading.Lock()

PLAN_SUFFIX = ("\n\nFirst, plan only: read what you need, then reply with a short numbered plan for this change. "
               "Do not edit any files yet.")
IMPLEMENT = "Now implement the plan."
REVIEW_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["findings"],
    "properties": {"findings": {"type": "array", "items": {
        "type": "object", "additionalProperties": False, "required": ["file", "description"],
        "properties": {"file": {"type": "string"}, "description": {"type": "string"}}}}},
}


def review_prompt(task) -> str:
    return ("Review the uncommitted change in this repository (see `git diff`). It is meant to do this:\n\n"
            f"{task.four_part()}\n\nCheck the change against the spec for bugs. Fix every bug you find and run the "
            "tests. In your final answer, list each bug you found; list none if you found none.")


def apply_prompt(task, patch: str) -> str:
    return (f"{task.four_part()}\n\nA teammate already wrote this change. Apply exactly this patch with `git apply`, "
            f"run the tests and report the result. Do not change anything else.\n\n```diff\n{patch}```")


def codex_version() -> str:
    return subprocess.run([CODEX, "--version"], capture_output=True, text=True).stdout.strip()


def cells(conditions: list[Condition], tasks: list[str]) -> list[tuple[str, str]]:
    out = []
    for c in conditions:
        pool = {"all": list(TASKS), "rule": RULE_TASKS, "seeded": SEEDED_TASKS}[c.tasks]
        out += [(c.name, t) for t in pool if t in tasks]
    return out


def load_records(tag: str) -> list[dict]:
    if not RUNS.exists():
        return []
    rows = [json.loads(l) for l in RUNS.read_text().splitlines() if l.strip()]
    return [r for r in rows if r["tag"] == tag]


def spent(tag: str) -> float:
    return sum(r.get("cost_usd") or 0 for r in load_records(tag))


def may_start(spent_usd: float, in_flight_usd: float, run_cap: float, cap: float) -> bool:
    """A run may start only if everything already spent or reserved, plus this run's own kill limit, fits."""
    return spent_usd + in_flight_usd + run_cap <= cap


def total_usage(invs: list[codexrun.Invocation]) -> dict:
    keys = ["input_tokens", "cached_input_tokens", "cache_write_input_tokens", "output_tokens", "reasoning_output_tokens"]
    return {k: sum(i.usage.get(k, 0) for i in invs) for k in keys}


def one_run(cond: Condition, task_id: str, model: str, tag: str, version: str, run_cap: float) -> dict:
    task = TASKS[task_id]
    run_id = f"{datetime.now():%Y%m%d-%H%M%S}-{cond.name}-{task_id[:3]}-{uuid.uuid4().hex[:4]}"
    raw = RESULTS / "raw" / run_id
    raw.mkdir(parents=True)
    base_dir = WORK / run_id
    repo = base_dir / "repo"
    home = codexrun.fresh_codex_home(base_dir / "codex-home")
    base = workspace.make_copy(repo, cond.agents)
    print(f"=== {run_id} | {cond.name} | {task_id} | {model}/{cond.effort}", flush=True)

    kw = dict(cwd=repo, codex_home=home, model=model, effort=cond.effort, spend_cap_usd=run_cap)
    invs: list[codexrun.Invocation] = []
    extra: dict = {}
    remaining = lambda: run_cap - sum(cost(model, i.usage) for i in invs)  # noqa: E731

    if cond.mode == "direct":
        prompt = task.four_part() if cond.prompt == "four_part" else task.one_line
        invs.append(codexrun.run(prompt, sandbox="workspace-write", events_out=raw / "events-1.jsonl", **kw))
    elif cond.mode == "plan":
        first = codexrun.run(task.four_part() + PLAN_SUFFIX, sandbox="read-only", events_out=raw / "events-1.jsonl", **kw)
        invs.append(first)
        extra["plan_text"] = first.final_message[:4000]
        extra["edits_during_plan"] = workspace.changed_files(repo, base)
        if first.status == "ok":
            kw["spend_cap_usd"] = remaining()
            invs.append(codexrun.run(IMPLEMENT, sandbox="workspace-write", resume_thread=first.thread_id,
                                     events_out=raw / "events-2.jsonl", **kw))
    else:  # review_same / review_fresh
        reviewed = repo.parent / "reviewed-variant"
        workspace.make_copy(reviewed, cond.agents)
        workspace.apply_edits(reviewed, task.reference() + [e for b in task.bugs.values() for e in b]
                              if cond.variant == "buggy" else task.reference())
        patch = workspace.diff(reviewed, workspace.git(reviewed, "rev-parse", "HEAD").strip())
        shutil.rmtree(reviewed)
        (raw / "seeded.patch").write_text(patch)
        schema = base_dir / "review-schema.json"
        schema.write_text(json.dumps(REVIEW_SCHEMA))
        if cond.mode == "review_same":
            first = codexrun.run(apply_prompt(task, patch), sandbox="workspace-write", events_out=raw / "events-1.jsonl", **kw)
            invs.append(first)
            extra["applied_exactly"] = workspace.diff(repo, base) == patch
            extra["before_review"] = workspace.grade_hidden(repo, task_id)
            if first.status == "ok":
                kw["spend_cap_usd"] = remaining()
                invs.append(codexrun.run(review_prompt(task), sandbox="workspace-write", resume_thread=first.thread_id,
                                         output_schema=schema, events_out=raw / "events-2.jsonl", **kw))
        else:
            subprocess.run(["git", "apply"], input=patch, text=True, cwd=repo, check=True)
            extra["applied_exactly"] = True
            extra["before_review"] = workspace.grade_hidden(repo, task_id)
            invs.append(codexrun.run(review_prompt(task), sandbox="workspace-write", output_schema=schema,
                                     events_out=raw / "events-1.jsonl", **kw))
        try:
            extra["findings"] = json.loads(invs[-1].final_message).get("findings", [])
        except (json.JSONDecodeError, AttributeError):
            extra["findings"] = None

    # ---- grade
    changed = workspace.changed_files(repo, base)
    (raw / "diff.patch").write_text(workspace.diff(repo, base))
    hidden = workspace.grade_hidden(repo, task_id)
    rule = workspace.grade_rule(repo, task_id)
    visible = workspace.grade_visible(repo)
    rollout = codexrun.find_rollout(home, invs[0].thread_id) if invs and invs[0].thread_id else None
    facts = codexrun.rollout_facts(rollout)
    if rollout:
        shutil.copy(rollout, raw / "rollout.jsonl")
    if cond.mode.startswith("review"):
        extra["bug_signatures"] = bug_signatures(task_id)
        failing = set(hidden["failed"])
        extra["bugs_caught"] = sorted(b for b, sig in extra["bug_signatures"].items() if not (set(sig) & failing))
        bug_tests = {t for sig in extra["bug_signatures"].values() for t in sig}
        extra["regressions"] = sorted(failing - bug_tests) if cond.variant == "buggy" else sorted(failing)

    commands = [c for i in invs for c in i.commands]
    status = next((i.status for i in invs if i.status != "ok"), "ok")
    usage = total_usage(invs)
    record = {
        "run_id": run_id, "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), "tag": tag,
        "condition": cond.name, "task": task_id, "model": model, "effort": cond.effort, "codex_version": version,
        "agents": cond.agents, "prompt": cond.prompt, "mode": cond.mode, "variant": cond.variant,
        "status": status, "error": next((i.error for i in invs if i.error), None),
        "invocations": [{"status": i.status, "wall_s": i.wall_s, "usage": i.usage, "exit": i.exit_code,
                         "stderr_tail": i.stderr_tail[-300:] if i.status != "ok" else ""} for i in invs],
        "usage": usage,
        "cost_usd": round(sum(cost(model, i.usage) for i in invs), 5),
        "cost_usd_low": round(sum(cost(model, i.usage, "write_30m") for i in invs), 5),
        "wall_s": round(sum(i.wall_s for i in invs), 1),
        "passed": hidden["ok"], "hidden": hidden, "visible": visible,
        "rule_followed": rule["ok"] if rule else None,
        "changed_files": changed, "out_of_scope": workspace.out_of_scope(changed, task.scope),
        "commands": len(commands),
        "peeked": [c for c in commands if any(s in c for s in (str(ROOT), "/hidden/", "/.codex/", "/.codex "))],
        "rollout": facts,
        **extra,
    }
    (raw / "record.json").write_text(json.dumps(record, indent=2))
    with LOCK:
        with RUNS.open("a") as fh:
            fh.write(json.dumps(record) + "\n")
    shutil.rmtree(base_dir, ignore_errors=True)
    print(f"    {status} passed={hidden['ok']} rule={record['rule_followed']} oos={record['out_of_scope']} "
          f"${record['cost_usd']:.3f} {record['wall_s']}s in={usage['input_tokens']} out={usage['output_tokens']}"
          + (f" caught={extra.get('bugs_caught')} regress={extra.get('regressions')} findings="
             f"{len(extra['findings']) if extra.get('findings') is not None else None}" if cond.mode.startswith('review') else ""),
          flush=True)
    return record


_SIG_CACHE: dict[str, dict] = {}


def bug_signatures(task_id: str) -> dict[str, list[str]]:
    """For each seeded bug: the hidden tests that fail when only that bug is present. Computed locally."""
    if task_id in _SIG_CACHE:
        return _SIG_CACHE[task_id]
    task = TASKS[task_id]
    sigs = {}
    for name, edits in task.bugs.items():
        repo = WORK / f"sig-{task_id}-{name}-{uuid.uuid4().hex[:4]}"
        workspace.make_copy(repo, "none")
        workspace.apply_edits(repo, task.reference() + edits)
        sigs[name] = workspace.grade_hidden(repo, task_id)["failed"]
        shutil.rmtree(repo, ignore_errors=True)
    _SIG_CACHE[task_id] = sigs
    return sigs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--model", default="gpt-6.1-terra")
    ap.add_argument("--conditions", help="comma-separated condition names (default: all)")
    ap.add_argument("--tasks", help="comma-separated task prefixes, e.g. t01,t07 (default: all)")
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--cap", type=float, required=True, help="hard limit on this tag's total spend, USD")
    ap.add_argument("--run-cap", type=float, default=0.75, help="kill a run whose own spend passes this, USD")
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--plan", help="JSON file with an explicit list of [condition, task] cells (overrides the matrix)")
    args = ap.parse_args()

    if not (ROOT / ".codex-home" / "auth.json").exists():
        raise SystemExit("run `codex login --with-api-key` with CODEX_HOME=.codex-home first")
    RESULTS.mkdir(exist_ok=True)
    version = codex_version()
    conds = [CONDITIONS_BY_NAME[c] for c in args.conditions.split(",")] if args.conditions else CONDITION_LIST
    tasks = [t for t in TASKS if not args.tasks or any(t.startswith(p) for p in args.tasks.split(","))]
    todo_cells = [tuple(c) for c in json.loads(Path(args.plan).read_text())] if args.plan else cells(conds, tasks)

    done: dict[tuple, int] = {}
    if args.resume:
        for r in load_records(args.tag):
            if r["status"] != "error" and r["model"] == args.model:
                done[(r["condition"], r["task"])] = done.get((r["condition"], r["task"]), 0) + 1
    queue = []
    for rep in range(args.repeat):
        for cell in todo_cells:
            if done.get(cell, 0) > rep:
                continue
            queue.append(cell)
    print(f"{len(queue)} runs to do for tag {args.tag!r}; spent so far ${spent(args.tag):.2f} of ${args.cap:.2f}", flush=True)

    in_flight = [0.0]

    def guarded(cell):
        with LOCK:
            committed = spent(args.tag) + in_flight[0]
            if not may_start(spent(args.tag), in_flight[0], args.run_cap, args.cap):
                print(f"    SKIP {cell}: ${committed:.2f} spent or in flight + run cap ${args.run_cap} > cap ${args.cap}",
                      flush=True)
                return None
            in_flight[0] += args.run_cap
        try:
            return one_run(CONDITIONS_BY_NAME[cell[0]], cell[1], args.model, args.tag, version, args.run_cap)
        except Exception as exc:  # a setup failure must not stop the batch
            print(f"    HARNESS FAILURE {cell}: {type(exc).__name__}: {exc}", flush=True)
            return None
        finally:
            with LOCK:
                in_flight[0] -= args.run_cap

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        list(pool.map(guarded, queue))
    print(f"done in {time.time() - t0:.0f}s; tag {args.tag!r} spend ${spent(args.tag):.2f} of ${args.cap:.2f}", flush=True)


if __name__ == "__main__":
    main()
