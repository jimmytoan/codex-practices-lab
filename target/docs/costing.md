# FIFO costing

`fifo_costing(events)` processes stock events in order and returns, for every SKU that appears,
`{"cogs_cents": ..., "on_hand": ..., "value_cents": ...}`: the cost of goods sold so far, the units left,
and the cost value of the units left.

Each event is a dict:

- `{"type": "receive", "sku", "qty", "unit_cost_cents"}` adds a lot of `qty` units at that unit cost.
- `{"type": "sell", "sku", "qty"}` takes units from the oldest lots first. The sale's cost is the sum of
  the lot costs of the units taken, and is added to the SKU's cost of goods sold.
- `{"type": "return", "sku", "qty"}` brings back units from the SKU's most recent sale. They come back as
  a new lot, after all existing lots (so they are sold last), at the average unit cost of that sale,
  rounded half up to whole cents with `shoplib.money.round_cents`. The cost of goods sold goes down by
  `qty` times that unit cost. Several returns may be made against the same sale, but in total no more
  units than it sold.

Raise `ValueError`, and return nothing, for: a quantity below 1, a negative unit cost, selling more units
than are on hand, a return when the SKU has had no sale, a return of more units than are still returnable
from the SKU's most recent sale, and an unknown event type. The `events` list must not be modified.
