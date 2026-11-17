import pytest

from shoplib.cart import Cart


def test_add_and_subtotal():
    cart = Cart()
    cart.add("A", 250, 2)
    cart.add("B", 1000)
    assert cart.line_total("A") == 500
    assert cart.subtotal() == 1500


def test_add_same_sku_merges():
    cart = Cart()
    cart.add("A", 250, 2)
    cart.add("A", 250, 3)
    assert cart.line_total("A") == 1250


def test_bad_qty():
    with pytest.raises(ValueError):
        Cart().add("A", 250, 0)
