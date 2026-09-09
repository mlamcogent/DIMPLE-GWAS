"""Repeated UMAP execution."""

from __future__ import annotations

import time
from typing import Any, Mapping


def _fit_one(matrix, parameters: Mapping[str, Any], seed: int):
    try:
        import umap.umap_ as umap
    except ImportError:  # pragma: no cover - fallback depends on installation
        import umap

    reducer = umap.UMAP(
        n_neighbors=int(parameters["n_neighbors"]),
        min_dist=float(parameters["min_dist"]),
        n_components=int(parameters["n_components"]),
        metric=str(parameters["metric"]),
        spread=float(parameters["spread"]),
        learning_rate=float(parameters["learning_rate"]),
        repulsion_strength=float(parameters["repulsion_strength"]),
        negative_sample_rate=int(parameters["negative_sample_rate"]),
        local_connectivity=float(parameters["local_connectivity"]),
        set_op_mix_ratio=float(parameters["set_op_mix_ratio"]),
        random_state=int(seed),
        densmap=bool(parameters["densmap"]),
    )
    return reducer.fit_transform(matrix).astype("float32", copy=False)


def ensemble_seeds(parameters: Mapping[str, Any], repeats: int, legacy_sequence: bool) -> list[int]:
    if legacy_sequence:
        return list(range(1, repeats + 1))
    start = int(parameters["random_state"])
    return list(range(start, start + repeats))


def run_repeated_umap(
    matrix,
    parameters: Mapping[str, Any],
    repeats: int,
    n_jobs: int,
    legacy_sequence: bool,
) -> dict[str, Any]:
    import numpy as np
    from joblib import Parallel, delayed

    if repeats < 1:
        raise ValueError("n_random_states must be >= 1")
    seeds = ensemble_seeds(parameters, repeats, legacy_sequence)
    started = time.perf_counter()
    values = matrix.values if hasattr(matrix, "values") else matrix
    if n_jobs == 1 or repeats == 1:
        embeddings = [_fit_one(values, parameters, seed) for seed in seeds]
    else:
        embeddings = Parallel(n_jobs=n_jobs)(
            delayed(_fit_one)(values, parameters, seed) for seed in seeds
        )
    rows, components = embeddings[0].shape
    consolidated = np.empty((rows, components * len(embeddings)), dtype=np.float32)
    for index, embedding in enumerate(embeddings):
        consolidated[:, index * components:(index + 1) * components] = embedding
    visualization = embeddings[0].copy()
    return {
        "embedding": consolidated,
        "visualization_embedding": visualization,
        "seeds": seeds,
        "runtime_seconds": time.perf_counter() - started,
    }

