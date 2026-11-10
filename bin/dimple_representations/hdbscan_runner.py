"""Contrib-HDBSCAN construction and candidate fitting."""

from __future__ import annotations

import time
from typing import Any, Mapping


GENERIC_METRICS = {
    "cosine", "correlation", "braycurtis", "canberra", "dice", "hamming",
    "jaccard", "russellrao", "sokalmichener", "sokalsneath", "yule",
}


def estimator_kwargs(parameters: Mapping[str, Any], core_dist_n_jobs: int = 1) -> dict[str, Any]:
    metric = str(parameters["metric"]).lower()
    kwargs = {
        "min_cluster_size": int(parameters["min_cluster_size"]),
        "min_samples": int(parameters["min_samples"]),
        "cluster_selection_epsilon": float(parameters["cluster_selection_epsilon"]),
        "cluster_selection_persistence": float(parameters["cluster_selection_persistence"]),
        "cluster_selection_method": str(parameters["cluster_selection_method"]),
        "alpha": float(parameters["alpha"]),
        "allow_single_cluster": bool(parameters["allow_single_cluster"]),
        "max_cluster_size": int(parameters["max_cluster_size"]),
        "metric": metric,
        "core_dist_n_jobs": int(core_dist_n_jobs),
    }
    if metric in GENERIC_METRICS:
        kwargs["algorithm"] = "generic"
    return kwargs


def fit_hdbscan(embedding, parameters: Mapping[str, Any], core_dist_n_jobs: int = 1) -> dict[str, Any]:
    import hdbscan

    started = time.perf_counter()
    clusterer = hdbscan.HDBSCAN(**estimator_kwargs(parameters, core_dist_n_jobs=core_dist_n_jobs))
    labels = clusterer.fit_predict(embedding)
    return {
        "clusterer": clusterer,
        "labels": labels,
        "runtime_seconds": time.perf_counter() - started,
    }

