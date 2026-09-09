from __future__ import annotations

import json

import pandas as pd

from dimple_gwas.pipeline import run_search


def test_custom_leaf_eom_metric_and_max_size_run(tmp_path, small_run_config):
    output = tmp_path / "run"
    result = run_search(small_run_config, output, command=["pytest", "integration"])
    all_models = pd.read_csv(output / "models" / "all_models.tsv", sep="\t")
    assert len(all_models) == 4
    assert set(all_models["hdbscan_cluster_selection_method"]) == {"eom", "leaf"}
    assert set(all_models["hdbscan_max_cluster_size"]) == {0, 10}
    assert (output / "search_space_manifest.json").is_file()
    assert (output / "models" / "ranked_models.tsv").is_file()
    assert (output / "models" / "pareto_front.tsv").is_file()
    assert (output / "models" / "family_summaries.tsv").is_file()
    assert (output / "logs" / "model_failures.tsv").is_file()
    manifest = json.loads((output / "run_manifest.json").read_text())
    assert manifest["search_space_size"] == 4
    assert len(result["ranked"]) == 4


def test_fixed_model_reproduction(tmp_path, small_run_config):
    small_run_config["search_mode"] = "fixed"
    small_run_config["hdbscan"]["cluster_selection_method"] = "eom"
    small_run_config["hdbscan"]["max_cluster_size"] = 0
    small_run_config["execution"]["top_n_models"] = 1
    output = tmp_path / "fixed"
    run_search(small_run_config, output, command=["pytest", "fixed"])
    best = json.loads((output / "models" / "best_model.json").read_text())
    assert best["parameters"]["hdbscan"]["cluster_selection_method"] == "eom"
    artifact_dirs = list((output / "models" / "top_model_artifacts").glob("model_*"))
    assert artifact_dirs
    assert (artifact_dirs[0] / "reproduce.yaml").is_file()
    assert (artifact_dirs[0] / "labels.tsv").is_file()

