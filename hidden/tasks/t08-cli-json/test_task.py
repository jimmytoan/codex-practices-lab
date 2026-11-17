import json

import pytest

from shoplib.cli import main

SALES = [
    {"sku": "B", "name": "Bowl", "qty": 1, "unit_price_cents": 900},
    {"sku": "A", "name": "Mug, large", "qty": 2, "unit_price_cents": 450},
]
ROWS = [
    {"sku": "A", "name": "Mug, large", "units": 2, "revenue_cents": 900},
    {"sku": "B", "name": "Bowl", "units": 1, "revenue_cents": 900},
]


@pytest.fixture
def sales_file(tmp_path):
    path = tmp_path / "sales.json"
    path.write_text(json.dumps(SALES))
    return str(path)


def test_json_content(sales_file, capsys):
    assert main(["report", sales_file, "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out) == ROWS


def test_json_layout_follows_conventions(sales_file, capsys):
    main(["report", sales_file, "--format", "json"])
    assert capsys.readouterr().out == json.dumps(ROWS, indent=2, sort_keys=True) + "\n"


def test_flag_before_file(sales_file, capsys):
    assert main(["report", "--format", "json", sales_file]) == 0
    assert json.loads(capsys.readouterr().out) == ROWS


def test_default_is_still_csv(sales_file, capsys):
    assert main(["report", sales_file]) == 0
    out = capsys.readouterr().out
    assert out.splitlines()[0] == "sku,name,units,revenue_cents"
    assert out.splitlines()[2] == "B,Bowl,1,900"


def test_explicit_csv(sales_file, capsys):
    assert main(["report", sales_file, "--format", "csv"]) == 0
    assert capsys.readouterr().out.startswith("sku,name,units,revenue_cents\n")


def test_unknown_format_is_a_usage_error(sales_file, capsys):
    with pytest.raises(SystemExit) as exc:
        main(["report", sales_file, "--format", "xml"])
    assert exc.value.code == 2


def test_empty_sales_json(tmp_path, capsys):
    path = tmp_path / "empty.json"
    path.write_text("[]")
    main(["report", str(path), "--format", "json"])
    assert capsys.readouterr().out == "[]\n"
