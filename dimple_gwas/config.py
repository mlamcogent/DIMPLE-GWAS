"""Configuration loading, precedence, normalization, and validation."""

from __future__ import annotations

import copy
import json
import math
from pathlib import Path
from typing import Any, Mapping


UMAP_KEYS = (
    "n_neighbors",
    "min_dist",
    "n_components",
    "metric",
    "spread",
    "learning_rate",
    "repulsion_strength",
    "negative_sample_rate",
    "local_connectivity",
    "set_op_mix_ratio",
    "random_state",
    "densmap",
)

HDBSCAN_KEYS = (
    "min_cluster_size",
    "min_samples",
    "cluster_selection_epsilon",
    "cluster_selection_persistence",
    "cluster_selection_method",
    "alpha",
    "allow_single_cluster",
    "max_cluster_size",
    "metric",
)

SUPPORTED_UMAP_METRICS = {
    "euclidean", "manhattan", "cityblock", "l1", "l2", "chebyshev",
    "minkowski", "canberra", "braycurtis", "cosine", "correlation",
    "hamming", "jaccard", "dice", "russellrao", "sokalmichener",
    "sokalsneath", "yule",
}

SUPPORTED_HDBSCAN_METRICS = {
    "euclidean", "manhattan", "cityblock", "l1", "l2", "chebyshev",
    "minkowski", "canberra", "braycurtis", "cosine", "correlation",
    "hamming", "jaccard", "dice", "russellrao", "sokalmichener",
    "sokalsneath", "yule",
}


def _base_config() -> dict[str, Any]:
    return {
        "search_mode": "standard",
        "input": {
            "path": None,
            "drop_first_n_cols": 4,
            "sep": None,
            "zscore_transform": "none",
            "annotation_file": None,
            "annotation_index_col": "index",
        },
        "umap": {
            "n_neighbors": 30,
            "min_dist": 0.0,
            "n_components": 3,
            "metric": "euclidean",
            "spread": 1.0,
            "learning_rate": 1.0,
            "repulsion_strength": 1.0,
            "negative_sample_rate": 5,
            "local_connectivity": 1.0,
            "set_op_mix_ratio": 1.0,
            "random_state": 42,
            "densmap": True,
        },
        "hdbscan": {
            "min_cluster_size": {"start": 5, "stop": 50, "step": 1},
            "min_samples": {"start": 2, "stop": 20, "step": 1},
            "cluster_selection_epsilon": {"start": 0, "stop": 3, "step": 1},
            "cluster_selection_persistence": 0.0,
            "cluster_selection_method": "eom",
            "alpha": 1.0,
            "allow_single_cluster": False,
            "max_cluster_size": 0,
            "metric": "euclidean",
        },
        "execution": {
            "n_random_states": 1000,
            "n_jobs": -1,
            "candidate_jobs": 1,
            "top_n_models": 20,
            "warn_candidate_count": 5000,
            "max_candidate_models": 0,
            "max_samples_trust": 3000,
            "max_samples_silhouette": 0,
            "trust_k": 30,
            "trust_seed": 42,
            "silhouette_seed": 42,
            "legacy_ensemble_seeds": True,
            "write_parquet": True,
            "compute_dbcv": True,
            "strict": False,
        },
        "scoring": {
            "profile": "legacy_dimple",
            "fit_include_noise": False,
            "custom": {},
        },
        "interpretation": {
            "similarity_metric": "pearson",
            "order": "cluster_then_hclust",
            "noise_policy": "separate_last",
            "undefined_correlation": "error",
            "require_complete_match": True,
            "max_full_heatmap": 1200,
            "write_similarity": True,
            "force_large_matrix": False,
            "coordinate_associations": False,
            "coordinate_methods": ["pearson"],
            "top_n_associations": 100,
        },
    }


def builtin_config(mode: str) -> dict[str, Any]:
    mode = str(mode).lower()
    cfg = _base_config()
    cfg["search_mode"] = mode
    if mode == "standard":
        return cfg
    if mode == "extended":
        cfg["umap"].update({
            "n_neighbors": [15, 30, 50],
            "min_dist": [0.0, 0.1],
            "metric": ["euclidean", "cosine"],
        })
        cfg["hdbscan"].update({
            "min_cluster_size": [5, 10, 20],
            "min_samples": [2, 5, 10],
            "cluster_selection_epsilon": [0.0, 0.05],
            "cluster_selection_method": ["eom", "leaf"],
            "max_cluster_size": [0, 100],
            "metric": ["euclidean", "cosine"],
        })
        cfg["execution"].update({"n_random_states": 10, "legacy_ensemble_seeds": False})
        return cfg
    if mode == "fixed":
        cfg["hdbscan"].update({
            "min_cluster_size": 5,
            "min_samples": 5,
            "cluster_selection_epsilon": 0.0,
        })
        cfg["execution"].update({"n_random_states": 1, "legacy_ensemble_seeds": False})
        return cfg
    if mode == "custom":
        cfg["execution"].update({"legacy_ensemble_seeds": False})
        return cfg
    raise ValueError(f"Unknown search mode: {mode!r}")


