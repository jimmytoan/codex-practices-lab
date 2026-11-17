import pytest

from shoplib.inventory import Inventory


def stocked():
    inv = Inventory()
    inv.receive("A", 10)
    inv.reserve("A", 6)
    return inv


def test_release_part():
    inv = stocked()
    inv.release("A", 2)
    assert inv.reserved("A") == 4
    assert inv.available("A") == 6
    assert inv.on_hand("A") == 10


def test_release_all_then_reserve_again():
    inv = stocked()
    inv.release("A", 6)
    assert inv.reserved("A") == 0
    inv.reserve("A", 10)
    assert inv.available("A") == 0


def test_release_more_than_reserved_changes_nothing():
    inv = stocked()
    with pytest.raises(ValueError):
        inv.release("A", 7)
    assert inv.reserved("A") == 6
    assert inv.available("A") == 4


@pytest.mark.parametrize("qty", [0, -1])
def test_qty_must_be_positive(qty):
    inv = stocked()
    with pytest.raises(ValueError):
        inv.release("A", qty)
    assert inv.reserved("A") == 6


def test_unknown_or_unreserved_sku():
    inv = stocked()
    inv.receive("B", 3)
    with pytest.raises(ValueError):
        inv.release("B", 1)
    with pytest.raises(ValueError):
        inv.release("NOPE", 1)
    assert inv.reserved("B") == 0
    assert inv.reserved("NOPE") == 0
