"""The ten coding tasks: prompts, scope, reference solutions and seeded bugs.

Reference solutions and seeded bugs are text edits (path, old, new) applied to the target repo.
They exist only for the self-test and for the review test (test 6); the agent never sees them,
except the seeded-bug patch that test 6 hands to the agent on purpose.
"""

from __future__ import annotations

from dataclasses import dataclass, field

Edit = tuple[str, str, str]  # (path relative to repo, old text, new text)


@dataclass
class Task:
    id: str
    one_line: str
    goal: str
    context: str
    constraints: str
    done_when: str
    scope: list[str]  # glob patterns of paths the task may touch
    edits: list[Edit]  # reference solution without the ShopError rule
    rule_edits: list[Edit] = field(default_factory=list)  # turn the reference into one that follows the rule
    bugs: dict[str, list[Edit]] = field(default_factory=dict)  # seeded bugs, each applied on top of the full reference

    @property
    def has_rule(self) -> bool:
        return bool(self.rule_edits)

    def four_part(self) -> str:
        return (f"Goal: {self.goal}\n\nContext: {self.context}\n\n"
                f"Constraints: {self.constraints}\n\nDone when: {self.done_when}")

    def reference(self) -> list[Edit]:
        return self.edits + self.rule_edits


IMPORT_SHOPERROR_SHIPPING = ('src/shoplib/shipping.py', '"""Shipping costs and parcel splitting. See docs/shipping.md."""\n',
                             '"""Shipping costs and parcel splitting. See docs/shipping.md."""\n\nfrom .errors import ShopError\n')

RELEASE_BODY = '''        if qty <= 0:
            raise ValueError("qty must be positive")
        if qty > self.reserved(sku):
            raise ValueError(f"only {self.reserved(sku)} of {sku} reserved")
        self._reserved[sku] -= qty
'''
RELEASE_EDIT = ("src/shoplib/inventory.py", "        changes nothing.\n        \"\"\"\n        raise NotImplementedError\n",
                "        changes nothing.\n        \"\"\"\n" + RELEASE_BODY)

TASKS: dict[str, Task] = {}


def add(task: Task) -> None:
    TASKS[task.id] = task


add(Task(
    id="t01-shipping-boundary",
    one_line="Fix the shipping cost: a parcel of exactly 1000 g is charged 800 instead of 500.",
    goal="Make shipping_cost charge the tier a parcel's weight falls into, with each tier's upper bound inclusive.",
    context="The tiers are specified in docs/shipping.md. The code is shipping_cost in src/shoplib/shipping.py; "
            "its tests are in tests/test_shipping.py.",
    constraints="Change only src/shoplib/shipping.py and files in tests/. Keep the function's signature.",
    done_when="Weights exactly on a tier bound (1000, 2000, 5000 and 20000 g) cost that tier's price, invalid weights "
              "still raise, and `python -m pytest -q` passes.",
    scope=["src/shoplib/shipping.py", "tests/*"],
    edits=[("src/shoplib/shipping.py", "        if weight_g < limit:\n", "        if weight_g <= limit:\n")],
    rule_edits=[
        IMPORT_SHOPERROR_SHIPPING,
        ("src/shoplib/shipping.py", 'raise ValueError("weight must be positive")', 'raise ShopError("weight must be positive")'),
        ("src/shoplib/shipping.py", 'raise ValueError("parcel is too heavy")', 'raise ShopError("parcel is too heavy")'),
    ],
))

add(Task(
    id="t02-bulk-discount",
    one_line="Add a 5% bulk discount to cart lines with 10 or more units.",
    goal="A cart line with 10 or more units gets 5% off that line's total.",
    context="The cart is in src/shoplib/cart.py. Money rules are in docs/CONVENTIONS.md and the money helpers in "
            "src/shoplib/money.py.",
    constraints="Change only src/shoplib/cart.py and files in tests/. Money stays integer cents.",
    done_when="line_total and subtotal include the discount, lines under 10 units are unchanged, and "
              "`python -m pytest -q` passes.",
    scope=["src/shoplib/cart.py", "tests/*"],
    edits=[
        ("src/shoplib/cart.py", "from dataclasses import dataclass\n",
         "from dataclasses import dataclass\n\nfrom .money import percent_of\n\nBULK_QTY = 10\nBULK_PERCENT = 5\n"),
        ("src/shoplib/cart.py", "        line = self._lines[sku]\n        return line.unit_price_cents * line.qty\n",
         "        line = self._lines[sku]\n        total = line.unit_price_cents * line.qty\n"
         "        if line.qty >= BULK_QTY:\n            total -= percent_of(total, BULK_PERCENT)\n        return total\n"),
    ],
))

