# Results: tag `pilot`, model `gpt-6.1-terra`

- Runs counted: 50. Excluded for provider/harness errors: 0.
- Spend: $3.78 upper bound (cache writes at the 12h price), $2.32 at the 30m price, errored runs included.
- Models: gpt-6.1-terra. Codex: codex-cli 0.169.0.
- Peeking at hidden tests or ~/.codex: 0 runs.

## Test 1 AGENTS.md size

| Condition | Runs | Passed | Rule followed | Out-of-scope runs | Median input tokens | Median output tokens | Cost (upper) | Cost per run | Cost per pass | Median wall s | Killed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| agents_none | 3 | 3/3 | 0/2 | 0 | 81,803 | 1,818 | $0.18 | $0.059 | $0.059 | 36 | 0 |
| base | 9 | 9/9 | 4/4 | 0 | 102,253 | 2,965 | $0.61 | $0.067 | $0.067 | 52 | 0 |
| agents_bloated | 3 | 3/3 | 2/2 | 0 | 112,972 | 1,696 | $0.23 | $0.076 | $0.076 | 30 | 0 |

- On the 3 tasks both ran: agents_none 3/3, base 3/3.
- On the 3 tasks both ran: agents_none 3/3, agents_bloated 3/3.
- On the 3 tasks both ran: base 3/3, agents_bloated 3/3.

## Test 2 32 KiB limit

| Condition | Runs | Passed | Rule followed | Out-of-scope runs | Median input tokens | Median output tokens | Cost (upper) | Cost per run | Cost per pass | Median wall s | Killed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| agents_none | 3 | 3/3 | 0/2 | 0 | 81,803 | 1,818 | $0.18 | $0.059 | $0.059 | 36 | 0 |
| base | 9 | 9/9 | 4/4 | 0 | 102,253 | 2,965 | $0.61 | $0.067 | $0.067 | 52 | 0 |
| rule_early | 2 | 2/2 | 2/2 | 0 | 131,672 | 1,540 | $0.15 | $0.077 | $0.077 | 35 | 0 |
| rule_late | 2 | 2/2 | 0/2 | 0 | 94,202 | 1,194 | $0.14 | $0.072 | $0.072 | 25 | 0 |

Rule tasks only:

| Condition | Runs (rule tasks) | Rule followed | AGENTS.md bytes loaded (median) | Loaded text contains the rule | Tasks passed |
|---|---|---|---|---|---|
| agents_none | 2 | 0/2 | 0 | 0/2 | 2/2 |
| base | 4 | 4/4 | 1,056 | 4/4 | 4/4 |
| rule_early | 2 | 2/2 | 32,768 | 2/2 | 2/2 |
| rule_late | 2 | 0/2 | 32,768 | 0/2 | 2/2 |

- On the 3 tasks both ran: agents_none 3/3, base 3/3.
- On the 1 tasks both ran: agents_none 1/1, rule_early 1/1.
- On the 1 tasks both ran: agents_none 1/1, rule_late 1/1.
- On the 2 tasks both ran: base 2/2, rule_early 2/2.
- On the 2 tasks both ran: base 2/2, rule_late 2/2.
- On the 2 tasks both ran: rule_early 2/2, rule_late 2/2.

## Test 3 prompt shape

| Condition | Runs | Passed | Rule followed | Out-of-scope runs | Median input tokens | Median output tokens | Cost (upper) | Cost per run | Cost per pass | Median wall s | Killed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_oneline | 14 | 14/14 | 5/5 | 0 | 83,551 | 1,466 | $0.86 | $0.061 | $0.061 | 30 | 0 |
| base | 9 | 9/9 | 4/4 | 0 | 102,253 | 2,965 | $0.61 | $0.067 | $0.067 | 52 | 0 |

- On the 9 tasks both ran: prompt_oneline 9/9, base 9/9.

## Test 4 plan first

