"""ID-safe structural comparison of retained clustering artifacts."""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path
from typing import Any

from .interpretation import detect_coordinate_columns, is_noise_label, label_sort_key
from .io import atomic_json_dump, ensure_empty_output_dir, json_safe, read_table, validated_identifiers
from .provenance import base_manifest, file_record, utc_now


def _resolve_labels(source_value: str | Path):
    source = Path(source_value)
    if not source.is_file():
        raise FileNotFoundError(f"Comparison source not found: {source}")
    if source.suffix.lower() != ".json":
        return read_table(source), source, None
    payload = json.loads(source.read_text(encoding="utf-8"))
    model_id = str(payload.get("model", {}).get("model_id", ""))
    labels_name = payload.get("labels_file")
    if labels_name:
        labels_path = source.parent / str(labels_name)
    elif model_id and source.parent.name == "models":
        labels_path = source.parent / "top_model_artifacts" / model_id / "labels.tsv"
    else:
        raise ValueError(f"JSON source does not resolve retained labels: {source}")
    return read_table(labels_path), labels_path, model_id or None


def _columns(frame, id_column: str, label_column: str) -> tuple[str, str]:
    def resolve(requested: str) -> str:
        matches = [column for column in frame.columns if str(column).casefold() == requested.casefold()]
        if len(matches) != 1:
            raise ValueError(f"Column {requested!r} is missing or ambiguous")
        return str(matches[0])
    return resolve(id_column), resolve(label_column)


def _variation_of_information(left, right) -> float:
    import numpy as np

    left = np.asarray(left, dtype=object)
    right = np.asarray(right, dtype=object)
    total = len(left)
    if not total:
        return math.nan
    left_values, left_counts = np.unique(left.astype(str), return_counts=True)
    right_values, right_counts = np.unique(right.astype(str), return_counts=True)
    h_left = -sum((count / total) * math.log(count / total) for count in left_counts)
    h_right = -sum((count / total) * math.log(count / total) for count in right_counts)
    mutual = 0.0
    for l_value, l_count in zip(left_values, left_counts):
        for r_value, r_count in zip(right_values, right_counts):
            joint = int(((left.astype(str) == l_value) & (right.astype(str) == r_value)).sum())
            if joint:
                mutual += (joint / total) * math.log((joint * total) / (l_count * r_count))
    return float(h_left + h_right - 2.0 * mutual)