add(Task(
    id="t03-inventory-release",
    one_line="Implement Inventory.release.",
    goal="Implement Inventory.release so reserved stock can be given back.",
    context="Inventory is in src/shoplib/inventory.py; the release docstring is the spec. Tests are in "
            "tests/test_inventory.py.",
    constraints="Change only src/shoplib/inventory.py and files in tests/. Do not change the other methods.",
    done_when="release behaves as its docstring says, including every error case, and `python -m pytest -q` passes.",
    scope=["src/shoplib/inventory.py", "tests/*"],
    edits=[RELEASE_EDIT],
    rule_edits=[
        ("src/shoplib/inventory.py", '"""Stock levels: on hand, reserved for orders, and available."""\n',
         '"""Stock levels: on hand, reserved for orders, and available."""\n\nfrom .errors import ShopError\n'),
        ("src/shoplib/inventory.py", '        changes nothing.\n        """\n' + RELEASE_BODY,
         '        changes nothing.\n        """\n' + RELEASE_BODY.replace("raise ValueError", "raise ShopError")),
    ],
    bugs={
        "checks-on-hand": [("src/shoplib/inventory.py", "        if qty > self.reserved(sku):\n            raise ShopError(f\"only {self.reserved(sku)} of {sku} reserved\")\n        self._reserved[sku] -= qty\n",
                            "        if qty > self.on_hand(sku):\n            raise ShopError(f\"only {self.reserved(sku)} of {sku} reserved\")\n        self._reserved[sku] -= qty\n")],
        "accepts-zero": [("src/shoplib/inventory.py","        changes nothing.\n        \"\"\"\n        if qty <= 0:\n",
                          "        changes nothing.\n        \"\"\"\n        if qty < 0:\n")],
    },
))

CANCEL = '''    def cancel(self) -> None:
        """Cancel the order. See docs/order-states.md."""
        if self.state == CANCELLED:
            return
        if self.state not in (NEW, PAID):
            raise ValueError(f"cannot go from {self.state} to {CANCELLED}")
        for sku, qty in self.lines.items():
            self.inventory.release(sku, qty)
        self.refund_due = self.state == PAID
        self.state = CANCELLED

    def deliver(self) -> None:
'''

add(Task(
    id="t04-order-cancel",
    one_line="Add a cancel() method to Order.",
    goal="Orders can be cancelled.",
    context="The order life cycle and the cancel rules are in docs/order-states.md. Order is in src/shoplib/orders.py "
            "and uses Inventory from src/shoplib/inventory.py, whose release method is not implemented yet.",
    constraints="Change only src/shoplib/orders.py, src/shoplib/inventory.py and files in tests/.",
    done_when="Order.cancel follows every rule in docs/order-states.md and `python -m pytest -q` passes.",
    scope=["src/shoplib/orders.py", "src/shoplib/inventory.py", "tests/*"],
    edits=[RELEASE_EDIT, ("src/shoplib/orders.py", "    def deliver(self) -> None:\n", CANCEL)],
    rule_edits=[
        ("src/shoplib/orders.py", "from .inventory import Inventory\n", "from .errors import ShopError\nfrom .inventory import Inventory\n"),
        ("src/shoplib/orders.py", 'raise ValueError(f"cannot go from {self.state} to {CANCELLED}")',
         'raise ShopError(f"cannot go from {self.state} to {CANCELLED}")'),
    ],
))

add(Task(
    id="t05-csv-quoting",
    one_line="Product names with commas break the CSV report. Fix it.",
    goal="to_csv produces valid CSV for any field value.",
    context="to_csv is in src/shoplib/reports.py. The CSV rules are in docs/CONVENTIONS.md.",
    constraints="Change only src/shoplib/reports.py and files in tests/. Output for plain values must not change.",
    done_when="Fields containing a comma, a double quote or a newline are quoted as the conventions say, and "
              "`python -m pytest -q` passes.",
    scope=["src/shoplib/reports.py", "tests/*"],
    edits=[
        ("src/shoplib/reports.py", 'COLUMNS = ["sku", "name", "units", "revenue_cents"]\n',
         'COLUMNS = ["sku", "name", "units", "revenue_cents"]\n\n\ndef _field(value) -> str:\n    text = str(value)\n'
         '    if any(ch in text for ch in \',"\\n\'):\n        return \'"\' + text.replace(\'"\', \'""\') + \'"\'\n    return text\n'),
        ("src/shoplib/reports.py", '        lines.append(",".join(str(row[col]) for col in COLUMNS))\n',
         '        lines.append(",".join(_field(row[col]) for col in COLUMNS))\n'),
    ],
))

