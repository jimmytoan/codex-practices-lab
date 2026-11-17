import pytest

from shoplib.search import Product, search

P = [
    Product("MUG-1", "Blue Mug", 1200, ["kitchen", "sale"]),
    Product("MUG-2", "Red Mug", 900, ["kitchen"]),
    Product("BWL-1", "Blue Bowl", 1500, ["Kitchen", "new"]),
    Product("TEE-1", "Mug Club T-shirt", 2500, ["apparel", "sale"]),
    Product("A*B", "Star Item", 100, []),
]


def skus(query):
    return [p.sku for p in search(P, query)]


def test_empty_query_matches_all():
    assert skus("") == ["MUG-1", "MUG-2", "BWL-1", "TEE-1", "A*B"]
    assert skus("   ") == ["MUG-1", "MUG-2", "BWL-1", "TEE-1", "A*B"]


def test_bare_words_are_substrings_and_all_must_match():
    assert skus("mug") == ["MUG-1", "MUG-2", "TEE-1"]
    assert skus("blue mug") == ["MUG-1"]
    assert skus("BLUE") == ["MUG-1", "BWL-1"]
    assert skus("pricey") == []


def test_quoted_phrase():
    assert skus('"mug club"') == ["TEE-1"]
    assert skus('"blue mug"') == ["MUG-1"]


def test_name_field():
    assert skus('name:"blue"') == ["MUG-1", "BWL-1"]
    assert skus('name:"blue mug"') == ["MUG-1"]
    assert skus("name:bowl") == ["BWL-1"]


def test_sku_is_exact_case_insensitive():
    assert skus("sku:mug-1") == ["MUG-1"]
    assert skus("sku:MUG") == []


def test_sku_prefix():
    assert skus("sku:MUG-*") == ["MUG-1", "MUG-2"]
    assert skus("sku:a*") == ["A*B"]


def test_star_inside_value_is_literal():
    assert skus("sku:A*B") == ["A*B"]


def test_tags():
    assert skus("tag:kitchen") == ["MUG-1", "MUG-2", "BWL-1"]
    assert skus("tag:KIT*") == ["MUG-1", "MUG-2", "BWL-1"]


def test_negation():
    assert skus("-tag:sale") == ["MUG-2", "BWL-1", "A*B"]
    assert skus("mug -tag:sale") == ["MUG-2"]
    assert skus('-"blue mug"') == ["MUG-2", "BWL-1", "TEE-1", "A*B"]


def test_price():
    assert skus("price>=1200") == ["MUG-1", "BWL-1", "TEE-1"]
    assert skus("price<1000") == ["MUG-2", "A*B"]
    assert skus("price=900") == ["MUG-2"]
    assert skus("price>1500 tag:sale") == ["TEE-1"]
    assert skus("-price>1000") == ["MUG-2", "A*B"]
    assert skus("price<=100") == ["A*B"]


def test_tab_separates_terms():
    assert skus("mug\ttag:sale") == ["MUG-1", "TEE-1"]


@pytest.mark.parametrize("query", ["colour:red", "price:5", "price>abc", "price>=12.5", "tag:", '"unclosed', "-", 'name:"open'])
def test_errors(query):
    with pytest.raises(ValueError):
        search(P, query)
