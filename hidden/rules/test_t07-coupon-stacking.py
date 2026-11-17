from datetime import date

import pytest
from shoplib.discounts import apply_coupons
from shoplib.errors import ShopError


def test_rule():
    with pytest.raises(ValueError) as exc:
        apply_coupons(-1, [], date(2026, 11, 17))
    assert type(exc.value) is ShopError
