import pytest
from shoplib.errors import ShopError
from shoplib.shipping import split_parcels


def test_rule():
    with pytest.raises(ValueError) as exc:
        split_parcels([("A", 5001, 1)], 5000)
    assert type(exc.value) is ShopError
    with pytest.raises(ValueError) as exc:
        split_parcels([("A", 100, 0)], 5000)
    assert type(exc.value) is ShopError
