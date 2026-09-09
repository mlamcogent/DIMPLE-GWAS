from __future__ import annotations

import csv
import json
import re
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[5]
EVIDENCE = PACKAGE_ROOT / "docs" / "edition3" / "evidence"
QA_ROOT = PACKAGE_ROOT / "docs" / "edition3" / "qa" / "stage1"

REQUIRED = [
    "00_SOURCE_INVENTORY_AND_CHECKSUMS.tsv",
    "01_AUTHORITY_LINEAGE_AND_RELEASE_BOUNDARY.md",
    "02_IMPLEMENTATION_TRUTH_REGISTER.tsv",
    "03_VERIFIED_METHODS_AND_EDUCATIONAL_EVIDENCE_DOSSIER.md",
    "04_PRIOR_REPORT_CLAIM_AUDIT.tsv",
    "05_CLAIM_EVIDENCE_REGISTER.tsv",
    "06_VERIFIED_BIBLIOGRAPHY.bib",
    "07_REVIEWER_LITERATURE_CROSSWALK.md",
    "08_ANALYSIS_HIERARCHY_AND_GOLDEN_RUNS.md",
    "09_FUNCTION_CONCEPT_OUTPUT_COVERAGE.tsv",
    "10_TUTORIAL_EXECUTION_BASELINE.md",
    "11_SAFE_LANGUAGE_AND_MISCONCEPTION_REGISTER.tsv",
    "12_UNRESOLVED_EVIDENCE_GAPS.md",
    "13_STAGE1_GATE_REPORT.md",
    "STAGE1_MANIFEST.json",
]

checks: list[dict[str, object]] = []


def add(check_id: str, passed: bool, observed: object, expected: object) -> None:
    checks.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "observed": observed, "expected": expected})


for name in REQUIRED:
    path = EVIDENCE / name
    add(f"required:{name}", path.is_file() and path.stat().st_size > 0, path.stat().st_size if path.exists() else None, "nonempty file")

for path in sorted(EVIDENCE.glob("*.tsv")):
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle, delimiter="\t"))
    width = len(rows[0]) if rows else 0
    bad = [index + 1 for index, row in enumerate(rows) if len(row) != width]
    add(f"tsv_rectangular:{path.name}", not bad and width > 1, {"rows": len(rows), "columns": width, "bad_rows": bad}, "all rows match header width")
    identifiers = [row[0] for row in rows[1:] if row]
    add(f"tsv_ids_unique:{path.name}", len(identifiers) == len(set(identifiers)), len(identifiers) - len(set(identifiers)), 0)

bib_text = (EVIDENCE / "06_VERIFIED_BIBLIOGRAPHY.bib").read_text(encoding="utf-8")
bib_keys = re.findall(r"^@[A-Za-z]+\{([^,]+),", bib_text, flags=re.MULTILINE)
dois = [value.lower() for value in re.findall(r"doi\s*=\s*\{([^}]+)\}", bib_text, flags=re.IGNORECASE)]
add("bibliography_entry_count", len(bib_keys) >= 35, len(bib_keys), ">=35")
add("bibliography_keys_unique", len(bib_keys) == len(set(bib_keys)), len(bib_keys) - len(set(bib_keys)), 0)
add("bibliography_dois_unique", len(dois) == len(set(dois)), len(dois) - len(set(dois)), 0)

gate_text = (EVIDENCE / "13_STAGE1_GATE_REPORT.md").read_text(encoding="utf-8")
add("single_gate_decision", gate_text.count("PASS_WITH_LIMITATIONS") == 1, gate_text.count("PASS_WITH_LIMITATIONS"), 1)
gate_rows = re.findall(r"^\| G(?:[1-9]|1[0-2]) \|", gate_text, flags=re.MULTILINE)
add("twelve_gate_rows", len(gate_rows) == 12, len(gate_rows), 12)

manifest = json.loads((EVIDENCE / "STAGE1_MANIFEST.json").read_text(encoding="utf-8"))
add("manifest_decision", manifest.get("decision") == "PASS_WITH_LIMITATIONS", manifest.get("decision"), "PASS_WITH_LIMITATIONS")
add("manifest_gate_count", len(manifest.get("gate_results", {})) == 12, len(manifest.get("gate_results", {})), 12)
add("manifest_gap_count", len(manifest.get("unresolved_gap_ids", [])) == 18, len(manifest.get("unresolved_gap_ids", [])), 18)
add("manifest_source_count", manifest.get("source_identity", {}).get("source_inventory_record_count") == 91, manifest.get("source_identity", {}).get("source_inventory_record_count"), 91)

dossier_text = (EVIDENCE / "03_VERIFIED_METHODS_AND_EDUCATIONAL_EVIDENCE_DOSSIER.md").read_text(encoding="utf-8")
domain_headings = re.findall(r"^## (?:[1-9]|1[0-4])\. ", dossier_text, flags=re.MULTILINE)
add("fourteen_dossier_domains", len(domain_headings) == 14, len(domain_headings), 14)

inventory_path = EVIDENCE / "00_SOURCE_INVENTORY_AND_CHECKSUMS.tsv"
with inventory_path.open(encoding="utf-8", newline="") as handle:
    inventory_rows = list(csv.DictReader(handle, delimiter="\t"))
add("source_inventory_count", len(inventory_rows) >= 80, len(inventory_rows), ">=80")
add("source_hash_format", all(re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) for row in inventory_rows), "all" if inventory_rows else "none", "all 64-char lowercase hex")

absolute_hits = []
secret_hits = []
for path in sorted(EVIDENCE.glob("*")):
    if not path.is_file():
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    if "/Users/" in text:
        absolute_hits.append(path.name)
    if re.search(r"(?i)(api[_-]?key|secret|token|password)\s*[=:]\s*[A-Za-z0-9_-]{12,}", text):
        secret_hits.append(path.name)
add("publishable_evidence_has_no_absolute_user_paths", not absolute_hits, absolute_hits, [])
add("publishable_evidence_has_no_secret_patterns", not secret_hits, secret_hits, [])

result = {
    "status": "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL",
    "checks": checks,
    "required_file_count": len(REQUIRED),
}
output = QA_ROOT / "test_results" / "evidence_pack_validation.json"
output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["status"] == "PASS" else 1)
