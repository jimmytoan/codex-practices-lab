"""The four harder tasks (t11-t14), added after the pilot hit a 100% pass rate on t01-t10.

Each is a spec-heavy function with many rules, some easy to miss. Same structure as harness/tasks.py.
"""

from __future__ import annotations

from .tasks import Task, add

INVOICE_OLD = '    """Build an invoice for an order. See docs/invoicing.md."""\n    raise NotImplementedError\n'
INVOICE_NEW = '''    """Build an invoice for an order. See docs/invoicing.md."""
    if region not in TAX_RATES:
        raise ValueError(f"unknown region {region!r}")
    if not lines:
        raise ValueError("an invoice needs at least one line")
    if coupon_cents < 0 or shipping_cents < 0:
        raise ValueError("coupon and shipping must not be negative")
    rates = TAX_RATES[region]
    gross = []
    for sku, price, qty, category in lines:
        if qty < 1 or price < 0:
            raise ValueError(f"bad line {sku}")
        if category not in rates:
            raise ValueError(f"unknown category {category!r}")
        gross.append(price * qty)
    total_gross = sum(gross)
    coupon = min(coupon_cents, total_gross)
    if total_gross == 0:
        alloc = [0] * len(gross)
    else:
        alloc = [coupon * g // total_gross for g in gross]
        rema = [coupon * g % total_gross for g in gross]
        order = sorted(range(len(gross)), key=lambda i: (-rema[i], i))
        for i in order[: coupon - sum(alloc)]:
            alloc[i] += 1
    out, total, any_taxed = [], 0, False
    for (sku, _price, _qty, category), g, d in zip(lines, gross, alloc):
        rate = rates[category]
        any_taxed = any_taxed or rate > 0
        net = g - d
        tax = percent_of(net, rate)
        out.append({"sku": sku, "gross_cents": g, "discount_cents": d, "net_cents": net, "tax_cents": tax})
        total += net + tax
    shipping_tax = percent_of(shipping_cents, rates["standard"]) if any_taxed else 0
    return {"lines": out, "shipping_cents": shipping_cents, "shipping_tax_cents": shipping_tax,
            "total_cents": total + shipping_cents + shipping_tax}
'''

add(Task(
    id="t11-invoice-tax",
    one_line="Implement build_invoice.",
    goal="Implement build_invoice: split an order-level coupon across the lines and compute tax.",
    context="The rules are in docs/invoicing.md. The code is in src/shoplib/invoice.py, with the tax rates in "
            "TAX_RATES. Money helpers are in src/shoplib/money.py and the money rules in docs/CONVENTIONS.md.",
    constraints="Change only src/shoplib/invoice.py and files in tests/. Do not change TAX_RATES.",
    done_when="Every numbered rule in docs/invoicing.md holds, including the coupon split and the error cases, and "
              "`python -m pytest -q` passes.",
    scope=["src/shoplib/invoice.py", "tests/*"],
    edits=[("src/shoplib/invoice.py", "# Tax rates in percent", "from .money import percent_of\n\n# Tax rates in percent"),
           ("src/shoplib/invoice.py", INVOICE_OLD, INVOICE_NEW)],
    bugs={
        "remainder-tie-to-later-line": [("src/shoplib/invoice.py", "key=lambda i: (-rema[i], i))", "key=lambda i: (-rema[i], -i))")],
        "tax-on-gross": [("src/shoplib/invoice.py", "tax = percent_of(net, rate)", "tax = percent_of(g, rate)")],
    },
))