def deep_merge(base: Mapping[str, Any], overlay: Mapping[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(dict(base))
    for key, value in overlay.items():
        if isinstance(value, Mapping) and isinstance(result.get(key), Mapping):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def load_yaml(path: str | Path) -> dict[str, Any]:
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - exercised in dependency-poor installs
        raise RuntimeError("PyYAML is required to load configuration files") from exc
    config_path = Path(path)
    if not config_path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError("Configuration root must be a YAML mapping")
    return data


def set_dotted(config: dict[str, Any], dotted: str, value: Any) -> None:
    node = config
    parts = dotted.split(".")
    for part in parts[:-1]:
        child = node.get(part)
        if not isinstance(child, dict):
            child = {}
            node[part] = child
        node = child
    node[parts[-1]] = value


def resolve_config(
    mode: str,
    config_path: str | Path | None = None,
    overrides: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    cfg = builtin_config(mode)
    if config_path:
        cfg = deep_merge(cfg, load_yaml(config_path))
    for dotted, value in (overrides or {}).items():
        if value is not None:
            set_dotted(cfg, dotted, value)
    cfg["search_mode"] = mode
    validate_config(cfg)
    return cfg


def _coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, int) and value in (0, 1):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"true", "t", "yes", "y", "1"}:
        return True
    if text in {"false", "f", "no", "n", "0"}:
        return False
    raise ValueError(f"Invalid boolean value: {value!r}")


def _range_values(spec: Mapping[str, Any], cast: type) -> list[Any]:
    if "start" not in spec or "stop" not in spec:
        raise ValueError(f"Range mapping requires start and stop: {spec!r}")
    start = cast(spec["start"])
    stop = cast(spec["stop"])
    step = cast(spec.get("step", 1))
    if step == 0:
        raise ValueError("Range step cannot be zero")
    values: list[Any] = []
    current = start
    if step > 0:
        compare = lambda x: x < stop
    else:
        compare = lambda x: x > stop
    while compare(current):
        values.append(cast(current))
        current = cast(current + step)
        if len(values) > 1_000_000:
            raise ValueError("Range expands beyond one million values")
    if not values:
        raise ValueError(f"Range is empty: {spec!r}")
    return values


def _string_sequence(value: str, cast: type) -> list[Any]:
    values: list[Any] = []
    for token in value.split(","):
        token = token.strip()
        if not token:
            continue
        if ":" in token and cast in (int, float):
            parts = token.split(":")
            if len(parts) not in (2, 3):
                raise ValueError(f"Malformed range: {token!r}")
            spec = {"start": parts[0], "stop": parts[1]}
            if len(parts) == 3:
                spec["step"] = parts[2]
            values.extend(_range_values(spec, cast))
        else:
            values.append(cast(token))
    if not values:
        raise ValueError(f"Empty parameter sequence: {value!r}")
    return values


def as_list(value: Any, cast: type | None = None) -> list[Any]:
    if isinstance(value, Mapping):
        if cast not in (int, float):
            raise ValueError(f"Ranges are only valid for numeric values: {value!r}")
        values = _range_values(value, cast)
    elif isinstance(value, (list, tuple)):
        values = list(value)
    elif isinstance(value, str) and ("," in value or (":" in value and cast in (int, float))):
        if cast is bool:
            values = [token.strip() for token in value.split(",") if token.strip()]
        else:
            values = _string_sequence(value, cast or str)
    else:
        values = [value]
    if cast is bool:
        return [_coerce_bool(item) for item in values]
    if cast is not None:
        return [cast(item) for item in values]
    return values


def normalized_parameter_space(config: Mapping[str, Any]) -> dict[str, dict[str, list[Any]]]:
    umap = dict(config.get("umap", {}))
    hdb = dict(config.get("hdbscan", {}))
    casts: dict[str, type] = {
        "n_neighbors": int,
        "min_dist": float,
        "n_components": int,
        "metric": str,
        "spread": float,
        "learning_rate": float,
        "repulsion_strength": float,
        "negative_sample_rate": int,
        "local_connectivity": float,
        "set_op_mix_ratio": float,
        "random_state": int,
        "densmap": bool,
    }
    hdb_casts: dict[str, type] = {
        "min_cluster_size": int,
        "min_samples": int,
        "cluster_selection_epsilon": float,
        "cluster_selection_persistence": float,
        "cluster_selection_method": str,
        "alpha": float,
        "allow_single_cluster": bool,
        "max_cluster_size": int,
        "metric": str,
    }
    missing_umap = set(UMAP_KEYS) - set(umap)
    missing_hdb = set(HDBSCAN_KEYS) - set(hdb)
    if missing_umap or missing_hdb:
        raise ValueError(
            f"Missing parameters; UMAP={sorted(missing_umap)}, HDBSCAN={sorted(missing_hdb)}"
        )
    return {
        "umap": {key: as_list(umap[key], casts[key]) for key in UMAP_KEYS},
        "hdbscan": {key: as_list(hdb[key], hdb_casts[key]) for key in HDBSCAN_KEYS},
    }


def _finite(values: list[float], name: str) -> None:
    if any(not math.isfinite(float(value)) for value in values):
        raise ValueError(f"{name} contains a non-finite value")


def validate_config(config: Mapping[str, Any]) -> None:
    unknown = set(config) - {
        "search_mode", "input", "umap", "hdbscan", "execution", "scoring",
        "interpretation",
    }
    if unknown:
        raise ValueError(f"Unknown top-level configuration keys: {sorted(unknown)}")
    space = normalized_parameter_space(config)
    u = space["umap"]
    h = space["hdbscan"]
    if config.get("search_mode") == "fixed":
        non_scalar = [
            f"umap.{key}" for key, values in u.items() if len(values) != 1
        ] + [
            f"hdbscan.{key}" for key, values in h.items() if len(values) != 1
        ]
        if non_scalar:
            raise ValueError(f"Fixed mode requires one value per searched parameter: {non_scalar}")

    _finite(u["min_dist"] + u["spread"] + u["learning_rate"] + u["repulsion_strength"] + u["local_connectivity"] + u["set_op_mix_ratio"], "UMAP parameters")
    _finite(h["cluster_selection_epsilon"] + h["cluster_selection_persistence"] + h["alpha"], "HDBSCAN parameters")
    if any(value < 2 for value in u["n_neighbors"]):
        raise ValueError("UMAP n_neighbors must be >= 2")
    if any(value < 1 for value in u["n_components"]):
        raise ValueError("UMAP n_components must be >= 1")
    if any(value < 0 for value in u["min_dist"]):
        raise ValueError("UMAP min_dist must be >= 0")
    if any(value <= 0 for value in u["spread"]):
        raise ValueError("UMAP spread must be > 0")
    if any(md > spread for md in u["min_dist"] for spread in u["spread"]):
        raise ValueError("Every UMAP min_dist must be <= every searched spread")
    if any(value <= 0 for value in u["learning_rate"] + u["repulsion_strength"]):
        raise ValueError("UMAP learning_rate and repulsion_strength must be > 0")
    if any(value < 1 for value in u["negative_sample_rate"]):
        raise ValueError("UMAP negative_sample_rate must be >= 1")
    if any(value < 0 for value in u["local_connectivity"]):
        raise ValueError("UMAP local_connectivity must be >= 0")
    if any(value < 0 or value > 1 for value in u["set_op_mix_ratio"]):
        raise ValueError("UMAP set_op_mix_ratio must be in [0, 1]")
    bad_umap_metrics = set(map(str.lower, u["metric"])) - SUPPORTED_UMAP_METRICS
    if bad_umap_metrics:
        raise ValueError(f"Unsupported UMAP metrics: {sorted(bad_umap_metrics)}")

    if any(value < 2 for value in h["min_cluster_size"]):
        raise ValueError("HDBSCAN min_cluster_size must be >= 2")
    if any(value < 1 for value in h["min_samples"]):
        raise ValueError("HDBSCAN min_samples must be >= 1")
    if any(value < 0 for value in h["cluster_selection_epsilon"] + h["cluster_selection_persistence"]):
        raise ValueError("HDBSCAN epsilon and persistence must be >= 0")
    if any(value <= 0 for value in h["alpha"]):
        raise ValueError("HDBSCAN alpha must be > 0")
    if set(map(str.lower, h["cluster_selection_method"])) - {"eom", "leaf"}:
        raise ValueError("HDBSCAN cluster_selection_method must be eom or leaf")
    if any(value < 0 for value in h["max_cluster_size"]):
        raise ValueError("HDBSCAN max_cluster_size must be 0 (unlimited) or >= min_cluster_size")
    invalid_size_pairs = [
        (maximum, minimum)
        for maximum in h["max_cluster_size"]
        for minimum in h["min_cluster_size"]
        if maximum != 0 and maximum < minimum
    ]
    if invalid_size_pairs:
        raise ValueError(f"max_cluster_size < min_cluster_size in searched combinations: {invalid_size_pairs[:5]}")
    bad_hdb_metrics = set(map(str.lower, h["metric"])) - SUPPORTED_HDBSCAN_METRICS
    if bad_hdb_metrics:
        raise ValueError(f"Unsupported HDBSCAN metrics: {sorted(bad_hdb_metrics)}")

    input_cfg = config.get("input", {})
    if int(input_cfg.get("drop_first_n_cols", 4)) < 0:
        raise ValueError("drop_first_n_cols must be >= 0")
    if input_cfg.get("zscore_transform", "none") not in {"none", "rint"}:
        raise ValueError("zscore_transform must be none or rint")

    execution = config.get("execution", {})
    for key in ("n_random_states", "top_n_models", "trust_k"):
        if int(execution.get(key, 1)) < 1:
            raise ValueError(f"execution.{key} must be >= 1")
    if int(execution.get("candidate_jobs", 1)) == 0:
        raise ValueError("execution.candidate_jobs cannot be zero")
    if int(execution.get("max_samples_trust", 0)) < 0:
        raise ValueError("execution.max_samples_trust must be >= 0")
    if int(execution.get("max_samples_silhouette", 0)) < 0:
        raise ValueError("execution.max_samples_silhouette must be >= 0")

    scoring = config.get("scoring", {})
    profile = scoring.get("profile", "legacy_dimple")
    if profile not in {"legacy_dimple", "custom"}:
        raise ValueError("scoring.profile must be legacy_dimple or custom")
    if profile == "custom":
        custom = scoring.get("custom")
        if not isinstance(custom, Mapping) or not custom:
            raise ValueError("Custom scoring requires a non-empty scoring.custom mapping")
        for metric, rule in custom.items():
            if not isinstance(rule, Mapping):
                raise ValueError(f"Custom scoring rule for {metric!r} must be a mapping")
            weight = float(rule.get("weight", 0))
            direction = rule.get("direction")
            if not math.isfinite(weight) or weight < 0:
                raise ValueError(f"Custom score weight for {metric!r} must be finite and >= 0")
            if direction not in {"maximize", "minimize"}:
                raise ValueError(f"Custom score direction for {metric!r} must be maximize or minimize")
        if sum(float(rule.get("weight", 0)) for rule in custom.values()) <= 0:
            raise ValueError("At least one custom score weight must be > 0")

    interpretation = config.get("interpretation", {})
    allowed_interpretation = {
        "similarity_metric", "order", "noise_policy", "undefined_correlation",
        "require_complete_match", "max_full_heatmap", "write_similarity",
        "force_large_matrix", "coordinate_associations", "coordinate_methods",
        "top_n_associations",
    }
    unknown_interpretation = set(interpretation) - allowed_interpretation
    if unknown_interpretation:
        raise ValueError(
            "Unknown interpretation configuration keys: "
            f"{sorted(unknown_interpretation)}"
        )
    if interpretation.get("similarity_metric", "pearson") not in {"pearson", "spearman"}:
        raise ValueError("interpretation.similarity_metric must be pearson or spearman")
    if interpretation.get("order", "cluster_then_hclust") not in {
        "cluster_then_hclust", "cluster", "hclust", "input",
    }:
        raise ValueError(
            "interpretation.order must be cluster_then_hclust, cluster, hclust, or input"
        )
    if interpretation.get("noise_policy", "separate_last") not in {
        "separate_last", "include", "exclude",
    }:
        raise ValueError(
            "interpretation.noise_policy must be separate_last, include, or exclude"
        )
    if interpretation.get("undefined_correlation", "error") not in {"error", "zero"}:
        raise ValueError("interpretation.undefined_correlation must be error or zero")
    if int(interpretation.get("max_full_heatmap", 1200)) < 1:
        raise ValueError("interpretation.max_full_heatmap must be >= 1")
    if int(interpretation.get("top_n_associations", 100)) < 1:
        raise ValueError("interpretation.top_n_associations must be >= 1")
    methods = interpretation.get("coordinate_methods", ["pearson"])
    if isinstance(methods, str):
        methods = [part.strip() for part in methods.split(",") if part.strip()]
    if not methods or set(methods) - {"pearson", "spearman"}:
        raise ValueError(
            "interpretation.coordinate_methods must contain pearson and/or spearman"
        )


def config_as_json(config: Mapping[str, Any]) -> str:
    return json.dumps(config, indent=2, sort_keys=True, default=str)
