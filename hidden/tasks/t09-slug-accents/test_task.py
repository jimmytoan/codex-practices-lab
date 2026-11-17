import pytest

from shoplib.textutil import slugify


@pytest.mark.parametrize(
    "text,slug",
    [
        ("Crème Brûlée", "creme-brulee"),
        ("Señor Piñata", "senor-pinata"),
        ("Žluťoučký kůň", "zlutoucky-kun"),
        ("ÅNGSTRÖM unit", "angstrom-unit"),
        ("Café—au lait", "cafe-au-lait"),
    ],
)
def test_accents(text, slug):
    assert slugify(text) == slug


def test_plain_names_unchanged():
    assert slugify("Blue  Mug (Large)") == "blue-mug-large"
    assert slugify("  --Hello, World!--  ") == "hello-world"
    assert slugify("USB-C 2m") == "usb-c-2m"


def test_empty():
    assert slugify("") == "n-a"
    assert slugify("!!!") == "n-a"
    assert slugify("日本") == "n-a"


def test_max_len_counts_after_transliteration():
    assert slugify("Crème Brûlée", max_len=5) == "creme"
    assert slugify("éééééééééé", max_len=4) == "eeee"


def test_cut_never_leaves_trailing_dash():
    assert slugify("Crème Brûlée", max_len=6) == "creme"
    assert slugify("ab cd ef", max_len=3) == "ab"
