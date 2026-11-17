"""Sales reports."""

COLUMNS = ["sku", "name", "units", "revenue_cents"]


def sales_summary(sales: list[dict]) -> list[dict]:
    """One row per SKU, sorted by SKU.

    `sales` is a list of {"sku", "name", "qty", "unit_price_cents"}. Each row is
    {"sku", "name", "units", "revenue_cents"}.
    """
    rows: dict[str, dict] = {}
    for sale in sales:
        row = rows.setdefault(
            sale["sku"], {"sku": sale["sku"], "name": sale["name"], "units": 0, "revenue_cents": 0}
        )
        row["units"] += sale["qty"]
        row["revenue_cents"] += sale["qty"] * sale["unit_price_cents"]
    return [rows[sku] for sku in sorted(rows)]


def to_csv(rows: list[dict]) -> str:
    """Render summary rows as CSV, following docs/CONVENTIONS.md."""
    lines = [",".join(COLUMNS)]
    for row in rows:
        lines.append(",".join(str(row[col]) for col in COLUMNS))
    return "\n".join(lines) + "\n"
