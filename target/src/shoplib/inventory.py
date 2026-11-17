"""Stock levels: on hand, reserved for orders, and available."""


class Inventory:
    def __init__(self):
        self._on_hand: dict[str, int] = {}
        self._reserved: dict[str, int] = {}

    def receive(self, sku: str, qty: int) -> None:
        if qty <= 0:
            raise ValueError("qty must be positive")
        self._on_hand[sku] = self._on_hand.get(sku, 0) + qty

    def on_hand(self, sku: str) -> int:
        return self._on_hand.get(sku, 0)

    def reserved(self, sku: str) -> int:
        return self._reserved.get(sku, 0)

    def available(self, sku: str) -> int:
        return self.on_hand(sku) - self.reserved(sku)

    def reserve(self, sku: str, qty: int) -> None:
        """Reserve `qty` available units for an order."""
        if qty <= 0:
            raise ValueError("qty must be positive")
        if qty > self.available(sku):
            raise ValueError(f"only {self.available(sku)} of {sku} available")
        self._reserved[sku] = self.reserved(sku) + qty

    def release(self, sku: str, qty: int) -> None:
        """Give `qty` reserved units back to available.

        `qty` must be positive. Releasing more than is currently reserved for
        the SKU (including a SKU with nothing reserved) raises ValueError and
        changes nothing.
        """
        raise NotImplementedError

    def ship(self, sku: str, qty: int) -> None:
        """Ship `qty` reserved units: they leave both reserved and on hand."""
        if qty <= 0:
            raise ValueError("qty must be positive")
        if qty > self.reserved(sku):
            raise ValueError(f"only {self.reserved(sku)} of {sku} reserved")
        self._reserved[sku] -= qty
        self._on_hand[sku] -= qty
