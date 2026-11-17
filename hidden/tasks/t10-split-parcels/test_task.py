import pytest

from shoplib.shipping import shipment_cost, split_parcels


def test_empty():
    assert split_parcels([], 5000) == []
    assert shipment_cost([], 5000) == 0


def test_single_parcel():
    assert split_parcels([("A", 1200, 2), ("B", 300, 1)], 5000) == [["A", "A", "B"]]


def test_heaviest_first_and_first_fit():
    items = [("S", 1500, 2), ("L", 3000, 1), ("M", 2500, 1)]
    # units: L3000, M2500, S1500, S1500
    # L -> p1 (3000); M -> p2 (2500); S -> p1 (4500); S -> p2 (4000)
    assert split_parcels(items, 5000) == [["L", "S"], ["M", "S"]]


def test_ties_ordered_by_sku():
    items = [("Z", 1000, 1), ("A", 1000, 1), ("M", 1000, 1)]
    assert split_parcels(items, 2000) == [["A", "M"], ["Z"]]


def test_exact_fit_is_allowed():
    assert split_parcels([("A", 2500, 2)], 5000) == [["A", "A"]]
    assert split_parcels([("A", 2500, 3)], 5000) == [["A", "A"], ["A"]]


def test_first_fit_not_best_fit():
    items = [("A", 600, 1), ("B", 500, 1), ("C", 400, 1), ("D", 300, 1), ("E", 200, 1)]
    # max 1000: A -> p1 (600); B -> p2 (500); C -> p1 (1000); D -> p2 (800); E -> p2 (1000)
    assert split_parcels(items, 1000) == [["A", "C"], ["B", "D", "E"]]


def test_later_small_unit_fills_earlier_parcel():
    items = [("A", 700, 2), ("B", 400, 1), ("C", 300, 2)]
    # A -> p1 (700); A -> p2 (700); B -> p3 (400); C -> p1 (1000); C -> p2 (1000)
    assert split_parcels(items, 1000) == [["A", "C"], ["A", "C"], ["B"]]


def test_unit_too_heavy():
    with pytest.raises(ValueError):
        split_parcels([("A", 5001, 1)], 5000)


@pytest.mark.parametrize("item", [("A", 100, 0), ("A", 100, -1), ("A", 0, 1), ("A", -5, 1)])
def test_bad_item(item):
    with pytest.raises(ValueError):
        split_parcels([item], 5000)


def test_input_not_mutated():
    items = [("B", 300, 1), ("A", 1200, 2)]
    split_parcels(items, 5000)
    assert items == [("B", 300, 1), ("A", 1200, 2)]


def test_shipment_cost():
    items = [("S", 1500, 2), ("L", 3000, 1), ("M", 2500, 1)]
    # parcels weigh 4500 and 4000 -> 1200 + 1200
    assert shipment_cost(items, 5000) == 2400
    # parcels weigh 1900, 1900, 300 -> 800 + 800 + 500
    assert shipment_cost([("A", 700, 2), ("B", 300, 1), ("C", 1200, 2)], 1900) == 2100
