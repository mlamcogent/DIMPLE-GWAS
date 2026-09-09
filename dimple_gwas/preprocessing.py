"""Dev-compatible GWAS summary-statistics preprocessing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .io import normalize_identifier, validated_identifiers


@dataclass(frozen=True)
class ExplanationMatrix:
    analysis: Any
    orientation: str
    vector_id_source: str
    feature_ids: list[str]


def rank_inverse_normal_transform(frame):
    import pandas as pd
    from scipy.stats import norm

    if frame.empty:
        return frame.copy()
    counts = frame.notna().sum(axis=0)
    if (counts < 1).any():
        raise ValueError("Cannot apply RINT to a column with no observed values")
    ranks = frame.rank(axis=0, method="average", na_option="keep")
    quantiles = (ranks - 0.5).div(counts, axis=1)
    transformed = norm.ppf(quantiles)
    return pd.DataFrame(transformed, index=frame.index, columns=frame.columns)


def prepare_analysis_matrix(frame, config: Mapping[str, Any]):
    import pandas as pd

    drop = int(config.get("drop_first_n_cols", 4))
    if frame.shape[1] <= drop:
        raise ValueError(
            f"Input has {frame.shape[1]} columns, so drop_first_n_cols={drop} leaves no analysis columns"
        )
    numeric = frame.iloc[:, drop:].copy().apply(pd.to_numeric, errors="coerce")
    if numeric.isna().any().any():
        count = int(numeric.isna().sum().sum())
        raise ValueError(
            f"Non-numeric values or missingness detected after coercion (NA cells={count})"
        )
    if config.get("zscore_transform", "none") == "rint":
        numeric = rank_inverse_normal_transform(numeric)
    matrix = numeric.T
    matrix.index = matrix.index.astype(str)
    return matrix


def _unique_feature_names(values) -> list[str]:
    """Create stable, nonempty names for original-space dimensions."""

    names: list[str] = []
    counts: dict[str, int] = {}
    for position, value in enumerate(values, start=1):
        base = normalize_identifier(value) or f"feature_{position}"
        counts[base] = counts.get(base, 0) + 1
        names.append(base if counts[base] == 1 else f"{base}#{counts[base]}")
    return names


def infer_explanation_orientation(
    frame,
    expected_vector_ids,
    *,
    drop_first_n_cols: int,
) -> tuple[str, str]:
    """Infer orientation only when one exact ID source is uniquely supported."""

    import pandas as pd

    expected = set(validated_identifiers(expected_vector_ids, context="label table"))
    if drop_first_n_cols < 0 or drop_first_n_cols >= frame.shape[1]:
        raise ValueError(
            f"drop_first_n_cols={drop_first_n_cols} leaves no analyzable columns"
        )
    candidates: list[tuple[float, str, str]] = []
    column_ids = [normalize_identifier(value) for value in frame.columns[drop_first_n_cols:]]
    if column_ids and all(column_ids) and len(column_ids) == len(set(column_ids)):
        overlap = len(expected & set(column_ids))
        candidates.append((overlap / max(len(expected), len(column_ids)), "variants_by_vectors", "matrix_columns"))
    for column in frame.columns:
        series = frame[column]
        values = [normalize_identifier(value) for value in series]
        if values and all(values) and len(values) == len(set(values)):
            overlap = len(expected & set(values))
            if overlap:
                candidates.append((overlap / max(len(expected), len(values)), "vectors_by_variants", f"column:{column}"))
    if not isinstance(frame.index, pd.RangeIndex) and frame.index.is_unique:
        values = [normalize_identifier(value) for value in frame.index]
        overlap = len(expected & set(values))
        if overlap:
            candidates.append((overlap / max(len(expected), len(values)), "vectors_by_variants", "matrix_index"))
    candidates.sort(key=lambda item: (-item[0], item[1], item[2]))
    if not candidates or candidates[0][0] < 0.5:
        raise ValueError(
            "Could not infer matrix orientation with sufficient ID overlap; specify it explicitly"
        )
    tied = [item for item in candidates if abs(item[0] - candidates[0][0]) < 1e-12]
    if len(tied) != 1:
        raise ValueError(
            "Matrix orientation is ambiguous; specify --matrix-orientation and --vector-id-source"
        )
    return candidates[0][1], candidates[0][2]


def prepare_explanation_matrix(
    frame,
    *,
    orientation: str,
    drop_first_n_cols: int,
    vector_id_source: str = "matrix_columns",
    zscore_transform: str = "none",
) -> ExplanationMatrix:
    """Prepare vectors × original dimensions for post-run interpretation."""

    import pandas as pd

    if orientation not in {"variants_by_vectors", "vectors_by_variants"}:
        raise ValueError("orientation must be variants_by_vectors or vectors_by_variants")
    if drop_first_n_cols < 0 or drop_first_n_cols >= frame.shape[1]:
        raise ValueError(
            f"drop_first_n_cols={drop_first_n_cols} leaves no analyzable columns"
        )
    if zscore_transform not in {"none", "rint"}:
        raise ValueError("zscore_transform must be none or rint")

    if orientation == "variants_by_vectors":
        if vector_id_source != "matrix_columns":
            raise ValueError("variants_by_vectors requires vector_id_source=matrix_columns")
        numeric = frame.iloc[:, drop_first_n_cols:].copy().apply(pd.to_numeric, errors="coerce")
        if numeric.isna().any().any():
            count = int(numeric.isna().sum().sum())
            raise ValueError(
                f"Non-numeric values or missingness detected after coercion (NA cells={count})"
            )
        if zscore_transform == "rint":
            numeric = rank_inverse_normal_transform(numeric)
        analysis = numeric.T
        identifiers = validated_identifiers(analysis.index, context="matrix columns")
        feature_source = frame.iloc[:, 0].tolist() if drop_first_n_cols else frame.index.tolist()
        feature_ids = _unique_feature_names(feature_source)
        analysis.index = identifiers
        analysis.columns = feature_ids
        return ExplanationMatrix(analysis, orientation, vector_id_source, feature_ids)

    if vector_id_source == "matrix_index":
        identifiers = validated_identifiers(frame.index, context="matrix index")
        id_column = None
    elif vector_id_source.startswith("column:"):
        requested = vector_id_source.split(":", 1)[1]
        matches = [column for column in frame.columns if str(column).casefold() == requested.casefold()]
        if len(matches) != 1:
            raise ValueError(f"Vector ID column {requested!r} is missing or ambiguous")
        id_column = matches[0]
        identifiers = validated_identifiers(frame[id_column], context=f"matrix column {id_column!r}")
    else:
        raise ValueError("vectors_by_variants requires vector_id_source=column:<name> or matrix_index")
    columns = list(frame.columns[drop_first_n_cols:])
    if id_column in columns:
        columns.remove(id_column)
    if not columns:
        raise ValueError("Metadata removal leaves no analyzable columns")
    numeric = frame.loc[:, columns].copy().apply(pd.to_numeric, errors="coerce")
    if numeric.isna().any().any():
        count = int(numeric.isna().sum().sum())
        raise ValueError(
            f"Non-numeric values or missingness detected after coercion (NA cells={count})"
        )
    if zscore_transform == "rint":
        numeric = rank_inverse_normal_transform(numeric)
    numeric.index = identifiers
    feature_ids = _unique_feature_names(columns)
    numeric.columns = feature_ids
    return ExplanationMatrix(numeric, orientation, vector_id_source, feature_ids)
