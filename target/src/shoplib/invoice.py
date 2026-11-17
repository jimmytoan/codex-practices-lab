"""Invoices: coupon allocation and tax. See docs/invoicing.md."""

# Tax rates in percent, by region and product category.
TAX_RATES = {
    "DE": {"standard": 19, "food": 7, "books": 7},
    "SG": {"standard": 9, "food": 9, "books": 0},
    "OR": {"standard": 0, "food": 0, "books": 0},
}


def build_invoice(lines, coupon_cents: int, shipping_cents: int, region: str) -> dict:
    """Build an invoice for an order. See docs/invoicing.md."""
    raise NotImplementedError
