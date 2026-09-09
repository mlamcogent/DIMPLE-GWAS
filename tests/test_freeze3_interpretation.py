from __future__ import annotations

import json

import numpy as np
import pandas as pd
import pytest

from dimple_gwas.config import resolve_config
from dimple_gwas.interpretation import (
    calculate_cutpoints,
    compute_order,
    compute_similarity,
    detect_coordinate_columns,
    run_explanation,
)
from dimple_gwas.io import ensure_empty_output_dir, read_table, validated_identifiers
from dimple_gwas.preprocessing import (
    infer_explanation_orientation,
    prepare_explanation_matrix,
)
from dimple_gwas.visualization import sample_block_preserving


def _native_fixture(tmp_path):
    matrix = pd.DataFrame({
        "variant": ["v1", "v2", "v3", "v4", "v5"],
        "a": [1.0, 2.0, 3.0, 4.0, 5.0],
        "b": [1.1, 2.0, 3.2, 4.0, 5.1],
        "c": [5.0, 4.0, 3.0, 2.0, 1.0],
        "noise": [0.0, 1.0, 0.2, 1.2, 0.1],
    })
    labels = pd.DataFrame({
        "feature_id": ["a", "b", "c", "noise"],
        "label": [0, 0, 1, -1],
        "UMAP_1": [0.0, 0.1, 2.0, 3.0],
        "UMAP_2": [0.0, 0.2, 2.1, 3.2],
    })
    matrix_path = tmp_path / "matrix.tsv"
    labels_path = tmp_path / "labels.tsv"
    summary_path = tmp_path / "summary.json"
    matrix.to_csv(matrix_path, sep="\t", index=False)
    labels.to_csv(labels_path, sep="\t", index=False)
    summary_path.write_text(json.dumps({
        "artifact_schema": "dimple-gwas.model-summary.v3",
        "model": {"model_id": "model_test"},
        "labels_file": "labels.tsv",
        "resolved_run_config": {
            "input": {
                "path": str(matrix_path), "drop_first_n_cols": 1,
                "sep": "\t", "zscore_transform": "none",
            }
        },
    }), encoding="utf-8")
    return matrix, labels, matrix_path, labels_path, summary_path


def test_interpretation_defaults_are_additive():
    config = resolve_config("standard")
    assert config["scoring"]["profile"] == "legacy_dimple"
    assert config["interpretation"]["similarity_metric"] == "pearson"
    assert config["interpretation"]["coordinate_associations"] is False
    assert "reducer" not in config


def test_invalid_interpretation_configuration_fails():
    with pytest.raises(ValueError, match="undefined_correlation"):
        resolve_config("standard", overrides={"interpretation.undefined_correlation": "ignore"})


def test_reader_supports_excel_sheet(tmp_path):
    pytest.importorskip("openpyxl")
    expected = pd.DataFrame({"id": ["a", "b"], "value": [1.5, 2.5]})
    path = tmp_path / "table.xlsx"
    expected.to_excel(path, index=False, sheet_name="Data")
    pd.testing.assert_frame_equal(read_table(path, sheet="Data"), expected)


def test_validated_identifiers_strip_but_reject_duplicates():
    assert validated_identifiers([" a ", "b"], context="test") == ["a", "b"]
    with pytest.raises(ValueError, match="duplicate"):
        validated_identifiers([" a", "a "], context="test")
    with pytest.raises(ValueError, match="empty"):
        validated_identifiers(["a", "  "], context="test")


def test_variants_by_vectors_preserves_vector_ids(tmp_path):
    matrix, *_ = _native_fixture(tmp_path)
    prepared = prepare_explanation_matrix(
        matrix, orientation="variants_by_vectors", drop_first_n_cols=1,
        vector_id_source="matrix_columns",
    )
    assert prepared.analysis.index.tolist() == ["a", "b", "c", "noise"]
    assert prepared.analysis.shape == (4, 5)


def test_vectors_by_variants_explicit_id_column():
    matrix = pd.DataFrame({
        "vector_id": ["v1", "v2", "v3"],
        "feature_a": [1.0, 2.0, 4.0], "feature_b": [4.0, 2.0, 1.0],
    })
    prepared = prepare_explanation_matrix(
        matrix, orientation="vectors_by_variants", drop_first_n_cols=1,
        vector_id_source="column:vector_id",
    )
    assert prepared.analysis.index.tolist() == ["v1", "v2", "v3"]
    assert prepared.analysis.columns.tolist() == ["feature_a", "feature_b"]


