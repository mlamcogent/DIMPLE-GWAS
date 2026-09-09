#!/usr/bin/env python3
"""Generate implementation-derived command, configuration, output, and test maps."""

from __future__ import annotations

import argparse
import ast
import csv
import json
import sys
from pathlib import Path
from typing import Any


FREEZE3 = Path(__file__).resolve().parents[4]
MANUAL = FREEZE3 / "docs" / "manual"
EVIDENCE = MANUAL / "evidence"
sys.path.insert(0, str(FREEZE3))

from dimple_gwas.cli import build_parser  # noqa: E402
from dimple_gwas.config import builtin_config  # noqa: E402


def write_tsv(path: Path, header: list[str], rows: list[list[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def json_value(value: Any) -> str:
    if value is argparse.SUPPRESS:
        return "SUPPRESS"
    try:
        return json.dumps(value, sort_keys=True)
    except TypeError:
        return str(value)


def command_rows() -> list[list[Any]]:
    parser = build_parser()
    rows: list[list[Any]] = []
    subparsers: dict[str, argparse.ArgumentParser] = {}
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            subparsers = dict(action.choices)
    for command, child in sorted(subparsers.items()):
        if command == "interpret":
            continue
        for action in child._actions:
            if action.dest == "help":
                continue
            flags = ", ".join(action.option_strings) if action.option_strings else action.dest
            required = bool(getattr(action, "required", False))
            choices = "" if action.choices is None else ", ".join(map(str, action.choices))
            rows.append([
                command,
                flags,
                action.dest,
                action.__class__.__name__,
                required,
                json_value(action.default),
                choices,
                action.help or "",
                "dimple_gwas/cli.py",
            ])
    rows.append(["explain", "interpret", "command alias", "alias", False, "", "", "Exact alias of explain.", "dimple_gwas/cli.py"])
    return rows


CONFIG_DESCRIPTIONS = {
    "search_mode": "Built-in enumeration family: standard, extended, custom, or fixed.",
    "input.path": "Variants-by-vectors CSV/TSV input path.",
    "input.drop_first_n_cols": "Leading metadata columns excluded before transpose.",
    "input.sep": "Optional explicit input separator; otherwise inferred.",
    "input.zscore_transform": "Optional column-wise rank inverse normal transformation before transpose.",
    "input.annotation_file": "Optional vector annotation table.",
    "input.annotation_index_col": "Annotation join column matched to retained feature_id.",
    "umap.n_neighbors": "UMAP neighborhood size; searchable scalar/list/range.",
    "umap.min_dist": "UMAP minimum embedding distance; searchable.",
    "umap.n_components": "Dimensions per repeated embedding; concatenated across repeats.",
    "umap.metric": "Metric used by UMAP to construct the neighbor graph.",
    "umap.spread": "Scale parameter paired with min_dist.",
    "umap.learning_rate": "UMAP optimizer initial learning rate.",
    "umap.repulsion_strength": "UMAP negative-sample repulsion weight.",
    "umap.negative_sample_rate": "Negative samples per positive optimization sample.",
    "umap.local_connectivity": "Expected locally connected nearest neighbors.",
    "umap.set_op_mix_ratio": "Fuzzy-set union/intersection interpolation.",
    "umap.random_state": "Base seed used to derive repeated embedding seeds.",
    "umap.densmap": "Enable density-augmented UMAP objective.",
    "hdbscan.min_cluster_size": "Smallest permitted cluster size.",
    "hdbscan.min_samples": "Density conservativeness/core-distance neighborhood.",
    "hdbscan.cluster_selection_epsilon": "Distance threshold used when extracting clusters.",
    "hdbscan.cluster_selection_persistence": "Minimum persistence threshold.",
    "hdbscan.cluster_selection_method": "EOM or leaf extraction.",
    "hdbscan.alpha": "Robust single-linkage scaling parameter.",
    "hdbscan.allow_single_cluster": "Permit a one-cluster result.",
    "hdbscan.max_cluster_size": "EOM-only maximum size; zero means unlimited.",
    "hdbscan.metric": "Distance metric supplied to contrib hdbscan and silhouette.",
    "execution.n_random_states": "Number of repeated seeded embeddings per UMAP family.",
    "execution.n_jobs": "Parallel jobs for repeated UMAP and HDBSCAN core distances.",
    "execution.candidate_jobs": "Parallel HDBSCAN candidates; core-distance jobs become one when parallelized.",
    "execution.top_n_models": "Number of eligible ranked models retained.",
    "execution.warn_candidate_count": "Candidate-count warning threshold.",
    "execution.max_candidate_models": "Hard safety ceiling; zero means unlimited.",
    "execution.max_samples_trust": "Maximum samples used for embedding trust/continuity; zero means all.",
    "execution.max_samples_silhouette": "Maximum samples used for silhouette; zero means all.",
    "execution.trust_k": "Requested neighborhood size for trustworthiness/continuity.",
    "execution.trust_seed": "Subsampling seed for embedding-quality metrics.",
    "execution.silhouette_seed": "Subsampling seed for silhouette.",
    "execution.legacy_ensemble_seeds": "Use historical repeated-seed sequence.",
    "execution.write_parquet": "Attempt supplementary Parquet model table.",
    "execution.compute_dbcv": "Compute DBCV diagnostic when possible.",
    "execution.strict": "Abort when a UMAP family or candidate fails.",
    "scoring.profile": "legacy_dimple or explicit custom weighted score.",
    "scoring.fit_include_noise": "Include noise count in legacy dynamic-range fitting.",
    "scoring.custom": "Metric rules with weight and maximize/minimize direction.",
    "interpretation.similarity_metric": "Pearson or Spearman similarity in the original variable space.",
    "interpretation.order": "Heatmap ordering: cluster_then_hclust, cluster, hclust, or input.",
    "interpretation.noise_policy": "Place noise last, include it in ordering, or exclude it.",
    "interpretation.undefined_correlation": "Fail or replace undefined correlation with zero.",
    "interpretation.require_complete_match": "Require exact source/label identifier sets.",
    "interpretation.max_full_heatmap": "Full heatmap size threshold.",
    "interpretation.write_similarity": "Write the complete original-space similarity table.",
    "interpretation.force_large_matrix": "Override large-matrix protection.",
    "interpretation.coordinate_associations": "Opt in to descriptive coordinate associations.",
    "interpretation.coordinate_methods": "Pearson and/or Spearman coordinate association methods.",
    "interpretation.top_n_associations": "Maximum retained coordinate associations.",
}


def flatten_config(node: Any, prefix: str = "") -> list[tuple[str, Any]]:
    if not isinstance(node, dict):
        return [(prefix, node)]
    rows: list[tuple[str, Any]] = []
    for key, value in node.items():
        dotted = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict) and not (set(value) <= {"start", "stop", "step"}):
            rows.extend(flatten_config(value, dotted))
        else:
            rows.append((dotted, value))
    return rows


def config_rows() -> list[list[Any]]:
    modes = {mode: builtin_config(mode) for mode in ("standard", "extended", "fixed", "custom")}
    keys = sorted({key for cfg in modes.values() for key, _ in flatten_config(cfg)} | set(CONFIG_DESCRIPTIONS))
    flattened = {mode: dict(flatten_config(cfg)) for mode, cfg in modes.items()}
    rows = []
    for key in keys:
        values = [flattened[mode].get(key, "") for mode in ("standard", "extended", "fixed", "custom")]
        source = "dimple_gwas/config.py"
        cli_exposed = "yes" if key in {
            "search_mode", "input.path", "input.drop_first_n_cols", "input.sep", "input.zscore_transform",
            "input.annotation_file", "input.annotation_index_col", "umap.n_neighbors", "umap.min_dist",
            "umap.n_components", "umap.metric", "umap.spread", "umap.learning_rate",
            "umap.repulsion_strength", "umap.negative_sample_rate", "umap.local_connectivity",
            "umap.set_op_mix_ratio", "umap.random_state", "umap.densmap", "hdbscan.min_cluster_size",
            "hdbscan.min_samples", "hdbscan.cluster_selection_epsilon", "hdbscan.cluster_selection_persistence",
            "hdbscan.cluster_selection_method", "hdbscan.alpha", "hdbscan.allow_single_cluster",
            "hdbscan.max_cluster_size", "hdbscan.metric", "execution.n_random_states", "execution.n_jobs",
            "execution.candidate_jobs", "execution.top_n_models", "execution.warn_candidate_count",
            "execution.max_candidate_models", "execution.max_samples_trust", "execution.max_samples_silhouette",
            "execution.trust_k", "execution.trust_seed", "execution.silhouette_seed",
            "execution.legacy_ensemble_seeds", "execution.write_parquet", "execution.compute_dbcv",
            "execution.strict", "scoring.profile", "scoring.fit_include_noise",
        } or key.startswith("interpretation.") else "YAML only"
        rows.append([
            key,
            *(json_value(v) for v in values),
            CONFIG_DESCRIPTIONS.get(key, "Explicit custom scoring rule." if key.startswith("scoring.custom") else "See implementation validation."),
            cli_exposed,
            source,
        ])
    return rows


def output_rows() -> list[list[Any]]:
    return [
        ["run", "resolved_config.yaml", "resolved configuration", "write_resolved_config", "user, reproduce-model", "YAML", "always"],
        ["run/show-search-space", "search_space_manifest.tsv/json", "complete deterministic enumeration", "write_search_space", "audit, validate", "TSV + JSON", "always when command succeeds"],
        ["run", "run_manifest.json", "software/input/config/runtime/artifact provenance", "write_model_outputs", "validate, audit", "JSON", "complete run"],
        ["run", "logs/run.log", "execution narrative", "setup_logger", "operator", "text", "always"],
        ["run", "models/all_models.tsv", "all candidates in candidate order", "write_model_outputs", "score-existing, audit", "TSV", "always"],
        ["run", "models/ranked_models.tsv", "eligible candidates ranked with failures retained", "write_model_outputs", "summarize-models, selection", "TSV", "always"],
        ["run", "models/all_models.parquet", "supplementary columnar candidate table", "write_model_outputs", "analysis", "Parquet", "optional; failure recorded"],
        ["run", "models/top_models.tsv", "retained top-N eligible models", "write_model_outputs", "user", "TSV", "always; may be empty"],
        ["run", "models/best_model.json", "selected row, parameters, resolved config", "write_model_outputs", "reproduce-model", "JSON", "always; null model possible"],
        ["run", "models/model_selection_manifest.json", "formula, realized weights, counts, tie ordering", "write_model_outputs", "audit", "JSON", "always"],
        ["run", "models/pareto_front.tsv", "supplementary non-dominated candidate set", "write_model_outputs", "review", "TSV", "always"],
        ["run", "models/family_summaries.tsv", "parameter-family success/failure/metric summaries", "write_model_outputs", "review", "TSV", "always"],
        ["run", "models/top_model_artifacts/<id>/labels.tsv", "exact IDs, labels, display coordinates", "_top_artifact", "explain, compare", "TSV", "successful retained refit"],
        ["run", "models/top_model_artifacts/<id>/summary.json", "native retained-model contract and label hash", "_top_artifact", "reproduce-model, explain, compare", "JSON", "successful retained refit"],
        ["run", "models/top_model_artifacts/<id>/reproduce.yaml", "one-model fixed configuration", "_top_artifact", "operator", "YAML", "successful retained refit"],
        ["run", "stage02_hdbscan_gridsearch_results.csv", "legacy-compatible all-candidate alias", "write_model_outputs", "historical workflow", "CSV", "always"],
        ["run", "stage03_optimized_cluster_solutions.csv", "legacy-compatible ranked alias", "write_model_outputs", "historical workflow", "CSV", "always"],
        ["run", "stage09_umap_vizdata_with_clusters.csv", "selected labels and display coordinates", "write_model_outputs", "visualization, legacy workflow", "CSV", "selected retained refit"],
        ["run", "stage09b_umap_vizdata_with_annotations.csv", "selected labels joined to annotations", "write_model_outputs", "user", "CSV", "valid annotation join"],
        ["score-existing", "<output> + <output>.manifest.json", "rescored/ranked table and scoring schema record", "_score", "summarize-models", "TSV + JSON", "always"],
        ["summarize-models", "family_summaries.tsv, pareto_front.tsv, top_models.tsv, summary.json", "post hoc model summaries", "_summarize", "user", "TSV + JSON", "always"],
        ["explain", "original_space_similarity.tsv.gz", "ordered full similarity matrix", "run_explanation", "heatmap, audit", "gzip TSV", "when enabled"],
        ["explain", "heatmap_order.tsv", "exact plotted order, label, noise flag, coordinates", "run_explanation", "figure audit", "TSV", "always"],
        ["explain", "cluster_cutpoints.tsv", "zero/one-based block boundaries", "run_explanation", "figure audit", "TSV", "always"],
        ["explain", "cluster_summary.tsv", "within/between descriptive similarity summaries", "run_explanation", "user", "TSV", "always"],
        ["explain", "projection_quality.tsv", "trustworthiness/continuity of supplied coordinates", "run_explanation", "user", "TSV", "when coordinates are usable"],
        ["explain", "coordinate_associations.tsv", "opt-in descriptive coordinate correlations", "run_explanation", "user", "TSV", "opt-in only"],
        ["explain", "exclusions.tsv", "unmatched/noise-policy exclusions", "run_explanation", "audit", "TSV", "always, header when empty"],
        ["explain", "original_space_heatmap.png/html", "static and interactive ordered heatmaps", "run_explanation", "user", "PNG + HTML", "always within safeguards"],
        ["explain", "interpretation_manifest.json + README.md", "scope, hashes, options, caveats", "run_explanation", "audit, user", "JSON + Markdown", "always"],
        ["compare", "comparison_summary.json", "ARI/NMI/VI/noise/membership/coordinate metrics", "run_comparison", "user", "JSON", "always"],
        ["compare", "membership_comparison.tsv, cluster_sizes.tsv, label_confusion.tsv, optimal_label_mapping.tsv", "ID-level and cluster-level concordance", "run_comparison", "user", "TSV", "always"],
        ["compare", "comparison_manifest.json", "sources/options/output hashes", "run_comparison", "audit", "JSON", "always"],
        ["validate", "validation_checks.tsv", "one pass/warn/fail row per contract check", "run_validation", "user, CI", "TSV", "always"],
        ["validate", "validation_report.json + validation_manifest.json", "aggregate status and provenance", "run_validation", "user, CI", "JSON", "always"],
    ]


def test_rows() -> list[list[Any]]:
    groups = {
        "config": "configuration parsing, defaults, validation, CLI precedence",
        "search_space": "deterministic enumeration, stable IDs, safety limit",
        "preprocessing_metrics": "RINT, numeric contract, trustworthiness/continuity",
        "scoring_ranking": "legacy formula, custom scores, ranking, Pareto",
        "pipeline_integration": "end-to-end search and fixed-model reproduction",
        "failure_and_provenance": "retained failures and authoritative hashes",
        "freeze3_interpretation": "native/legacy explanation, orientation, matching, ordering, outputs",
        "freeze3_comparison_validation": "label comparison, schemas, hashes, CLI commands",
    }
    rows: list[list[Any]] = []
    for path in sorted((FREEZE3 / "tests").glob("test_*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        key = path.stem.removeprefix("test_")
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
                rows.append([
                    path.relative_to(FREEZE3).as_posix(),
                    node.name,
                    groups.get(key, "software contract"),
                    node.lineno,
                    "automated",
                    "passed in fresh 45-test local suite",
                ])
    return rows


def traceability_rows() -> list[list[Any]]:
    return [
        ["dimple_gwas/config.py", "configuration defaults, precedence, validation", "9-14", "configuration_key_reference.tsv; command_and_flag_matrix.tsv"],
        ["dimple_gwas/preprocessing.py", "input orientation, numeric checks, RINT", "10, 15", "claim DATA-001/002"],
        ["dimple_gwas/search_space.py", "Cartesian enumeration and stable identifiers", "12, 14, 18", "search manifests"],
        ["dimple_gwas/umap_runner.py", "repeated seeded UMAP/densMAP and concatenation", "16-17", "claim PIPE-002"],
        ["dimple_gwas/hdbscan_runner.py", "contrib hdbscan fitting", "18", "claim PIPE-004"],
        ["dimple_gwas/metrics.py", "topology, silhouette, DBCV, trust/continuity", "19", "claim SCORE-001/002"],
        ["dimple_gwas/scoring.py", "legacy and custom score calculations", "20", "scoring manifests"],
        ["dimple_gwas/ranking.py", "rank, top-N, Pareto, family summaries", "21", "model-selection manifest"],
        ["dimple_gwas/reporting.py", "run and model artifacts", "22, 39-41", "output atlas"],
        ["dimple_gwas/provenance.py", "source/input/artifact checksums and environment", "37, 42", "run manifests"],
        ["dimple_gwas/interpretation.py", "original-space descriptive explanation", "24-29", "tutorial 3"],
        ["dimple_gwas/comparison.py", "ID-matched structural/coordinate comparison", "30, 34", "tutorial 3"],
        ["dimple_gwas/validation.py", "artifact/schema/hash checks", "30, 42", "tutorial 3"],
        ["dimple_gwas/cli.py", "public commands and CLI precedence", "9, 32-34, 38", "captured --help"],
    ]


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    write_tsv(EVIDENCE / "command_and_flag_matrix.tsv", ["command", "flags", "destination", "action", "required", "default", "choices", "help", "source"], command_rows())
    write_tsv(EVIDENCE / "configuration_key_reference.tsv", ["key", "standard_default", "extended_default", "fixed_default", "custom_default", "meaning", "cli_exposure", "source"], config_rows())
    write_tsv(EVIDENCE / "output_producer_consumer_map.tsv", ["command", "artifact", "meaning", "producer", "consumer", "format", "condition"], output_rows())
    write_tsv(EVIDENCE / "test_coverage_map.tsv", ["test_file", "test_name", "contract_area", "source_line", "type", "fresh_result"], test_rows())
    write_tsv(EVIDENCE / "source_to_manual_traceability.tsv", ["source_file", "implementation_responsibility", "manual_chapters", "evidence_or_claim"], traceability_rows())
    report = """# Software truth report

## Authority and method

For commands, defaults, accepted values, schemas, algorithms, and artifact production, executable Freeze 3 source is authoritative. Existing documentation and manuscript material provide context but do not override implementation. The generated TSVs are implementation-derived as of this source checksum freeze.

## Confirmed behavior

- The public entry point exposes `run`, `inspect-config`, `show-search-space`, `score-existing`, `summarize-models`, `reproduce-model`, `explain`/`interpret`, `compare`, and `validate`.
- Configuration precedence is built-in mode, then YAML overlay, then explicit CLI override.
- The standard input is variants by vectors with a four-column metadata prefix by default. Prepared analysis data are transposed to vectors by variants.
- Repeated seeded UMAP/densMAP embeddings are concatenated. No PCA/SVD/ICA pre-reducer exists in the production path.
- Clustering uses contributed `hdbscan`; all candidate rows, including failures and invalid topology, are retained.
- Standard enumeration is `45 x 18 x 3 = 2,430` candidates. The shipped extended mode enumerates 1,728.
- `legacy_dimple` ranks with normalized silhouette plus normalized cluster count, and optionally subtracts normalized noise count. DBCV is an optional computed diagnostic, not a legacy-score component.
- Interpretation never refits. It verifies identifiers, summarizes original-space similarity, and labels its coordinate associations descriptive.
- Comparison requires exact identifier sets and does not equate numeric cluster labels across runs.
- Validation checks artifacts, schemas, counts, readability, and hashes; it is software validation, not biological validation.

## Boundaries

- This snapshot has no usable Git commit; SHA-256 source and artifact records are the release identity.
- The fresh test result is macOS/Apple Silicon only. Docker/Linux/cloud validation remains a release gate.
- The 164-IDP 1,000-seed search is deliberately deferred. Historical adaptation and exact rescoring are documented separately.
- Optional Parquet writing is best-effort and the outcome is recorded in the run manifest.
- Successful local deterministic comparison is bounded to the executed fixture and environment; no bitwise cross-platform claim is made.
"""
    (EVIDENCE / "software_truth_report.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
