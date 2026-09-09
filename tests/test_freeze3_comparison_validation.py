from __future__ import annotations

import json

import pandas as pd
import pytest
import yaml

from dimple_gwas.cli import build_parser, main
from dimple_gwas.comparison import run_comparison
from dimple_gwas.config import resolve_config
from dimple_gwas.io import atomic_json_dump
from dimple_gwas.provenance import file_record, package_source_digest, sha256_file
from dimple_gwas.scoring import normalize_model_table_schema
from dimple_gwas.validation import run_validation


def _label_tables(tmp_path):
    left = pd.DataFrame({
        "feature_id": ["a", "b", "c", "d"],
        "label": [0, 0, 1, -1],
        "UMAP_1": [0.0, 0.1, 2.0, 3.0],
        "UMAP_2": [0.0, 0.2, 2.1, 3.1],
    })
    right = pd.DataFrame({
        "feature_id": ["d", "c", "b", "a"],
        "label": [-1, 9, 5, 5],
        "UMAP_1": [3.0, 2.0, 0.1, 0.0],
        "UMAP_2": [3.1, 2.1, 0.2, 0.0],
    })
    left_path = tmp_path / "left.tsv"
    right_path = tmp_path / "right.tsv"
    left.to_csv(left_path, sep="\t", index=False)
    right.to_csv(right_path, sep="\t", index=False)
    return left_path, right_path


def test_label_permutation_comparison_is_structurally_equal(tmp_path):
    left, right = _label_tables(tmp_path)
    summary = run_comparison(left, right, tmp_path / "comparison")
    assert summary["adjusted_rand_index"] == pytest.approx(1.0)
    assert summary["normalized_mutual_information"] == pytest.approx(1.0)
    assert summary["variation_of_information_nats"] == pytest.approx(0.0)
    assert summary["noise_set_jaccard"] == pytest.approx(1.0)
    assert summary["mapped_membership_match_fraction"] == pytest.approx(1.0)


def test_comparison_requires_identical_id_sets(tmp_path):
    left, right = _label_tables(tmp_path)
    frame = pd.read_csv(right, sep="\t").iloc[:-1]
    frame.to_csv(right, sep="\t", index=False)
    with pytest.raises(ValueError, match="identical ID sets"):
        run_comparison(left, right, tmp_path / "comparison")


def test_comparison_rejects_duplicate_ids(tmp_path):
    left, right = _label_tables(tmp_path)
    frame = pd.read_csv(right, sep="\t")
    frame.loc[1, "feature_id"] = frame.loc[0, "feature_id"]
    frame.to_csv(right, sep="\t", index=False)
    with pytest.raises(ValueError, match="duplicate"):
        run_comparison(left, right, tmp_path / "comparison")


def _minimal_valid_run(tmp_path):
    root = tmp_path / "run"
    model_id = "model_abc"
    artifact = root / "models/top_model_artifacts" / model_id
    artifact.mkdir(parents=True)
    config = resolve_config("fixed")
    (root / "resolved_config.yaml").write_text(
        yaml.safe_dump(config, sort_keys=False), encoding="utf-8"
    )
    search = pd.DataFrame({"model_id": [model_id], "umap_id": ["u"], "hdbscan_id": ["h"]})
    search.to_csv(root / "search_space_manifest.tsv", sep="\t", index=False)
    atomic_json_dump({"candidate_models": 1}, root / "search_space_manifest.json")
    ranked = pd.DataFrame({
        "model_id": [model_id], "status": ["success"], "rank": [1], "score": [1.0]
    })
    ranked.to_csv(root / "models/all_models.tsv", sep="\t", index=False)
    ranked.to_csv(root / "models/ranked_models.tsv", sep="\t", index=False)
    ranked.to_csv(root / "models/top_models.tsv", sep="\t", index=False)
    atomic_json_dump({"selected_model": model_id}, root / "models/model_selection_manifest.json")
    labels = pd.DataFrame({"feature_id": ["a", "b"], "label": [0, 1]})
    labels.to_csv(artifact / "labels.tsv", sep="\t", index=False)
    atomic_json_dump({
        "artifact_schema": "dimple-gwas.model-summary.v3",
        "model": {"model_id": model_id},
        "labels_file": "labels.tsv",
        "labels_sha256": sha256_file(artifact / "labels.tsv"),
    }, artifact / "summary.json")
    artifacts = {
        "all_models": file_record(root / "models/all_models.tsv"),
        "ranked_models": file_record(root / "models/ranked_models.tsv"),
        "top_models": file_record(root / "models/top_models.tsv"),
    }
    atomic_json_dump({
        "manifest_schema": "dimple-gwas.provenance.v3",
        "status": "complete", "selected_model": model_id, "artifacts": artifacts,
    }, root / "run_manifest.json")
    return root


def test_validation_passes_complete_contract(tmp_path):
    root = _minimal_valid_run(tmp_path)
    report = run_validation(root, tmp_path / "validation")
    assert report["status"] == "pass"
    assert report["failures"] == 0
    assert (tmp_path / "validation/validation_checks.tsv").is_file()


def test_validation_detects_hash_mismatch(tmp_path):
    root = _minimal_valid_run(tmp_path)
    (root / "models/ranked_models.tsv").write_text("changed\n", encoding="utf-8")
    report = run_validation(root, tmp_path / "validation")
    assert report["status"] == "fail"
    checks = pd.read_csv(tmp_path / "validation/validation_checks.tsv", sep="\t")
    assert (checks["detail"] == "SHA-256 mismatch").any()


def test_package_source_digest_is_stable():
    first = package_source_digest()
    second = package_source_digest()
    assert len(first) == 64
    assert first == second


def test_historical_notebook_model_schema_is_adapted():
    source = pd.DataFrame({
        "Silhouette_avg": [0.4], "Clusters": [5], "Noise_points": [2],
        "Min_samples": [4], "Min_cluster_size": [6], "Epsilon": [0],
        "Score": [-0.2],
    })
    adapted, migration = normalize_model_table_schema(source)
    assert adapted.loc[0, "silhouette"] == 0.4
    assert adapted.loc[0, "source_Score"] == -0.2
    assert adapted.loc[0, "status"] == "success"
    assert migration["column_migrations"]["Clusters"] == "number_of_clusters"


def test_cli_exposes_new_commands_and_alias():
    parser = build_parser()
    help_text = parser.format_help()
    assert "explain" in help_text
    assert "compare" in help_text
    assert "validate" in help_text
    parsed = parser.parse_args(["interpret", "--model-json", "summary.json"])
    assert parsed.command == "interpret"


def test_cli_compare_end_to_end(tmp_path):
    left, right = _label_tables(tmp_path)
    status = main([
        "compare", "--left", str(left), "--right", str(right),
        "--output-dir", str(tmp_path / "comparison"),
    ])
    assert status == 0
    payload = json.loads((tmp_path / "comparison/comparison_summary.json").read_text())
    assert payload["adjusted_rand_index"] == pytest.approx(1.0)
