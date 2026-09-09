#!/usr/bin/env python3
"""Build a verified, machine-readable output atlas from source maps and tutorial artifacts."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any


FREEZE3 = Path(__file__).resolve().parents[4]
MANUAL = FREEZE3 / "docs" / "manual"
EVIDENCE = MANUAL / "evidence"
TUTORIALS = MANUAL / "tutorials"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def first_header(path: Path) -> str:
    suffixes = path.suffixes
    if suffixes[-2:] == [".tsv", ".gz"]:
        with gzip.open(path, "rt", encoding="utf-8") as stream:
            return stream.readline().rstrip("\n")[:700]
    if path.suffix in {".tsv", ".csv"}:
        delimiter = "\t" if path.suffix == ".tsv" else ","
        with path.open(encoding="utf-8") as stream:
            row = next(csv.reader(stream, delimiter=delimiter), [])
        return " | ".join(row)[:700]
    if path.suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            return "JSON keys: " + ", ".join(payload.keys())[:650]
    if path.suffix in {".yaml", ".yml"}:
        return "YAML mapping; inspect resolved values and source checksum"
    if path.suffix == ".png":
        from PIL import Image
        with Image.open(path) as image:
            return f"PNG {image.width}x{image.height}, mode={image.mode}"
    return f"{path.suffix.lstrip('.').upper() or 'file'}; inspect with format-appropriate reader"


EXAMPLES = {
    "resolved_config.yaml": "01_fixed_synthetic/run_20260825_v2/resolved_config.yaml",
    "search_space_manifest.tsv/json": "02_custom_search_space/run_20260825/search_space_manifest.tsv",
    "run_manifest.json": "02_custom_search_space/run_20260825/run_manifest.json",
    "logs/run.log": "02_custom_search_space/run_20260825/logs/run.log",
    "models/all_models.tsv": "02_custom_search_space/run_20260825/models/all_models.tsv",
    "models/ranked_models.tsv": "02_custom_search_space/run_20260825/models/ranked_models.tsv",
    "models/all_models.parquet": "02_custom_search_space/run_20260825/models/all_models.parquet",
    "models/top_models.tsv": "02_custom_search_space/run_20260825/models/top_models.tsv",
    "models/best_model.json": "02_custom_search_space/run_20260825/models/best_model.json",
    "models/model_selection_manifest.json": "02_custom_search_space/run_20260825/models/model_selection_manifest.json",
    "models/pareto_front.tsv": "02_custom_search_space/run_20260825/models/pareto_front.tsv",
    "models/family_summaries.tsv": "02_custom_search_space/run_20260825/models/family_summaries.tsv",
    "stage02_hdbscan_gridsearch_results.csv": "02_custom_search_space/run_20260825/stage02_hdbscan_gridsearch_results.csv",
    "stage03_optimized_cluster_solutions.csv": "02_custom_search_space/run_20260825/stage03_optimized_cluster_solutions.csv",
    "stage09_umap_vizdata_with_clusters.csv": "02_custom_search_space/run_20260825/stage09_umap_vizdata_with_clusters.csv",
    "stage09b_umap_vizdata_with_annotations.csv": "02_custom_search_space/run_20260825/stage09b_umap_vizdata_with_annotations.csv",
    "<output> + <output>.manifest.json": "03_explain_compare_validate/scored_20260825.tsv",
    "family_summaries.tsv, pareto_front.tsv, top_models.tsv, summary.json": "03_explain_compare_validate/summaries_20260825/summary.json",
    "original_space_similarity.tsv.gz": "03_explain_compare_validate/explanation_20260825/original_space_similarity.tsv.gz",
    "heatmap_order.tsv": "03_explain_compare_validate/explanation_20260825/heatmap_order.tsv",
    "cluster_cutpoints.tsv": "03_explain_compare_validate/explanation_20260825/cluster_cutpoints.tsv",
    "cluster_summary.tsv": "03_explain_compare_validate/explanation_20260825/cluster_summary.tsv",
    "projection_quality.tsv": "03_explain_compare_validate/explanation_20260825/projection_quality.tsv",
    "coordinate_associations.tsv": "",
    "exclusions.tsv": "03_explain_compare_validate/explanation_20260825/exclusions.tsv",
    "original_space_heatmap.png/html": "03_explain_compare_validate/explanation_20260825/original_space_heatmap.png",
    "interpretation_manifest.json + README.md": "03_explain_compare_validate/explanation_20260825/interpretation_manifest.json",
    "comparison_summary.json": "03_explain_compare_validate/comparison_20260825/comparison_summary.json",
    "membership_comparison.tsv, cluster_sizes.tsv, label_confusion.tsv, optimal_label_mapping.tsv": "03_explain_compare_validate/comparison_20260825/membership_comparison.tsv",
    "comparison_manifest.json": "03_explain_compare_validate/comparison_20260825/comparison_manifest.json",
    "validation_checks.tsv": "03_explain_compare_validate/validation_20260825/validation_checks.tsv",
    "validation_report.json + validation_manifest.json": "03_explain_compare_validate/validation_20260825/validation_report.json",
}


CLASSIFICATION = {
    "resolved configuration": ("machine-facing", "authoritative configuration"),
    "complete deterministic enumeration": ("both", "authoritative enumeration"),
    "software/input/config/runtime/artifact provenance": ("both", "authoritative provenance"),
    "execution narrative": ("human-facing", "diagnostic"),
}


def privacy_for(artifact: str) -> str:
    if any(token in artifact for token in ("labels", "annotation", "heatmap", "similarity", "association", "input")):
        return "May expose phenotype identifiers, annotations, or derived study structure; apply the input study's access policy."
    if "manifest" in artifact or "log" in artifact or "config" in artifact:
        return "May expose paths, commands, host metadata, or input hashes; sanitize before publication."
    return "Usually derived metrics; still review identifiers, paths, and study-policy restrictions."


def inspection_for(fmt: str, artifact: str) -> str:
    if "TSV" in fmt or "CSV" in fmt:
        return "Check the header, row count, identifier uniqueness, status/missing fields, and delimiter with a tabular reader."
    if "JSON" in fmt:
        return "Parse as JSON; confirm schema/version/status, hashes, counts, and paths rather than relying on visual text search."
    if "YAML" in fmt:
        return "Use inspect-config or a YAML parser; distinguish resolved values from the source overlay."
    if "PNG" in fmt or "HTML" in fmt:
        return "Read sidecar order/manifest tables first, then inspect the rendering for clipping and label consistency."
    return "Inspect with the format-appropriate reader and retain the generating manifest."


def healthy_for(artifact: str) -> str:
    if "run_manifest" in artifact:
        return "status=complete; source/input hashes present; failed count understood; selected model and artifact records resolve."
    if "validation" in artifact:
        return "Every check is visible; aggregate status matches pass/warn/fail rows; a warning is not silently treated as a pass."
    if "all_models" in artifact or "ranked" in artifact:
        return "Candidate count agrees with enumeration; failures remain; ranks and score eligibility are internally consistent."
    if "labels" in artifact or "membership" in artifact:
        return "Identifiers are unique and exactly match the intended input; label -1 is treated as noise/unassigned."
    if "heatmap" in artifact:
        return "Image dimensions are nonzero; order and cutpoints match sidecars; no inferential claim is attached."
    return "Artifact exists under the new output root, is readable, and its checksum is recorded."


def main() -> None:
    source = EVIDENCE / "output_producer_consumer_map.tsv"
    with source.open(encoding="utf-8") as stream:
        producer_rows = list(csv.DictReader(stream, delimiter="\t"))
    rows: list[list[Any]] = []
    for index, record in enumerate(producer_rows, start=1):
        artifact = record["artifact"]
        example_rel = EXAMPLES.get(artifact, "")
        example = TUTORIALS / example_rel if example_rel else None
        verified = bool(example and example.is_file())
        excerpt = first_header(example) if verified else "Not generated because optional feature was not enabled in the executed bounded tutorials."
        checksum = sha256(example) if verified else ""
        audience, authority = CLASSIFICATION.get(record["meaning"], ("both", "derived" if "summary" in record["meaning"] or "diagnostic" in record["meaning"] else "authoritative or contract-bearing"))
        rows.append([
            f"ART-{index:03d}", artifact, record["command"], record["producer"], record["condition"], record["format"],
            record["meaning"], "Rows are observations/candidates/IDs/checks as named; JSON/YAML are mappings.", excerpt,
            "feature_id/model_id/candidate_ordinal or documented JSON keys", "-1 means HDBSCAN noise/unassigned; other integers are local labels.",
            "Rank is score-descending, raw-score-descending, model_id-ascending where applicable.", inspection_for(record["format"], artifact),
            healthy_for(artifact), "Do not compare numeric cluster labels across runs; do not infer biology from internal scores.",
            record["consumer"], audience, authority, privacy_for(artifact), example_rel, checksum,
            "3.0.0rc1" if verified else "", "verified" if verified else "optional_not_executed",
        ])

    # Explicitly record important non-artifacts so readers do not hunt for files the implementation never emits.
    rows.extend([
        ["NON-001", "cleaned/transformed input matrix", "run", "not emitted by Freeze 3", "never", "not applicable", "Prepared in memory", "vectors x variables after transpose", "No file", "feature_id in memory", "not applicable", "not applicable", "Inspect resolved_config and input contract; reproduce preprocessing from source.", "Absence is expected.", "Do not assume the original input was rewritten.", "embedding stage", "machine-facing", "ephemeral", "Original input may be restricted.", "", "", "3.0.0rc1", "verified_non_artifact"],
        ["NON-002", "individual repeated UMAP embeddings", "run", "not emitted by Freeze 3", "never", "not applicable", "Computed and cached in memory by UMAP family", "vectors x n_components per repeat", "No file", "feature_id order follows prepared analysis matrix", "not applicable", "not applicable", "Inspect run manifest seeds and selected visualization coordinates.", "Absence is expected.", "Do not invent per-seed embedding files.", "concatenation", "machine-facing", "ephemeral", "Embeddings may reveal study structure.", "", "", "3.0.0rc1", "verified_non_artifact"],
        ["NON-003", "concatenated embedding matrix", "run", "not emitted by Freeze 3", "never", "not applicable", "Computed and cached in memory for HDBSCAN", "vectors x (n_components x repeats)", "No file", "feature_id order follows prepared analysis matrix", "not applicable", "not applicable", "Use retained labels and manifest; a future feature would require a new contract.", "Absence is expected.", "Visualization coordinates are not the full concatenated embedding.", "HDBSCAN", "machine-facing", "ephemeral", "Embedding may reveal study structure.", "", "", "3.0.0rc1", "verified_non_artifact"],
    ])
    header = [
        "artifact_id", "name_or_pattern", "producing_command", "producer", "creation_condition", "format_encoding",
        "meaning", "orientation", "verified_schema_or_excerpt", "identifiers", "cluster_noise_convention", "ordering_ranking_semantics",
        "safe_inspection", "healthy_properties", "warning_signs_common_mistakes", "downstream_consumers", "audience", "authority_class",
        "privacy_security", "verified_tutorial_example", "example_sha256", "software_version", "verification_status",
    ]
    with (EVIDENCE / "output_atlas.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


if __name__ == "__main__":
    main()
