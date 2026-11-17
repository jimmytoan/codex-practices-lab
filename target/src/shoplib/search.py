"""Product search. See docs/search.md."""

from dataclasses import dataclass, field


@dataclass
class Product:
    sku: str
    name: str
    price_cents: int
    tags: list[str] = field(default_factory=list)


def search(products: list[Product], query: str) -> list[Product]:
    """The products that match `query`, in their input order. See docs/search.md."""
    raise NotImplementedError
