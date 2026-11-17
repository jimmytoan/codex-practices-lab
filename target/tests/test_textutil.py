from shoplib.textutil import slugify, truncate


def test_slugify_basic():
    assert slugify("Blue  Mug (Large)") == "blue-mug-large"
    assert slugify("!!!") == "n-a"


def test_truncate():
    assert truncate("hello world", 8) == "hello..."
    assert truncate("short", 8) == "short"
