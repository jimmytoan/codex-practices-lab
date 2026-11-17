from datetime import date

import pytest

from shoplib.dates import add_business_days

FRI = date(2026, 11, 13)
SAT = date(2026, 11, 14)
SUN = date(2026, 11, 15)
MON = date(2026, 11, 16)
TUE = date(2026, 11, 17)
WED = date(2026, 11, 18)
THU = date(2026, 11, 19)


def test_forward_still_works():
    assert add_business_days(FRI, 1) == MON
    assert add_business_days(MON, 3) == THU
    assert add_business_days(SAT, 1) == MON


def test_forward_skips_holidays():
    assert add_business_days(FRI, 1, holidays={MON}) == TUE
    assert add_business_days(FRI, 2, holidays={MON, WED}) == THU


def test_backward():
    assert add_business_days(MON, -1) == FRI
    assert add_business_days(WED, -2) == MON
    assert add_business_days(WED, -4) == date(2026, 11, 12)


def test_backward_from_weekend():
    assert add_business_days(SUN, -1) == FRI
    assert add_business_days(SAT, -2) == date(2026, 11, 12)


def test_backward_skips_holidays():
    assert add_business_days(TUE, -1, holidays={MON}) == FRI
    assert add_business_days(WED, -2, holidays=[MON, FRI]) == date(2026, 11, 12)


def test_zero_on_business_day():
    assert add_business_days(MON, 0) == MON


def test_zero_on_weekend_moves_forward():
    assert add_business_days(SAT, 0) == MON
    assert add_business_days(SUN, 0) == MON


def test_zero_on_holiday_moves_forward():
    assert add_business_days(MON, 0, holidays={MON}) == TUE
    assert add_business_days(FRI, 0, holidays={FRI, MON}) == TUE


def test_holiday_on_weekend_changes_nothing():
    assert add_business_days(FRI, 1, holidays={SAT, SUN}) == MON


@pytest.mark.parametrize("n", [5, 10, 23])
def test_round_trip(n):
    there = add_business_days(MON, n, holidays={WED})
    assert add_business_days(there, -n, holidays={WED}) == MON
