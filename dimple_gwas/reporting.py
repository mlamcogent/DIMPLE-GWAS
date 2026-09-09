"""Required Freeze 2 artifact writers."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .io import atomic_json_dump, json_safe
from .provenance import file_record, sha256_file, utc_now
from .search_space import flatten_candidate


def _write_tsv(frame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, sep="\t", index=False)


def write_resolved_config(config: Mapping[str, Any], output_dir: str | Path) -> Path:
    import yaml

    destination = Path(output_dir) / "resolved_config.yaml"
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(dict(config), handle, sort_keys=False)
    return destination


def write_search_space(
    candidates: list[Mapping[str, Any]],
    config: Mapping[str, Any],
    output_dir: str | Path,
) -> dict[str, Path]:
    import pandas as pd

    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    rows = [flatten_candidate(candidate) for candidate in candidates]
    table = pd.DataFrame(rows)
    tsv_path = root / "search_space_manifest.tsv"
    json_path = root / "search_space_manifest.json"
    _write_tsv(table, tsv_path)
    atomic_json_dump({
        "search_mode": config["search_mode"],
        "candidate_models": len(candidates),
        "umap_configurations": int(table["umap_id"].nunique()) if not table.empty else 0,
        "hdbscan_configurations": int(table["hdbscan_id"].nunique()) if not table.empty else 0,
        "enumeration": "complete deterministic Cartesian product; no silent sampling",
        "candidates": [json_safe(row) for row in rows],
    }, json_path)
    return {"tsv": tsv_path, "json": json_path}


def _top_artifact(
    row,
    labels,
    feature_ids,
    candidate: Mapping[str, Any],
    config: Mapping[str, Any],
    root: Path,
    visualization=None,
    annotation_frame=None,
):
    import pandas as pd
    import yaml

    model_id = str(row["model_id"])
    target = root / "models" / "top_model_artifacts" / model_id
    target.mkdir(parents=True, exist_ok=True)
    label_table = pd.DataFrame({"feature_id": list(feature_ids), "label": labels})
    if visualization is not None:
        for index in range(visualization.shape[1]):
            label_table[f"UMAP_{index + 1}"] = visualization[:, index]
    label_table.to_csv(target / "labels.tsv", sep="\t", index=False)
    annotated = None
    if annotation_frame is not None:
        join_column = str(config.get("input", {}).get("annotation_index_col", "index"))
        annotation = annotation_frame.copy()
        annotation[join_column] = annotation[join_column].astype(str)
        annotation = annotation.drop_duplicates(subset=[join_column], keep="first")
        annotated = label_table.merge(annotation, left_on="feature_id", right_on=join_column, how="left")
        annotated.to_csv(target / "labels_with_annotations.tsv", sep="\t", index=False)
    summary = {
        "artifact_schema": "dimple-gwas.model-summary.v3",
        "model": json_safe(row.to_dict()),
        "parameters": {"umap": candidate["umap"], "hdbscan": candidate["hdbscan"]},
        "resolved_run_config": json_safe(config),
        "labels_file": "labels.tsv",
        "labels_sha256": sha256_file(target / "labels.tsv"),
        "feature_id_count": int(len(label_table)),
    }
    input_path = config.get("input", {}).get("path")
    if input_path and Path(input_path).is_file():
        summary["input"] = file_record(input_path)
    atomic_json_dump(summary, target / "summary.json")
    reproduce = dict(config)
    reproduce["search_mode"] = "fixed"
    reproduce["umap"] = dict(candidate["umap"])
    reproduce["hdbscan"] = dict(candidate["hdbscan"])
    reproduce["execution"] = dict(reproduce["execution"])
    with (target / "reproduce.yaml").open("w", encoding="utf-8") as handle:
        yaml.safe_dump(json_safe(reproduce), handle, sort_keys=False)
    return label_table, annotated


def write_model_outputs(
    ranked,
    top,
    pareto,
    families,
    candidates_by_id: Mapping[str, Mapping[str, Any]],
    labels_by_id: Mapping[str, Any],
    visualizations_by_umap: Mapping[str, Any],
    feature_ids,
    annotation_frame,
    config: Mapping[str, Any],
    scoring_manifest: Mapping[str, Any],
    run_manifest: Mapping[str, Any],
    output_dir: str | Path,
) -> dict[str, Any]:
    root = Path(output_dir)
    models_dir = root / "models"
    logs_dir = root / "logs"
    models_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    all_path = models_dir / "all_models.tsv"
    ranked_path = models_dir / "ranked_models.tsv"
    top_path = models_dir / "top_models.tsv"
    pareto_path = models_dir / "pareto_front.tsv"
    family_path = models_dir / "family_summaries.tsv"
    _write_tsv(ranked.sort_values("candidate_ordinal"), all_path)
    _write_tsv(ranked, ranked_path)
    _write_tsv(top, top_path)
    _write_tsv(pareto, pareto_path)
    _write_tsv(families, family_path)
    failures = ranked.loc[ranked["status"].eq("failed")].copy()
    _write_tsv(failures, logs_dir / "model_failures.tsv")

    parquet_status = {"written": False, "path": str(models_dir / "all_models.parquet"), "error": None}
    if bool(config.get("execution", {}).get("write_parquet", True)):
        try:
            ranked.sort_values("candidate_ordinal").to_parquet(models_dir / "all_models.parquet", index=False)
            parquet_status["written"] = True
        except Exception as exc:
            parquet_status["error"] = f"{type(exc).__name__}: {exc}"
    else:
        parquet_status["error"] = "disabled by execution.write_parquet=false"

    best_payload = None
    if not top.empty:
        best = top.sort_values("rank").iloc[0]
        candidate = candidates_by_id[str(best["model_id"])]
        best_payload = {
            "model": json_safe(best.to_dict()),
            "parameters": {"umap": candidate["umap"], "hdbscan": candidate["hdbscan"]},
            "resolved_run_config": json_safe(config),
        }
    atomic_json_dump(best_payload or {"model": None, "reason": "no eligible model"}, models_dir / "best_model.json")

    for _, row in top.iterrows():
        model_id = str(row["model_id"])
        if model_id in labels_by_id:
            label_table, annotated = _top_artifact(
                row,
                labels_by_id[model_id],
                feature_ids,
                candidates_by_id[model_id],
                config,
                root,
                visualization=visualizations_by_umap.get(candidates_by_id[model_id]["umap_id"]),
                annotation_frame=annotation_frame,
            )
            if int(row["rank"]) == 1:
                label_table.to_csv(root / "stage09_umap_vizdata_with_clusters.csv", index=False)
                if annotated is not None:
                    annotated.to_csv(root / "stage09b_umap_vizdata_with_annotations.csv", index=False)

    selection = dict(scoring_manifest)
    selection.update({
        "rank_order": ["score descending", "raw_score descending", "model_id ascending"],
        "candidate_models": int(len(ranked)),
        "successful_models": int(ranked["status"].eq("success").sum()),
        "invalid_topology_models": int(ranked["status"].eq("invalid_topology").sum()),
        "failed_models": int(ranked["status"].eq("failed").sum()),
        "top_n_requested": int(config["execution"]["top_n_models"]),
        "top_n_retained": int(len(top)),
        "selected_model": str(top.iloc[0]["model_id"]) if not top.empty else None,
        "pareto_note": "Pareto membership is supplementary and is not a uniquely correct clustering solution.",
    })
    atomic_json_dump(json_safe(selection), models_dir / "model_selection_manifest.json")

    manifest = dict(run_manifest)
    artifact_records = {
        name: file_record(path)
        for name, path in {
            "all_models": all_path,
            "ranked_models": ranked_path,
            "top_models": top_path,
            "pareto_front": pareto_path,
            "family_summaries": family_path,
            "model_failures": logs_dir / "model_failures.tsv",
        }.items()
    }
    manifest.update({
        "configuration": json_safe(config),
        "completed_models": int((ranked["status"] != "failed").sum()),
        "failed_models": int(ranked["status"].eq("failed").sum()),
        "selected_model": selection["selected_model"],
        "scoring_profile": config["scoring"]["profile"],
        "parquet_output": parquet_status,
        "artifacts": artifact_records,
        "status": "complete",
        "finished_at_utc": utc_now(),
    })
    atomic_json_dump(json_safe(manifest), root / "run_manifest.json")

    # Compatibility-oriented tabular aliases for users of the dev stage names.
    ranked.sort_values("candidate_ordinal").to_csv(root / "stage02_hdbscan_gridsearch_results.csv", index=False)
    ranked.to_csv(root / "stage03_optimized_cluster_solutions.csv", index=False)
    return {"selection": selection, "run_manifest": manifest, "parquet": parquet_status}
