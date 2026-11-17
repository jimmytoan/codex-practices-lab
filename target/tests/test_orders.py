import pytest

from shoplib.inventory import Inventory
from shoplib.orders import DELIVERED, NEW, Order


def make():
    inv = Inventory()
    inv.receive("A", 5)
    return inv, Order("o1", {"A": 2}, inv)


def test_happy_path():
    inv, order = make()
    assert order.state == NEW
    assert inv.available("A") == 3
    order.pay()
    order.ship()
    order.deliver()
    assert order.state == DELIVERED
    assert inv.on_hand("A") == 3


def test_cannot_ship_unpaid():
    _, order = make()
    with pytest.raises(ValueError):
        order.ship()
