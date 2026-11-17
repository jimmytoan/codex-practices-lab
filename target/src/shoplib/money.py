"""Money helpers. All money in shoplib is an integer number of cents."""

from decimal import ROUND_HALF_UP, Decimal


def round_cents(amount) -> int:
    """Round a fractional number of cents to whole cents, half up (0.5 -> 1)."""
    return int(Decimal(str(amount)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def percent_of(cents: int, percent) -> int:
    """`percent` percent of `cents`, rounded half up. Uses Decimal, not float."""
    return round_cents(Decimal(cents) * Decimal(str(percent)) / Decimal(100))


def format_money(cents: int) -> str:
    """Format cents as dollars: 1234 -> '$12.34', -5 -> '-$0.05'."""
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}${cents // 100}.{cents % 100:02d}"
