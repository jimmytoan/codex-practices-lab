from datetime import date

import pytest

from shoplib.discounts import Coupon, apply_coupons

TODAY = date(2026, 11, 17)
YESTERDAY = date(2026, 11, 16)
TOMORROW = date(2026, 11, 18)


def test_no_coupons():
    assert apply_coupons(1000, [], TODAY) == (1000, [])


def test_percent_then_fixed():
    coupons = [Coupon("FIVE", "fixed", 500), Coupon("TEN", "percent", 10)]
    assert apply_coupons(10000, coupons, TODAY) == (8500, ["FIVE", "TEN"])


def test_only_best_percent_applies():
    coupons = [Coupon("TEN", "percent", 10), Coupon("TWENTY", "percent", 20), Coupon("FIVE", "percent", 5)]
    assert apply_coupons(10000, coupons, TODAY) == (8000, ["TWENTY"])


def test_percent_tie_takes_first_code():
    coupons = [Coupon("ZED", "percent", 10), Coupon("ABE", "percent", 10)]
    assert apply_coupons(1000, coupons, TODAY) == (900, ["ABE"])


def test_all_fixed_apply():
    coupons = [Coupon("B", "fixed", 200), Coupon("A", "fixed", 300)]
    assert apply_coupons(1000, coupons, TODAY) == (500, ["A", "B"])


def test_never_below_zero_and_codes_still_listed():
    coupons = [Coupon("BIG", "fixed", 900), Coupon("HALF", "percent", 50), Coupon("MORE", "fixed", 900)]
    assert apply_coupons(1000, coupons, TODAY) == (0, ["BIG", "HALF", "MORE"])


def test_expired_ignored_but_today_is_valid():
    coupons = [
        Coupon("OLD", "percent", 50, expires=YESTERDAY),
        Coupon("LASTDAY", "percent", 10, expires=TODAY),
        Coupon("OLDFIX", "fixed", 100, expires=YESTERDAY),
        Coupon("NEWFIX", "fixed", 100, expires=TOMORROW),
    ]
    assert apply_coupons(1000, coupons, TODAY) == (800, ["LASTDAY", "NEWFIX"])


def test_expired_best_percent_falls_back_to_next():
    coupons = [Coupon("BEST", "percent", 30, expires=YESTERDAY), Coupon("OK", "percent", 20)]
    assert apply_coupons(1000, coupons, TODAY) == (800, ["OK"])


def test_minimum_uses_original_subtotal():
    coupons = [Coupon("HALF", "percent", 50), Coupon("MIN", "fixed", 100, min_subtotal_cents=1000)]
    # after the percent the running total is 500, but the minimum looks at the original 1000
    assert apply_coupons(1000, coupons, TODAY) == (400, ["HALF", "MIN"])


def test_minimum_not_met():
    coupons = [Coupon("MIN", "fixed", 100, min_subtotal_cents=1001), Coupon("PMIN", "percent", 50, min_subtotal_cents=2000)]
    assert apply_coupons(1000, coupons, TODAY) == (1000, [])


def test_percent_rounds_half_up():
    # 15% of 1010 is 151.5 -> 152
    assert apply_coupons(1010, [Coupon("P", "percent", 15)], TODAY) == (858, ["P"])
    # 5% of 3330 is 166.5 -> 167
    assert apply_coupons(3330, [Coupon("P", "percent", 5)], TODAY) == (3163, ["P"])


def test_negative_subtotal():
    with pytest.raises(ValueError):
        apply_coupons(-1, [], TODAY)


def test_zero_subtotal():
    assert apply_coupons(0, [Coupon("F", "fixed", 100)], TODAY) == (0, ["F"])
