# Results: tag `full-luna`, model `gpt-6-luna`

- Runs counted: 420. Excluded for provider/harness errors: 1.
- Spend: $4.20 upper bound (cache writes at the 12h price), $2.82 at the 30m price, errored runs included.
- Models: gpt-6-luna. Codex: codex-cli 0.169.0.
- Peeking at hidden tests or ~/.codex: 0 runs.

## Test 1 AGENTS.md size

| Condition | Runs | Passed | Rule followed | Out-of-scope runs | Median input tokens | Median output tokens | Cost (upper) | Cost per run | Cost per pass | Median wall s | Killed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| agents_none | 42 | 42/42 | 0/15 | 0 | 100,693 | 2,809 | $0.30 | $0.007 | $0.007 | 33 | 0 |
| base | 42 | 42/42 | 13/15 | 0 | 117,430 | 3,108 | $0.32 | $0.008 | $0.008 | 36 | 0 |
| agents_bloated | 42 | 42/42 | 15/15 | 0 | 184,440 | 3,730 | $0.42 | $0.010 | $0.010 | 45 | 0 |

- On the 14 tasks both ran: agents_none 42/42, base 42/42.
- On the 14 tasks both ran: agents_none 42/42, agents_bloated 42/42.
- On the 14 tasks both ran: base 42/42, agents_bloated 42/42.

## Test 2 32 KiB limit

| Condition | Runs | Passed | Rule followed | Out-of-scope runs | Median input tokens | Median output tokens | Cost (upper) | Cost per run | Cost per pass | Median wall s | Killed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| agents_none | 42 | 42/42 | 0/15 | 0 | 100,693 | 2,809 | $0.30 | $0.007 | $0.007 | 33 | 0 |
| base | 42 | 42/42 | 13/15 | 0 | 117,430 | 3,108 | $0.32 | $0.008 | $0.008 | 36 | 0 |
| rule_early | 15 | 15/15 | 15/15 | 0 | 166,163 | 3,134 | $0.16 | $0.010 | $0.010 | 36 | 0 |
| rule_late | 15 | 15/15 | 0/15 | 0 | 170,377 | 2,813 | $0.15 | $0.010 | $0.010 | 36 | 0 |

Rule tasks only:

| Condition | Runs (rule tasks) | Rule followed | AGENTS.md bytes loaded (median) | Loaded text contains the rule | Tasks passed |
|---|---|---|---|---|---|
| agents_none | 15 | 0/15 | 0 | 0/15 | 15/15 |
| base | 15 | 13/15 | 1,056 | 15/15 | 15/15 |
| rule_early | 15 | 15/15 | 32,768 | 15/15 | 15/15 |
| rule_late | 15 | 0/15 | 32,768 | 0/15 | 15/15 |

- On the 14 tasks both ran: agents_none 42/42, base 42/42.
- On the 5 tasks both ran: agents_none 15/15, rule_early 15/15.
- On the 5 tasks both ran: agents_none 15/15, rule_late 15/15.
- On the 5 tasks both ran: base 15/15, rule_early 15/15.
- On the 5 tasks both ran: base 15/15, rule_late 15/15.
- On the 5 tasks both ran: rule_early 15/15, rule_late 15/15.

## Test 3 prompt shape

| Condition | Runs | Passed | Rule followed | Out-of-scope runs | Median input tokens | Median output tokens | Cost (upper) | Cost per run | Cost per pass | Median wall s | Killed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_oneline | 42 | 42/42 | 13/15 | 2 | 127,474 | 2,382 | $0.32 | $0.008 | $0.008 | 35 | 0 |
| base | 42 | 42/42 | 13/15 | 0 | 117,430 | 3,108 | $0.32 | $0.008 | $0.008 | 36 | 0 |

- On the 14 tasks both ran: prompt_oneline 42/42, base 42/42.

## Test 4 plan first

| Condition | Runs | Passed | Rule followed | Out-of-scope runs | Median input tokens | Median output tokens | Cost (upper) | Cost per run | Cost per pass | Median wall s | Killed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| base | 42 | 42/42 | 13/15 | 0 | 117,430 | 3,108 | $0.32 | $0.008 | $0.008 | 36 | 0 |
| plan | 42 | 41/42 | 15/15 | 0 | 159,600 | 3,962 | $0.53 | $0.013 | $0.013 | 41 | 0 |

