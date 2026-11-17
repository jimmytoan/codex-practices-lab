import pytest
from shoplib.errors import ShopError
from shoplib.inventory import Inventory
from shoplib.orders import Order


def test_rule():
    inv = Inventory()
    inv.receive("A", 5)
    order = Order("o1", {"A": 2}, inv)
    order.pay()
    order.ship()
    with pytest.raises(ValueError) as exc:
        order.cancel()
    assert type(exc.value) is ShopError
