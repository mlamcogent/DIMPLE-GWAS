from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[5]
WORKSPACE_ROOT = PACKAGE_ROOT.parent
EVIDENCE = PACKAGE_ROOT / "docs" / "edition3" / "evidence"
QA_ROOT = PACKAGE_ROOT / "docs" / "edition3" / "qa" / "stage1"
OUTPUT = EVIDENCE / "STAGE1_MANIFEST.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def package_relative(path: Path) -> str:
    return path.relative_to(PACKAGE_ROOT).as_posix()


with (EVIDENCE / "00_SOURCE_INVENTORY_AND_CHECKSUMS.tsv").open(encoding="utf-8", newline="") as handle:
    inventory = list(csv.DictReader(handle, delimiter="\t"))
source_hashes = {row["workspace_relative_path"]: row["sha256"] for row in inventory}

evidence_files = sorted(path for path in EVIDENCE.iterdir() if path.is_file() and path.name != OUTPUT.name)
qa_evidence = [
    QA_ROOT / "test_results" / "freeze3_pytest.xml",
    QA_ROOT / "test_results" / "generated_output_checks.json",
    QA_ROOT / "generated" / "fixed_run" / "run_manifest.json",
    QA_ROOT / "generated" / "fixed_comparison" / "comparison_summary.json",
    QA_ROOT / "generated" / "fixed_validation" / "validation_report.json",
    QA_ROOT / "generated" / "fresh_rescored_164_models.tsv",
]
produced_hashes = {package_relative(path): sha256(path) for path in evidence_files + qa_evidence}

manifest = {
    "manifest_schema": "dimple-gwas.edition3-stage1.v1",
    "created_at_utc": datetime.now(timezone.utc).isoformat(),
    "decision": "PASS_WITH_LIMITATIONS",
    "scope": "Edition 3 Stage 1 local evidence closure only; textbook authoring not begun",
    "authoritative_source": "DIMPLE-GWAS-freeze3",
    "software_version": "3.0.0rc1",
    "source_identity": {
        "git_commit": None,
        "git_identity_status": "unavailable_not_a_git_repository",
        "package_source_sha256": "df87825992ab51dc016c673cf420a978ba5c161bd6c755e00a5199ead310e65b",
        "source_inventory_record_count": len(inventory),
        "source_inventory_sha256": sha256(EVIDENCE / "00_SOURCE_INVENTORY_AND_CHECKSUMS.tsv"),
        "source_hashes": source_hashes,
    },
    "exact_configuration_and_artifact_ids": {
        "fixed_tutorial_config_file_sha256": "16406ec39de81f87493c6bc6cbe28252a607ab85c429195af4b9924154d6e8ff",
        "fixed_resolved_configuration_sha256": "67b5f18293839440de6c04fc8cc171bf2f349d83900fa0092c50ba79e7e14ef9",
        "fixed_input_sha256": "77d1956fd074da9d82ce0d6a9c896446895a5e22b2fc6da85417169d13b9bb01",
        "fixed_annotations_sha256": "39a8abf9426723ee812e0ff9463add0e04a25768245cf5ca630fd907a70974bd",
        "fixed_selected_model_id": "model_060fac0208bb58e2",
        "fixed_labels_sha256": "5b7ba37a542efcceebd5d39a69342279e44565f017c2c099e36060c3eb0496ee",
        "historical_164_input_sha256": "0cc17db052e28e3c1cd7600f7140f9b929b9e2d2a5b4f9ded3ebf4df3e032f96",
        "historical_164_id_key_sha256": "b664e6139e18305168327c5420c1a1af8379312f3ce0645f5f42dbcc394febc4",
        "historical_164_model_table_sha256": "78600f27b1ebc580327e409e30634acde92ff6089575a5818c81adc3d9edeb88",
        "historical_164_selected_config_file_sha256": source_hashes["DIMPLE-GWAS-freeze3/configs/original_idp_164_selected.yaml"],
    },
    "fresh_local_execution": {
        "platform": "macOS-26.5.1-arm64-arm-64bit",
        "python": "3.12.13",
        "environment_source": "retained Freeze 2 project virtual environment; Freeze 3 source imported from working directory",
        "logged_commands": 31,
        "logged_command_failures": 0,
        "pytest": {"passed": 44, "skipped": 1, "warnings": 5, "duration_seconds": 10.70, "skip_reason": "openpyxl absent for optional XLSX test"},
        "search_space_counts": {"standard": 2430, "extended": 1728, "fixed": 1},
        "fixed_run": {"successful": 1, "invalid_topology": 0, "failed": 0, "clusters": 3, "noise": 0},
        "fixed_reproduction": {"model_id_equal": True, "labels_byte_identical": True},
        "fixed_comparison": {"ari": 1.0, "nmi": 1.0, "noise_set_jaccard": 1.0, "mapped_membership_fraction": 1.0, "variation_of_information_nats": 0.0, "procrustes_disparity": 2.7088204667806472e-31},
        "fixed_validation": {"passed": 24, "failed": 0, "warnings": 0},
        "historical_164_rescore": {"rows": 333, "joined_rows": 333, "score_max_abs_delta": 0.0},
    },
    "gate_results": {
        "G1_source_inventory": "met",
        "G2_authority_lineage_release_boundary": "met",
        "G3_implementation_truth": "met",
        "G4_claim_audit": "met",
        "G5_methods_and_education_literature": "met",
        "G6_reviewer_crosswalk": "met",
        "G7_analysis_hierarchy": "met",
        "G8_function_concept_output_coverage": "met",
        "G9_safe_language": "met",
        "G10_cli_config_tests": "met_with_optional_xlsx_limit",
        "G11_bounded_end_to_end": "met",
        "G12_manifest_privacy_and_gaps": "met_with_publication_path_limit",
    },
    "unresolved_gap_ids": [f"G-{index:03d}" for index in range(1, 19)],
    "release_boundary": {
        "included": ["local software execution", "fixed synthetic fixture", "retained score reconstruction", "artifact integrity", "documentation evidence closure"],
        "excluded": ["scientific freeze", "fresh 164-IDP 1000-seed fit", "fresh 2315-IDP fit", "fresh 459-IDP fit", "cross-platform or Docker validation", "new reviewer scientific analyses"],
    },
    "privacy_and_path_review": {
        "publishable_evidence_absolute_user_paths": 0,
        "publishable_evidence_secret_patterns": 0,
        "local_qa_absolute_paths_present": True,
        "publication_action": "sanitize copies of runtime manifests and logs; preserve private originals",
    },
    "produced_file_hashes": produced_hashes,
    "generated_checksum_index": "docs/edition3/qa/stage1/generated_checksums.tsv",
    "self_hash_policy": "The manifest does not hash itself. The QA checksum index records the QA tree and intentionally excludes its own recursive hash.",
}

OUTPUT.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(f"wrote {OUTPUT}")
