"""Coupons. See docs/discounts.md."""

from dataclasses import dataclass
from datetime import date

from .money import percent_of


@dataclass(frozen=True)
class Coupon:
    code: str
    kind: str  # "percent" or "fixed"
    value: int  # percent points, or cents
    expires: date | None = None
    min_subtotal_cents: int = 0


def apply_coupon(subtotal_cents: int, coupon: Coupon) -> int:
    """Apply one coupon, ignoring expiry and minimum. Never returns less than 0."""
    if subtotal_cents < 0:
        raise ValueError("subtotal must not be negative")
    if coupon.kind == "percent":
        total = subtotal_cents - percent_of(subtotal_cents, coupon.value)
    elif coupon.kind == "fixed":
        total = subtotal_cents - coupon.value
    else:
        raise ValueError(f"unknown coupon kind {coupon.kind!r}")
    return max(total, 0)


def apply_coupons(subtotal_cents: int, coupons: list[Coupon], today: date) -> tuple[int, list[str]]:
    """Apply several coupons following the rules in docs/discounts.md."""
    raise NotImplementedError
