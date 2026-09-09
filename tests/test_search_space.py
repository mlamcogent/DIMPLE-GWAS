from __future__ import annotations

from dimple_gwas.config import resolve_config
from dimple_gwas.search_space import enumerate_candidates


def test_search_enumeration_and_stable_ids():
    config = resolve_config("custom", overrides={
        "umap.metric": ["euclidean", "cosine"],
        "hdbscan.min_cluster_size": [5, 10],
        "hdbscan.min_samples": 2,
        "hdbscan.cluster_selection_epsilon": 0.0,
        "hdbscan.cluster_selection_method": ["eom", "leaf"],
        "hdbscan.max_cluster_size": [0, 20],
    })
    first = enumerate_candidates(config)
    second = enumerate_candidates(config)
    assert len(first) == 16
    assert [item["model_id"] for item in first] == [item["model_id"] for item in second]
    assert len({item["model_id"] for item in first}) == 16
    assert {item["hdbscan"]["cluster_selection_method"] for item in first} == {"eom", "leaf"}


def test_search_limit_never_silently_samples():
    config = resolve_config("custom", overrides={
        "hdbscan.min_cluster_size": [5, 10],
        "execution.max_candidate_models": 1,
    })
    try:
        enumerate_candidates(config)
    except ValueError as exc:
        assert "never silently samples" in str(exc)
    else:
        raise AssertionError("expected complete-grid limit rejection")

