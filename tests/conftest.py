from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def synthetic_matrix(tmp_path):
    rng = np.random.default_rng(20260722)
    variants = 80
    x = np.linspace(0, 4 * np.pi, variants)
    templates = [
        np.sin(x),
        np.cos(x),
        np.where(np.arange(variants) < variants // 2, -1.0, 1.0),
    ]
    data = {
        "CHR": np.ones(variants, dtype=int),
        "BP": np.arange(variants),
        "A1": ["A"] * variants,
        "A2": ["G"] * variants,
    }
    for group, template in enumerate(templates):
        for member in range(8):
            data[f"trait_g{group}_{member}"] = template + rng.normal(0, 0.06, variants)
    path = tmp_path / "synthetic.tsv"
    pd.DataFrame(data).to_csv(path, sep="\t", index=False)
    return path


@pytest.fixture
def small_run_config(synthetic_matrix):
    from dimple_gwas.config import resolve_config

    return resolve_config("custom", overrides={
        "input.path": str(synthetic_matrix),
        "umap.n_neighbors": 5,
        "umap.min_dist": 0.0,
        "umap.n_components": 2,
        "umap.densmap": False,
        "hdbscan.min_cluster_size": 3,
        "hdbscan.min_samples": 2,
        "hdbscan.cluster_selection_epsilon": 0.0,
        "hdbscan.cluster_selection_method": "eom,leaf",
        "hdbscan.max_cluster_size": "0,10",
        "execution.n_random_states": 1,
        "execution.n_jobs": 1,
        "execution.top_n_models": 2,
        "execution.max_samples_trust": 100,
        "execution.trust_k": 3,
        "execution.compute_dbcv": False,
        "execution.write_parquet": False,
    })