| Condition | Runs | Passed | Rule followed | Out-of-scope runs | Median input tokens | Median output tokens | Cost (upper) | Cost per run | Cost per pass | Median wall s | Killed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| base | 9 | 9/9 | 4/4 | 0 | 102,253 | 2,965 | $0.61 | $0.067 | $0.067 | 52 | 0 |
| plan | 3 | 3/3 | 3/3 | 0 | 157,362 | 2,681 | $0.35 | $0.116 | $0.116 | 44 | 0 |

- On the 3 tasks both ran: base 3/3, plan 3/3.

## Test 5 reasoning effort

| Condition | Runs | Passed | Rule followed | Out-of-scope runs | Median input tokens | Median output tokens | Cost (upper) | Cost per run | Cost per pass | Median wall s | Killed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| effort_low | 6 | 6/6 | 2/2 | 0 | 88,158 | 2,042 | $0.36 | $0.060 | $0.060 | 34 | 0 |
| base | 9 | 9/9 | 4/4 | 0 | 102,253 | 2,965 | $0.61 | $0.067 | $0.067 | 52 | 0 |
| effort_high | 2 | 2/2 | 2/2 | 0 | 198,735 | 6,430 | $0.21 | $0.103 | $0.103 | 117 | 0 |

- On the 6 tasks both ran: effort_low 6/6, base 6/6.
- On the 2 tasks both ran: effort_low 2/2, effort_high 2/2.
- On the 2 tasks both ran: base 2/2, effort_high 2/2.

## Test 6 review session

| Condition | Runs | Seeded bugs | Bugs caught | Regressions (tests broken that passed before) | Findings reported | Patch applied exactly | Passed after review | Cost per run |
|---|---|---|---|---|---|---|---|---|
| review_same_buggy | 2 | 4 | 4 | 0 | 4 (in 2 parsed answers) | 2/2 | 2/2 | $0.166 |
| review_fresh_buggy | 2 | 4 | 4 | 0 | 5 (in 2 parsed answers) | 2/2 | 2/2 | $0.062 |
| review_same_clean | 1 | 0 | – | 0 | 1 (in 1 parsed answers) | 0/1 | 1/1 | $0.183 |
| review_fresh_clean | 1 | 0 | – | 0 | 1 (in 1 parsed answers) | 1/1 | 1/1 | $0.060 |

## Passes by task and condition

| Task | base | agents_none | agents_bloated | rule_early | rule_late | prompt_oneline | plan | effort_low | effort_high | review_same_buggy | review_fresh_buggy | review_same_clean | review_fresh_clean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t01-shipping-boundary | 1/1 |  |  | 1/1 | 1/1 | 1/1 |  |  |  |  |  |  |  |
| t02-bulk-discount | 1/1 | 1/1 | 1/1 |  |  | 1/1 |  |  |  |  |  |  |  |
| t03-inventory-release |  |  |  |  |  | 1/1 |  |  |  |  |  |  |  |
| t04-order-cancel | 1/1 | 1/1 | 1/1 |  |  | 1/1 | 1/1 |  |  |  |  |  |  |
| t05-csv-quoting |  |  |  |  |  | 1/1 |  |  |  |  |  |  |  |
| t06-business-days |  |  |  |  |  | 1/1 |  |  |  | 1/1 | 1/1 |  |  |
| t07-coupon-stacking | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |  |  | 1/1 | 1/1 |
| t08-cli-json |  |  |  |  |  | 1/1 |  |  |  |  |  |  |  |
| t09-slug-accents |  |  |  |  |  | 1/1 |  |  |  |  |  |  |  |
| t10-split-parcels | 1/1 |  |  |  |  | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |  |  |
| t11-invoice-tax | 1/1 |  |  |  |  | 1/1 |  | 1/1 |  |  |  |  |  |
| t12-search-query | 1/1 |  |  |  |  | 1/1 |  | 1/1 |  |  |  |  |  |
| t13-fifo-costing | 1/1 |  |  |  |  | 1/1 |  | 1/1 |  |  |  |  |  |
| t14-store-days | 1/1 |  |  |  |  | 1/1 |  | 1/1 |  |  |  |  |  |

## Runs worth reading

- none
