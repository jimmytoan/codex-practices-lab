import pytest
from shoplib.errors import ShopError
from shoplib.inventory import Inventory


def test_rule():
    inv = Inventory()
    inv.receive("A", 5)
    inv.reserve("A", 2)
    with pytest.raises(ValueError) as exc:
        inv.release("A", 3)
    assert type(exc.value) is ShopError
    with pytest.raises(ValueError) as exc:
        inv.release("A", 0)
    assert type(exc.value) is ShopError