DATES_OLD = '''    # TODO: holidays and negative n are not handled yet
    day = start
    while n > 0:
        day += timedelta(days=1)
        if day.weekday() < 5:
            n -= 1
    return day
'''
DATES_NEW = '''    holidays = set(holidays)
    day = start
    if n == 0:
        while not is_business_day(day, holidays):
            day += timedelta(days=1)
        return day
    step = 1 if n > 0 else -1
    remaining = abs(n)
    while remaining:
        day += timedelta(days=step)
        if is_business_day(day, holidays):
            remaining -= 1
    return day
'''

add(Task(
    id="t06-business-days",
    one_line="Finish add_business_days: it ignores holidays and negative n.",
    goal="Complete add_business_days.",
    context="add_business_days is in src/shoplib/dates.py; its docstring is the spec. Tests are in tests/test_dates.py.",
    constraints="Change only src/shoplib/dates.py and files in tests/. Keep the signature.",
    done_when="Holidays, negative n and n == 0 behave as the docstring says, and `python -m pytest -q` passes.",
    scope=["src/shoplib/dates.py", "tests/*"],
    edits=[("src/shoplib/dates.py", DATES_OLD, DATES_NEW)],
    bugs={
        "zero-does-not-move": [("src/shoplib/dates.py",
                                "    if n == 0:\n        while not is_business_day(day, holidays):\n            day += timedelta(days=1)\n        return day\n",
                                "    if n == 0:\n        return day\n")],
        "backward-ignores-holidays": [("src/shoplib/dates.py", "        if is_business_day(day, holidays):\n            remaining -= 1\n",
                                       "        if is_business_day(day, holidays if step > 0 else ()):\n            remaining -= 1\n")],
    },
))

COUPONS_NEW = '''    if subtotal_cents < 0:
        raise ValueError("subtotal must not be negative")
    eligible = [
        c for c in coupons
        if (c.expires is None or today <= c.expires) and subtotal_cents >= c.min_subtotal_cents
    ]
    percents = sorted((c for c in eligible if c.kind == "percent"), key=lambda c: (-c.value, c.code))
    total = subtotal_cents
    applied = []
    if percents:
        total -= percent_of(subtotal_cents, percents[0].value)
        applied.append(percents[0].code)
    for c in eligible:
        if c.kind == "fixed":
            total -= c.value
            applied.append(c.code)
    return max(total, 0), sorted(applied)
'''
COUPONS_OLD = '    """Apply several coupons following the rules in docs/discounts.md."""\n    raise NotImplementedError\n'

add(Task(
    id="t07-coupon-stacking",
    one_line="Implement apply_coupons.",
    goal="Implement apply_coupons so several coupons can be combined on one order.",
    context="The rules are in docs/discounts.md. The code is in src/shoplib/discounts.py and the money helpers in "
            "src/shoplib/money.py.",
    constraints="Change only src/shoplib/discounts.py and files in tests/. Do not change apply_coupon or Coupon.",
    done_when="Every rule in docs/discounts.md holds and `python -m pytest -q` passes.",
    scope=["src/shoplib/discounts.py", "tests/*"],
    edits=[("src/shoplib/discounts.py", COUPONS_OLD, COUPONS_OLD.split("    raise")[0] + COUPONS_NEW)],
    rule_edits=[
        ("src/shoplib/discounts.py", "from .money import percent_of\n", "from .errors import ShopError\nfrom .money import percent_of\n"),
        ("src/shoplib/discounts.py", '    if subtotal_cents < 0:\n        raise ValueError("subtotal must not be negative")\n    eligible',
         '    if subtotal_cents < 0:\n        raise ShopError("subtotal must not be negative")\n    eligible'),
    ],
    bugs={
        "expiry-day-excluded": [("src/shoplib/discounts.py", "today <= c.expires", "today < c.expires")],
        "tie-not-by-code": [("src/shoplib/discounts.py", "key=lambda c: (-c.value, c.code))", "key=lambda c: -c.value)")],
    },
))

add(Task(
    id="t08-cli-json",
    one_line="Add a --format json option to the report command.",
    goal="`python -m shoplib.cli report SALES_JSON --format json` prints the sales summary as JSON.",
    context="The command is in src/shoplib/cli.py and documented in docs/cli.md. Output conventions are in "
            "docs/CONVENTIONS.md.",
    constraints="Change only src/shoplib/cli.py, docs/cli.md and files in tests/. CSV stays the default and its output "
                "does not change.",
    done_when="--format accepts csv or json, the JSON output follows the conventions, an unknown format is a usage "
              "error, and `python -m pytest -q` passes.",
    scope=["src/shoplib/cli.py", "docs/cli.md", "tests/*"],
    edits=[
        ("src/shoplib/cli.py", '    report.add_argument("sales_json", help="file with a JSON list of sales")\n',
         '    report.add_argument("sales_json", help="file with a JSON list of sales")\n'
         '    report.add_argument("--format", choices=["csv", "json"], default="csv")\n'),
        ("src/shoplib/cli.py", "        sys.stdout.write(to_csv(sales_summary(sales)))\n",
         "        rows = sales_summary(sales)\n        if args.format == \"json\":\n"
         "            sys.stdout.write(json.dumps(rows, indent=2, sort_keys=True) + \"\\n\")\n"
         "        else:\n            sys.stdout.write(to_csv(rows))\n"),
    ],
))

