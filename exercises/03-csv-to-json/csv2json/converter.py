from collections.abc import Iterable, Iterator
from typing import Any

from csv2json.types import infer_value


def convert_row(
    row: dict[str, str],
    *,
    infer_types: bool = True,
    columns: list[str] | None = None,
) -> dict[str, Any]:
    """Convert one CSV row into a JSON-serializable dictionary."""
    converted_row: dict[str, Any] = {}

    selected_columns = columns if columns is not None else list(row.keys())

    for column in selected_columns:
        if column not in row:
            raise ValueError(f"Column not found: {column}")

        value = row[column]
        converted_row[column] = infer_value(value) if infer_types else value

    return converted_row


def csv_to_json_rows(
    rows: Iterable[dict[str, str]],
    *,
    infer_types: bool = True,
    columns: list[str] | None = None,
) -> Iterator[dict[str, Any]]:
    """Convert CSV rows lazily, one row at a time."""
    for row in rows:
        yield convert_row(row, infer_types=infer_types, columns=columns)


def csv_to_json(
    rows: Iterable[dict[str, str]],
    *,
    infer_types: bool = True,
    columns: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Convert CSV rows into a list.

    This is convenient for small files, but csv_to_json_rows is better
    for large files because it streams one row at a time.
    """
    return list(
        csv_to_json_rows(rows, infer_types=infer_types, columns=columns)
    )