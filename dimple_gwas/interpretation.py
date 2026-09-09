"""Post-run original-space interpretation for native and legacy artifacts."""

from __future__ import annotations

import json
import math
import re
import sys
import time
from pathlib import Path
from typing import Any, Mapping, Sequence

from .io import (
    atomic_json_dump,
    ensure_empty_output_dir,
    json_safe,
    normalize_identifier,
    read_table,
    validated_identifiers,
)
from .metrics import embedding_quality_metrics
from .preprocessing import (
    infer_explanation_orientation,
    prepare_explanation_matrix,
)
from .provenance import base_manifest, file_record, sha256_file, utc_now
from .visualization import render_heatmap


def is_noise_label(value: Any) -> bool:
    text = str(value).strip().casefold()
    return text in {"-1", "-1.0", "noise"}


def label_sort_key(value: Any) -> tuple[int, float | str]:
    if is_noise_label(value):
        return (2, str(value))
    try:
        return (0, float(value))
    except (TypeError, ValueError):
        return (1, str(value))


def detect_coordinate_columns(frame, requested: Sequence[str] | str | None = None) -> list[str]:
    if requested:
        values = requested.split(",") if isinstance(requested, str) else list(requested)
        result: list[str] = []
        for value in values:
            matches = [column for column in frame.columns if str(column).casefold() == str(value).strip().casefold()]
            if len(matches) != 1:
                raise ValueError(f"Coordinate column {value!r} is missing or ambiguous")
            result.append(str(matches[0]))
        if len(result) < 2:
            raise ValueError("At least two coordinate columns are required")
        return result
    numbered: list[tuple[int, str]] = []
    for column in frame.columns:
        match = re.match(r"^umap[\s_-]?(\d+)$", str(column).strip(), flags=re.IGNORECASE)
        if match:
            numbered.append((int(match.group(1)), str(column)))
    numbered.sort()
    return [column for _, column in numbered]


def _resolve_column(frame, requested: str | None, candidates: Sequence[str], purpose: str) -> str:
    if requested and requested != "auto":
        matches = [column for column in frame.columns if str(column).casefold() == requested.casefold()]
        if len(matches) != 1:
            raise ValueError(f"{purpose} column {requested!r} is missing or ambiguous")
        return str(matches[0])
    matched: list[str] = []
    candidate_keys = {value.casefold() for value in candidates}
    for column in frame.columns:
        normalized = re.sub(r"[^a-z0-9]+", "_", str(column).casefold()).strip("_")
        if normalized in candidate_keys:
            matched.append(str(column))
    if len(matched) != 1:
        raise ValueError(
            f"Could not safely identify one {purpose} column; candidates={matched}. Specify it explicitly"
        )
    return matched[0]


def _native_sources(model_json: str | Path, input_override: str | Path | None):
    source = Path(model_json)
    if not source.is_file():
        raise FileNotFoundError(f"Model JSON not found: {source}")
    payload = json.loads(source.read_text(encoding="utf-8"))
    model_id = str(payload.get("model", {}).get("model_id", ""))
    labels_name = payload.get("labels_file")
    if labels_name:
        labels_path = source.parent / str(labels_name)
    elif model_id and source.parent.name == "models":
        labels_path = source.parent / "top_model_artifacts" / model_id / "labels.tsv"
    else:
        raise ValueError(
            "Model JSON does not resolve retained labels; use a top-model summary.json"
        )
    if not labels_path.is_file():
        raise FileNotFoundError(f"Retained label table not found: {labels_path}")
    expected_hash = payload.get("labels_sha256")
    if expected_hash and sha256_file(labels_path) != expected_hash:
        raise ValueError("Retained label table hash does not match the model summary")
    config = payload.get("resolved_run_config") or {}
    input_path = input_override or config.get("input", {}).get("path")
    if not input_path:
        raise ValueError("Native explanation cannot resolve the original input; pass --input")
    return payload, labels_path, Path(input_path), config


