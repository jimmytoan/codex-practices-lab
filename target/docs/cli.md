# Command line

    python -m shoplib.cli report SALES_JSON

`SALES_JSON` is a file holding a list of sales, each
`{"sku": ..., "name": ..., "qty": ..., "unit_price_cents": ...}`.
The command prints the sales summary (one row per SKU) as CSV and exits 0.
Output formats follow docs/CONVENTIONS.md.
