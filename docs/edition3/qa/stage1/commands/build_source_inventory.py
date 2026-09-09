from __future__ import annotations

import hashlib
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[5]
WORKSPACE_ROOT = PACKAGE_ROOT.parent
PATH_LIST = Path(__file__).with_name("source_paths.txt")
OUTPUT = PACKAGE_ROOT / "docs" / "edition3" / "evidence" / "00_SOURCE_INVENTORY_AND_CHECKSUMS.tsv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_role(path: str) -> str:
    if path.endswith((".pdf", ".docx")):
        return "supplied_document"
    if "/dimple_gwas/" in path or path.endswith("DIMPLEGWAS.py") or path.endswith("DIMPLEGWAS_1b_sklearnHDBSCan.py"):
        return "implementation"
    if "/tests/" in path:
        return "test"
    if "/configs/" in path or path.endswith("tutorial_config.yaml"):
        return "configuration"
    if "/comparisons/" in path:
        return "retained_analysis_artifact"
    if "/reports/" in path or "review" in path.lower():
        return "prior_audit_or_report"
    if path.endswith(".bib"):
        return "prior_bibliography"
    return "governance_or_package_metadata"


rows = []
for relative in PATH_LIST.read_text(encoding="utf-8").splitlines():
    if not relative.strip():
        continue
    source = WORKSPACE_ROOT / relative
    if not source.is_file():
        raise FileNotFoundError(source)
    rows.append(
        "\t".join(
            (
                relative,
                source_role(relative),
                str(source.stat().st_size),
                sha256(source),
                "verified_present",
            )
        )
    )

header = "workspace_relative_path\tsource_role\tbytes\tsha256\tverification_status\n"
OUTPUT.write_text(header + "\n".join(rows) + "\n", encoding="utf-8")
print(f"wrote {OUTPUT} with {len(rows)} source records")