def _align_inputs(analysis, labels, *, id_column: str, require_complete: bool):
    import pandas as pd

    matrix_ids = validated_identifiers(analysis.index, context="analysis matrix")
    label_ids = validated_identifiers(labels[id_column], context="label table")
    matrix_set = set(matrix_ids)
    label_set = set(label_ids)
    exclusions: list[dict[str, str]] = []
    for value in matrix_ids:
        if value not in label_set:
            exclusions.append({"feature_id": value, "source": "matrix", "reason": "missing_from_labels"})
    for value in label_ids:
        if value not in matrix_set:
            exclusions.append({"feature_id": value, "source": "labels", "reason": "missing_from_matrix"})
    if require_complete and exclusions:
        raise ValueError(
            "Complete ID matching failed: "
            f"matrix_only={sum(row['source'] == 'matrix' for row in exclusions)}, "
            f"labels_only={sum(row['source'] == 'labels' for row in exclusions)}"
        )
    retained = [value for value in matrix_ids if value in label_set]
    if len(retained) < 2:
        raise ValueError("Fewer than two vectors remain after ID matching")
    aligned_analysis = analysis.copy()
    aligned_analysis.index = matrix_ids
    aligned_analysis = aligned_analysis.loc[retained]
    aligned_labels = labels.copy()
    aligned_labels[id_column] = label_ids
    aligned_labels = aligned_labels.set_index(id_column, drop=False).loc[retained]
    if not aligned_analysis.index.equals(pd.Index(aligned_labels.index)):
        raise RuntimeError("Internal ID alignment failure")
    return aligned_analysis, aligned_labels, exclusions


def compute_similarity(analysis, *, method: str, undefined_policy: str):
    import numpy as np

    values = analysis.to_numpy(dtype=float)
    if method == "spearman":
        from scipy.stats import rankdata

        values = np.apply_along_axis(rankdata, 1, values, method="average")
    correlation = np.corrcoef(values)
    undefined = ~np.isfinite(correlation)
    undefined_count = int(undefined.sum())
    if undefined_count and undefined_policy == "error":
        affected = int(np.unique(np.where(undefined)[0]).size)
        raise ValueError(
            f"Original-space similarity contains {undefined_count} undefined cells "
            f"affecting {affected} vectors (often constant vectors)"
        )
    if undefined_count:
        correlation[undefined] = 0.0
        np.fill_diagonal(correlation, 1.0)
    return correlation, undefined_count


def _hierarchical_order(correlation) -> list[int]:
    import numpy as np

    count = int(correlation.shape[0])
    if count <= 1:
        return list(range(count))
    from scipy.cluster.hierarchy import leaves_list, linkage
    from scipy.spatial.distance import squareform

    distance = np.clip(1.0 - np.asarray(correlation, dtype=float), 0.0, 2.0)
    distance = (distance + distance.T) / 2.0
    np.fill_diagonal(distance, 0.0)
    tree = linkage(squareform(distance, checks=False), method="average", optimal_ordering=True)
    return leaves_list(tree).astype(int).tolist()


def compute_order(correlation, labels: Sequence[Any], *, method: str, noise_policy: str) -> list[int]:
    indices = list(range(len(labels)))
    if method == "input":
        return indices
    if method == "hclust" and noise_policy == "include":
        return _hierarchical_order(correlation)
    groups: dict[str, list[int]] = {}
    values: dict[str, Any] = {}
    for index, label in enumerate(labels):
        key = str(label)
        groups.setdefault(key, []).append(index)
        values[key] = label
    ordered_groups = sorted(groups, key=lambda key: label_sort_key(values[key]))
    result: list[int] = []
    for key in ordered_groups:
        block = groups[key]
        if method in {"cluster_then_hclust", "hclust"} and len(block) > 1:
            import numpy as np

            within = correlation[np.ix_(block, block)]
            block = [block[index] for index in _hierarchical_order(within)]
        result.extend(block)
    return result


def calculate_cutpoints(labels: Sequence[Any]):
    import pandas as pd

    rows: list[dict[str, Any]] = []
    if not labels:
        return pd.DataFrame(columns=[
            "cluster_label", "start_index_0_based", "end_index_0_based",
            "start_index_1_based", "end_index_1_based", "size",
        ])
    start = 0
    for index in range(1, len(labels) + 1):
        if index == len(labels) or str(labels[index]) != str(labels[start]):
            rows.append({
                "cluster_label": labels[start],
                "start_index_0_based": start,
                "end_index_0_based": index - 1,
                "start_index_1_based": start + 1,
                "end_index_1_based": index,
                "size": index - start,
            })
            start = index
    return pd.DataFrame(rows)


