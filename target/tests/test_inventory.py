import pytest

from shoplib.inventory import Inventory


def test_reserve_and_ship():
    inv = Inventory()
    inv.receive("A", 10)
    inv.reserve("A", 4)
    assert inv.available("A") == 6
    inv.ship("A", 4)
    assert inv.on_hand("A") == 6
    assert inv.reserved("A") == 0


def test_cannot_reserve_more_than_available():
    inv = Inventory()
    inv.receive("A", 2)
    with pytest.raises(ValueError):
        inv.reserve("A", 3)
