"""Build the AGENTS.md variants: none, short, bloated, rule_early, rule_late.

  python -m harness.agentsmd   # (re)write conditions/*.md and print their sizes

The filler is generated deterministically and is deliberately the kind of thing that piles up in real
instruction files: a long changelog, a glossary and generic advice. It never mentions error types, money
rounding or anything a hidden test depends on.
"""

from __future__ import annotations

import random

from .config import CONDITIONS

LIMIT = 32 * 1024  # project_doc_max_bytes default

RULE_MARKER = "shoplib.errors.ShopError"
RULE = ("- Raise `shoplib.errors.ShopError` (defined in src/shoplib/errors.py, a ValueError subclass), never a bare "
        "`ValueError`, for invalid arguments and disallowed operations in any code you write or change.\n")

SHORT_HEAD = """# AGENTS.md

## Layout
- `src/shoplib/`: library code, one module per area (cart, inventory, orders, shipping, discounts, dates, textutil, reports, cli).
- `tests/`: pytest tests, one file per module.
- `docs/`: specs. `docs/CONVENTIONS.md` has the money, error and output rules; read it before changing money or output code.

## Commands
- Test: `python -m pytest -q`
- No build or lint step. Standard library only; do not add dependencies.

## Rules
- Money is integer cents. Percentages go through `shoplib.money.percent_of` (rounds half up). Never use `round()` or float for money.
"""
SHORT_TAIL = """- Do not modify `src/shoplib/legacy_pricing.py`; an external importer depends on it.
- Keep changes to the files the task needs.

## Done means
- The behaviour asked for, and the spec it refers to, holds, with tests for it in `tests/`.
- `python -m pytest -q` passes.
"""

AREAS = ["cart", "inventory", "orders", "shipping", "discounts", "dates", "reports", "cli", "textutil", "docs", "tests"]
VERBS = ["Tidy", "Clarify", "Rename internals in", "Document", "Simplify", "Reorder imports in", "Expand tests for",
         "Improve messages in", "Refactor helpers in", "Speed up"]
OBJECTS = ["edge cases", "the public API notes", "naming", "docstrings", "examples", "the README section",
           "type hints", "internal helpers", "test fixtures", "comments"]
GLOSSARY = [
    ("SKU", "stock keeping unit; the identifier of a product variant"), ("Line", "one SKU in a cart with a quantity"),
    ("Subtotal", "sum of line totals before coupons"), ("Coupon", "a code that lowers the price of an order"),
    ("Reservation", "stock held for an order that has not shipped"), ("On hand", "units physically in the warehouse"),
    ("Available", "on hand minus reserved"), ("Parcel", "one box sent to a customer"),
    ("Tier", "a weight band with one shipping price"), ("Order", "a confirmed purchase with a life cycle"),
    ("Refund", "money returned to a customer"), ("Slug", "the URL-safe form of a product name"),
    ("Report", "an export of sales data"), ("Business day", "a weekday that is not a holiday"),
    ("Importer", "the nightly job that loads supplier prices"), ("Fulfilment", "picking, packing and shipping"),
]
ADVICE = [
    "Prefer small, focused functions with clear names.", "Write code that is easy to read before code that is clever.",
    "Leave the code a little better than you found it.", "Keep pull requests small enough to review in one sitting.",
    "Explain why in comments, not what.", "Avoid deep nesting; return early.", "Name things after what they mean in the shop.",
    "Delete dead code instead of commenting it out.", "Do not optimise without measuring first.",
    "Keep modules cohesive; one area per module.", "Write tests that describe behaviour, not implementation.",
    "Be consistent with the surrounding code.", "Prefer plain data structures over clever classes.",
    "Avoid global state.", "Make invalid states hard to represent.", "Keep functions pure where you can.",
    "Think about the reader who comes after you.", "When in doubt, ask in the team channel.",
]


def filler(target_bytes: int, seed: int = 7) -> str:
    rnd = random.Random(seed)
    parts = ["\n## Team notes\n\nThese notes collect things the team has agreed over time. Most are general.\n\n### Working style\n"]
    for line in ADVICE:
        parts.append(f"- {line}\n")
    parts.append("\n### Glossary\n")
    for term, meaning in GLOSSARY:
        parts.append(f"- **{term}**: {meaning}.\n")
    parts.append("\n### Changelog\n")
    text = "".join(parts)
    version, n = [0, 4, 0], 0
    while len(text.encode()) < target_bytes:
        if n % 12 == 0:
            text += f"\n#### {version[0]}.{version[1]}.{version[2]}\n"
            version[2] = (version[2] + 1) % 10
            if version[2] == 0:
                version[1] = max(version[1] - 1, 0)
        n += 1
        text += (f"- {rnd.choice(VERBS)} {rnd.choice(AREAS)}: {rnd.choice(OBJECTS)} "
                 f"(SHOP-{rnd.randint(100, 999)}). {rnd.choice(ADVICE)}\n")
    return text


def build(kind: str) -> str | None:
    """The AGENTS.md text for a condition, or None for no file."""
    short = SHORT_HEAD + RULE + SHORT_TAIL
    if kind == "none":
        return None
    if kind == "short":
        return short
    if kind == "bloated":  # the short file plus about 25 KiB of filler, still under the 32 KiB limit
        return short + filler(25 * 1024)
    if kind == "rule_early":  # rule in the first KiB, file well past the limit
        return short + filler(40 * 1024 - len(short.encode()))
    if kind == "rule_late":  # same size, rule moved to the end, past byte 32768
        body = SHORT_HEAD + SHORT_TAIL + filler(40 * 1024 - len(short.encode()))
        return body + "\n## Error handling\n" + RULE
    raise ValueError(kind)


KINDS = ["none", "short", "bloated", "rule_early", "rule_late"]


def write_all() -> dict[str, tuple[int, int | None]]:
    CONDITIONS.mkdir(exist_ok=True)
    sizes = {}
    for kind in KINDS:
        text = build(kind)
        if text is None:
            continue
        (CONDITIONS / f"AGENTS.{kind}.md").write_text(text)
        data = text.encode()
        sizes[kind] = (len(data), data.find(RULE_MARKER.encode()) if RULE_MARKER.encode() in data else None)
    return sizes


if __name__ == "__main__":
    for kind, (size, offset) in write_all().items():
        print(f"{kind:11s} {size:6d} bytes, rule at byte {offset}")