add(Task(
    id="t09-slug-accents",
    one_line="slugify mangles accented names like 'Crème Brûlée'. Fix it.",
    goal="slugify handles accented letters.",
    context="slugify is in src/shoplib/textutil.py; its docstring is the spec. Tests are in tests/test_textutil.py.",
    constraints="Change only src/shoplib/textutil.py and files in tests/. Standard library only.",
    done_when="Every rule in the docstring holds, including max_len, and `python -m pytest -q` passes.",
    scope=["src/shoplib/textutil.py", "tests/*"],
    edits=[
        ("src/shoplib/textutil.py", "import re\n", "import re\nimport unicodedata\n"),
        ("src/shoplib/textutil.py", '    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")\n',
         '    decomposed = unicodedata.normalize("NFKD", text)\n'
         '    text = "".join(ch for ch in decomposed if not unicodedata.combining(ch))\n'
         '    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")\n'),
    ],
))

SPLIT_OLD = '''def split_parcels(items: list[tuple[str, int, int]], max_weight_g: int) -> list[list[str]]:
    """Split order items into parcels. See docs/shipping.md."""
    raise NotImplementedError


def shipment_cost(items: list[tuple[str, int, int]], max_weight_g: int) -> int:
    """Total shipping cost of an order. See docs/shipping.md."""
    raise NotImplementedError
'''
SPLIT_NEW = '''def _pack(items, max_weight_g):
    units = []
    for sku, weight, qty in items:
        if qty < 1 or weight < 1:
            raise ValueError(f"bad item {sku}")
        if weight > max_weight_g:
            raise ValueError(f"{sku} is heavier than a parcel may be")
        units.extend([(sku, weight)] * qty)
    units.sort(key=lambda unit: (-unit[1], unit[0]))
    parcels, loads = [], []
    for sku, weight in units:
        for i, load in enumerate(loads):
            if load + weight <= max_weight_g:
                parcels[i].append(sku)
                loads[i] += weight
                break
        else:
            parcels.append([sku])
            loads.append(weight)
    return parcels, loads


def split_parcels(items: list[tuple[str, int, int]], max_weight_g: int) -> list[list[str]]:
    """Split order items into parcels. See docs/shipping.md."""
    return _pack(items, max_weight_g)[0]


def shipment_cost(items: list[tuple[str, int, int]], max_weight_g: int) -> int:
    """Total shipping cost of an order. See docs/shipping.md."""
    return sum(shipping_cost(load) for load in _pack(items, max_weight_g)[1])
'''

add(Task(
    id="t10-split-parcels",
    one_line="Implement split_parcels and shipment_cost.",
    goal="Implement split_parcels and shipment_cost.",
    context="The algorithm is specified in docs/shipping.md. The code is in src/shoplib/shipping.py.",
    constraints="Change only src/shoplib/shipping.py and files in tests/. Do not change shipping_cost.",
    done_when="split_parcels follows the spec exactly, including unit order and error cases, shipment_cost uses it, "
              "and `python -m pytest -q` passes.",
    scope=["src/shoplib/shipping.py", "tests/*"],
    edits=[("src/shoplib/shipping.py", SPLIT_OLD, SPLIT_NEW)],
    rule_edits=[
        IMPORT_SHOPERROR_SHIPPING,
        ("src/shoplib/shipping.py", 'raise ValueError(f"bad item {sku}")', 'raise ShopError(f"bad item {sku}")'),
        ("src/shoplib/shipping.py", 'raise ValueError(f"{sku} is heavier than a parcel may be")',
         'raise ShopError(f"{sku} is heavier than a parcel may be")'),
    ],
    bugs={
        "exact-fit-rejected": [("src/shoplib/shipping.py", "if load + weight <= max_weight_g:", "if load + weight < max_weight_g:")],
        "accepts-zero-qty": [("src/shoplib/shipping.py", "if qty < 1 or weight < 1:", "if qty < 0 or weight < 1:")],
    },
))

from . import tasks_hard  # noqa: E402,F401  (registers t11-t14)

RULE_TASKS = [t for t, task in TASKS.items() if task.has_rule]
SEEDED_TASKS = [t for t, task in TASKS.items() if task.bugs]
