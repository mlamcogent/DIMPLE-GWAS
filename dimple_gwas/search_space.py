"""Deterministic search-space enumeration and stable model identities."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import warnings
from collections.abc import Iterable, Mapping
from typing import Any

from .config import HDBSCAN_KEYS, UMAP_KEYS, normalized_parameter_space


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, default=str)


def stable_identifier(prefix: str, value: Any, length: int = 16) -> str:
    digest = hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()[:length]
    return f"{prefix}_{digest}"


def count_candidates(config: Mapping[str, Any]) -> dict[str, int]:
    space = normalized_parameter_space(config)
    umap_count = math.prod(len(space["umap"][key]) for key in UMAP_KEYS)
    hdbscan_count = math.prod(len(space["hdbscan"][key]) for key in HDBSCAN_KEYS)
    return {
        "umap_configurations": int(umap_count),
        "hdbscan_configurations": int(hdbscan_count),
        "candidate_models": int(umap_count * hdbscan_count),
    }


def _dict_product(space: Mapping[str, list[Any]], keys: Iterable[str]):
    ordered_keys = tuple(keys)
    for values in itertools.product(*(space[key] for key in ordered_keys)):
        yield dict(zip(ordered_keys, values))


def model_family(umap_params: Mapping[str, Any], hdbscan_params: Mapping[str, Any]) -> str:
    maximum = int(hdbscan_params["max_cluster_size"])
    maximum_text = "unlimited" if maximum == 0 else str(maximum)
    return "|".join((
        f"umap={umap_params['metric']}",
        f"hdbscan={hdbscan_params['metric']}",
        f"method={hdbscan_params['cluster_selection_method']}",
        f"max_cluster={maximum_text}",
    ))


def enumerate_candidates(config: Mapping[str, Any]) -> list[dict[str, Any]]:
    counts = count_candidates(config)
    execution = config.get("execution", {})
    warning_threshold = int(execution.get("warn_candidate_count", 5000))
    hard_limit = int(execution.get("max_candidate_models", 0))
    total = counts["candidate_models"]
    if warning_threshold > 0 and total > warning_threshold:
        warnings.warn(
            f"Search expands to {total:,} candidate models; this may require substantial compute.",
            RuntimeWarning,
            stacklevel=2,
        )
    if hard_limit > 0 and total > hard_limit:
        raise ValueError(
            f"Search expands to {total:,} candidates, above max_candidate_models={hard_limit:,}. "
            "Narrow the search or explicitly raise the limit; Freeze 2 never silently samples the grid."
        )

    space = normalized_parameter_space(config)
    umap_configs = []
    for params in _dict_product(space["umap"], UMAP_KEYS):
        params["metric"] = str(params["metric"]).lower()
        umap_configs.append({"umap_id": stable_identifier("umap", params), "parameters": params})

    hdbscan_configs = []
    for params in _dict_product(space["hdbscan"], HDBSCAN_KEYS):
        params["metric"] = str(params["metric"]).lower()
        params["cluster_selection_method"] = str(params["cluster_selection_method"]).lower()
        hdbscan_configs.append({"hdbscan_id": stable_identifier("hdb", params), "parameters": params})

    candidates: list[dict[str, Any]] = []
    ordinal = 0
    for umap_item, hdb_item in itertools.product(umap_configs, hdbscan_configs):
        ordinal += 1
        identity = {
            "umap": umap_item["parameters"],
            "hdbscan": hdb_item["parameters"],
        }
        candidates.append({
            "candidate_ordinal": ordinal,
            "model_id": stable_identifier("model", identity),
            "model_family": model_family(identity["umap"], identity["hdbscan"]),
            "umap_id": umap_item["umap_id"],
            "hdbscan_id": hdb_item["hdbscan_id"],
            "umap": dict(identity["umap"]),
            "hdbscan": dict(identity["hdbscan"]),
        })
    return candidates


def flatten_candidate(candidate: Mapping[str, Any]) -> dict[str, Any]:
    row = {
        "candidate_ordinal": candidate["candidate_ordinal"],
        "model_id": candidate["model_id"],
        "model_family": candidate["model_family"],
        "umap_id": candidate["umap_id"],
        "hdbscan_id": candidate["hdbscan_id"],
    }
    row.update({f"umap_{key}": value for key, value in candidate["umap"].items()})
    row.update({f"hdbscan_{key}": value for key, value in candidate["hdbscan"].items()})
    return row