- On the 14 tasks both ran: base 42/42, plan 41/42.

## Test 5 reasoning effort

| Condition | Runs | Passed | Rule followed | Out-of-scope runs | Median input tokens | Median output tokens | Cost (upper) | Cost per run | Cost per pass | Median wall s | Killed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| effort_low | 42 | 42/42 | 11/15 | 0 | 92,159 | 1,449 | $0.25 | $0.006 | $0.006 | 20 | 0 |
| base | 42 | 42/42 | 13/15 | 0 | 117,430 | 3,108 | $0.32 | $0.008 | $0.008 | 36 | 0 |
| effort_high | 42 | 42/42 | 15/15 | 0 | 115,790 | 3,684 | $0.37 | $0.009 | $0.009 | 44 | 0 |

- On the 14 tasks both ran: effort_low 42/42, base 42/42.
- On the 14 tasks both ran: effort_low 42/42, effort_high 42/42.
- On the 14 tasks both ran: base 42/42, effort_high 42/42.

## Test 6 review session

| Condition | Runs | Seeded bugs | Bugs caught | Regressions (tests broken that passed before) | Findings reported | Patch applied exactly | Passed after review | Cost per run |
|---|---|---|---|---|---|---|---|---|
| review_same_buggy | 24 | 48 | 48 | 0 | 65 (in 24 parsed answers) | 24/24 | 24/24 | $0.020 |
| review_fresh_buggy | 24 | 48 | 48 | 0 | 62 (in 24 parsed answers) | 24/24 | 24/24 | $0.008 |
| review_same_clean | 24 | 0 | – | 0 | 24 (in 24 parsed answers) | 24/24 | 24/24 | $0.021 |
| review_fresh_clean | 24 | 0 | – | 0 | 28 (in 24 parsed answers) | 24/24 | 24/24 | $0.009 |

## Passes by task and condition

| Task | base | agents_none | agents_bloated | rule_early | rule_late | prompt_oneline | plan | effort_low | effort_high | review_same_buggy | review_fresh_buggy | review_same_clean | review_fresh_clean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t01-shipping-boundary | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |  |  |  |  |
| t02-bulk-discount | 3/3 | 3/3 | 3/3 |  |  | 3/3 | 3/3 | 3/3 | 3/3 |  |  |  |  |
| t03-inventory-release | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| t04-order-cancel | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |  |  |  |  |
| t05-csv-quoting | 3/3 | 3/3 | 3/3 |  |  | 3/3 | 3/3 | 3/3 | 3/3 |  |  |  |  |
| t06-business-days | 3/3 | 3/3 | 3/3 |  |  | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| t07-coupon-stacking | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| t08-cli-json | 3/3 | 3/3 | 3/3 |  |  | 3/3 | 3/3 | 3/3 | 3/3 |  |  |  |  |
| t09-slug-accents | 3/3 | 3/3 | 3/3 |  |  | 3/3 | 3/3 | 3/3 | 3/3 |  |  |  |  |
| t10-split-parcels | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| t11-invoice-tax | 3/3 | 3/3 | 3/3 |  |  | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| t12-search-query | 3/3 | 3/3 | 3/3 |  |  | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| t13-fifo-costing | 3/3 | 3/3 | 3/3 |  |  | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| t14-store-days | 3/3 | 3/3 | 3/3 |  |  | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |

## Runs worth reading

- `20261118-035030-prompt_oneline-t08-6470` (prompt_oneline, t08-cli-json): out of scope ['src/shoplib/reports.py']
- `20261118-040709-plan-t14-a3bf` (plan, t14-store-days): failed 1 hidden: ['test_offsets_in_timestamps']
- `20261118-053551-prompt_oneline-t08-e5ce` (prompt_oneline, t08-cli-json): out of scope ['src/shoplib/reports.py']

## Excluded runs

- `20261118-064447-review_fresh_clean-t14-94d5` (review_fresh_clean, t14-store-days): {"type": "error", "message": "Reconnecting... 2/5 (stream disconnected before completion: IO error: Connection reset by peer (os error 54))"}
