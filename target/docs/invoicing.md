# Invoicing

`build_invoice(lines, coupon_cents, shipping_cents, region)`

- `lines` is a list of `(sku, unit_price_cents, qty, category)`. `category` must be a key of the
  region's entry in `TAX_RATES`.
- The result is `{"lines": [...], "shipping_cents": ..., "shipping_tax_cents": ..., "total_cents": ...}`.
  Each line is `{"sku", "gross_cents", "discount_cents", "net_cents", "tax_cents"}`, in input order.

Rules:

1. A line's gross is `unit_price_cents * qty`.
2. The coupon is an amount off the whole order. It is capped at the sum of the gross amounts. It is split
   across the lines in proportion to their gross using the largest-remainder method: each line first gets
   `floor(coupon * gross / total_gross)`; the cents left over then go, one cent each, to the lines with the
   largest remainders (the fractional parts the floor dropped). On equal remainders the earlier line goes
   first. The line discounts always add up to the (capped) coupon. If the total gross is 0, every
   discount is 0.
3. A line's net is gross minus its discount.
4. A line's tax is `percent_of(net, rate)`, where the rate is the region's rate for the line's category.
   Tax is computed and rounded per line, never on the order total.
5. Shipping is taxed at the region's `standard` rate, but only if at least one line's category has a rate
   above 0 in that region. Otherwise the shipping tax is 0.
6. `total_cents` is the sum of the nets, the line taxes, the shipping and the shipping tax.
7. Raise `ValueError` for an unknown region, an unknown category, an empty `lines`, a quantity below 1,
   or a negative price, coupon or shipping amount.
