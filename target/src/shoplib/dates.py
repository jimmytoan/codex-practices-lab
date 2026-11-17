"""Business-day arithmetic for delivery estimates."""

from datetime import date, timedelta


def is_business_day(day: date, holidays=()) -> bool:
    """Monday to Friday, and not listed in `holidays`."""
    return day.weekday() < 5 and day not in holidays


def add_business_days(start: date, n: int, holidays=()) -> date:
    """Move `n` business days from `start`.

    Business days are Monday to Friday that are not in `holidays`.

    - n > 0: the n-th business day strictly after `start`.
    - n < 0: the |n|-th business day strictly before `start`.
    - n == 0: `start` itself if it is a business day, otherwise the first
      business day after it.

    `start` does not have to be a business day.
    """
    # TODO: holidays and negative n are not handled yet
    day = start
    while n > 0:
        day += timedelta(days=1)
        if day.weekday() < 5:
            n -= 1
    return day
