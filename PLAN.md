# PLAN: Codex best-practices lab

Stage 1 (build and pilot) is done. Nothing below has been run at full scale. **The full run needs your
approval.**

## 1. What was built

- **Target repo** (`target/`): `shoplib`, a small Python order-handling library with docs, visible tests and
  14 tasks. t01–t10 are small fixes and features. t11–t14 are harder, spec-heavy functions (invoice tax with
  largest-remainder coupon split, a search query language, FIFO costing with returns, store days across
  time zones). I added them after the first pilot rounds hit a 100% pass rate.
- **Hidden tests** (`hidden/`): 9 to 24 tests per task, plus a rule test for 5 tasks. They are copied into a
  temporary folder at grading time and never placed in, or above, a working copy. No model grades anything.
- **Harness** (`harness/`): one fresh working copy and one fresh `CODEX_HOME` per run; `codex exec --json`;
  live spend guard; stall detection; one record per run in `results/runs.jsonl`; raw events, Codex rollout
  and diff per run in `results/raw/<run_id>/`; `--resume`; a hard `--cap` per tag.
- **Self-test** (`python -m harness.selftest`, no model calls): passes, 93 checks. It shows that:
  - every task fails its hidden tests on the untouched repo and passes them with a reference solution;
  - the rule test tells `ShopError` apart from a bare `ValueError`;
  - each seeded bug breaks its own set of hidden tests while still passing the visible suite;
  - the out-of-scope detector flags only the out-of-scope file, including after the agent commits;
  - the event parser reads a real recorded run;
  - the AGENTS.md variants have the sizes and rule positions claimed;
  - the cost function and the cap check are right.

## 2. What the probe verified against the design