SEARCH_OLD = '    """The products that match `query`, in their input order. See docs/search.md."""\n    raise NotImplementedError\n'
SEARCH_NEW = '''    """The products that match `query`, in their input order. See docs/search.md."""
    predicates = [_term(text, first_quote) for text, first_quote in _tokens(query)]
    return [p for p in products if all(pred(p) for pred in predicates)]


FIELDS = ("sku", "name", "tag")
PRICE = re.compile(r"price(<=|>=|<|>|=)(.*)\\Z", re.S)
OPS = {"<": operator.lt, "<=": operator.le, ">": operator.gt, ">=": operator.ge, "=": operator.eq}


def _tokens(query):
    """Split on whitespace outside quotes. Each token is (text without quotes, index where the first quote was)."""
    tokens, cur, in_quote, started, first_quote = [], [], False, False, None
    for ch in query:
        if ch == '"':
            if first_quote is None:
                first_quote = len(cur)
            in_quote = not in_quote
            started = True
        elif ch.isspace() and not in_quote:
            if started:
                tokens.append(("".join(cur), first_quote))
            cur, started, first_quote = [], False, None
        else:
            cur.append(ch)
            started = True
    if in_quote:
        raise ValueError("unclosed quote")
    if started:
        tokens.append(("".join(cur), first_quote))
    return tokens


def _term(text, first_quote):
    if text.startswith("-") and first_quote != 0:
        inner = _term_body(text[1:], None if first_quote is None else first_quote - 1)
        return lambda p: not inner(p)
    return _term_body(text, first_quote)


def _term_body(text, first_quote):
    if text == "" and first_quote is None:
        raise ValueError("empty term")
    unquoted = text if first_quote is None else text[:first_quote]
    m = PRICE.match(text) if first_quote is None else None
    if m:
        op, value = m.groups()
        if not re.fullmatch(r"[0-9]+", value):
            raise ValueError(f"bad price {value!r}")
        return lambda p: OPS[op](p.price_cents, int(value))
    if ":" in unquoted:
        field, value = text.split(":", 1)
        if field not in FIELDS:
            raise ValueError(f"unknown field {field!r}")
        if value == "":
            raise ValueError(f"empty value for {field}")
        v = value.lower()
        if field == "name":
            return lambda p: v in p.name.lower()
        if v.endswith("*"):
            prefix = v[:-1]
            if field == "sku":
                return lambda p: p.sku.lower().startswith(prefix)
            return lambda p: any(t.lower().startswith(prefix) for t in p.tags)
        if field == "sku":
            return lambda p: p.sku.lower() == v
        return lambda p: any(t.lower() == v for t in p.tags)
    word = text.lower()
    return lambda p: word in p.name.lower()
'''

add(Task(
    id="t12-search-query",
    one_line="Implement search.",
    goal="Implement product search with the query language in docs/search.md.",
    context="The spec is docs/search.md. The code is in src/shoplib/search.py.",
    constraints="Change only src/shoplib/search.py and files in tests/. Standard library only. Keep Product as it is.",
    done_when="Every rule in docs/search.md holds, including quoting, negation, prefixes, price comparisons and every "
              "error case, and `python -m pytest -q` passes.",
    scope=["src/shoplib/search.py", "tests/*"],
    edits=[("src/shoplib/search.py", "from dataclasses import dataclass, field\n",
            "import operator\nimport re\nfrom dataclasses import dataclass, field\n"),
           ("src/shoplib/search.py", SEARCH_OLD, SEARCH_NEW)],
    bugs={
        "name-is-exact": [("src/shoplib/search.py", "            return lambda p: v in p.name.lower()\n",
                           "            return lambda p: v == p.name.lower()\n")],
        "tags-case-sensitive": [("src/shoplib/search.py", "any(t.lower().startswith(prefix) for t in p.tags)",
                                 "any(t.startswith(prefix) for t in p.tags)"),
                                ("src/shoplib/search.py", "any(t.lower() == v for t in p.tags)", "any(t == v for t in p.tags)")],
    },
))

COSTING_OLD = '    """Process stock events and report cost per SKU. See docs/costing.md."""\n    raise NotImplementedError\n'
COSTING_NEW = '''    """Process stock events and report cost per SKU. See docs/costing.md."""
    lots: dict[str, list[list[int]]] = {}
    cogs: dict[str, int] = {}
    last_sale: dict[str, dict] = {}
    for ev in events:
        kind, sku, qty = ev["type"], ev["sku"], ev["qty"]
        if qty < 1:
            raise ValueError("qty must be at least 1")
        lots.setdefault(sku, [])
        cogs.setdefault(sku, 0)
        if kind == "receive":
            if ev["unit_cost_cents"] < 0:
                raise ValueError("unit cost must not be negative")
            lots[sku].append([qty, ev["unit_cost_cents"]])
        elif kind == "sell":
            if qty > sum(q for q, _ in lots[sku]):
                raise ValueError(f"not enough {sku} on hand")
            need, cost = qty, 0
            while need:
                lot = lots[sku][0]
                take = min(need, lot[0])
                cost += take * lot[1]
                lot[0] -= take
                need -= take
                if lot[0] == 0:
                    lots[sku].pop(0)
            cogs[sku] += cost
            last_sale[sku] = {"qty": qty, "cost": cost, "returned": 0}
        elif kind == "return":
            sale = last_sale.get(sku)
            if sale is None or qty > sale["qty"] - sale["returned"]:
                raise ValueError(f"cannot return {qty} of {sku}")
            unit = round_cents(Decimal(sale["cost"]) / sale["qty"])
            sale["returned"] += qty
            lots[sku].append([qty, unit])
            cogs[sku] -= qty * unit
        else:
            raise ValueError(f"unknown event type {kind!r}")
    return {sku: {"cogs_cents": cogs[sku], "on_hand": sum(q for q, _ in lots[sku]),
                  "value_cents": sum(q * c for q, c in lots[sku])} for sku in lots}
'''

