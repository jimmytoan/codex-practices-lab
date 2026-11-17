"""DEPRECATED price helpers, still imported by the old nightly importer.

Kept byte-for-byte compatible with the importer's expectations. Do not modify;
new code should use shoplib.money instead.
"""


def discounted(price, pct):
    # float maths on purpose: the importer compares against values stored this way
    return round(price * (1 - pct / 100.0), 2)


def with_tax(price, rate=0.08):
    return round(price + price * rate, 2)
