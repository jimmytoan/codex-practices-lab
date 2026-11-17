"""Shopping cart."""

from dataclasses import dataclass


@dataclass
class Line:
    sku: str
    unit_price_cents: int
    qty: int


class Cart:
    def __init__(self):
        self._lines: dict[str, Line] = {}

    def add(self, sku: str, unit_price_cents: int, qty: int = 1) -> None:
        """Add `qty` units. Adding a SKU already in the cart increases its quantity."""
        if qty <= 0:
            raise ValueError("qty must be positive")
        if unit_price_cents < 0:
            raise ValueError("price must not be negative")
        if sku in self._lines:
            self._lines[sku].qty += qty
        else:
            self._lines[sku] = Line(sku, unit_price_cents, qty)

    def remove(self, sku: str) -> None:
        if sku not in self._lines:
            raise ValueError(f"{sku} is not in the cart")
        del self._lines[sku]

    def lines(self) -> list[Line]:
        return sorted(self._lines.values(), key=lambda line: line.sku)

    def line_total(self, sku: str) -> int:
        """Total for one line in cents."""
        if sku not in self._lines:
            raise ValueError(f"{sku} is not in the cart")
        line = self._lines[sku]
        return line.unit_price_cents * line.qty

    def subtotal(self) -> int:
        """Sum of all line totals in cents."""
        return sum(self.line_total(sku) for sku in self._lines)
