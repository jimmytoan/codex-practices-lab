"""Aggregate results/runs.jsonl into the tables the write-up uses.

  python -m harness.report --tag pilot            # print markdown
  python -m harness.report --tag full --out results/report-full.md

Runs that ended in a provider or harness error (status "error") are left out and counted. Runs killed by the
per-run spend cap or the time limit are kept: they are failures of the condition, not of the provider.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from statistics import mean, median

from .config import CONDITIONS_BY_NAME, RESULTS, TESTS
from .tasks import RULE_TASKS, TASKS


def load(tag: str) -> tuple[list[dict], list[dict]]:
    rows = [json.loads(l) for l in (RESULTS / "runs.jsonl").read_text().splitlines() if l.strip()]
    rows = [r for r in rows if r["tag"] == tag]
    return [r for r in rows if r["status"] != "error"], [r for r in rows if r["status"] == "error"]


def frac(xs) -> str:
    xs = list(xs)
    return f"{sum(xs)}/{len(xs)}" if xs else "–"


def med(xs) -> str:
    xs = list(xs)
    return f"{median(xs):,.0f}" if xs else "–"


def condition_table(rows: list[dict], names: list[str]) -> str:
    out = ["| Condition | Runs | Passed | Rule followed | Out-of-scope runs | Median input tokens | Median output tokens "
           "| Cost (upper) | Cost per run | Cost per pass | Median wall s | Killed |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for name in names:
        rs = [r for r in rows if r["condition"] == name]
        if not rs:
            out.append(f"| {name} | 0 |" + " – |" * 10)
            continue
        spend = sum(r["cost_usd"] for r in rs)
        n_pass = sum(r["passed"] for r in rs)
        rule = [r["rule_followed"] for r in rs if r["rule_followed"] is not None]
        out.append(
            f"| {name} | {len(rs)} | {n_pass}/{len(rs)} | {frac(rule)} | {sum(bool(r['out_of_scope']) for r in rs)} "
            f"| {med(r['usage']['input_tokens'] for r in rs)} | {med(r['usage']['output_tokens'] for r in rs)} "
            f"| ${spend:.2f} | ${spend / len(rs):.3f} | {'$%.3f' % (spend / n_pass) if n_pass else 'n/a'} "
            f"| {med(r['wall_s'] for r in rs)} | {sum(r['status'] != 'ok' for r in rs)} |")
    return "\n".join(out)


def paired_note(rows: list[dict], a: str, b: str) -> str:
    """Pass rate on the tasks both conditions ran, so a subset pilot does not mislead."""
    tasks = {r["task"] for r in rows if r["condition"] == a} & {r["task"] for r in rows if r["condition"] == b}
    if not tasks:
        return ""
    pa = [r["passed"] for r in rows if r["condition"] == a and r["task"] in tasks]
    pb = [r["passed"] for r in rows if r["condition"] == b and r["task"] in tasks]
    return f"- On the {len(tasks)} tasks both ran: {a} {frac(pa)}, {b} {frac(pb)}."


def rule_table(rows: list[dict]) -> str:
    out = ["| Condition | Runs (rule tasks) | Rule followed | AGENTS.md bytes loaded (median) | Loaded text contains the rule | Tasks passed |",
           "|---|---|---|---|---|---|"]
    for name in TESTS["2 32 KiB limit"]:
        rs = [r for r in rows if r["condition"] == name and r["task"] in RULE_TASKS]
        if not rs:
            continue
        loaded = [r["rollout"].get("agents_loaded_bytes") for r in rs if r["rollout"].get("agents_loaded_bytes") is not None]
        out.append(f"| {name} | {len(rs)} | {frac(r['rule_followed'] for r in rs)} | {med(loaded)} "
                   f"| {frac(bool(r['rollout'].get('agents_loaded_has_rule')) for r in rs)} | {frac(r['passed'] for r in rs)} |")
    return "\n".join(out)


def review_table(rows: list[dict]) -> str:
    out = ["| Condition | Runs | Seeded bugs | Bugs caught | Regressions (tests broken that passed before) | Findings reported "
           "| Patch applied exactly | Passed after review | Cost per run |",
           "|---|---|---|---|---|---|---|---|---|"]
    for name in TESTS["6 review session"]:
        rs = [r for r in rows if r["condition"] == name]
        if not rs:
            continue
        seeded = sum(len(r["bug_signatures"]) for r in rs) if CONDITIONS_BY_NAME[name].variant == "buggy" else 0
        caught = sum(len(r["bugs_caught"]) for r in rs) if seeded else 0
        findings = [len(r["findings"]) for r in rs if r.get("findings") is not None]
        out.append(f"| {name} | {len(rs)} | {seeded} | {caught if seeded else '–'} | {sum(len(r['regressions']) for r in rs)} "
                   f"| {sum(findings)} (in {len(findings)} parsed answers) | {frac(r.get('applied_exactly') for r in rs)} "
                   f"| {frac(r['passed'] for r in rs)} | ${mean(r['cost_usd'] for r in rs):.3f} |")
    return "\n".join(out)


def task_matrix(rows: list[dict]) -> str:
    names = [c for c in CONDITIONS_BY_NAME if any(r["condition"] == c for r in rows)]
    out = ["| Task | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
    for t in TASKS:
        cells = []
        for c in names:
            rs = [r for r in rows if r["condition"] == c and r["task"] == t]
            cells.append(frac(r["passed"] for r in rs) if rs else "")
        out.append(f"| {t} | " + " | ".join(cells) + " |")
    return "\n".join(out)


def failures(rows: list[dict]) -> str:
    out = []
    for r in rows:
        notes = []
        if not r["passed"]:
            notes.append(f"failed {len(r['hidden']['failed'])} hidden: {r['hidden']['failed'][:6]}"
                         + (f" error={str(r['hidden']['error'])[:120]}" if r["hidden"]["error"] else ""))
        if r["out_of_scope"]:
            notes.append(f"out of scope {r['out_of_scope']}")
        if r["status"] != "ok":
            notes.append(f"status {r['status']}")
        if r["peeked"]:
            notes.append(f"PEEKED {r['peeked'][:2]}")
        if not r["visible"]["ok"]:
            notes.append(f"visible suite failed {r['visible']['tail']}")
        if notes:
            out.append(f"- `{r['run_id']}` ({r['condition']}, {r['task']}): " + "; ".join(notes))
    return "\n".join(out) or "- none"


def render(tag: str) -> str:
    rows, errored = load(tag)
    spend_all = sum(r["cost_usd"] for r in rows + errored)
    spend_low = sum(r["cost_usd_low"] for r in rows + errored)
    versions = sorted({r["codex_version"] for r in rows})
    models = sorted({r["model"] for r in rows})
    parts = [f"# Results: tag `{tag}`\n",
             f"- Runs counted: {len(rows)}. Excluded for provider/harness errors: {len(errored)}.",
             f"- Spend: ${spend_all:.2f} upper bound (cache writes at the 12h price), ${spend_low:.2f} at the 30m price, "
             "errored runs included.",
             f"- Models: {', '.join(models)}. Codex: {', '.join(versions)}.",
             f"- Peeking at hidden tests or ~/.codex: {sum(bool(r['peeked']) for r in rows)} runs.\n"]
    for test, names in TESTS.items():
        parts.append(f"## Test {test}\n")
        if test.startswith("6"):
            parts.append(review_table(rows))
        else:
            parts.append(condition_table(rows, names))
            if test.startswith("2"):
                parts.append("\nRule tasks only:\n\n" + rule_table(rows))
            pairs = [(names[i], names[j]) for i in range(len(names)) for j in range(i + 1, len(names))]
            notes = [paired_note(rows, a, b) for a, b in pairs]
            parts.append("\n" + "\n".join(n for n in notes if n))
        parts.append("")
    parts += ["## Passes by task and condition\n", task_matrix(rows), "", "## Runs worth reading\n", failures(rows)]
    if errored:
        parts += ["", "## Excluded runs\n"] + [f"- `{r['run_id']}` ({r['condition']}, {r['task']}): {str(r['error'])[:200]}" for r in errored]
    return "\n".join(parts) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--out")
    args = ap.parse_args()
    text = render(args.tag)
    if args.out:
        (RESULTS.parent / args.out).write_text(text)
    print(text)


if __name__ == "__main__":
    main()
