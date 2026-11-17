"""Shipping costs and parcel splitting. See docs/shipping.md."""

# (upper bound in grams, cost in cents)
TIERS = [(1000, 500), (2000, 800), (5000, 1200), (20000, 2500)]


def shipping_cost(weight_g: int) -> int:
    """Cost in cents of one parcel of `weight_g` grams. See docs/shipping.md."""
    if weight_g <= 0:
        raise ValueError("weight must be positive")
    for limit, cost in TIERS:
        if weight_g < limit:
            return cost
    raise ValueError("parcel is too heavy")


def split_parcels(items: list[tuple[str, int, int]], max_weight_g: int) -> list[list[str]]:
    """Split order items into parcels. See docs/shipping.md."""
    raise NotImplementedError


def shipment_cost(items: list[tuple[str, int, int]], max_weight_g: int) -> int:
    """Total shipping cost of an order. See docs/shipping.md."""
    raise NotImplementedError
