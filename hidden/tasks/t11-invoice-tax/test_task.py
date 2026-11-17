import pytest

from shoplib.invoice import build_invoice


def discounts(inv):
    return [line["discount_cents"] for line in inv["lines"]]


def test_no_coupon_de():
    inv = build_invoice([("A", 1000, 2, "standard"), ("B", 500, 1, "food")], 0, 0, "DE")
    assert inv["lines"] == [
        {"sku": "A", "gross_cents": 2000, "discount_cents": 0, "net_cents": 2000, "tax_cents": 380},
        {"sku": "B", "gross_cents": 500, "discount_cents": 0, "net_cents": 500, "tax_cents": 35},
    ]
    assert inv["shipping_tax_cents"] == 0
    assert inv["total_cents"] == 2915


def test_proportional_coupon():
    inv = build_invoice([("A", 1000, 2, "standard"), ("B", 500, 1, "food")], 300, 0, "DE")
    assert discounts(inv) == [240, 60]
    assert [line["net_cents"] for line in inv["lines"]] == [1760, 440]
    # 19% of 1760 = 334.4 -> 334; 7% of 440 = 30.8 -> 31
    assert [line["tax_cents"] for line in inv["lines"]] == [334, 31]
    assert inv["total_cents"] == 1760 + 440 + 334 + 31


def test_largest_remainder_goes_to_largest_fraction_not_first_line():
    inv = build_invoice([("A", 200, 1, "standard"), ("B", 300, 1, "standard"), ("C", 500, 1, "standard")], 7, 0, "DE")
    # exact shares 1.4, 2.1, 3.5 -> floors 1, 2, 3; the left-over cent goes to C (remainder .5)
    assert discounts(inv) == [1, 2, 4]


def test_equal_remainders_go_to_earlier_line():
    inv = build_invoice([("A", 100, 1, "standard"), ("B", 100, 1, "standard"), ("C", 100, 1, "standard")], 100, 0, "OR")
    assert discounts(inv) == [34, 33, 33]
    inv = build_invoice([("A", 100, 1, "standard"), ("B", 100, 1, "standard"), ("C", 100, 1, "standard")], 200, 0, "OR")
    assert discounts(inv) == [67, 67, 66]


@pytest.mark.parametrize("coupon", [1, 2, 3, 99, 101, 997, 1234])
def test_discounts_always_add_up(coupon):
    lines = [("A", 333, 1, "standard"), ("B", 667, 3, "food"), ("C", 1, 7, "books"), ("D", 250, 2, "standard")]
    inv = build_invoice(lines, coupon, 0, "OR")
    assert sum(discounts(inv)) == coupon
    assert all(d >= 0 for d in discounts(inv))


def test_coupon_capped_at_gross():
    inv = build_invoice([("A", 1000, 1, "standard"), ("B", 500, 1, "standard")], 5000, 400, "DE")
    assert discounts(inv) == [1000, 500]
    assert [line["tax_cents"] for line in inv["lines"]] == [0, 0]
    assert inv["shipping_tax_cents"] == 76
    assert inv["total_cents"] == 476


def test_tax_rounded_per_line():
    inv = build_invoice([("A", 3, 1, "standard"), ("B", 3, 1, "standard")], 0, 0, "DE")
    # 19% of 3 = 0.57 -> 1 per line; on the total it would be 1.14 -> 1
    assert [line["tax_cents"] for line in inv["lines"]] == [1, 1]
    assert inv["total_cents"] == 8


def test_tax_half_up():
    inv = build_invoice([("A", 50, 1, "food")], 0, 0, "SG")
    assert inv["lines"][0]["tax_cents"] == 5  # 9% of 50 = 4.5


def test_shipping_not_taxed_when_no_line_is_taxed():
    inv = build_invoice([("A", 1000, 1, "books")], 0, 500, "SG")
    assert inv["shipping_tax_cents"] == 0
    assert inv["total_cents"] == 1500


def test_shipping_taxed_at_standard_rate():
    inv = build_invoice([("A", 1000, 1, "books"), ("B", 100, 1, "food")], 0, 500, "SG")
    assert inv["shipping_tax_cents"] == 45
    inv = build_invoice([("A", 1000, 1, "food")], 0, 500, "DE")
    assert inv["shipping_tax_cents"] == 95  # standard 19%, not the food rate
    assert inv["shipping_cents"] == 500


def test_zero_gross_with_coupon():
    inv = build_invoice([("A", 0, 1, "standard")], 100, 200, "OR")
    assert discounts(inv) == [0]
    assert inv["total_cents"] == 200


@pytest.mark.parametrize("args", [
    ([("A", 100, 1, "standard")], 0, 0, "FR"),
    ([("A", 100, 1, "toys")], 0, 0, "DE"),
    ([], 0, 0, "DE"),
    ([("A", 100, 0, "standard")], 0, 0, "DE"),
    ([("A", -1, 1, "standard")], 0, 0, "DE"),
    ([("A", 100, 1, "standard")], -1, 0, "DE"),
    ([("A", 100, 1, "standard")], 0, -1, "DE"),
])
def test_errors(args):
    with pytest.raises(ValueError):
        build_invoice(*args)
