from collections.abc import Iterable
from typing import Any

from csv2json.types import infer_value


def csv_to_json(
    rows: Iterable[dict[str, str]],
    *,
    infer_types: bool = True,
    columns: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Convert CSV rows into JSON-serializable dictionaries."""
    output: list[dict[str, Any]] = []

    for row in rows:
        converted_row: dict[str, Any] = {}

        selected_columns = columns if columns is not None else list(row.keys())

        for column in selected_columns:
            if column not in row:
                raise ValueError(f"Column not found: {column}")

            value = row[column]
            converted_row[column] = infer_value(value) if infer_types else value

        output.append(converted_row)

    return output