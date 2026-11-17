# Coupons

A coupon has a `code`, a `kind` (`"percent"` or `"fixed"`), a `value` (percent
points, or cents), an optional `expires` date and a `min_subtotal_cents`.

`apply_coupons(subtotal_cents, coupons, today)` combines several coupons:

1. A coupon is eligible when it has not expired (a coupon is still valid on its
   `expires` date) and the original subtotal is at least its
   `min_subtotal_cents`.
2. At most one percent coupon applies: the eligible one with the highest value.
   If two have the same value, the one whose code sorts first applies.
3. The percent discount is taken first, from the original subtotal, using
   `shoplib.money.percent_of`. Then every eligible fixed coupon is subtracted.
4. The total never goes below 0.
5. The result is `(total_cents, applied_codes)`, where `applied_codes` is the
   sorted list of codes of the coupons that applied (the chosen percent coupon
   and every eligible fixed coupon).
6. A negative subtotal raises `ValueError`.
