# Results: tag `full-terra`, model `gpt-6.1-terra`

- Runs counted: 420. Excluded for provider/harness errors: 0.
- Spend: $35.40 upper bound (cache writes at the 12h price), $21.60 at the 30m price, errored runs included.
- Models: gpt-6.1-terra. Codex: codex-cli 0.169.0.
- Peeking at hidden tests or ~/.codex: 0 runs.

## Test 1 AGENTS.md size

| Condition | Runs | Passed | Rule followed | Out-of-scope runs | Median input tokens | Median output tokens | Cost (upper) | Cost per run | Cost per pass | Median wall s | Killed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| agents_none | 42 | 42/42 | 0/15 | 0 | 81,705 | 1,786 | $2.56 | $0.061 | $0.061 | 36 | 0 |
| base | 42 | 42/42 | 15/15 | 0 | 92,559 | 2,222 | $2.73 | $0.065 | $0.065 | 39 | 0 |
| agents_bloated | 42 | 42/42 | 15/15 | 0 | 126,768 | 2,102 | $3.47 | $0.083 | $0.083 | 46 | 0 |

- On the 14 tasks both ran: agents_none 42/42, base 42/42.
- On the 14 tasks both ran: agents_none 42/42, agents_bloated 42/42.
- On the 14 tasks both ran: base 42/42, agents_bloated 42/42.

## Test 2 32 KiB limit

| Condition | Runs | Passed | Rule followed | Out-of-scope runs | Median input tokens | Median output tokens | Cost (upper) | Cost per run | Cost per pass | Median wall s | Killed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| agents_none | 42 | 42/42 | 0/15 | 0 | 81,705 | 1,786 | $2.56 | $0.061 | $0.061 | 36 | 0 |
| base | 42 | 42/42 | 15/15 | 0 | 92,559 | 2,222 | $2.73 | $0.065 | $0.065 | 39 | 0 |
| rule_early | 15 | 15/15 | 15/15 | 0 | 120,301 | 1,862 | $1.23 | $0.082 | $0.082 | 34 | 0 |
| rule_late | 15 | 15/15 | 4/15 | 0 | 122,994 | 1,808 | $1.24 | $0.083 | $0.083 | 30 | 0 |

Rule tasks only:

| Condition | Runs (rule tasks) | Rule followed | AGENTS.md bytes loaded (median) | Loaded text contains the rule | Tasks passed |
|---|---|---|---|---|---|
| agents_none | 15 | 0/15 | 0 | 0/15 | 15/15 |
| base | 15 | 15/15 | 1,056 | 15/15 | 15/15 |
| rule_early | 15 | 15/15 | 32,768 | 15/15 | 15/15 |
| rule_late | 15 | 4/15 | 32,768 | 0/15 | 15/15 |

- On the 14 tasks both ran: agents_none 42/42, base 42/42.
- On the 5 tasks both ran: agents_none 15/15, rule_early 15/15.
- On the 5 tasks both ran: agents_none 15/15, rule_late 15/15.
- On the 5 tasks both ran: base 15/15, rule_early 15/15.
- On the 5 tasks both ran: base 15/15, rule_late 15/15.
- On the 5 tasks both ran: rule_early 15/15, rule_late 15/15.

## Test 3 prompt shape

| Condition | Runs | Passed | Rule followed | Out-of-scope runs | Median input tokens | Median output tokens | Cost (upper) | Cost per run | Cost per pass | Median wall s | Killed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_oneline | 42 | 42/42 | 15/15 | 0 | 97,720 | 1,618 | $2.60 | $0.062 | $0.062 | 36 | 0 |
| base | 42 | 42/42 | 15/15 | 0 | 92,559 | 2,222 | $2.73 | $0.065 | $0.065 | 39 | 0 |

- On the 14 tasks both ran: prompt_oneline 42/42, base 42/42.

## Test 4 plan first

| Condition | Runs | Passed | Rule followed | Out-of-scope runs | Median input tokens | Median output tokens | Cost (upper) | Cost per run | Cost per pass | Median wall s | Killed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| base | 42 | 42/42 | 15/15 | 0 | 92,559 | 2,222 | $2.73 | $0.065 | $0.065 | 39 | 0 |
| plan | 42 | 42/42 | 15/15 | 0 | 155,143 | 2,352 | $4.55 | $0.108 | $0.108 | 53 | 0 |

- On the 14 tasks both ran: base 42/42, plan 42/42.

## Test 5 reasoning effort

| Condition | Runs | Passed | Rule followed | Out-of-scope runs | Median input tokens | Median output tokens | Cost (upper) | Cost per run | Cost per pass | Median wall s | Killed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| effort_low | 42 | 42/42 | 15/15 | 0 | 79,730 | 1,334 | $2.26 | $0.054 | $0.054 | 33 | 0 |
| base | 42 | 42/42 | 15/15 | 0 | 92,559 | 2,222 | $2.73 | $0.065 | $0.065 | 39 | 0 |
| effort_high | 42 | 42/42 | 15/15 | 0 | 108,052 | 2,917 | $3.25 | $0.077 | $0.077 | 66 | 0 |

- On the 14 tasks both ran: effort_low 42/42, base 42/42.
- On the 14 tasks both ran: effort_low 42/42, effort_high 42/42.
- On the 14 tasks both ran: base 42/42, effort_high 42/42.

## Test 6 review session

| Condition | Runs | Seeded bugs | Bugs caught | Regressions (tests broken that passed before) | Findings reported | Patch applied exactly | Passed after review | Cost per run |
|---|---|---|---|---|---|---|---|---|
| review_same_buggy | 24 | 48 | 48 | 0 | 77 (in 24 parsed answers) | 24/24 | 24/24 | $0.174 |
| review_fresh_buggy | 24 | 48 | 48 | 0 | 78 (in 24 parsed answers) | 24/24 | 24/24 | $0.066 |
| review_same_clean | 24 | 0 | – | 0 | 35 (in 24 parsed answers) | 24/24 | 24/24 | $0.170 |
| review_fresh_clean | 24 | 0 | – | 0 | 42 (in 24 parsed answers) | 24/24 | 24/24 | $0.070 |

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
| t14-store-days | 3/3 | 3/3 | 3/3 |  |  | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |

## Runs worth reading

- none
