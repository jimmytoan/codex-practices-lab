# Derived findings (full run)

Runs: 840 counted (Terra 420, Luna 420). Computed by `python -m harness.analysis`.

## 1. Each condition against `base` (all conditions below ran all 14 tasks, 3 times)

| Model | Condition | Passed | Median input tokens | vs base | Median output tokens | vs base | Mean cost | vs base | Median wall s | vs base |
|---|---|---|---|---|---|---|---|---|---|---|
| Terra | base | 42/42 | 92,559 | +0% | 2,222 | +0% | $0.0650 | +0% | 39 | +0% |
| Terra | agents_none | 42/42 | 81,705 | -12% | 1,786 | -20% | $0.0610 | -6% | 36 | -8% |
| Terra | agents_bloated | 42/42 | 126,768 | +37% | 2,102 | -5% | $0.0827 | +27% | 46 | +18% |
| Terra | prompt_oneline | 42/42 | 97,720 | +6% | 1,618 | -27% | $0.0620 | -5% | 36 | -8% |
| Terra | plan | 42/42 | 155,143 | +68% | 2,352 | +6% | $0.1082 | +67% | 53 | +36% |
| Terra | effort_low | 42/42 | 79,730 | -14% | 1,334 | -40% | $0.0538 | -17% | 33 | -15% |
| Terra | effort_high | 42/42 | 108,052 | +17% | 2,917 | +31% | $0.0773 | +19% | 66 | +69% |
| Luna | base | 42/42 | 117,430 | +0% | 3,108 | +0% | $0.0077 | +0% | 36 | +0% |
| Luna | agents_none | 42/42 | 100,693 | -14% | 2,809 | -10% | $0.0071 | -7% | 33 | -8% |
| Luna | agents_bloated | 42/42 | 184,440 | +57% | 3,730 | +20% | $0.0100 | +30% | 45 | +25% |
| Luna | prompt_oneline | 42/42 | 127,474 | +9% | 2,382 | -23% | $0.0076 | -1% | 35 | -3% |
| Luna | plan | 41/42 | 159,600 | +36% | 3,962 | +27% | $0.0125 | +63% | 41 | +14% |
| Luna | effort_low | 42/42 | 92,159 | -22% | 1,449 | -53% | $0.0059 | -23% | 20 | -44% |
| Luna | effort_high | 42/42 | 115,790 | -1% | 3,684 | +19% | $0.0087 | +14% | 44 | +22% |

## 2. Same, hard tasks t11-t14 only

| Model | Condition | Passed | Mean cost | vs base | Median wall s |
|---|---|---|---|---|---|
| Terra | base | 12/12 | $0.0775 | +0% | 68 |
| Terra | agents_none | 12/12 | $0.0690 | -11% | 55 |
| Terra | agents_bloated | 12/12 | $0.0961 | +24% | 68 |
| Terra | prompt_oneline | 12/12 | $0.0749 | -3% | 51 |
| Terra | plan | 12/12 | $0.1182 | +52% | 65 |
| Terra | effort_low | 12/12 | $0.0605 | -22% | 42 |
| Terra | effort_high | 12/12 | $0.0966 | +25% | 98 |
| Luna | base | 12/12 | $0.0097 | +0% | 58 |
| Luna | agents_none | 12/12 | $0.0093 | -5% | 52 |
| Luna | agents_bloated | 12/12 | $0.0126 | +29% | 64 |
| Luna | prompt_oneline | 12/12 | $0.0101 | +3% | 60 |
| Luna | plan | 11/12 | $0.0153 | +57% | 69 |
| Luna | effort_low | 12/12 | $0.0071 | -27% | 31 |
| Luna | effort_high | 12/12 | $0.0116 | +20% | 81 |

## 3. Commands that touch AGENTS.md

`mentions` = any shell command containing `AGENTS.md` (mostly `rg --files -g AGENTS.md`, looking for nested files). `reads` = a command that prints its content (cat/tail/head/sed/rg -n ... AGENTS.md). `outside repo` = looked for AGENTS.md above the repo root.

| Model | Condition | Runs | mentions | reads | outside repo |
|---|---|---|---|---|---|
| Terra | agents_none | 42 | 42 | 0 | 8 |
| Terra | base | 42 | 33 | 13 | 0 |
| Terra | agents_bloated | 42 | 41 | 2 | 0 |
| Terra | rule_early | 15 | 15 | 1 | 0 |
| Terra | rule_late | 15 | 15 | 4 | 0 |
| Terra | prompt_oneline | 42 | 39 | 19 | 0 |
| Terra | plan | 42 | 22 | 9 | 0 |
| Terra | effort_low | 42 | 7 | 0 | 0 |
| Terra | effort_high | 42 | 38 | 23 | 0 |
| Luna | agents_none | 42 | 11 | 0 | 0 |
| Luna | base | 42 | 1 | 1 | 0 |
| Luna | agents_bloated | 42 | 0 | 0 | 0 |
| Luna | rule_early | 15 | 0 | 0 | 0 |
| Luna | rule_late | 15 | 0 | 0 | 0 |
| Luna | prompt_oneline | 42 | 6 | 0 | 0 |
| Luna | plan | 42 | 0 | 0 | 0 |
| Luna | effort_low | 42 | 0 | 0 | 0 |
| Luna | effort_high | 42 | 1 | 0 | 0 |