def calculate_cluster_summary(correlation, labels: Sequence[Any]):
    import numpy as np
    import pandas as pd

    rows: list[dict[str, Any]] = []
    label_array = np.asarray(list(labels), dtype=object)
    for label in sorted(pd.unique(label_array).tolist(), key=label_sort_key):
        inside = np.flatnonzero(np.asarray([str(value) == str(label) for value in label_array]))
        outside = np.flatnonzero(np.asarray([str(value) != str(label) for value in label_array]))
        if len(inside) > 1:
            block = correlation[np.ix_(inside, inside)]
            within = block[np.triu_indices(len(inside), k=1)]
        else:
            within = np.asarray([], dtype=float)
        between = correlation[np.ix_(inside, outside)].ravel() if len(outside) else np.asarray([], dtype=float)
        rows.append({
            "cluster_label": label,
            "is_noise": is_noise_label(label),
            "size": int(len(inside)),
            "singleton": bool(len(inside) == 1),
            "within_similarity_pair_count": int(len(within)),
            "within_similarity_mean": float(np.mean(within)) if len(within) else math.nan,
            "within_similarity_median": float(np.median(within)) if len(within) else math.nan,
            "between_similarity_pair_count": int(len(between)),
            "between_similarity_mean": float(np.mean(between)) if len(between) else math.nan,
        })
    return pd.DataFrame(rows)


def coordinate_association_table(analysis, coordinates, *, methods: Sequence[str], top_n: int):
    import numpy as np
    import pandas as pd

    rows = []
    for method in methods:
        feature_values = analysis
        coordinate_values = coordinates
        if method == "spearman":
            feature_values = analysis.rank(axis=0, method="average")
            coordinate_values = coordinates.rank(axis=0, method="average")
        for coordinate in coordinate_values.columns:
            values = feature_values.corrwith(coordinate_values[coordinate], axis=0, method="pearson")
            table = pd.DataFrame({
                "original_dimension": values.index.astype(str),
                "coordinate": str(coordinate),
                "method": method,
                "correlation": values.to_numpy(dtype=float),
            })
            table["absolute_correlation"] = np.abs(table["correlation"])
            table = table.sort_values(
                ["absolute_correlation", "original_dimension"],
                ascending=[False, True], kind="mergesort",
            ).head(int(top_n))
            table.insert(0, "rank_within_coordinate_method", range(1, len(table) + 1))
            rows.append(table)
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def _write_readme(root: Path, *, mode: str, metric: str, rendered: Mapping[str, Any]) -> None:
    root.joinpath("README.md").write_text(
        "# DIMPLE-GWAS Freeze 3 interpretation\n\n"
        f"Mode: `{mode}`. Original-space similarity: `{metric}`.\n\n"
        "This directory is a post-run diagnostic package. It does not refit UMAP or "
        "HDBSCAN, change labels, or alter model ranking. `heatmap_order.tsv`, "
        "`cluster_cutpoints.tsv`, `cluster_summary.tsv`, and `projection_quality.tsv` "
        "are the machine-readable sources for the visual report.\n\n"
        f"The figure renders {rendered['rendered_vectors']} of {rendered['total_vectors']} "
        f"vectors using `{rendered['sampling']}` sampling. The complete similarity table "
        "is retained when enabled. Coordinate associations, if present, are descriptive "
        "correlations and are not loadings, drivers, mechanisms, or causal effects.\n",
        encoding="utf-8",
    )


