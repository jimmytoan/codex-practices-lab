import pytest

from shoplib.shipping import shipping_cost


def test_tiers():
    assert shipping_cost(300) == 500
    assert shipping_cost(1500) == 800
    assert shipping_cost(4000) == 1200
    assert shipping_cost(12000) == 2500


def test_invalid_weight():
    with pytest.raises(ValueError):
        shipping_cost(0)
    with pytest.raises(ValueError):
        shipping_cost(25000)
