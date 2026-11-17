import pytest

from shoplib.storedays import daily_revenue


def sale(at, cents=100):
    return {"at": at, "cents": cents}


def test_early_morning_belongs_to_previous_day():
    # 18:30Z is 02:30 on 18 Nov at UTC+8
    assert daily_revenue([sale("2026-11-17T18:30:00Z")]) == [("2026-11-17", 100)]


def test_exactly_at_start_hour_is_new_day():
    assert daily_revenue([sale("2026-11-17T20:00:00Z")]) == [("2026-11-18", 100)]
    assert daily_revenue([sale("2026-11-17T19:59:59Z")]) == [("2026-11-17", 100)]


def test_offsets_in_timestamps():
    assert daily_revenue([sale("2026-11-18T03:00:00+08:00")]) == [("2026-11-17", 100)]
    assert daily_revenue([sale("2026-11-17T21:00:00+02:00")]) == [("2026-11-17", 100)]
    # 15:30 at -05:00 is 20:30Z, 04:30 on the 18th at UTC+8
    assert daily_revenue([sale("2026-11-17T15:30:00-05:00")]) == [("2026-11-18", 100)]


def test_totals_and_refunds():
    sales = [sale("2026-11-17T02:00:00Z", 500), sale("2026-11-17T10:00:00Z", 300), sale("2026-11-17T11:00:00Z", -200)]
    assert daily_revenue(sales) == [("2026-11-17", 600)]


def test_gaps_filled_with_zero_and_sorted():
    sales = [sale("2026-11-20T02:00:00Z", 50), sale("2026-11-17T02:00:00Z", 10)]
    assert daily_revenue(sales) == [("2026-11-17", 10), ("2026-11-18", 0), ("2026-11-19", 0), ("2026-11-20", 50)]


def test_other_offset_and_start():
    # 10:00Z at UTC-5 is 05:00 local on the 17th, before a 06:00 start -> store day 16th
    assert daily_revenue([sale("2026-11-17T10:00:00Z")], utc_offset_hours=-5, day_starts_hour=6) == [("2026-11-16", 100)]
    assert daily_revenue([sale("2026-11-17T23:30:00Z")], utc_offset_hours=0, day_starts_hour=0) == [("2026-11-17", 100)]


def test_year_boundary():
    assert daily_revenue([sale("2026-12-31T19:00:00Z")]) == [("2026-12-31", 100)]
    assert daily_revenue([sale("2026-12-31T20:30:00Z")]) == [("2027-01-01", 100)]


def test_empty():
    assert daily_revenue([]) == []


def test_naive_timestamp_is_an_error():
    with pytest.raises(ValueError):
        daily_revenue([sale("2026-11-17T18:30:00")])
