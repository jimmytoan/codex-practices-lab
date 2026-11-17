# Store days

The shop closes late, so its sales day does not run midnight to midnight.

`daily_revenue(sales, utc_offset_hours=8, day_starts_hour=4)`

- Each sale is `{"at": timestamp, "cents": amount}`. Timestamps are ISO 8601 with a zone, either `Z` or
  `+HH:MM` / `-HH:MM`. A timestamp without a zone raises `ValueError`.
- The shop's local time is UTC plus `utc_offset_hours`.
- A store day starts at `day_starts_hour`:00 local time and lasts 24 hours. It is named by the local date
  on which it starts: with the defaults, a sale at 02:30 local time on 18 November belongs to the store
  day `2026-11-17`. A sale exactly at the start hour belongs to the day that starts then.
- Refunds are sales with negative `cents` and count like any other sale.
- The result is a list of `(store_day, total_cents)` with `store_day` as `YYYY-MM-DD`, one entry for
  every store day from the first to the last day that has a sale, both included, with 0 for days without
  sales, in date order. No sales gives an empty list.
