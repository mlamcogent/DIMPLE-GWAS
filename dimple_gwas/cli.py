"""Command-line interface for DIMPLE-GWAS Freeze 3."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from . import __version__
from .config import config_as_json, resolve_config, validate_config
from .io import atomic_json_dump, json_safe, read_model_table
from .pipeline import run_search
from .ranking import family_summaries, pareto_front, rank_models, top_models
from .reporting import write_search_space
from .scoring import apply_scoring, normalize_model_table_schema
from .search_space import count_candidates, enumerate_candidates, flatten_candidate


def _add_config_source(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--search-mode", choices=["standard", "extended", "custom", "fixed"], default="standard")
    parser.add_argument("--config", help="YAML configuration; explicit CLI values override it")


def _add_run_options(parser: argparse.ArgumentParser, include_output: bool = True) -> None:
    parser.add_argument("--input", "--datainput", dest="input_path", help="GWAS summary-statistics matrix (CSV/TSV)")
    if include_output:
        parser.add_argument("--output-dir", "--outdir", default="outputs")
    parser.add_argument("--drop-first-n-cols", "--drop_first_n_cols", type=int)
    parser.add_argument("--sep")
    parser.add_argument("--zscore-transform", "--zscore_transform", choices=["none", "rint"])
    parser.add_argument("--annotation-file", "--annotation_file", "--idp_key", dest="annotation_file")
    parser.add_argument("--annotation-index-col", "--annotation_index_col")

    parser.add_argument("--umap-n-neighbors", "--n-neighbors", "--n_neighbors", dest="umap_n_neighbors")
    parser.add_argument("--umap-min-dist", "--min-dist", "--min_dist", dest="umap_min_dist")
    parser.add_argument("--umap-n-components", "--n-components", "--n_components", dest="umap_n_components")
    parser.add_argument("--umap-metric", "--umap_metric")
    parser.add_argument("--umap-spread")
    parser.add_argument("--umap-learning-rate")
    parser.add_argument("--umap-repulsion-strength")
    parser.add_argument("--umap-negative-sample-rate")
    parser.add_argument("--umap-local-connectivity")
    parser.add_argument("--umap-set-op-mix-ratio")
    parser.add_argument("--random-state", "--random_state", dest="umap_random_state")
    parser.add_argument("--densmap", dest="umap_densmap", action="store_true", default=None)
    parser.add_argument("--no-densmap", dest="umap_densmap", action="store_false")

    parser.add_argument("--hdbscan-min-cluster-size", "--grid-min-cluster-size", "--grid_min_cluster_size", dest="hdbscan_min_cluster_size")
    parser.add_argument("--hdbscan-min-samples", "--grid-min-samples", "--grid_min_samples", dest="hdbscan_min_samples")
    parser.add_argument("--hdbscan-cluster-selection-epsilon", "--grid-eps", "--grid_eps", dest="hdbscan_cluster_selection_epsilon")
    parser.add_argument("--hdbscan-cluster-selection-persistence", "--grid-cluster-selection-persistence", "--grid_cluster_selection_persistence", dest="hdbscan_cluster_selection_persistence")
    parser.add_argument("--hdbscan-cluster-selection-method", "--grid-cluster-selection-method", "--grid_cluster_selection_method", "--cluster_selection_method", dest="hdbscan_cluster_selection_method")
    parser.add_argument("--hdbscan-alpha", "--grid-alpha", "--grid_alpha", dest="hdbscan_alpha")
    parser.add_argument("--hdbscan-allow-single-cluster", "--grid-allow-single-cluster", "--grid_allow_single_cluster", dest="hdbscan_allow_single_cluster")
    parser.add_argument("--hdbscan-max-cluster-size", "--max-cluster-size", "--max_cluster_size", dest="hdbscan_max_cluster_size")
    parser.add_argument("--hdbscan-metric", "--hdbscan_metric")

    parser.add_argument("--n-random-states", "--n_random_states", type=int)
    parser.add_argument("--n-jobs", "--n_jobs", type=int)
    parser.add_argument("--candidate-jobs", type=int)
    parser.add_argument("--top-n-models", type=int)
    parser.add_argument("--warn-candidate-count", type=int)
    parser.add_argument("--max-candidate-models", type=int)
    parser.add_argument("--max-samples-trust", "--max_samples_trust", type=int)
    parser.add_argument("--max-samples-silhouette", type=int)
    parser.add_argument("--trust-k", "--trust_k", type=int)
    parser.add_argument("--trust-seed", "--trust_seed", type=int)
    parser.add_argument("--silhouette-seed", type=int)
    parser.add_argument("--legacy-ensemble-seeds", dest="legacy_ensemble_seeds", action="store_true", default=None)
    parser.add_argument("--no-legacy-ensemble-seeds", dest="legacy_ensemble_seeds", action="store_false")
    parser.add_argument("--compute-dbcv", dest="compute_dbcv", action="store_true", default=None)
    parser.add_argument("--no-compute-dbcv", dest="compute_dbcv", action="store_false")
    parser.add_argument("--write-parquet", dest="write_parquet", action="store_true", default=None)
    parser.add_argument("--no-write-parquet", dest="write_parquet", action="store_false")
    parser.add_argument("--strict", dest="strict", action="store_true", default=None)

    parser.add_argument("--scoring-profile", choices=["legacy_dimple", "custom"])
    parser.add_argument("--fit-include-noise", dest="fit_include_noise", action="store_true", default=None)
    parser.add_argument("--fit-exclude-noise", dest="fit_include_noise", action="store_false")


OVERRIDE_MAP = {
    "input_path": "input.path",
    "drop_first_n_cols": "input.drop_first_n_cols",
    "sep": "input.sep",
    "zscore_transform": "input.zscore_transform",
    "annotation_file": "input.annotation_file",
    "annotation_index_col": "input.annotation_index_col",
    "umap_n_neighbors": "umap.n_neighbors",
    "umap_min_dist": "umap.min_dist",
    "umap_n_components": "umap.n_components",
    "umap_metric": "umap.metric",
    "umap_spread": "umap.spread",
    "umap_learning_rate": "umap.learning_rate",
    "umap_repulsion_strength": "umap.repulsion_strength",
    "umap_negative_sample_rate": "umap.negative_sample_rate",
    "umap_local_connectivity": "umap.local_connectivity",
    "umap_set_op_mix_ratio": "umap.set_op_mix_ratio",
    "umap_random_state": "umap.random_state",
    "umap_densmap": "umap.densmap",
    "hdbscan_min_cluster_size": "hdbscan.min_cluster_size",
    "hdbscan_min_samples": "hdbscan.min_samples",
    "hdbscan_cluster_selection_epsilon": "hdbscan.cluster_selection_epsilon",
    "hdbscan_cluster_selection_persistence": "hdbscan.cluster_selection_persistence",
    "hdbscan_cluster_selection_method": "hdbscan.cluster_selection_method",
    "hdbscan_alpha": "hdbscan.alpha",
    "hdbscan_allow_single_cluster": "hdbscan.allow_single_cluster",
    "hdbscan_max_cluster_size": "hdbscan.max_cluster_size",
    "hdbscan_metric": "hdbscan.metric",
    "n_random_states": "execution.n_random_states",
    "n_jobs": "execution.n_jobs",
    "candidate_jobs": "execution.candidate_jobs",
    "top_n_models": "execution.top_n_models",
    "warn_candidate_count": "execution.warn_candidate_count",
    "max_candidate_models": "execution.max_candidate_models",
    "max_samples_trust": "execution.max_samples_trust",
    "max_samples_silhouette": "execution.max_samples_silhouette",
    "trust_k": "execution.trust_k",
    "trust_seed": "execution.trust_seed",
    "silhouette_seed": "execution.silhouette_seed",
    "legacy_ensemble_seeds": "execution.legacy_ensemble_seeds",
    "compute_dbcv": "execution.compute_dbcv",
    "write_parquet": "execution.write_parquet",
    "strict": "execution.strict",
    "scoring_profile": "scoring.profile",
    "fit_include_noise": "scoring.fit_include_noise",
}


def _overrides(args: argparse.Namespace) -> dict[str, Any]:
    return {
        dotted: getattr(args, attribute)
        for attribute, dotted in OVERRIDE_MAP.items()
        if hasattr(args, attribute) and getattr(args, attribute) is not None
    }


def _resolved(args: argparse.Namespace):
    if args.search_mode == "custom" and not args.config:
        raise ValueError("custom search mode requires --config")
    return resolve_config(args.search_mode, args.config, _overrides(args))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dimple-gwas",
        description="DIMPLE-GWAS Freeze 3 topology search and original-space interpretation",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser("run", help="Run UMAP/HDBSCAN topology search")
    _add_config_source(run)
    _add_run_options(run)

    inspect = subparsers.add_parser("inspect-config", help="Resolve and validate configuration")
    _add_config_source(inspect)
    _add_run_options(inspect, include_output=False)
    inspect.add_argument("--output", help="Optional resolved YAML path")

    show = subparsers.add_parser("show-search-space", help="Enumerate candidate models without fitting")
    _add_config_source(show)
    _add_run_options(show, include_output=False)
    show.add_argument("--output-dir", help="Write complete TSV/JSON manifests here")
    show.add_argument("--show-first", type=int, default=10)

    score = subparsers.add_parser("score-existing", help="Apply a declared score to an existing model table")
    score.add_argument("--models", required=True)
    score.add_argument("--config")
    score.add_argument("--scoring-profile", choices=["legacy_dimple", "custom"], default="legacy_dimple")
    score.add_argument("--fit-include-noise", action="store_true")
    score.add_argument("--output", required=True)

    summarize = subparsers.add_parser("summarize-models", help="Create family and Pareto summaries")
    summarize.add_argument("--models", required=True)
    summarize.add_argument("--output-dir", required=True)
    summarize.add_argument("--top-n-models", type=int, default=20)

    reproduce = subparsers.add_parser("reproduce-model", help="Re-run a retained model artifact")
    reproduce.add_argument("--model-json", required=True, help="best_model.json or top-model summary.json")
    reproduce.add_argument("--input", dest="input_path")
    reproduce.add_argument("--output-dir", required=True)
    reproduce.add_argument("--n-jobs", type=int)

    explain = subparsers.add_parser(
        "explain", aliases=["interpret"],
        help="Explain retained labels in the original input space without refitting",
    )
    source = explain.add_mutually_exclusive_group(required=True)
    source.add_argument("--model-json", help="Native top-model summary.json")
    source.add_argument("--legacy-table", help="Legacy label/UMAP table (CSV/TSV/XLSX)")
    explain.add_argument("--input", dest="input_path", help="Original matrix; optional native path override")
    explain.add_argument("--outdir", "--output-dir", dest="output_dir")
    explain.add_argument("--config", help="Optional Freeze 3 YAML providing interpretation defaults")
    explain.add_argument("--input-sep")
    explain.add_argument("--input-sheet", default=0)
    explain.add_argument("--legacy-sheet", default=0)
    explain.add_argument(
        "--matrix-orientation",
        choices=["auto", "variants_by_vectors", "vectors_by_variants"], default="auto",
    )
    explain.add_argument("--vector-id-source", default="auto")
    explain.add_argument("--drop-first-n-cols", type=int)
    explain.add_argument("--zscore-transform", choices=["none", "rint"])
    explain.add_argument("--id-column")
    explain.add_argument("--label-column")
    explain.add_argument("--coordinate-columns", help="Comma-separated supplied UMAP columns")
    explain.add_argument("--similarity-metric", choices=["pearson", "spearman"])
    explain.add_argument(
        "--order", choices=["cluster_then_hclust", "cluster", "hclust", "input"]
    )
    explain.add_argument("--noise-policy", choices=["separate_last", "include", "exclude"])
    explain.add_argument("--undefined-correlation", choices=["error", "zero"])
    explain.add_argument("--require-complete-match", dest="require_complete_match", action="store_true", default=None)
    explain.add_argument("--allow-incomplete-match", dest="require_complete_match", action="store_false")
    explain.add_argument("--max-full-heatmap", type=int)
    explain.add_argument("--write-similarity", dest="write_similarity", action="store_true", default=None)
    explain.add_argument("--no-write-similarity", dest="write_similarity", action="store_false")
    explain.add_argument("--force-large-matrix", action="store_true", default=None)
    explain.add_argument("--coordinate-associations", action="store_true", default=None)
    explain.add_argument("--coordinate-methods")
    explain.add_argument("--top-n-associations", type=int)

    compare = subparsers.add_parser("compare", help="Compare two retained clustering artifacts by exact IDs")
    compare.add_argument("--left", required=True, help="Left summary JSON or label table")
    compare.add_argument("--right", required=True, help="Right summary JSON or label table")
    compare.add_argument("--output-dir", required=True)
    compare.add_argument("--id-column", default="feature_id")
    compare.add_argument("--label-column", default="label")
    compare.add_argument("--require-same-order", action="store_true")

    validate = subparsers.add_parser("validate", help="Validate run schemas, artifacts, and recorded hashes")
    validate.add_argument("--run-dir", required=True)
    validate.add_argument("--output-dir")
    return parser


def _inspect(args: argparse.Namespace) -> int:
    import yaml

    config = _resolved(args)
    rendered = yaml.safe_dump(config, sort_keys=False)
    if args.output:
        destination = Path(args.output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    print(json.dumps(count_candidates(config), indent=2))
    return 0


def _show(args: argparse.Namespace) -> int:
    config = _resolved(args)
    candidates = enumerate_candidates(config)
    print(json.dumps(count_candidates(config), indent=2))
    for candidate in candidates[:max(0, int(args.show_first))]:
        print(json.dumps(json_safe(flatten_candidate(candidate)), sort_keys=True))
    if args.output_dir:
        write_search_space(candidates, config, args.output_dir)
    return 0


def _score(args: argparse.Namespace) -> int:
    config = resolve_config("custom", args.config, {
        "scoring.profile": args.scoring_profile,
        "scoring.fit_include_noise": bool(args.fit_include_noise),
    }) if args.config else resolve_config("standard", None, {
        "scoring.profile": args.scoring_profile,
        "scoring.fit_include_noise": bool(args.fit_include_noise),
    })
    models, schema_migration = normalize_model_table_schema(read_model_table(args.models))
    scored, manifest = apply_scoring(models, config["scoring"])
    manifest["input_schema"] = schema_migration
    ranked = rank_models(scored)
    destination = Path(args.output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    ranked.to_csv(destination, sep="\t", index=False)
    atomic_json_dump(json_safe(manifest), destination.with_suffix(destination.suffix + ".manifest.json"))
    return 0


def _summarize(args: argparse.Namespace) -> int:
    root = Path(args.output_dir)
    root.mkdir(parents=True, exist_ok=True)
    models = read_model_table(args.models)
    if "rank" not in models or models["rank"].isna().all():
        models = rank_models(models)
    family_summaries(models).to_csv(root / "family_summaries.tsv", sep="\t", index=False)
    pareto_front(models).to_csv(root / "pareto_front.tsv", sep="\t", index=False)
    top_models(models, args.top_n_models).to_csv(root / "top_models.tsv", sep="\t", index=False)
    atomic_json_dump({
        "candidate_models": int(len(models)),
        "successful_models": int(models["status"].eq("success").sum()),
        "failed_models": int(models["status"].eq("failed").sum()),
    }, root / "summary.json")
    return 0


def _reproduce(args: argparse.Namespace) -> int:
    source = Path(args.model_json)
    payload = json.loads(source.read_text(encoding="utf-8"))
    if not payload.get("parameters"):
        raise ValueError("Model JSON does not contain a parameters mapping")
    config = payload.get("resolved_run_config") or {}
    if not config:
        config = resolve_config("fixed")
    config["search_mode"] = "fixed"
    config["umap"] = payload["parameters"]["umap"]
    config["hdbscan"] = payload["parameters"]["hdbscan"]
    config["execution"] = dict(config.get("execution", {}))
    config["execution"]["top_n_models"] = 1
    if args.input_path:
        config.setdefault("input", {})["path"] = args.input_path
    if args.n_jobs is not None:
        config["execution"]["n_jobs"] = args.n_jobs
    validate_config(config)
    run_search(config, args.output_dir, command=sys.argv)
    return 0


def _explain(args: argparse.Namespace) -> int:
    from .interpretation import run_explanation

    config = resolve_config("standard", args.config) if args.config else resolve_config("standard")
    interpretation = dict(config["interpretation"])
    for attribute, key in {
        "similarity_metric": "similarity_metric",
        "order": "order",
        "noise_policy": "noise_policy",
        "undefined_correlation": "undefined_correlation",
        "require_complete_match": "require_complete_match",
        "max_full_heatmap": "max_full_heatmap",
        "write_similarity": "write_similarity",
        "force_large_matrix": "force_large_matrix",
        "coordinate_associations": "coordinate_associations",
        "coordinate_methods": "coordinate_methods",
        "top_n_associations": "top_n_associations",
    }.items():
        value = getattr(args, attribute)
        if value is not None:
            interpretation[key] = value
    if isinstance(interpretation.get("coordinate_methods"), str):
        interpretation["coordinate_methods"] = [
            part.strip() for part in interpretation["coordinate_methods"].split(",") if part.strip()
        ]
    config["interpretation"] = interpretation
    validate_config(config)
    output_dir = args.output_dir
    if not output_dir:
        if not args.model_json:
            raise ValueError("Legacy explanation requires --outdir")
        output_dir = str(Path(args.model_json).parent / "interpretation")
    run_explanation(
        output_dir=output_dir,
        interpretation_config=interpretation,
        model_json=args.model_json,
        legacy_table=args.legacy_table,
        input_path=args.input_path,
        input_sep=args.input_sep,
        input_sheet=args.input_sheet,
        legacy_sheet=args.legacy_sheet,
        matrix_orientation=args.matrix_orientation,
        vector_id_source=args.vector_id_source,
        drop_first_n_cols=args.drop_first_n_cols,
        zscore_transform=args.zscore_transform,
        id_column=args.id_column,
        label_column=args.label_column,
        coordinate_columns=args.coordinate_columns,
        command=["dimple-gwas", *(sys.argv[1:])],
    )
    return 0


def _compare(args: argparse.Namespace) -> int:
    from .comparison import run_comparison

    run_comparison(
        args.left,
        args.right,
        args.output_dir,
        id_column=args.id_column,
        label_column=args.label_column,
        require_same_order=args.require_same_order,
        command=["dimple-gwas", *(sys.argv[1:])],
    )
    return 0


def _validate(args: argparse.Namespace) -> int:
    from .validation import run_validation

    report = run_validation(
        args.run_dir,
        args.output_dir,
        command=["dimple-gwas", *(sys.argv[1:])],
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "pass" else 1


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "run":
            config = _resolved(args)
            run_search(config, args.output_dir, command=[parser.prog, *(argv or sys.argv[1:])])
            return 0
        if args.command == "inspect-config":
            return _inspect(args)
        if args.command == "show-search-space":
            return _show(args)
        if args.command == "score-existing":
            return _score(args)
        if args.command == "summarize-models":
            return _summarize(args)
        if args.command == "reproduce-model":
            return _reproduce(args)
        if args.command in {"explain", "interpret"}:
            return _explain(args)
        if args.command == "compare":
            return _compare(args)
        if args.command == "validate":
            return _validate(args)
    except (ValueError, FileNotFoundError, RuntimeError) as exc:
        parser.error(str(exc))
    return 2
