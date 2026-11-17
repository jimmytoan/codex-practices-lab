from shoplib.cart import Cart


def cart_with(*lines):
    cart = Cart()
    for sku, price, qty in lines:
        cart.add(sku, price, qty)
    return cart


def test_no_discount_below_ten():
    cart = cart_with(("A", 333, 9))
    assert cart.line_total("A") == 2997
    assert cart.subtotal() == 2997


def test_discount_at_ten():
    cart = cart_with(("A", 1000, 10))
    assert cart.line_total("A") == 9500


def test_half_cent_rounds_up_3330():
    # 5% of 3330 is 166.5 -> 167 off
    cart = cart_with(("A", 333, 10))
    assert cart.line_total("A") == 3163


def test_half_cent_rounds_up_1990():
    # 5% of 1990 is 99.5 -> 100 off
    cart = cart_with(("A", 199, 10))
    assert cart.line_total("A") == 1890


def test_half_cent_rounds_up_10():
    # 5% of 10 is 0.5 -> 1 off
    cart = cart_with(("A", 1, 10))
    assert cart.line_total("A") == 9


def test_discount_is_per_line():
    cart = cart_with(("A", 333, 10), ("B", 500, 9), ("C", 77, 30))
    # A: 3330 - 167; B: 4500; C: 2310 - 116 (115.5 rounds up)
    assert cart.line_total("C") == 2194
    assert cart.subtotal() == 3163 + 4500 + 2194


def test_merged_adds_reach_threshold():
    cart = Cart()
    cart.add("A", 100, 6)
    assert cart.line_total("A") == 600
    cart.add("A", 100, 4)
    assert cart.line_total("A") == 950


def test_totals_are_ints():
    cart = cart_with(("A", 333, 10))
    assert type(cart.line_total("A")) is int
    assert type(cart.subtotal()) is int