| Design assumption | Installed codex-cli 0.169.0 | Status |
|---|---|---|
| Model via `-m` | Works; the rollout's `turn_context` records the model | verified |
| Effort via `-c model_reasoning_effort="…"` | Works for low/medium/high; recorded per turn in every run | verified |
| Token use in `turn.completed` | Yes, `usage` holds `input_tokens`, `cached_input_tokens`, **`cache_write_input_tokens`** (not in the docs' example), `output_tokens` and `reasoning_output_tokens` | verified, with the extra field |
| AGENTS.md stops loading at 32 KiB | A single 40 KiB file is **cut at exactly 32,768 bytes**, mid-sentence, with no warning in the event stream | verified (4 runs) |
| Plan mode drivable non-interactively | No. `/plan` is an interactive collaboration mode, and `exec` always runs in `default` mode | test 4 approximated (see section 5) |
| `CODEX_HOME` isolates the user's settings | Yes. `~/.codex/AGENTS.md`, `config.toml` and `auth.json` are byte-identical after about 100 runs, and no file in `~/.codex` mentions the lab. One temp lock file in `~/.codex/tmp/` has a timestamp matching a run start; the desktop app (running throughout) made an identical one before the CLI was installed, so it is most likely the app's. Not proven | verified with that caveat |

Other things the probe found:

- **Login shell.** Codex runs commands through a login shell, which put Homebrew's Python ahead of the lab
  venv. `-c allow_login_shell=false` fixes this; checked in a run.
- **Resume.** `codex exec resume <id>` does not accept `-s`, so the sandbox is set with
  `-c sandbox_mode=...`; checked in a run.
- **Cache-write pricing.** The pricing page lists cache-write prices (30-minute and 12-hour). Codex does
  not say which one applies. Costs are recorded both ways: the cap uses the higher 12-hour price, and the
  lower figure is roughly 60% of it.

## 3. What the pilot showed

96 runs, tag `pilot`, $4.09 upper bound ($2.53 at the lower cache-write price), under the $5 cap enforced in
code. 5 Luna runs stalled: the event stream stopped and nothing came for 15+ minutes, twice before the first
response. I relabelled these as provider errors after reading their events. 91 runs are counted.
Reports: `results/report-pilot-gpt-6.1-terra.md` and `results/report-pilot-gpt-6-luna.md`.

**Headline: every one of the 91 counted runs passed its hidden tests.** That covers both models, all 14
tasks and every condition. The pilot cells are small (often 2–3 runs each), so everything below is
direction, not a result.

| Advice | Pilot signal (gpt-6.1-terra unless noted) |
|---|---|
| 1. AGENTS.md, short | No pass-rate difference. The bloated file (+25 KiB) raised median input tokens 35% and cost 32% on the same 3 tasks. No file versus the short file: no difference in tokens or cost. |
| 2. 32 KiB limit | Clear and mechanical. A rule placed before the cut was followed 2/2; after it, 0/2 (the rule is not in the loaded text). With the short file it was followed 9/9 Terra and 5/5 Luna; with no file, 0/7 across both models. The model never used `ShopError` unless told to. |
| 3. Four-part prompt | No pass-rate difference (one-line 14/14). One out-of-scope edit in 28 one-line runs (Luna, t08: put `to_json` in `reports.py`). Four-part prompts: 0 out-of-scope edits. |
| 4. Plan first | No pass-rate difference; +69% cost on the same 3 tasks. |
| 5. Reasoning effort | No pass-rate difference. Low versus medium: −23% cost, −38% median wall time on the same 6 tasks. High versus medium: +41% cost and almost double the wall time (2 tasks). |
| 6. Fresh-session review | Both caught all 4 seeded bugs in 2 runs each. Same-session cost 2.7× as much ($0.166 against $0.062), because it carries the session that applied the patch. On bug-free code, both reported one finding (unknown coupon kinds are silently ignored, which the spec does not address). Both also flagged the real, pre-existing `shipping_cost` boundary bug without being asked. |

Behaviour worth a sentence in the post: with no AGENTS.md, Terra went looking for one in every parent
folder up to `/Users` (run `20261117-173620-agents_none-t07-caa9`).

## 4. Model choice

- **gpt-6.1-terra (primary).** The mid tier, at $0.07 a run on average. The best-practices page recommends
  GPT-6.1 Sol, but Sol costs twice as much and Terra already passes everything, so Sol would only add
  cost.
- **gpt-6-luna (second model).** At $0.008 a run, the whole matrix costs about $4. It is the weaker model
  and showed the only scope violation, so it is the best remaining chance of a pass-rate difference. It
  also stalls now and then; stalls are now detected after 5 minutes of silence and redone by `--resume`.

## 5. Changes from the design

- **Tasks.** 14 instead of about 10; t11–t14 were added because t01–t10 were at 100%. They did not break
  the ceiling either.
- **Test 4 is kept, but approximated.** Plan mode itself cannot be driven from `codex exec`. The `plan`
  condition is a read-only planning turn ("reply with a numbered plan, do not edit") followed by
  `codex exec resume` with "Now implement the plan". The guide also suggests asking for a plan explicitly.
  No files changed during any planning turn (checked in all 3 runs).
- **Shared baseline.** Every test changes one thing from `base`: short AGENTS.md, four-part prompt, medium
  effort, no plan step. Tests 1, 3, 4 and 5 share the `base` cells. That gives 140 cells per repeat instead
  of the about 165 a separate baseline per test would need.
- **Test 2 control.** It uses the `agents_none` and `base` cells as its no-rule and rule-loaded controls.
- **Test 6 design.** Seeded-bug and bug-free versions of 8 tasks (t03, t06, t07, t10–t14). "Same session":
  the session that applied the patch (told to apply it and run the tests) is then asked to review it.
  "Fresh session": a new session reviews the same uncommitted patch. Bugs caught = seeded bugs whose
  signature tests pass after review. False alarms = findings on bug-free code, plus any test the review
  broke.
- **Errors.** Stalls (5 minutes with no output) count as provider errors, which are excluded and redone.
  Timeouts (15 minutes) and runs killed by the per-run spend cap count as failures of the condition.

## 6. Full run matrix (3 repeats per condition)

| Condition | Tasks | Runs per repeat |
|---|---|---|
| base, agents_none, agents_bloated, prompt_oneline, plan, effort_low, effort_high | all 14 | 98 |
| rule_early, rule_late | 5 rule tasks | 10 |
| review_{same,fresh}_{buggy,clean} | 8 seeded tasks | 32 |
| **Total** | | **140 × 3 = 420 per model** |

The pilot runs are not reused; the full run starts clean under a new tag per model.

## 7. Projected cost and duration

Projected from pilot cost per condition; conditions with no pilot runs use multiples of `base`.

| | Runs | Cost (upper / lower cache price) | Duration, sequential |
|---|---|---|---|
| gpt-6.1-terra | 420 | about $36 / $22 | about 7 h |
| gpt-6-luna | 420 | about $4.40 / $3 | about 6 h, plus stall retries |
| **Both** | 840 | **about $41 / $25** | about 13 h, or about 7 h with `--jobs 2` |

Sequential is the default, per the standing rule. `--jobs 2` halves the time and works, since each run has
its own `CODEX_HOME` and working copy, but it doubles the load on the shared API limits. Your call.

## 8. Proposed hard cap

- `--tag full-terra --cap 45 --run-cap 0.75`, and `--tag full-luna --cap 6 --run-cap 0.15`: **$51 in total**.
- How it holds: a run starts only if everything already spent, plus every run in flight, plus its own kill
  limit fits under the cap. A run is killed the moment its own upper-bound spend passes `--run-cap`.
- This is above the design's $15–40 estimate because of the second model and 14 rather than 10 tasks.
  Terra alone needs a $45 cap.

## 9. The decision that matters before spending

The pilot says pass rate will probably stay at or near 100% everywhere. If so, the post's findings are:

- what each piece of advice costs (tokens, dollars, time);
- what it changes in behaviour (rule-following, scope);
- the 32 KiB cut, which silently drops rules.

They are not "which advice makes Codex succeed more". That is an honest, publishable result ("on
well-specified tasks, none of this changed whether the work was right; here is what it changed instead"),
but it is a different post from the angle in the brief. Making pass rate move would take tasks where key
information is not discoverable from the repo: under-specified tasks whose only source of truth is the
AGENTS.md or the prompt. That would be a redesign, and I have not built it.

**Recommendation:** approve the full run as specified (both models, $51 cap) and frame the post around cost
and behaviour, with the ceiling stated plainly.

## 10. Verified and not verified

- **Verified:**
  - the self-test passes;
  - flags, events, resume, sandbox switch and truncation behave as described (from real runs);
  - every pilot run used the intended model and effort (from rollouts);
  - no run read the hidden tests or `~/.codex` (no command matched; one false positive in round 1 was fixed);
  - the $5 cap held ($4.09 spent).
- **Not verified:**
  - which cache-write price OpenAI actually charges (costs are given as a range);
  - whether the `~/.codex/tmp` lock file came from the desktop app or the CLI;
  - whether any effect holds beyond 2–3 pilot runs per cell;
  - plan mode proper (approximated, see section 5).