def run_explanation(
    *,
    output_dir: str | Path,
    interpretation_config: Mapping[str, Any],
    model_json: str | Path | None = None,
    legacy_table: str | Path | None = None,
    input_path: str | Path | None = None,
    input_sep: str | None = None,
    input_sheet: str | int = 0,
    legacy_sheet: str | int = 0,
    matrix_orientation: str = "auto",
    vector_id_source: str = "auto",
    drop_first_n_cols: int | None = None,
    zscore_transform: str | None = None,
    id_column: str | None = None,
    label_column: str | None = None,
    coordinate_columns: Sequence[str] | str | None = None,
    command: list[str] | None = None,
) -> dict[str, Any]:
    """Build an auditable interpretation artifact directory."""

    import numpy as np
    import pandas as pd

    if bool(model_json) == bool(legacy_table):
        raise ValueError("Specify exactly one of model_json or legacy_table")
    started = time.perf_counter()
    root = ensure_empty_output_dir(output_dir)
    manifest = base_manifest(command or sys.argv)
    manifest.update({"manifest_schema": "dimple-gwas.interpretation.v3"})

    if model_json:
        mode = "native"
        model_payload, labels_path, resolved_input, run_config = _native_sources(model_json, input_path)
        labels = read_table(labels_path)
        id_name = _resolve_column(labels, id_column or "feature_id", ["feature_id"], "feature ID")
        label_name = _resolve_column(labels, label_column or "label", ["label"], "label")
        coords = detect_coordinate_columns(labels, coordinate_columns)
        input_cfg = run_config.get("input", {})
        resolved_drop = int(drop_first_n_cols if drop_first_n_cols is not None else input_cfg.get("drop_first_n_cols", 4))
        resolved_transform = zscore_transform or input_cfg.get("zscore_transform", "none")
        frame = read_table(resolved_input, sep=input_sep or input_cfg.get("sep"), sheet=input_sheet)
        prepared = prepare_explanation_matrix(
            frame,
            orientation="variants_by_vectors",
            drop_first_n_cols=resolved_drop,
            vector_id_source="matrix_columns",
            zscore_transform=resolved_transform,
        )
        require_complete = True
        source_records = {
            "model_json": file_record(model_json),
            "labels": file_record(labels_path),
            "input": file_record(resolved_input),
        }
        native_model_id = model_payload.get("model", {}).get("model_id")
    else:
        mode = "legacy"
        if not input_path:
            raise ValueError("Legacy explanation requires input_path")
        labels_path = Path(legacy_table)  # type: ignore[arg-type]
        labels = read_table(labels_path, sheet=legacy_sheet)
        id_name = _resolve_column(
            labels, id_column, ["feature_id", "index", "vector_id", "id", "trait_id", "trait"], "feature ID"
        )
        label_name = _resolve_column(
            labels, label_column, ["label", "cluster", "cluster_label", "hdbscan_label"], "label"
        )
        coords = detect_coordinate_columns(labels, coordinate_columns)
        frame = read_table(input_path, sep=input_sep, sheet=input_sheet)
        resolved_drop = int(4 if drop_first_n_cols is None else drop_first_n_cols)
        label_ids = validated_identifiers(labels[id_name], context="legacy label table")
        if matrix_orientation == "auto":
            inferred_orientation, inferred_source = infer_explanation_orientation(
                frame, label_ids, drop_first_n_cols=resolved_drop
            )
        else:
            inferred_orientation = matrix_orientation
            inferred_source = (
                "matrix_columns" if matrix_orientation == "variants_by_vectors" and vector_id_source == "auto"
                else vector_id_source
            )
        if inferred_source == "auto":
            raise ValueError("vectors_by_variants requires an explicit --vector-id-source")
        resolved_transform = zscore_transform or "none"
        prepared = prepare_explanation_matrix(
            frame,
            orientation=inferred_orientation,
            drop_first_n_cols=resolved_drop,
            vector_id_source=inferred_source,
            zscore_transform=resolved_transform,
        )
        require_complete = bool(interpretation_config.get("require_complete_match", True))
        source_records = {"labels": file_record(labels_path), "input": file_record(input_path)}
        native_model_id = None

    if labels[label_name].isna().any():
        raise ValueError(f"Label column {label_name!r} contains missing values")
    for column in coords:
        labels[column] = pd.to_numeric(labels[column], errors="coerce")
        if labels[column].isna().any():
            raise ValueError(f"Coordinate column {column!r} contains non-numeric or missing values")
    analysis, annotations, exclusions = _align_inputs(
        prepared.analysis, labels, id_column=id_name, require_complete=require_complete
    )

    noise_policy = str(interpretation_config.get("noise_policy", "separate_last"))
    if noise_policy == "exclude":
        keep = np.asarray([not is_noise_label(value) for value in annotations[label_name]])
        for vector_id in annotations.index[~keep]:
            exclusions.append({"feature_id": str(vector_id), "source": "labels", "reason": "noise_policy_exclude"})
        analysis = analysis.loc[keep]
        annotations = annotations.loc[keep]
    if len(analysis) < 2:
        raise ValueError("Fewer than two vectors remain after applying the noise policy")

    similarity_metric = str(interpretation_config.get("similarity_metric", "pearson"))
    undefined_policy = str(interpretation_config.get("undefined_correlation", "error"))
    if len(analysis) > 10_000 and not bool(interpretation_config.get("force_large_matrix", False)):
        raise ValueError(
            "More than 10,000 vectors requires interpretation.force_large_matrix=true"
        )
    correlation, undefined_count = compute_similarity(
        analysis, method=similarity_metric, undefined_policy=undefined_policy
    )
    order_method = str(interpretation_config.get("order", "cluster_then_hclust"))
    order = compute_order(
        correlation, annotations[label_name].tolist(), method=order_method, noise_policy=noise_policy
    )
    correlation = correlation[np.ix_(order, order)]
    analysis = analysis.iloc[order]
    annotations = annotations.iloc[order]
    ordered_ids = analysis.index.astype(str).tolist()
    ordered_labels = annotations[label_name].tolist()

    order_table = pd.DataFrame({
        "order_1_based": range(1, len(analysis) + 1),
        "feature_id": ordered_ids,
        "label": ordered_labels,
        "is_noise": [is_noise_label(value) for value in ordered_labels],
    })
    for column in coords:
        order_table[column] = annotations[column].to_numpy()
    order_table.to_csv(root / "heatmap_order.tsv", sep="\t", index=False)
    calculate_cutpoints(ordered_labels).to_csv(root / "cluster_cutpoints.tsv", sep="\t", index=False)
    calculate_cluster_summary(correlation, ordered_labels).to_csv(
        root / "cluster_summary.tsv", sep="\t", index=False
    )
    exclusion_table = pd.DataFrame(exclusions, columns=["feature_id", "source", "reason"])
    exclusion_table.to_csv(root / "exclusions.tsv", sep="\t", index=False)

    write_similarity = bool(interpretation_config.get("write_similarity", True))
    similarity_path = root / "original_space_similarity.tsv.gz"
    if write_similarity:
        pd.DataFrame(correlation, index=ordered_ids, columns=ordered_ids).rename_axis(
            "feature_id"
        ).to_csv(similarity_path, sep="\t", compression="gzip")

    quality = embedding_quality_metrics(
        analysis.to_numpy(dtype=float),
        annotations[coords].to_numpy(dtype=float),
        requested_k=30,
        max_samples=3000,
        seed=42,
    ) if len(coords) >= 2 else {
        "trustworthiness": math.nan,
        "continuity": math.nan,
        "metric_warnings": "fewer than two coordinate columns",
    }
    quality.update({
        "scope": "supplied_visualization_projection_not_clustering_validity",
        "coordinate_columns": ",".join(coords),
    })
    pd.DataFrame([quality]).to_csv(root / "projection_quality.tsv", sep="\t", index=False)

    associations_written = False
    if bool(interpretation_config.get("coordinate_associations", False)) and coords:
        methods = interpretation_config.get("coordinate_methods", ["pearson"])
        if isinstance(methods, str):
            methods = [item.strip() for item in methods.split(",") if item.strip()]
        association = coordinate_association_table(
            analysis,
            annotations[coords],
            methods=methods,
            top_n=int(interpretation_config.get("top_n_associations", 100)),
        )
        association.to_csv(root / "coordinate_associations.tsv", sep="\t", index=False)
        associations_written = True

    rendered = render_heatmap(
        correlation,
        ordered_labels,
        ordered_ids,
        png_path=root / "original_space_heatmap.png",
        html_path=root / "original_space_heatmap.html",
        maximum=int(interpretation_config.get("max_full_heatmap", 1200)),
    )
    _write_readme(root, mode=mode, metric=similarity_metric, rendered=rendered)

    artifact_names = [
        "heatmap_order.tsv", "cluster_cutpoints.tsv", "cluster_summary.tsv",
        "exclusions.tsv", "projection_quality.tsv", "original_space_heatmap.png",
        "original_space_heatmap.html", "README.md",
    ]
    if write_similarity:
        artifact_names.append("original_space_similarity.tsv.gz")
    if associations_written:
        artifact_names.append("coordinate_associations.tsv")
    manifest.update({
        "status": "complete",
        "finished_at_utc": utc_now(),
        "runtime_seconds": time.perf_counter() - started,
        "mode": mode,
        "model_id": native_model_id,
        "sources": source_records,
        "data_contract": {
            "orientation": prepared.orientation,
            "vector_id_source": prepared.vector_id_source,
            "drop_first_n_cols": resolved_drop,
            "preprocessing": resolved_transform,
            "id_column": id_name,
            "label_column": label_name,
            "coordinate_columns": coords,
            "complete_match_required": require_complete,
        },
        "interpretation_configuration": json_safe(dict(interpretation_config)),
        "vector_counts": {
            "label_rows": int(len(labels)),
            "matrix_vectors": int(len(prepared.analysis)),
            "analyzed": int(len(analysis)),
            "excluded": int(len(exclusions)),
        },
        "undefined_similarity_cells": undefined_count,
        "warnings": ([
            f"{undefined_count} undefined correlations were explicitly zero-filled"
        ] if undefined_count else []),
        "exclusions": json_safe(exclusions),
        "rendering": rendered,
        "artifacts": {name: file_record(root / name) for name in artifact_names},
    })
    atomic_json_dump(json_safe(manifest), root / "interpretation_manifest.json")
    return manifest
