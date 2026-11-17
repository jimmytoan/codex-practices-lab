import copy

import pytest

from shoplib.costing import fifo_costing


def recv(sku, qty, cost):
    return {"type": "receive", "sku": sku, "qty": qty, "unit_cost_cents": cost}


def sell(sku, qty):
    return {"type": "sell", "sku": sku, "qty": qty}


def ret(sku, qty):
    return {"type": "return", "sku": sku, "qty": qty}


def test_receive_only():
    assert fifo_costing([recv("A", 5, 100)]) == {"A": {"cogs_cents": 0, "on_hand": 5, "value_cents": 500}}


def test_oldest_lots_first():
    out = fifo_costing([recv("A", 3, 100), recv("A", 5, 120), sell("A", 4)])
    assert out == {"A": {"cogs_cents": 420, "on_hand": 4, "value_cents": 480}}


def test_skus_are_independent():
    out = fifo_costing([recv("A", 2, 100), recv("B", 2, 300), sell("B", 1), sell("A", 2)])
    assert out == {"A": {"cogs_cents": 200, "on_hand": 0, "value_cents": 0},
                   "B": {"cogs_cents": 300, "on_hand": 1, "value_cents": 300}}


def test_return_at_average_cost_half_up():
    out = fifo_costing([recv("A", 1, 100), recv("A", 1, 101), sell("A", 2), ret("A", 1)])
    # sale cost 201 for 2 units -> average 100.5 -> 101
    assert out == {"A": {"cogs_cents": 100, "on_hand": 1, "value_cents": 101}}


def test_returned_units_are_sold_last():
    out = fifo_costing([recv("A", 2, 100), sell("A", 2), recv("A", 2, 150), ret("A", 1), sell("A", 2)])
    # lots after the return: 2@150 then 1@100; the next sale takes the two 150s
    assert out == {"A": {"cogs_cents": 200 - 100 + 300, "on_hand": 1, "value_cents": 100}}


def test_several_returns_against_one_sale():
    events = [recv("A", 5, 100), sell("A", 2), ret("A", 1), ret("A", 1)]
    assert fifo_costing(events) == {"A": {"cogs_cents": 0, "on_hand": 5, "value_cents": 500}}
    with pytest.raises(ValueError):
        fifo_costing(events + [ret("A", 1)])


def test_return_is_against_most_recent_sale_only():
    with pytest.raises(ValueError):
        fifo_costing([recv("A", 5, 100), sell("A", 3), sell("A", 1), ret("A", 2)])


def test_return_without_sale():
    with pytest.raises(ValueError):
        fifo_costing([recv("A", 5, 100), ret("A", 1)])


def test_cannot_oversell():
    with pytest.raises(ValueError):
        fifo_costing([recv("A", 2, 100), sell("A", 3)])
    with pytest.raises(ValueError):
        fifo_costing([recv("A", 2, 100), sell("B", 1)])


@pytest.mark.parametrize("event", [recv("A", 0, 100), recv("A", 1, -1), sell("A", 0), {"type": "steal", "sku": "A", "qty": 1}])
def test_bad_events(event):
    with pytest.raises(ValueError):
        fifo_costing([recv("A", 5, 100), event])


def test_zero_cost_is_allowed():
    assert fifo_costing([recv("A", 2, 0), sell("A", 1)]) == {"A": {"cogs_cents": 0, "on_hand": 1, "value_cents": 0}}


def test_events_not_modified():
    events = [recv("A", 3, 100), recv("A", 5, 120), sell("A", 4), ret("A", 1)]
    before = copy.deepcopy(events)
    fifo_costing(events)
    assert events == before