def run_comparison(
    left_source: str | Path,
    right_source: str | Path,
    output_dir: str | Path,
    *,
    id_column: str = "feature_id",
    label_column: str = "label",
    require_same_order: bool = False,
    command: list[str] | None = None,
) -> dict[str, Any]:
    import numpy as np
    import pandas as pd
    from scipy.optimize import linear_sum_assignment
    from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

    started = time.perf_counter()
    root = ensure_empty_output_dir(output_dir)
    left, left_path, left_model = _resolve_labels(left_source)
    right, right_path, right_model = _resolve_labels(right_source)
    left_id, left_label = _columns(left, id_column, label_column)
    right_id, right_label = _columns(right, id_column, label_column)
    left_ids = validated_identifiers(left[left_id], context="left labels")
    right_ids = validated_identifiers(right[right_id], context="right labels")
    if set(left_ids) != set(right_ids):
        raise ValueError(
            "Comparison requires identical ID sets: "
            f"left_only={len(set(left_ids) - set(right_ids))}, "
            f"right_only={len(set(right_ids) - set(left_ids))}"
        )
    order_equal = left_ids == right_ids
    if require_same_order and not order_equal:
        raise ValueError("Comparison requires identical ID order")
    left = left.copy()
    right = right.copy()
    left[left_id] = left_ids
    right[right_id] = right_ids
    left = left.set_index(left_id, drop=False)
    right = right.set_index(right_id, drop=False).loc[left_ids]
    left_values = left[left_label].astype(str).to_numpy()
    right_values = right[right_label].astype(str).to_numpy()

    left_clusters = sorted(set(left_values), key=label_sort_key)
    right_clusters = sorted(set(right_values), key=label_sort_key)
    confusion = pd.crosstab(
        pd.Series(left_values, name="left_label"),
        pd.Series(right_values, name="right_label"),
        dropna=False,
    ).reindex(index=left_clusters, columns=right_clusters, fill_value=0)
    row_indices, column_indices = linear_sum_assignment(-confusion.to_numpy(dtype=float))
    mapping = {
        right_clusters[column]: left_clusters[row]
        for row, column in zip(row_indices.tolist(), column_indices.tolist())
    }
    mapping_table = pd.DataFrame([
        {
            "right_label": right_label_value,
            "mapped_left_label": left_label_value,
            "overlap": int(confusion.loc[left_label_value, right_label_value]),
        }
        for right_label_value, left_label_value in sorted(mapping.items(), key=lambda item: label_sort_key(item[0]))
    ])
    mapped_right = np.asarray([mapping.get(value, f"unmapped:{value}") for value in right_values], dtype=object)
    left_noise = np.asarray([is_noise_label(value) for value in left_values])
    right_noise = np.asarray([is_noise_label(value) for value in right_values])
    union = int((left_noise | right_noise).sum())
    noise_jaccard = float((left_noise & right_noise).sum() / union) if union else 1.0
    membership = pd.DataFrame({
        "feature_id": left_ids,
        "left_label": left_values,
        "right_label": right_values,
        "right_label_mapped": mapped_right,
        "same_mapped_cluster": left_values == mapped_right,
        "left_noise": left_noise,
        "right_noise": right_noise,
        "changed_noise_status": left_noise != right_noise,
    })

    procrustes_disparity = math.nan
    left_coords = detect_coordinate_columns(left)
    right_coords = detect_coordinate_columns(right)
    if len(left_coords) >= 2 and len(left_coords) == len(right_coords):
        try:
            from scipy.spatial import procrustes

            _, _, procrustes_disparity = procrustes(
                left[left_coords].to_numpy(dtype=float),
                right[right_coords].to_numpy(dtype=float),
            )
            procrustes_disparity = float(procrustes_disparity)
        except ValueError:
            procrustes_disparity = math.nan

    confusion_output = confusion.copy()
    confusion_output.index.name = "left_label"
    confusion_output.to_csv(root / "label_confusion.tsv", sep="\t")
    mapping_table.to_csv(root / "optimal_label_mapping.tsv", sep="\t", index=False)
    membership.to_csv(root / "membership_comparison.tsv", sep="\t", index=False)
    sizes = pd.concat([
        left[left_label].astype(str).value_counts().rename_axis("label").reset_index(name="size").assign(side="left"),
        right[right_label].astype(str).value_counts().rename_axis("label").reset_index(name="size").assign(side="right"),
    ], ignore_index=True)
    sizes["is_noise"] = sizes["label"].map(is_noise_label)
    sizes.to_csv(root / "cluster_sizes.tsv", sep="\t", index=False)

    summary = {
        "comparison_schema": "dimple-gwas.comparison.v3",
        "left_model_id": left_model,
        "right_model_id": right_model,
        "sample_count": int(len(left_ids)),
        "id_sets_equal": True,
        "id_order_equal": order_equal,
        "left_cluster_count_excluding_noise": len([value for value in left_clusters if not is_noise_label(value)]),
        "right_cluster_count_excluding_noise": len([value for value in right_clusters if not is_noise_label(value)]),
        "left_noise_count": int(left_noise.sum()),
        "right_noise_count": int(right_noise.sum()),
        "adjusted_rand_index": float(adjusted_rand_score(left_values, right_values)),
        "normalized_mutual_information": float(normalized_mutual_info_score(left_values, right_values)),
        "variation_of_information_nats": _variation_of_information(left_values, right_values),
        "noise_set_jaccard": noise_jaccard,
        "mapped_membership_matches": int((left_values == mapped_right).sum()),
        "mapped_membership_match_fraction": float((left_values == mapped_right).mean()),
        "changed_noise_status_count": int((left_noise != right_noise).sum()),
        "procrustes_disparity": procrustes_disparity,
        "interpretation": (
            "Structural concordance metrics are label-permutation invariant; numeric label equality "
            "is not treated as cluster identity. Procrustes, when finite, evaluates only supplied coordinates."
        ),
    }
    atomic_json_dump(json_safe(summary), root / "comparison_summary.json")
    manifest = base_manifest(command or sys.argv)
    manifest.update({
        "manifest_schema": "dimple-gwas.comparison-manifest.v3",
        "status": "complete",
        "finished_at_utc": utc_now(),
        "runtime_seconds": time.perf_counter() - started,
        "sources": {"left": file_record(left_path), "right": file_record(right_path)},
        "summary": json_safe(summary),
        "artifacts": {
            name: file_record(root / name)
            for name in [
                "comparison_summary.json", "label_confusion.tsv",
                "optimal_label_mapping.tsv", "membership_comparison.tsv", "cluster_sizes.tsv",
            ]
        },
    })
    atomic_json_dump(json_safe(manifest), root / "comparison_manifest.json")
    return summary
