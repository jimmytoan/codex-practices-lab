# Results report: Codex best-practices lab, full run

Run 17–18 November 2026 with codex-cli 0.169.0. 840 runs counted: 420 on `gpt-6.1-terra` (tag `full-terra`)
and 420 on `gpt-6-luna` (tag `full-luna`). That is 3 repeats of 140 cells (13 conditions over 14 tasks; see
PLAN.md section 6). One Luna run was excluded as a provider error ("Reconnecting... 2/5, connection reset by
peer") and redone with `--resume`.

Every number in the blog draft comes from one of these files, all generated from `runs.jsonl` and
`raw/<run_id>/`:

| File | What it holds | Regenerate with |
|---|---|---|
| `report-full-terra.md` | per-test tables for Terra: pass, rule-following, scope, tokens, cost, time, review | `python -m harness.report --tag full-terra --model gpt-6.1-terra --out results/report-full-terra.md` |
| `report-full-luna.md` | the same for Luna | `python -m harness.report --tag full-luna --model gpt-6-luna --out results/report-full-luna.md` |
| `findings-full.md` | changes against `base`, AGENTS.md reading behaviour, the rule_late cross-tab, rule misses, review cost ratio and finding categories, failures, totals | `python -m harness.analysis > results/findings-full.md` |
| `report-pilot-*.md` | the pilot (96 runs, not part of the full results) | see PLAN.md |
| `selftest-before-full.txt` | self-test output from just before the full run | `python -m harness.selftest` |

## Headline numbers

- **Pass rate.** 839 of 840 runs passed every hidden test: Terra 420/420, Luna 419/420. The one failure is
  `20261118-040709-plan-t14-a3bf`. (`findings-full.md` §7–8)
- **Spend.**
  - Terra: $35.40 upper bound, $21.60 at the lower cache-write price.
  - Luna: $4.20 upper, $2.82 lower, including the excluded run.
  - Pilot: $4.09 upper.
  (report headers)
- **Rule-following.** The AGENTS.md rule ("raise `ShopError`, not a bare `ValueError`") was checked on 5 tasks
  × 3 repeats per condition. (reports, test 2)

  | Condition | Terra | Luna |
  |---|---|---|
  | No file | 0/15 | 0/15 |
  | Short file | 15/15 | 13/15 |
  | Rule before the 32 KiB cut | 15/15 | 15/15 |
  | Rule after the cut | 4/15 | 0/15 |

  - **Truncation.** The 40 KiB file was loaded as exactly 32,768 bytes in every run, cut mid-sentence and with
    no notice in the loaded text (rollouts; `report-full-*.md` test 2).
  - **The 4 Terra runs after the cut.** They are the 4 that printed the file's content with a shell command
    (`tail -80 AGENTS.md` and similar). The other 11 did not. (`findings-full.md` §4)
  - **Luna's misses.** 7 of Luna's 8 misses with the rule loaded are on t01. That task's fix touches no
    `raise` line, and the rule says "in any code you write or change", so this is partly a weakness of the
    t01 rule test. On the other 4 rule tasks Luna followed it 119/120. (`findings-full.md` §5)
- **Cost and time against `base`.** (`findings-full.md` §1)

  | Condition | Terra cost | Terra time | Luna cost | Luna time |
  |---|---|---|---|---|
  | Plan first | +67% | +36% | +63% | +14% |
  | Bloated AGENTS.md | +27% (input tokens +37%) | | +30% (input tokens +57%) | |
  | Low effort | −17% | −15% | −23% | −44% |
  | High effort | +19% | +69% | +14% | +22% |
  | No AGENTS.md | −6% | | −7% | |
  | One-line prompt | −5% | | −1% | |

- **Scope.** 2 out-of-scope edits in 840 runs, both Luna, one-line prompt, task t08: each added `to_json`
  to `reports.py`. (`findings-full.md` §7)
- **Review.** Same-session and fresh-session review both caught all 48 seeded bugs, on both models.
  Same-session cost 2.54× as much on Terra and 2.39× on Luna. On the bug-free patches, the reviewers reported
  findings per run as follows (`findings-full.md` §6):

  | | Same session | Fresh session |
  |---|---|---|
  | Terra | 1.46 | 1.75 |
  | Luna | 1.00 | 1.17 |

  Most of those findings were correct rather than false alarms: rule violations in my reference patches, and
  the pre-existing `shipping_cost` bug. The rest were hardening beyond the spec. No review broke a test.

## Transcript checks behind the stories

- **The one failure** (`20261118-040709-plan-t14-a3bf`, Luna, plan, t14).
  - The plan said "convert them to shop-local time".
  - The code did `parsed + timedelta(hours=utc_offset_hours)`, adding the shop offset to the timestamp's own
    wall-clock time.
  - Its own test expects a refund at `2026-11-20T03:59:00+08:00` on store day 2026-11-20. The spec says
    2026-11-19, because the day starts at 04:00 local.
  - Its 25 tests passed, and its final message says it converts each timestamp to the shop's local time.
  - Checked in `diff.patch`, `events-1.jsonl`, `events-2.jsonl` and `record.json` (`plan_text`).
- **Reading the truncated file** (`20261117-214459-rule_late-t03-0c71`, Terra). It ran
  `tail -80 AGENTS.md`, then `rg -n 'ShopError|Error handling' src tests AGENTS.md`, then wrote "The
  repository's error rule also requires `ShopError`". The loaded instructions in its rollout end with
  "Keep pull requests small enough to" and no truncation note.
- **Searching above the repo** (`20261117-211930-agents_none-t03-bc20`, Terra, no AGENTS.md). It ran
  `for path in /AGENTS.md /Users/AGENTS.md /Users/jimmynguyen/AGENTS.md ...`, walking up from the filesystem
  root to the working copy (8 of 42 such runs).
- **The pre-existing bug.** Reviewers on t10 reported the `shipping_cost` boundary bug and left it alone ("It
  remains unchanged as requested"). That is the t01 bug, which is in the base repo.

## Limits

- The ceiling: almost everything passed, so pass rate could not separate the conditions.
- One model family: two OpenAI models through Codex.
- 14 small Python tasks in one repo.
- 3 repeats per cell.
- Codex 0.169.0 only.
- Plan mode was approximated by a read-only planning turn followed by `codex exec resume`.
- Costs are token counts × list price, given as a range because Codex does not say which cache-write price
  applies.
- Finding categories come from keywords.
- The hard tasks t11–t14 were added after the pilot.
