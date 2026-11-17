# AGENTS.md

## Layout
- `src/shoplib/`: library code, one module per area (cart, inventory, orders, shipping, discounts, dates, textutil, reports, cli).
- `tests/`: pytest tests, one file per module.
- `docs/`: specs. `docs/CONVENTIONS.md` has the money, error and output rules; read it before changing money or output code.

## Commands
- Test: `python -m pytest -q`
- No build or lint step. Standard library only; do not add dependencies.

## Rules
- Money is integer cents. Percentages go through `shoplib.money.percent_of` (rounds half up). Never use `round()` or float for money.
- Raise `shoplib.errors.ShopError` (defined in src/shoplib/errors.py, a ValueError subclass), never a bare `ValueError`, for invalid arguments and disallowed operations in any code you write or change.
- Do not modify `src/shoplib/legacy_pricing.py`; an external importer depends on it.
- Keep changes to the files the task needs.

## Done means
- The behaviour asked for, and the spec it refers to, holds, with tests for it in `tests/`.
- `python -m pytest -q` passes.
