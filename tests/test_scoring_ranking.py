from __future__ import annotations

import numpy as np
import pandas as pd

from dimple_gwas.ranking import pareto_front, rank_models, top_models
from dimple_gwas.scoring import custom_score, legacy_dimple_score


def _models():
    return pd.DataFrame({
        "candidate_ordinal": [1, 2, 3, 4],
        "model_id": ["m1", "m2", "m3", "m4"],
        "status": ["success", "success", "success", "failed"],
        "silhouette": [0.2, 0.5, 0.4, np.nan],
        "number_of_clusters": [3, 2, 5, np.nan],
        "number_of_noise_points": [1, 3, 2, np.nan],
        "noise_fraction": [0.1, 0.3, 0.2, np.nan],
        "largest_cluster_fraction": [0.5, 0.4, 0.3, np.nan],
        "hdbscan_persistence_mean": [0.4, 0.7, 0.5, np.nan],
    })


def test_legacy_formula_matches_literal_reference():
    frame = _models()
    scored, manifest = legacy_dimple_score(frame, fit_include_noise=True)
    eligible = frame.iloc[:3]
    sil_norm = eligible["silhouette"] / eligible["silhouette"].max()
    clu_norm = eligible["number_of_clusters"] / eligible["number_of_clusters"].max()
    noise_norm = eligible["number_of_noise_points"] / eligible["number_of_noise_points"].max()
    ranges = np.array([
        eligible["silhouette"].max() - eligible["silhouette"].min(),
        eligible["number_of_clusters"].max() - eligible["number_of_clusters"].min(),
        eligible["number_of_noise_points"].max() - eligible["number_of_noise_points"].min(),
    ])
    weights = ranges / ranges.sum()
    raw = weights[0] * sil_norm + weights[1] * clu_norm - weights[2] * noise_norm
    expected = (raw - raw.min()) / (raw.max() - raw.min())
    assert np.allclose(scored.loc[:2, "Score_raw"], raw)
    assert np.allclose(scored.loc[:2, "Score"], expected)
    assert manifest["weights"]["number_of_noise_points"] > 0


def test_zero_variance_and_noise_exclusion():
    frame = _models().iloc[:1]
    scored, manifest = legacy_dimple_score(frame, fit_include_noise=False)
    assert scored.iloc[0]["score"] == 1.0
    assert manifest["weights"]["number_of_noise_points"] == 0.0


def test_custom_scoring_ranking_top_n_and_pareto():
    scored, _ = custom_score(_models(), {
        "silhouette": {"weight": 0.5, "direction": "maximize"},
        "noise_fraction": {"weight": 0.5, "direction": "minimize"},
    })
    ranked = rank_models(scored)
    assert ranked["rank"].notna().sum() == 3
    assert len(top_models(ranked, 2)) == 2
    assert set(pareto_front(ranked)["model_id"]).issubset({"m1", "m2", "m3"})

