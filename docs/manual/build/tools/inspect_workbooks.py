#!/usr/bin/env python3
"""Create a compact read-only inventory of scientific XLSX source workbooks."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from openpyxl import load_workbook


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def inspect(path: Path) -> dict[str, object]:
    workbook = load_workbook(path, read_only=True, data_only=False)
    sheets: list[dict[str, object]] = []
    for sheet in workbook.worksheets:
        preview: list[list[object]] = []
        for row in sheet.iter_rows(min_row=1, max_row=min(5, sheet.max_row), values_only=True):
            preview.append([value if value is None or isinstance(value, (str, int, float, bool)) else str(value) for value in row[:20]])
        sheets.append(
            {
                "title": sheet.title,
                "max_row": sheet.max_row,
                "max_column": sheet.max_column,
                "preview_first_five_rows_first_twenty_columns": preview,
            }
        )
    workbook.close()
    return {
        "path": str(path.resolve()),
        "size_bytes": path.stat().st_size,
        "sha256": digest(path),
        "sheets": sheets,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("inputs", nargs="+", type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = [inspect(path) for path in args.inputs]
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
