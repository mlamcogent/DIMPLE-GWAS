from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


PACKAGE_ROOT = Path(__file__).resolve().parents[5]
WORKSPACE_ROOT = PACKAGE_ROOT.parent
QA_ROOT = PACKAGE_ROOT / "docs" / "edition3" / "qa" / "stage1"
GEN_ROOT = QA_ROOT / "generated"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


checks: list[dict[str, object]] = []


def record(check_id: str, passed: bool, observed: object, expected: object) -> None:
    checks.append(
        {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "observed": observed,
            "expected": expected,
        }
    )


junit_path = QA_ROOT / "test_results" / "freeze3_pytest.xml"
record("junit_exists", junit_path.is_file(), str(junit_path.relative_to(PACKAGE_ROOT)), "file exists")

command_files = sorted((QA_ROOT / "logs").glob("*.command.txt"))
statuses: dict[str, int] = {}
for command_file in command_files:
    fields = {}
    for line in command_file.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            fields[key] = value
    statuses[fields.get("name", command_file.stem)] = int(fields.get("exit_status", "-1"))
record("all_logged_commands_exit_zero", bool(statuses) and all(v == 0 for v in statuses.values()), statuses, "all 0")

comparison_path = GEN_ROOT / "fixed_comparison" / "comparison_summary.json"
comparison = json.loads(comparison_path.read_text(encoding="utf-8"))
for key in ("adjusted_rand_index", "normalized_mutual_information", "noise_set_jaccard", "mapped_membership_match_fraction"):
    value = float(comparison[key])
    record(f"fixed_comparison_{key}", np.isclose(value, 1.0), value, 1.0)

validation_path = GEN_ROOT / "fixed_validation" / "validation_report.json"
validation = json.loads(validation_path.read_text(encoding="utf-8"))
record("fixed_validation_passed", validation.get("status") == "pass", validation.get("status"), "pass")

fresh_path = GEN_ROOT / "fresh_rescored_164_models.tsv"
retained_path = WORKSPACE_ROOT / "freeze3_workspace" / "comparisons" / "idp_runs" / "freeze3_rescored_164_models.tsv"
fresh = pd.read_csv(fresh_path, sep="\t")
retained = pd.read_csv(retained_path, sep="\t")
keys = [column for column in ("model_id", "min_cluster_size", "min_samples", "cluster_selection_epsilon") if column in fresh.columns and column in retained.columns]
merged = fresh.merge(retained, on=keys, suffixes=("_fresh", "_retained"), validate="one_to_one")
score_columns = [column for column in ("legacy_score", "fit_score", "score") if f"{column}_fresh" in merged.columns]
if not score_columns:
    score_columns = [column.removesuffix("_fresh") for column in merged.columns if column.endswith("_fresh") and "score" in column]
record("historical_164_row_count", len(fresh) == 333, len(fresh), 333)
record("historical_164_join_count", len(merged) == 333, len(merged), 333)
for column in score_columns:
    delta = np.nanmax(np.abs(merged[f"{column}_fresh"] - merged[f"{column}_retained"]))
    record(f"historical_164_{column}_max_abs_delta", bool(delta <= 1e-12), float(delta), "<=1e-12")

best = json.loads((GEN_ROOT / "fixed_run" / "models" / "best_model.json").read_text(encoding="utf-8"))["model"]
reproduced = json.loads((GEN_ROOT / "fixed_reproduction" / "models" / "best_model.json").read_text(encoding="utf-8"))["model"]
record("fixed_model_id_stable", best["model_id"] == reproduced["model_id"], reproduced["model_id"], best["model_id"])

result = {
    "status": "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL",
    "checks": checks,
    "generated_file_count": sum(1 for path in GEN_ROOT.rglob("*") if path.is_file()),
}
(QA_ROOT / "test_results" / "generated_output_checks.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)

checksum_rows = []
for path in sorted(QA_ROOT.rglob("*")):
    if not path.is_file() or path.name == "generated_checksums.tsv":
        continue
    checksum_rows.append(
        {
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
            "path": path.relative_to(PACKAGE_ROOT).as_posix(),
        }
    )
pd.DataFrame(checksum_rows).to_csv(QA_ROOT / "generated_checksums.tsv", sep="\t", index=False)

print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["status"] == "PASS" else 1)