def test_orientation_inference_uses_exact_overlap(tmp_path):
    matrix, labels, *_ = _native_fixture(tmp_path)
    orientation, source = infer_explanation_orientation(
        matrix, labels["feature_id"], drop_first_n_cols=1
    )
    assert (orientation, source) == ("variants_by_vectors", "matrix_columns")


def test_coordinate_detection_is_numeric_suffix_order():
    frame = pd.DataFrame({"UMAP_10": [0], "UMAP_2": [0], "UMAP_1": [0]})
    assert detect_coordinate_columns(frame) == ["UMAP_1", "UMAP_2", "UMAP_10"]


def test_similarity_undefined_fails_by_default():
    analysis = pd.DataFrame([[1, 1, 1], [1, 2, 3]], index=["constant", "varied"])
    with pytest.raises(ValueError, match="undefined"):
        compute_similarity(analysis, method="pearson", undefined_policy="error")
    similarity, count = compute_similarity(analysis, method="pearson", undefined_policy="zero")
    assert count > 0
    assert np.isfinite(similarity).all()
    assert np.diag(similarity).tolist() == [1.0, 1.0]


def test_cluster_order_is_numeric_and_noise_last():
    correlation = np.eye(5)
    labels = [-1, 10, 2, 2, 10]
    order = compute_order(correlation, labels, method="cluster", noise_policy="separate_last")
    assert order == [2, 3, 1, 4, 0]


def test_cutpoint_indices_are_auditable():
    result = calculate_cutpoints([2, 2, 10, 10, -1])
    assert result["start_index_0_based"].tolist() == [0, 2, 4]
    assert result["end_index_1_based"].tolist() == [2, 4, 5]


def test_block_sampling_preserves_tiny_cluster():
    labels = [0] * 100 + [1] * 2 + [2] * 100 + [-1]
    selected = sample_block_preserving(labels, 20)
    assert len(selected) == 20
    assert {labels[index] for index in selected} == {0, 1, 2, -1}


def test_native_explanation_end_to_end(tmp_path):
    *_, summary_path = _native_fixture(tmp_path)
    output = tmp_path / "interpretation"
    config = resolve_config("standard")["interpretation"]
    manifest = run_explanation(
        output_dir=output, interpretation_config=config, model_json=summary_path
    )
    assert manifest["status"] == "complete"
    assert manifest["vector_counts"]["analyzed"] == 4
    expected = {
        "interpretation_manifest.json", "original_space_similarity.tsv.gz",
        "heatmap_order.tsv", "cluster_cutpoints.tsv", "cluster_summary.tsv",
        "projection_quality.tsv", "original_space_heatmap.html",
        "original_space_heatmap.png", "exclusions.tsv", "README.md",
    }
    assert expected <= {path.name for path in output.iterdir()}
    assert "data:image/png;base64" in (output / "original_space_heatmap.html").read_text()


def test_native_explanation_refuses_nonempty_output(tmp_path):
    *_, summary_path = _native_fixture(tmp_path)
    output = tmp_path / "interpretation"
    output.mkdir()
    (output / "existing.txt").write_text("keep", encoding="utf-8")
    with pytest.raises(ValueError, match="not empty"):
        run_explanation(
            output_dir=output,
            interpretation_config=resolve_config("standard")["interpretation"],
            model_json=summary_path,
        )
    assert (output / "existing.txt").read_text(encoding="utf-8") == "keep"


def test_legacy_incomplete_matching_writes_exclusions(tmp_path):
    _, labels, matrix_path, labels_path, _ = _native_fixture(tmp_path)
    labels.iloc[:-1].to_csv(labels_path, sep="\t", index=False)
    config = dict(resolve_config("standard")["interpretation"])
    config["require_complete_match"] = False
    manifest = run_explanation(
        output_dir=tmp_path / "legacy",
        interpretation_config=config,
        legacy_table=labels_path,
        input_path=matrix_path,
        matrix_orientation="variants_by_vectors",
        vector_id_source="matrix_columns",
        drop_first_n_cols=1,
    )
    exclusions = pd.read_csv(tmp_path / "legacy/exclusions.tsv", sep="\t")
    assert manifest["mode"] == "legacy"
    assert exclusions["feature_id"].tolist() == ["noise"]


def test_empty_output_directory_helper(tmp_path):
    created = ensure_empty_output_dir(tmp_path / "new")
    assert created.is_dir()
    assert ensure_empty_output_dir(created) == created
