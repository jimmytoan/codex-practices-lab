from shoplib.money import format_money, percent_of, round_cents


def test_round_half_up():
    assert round_cents("0.5") == 1
    assert round_cents("2.5") == 3
    assert round_cents("2.4") == 2


def test_percent_of():
    assert percent_of(1000, 15) == 150
    assert percent_of(333, 50) == 167


def test_format_money():
    assert format_money(1234) == "$12.34"
    assert format_money(-5) == "-$0.05"
