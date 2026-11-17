"""Command line entry point. See docs/cli.md."""

import argparse
import json
import sys

from .reports import sales_summary, to_csv


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="shoplib")
    sub = parser.add_subparsers(dest="command", required=True)
    report = sub.add_parser("report", help="print the sales summary")
    report.add_argument("sales_json", help="file with a JSON list of sales")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "report":
        with open(args.sales_json) as fh:
            sales = json.load(fh)
        sys.stdout.write(to_csv(sales_summary(sales)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
