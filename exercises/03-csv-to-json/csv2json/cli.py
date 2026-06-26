import argparse
import csv
import json
import sys
from pathlib import Path

from csv2json.converter import csv_to_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="csv2json",
        description="Convert CSV files to JSON.",
    )

    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        help="Input CSV file. Defaults to stdin.",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output JSON file. Defaults to stdout.",
    )

    parser.add_argument(
        "--columns",
        help="Comma-separated list of columns to include.",
    )

    parser.add_argument(
        "--no-infer-types",
        action="store_true",
        help="Keep all CSV values as strings.",
    )

    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output.",
    )

    return parser


def read_csv(input_path: Path | None) -> list[dict[str, str]]:
    """Read CSV rows from a file or stdin."""
    if input_path is None:
        return list(csv.DictReader(sys.stdin))

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with input_path.open("r", newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def write_json(data: list[dict], output_path: Path | None, pretty: bool) -> None:
    """Write JSON to a file or stdout."""
    indent = 2 if pretty else None

    if output_path is None:
        json.dump(data, sys.stdout, indent=indent)
        sys.stdout.write("\n")
        return

    with output_path.open("w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=indent)
        json_file.write("\n")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        columns = args.columns.split(",") if args.columns else None

        rows = read_csv(args.input)

        data = csv_to_json(
            rows,
            infer_types=not args.no_infer_types,
            columns=columns,
        )

        write_json(data, args.output, args.pretty)

    except (FileNotFoundError, ValueError, csv.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()