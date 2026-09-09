#!/usr/bin/env python3
"""Summarize the executed manual-build environment, tutorials, and checksums."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FREEZE3 = Path(__file__).resolve().parents[4]
MANUAL = FREEZE3 / "docs" / "manual"
BUILD = MANUAL / "build"
EVIDENCE = MANUAL / "evidence"
TUTORIALS = MANUAL / "tutorials"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_tsv(path: Path, header: list[str], rows: list[list[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dependencies() -> None:
    log = (BUILD / "logs" / "pip_freeze.log").read_text(encoding="utf-8")
    stdout = log.split("===== STDOUT =====\n", 1)[1].split("\n===== STDERR =====", 1)[0].strip()
    (EVIDENCE / "resolved_dependencies.txt").write_text(stdout + "\n", encoding="utf-8")


def runtime_environment() -> None:
    run = load(TUTORIALS / "02_custom_search_space" / "run_20260825" / "run_manifest.json")
    pytest_meta = load(BUILD / "logs" / "pytest_full.json")
    pip_check = load(BUILD / "logs" / "pip_check.json")
    text = f"""# Runtime environment

- Evidence recorded: `{datetime.now(timezone.utc).isoformat()}`
- Operating system/platform: `{run['platform']}`
- Architecture: `{run['architecture']}`
- Isolated Python: `{run['python_version']}`
- Package: DIMPLE-GWAS `{run['software_version']}`
- Package-source SHA-256: `{run['package_source_sha256']}`
- Input SHA-256 for executed synthetic tutorials: `{run['input']['sha256']}`
- Reducer backend: `{run['backends']['reducer']}`
- Clusterer backend: `{run['backends']['clusterer']}`
- Tutorial thread settings: `n_jobs={run['thread_settings']['n_jobs']}`, `candidate_jobs={run['thread_settings']['candidate_jobs']}`, `core_dist_n_jobs={run['thread_settings']['hdbscan_core_dist_n_jobs']}`
- Test thread caps: `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `NUMBA_NUM_THREADS=1`
- Dependency integrity: `pip check` exit `{pip_check['exit_code']}`
- Fresh pytest: exit `{pytest_meta['exit_code']}`, duration `{pytest_meta['duration_seconds']:.2f}` seconds

## Installed scientific stack

| Package | Exact version |
| --- | --- |
"""
    for package, version in run["package_versions"].items():
        text += f"| `{package}` | `{version}` |\n"
    text += """

## Reproducibility boundary

These versions and checksums identify the executed macOS/Apple-Silicon environment. They do not guarantee bitwise equality on Linux, another architecture, another BLAS/OpenMP implementation, or a future Docker image. The Docker phase should reuse the exact source/checksum manifest and record any platform-dependent tolerance.
"""
    (EVIDENCE / "runtime_environment.md").write_text(text, encoding="utf-8")


def test_report() -> None:
    meta = load(BUILD / "logs" / "pytest_full.json")
    log = (BUILD / "logs" / "pytest_full.log").read_text(encoding="utf-8")
    summary = next((line.strip() for line in reversed(log.splitlines()) if "passed" in line), "summary not found")
    report = f"""# Fresh test execution report

- Command: `{' '.join(meta['command'])}`
- Working directory: `{meta['working_directory']}`
- Started UTC: `{meta['started_utc']}`
- Duration: `{meta['duration_seconds']:.3f}` seconds
- Exit status: `{meta['exit_code']}`
- Pytest summary: `{summary}`
- Machine-readable JUnit: `docs/manual/build/logs/pytest_full.xml`

The suite is evidence of tested software contracts. It is not a biological validation and is not a cross-platform compatibility result. Warnings remain visible in the complete log at `docs/manual/build/logs/pytest_full.log`.
"""
    (EVIDENCE / "test_execution_report.md").write_text(report, encoding="utf-8")


def tutorial_manifest(name: str, root: Path, status: str, command_logs: list[str], notes: list[str]) -> None:
    files = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and "execution_manifest" not in path.name:
            files.append({
                "path": path.relative_to(MANUAL).as_posix(),
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
            })
    payload = {
        "schema": "dimple-gwas.manual-tutorial.v1",
        "tutorial": name,
        "status": status,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "software_version": "3.0.0rc1",
        "package_source_sha256": load(TUTORIALS / "02_custom_search_space" / "run_20260825" / "run_manifest.json")["package_source_sha256"],
        "command_logs": command_logs,
        "notes": notes,
        "artifacts": files,
    }
    (root / "execution_manifest.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def tutorials() -> None:
    run1 = load(TUTORIALS / "01_fixed_synthetic" / "run_20260825_v2" / "run_manifest.json")
    run2 = load(TUTORIALS / "02_custom_search_space" / "run_20260825" / "run_manifest.json")
    comparison = load(TUTORIALS / "03_explain_compare_validate" / "comparison_20260825" / "comparison_summary.json")
    validation = load(TUTORIALS / "03_explain_compare_validate" / "validation_20260825" / "validation_report.json")

    tutorial_manifest(
        "01_fixed_synthetic",
        TUTORIALS / "01_fixed_synthetic",
        "complete",
        ["build/logs/tutorial01_inspect_config.log", "build/logs/tutorial01_show_search_space.log", "build/logs/tutorial01_run_v2.log"],
        [f"One candidate; selected {run1['selected_model']}; {run1['completed_models']} completed model.", "The earlier run_20260825 is retained as a documented annotation-join mistake; run_20260825_v2 is canonical."],
    )
    tutorial_manifest(
        "02_custom_search_space",
        TUTORIALS / "02_custom_search_space",
        "complete",
        ["build/logs/tutorial02_inspect_config.log", "build/logs/tutorial02_show_search_space.log", "build/logs/tutorial02_run.log"],
        [f"{run2['search_space_size']} candidates, {run2['completed_models']} completed, {run2['failed_models']} failed; selected {run2['selected_model']}.", f"Runtime {run2['runtime_seconds']:.3f} seconds in the recorded local environment."],
    )
    tutorial_manifest(
        "03_explain_compare_validate",
        TUTORIALS / "03_explain_compare_validate",
        "complete",
        [
            "build/logs/tutorial03_score_existing.log", "build/logs/tutorial03_summarize.log",
            "build/logs/tutorial03_reproduce.log", "build/logs/tutorial03_explain.log",
            "build/logs/tutorial03_compare.log", "build/logs/tutorial03_validate.log",
        ],
        [f"Comparison ARI={comparison['adjusted_rand_index']}, NMI={comparison['normalized_mutual_information']}, mapped membership={comparison['mapped_membership_match_fraction']}, Procrustes={comparison['procrustes_disparity']:.3e}.", f"Validation {validation['status']}: {validation['passed']}/{validation['checks']} checks, {validation['warnings']} warnings, {validation['failures']} failures."],
    )
    tutorial_manifest(
        "04_mnist_benchmark",
        TUTORIALS / "04_mnist_benchmark",
        "bounded_historical_evidence",
        [],
        ["Not freshly rerun in the manual build; prior verified outputs and a 273.47-second historical runtime are documented.", "A fresh acquisition/rerun belongs to the Docker stage and must record dataset identity and licence."],
    )
    tutorial_manifest(
        "05_original_idp_reconstruction",
        TUTORIALS / "05_original_idp_reconstruction",
        "historical_track_complete_fresh_track_deferred",
        [],
        ["Track A documents immutable historical counts, score adaptation, and manual row-16 selection.", "Track B full 164-IDP 1,000-seed execution is deferred until Docker by coordinator direction."],
    )
    issues = [
        ["TUT-001", "Tutorial 1 initial annotation join", "The first executed configuration used annotation_index_col=feature_id, but the supplied annotation table uses index.", "Annotation was skipped with a warning; clustering remained complete.", "Changed both tutorial YAML files to annotation_index_col=index and reran Tutorial 1 as run_20260825_v2.", "resolved", "run_20260825 retained; run_20260825_v2 canonical"],
        ["TUT-002", "First-run JIT overhead", "Small UMAP runs include Numba compilation/startup overhead.", "Wall time is not a steady-state performance benchmark.", "Report exact manifest runtime only and label it environment/fixture-specific.", "bounded", "all tutorials"],
        ["TUT-003", "Full 164-IDP run", "The original-data protocol requests 1,000 repeated seeds.", "High-cost scientific reproduction is not present in this documentation build.", "Deferred until Docker image exists, per coordinator direction; historical adaptation remains separate.", "deferred", "Tutorial 5"],
        ["TUT-004", "Cross-platform equality", "Only macOS arm64 was executed.", "No Docker/Linux/cloud compatibility conclusion is available.", "Docker handoff defines checksums, commands, and exact/tolerance gates.", "open", "Chapter 44"],
    ]
    write_tsv(EVIDENCE / "tutorial_issue_register.tsv", ["issue_id", "area", "observation", "impact", "resolution_or_handling", "status", "scope"], issues)

    fixture = FREEZE3 / "benchmarks" / "synthetic" / "synthetic_matrix.tsv"
    config1 = TUTORIALS / "01_fixed_synthetic" / "tutorial_config.yaml"
    config2 = TUTORIALS / "02_custom_search_space" / "tutorial_config.yaml"
    input_hash = sha256(fixture)
    step_specs = [
        ("T01-S01", "01_fixed_synthetic", "tutorial01_inspect_config", config1, "resolved configuration is valid; one candidate", "Chapters 11-13"),
        ("T01-S02", "01_fixed_synthetic", "tutorial01_show_search_space", config1, "candidate_models=1; complete manifests written", "Chapters 12-13"),
        ("T01-S03", "01_fixed_synthetic", "tutorial01_run_v2", config1, "exit 0; one successful model; three non-noise clusters", "Chapters 13-14, 32"),
        ("T02-S01", "02_custom_search_space", "tutorial02_inspect_config", config2, "resolved configuration is valid; 32 candidates", "Chapters 11-12, 33"),
        ("T02-S02", "02_custom_search_space", "tutorial02_show_search_space", config2, "candidate_models=32; complete manifests written", "Chapters 12, 33"),
        ("T02-S03", "02_custom_search_space", "tutorial02_run", config2, "exit 0; 32/32 completed; no failures", "Chapters 18-21, 33"),
        ("T03-S01", "03_explain_compare_validate", "tutorial03_score_existing", config1, "rescored table and scoring manifest exist", "Chapters 20-21, 34"),
        ("T03-S02", "03_explain_compare_validate", "tutorial03_summarize", config1, "family, Pareto, top-model, and summary outputs exist", "Chapters 21, 34"),
        ("T03-S03", "03_explain_compare_validate", "tutorial03_reproduce", config1, "fixed reproduction completed with one selected model", "Chapters 22, 34"),
        ("T03-S04", "03_explain_compare_validate", "tutorial03_explain", config1, "original-space heatmap, tables, and manifest exist", "Chapters 25-27, 34"),
        ("T03-S05", "03_explain_compare_validate", "tutorial03_compare", config1, "ARI=NMI=noise Jaccard=mapped membership=1", "Chapters 23, 30, 34"),
        ("T03-S06", "03_explain_compare_validate", "tutorial03_validate", config1, "24/24 validation checks pass", "Chapters 23, 30, 34"),
    ]
    execution_rows: list[list[Any]] = []
    for step_id, tutorial, log_stem, config_path, assertion, chapters in step_specs:
        meta_path = BUILD / "logs" / f"{log_stem}.json"
        meta = load(meta_path)
        execution_rows.append([
            tutorial,
            step_id,
            json.dumps(meta["command"]),
            meta["working_directory"],
            "docs/manual/build/runtime_env; package 3.0.0rc1",
            fixture.relative_to(FREEZE3).as_posix(),
            input_hash,
            config_path.relative_to(FREEZE3).as_posix(),
            sha256(config_path),
            meta["started_utc"],
            meta["ended_utc"],
            f"{meta['duration_seconds']:.6f}",
            "see resolved config/run manifest; tutorial jobs=1 and seeds fixed",
            meta["exit_code"],
            (BUILD / "logs" / f"{log_stem}.log").relative_to(FREEZE3).as_posix(),
            assertion,
            chapters,
        ])
    write_tsv(
        EVIDENCE / "tutorial_execution_manifest.tsv",
        ["tutorial", "step_id", "exact_command_json", "working_directory", "environment_identifier", "input_path", "input_sha256", "configuration_path", "configuration_sha256", "started_utc", "ended_utc", "duration_seconds", "threads_and_seeds", "exit_code", "stdout_stderr_log", "validation_assertion", "manual_section"],
        execution_rows,
    )
    with (EVIDENCE / "tutorial_execution_manifest.tsv").open("a", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(["04_mnist_benchmark", "T04-S01", "protocol only; see tutorials/04_mnist_benchmark/README.md", str(FREEZE3), "historical verified evidence", "MNIST source must be reverified", "", "benchmarks/mnist/benchmark_config.yaml", sha256(FREEZE3 / "benchmarks" / "mnist" / "benchmark_config.yaml"), "", "", "", "must be recorded on rerun", "not_executed", "", "historical report/outputs identified; no fresh claim", "Chapter 35"])
        writer.writerow(["05_original_idp_reconstruction", "T05-S01", "historical adaptation/rescoring evidence; no fresh model fit", str(FREEZE3), "historical Freeze 3 evidence", "authoritative historical workbook/labels", "see source checksum inventory", "configs/original_idp_164_selected.yaml", sha256(FREEZE3 / "configs" / "original_idp_164_selected.yaml"), "", "", "", "historical settings", "historical_only", "", "164 IDs; noise=102; clusters=9/13/15/14/11; manual row 16", "Chapter 36"])
        writer.writerow(["05_original_idp_reconstruction", "T05-S02", "protocol only; exact templates in tutorials/05_original_idp_reconstruction/README.md", str(FREEZE3), "future Docker environment", "authoritative 164 matrix pending mounted path", "must verify before run", "configs/original_idp_164_historical_search.yaml", sha256(FREEZE3 / "configs" / "original_idp_164_historical_search.yaml"), "", "", "", "1,000 seeds; thread/resource preflight required", "deferred", "", "no fresh labels, metrics, runtime, or validation claimed", "Chapter 36; Docker handoff"])


def artifact_checksums() -> None:
    rows: list[list[Any]] = []
    for path in sorted(MANUAL.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(MANUAL).as_posix()
        if relative.startswith("build/runtime_env/") or relative == "evidence/artifact_checksums.tsv":
            continue
        role = "manual_source"
        if relative.startswith("tutorials/"):
            role = "executed_tutorial"
        elif relative.startswith("build/logs/"):
            role = "execution_log"
        elif relative.startswith("evidence/"):
            role = "evidence_register"
        elif relative.startswith("assets/"):
            role = "manual_asset"
        rows.append([relative, path.stat().st_size, sha256(path), role])
    write_tsv(EVIDENCE / "artifact_checksums.tsv", ["relative_path", "size_bytes", "sha256", "role"], rows)


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    dependencies()
    runtime_environment()
    test_report()
    tutorials()
    artifact_checksums()


if __name__ == "__main__":
    main()
