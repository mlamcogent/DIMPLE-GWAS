from __future__ import annotations

import inspect

import numpy as np
import pandas as pd

from dimple_gwas.metrics import effective_neighbor_count, embedding_quality_metrics
from dimple_gwas.preprocessing import prepare_analysis_matrix, rank_inverse_normal_transform
import dimple_gwas.metrics as metrics_module


def test_rint_and_numeric_matrix():
    frame = pd.DataFrame({"meta": [1, 2, 3, 4], "a": [1, 2, 3, 4], "b": [4, 3, 2, 1]})
    matrix = prepare_analysis_matrix(frame, {"drop_first_n_cols": 1, "zscore_transform": "rint"})
    assert matrix.shape == (2, 4)
    assert np.allclose(matrix.loc["a"], -matrix.loc["b"])
    assert np.isfinite(rank_inverse_normal_transform(frame[["a", "b"]])).all().all()


def test_optimized_trustworthiness_and_continuity():
    rng = np.random.default_rng(1)
    original = rng.normal(size=(30, 6))
    embedded = original[:, :3]
    result = embedding_quality_metrics(original, embedded, requested_k=30, max_samples=20, seed=42)
    assert result["trust_sampled"] is True
    assert result["trust_k_used"] < result["trust_sample_size"] / 2
    assert 0 <= result["trustworthiness"] <= 1
    assert 0 <= result["continuity"] <= 1
    source = inspect.getsource(metrics_module)
    assert "NearestNeighbors" not in source
    assert "np.zeros((n_samples, n_samples))" not in source


def test_effective_neighbor_edge_cases():
    assert effective_neighbor_count(2, 30) == 0
    assert effective_neighbor_count(5, 30) == 2