add(Task(
    id="t13-fifo-costing",
    one_line="Implement fifo_costing.",
    goal="Implement fifo_costing: FIFO cost of goods sold, including customer returns.",
    context="The spec is docs/costing.md. The code is in src/shoplib/costing.py; money helpers are in "
            "src/shoplib/money.py.",
    constraints="Change only src/shoplib/costing.py and files in tests/. Money stays integer cents.",
    done_when="Every rule in docs/costing.md holds, including how returns are costed and ordered and every error "
              "case, and `python -m pytest -q` passes.",
    scope=["src/shoplib/costing.py", "tests/*"],
    edits=[("src/shoplib/costing.py", '"""Cost of goods sold with FIFO lots. See docs/costing.md."""\n',
            '"""Cost of goods sold with FIFO lots. See docs/costing.md."""\n\nfrom decimal import Decimal\n\nfrom .money import round_cents\n'),
           ("src/shoplib/costing.py", COSTING_OLD, COSTING_NEW)],
    bugs={
        "return-cost-floored": [("src/shoplib/costing.py", 'unit = round_cents(Decimal(sale["cost"]) / sale["qty"])',
                                 'unit = sale["cost"] // sale["qty"]')],
        "returns-sold-first": [("src/shoplib/costing.py", "            lots[sku].append([qty, unit])\n",
                                "            lots[sku].insert(0, [qty, unit])\n")],
    },
))

DAYS_OLD = '    """Revenue per store day. See docs/store-days.md."""\n    raise NotImplementedError\n'
DAYS_NEW = '''    """Revenue per store day. See docs/store-days.md."""
    tz = timezone(timedelta(hours=utc_offset_hours))
    totals: dict = {}
    for sale in sales:
        at = datetime.fromisoformat(sale["at"])
        if at.tzinfo is None:
            raise ValueError(f"timestamp without a zone: {sale['at']}")
        day = (at.astimezone(tz) - timedelta(hours=day_starts_hour)).date()
        totals[day] = totals.get(day, 0) + sale["cents"]
    if not totals:
        return []
    out, day = [], min(totals)
    while day <= max(totals):
        out.append((day.isoformat(), totals.get(day, 0)))
        day += timedelta(days=1)
    return out
'''

add(Task(
    id="t14-store-days",
    one_line="Implement daily_revenue.",
    goal="Implement daily_revenue: total sales per store day.",
    context="The spec is docs/store-days.md. The code is in src/shoplib/storedays.py.",
    constraints="Change only src/shoplib/storedays.py and files in tests/. Standard library only.",
    done_when="Every rule in docs/store-days.md holds, including the day boundary, time zones, gaps and the error "
              "case, and `python -m pytest -q` passes.",
    scope=["src/shoplib/storedays.py", "tests/*"],
    edits=[("src/shoplib/storedays.py", '"""Revenue per store day. See docs/store-days.md."""\n\n\ndef',
            '"""Revenue per store day. See docs/store-days.md."""\n\nfrom datetime import datetime, timedelta, timezone\n\n\ndef'),
           ("src/shoplib/storedays.py", DAYS_OLD, DAYS_NEW)],
    bugs={
        "start-hour-goes-to-previous-day": [("src/shoplib/storedays.py", "timedelta(hours=day_starts_hour)).date()",
                                             "timedelta(hours=day_starts_hour, microseconds=1)).date()")],
        "no-gap-days": [("src/shoplib/storedays.py", "        out.append((day.isoformat(), totals.get(day, 0)))\n",
                         "        if day in totals:\n            out.append((day.isoformat(), totals[day]))\n")],
    },
))
