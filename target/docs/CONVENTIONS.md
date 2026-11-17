# Conventions

## Money
- Money is always an integer number of cents. Never use `float` for money.
- Percentages of an amount go through `shoplib.money.percent_of`, which rounds
  half up (0.5 of a cent rounds up). Do not use the built-in `round` for money:
  it rounds half to even.

## Errors
- Invalid arguments raise `ValueError` with a short message.
- A failed operation must leave state unchanged.

## Text output
- CSV: lines end with `\n` (never `\r\n`). Fields are quoted only when they
  contain a comma, a double quote or a newline; quotes inside a quoted field are
  doubled. The header row is always present.
- JSON: `json.dumps(obj, indent=2, sort_keys=True)` followed by one newline.
  Money stays in integer cents.

## Tests
- Tests live in `tests/`, one file per module, run with `python -m pytest -q`.
