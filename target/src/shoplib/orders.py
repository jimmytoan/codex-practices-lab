"""Orders and their life cycle. See docs/order-states.md."""

from .inventory import Inventory

NEW = "NEW"
PAID = "PAID"
SHIPPED = "SHIPPED"
DELIVERED = "DELIVERED"
CANCELLED = "CANCELLED"


class Order:
    def __init__(self, order_id: str, lines: dict[str, int], inventory: Inventory):
        """Create an order for `lines` (sku -> qty) and reserve its stock."""
        if not lines:
            raise ValueError("an order needs at least one line")
        self.order_id = order_id
        self.lines = dict(lines)
        self.inventory = inventory
        self.state = NEW
        self.refund_due = False
        reserved = []
        try:
            for sku, qty in self.lines.items():
                inventory.reserve(sku, qty)
                reserved.append((sku, qty))
        except ValueError:
            for sku, qty in reserved:
                inventory._reserved[sku] -= qty
            raise

    def _transition(self, allowed_from: tuple[str, ...], to: str) -> None:
        if self.state not in allowed_from:
            raise ValueError(f"cannot go from {self.state} to {to}")
        self.state = to

    def pay(self) -> None:
        self._transition((NEW,), PAID)

    def ship(self) -> None:
        if self.state != PAID:
            raise ValueError(f"cannot go from {self.state} to {SHIPPED}")
        for sku, qty in self.lines.items():
            self.inventory.ship(sku, qty)
        self.state = SHIPPED

    def deliver(self) -> None:
        self._transition((SHIPPED,), DELIVERED)
