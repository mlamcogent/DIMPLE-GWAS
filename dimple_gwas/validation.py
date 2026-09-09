"""Contract and checksum validation for completed DIMPLE-GWAS run directories."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

from .io import atomic_json_dump, ensure_empty_output_dir, json_safe, read_model_table, read_table
from .provenance import base_manifest, file_record, sha256_file, utc_now


def run_validation(
    run_dir: str | Path,
    output_dir: str | Path | None = None,
    *,
    command: list[str] | None = None,
) -> dict[str, Any]:
    import pandas as pd
    import yaml

    started = time.perf_counter()
    root = Path(run_dir)
    if not root.is_dir():
        raise FileNotFoundError(f"Run directory not found: {root}")
    destination = ensure_empty_output_dir(output_dir or (root / "validation"))
    checks: list[dict[str, str]] = []

    def record(check: str, status: str, detail: str) -> None:
        checks.append({"check": check, "status": status, "detail": detail})

    required = [
        "resolved_config.yaml", "search_space_manifest.tsv", "search_space_manifest.json",
        "models/all_models.tsv", "models/ranked_models.tsv", "models/top_models.tsv",
        "models/model_selection_manifest.json", "run_manifest.json",
    ]
    for relative in required:
        path = root / relative
        record(f"required:{relative}", "pass" if path.is_file() else "fail", str(path))

    run_manifest: dict[str, Any] = {}
    manifest_path = root / "run_manifest.json"
    if manifest_path.is_file():
        try:
            run_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            record("run_manifest_json", "pass", "valid JSON")
        except Exception as exc:
            record("run_manifest_json", "fail", f"{type(exc).__name__}: {exc}")
    if (root / "resolved_config.yaml").is_file():
        try:
            config = yaml.safe_load((root / "resolved_config.yaml").read_text(encoding="utf-8"))
            record("resolved_config_yaml", "pass" if isinstance(config, dict) else "fail", "mapping expected")
        except Exception as exc:
            record("resolved_config_yaml", "fail", f"{type(exc).__name__}: {exc}")

    table_count = json_count = None
    try:
        table_count = len(read_table(root / "search_space_manifest.tsv"))
        record("search_space_tsv_readable", "pass", f"rows={table_count}")
    except Exception as exc:
        record("search_space_tsv_readable", "fail", f"{type(exc).__name__}: {exc}")
    try:
        search_payload = json.loads((root / "search_space_manifest.json").read_text(encoding="utf-8"))
        json_count = int(search_payload["candidate_models"])
        record("search_space_json_readable", "pass", f"candidate_models={json_count}")
    except Exception as exc:
        record("search_space_json_readable", "fail", f"{type(exc).__name__}: {exc}")
    if table_count is not None and json_count is not None:
        record(
            "search_space_counts_equal", "pass" if table_count == json_count else "fail",
            f"tsv={table_count}; json={json_count}",
        )

    ranked = top = None
    try:
        ranked = read_model_table(root / "models/ranked_models.tsv")
        required_columns = {"model_id", "status", "rank", "score"}
        missing = sorted(required_columns - set(ranked.columns))
        record("ranked_model_schema", "pass" if not missing else "fail", f"missing={missing}")
    except Exception as exc:
        record("ranked_model_schema", "fail", f"{type(exc).__name__}: {exc}")
    try:
        top = read_model_table(root / "models/top_models.tsv")
        record("top_models_readable", "pass", f"rows={len(top)}")
    except Exception as exc:
        record("top_models_readable", "fail", f"{type(exc).__name__}: {exc}")

    selected = run_manifest.get("selected_model")
    if selected:
        model_root = root / "models/top_model_artifacts" / str(selected)
        summary_path = model_root / "summary.json"
        labels_path = model_root / "labels.tsv"
        record("selected_model_summary", "pass" if summary_path.is_file() else "fail", str(summary_path))
        record("selected_model_labels", "pass" if labels_path.is_file() else "fail", str(labels_path))
        if summary_path.is_file() and labels_path.is_file():
            try:
                summary = json.loads(summary_path.read_text(encoding="utf-8"))
                expected = summary.get("labels_sha256")
                status = "pass" if not expected or expected == sha256_file(labels_path) else "fail"
                record("selected_labels_hash", status, "recorded hash matches" if status == "pass" else "hash mismatch")
            except Exception as exc:
                record("selected_model_summary_json", "fail", f"{type(exc).__name__}: {exc}")
    else:
        record("selected_model_declared", "warn", "run has no selected model")

    artifacts = run_manifest.get("artifacts", {}) if isinstance(run_manifest, dict) else {}
    for name, value in artifacts.items():
        if isinstance(value, dict):
            artifact_path = Path(value.get("path", ""))
            expected = value.get("sha256")
        else:
            artifact_path = Path(str(value))
            expected = None
        if not artifact_path.is_absolute():
            artifact_path = root / artifact_path
        if not artifact_path.is_file():
            record(f"artifact:{name}", "fail", f"missing {artifact_path}")
        elif expected and sha256_file(artifact_path) != expected:
            record(f"artifact:{name}", "fail", "SHA-256 mismatch")
        else:
            record(f"artifact:{name}", "pass", str(artifact_path))

    frame = pd.DataFrame(checks)
    frame.to_csv(destination / "validation_checks.tsv", sep="\t", index=False)
    failures = int(frame["status"].eq("fail").sum())
    warnings = int(frame["status"].eq("warn").sum())
    report = {
        "validation_schema": "dimple-gwas.validation.v3",
        "status": "pass" if failures == 0 else "fail",
        "run_dir": str(root.resolve()),
        "checks": int(len(frame)),
        "passed": int(frame["status"].eq("pass").sum()),
        "warnings": warnings,
        "failures": failures,
    }
    atomic_json_dump(json_safe(report), destination / "validation_report.json")
    manifest = base_manifest(command or sys.argv)
    manifest.update({
        "manifest_schema": "dimple-gwas.validation-manifest.v3",
        "status": "complete",
        "finished_at_utc": utc_now(),
        "runtime_seconds": time.perf_counter() - started,
        "validated_run_manifest": file_record(manifest_path) if manifest_path.is_file() else None,
        "result": report,
        "artifacts": {
            "checks": file_record(destination / "validation_checks.tsv"),
            "report": file_record(destination / "validation_report.json"),
        },
    })
    atomic_json_dump(json_safe(manifest), destination / "validation_manifest.json")
    return report
