from shoplib.discounts import Coupon, apply_coupon


def test_percent():
    assert apply_coupon(1000, Coupon("TEN", "percent", 10)) == 900


def test_fixed_never_negative():
    assert apply_coupon(300, Coupon("FIVE", "fixed", 500)) == 0
