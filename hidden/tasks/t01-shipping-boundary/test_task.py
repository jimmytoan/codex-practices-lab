import pytest

from shoplib.shipping import shipping_cost


@pytest.mark.parametrize("weight,cost", [(1000, 500), (2000, 800), (5000, 1200), (20000, 2500)])
def test_upper_bound_is_inclusive(weight, cost):
    assert shipping_cost(weight) == cost


@pytest.mark.parametrize("weight,cost", [(1, 500), (999, 500), (1001, 800), (2001, 1200), (5001, 2500), (19999, 2500)])
def test_inside_and_just_over(weight, cost):
    assert shipping_cost(weight) == cost


@pytest.mark.parametrize("weight", [0, -1, 20001, 50000])
def test_invalid(weight):
    with pytest.raises(ValueError):
        shipping_cost(weight)
