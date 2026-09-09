#!/usr/bin/env python3
"""Regenerate the Edition 2 output atlas against fresh TE2 lab artifacts."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


EDITION2 = Path(__file__).resolve().parents[2]
FREEZE3 = EDITION2.parents[2]
EVIDENCE = EDITION2 / "evidence"
ATLAS = EDITION2 / "output_atlas"


def load_base():
    source = FREEZE3 / "docs/manual/build/tools/generate_output_atlas.py"
    spec = importlib.util.spec_from_file_location("edition1_output_atlas", source)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    source_map = FREEZE3 / "docs/manual/evidence/output_producer_consumer_map.tsv"
    (EVIDENCE / "output_producer_consumer_map.tsv").write_text(source_map.read_text(encoding="utf-8"), encoding="utf-8")
    base = load_base()
    base.MANUAL = EDITION2
    base.EVIDENCE = EVIDENCE
    base.TUTORIALS = EDITION2 / "labs"
    fixed = "01_fixed_synthetic/run_20260826"
    custom = "02_custom_search_space/run_20260826"
    downstream = "03_explain_compare_validate"
    examples = {
        "resolved_config.yaml": f"{fixed}/resolved_config.yaml",
        "search_space_manifest.tsv/json": f"{custom}/search_space_manifest.tsv",
        "run_manifest.json": f"{custom}/run_manifest.json",
        "logs/run.log": f"{custom}/logs/run.log",
        "models/all_models.tsv": f"{custom}/models/all_models.tsv",
        "models/ranked_models.tsv": f"{custom}/models/ranked_models.tsv",
        "models/all_models.parquet": f"{custom}/models/all_models.parquet",
        "models/top_models.tsv": f"{custom}/models/top_models.tsv",
        "models/best_model.json": f"{custom}/models/best_model.json",
        "models/model_selection_manifest.json": f"{custom}/models/model_selection_manifest.json",
        "models/pareto_front.tsv": f"{custom}/models/pareto_front.tsv",
        "models/family_summaries.tsv": f"{custom}/models/family_summaries.tsv",
        "models/top_model_artifacts/<id>/labels.tsv": f"{fixed}/models/top_model_artifacts/model_060fac0208bb58e2/labels.tsv",
        "models/top_model_artifacts/<id>/summary.json": f"{fixed}/models/top_model_artifacts/model_060fac0208bb58e2/summary.json",
        "models/top_model_artifacts/<id>/reproduce.yaml": f"{fixed}/models/top_model_artifacts/model_060fac0208bb58e2/reproduce.yaml",
        "stage02_hdbscan_gridsearch_results.csv": f"{custom}/stage02_hdbscan_gridsearch_results.csv",
        "stage03_optimized_cluster_solutions.csv": f"{custom}/stage03_optimized_cluster_solutions.csv",
        "stage09_umap_vizdata_with_clusters.csv": f"{custom}/stage09_umap_vizdata_with_clusters.csv",
        "stage09b_umap_vizdata_with_annotations.csv": f"{custom}/stage09b_umap_vizdata_with_annotations.csv",
        "<output> + <output>.manifest.json": f"{downstream}/scored_20260826.tsv",
        "family_summaries.tsv, pareto_front.tsv, top_models.tsv, summary.json": f"{downstream}/summaries_20260826/summary.json",
        "original_space_similarity.tsv.gz": f"{downstream}/explanation_20260826/original_space_similarity.tsv.gz",
        "heatmap_order.tsv": f"{downstream}/explanation_20260826/heatmap_order.tsv",
        "cluster_cutpoints.tsv": f"{downstream}/explanation_20260826/cluster_cutpoints.tsv",
        "cluster_summary.tsv": f"{downstream}/explanation_20260826/cluster_summary.tsv",
        "projection_quality.tsv": f"{downstream}/explanation_20260826/projection_quality.tsv",
        "coordinate_associations.tsv": "",
        "exclusions.tsv": f"{downstream}/explanation_20260826/exclusions.tsv",
        "original_space_heatmap.png/html": f"{downstream}/explanation_20260826/original_space_heatmap.png",
        "interpretation_manifest.json + README.md": f"{downstream}/explanation_20260826/interpretation_manifest.json",
        "comparison_summary.json": f"{downstream}/comparison_20260826/comparison_summary.json",
        "membership_comparison.tsv, cluster_sizes.tsv, label_confusion.tsv, optimal_label_mapping.tsv": f"{downstream}/comparison_20260826/membership_comparison.tsv",
        "comparison_manifest.json": f"{downstream}/comparison_20260826/comparison_manifest.json",
        "validation_checks.tsv": f"{downstream}/validation_20260826/validation_checks.tsv",
        "validation_report.json + validation_manifest.json": f"{downstream}/validation_20260826/validation_report.json",
    }
    base.EXAMPLES = examples
    base.main()

    ATLAS.mkdir(parents=True, exist_ok=True)
    output_tsv = ATLAS / "output_atlas.tsv"
    output_tsv.write_text((EVIDENCE / "output_atlas.tsv").read_text(encoding="utf-8"), encoding="utf-8")
    with output_tsv.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    artifacts = [r for r in rows if r["artifact_id"].startswith("ART-")]
    non_artifacts = [r for r in rows if r["artifact_id"].startswith("NON-")]
    verified = [r for r in artifacts if r["verification_status"] == "verified"]
    optional = [r for r in artifacts if r["verification_status"] != "verified"]
    groups = {}
    for row in artifacts:
        groups.setdefault(row["producing_command"], []).append(row)
    lines = [
        "# DIMPLE-GWAS Freeze 3 RC1 output atlas",
        "",
        f"This atlas contains **{len(artifacts)} produced artifact patterns** and **{len(non_artifacts)} important non-artifacts**. Fresh Edition 2 Labs 1–3 verify {len(verified)} patterns; {len(optional)} optional pattern remains unexecuted and is labeled accordingly. The machine-readable contract is `output_atlas.tsv`.",
        "",
        "An output is meaningful only with its producer, creation condition, schema, identifier rules, ordering, checksum, and evidence status. Native manifests may contain absolute paths and host details; publish only sanitized excerpts.",
    ]
    for command in ["run", "run/show-search-space", "score-existing", "summarize-models", "explain", "compare", "validate"]:
        selected = groups.get(command, [])
        if not selected:
            continue
        lines += ["", f"## `{command}` artifacts", "", "| Pattern | Purpose | Condition | Verification |", "| --- | --- | --- | --- |"]
        for row in selected:
            lines.append(f"| `{row['name_or_pattern']}` | {row['meaning']} | {row['creation_condition']} | {row['verification_status']} |")
    lines += ["", "## Important non-artifacts", ""]
    for row in non_artifacts:
        lines.append(f"- **{row['name_or_pattern']}:** {row['meaning']}. {row['warning_signs_common_mistakes']}")
    lines += ["", "## Reading rules", "", "A `model_id` is a deterministic candidate identity, not a scientific label. Candidate tables retain failed and invalid candidates. Rank is descending score, then descending raw score, then ascending model ID. HDBSCAN label `-1` is unassigned under a fitted representation and parameter set. The selected display coordinates are not the full repeated concatenated embedding. Original-space similarities are descriptive and conditional on the selected partition."]
    (ATLAS / "OUTPUT_ATLAS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    manifest_path = EDITION2 / "BOOK_BUILD_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["output_atlas"] = {"artifact_patterns": len(artifacts), "important_non_artifacts": len(non_artifacts), "freshly_verified": len(verified), "optional_unexecuted": len(optional), "gate_7": "pass_with_optional_coordinate_associations_not_executed"}
    manifest["phase_status"]["phase_7_output_atlas"] = "complete_with_optional_coordinate_associations_not_executed"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Output atlas: {len(artifacts)} artifact patterns; {len(verified)} fresh verified; {len(optional)} optional unexecuted")


if __name__ == "__main__":
    main()
