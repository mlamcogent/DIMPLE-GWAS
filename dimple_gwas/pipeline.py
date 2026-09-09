"""Freeze 3 end-to-end topology-search workflow."""

from __future__ import annotations

import json
import logging
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping

from .hdbscan_runner import fit_hdbscan
from .io import read_table
from .metrics import embedding_quality_metrics, evaluate_candidate
from .preprocessing import prepare_analysis_matrix
from .provenance import base_manifest, file_record
from .ranking import family_summaries, pareto_front, rank_models, top_models
from .reporting import write_model_outputs, write_resolved_config, write_search_space
from .scoring import apply_scoring
from .search_space import canonical_json, enumerate_candidates, flatten_candidate, stable_identifier
from .umap_runner import run_repeated_umap


def setup_logger(output_dir: str | Path) -> logging.Logger:
    root = Path(output_dir)
    (root / "logs").mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("dimple_gwas.freeze3")
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    file_handler = logging.FileHandler(root / "logs" / "run.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(console)
    logger.addHandler(file_handler)
    logger.propagate = False
    return logger


def _failed_row(candidate: Mapping[str, Any], error: Exception | str, umap_runtime: float = 0.0):
    row = flatten_candidate(candidate)
    row.update({
        "status": "failed",
        "error_message": str(error),
        "metric_warnings": "",
        "runtime_seconds": 0.0,
        "umap_runtime_seconds": float(umap_runtime),
        "number_of_clusters": None,
        "number_of_noise_points": None,
        "noise_fraction": None,
        "largest_cluster_size": None,
        "largest_cluster_fraction": None,
        "smallest_cluster_size": None,
        "median_cluster_size": None,
        "mean_cluster_size": None,
        "cluster_size_dispersion": None,
        "silhouette": None,
        "dbcv": None,
        "calinski_harabasz": None,
        "davies_bouldin": None,
    })
    return row


def _evaluate_one(
    candidate: Mapping[str, Any],
    embedding,
    embedding_metrics: Mapping[str, Any],
    umap_runtime: float,
    seeds: list[int],
    fit_include_noise: bool,
    compute_dbcv: bool,
    core_dist_n_jobs: int,
    max_samples_silhouette: int,
    silhouette_seed: int,
) -> dict[str, Any]:
    row = flatten_candidate(candidate)
    try:
        fitted = fit_hdbscan(embedding, candidate["hdbscan"], core_dist_n_jobs=core_dist_n_jobs)
        model_metrics = evaluate_candidate(
            embedding,
            fitted["labels"],
            fitted["clusterer"],
            silhouette_metric=str(candidate["hdbscan"]["metric"]),
            fit_include_noise=fit_include_noise,
            compute_dbcv=compute_dbcv,
            max_samples_silhouette=max_samples_silhouette,
            silhouette_seed=silhouette_seed,
        )
        row.update(embedding_metrics)
        row.update(model_metrics)
        row.update({
            "status": "success" if int(model_metrics["number_of_clusters"]) >= 2 else "invalid_topology",
            "error_message": "" if int(model_metrics["number_of_clusters"]) >= 2 else "fewer than two non-noise clusters",
            "runtime_seconds": float(fitted["runtime_seconds"]),
            "umap_runtime_seconds": float(umap_runtime),
            "umap_seeds": json.dumps(seeds),
            "parameter_notes": (
                "max_cluster_size has no effect for leaf selection"
                if candidate["hdbscan"]["cluster_selection_method"] == "leaf"
                and int(candidate["hdbscan"]["max_cluster_size"]) != 0
                else ""
            ),
        })
        return row
    except Exception as exc:
        row = _failed_row(candidate, f"{type(exc).__name__}: {exc}", umap_runtime=umap_runtime)
        row["umap_seeds"] = json.dumps(seeds)
        return row


def _annotation_frame(config: Mapping[str, Any], logger: logging.Logger):
    annotation_path = config.get("input", {}).get("annotation_file")
    if not annotation_path:
        return None
    try:
        frame = read_table(annotation_path)
    except Exception as exc:
        logger.warning("Annotation file could not be read and will be skipped: %s", exc)
        return None
    join_column = str(config.get("input", {}).get("annotation_index_col", "index"))
    if join_column not in frame.columns:
        logger.warning("Annotation file lacks join column %r and will be skipped", join_column)
        return None
    return frame


def run_search(config: Mapping[str, Any], output_dir: str | Path, command: list[str] | None = None) -> dict[str, Any]:
    import pandas as pd
    from joblib import Parallel, delayed

    started = time.perf_counter()
    manifest = base_manifest(command)
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    logger = setup_logger(root)
    write_resolved_config(config, root)

    candidates = enumerate_candidates(config)
    write_search_space(candidates, config, root)
    candidates_by_id = {candidate["model_id"]: candidate for candidate in candidates}
    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for candidate in candidates:
        grouped[candidate["umap_id"]].append(candidate)
    logger.info(
        "Resolved %d candidate models across %d UMAP and %d HDBSCAN configurations",
        len(candidates),
        len(grouped),
        len({candidate["hdbscan_id"] for candidate in candidates}),
    )

    input_path = config.get("input", {}).get("path")
    if not input_path:
        raise ValueError("An input matrix is required (input.path or --input)")
    input_frame = read_table(input_path, sep=config.get("input", {}).get("sep"))
    analysis = prepare_analysis_matrix(input_frame, config.get("input", {}))
    feature_ids = analysis.index.tolist()
    logger.info("Prepared analysis matrix with %d features and %d input variables", analysis.shape[0], analysis.shape[1])
    annotation = _annotation_frame(config, logger)

    execution = config.get("execution", {})
    fit_include_noise = bool(config.get("scoring", {}).get("fit_include_noise", False))
    strict = bool(execution.get("strict", False))
    candidate_jobs = int(execution.get("candidate_jobs", 1))
    core_jobs = int(execution.get("n_jobs", -1)) if candidate_jobs == 1 else 1
    rows: list[dict[str, Any]] = []
    embedding_cache: dict[str, Any] = {}
    visualization_cache: dict[str, Any] = {}
    umap_done = 0

    for umap_id, group in grouped.items():
        umap_done += 1
        umap_params = group[0]["umap"]
        logger.info("UMAP family %d/%d: %s (%d candidate models)", umap_done, len(grouped), umap_id, len(group))
        try:
            embedded = run_repeated_umap(
                analysis,
                umap_params,
                repeats=int(execution.get("n_random_states", 1)),
                n_jobs=int(execution.get("n_jobs", -1)),
                legacy_sequence=bool(execution.get("legacy_ensemble_seeds", False)),
            )
            quality = embedding_quality_metrics(
                analysis.values,
                embedded["embedding"],
                requested_k=int(execution.get("trust_k", 30)),
                max_samples=int(execution.get("max_samples_trust", 3000)),
                seed=int(execution.get("trust_seed", 42)),
            )
            embedding_cache[umap_id] = embedded["embedding"]
            visualization_cache[umap_id] = embedded["visualization_embedding"]
        except Exception as exc:
            logger.exception("UMAP family %s failed", umap_id)
            rows.extend(_failed_row(candidate, f"UMAP {type(exc).__name__}: {exc}") for candidate in group)
            if strict:
                raise
            continue

        arguments = (
            embedded["embedding"],
            quality,
            float(embedded["runtime_seconds"]),
            list(embedded["seeds"]),
            fit_include_noise,
            bool(execution.get("compute_dbcv", True)),
            core_jobs,
            int(execution.get("max_samples_silhouette", 0)),
            int(execution.get("silhouette_seed", 42)),
        )
        if candidate_jobs == 1:
            group_rows = [_evaluate_one(candidate, *arguments) for candidate in group]
        else:
            group_rows = Parallel(n_jobs=candidate_jobs)(
                delayed(_evaluate_one)(candidate, *arguments) for candidate in group
            )
        rows.extend(group_rows)
        failures = sum(row["status"] == "failed" for row in group_rows)
        logger.info("Completed UMAP family %s: %d evaluated, %d failed", umap_id, len(group_rows), failures)
        if strict and failures:
            raise RuntimeError(f"Strict mode: {failures} HDBSCAN candidates failed in {umap_id}")

    models = pd.DataFrame(rows)
    if models.empty:
        raise RuntimeError("No candidate model rows were produced")
    scored, scoring_manifest = apply_scoring(models, config.get("scoring", {}))
    ranked = rank_models(scored)
    top = top_models(ranked, int(execution.get("top_n_models", 20)))
    pareto = pareto_front(ranked)
    families = family_summaries(ranked)

    labels_by_id = {}
    for _, top_row in top.iterrows():
        model_id = str(top_row["model_id"])
        candidate = candidates_by_id[model_id]
        try:
            fitted = fit_hdbscan(
                embedding_cache[candidate["umap_id"]],
                candidate["hdbscan"],
                core_dist_n_jobs=core_jobs,
            )
            labels_by_id[model_id] = fitted["labels"]
        except Exception as exc:
            logger.error("Could not refit top model %s for label retention: %s", model_id, exc)

    manifest.update({
        "input": file_record(input_path),
        "input_contract": {
            "orientation": "variants_by_vectors",
            "drop_first_n_cols": int(config.get("input", {}).get("drop_first_n_cols", 4)),
            "separator": config.get("input", {}).get("sep"),
            "preprocessing": config.get("input", {}).get("zscore_transform", "none"),
            "vector_identifier_source": "analysis column names",
        },
        "configuration_sha256": stable_identifier("sha256", config, length=64).split("_", 1)[1],
        "random_seeds": sorted({seed for value in ranked.get("umap_seeds", []) if isinstance(value, str) for seed in json.loads(value)}),
        "thread_settings": {
            "n_jobs": int(execution.get("n_jobs", -1)),
            "candidate_jobs": candidate_jobs,
            "hdbscan_core_dist_n_jobs": core_jobs,
        },
        "backends": {"reducer": "umap-learn", "clusterer": "hdbscan.contrib"},
        "scoring_formula_version": str(scoring_manifest.get("formula", scoring_manifest.get("profile", "unknown"))),
        "search_space_size": len(candidates),
        "umap_configurations": len(grouped),
        "runtime_seconds": time.perf_counter() - started,
    })
    output_status = write_model_outputs(
        ranked,
        top,
        pareto,
        families,
        candidates_by_id,
        labels_by_id,
        visualization_cache,
        feature_ids,
        annotation,
        config,
        scoring_manifest,
        manifest,
        root,
    )
    logger.info(
        "Run complete: %d successful, %d invalid topology, %d failed; selected=%s",
        int(ranked["status"].eq("success").sum()),
        int(ranked["status"].eq("invalid_topology").sum()),
        int(ranked["status"].eq("failed").sum()),
        output_status["selection"]["selected_model"],
    )
    return {
        "ranked": ranked,
        "top": top,
        "pareto": pareto,
        "families": families,
        "output_status": output_status,
    }
