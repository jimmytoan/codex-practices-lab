from datetime import date

from shoplib.dates import add_business_days, is_business_day


def test_is_business_day():
    assert is_business_day(date(2026, 11, 16))  # Monday
    assert not is_business_day(date(2026, 11, 15))  # Sunday


def test_forward_over_weekend():
    # Friday + 1 business day = Monday
    assert add_business_days(date(2026, 11, 13), 1) == date(2026, 11, 16)
    assert add_business_days(date(2026, 11, 16), 3) == date(2026, 11, 19)
