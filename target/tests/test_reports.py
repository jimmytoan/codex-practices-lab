from shoplib.reports import sales_summary, to_csv

SALES = [
    {"sku": "B", "name": "Bowl", "qty": 1, "unit_price_cents": 900},
    {"sku": "A", "name": "Mug", "qty": 2, "unit_price_cents": 450},
    {"sku": "A", "name": "Mug", "qty": 1, "unit_price_cents": 450},
]


def test_summary():
    assert sales_summary(SALES) == [
        {"sku": "A", "name": "Mug", "units": 3, "revenue_cents": 1350},
        {"sku": "B", "name": "Bowl", "units": 1, "revenue_cents": 900},
    ]


def test_csv():
    assert to_csv(sales_summary(SALES)) == "sku,name,units,revenue_cents\nA,Mug,3,1350\nB,Bowl,1,900\n"
