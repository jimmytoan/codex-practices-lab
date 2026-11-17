import json

from shoplib.cli import main


def test_report_csv(tmp_path, capsys):
    path = tmp_path / "sales.json"
    path.write_text(json.dumps([{"sku": "A", "name": "Mug", "qty": 2, "unit_price_cents": 450}]))
    assert main(["report", str(path)]) == 0
    assert capsys.readouterr().out == "sku,name,units,revenue_cents\nA,Mug,2,900\n"
