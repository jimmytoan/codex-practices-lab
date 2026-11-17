# Results: tag `pilot`, model `gpt-6-luna`

- Runs counted: 41. Excluded for provider/harness errors: 5.
- Spend: $0.31 upper bound (cache writes at the 12h price), $0.21 at the 30m price, errored runs included.
- Models: gpt-6-luna. Codex: codex-cli 0.169.0.
- Peeking at hidden tests or ~/.codex: 0 runs.

## Test 1 AGENTS.md size

| Condition | Runs | Passed | Rule followed | Out-of-scope runs | Median input tokens | Median output tokens | Cost (upper) | Cost per run | Cost per pass | Median wall s | Killed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| agents_none | 13 | 13/13 | 0/5 | 0 | 105,139 | 2,595 | $0.09 | $0.007 | $0.007 | 34 | 0 |
| base | 10 | 10/10 | 5/5 | 0 | 102,006 | 1,756 | $0.07 | $0.007 | $0.007 | 31 | 0 |
| agents_bloated | 0 | – | – | – | – | – | – | – | – | – | – |

- On the 10 tasks both ran: agents_none 10/10, base 10/10.

## Test 2 32 KiB limit

| Condition | Runs | Passed | Rule followed | Out-of-scope runs | Median input tokens | Median output tokens | Cost (upper) | Cost per run | Cost per pass | Median wall s | Killed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| agents_none | 13 | 13/13 | 0/5 | 0 | 105,139 | 2,595 | $0.09 | $0.007 | $0.007 | 34 | 0 |
| base | 10 | 10/10 | 5/5 | 0 | 102,006 | 1,756 | $0.07 | $0.007 | $0.007 | 31 | 0 |
| rule_early | 0 | – | – | – | – | – | – | – | – | – | – |
| rule_late | 0 | – | – | – | – | – | – | – | – | – | – |

Rule tasks only:

| Condition | Runs (rule tasks) | Rule followed | AGENTS.md bytes loaded (median) | Loaded text contains the rule | Tasks passed |
|---|---|---|---|---|---|
| agents_none | 5 | 0/5 | 0 | 0/5 | 5/5 |
| base | 5 | 5/5 | 1,056 | 5/5 | 5/5 |

- On the 10 tasks both ran: agents_none 10/10, base 10/10.

## Test 3 prompt shape

| Condition | Runs | Passed | Rule followed | Out-of-scope runs | Median input tokens | Median output tokens | Cost (upper) | Cost per run | Cost per pass | Median wall s | Killed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_oneline | 14 | 14/14 | 5/5 | 1 | 134,452 | 2,598 | $0.11 | $0.008 | $0.008 | 32 | 0 |
| base | 10 | 10/10 | 5/5 | 0 | 102,006 | 1,756 | $0.07 | $0.007 | $0.007 | 31 | 0 |

- On the 10 tasks both ran: prompt_oneline 10/10, base 10/10.

## Test 4 plan first

| Condition | Runs | Passed | Rule followed | Out-of-scope runs | Median input tokens | Median output tokens | Cost (upper) | Cost per run | Cost per pass | Median wall s | Killed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| base | 10 | 10/10 | 5/5 | 0 | 102,006 | 1,756 | $0.07 | $0.007 | $0.007 | 31 | 0 |
| plan | 0 | – | – | – | – | – | – | – | – | – | – |



## Test 5 reasoning effort

| Condition | Runs | Passed | Rule followed | Out-of-scope runs | Median input tokens | Median output tokens | Cost (upper) | Cost per run | Cost per pass | Median wall s | Killed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| effort_low | 4 | 4/4 | – | 0 | 120,341 | 2,546 | $0.03 | $0.007 | $0.007 | 30 | 0 |
| base | 10 | 10/10 | 5/5 | 0 | 102,006 | 1,756 | $0.07 | $0.007 | $0.007 | 31 | 0 |
| effort_high | 0 | – | – | – | – | – | – | – | – | – | – |



## Test 6 review session

| Condition | Runs | Seeded bugs | Bugs caught | Regressions (tests broken that passed before) | Findings reported | Patch applied exactly | Passed after review | Cost per run |
|---|---|---|---|---|---|---|---|---|

## Passes by task and condition

| Task | base | agents_none | prompt_oneline | effort_low |
|---|---|---|---|---|
| t01-shipping-boundary | 1/1 | 1/1 | 1/1 |  |
| t02-bulk-discount | 1/1 | 1/1 | 1/1 |  |
| t03-inventory-release | 1/1 | 1/1 | 1/1 |  |
| t04-order-cancel | 1/1 | 1/1 | 1/1 |  |
| t05-csv-quoting | 1/1 | 1/1 | 1/1 |  |
| t06-business-days | 1/1 | 1/1 | 1/1 |  |
| t07-coupon-stacking | 1/1 | 1/1 | 1/1 |  |
| t08-cli-json | 1/1 | 1/1 | 1/1 |  |
| t09-slug-accents | 1/1 | 1/1 | 1/1 |  |
| t10-split-parcels | 1/1 | 1/1 | 1/1 |  |
| t11-invoice-tax |  |  | 1/1 | 1/1 |
| t12-search-query |  | 1/1 | 1/1 | 1/1 |
| t13-fifo-costing |  | 1/1 | 1/1 | 1/1 |
| t14-store-days |  | 1/1 | 1/1 | 1/1 |

## Runs worth reading

- `20261117-181713-prompt_oneline-t08-dbf8` (prompt_oneline, t08-cli-json): out of scope ['src/shoplib/reports.py']

## Excluded runs

- `20261117-190504-base-t11-898d` (base, t11-invoice-tax): stall: no output for >10 min (relabelled after inspecting events/rollout; see PLAN.md)
- `20261117-192134-base-t12-169a` (base, t12-search-query): stall: no output for >10 min (relabelled after inspecting events/rollout; see PLAN.md)
- `20261117-194018-base-t13-85f8` (base, t13-fifo-costing): stall: no output for >10 min (relabelled after inspecting events/rollout; see PLAN.md)
- `20261117-195811-base-t14-5608` (base, t14-store-days): stall: no output for >10 min (relabelled after inspecting events/rollout; see PLAN.md)
- `20261117-201539-agents_none-t11-dc30` (agents_none, t11-invoice-tax): stall: no output for >10 min (relabelled after inspecting events/rollout; see PLAN.md)
