from __future__ import annotations

import pytest

from dimple_gwas.config import as_list, normalized_parameter_space, resolve_config
from dimple_gwas.search_space import count_candidates


def test_scalar_list_and_range_handling():
    assert as_list(5, int) == [5]
    assert as_list([2, 4], int) == [2, 4]
    assert as_list("2:6:2", int) == [2, 4]
    assert as_list({"start": 0.0, "stop": 0.3, "step": 0.1}, float) == pytest.approx([0.0, 0.1, 0.2])
    assert as_list("false,true", bool) == [False, True]


def test_cli_override_precedence(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text("umap:\n  n_neighbors: 17\nexecution:\n  top_n_models: 7\n", encoding="utf-8")
    config = resolve_config("custom", config_file, {"umap.n_neighbors": "9,11"})
    assert normalized_parameter_space(config)["umap"]["n_neighbors"] == [9, 11]
    assert config["execution"]["top_n_models"] == 7


def test_standard_defaults_match_dev_declarations():
    config = resolve_config("standard")
    assert config["umap"]["n_neighbors"] == 30
    assert config["umap"]["min_dist"] == 0.0
    assert config["umap"]["n_components"] == 3
    assert config["umap"]["densmap"] is True
    assert config["execution"]["n_random_states"] == 1000
    assert count_candidates(config)["candidate_models"] == 3 * 18 * 45


@pytest.mark.parametrize("overrides,match", [
    ({"hdbscan.max_cluster_size": 4, "hdbscan.min_cluster_size": 5}, "max_cluster_size"),
    ({"umap.metric": "not-a-metric"}, "Unsupported UMAP"),
    ({"umap.min_dist": 2.0, "umap.spread": 1.0}, "min_dist"),
    ({"hdbscan.cluster_selection_method": "ward"}, "eom or leaf"),
])
def test_invalid_combinations_rejected(overrides, match):
    with pytest.raises(ValueError, match=match):
        resolve_config("fixed", overrides=overrides)


def test_fixed_mode_rejects_lists():
    with pytest.raises(ValueError, match="Fixed mode requires"):
        resolve_config("fixed", overrides={"hdbscan.min_samples": [2, 3]})
