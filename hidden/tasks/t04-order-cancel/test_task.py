import pytest

from shoplib.inventory import Inventory
from shoplib.orders import CANCELLED, DELIVERED, SHIPPED, Order


def make():
    inv = Inventory()
    inv.receive("A", 5)
    inv.receive("B", 4)
    return inv, Order("o1", {"A": 2, "B": 3}, inv)


def test_cancel_new_releases_stock():
    inv, order = make()
    order.cancel()
    assert order.state == CANCELLED
    assert order.refund_due is False
    assert (inv.available("A"), inv.available("B")) == (5, 4)
    assert (inv.reserved("A"), inv.reserved("B")) == (0, 0)
    assert (inv.on_hand("A"), inv.on_hand("B")) == (5, 4)


def test_cancel_paid_sets_refund():
    inv, order = make()
    order.pay()
    order.cancel()
    assert order.state == CANCELLED
    assert order.refund_due is True
    assert (inv.available("A"), inv.available("B")) == (5, 4)


def test_cancel_twice_is_a_no_op():
    inv, order = make()
    order.pay()
    order.cancel()
    other = Order("o2", {"A": 4}, inv)
    order.cancel()
    assert order.state == CANCELLED
    assert order.refund_due is True
    assert inv.reserved("A") == 4
    assert inv.available("A") == 1
    assert other.state == "NEW"


def test_cannot_cancel_shipped():
    inv, order = make()
    order.pay()
    order.ship()
    with pytest.raises(ValueError):
        order.cancel()
    assert order.state == SHIPPED
    assert order.refund_due is False
    assert inv.on_hand("A") == 3


def test_cannot_cancel_delivered():
    inv, order = make()
    order.pay()
    order.ship()
    order.deliver()
    with pytest.raises(ValueError):
        order.cancel()
    assert order.state == DELIVERED
    assert order.refund_due is False


def test_cancelled_order_cannot_be_paid_or_shipped():
    _, order = make()
    order.cancel()
    with pytest.raises(ValueError):
        order.pay()
    with pytest.raises(ValueError):
        order.ship()


def test_other_orders_keep_their_reservation():
    inv, order = make()
    other = Order("o2", {"A": 3}, inv)
    order.cancel()
    assert inv.reserved("A") == 3
    other.pay()
    other.ship()
    assert inv.on_hand("A") == 2