## 4. Rule placed after byte 32,768: read the file itself vs followed the rule

| Model | Read AGENTS.md content | Followed | Runs |
|---|---|---|---|
| Terra | False | False | 11 |
| Terra | True | True | 4 |
| Luna | False | False | 15 |

Terra rule_late runs that followed the rule: 20261117-214459-rule_late-t03-0c71, 20261117-235807-rule_late-t07-f0b9, 20261117-235851-rule_late-t10-d83d, 20261118-015656-rule_late-t04-a458

## 5. Rule in the loaded AGENTS.md but not followed

| Run | Model | Condition | Task | ShopError anywhere in diff | `raise ValueError` lines added |
|---|---|---|---|---|---|
| `20261118-040802-effort_low-t01-6d0c` | Luna | effort_low | t01-shipping-boundary | False | 0 |
| `20261118-040853-effort_low-t04-2580` | Luna | effort_low | t04-order-cancel | False | 4 |
| `20261118-045630-base-t01-78a6` | Luna | base | t01-shipping-boundary | False | 0 |
| `20261118-053249-prompt_oneline-t01-5e54` | Luna | prompt_oneline | t01-shipping-boundary | False | 0 |
| `20261118-055338-effort_low-t01-ccb5` | Luna | effort_low | t01-shipping-boundary | False | 0 |
| `20261118-064540-base-t01-a1e7` | Luna | base | t01-shipping-boundary | False | 0 |
| `20261118-072205-prompt_oneline-t01-226d` | Luna | prompt_oneline | t01-shipping-boundary | False | 0 |
| `20261118-074525-effort_low-t01-df45` | Luna | effort_low | t01-shipping-boundary | False | 0 |

Rule followed when it was in the loaded text, all conditions:

- Luna, rule tasks other than t01: 119/120
- Luna, t01 only: 14/21
- Terra, rule tasks other than t01: 120/120
- Terra, t01 only: 21/21

## 6. Review: same session vs fresh session

| Model | Condition | Runs | Bugs caught | Mean cost | Median wall s | Findings | Findings per run |
|---|---|---|---|---|---|---|---|
| Terra | review_same_buggy | 24 | 48/48 | $0.1739 | 67 | 77 | 3.21 |
| Terra | review_fresh_buggy | 24 | 48/48 | $0.0657 | 44 | 78 | 3.25 |
| Terra | review_same_clean | 24 | - | $0.1699 | 67 | 35 | 1.46 |
| Terra | review_fresh_clean | 24 | - | $0.0696 | 50 | 42 | 1.75 |
| Terra | same / fresh cost ratio | | | 2.54x | | | |
| Luna | review_same_buggy | 24 | 48/48 | $0.0197 | 68 | 65 | 2.71 |
| Luna | review_fresh_buggy | 24 | 48/48 | $0.0078 | 39 | 62 | 2.58 |
| Luna | review_same_clean | 24 | - | $0.0212 | 67 | 24 | 1.00 |
| Luna | review_fresh_clean | 24 | - | $0.0093 | 51 | 28 | 1.17 |
| Luna | same / fresh cost ratio | | | 2.39x | | | |

Findings on the bug-free patches, sorted by keyword (one finding can only land in the first matching group):

| Model | Session | Findings | ShopError / ValueError rule | shipping_cost tier bug (pre-existing) | unknown coupon kind (spec silent) | other (hardening beyond the spec) |
|---|---|---|---|---|---|---|
| Terra | same | 35 | 14 | 3 | 3 | 15 |
| Terra | fresh | 42 | 16 | 3 | 3 | 20 |
| Luna | same | 23 | 11 | 1 | 3 | 8 |
| Luna | fresh | 28 | 18 | 1 | 3 | 6 |

Note: the bug-free patches for t11-t14 raise a bare ValueError, which the repo's AGENTS.md forbids, and t10's touches code next to the pre-existing shipping_cost boundary bug (task t01). Findings in those two groups are correct, not false alarms.

## 7. Failed runs and out-of-scope edits

- `20261118-035030-prompt_oneline-t08-6470` Luna prompt_oneline t08-cli-json: passed=True failed=[] out_of_scope=['src/shoplib/reports.py']
- `20261118-040709-plan-t14-a3bf` Luna plan t14-store-days: passed=False failed=['test_offsets_in_timestamps'] out_of_scope=[]
- `20261118-053551-prompt_oneline-t08-e5ce` Luna prompt_oneline t08-cli-json: passed=True failed=[] out_of_scope=['src/shoplib/reports.py']

## 8. Totals

- Terra: 420 runs, passed 420, spend $35.40 upper / $21.60 lower, input tokens 54,455,817, output tokens 1,123,150, wall 5.9 h
- Luna: 420 runs, passed 419, spend $4.19 upper / $2.81 lower, input tokens 69,034,411, output tokens 1,707,957, wall 5.3 h
