import pytest
from shoplib.errors import ShopError
from shoplib.shipping import shipping_cost


def test_rule():
    with pytest.raises(ValueError) as exc:
        shipping_cost(-5)
    assert type(exc.value) is ShopError
    with pytest.raises(ValueError) as exc:
        shipping_cost(30000)
    assert type(exc.value) is ShopError
