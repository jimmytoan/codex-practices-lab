import csv
import io

from shoplib.reports import to_csv

HEADER = "sku,name,units,revenue_cents\n"


def row(name, sku="A"):
    return {"sku": sku, "name": name, "units": 2, "revenue_cents": 900}


def parse(text):
    return list(csv.reader(io.StringIO(text, newline="")))


def test_plain_rows_are_unchanged():
    assert to_csv([row("Mug"), row("Bowl", "B")]) == HEADER + "A,Mug,2,900\nB,Bowl,2,900\n"


def test_comma_is_quoted():
    assert to_csv([row("Mug, large")]) == HEADER + 'A,"Mug, large",2,900\n'


def test_quote_is_doubled():
    assert to_csv([row('12" plate')]) == HEADER + 'A,"12"" plate",2,900\n'


def test_newline_in_field():
    text = to_csv([row("Gift\nset")])
    assert text == HEADER + 'A,"Gift\nset",2,900\n'
    assert parse(text)[1] == ["A", "Gift\nset", "2", "900"]


def test_no_carriage_returns():
    text = to_csv([row("Mug, large"), row("Bowl", "B")])
    assert "\r" not in text
    assert text.endswith("900\n")


def test_round_trip():
    names = ["Mug, large", '12" plate', 'He said "hi", twice', "plain"]
    text = to_csv([row(n, f"S{i}") for i, n in enumerate(names)])
    parsed = parse(text)
    assert parsed[0] == ["sku", "name", "units", "revenue_cents"]
    assert [r[1] for r in parsed[1:]] == names


def test_empty_rows_still_has_header():
    assert to_csv([]) == HEADER


def test_sku_with_comma_is_quoted_too():
    assert to_csv([row("Mug", "A,1")]) == HEADER + '"A,1",Mug,2,900\n'
