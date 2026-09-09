"""Input and tabular output helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def resolve_separator(path: str | Path, override: str | None = None) -> str:
    if override is not None:
        return override
    return "\t" if str(path).lower().endswith((".tsv", ".tsv.gz")) else ","


def read_table(
    path: str | Path,
    sep: str | None = None,
    *,
    sheet: str | int = 0,
    nrows: int | None = None,
):
    import pandas as pd

    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(f"Input file not found: {source}")
    suffix = source.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        if isinstance(sheet, str) and sheet.strip().lstrip("-").isdigit():
            sheet = int(sheet)
        try:
            return pd.read_excel(source, sheet_name=sheet, nrows=nrows)
        except ImportError as exc:
            raise RuntimeError(
                f"Reading {suffix} requires the corresponding Excel engine: {exc}"
            ) from exc
    delimiter = resolve_separator(source, sep)
    try:
        return pd.read_csv(source, sep=delimiter, engine="pyarrow", nrows=nrows)
    except Exception:
        return pd.read_csv(source, sep=delimiter, nrows=nrows, low_memory=False)


def read_model_table(path: str | Path):
    import pandas as pd

    source = Path(path)
    if source.suffix.lower() == ".parquet":
        return pd.read_parquet(source)
    return pd.read_csv(source, sep=resolve_separator(source))


def ensure_empty_output_dir(path: str | Path) -> Path:
    """Create an output directory, refusing to mix with existing artifacts."""

    destination = Path(path)
    if destination.exists():
        if not destination.is_dir():
            raise ValueError(f"Output path exists and is not a directory: {destination}")
        if any(destination.iterdir()):
            raise ValueError(f"Output directory is not empty: {destination}")
    else:
        destination.mkdir(parents=True, exist_ok=False)
    return destination


def normalize_identifier(value: Any) -> str:
    """Return the exact string identity after removing surrounding whitespace."""

    try:
        import pandas as pd

        if bool(pd.isna(value)):
            return ""
    except (ImportError, TypeError, ValueError):
        pass
    return str(value).strip()


def validated_identifiers(values, *, context: str) -> list[str]:
    """Normalize identifiers and reject missing or duplicate identities."""

    import pandas as pd

    identifiers = [normalize_identifier(value) for value in values]
    missing = [index + 1 for index, value in enumerate(identifiers) if not value]
    if missing:
        raise ValueError(
            f"{context} contains empty identifiers at 1-based rows {missing[:8]}"
        )
    series = pd.Series(identifiers, dtype="string")
    duplicates = sorted(series[series.duplicated(keep=False)].unique().tolist())
    if duplicates:
        raise ValueError(f"{context} contains duplicate identifiers: {duplicates[:8]}")
    return identifiers


def atomic_json_dump(value: Any, path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, sort_keys=True, default=str, allow_nan=False)
        handle.write("\n")
    temporary.replace(destination)


def json_safe(value: Any) -> Any:
    try:
        import numpy as np
        import pandas as pd
    except ImportError:  # pragma: no cover
        np = None
        pd = None
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        return value if value == value and abs(value) != float("inf") else None
    if np is not None and isinstance(value, np.generic):
        return json_safe(value.item())
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    if pd is not None:
        try:
            if bool(pd.isna(value)):
                return None
        except (TypeError, ValueError):
            pass
    return str(value)
