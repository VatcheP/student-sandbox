import argparse
import csv
import json
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any, TextIO

from csv2json.converter import csv_to_json_rows


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="csv2json",
        description="Convert CSV files to JSON.",
    )

    parser.add_argument("--input", "-i", type=Path, help="Input CSV file. Defaults to stdin.")
    parser.add_argument("--output", "-o", type=Path, help="Output JSON file. Defaults to stdout.")
    parser.add_argument("--columns", help="Comma-separated list of columns to include.")
    parser.add_argument("--no-infer-types", action="store_true", help="Keep all CSV values as strings.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")

    return parser


def open_input(input_path: Path | None) -> TextIO:
    """Open a CSV input file or return stdin."""
    if input_path is None:
        return sys.stdin

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    return input_path.open("r", newline="", encoding="utf-8")


def write_json_stream(
    rows: Iterable[dict[str, Any]],
    output_path: Path | None,
    *,
    pretty: bool,
) -> None:
    """Write JSON array while streaming rows one at a time."""
    indent = 2 if pretty else None

    output_file = output_path.open("w", encoding="utf-8") if output_path else sys.stdout

    try:
        output_file.write("[")
        first = True

        for row in rows:
            if first:
                first = False
            else:
                output_file.write(",")

            if pretty:
                output_file.write("\n")
                output_file.write(json.dumps(row, indent=indent))
            else:
                output_file.write(json.dumps(row))

        if pretty and not first:
            output_file.write("\n")

        output_file.write("]\n")

    finally:
        if output_path:
            output_file.close()


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        columns = args.columns.split(",") if args.columns else None

        with open_input(args.input) as csv_file:
            reader = csv.DictReader(csv_file)

            rows = csv_to_json_rows(
                reader,
                infer_types=not args.no_infer_types,
                columns=columns,
            )

            write_json_stream(rows, args.output, pretty=args.pretty)

    except (FileNotFoundError, ValueError, csv.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()