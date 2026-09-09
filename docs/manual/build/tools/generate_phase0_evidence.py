#!/usr/bin/env python3
"""Generate Phase-0 evidence inventory and checksum registers for the manual."""

from __future__ import annotations

import csv
import hashlib
import os
import platform
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


WORKSPACE = Path(__file__).resolve().parents[5]
FREEZE3 = WORKSPACE / "DIMPLE-GWAS-freeze3"
MANUAL = FREEZE3 / "docs" / "manual"
EVIDENCE = MANUAL / "evidence"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_text(command: list[str]) -> str:
    try:
        return subprocess.run(command, check=True, text=True, capture_output=True).stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return "unavailable"


def authority_for(path: Path) -> tuple[str, str]:
    relative = path.relative_to(WORKSPACE).as_posix()
    if relative.startswith("DIMPLE-GWAS-freeze3/dimple_gwas/") or relative in {
        "DIMPLE-GWAS-freeze3/pyproject.toml",
        "DIMPLE-GWAS-freeze3/requirements.txt",
    }:
        return "1", "authoritative Freeze 3 executable source or metadata"
    if relative.startswith("DIMPLE-GWAS-freeze3/tests/") or relative.startswith("DIMPLE-GWAS-freeze3/configs/"):
        return "1", "authoritative executable test or configuration"
    if relative.startswith("freeze3_workspace/"):
        return "2", "Freeze 3 run evidence, audit record, or validation artifact"
    if relative.startswith("DIMPLE-GWAS-freeze3/docs/") and "/manual/" not in relative:
        return "3", "Freeze 3 coordinator documentation"
    if relative.startswith("umap-hdbscan/") or relative.startswith("DIMPLE-GWAS-freeze2/"):
        return "4", "historical or compatibility evidence"
    if relative.startswith("Cogent manuscript/"):
        return "5", "manuscript, supplement, reviewer, or editorial source"
    if relative.endswith("DIMPLE-GWAS Methods Research Plan.pdf"):
        return "7", "provisional Gemini research narrative"
    if "reviewer" in relative.lower():
        return "5", "reviewer correspondence or derived action register"
    return "6", "supporting source"


def role_for(path: Path) -> str:
    relative = path.relative_to(WORKSPACE).as_posix().lower()
    if "/tests/" in relative:
        return "test"
    if "/configs/" in relative or relative.endswith(('.yaml', '.yml')):
        return "configuration"
    if relative.endswith(('.py', '.toml')) and relative.startswith("dimple-gwas-freeze3/"):
        return "software"
    if "review" in relative or "correspond" in relative:
        return "review evidence"
    if "manuscript" in relative or "supplement" in relative:
        return "scientific narrative"
    if relative.endswith(('.xlsx', '.xls', '.csv', '.tsv', '.npy', '.json')):
        return "data or run artifact"
    if relative.endswith('.pdf'):
        return "documentary evidence"
    return "documentation or provenance"


def sensitive_for(path: Path) -> str:
    relative = path.relative_to(WORKSPACE).as_posix()
    if relative.startswith("Cogent manuscript/"):
        return "yes - unpublished manuscript/review material"
    if relative.startswith("umap-hdbscan/") and path.suffix.lower() in {".csv", ".tsv", ".xlsx", ".xls"}:
        return "provisional - original scientific artifact"
    return "no known restriction; redistribution still subject to licence review"


def iter_inputs() -> list[Path]:
    selected: list[Path] = []
    roots = [
        FREEZE3 / "dimple_gwas",
        FREEZE3 / "tests",
        FREEZE3 / "configs",
        FREEZE3 / "benchmarks",
        FREEZE3 / "test_data",
        FREEZE3 / "docs",
        WORKSPACE / "freeze3_workspace",
    ]
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if (
                "/docs/manual/" in path.as_posix()
                or "__pycache__" in path.parts
                or ".venv" in path.parts
                or "site-packages" in path.parts
            ):
                continue
            selected.append(path)

    explicit = [
        FREEZE3 / "README.md",
        FREEZE3 / "pyproject.toml",
        FREEZE3 / "requirements.txt",
        WORKSPACE / "DIMPLE_GWAS_FREEZE3_CODEX_TEXTBOOK_MANUAL_BUILD_RUN_MACRO.md",
        WORKSPACE / "DIMPLE-GWAS Methods Research Plan.pdf",
        WORKSPACE / "nature_communications_preliminary_reviewer_2_action_register.md",
        WORKSPACE / "nature_communications_preliminary_reviewer_2_action_register.pdf",
        WORKSPACE / "Cogent manuscript" / "78622_0_merged_pdf_942956_t8sw87.pdf",
        WORKSPACE / "Cogent manuscript" / "Manuscript-draft5_05.25.2026.docx",
        WORKSPACE / "Cogent manuscript" / "Re_ manuscript" / "Supplement-Draft5_05.07.2026.docx",
        WORKSPACE / "Cogent manuscript" / "COGENT-Supplementary-Methods-FactChecker-updated.docx",
        WORKSPACE / "umap-hdbscan" / "final_merged_data_2135_3159_164_08Oct.xlsx",
        WORKSPACE / "umap-hdbscan" / "IDP-Results-Summary.xlsx",
    ]
    selected.extend(path for path in explicit if path.exists())
    return sorted(set(selected), key=lambda item: item.as_posix())


def write_tsv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    now = datetime.now(ZoneInfo("Asia/Singapore"))
    usage = shutil.disk_usage(WORKSPACE)
    files = iter_inputs()

    inventory_rows: list[list[object]] = []
    checksum_rows: list[list[object]] = []
    for path in files:
        stat = path.stat()
        authority, authority_note = authority_for(path)
        digest = sha256(path)
        relative = path.relative_to(WORKSPACE).as_posix()
        inventory_rows.append(
            [
                relative,
                path.suffix.lower().lstrip(".") or "none",
                role_for(path),
                stat.st_size,
                datetime.fromtimestamp(stat.st_mtime, ZoneInfo("Asia/Singapore")).isoformat(),
                digest,
                authority,
                authority_note,
                sensitive_for(path),
            ]
        )
        checksum_rows.append([relative, stat.st_size, digest])

    write_tsv(
        EVIDENCE / "01_input_inventory.tsv",
        ["path", "type", "role", "size_bytes", "modified_sgt", "sha256", "authority_level", "authority_note", "sensitivity"],
        inventory_rows,
    )
    write_tsv(EVIDENCE / "04_source_checksums.tsv", ["path", "size_bytes", "sha256"], checksum_rows)

    conflicts = [
        ["AUTH-001", "Repository commit", "No usable Git metadata exists at the workspace or Freeze 3 source root.", "Use file checksums as the immutable identity record; report commit as unavailable.", "resolved_with_limitation", "1"],
        ["AUTH-002", "Manuscript authority", "Several dated manuscript/supplement drafts coexist.", "Treat submitted merged PDF as submitted record; use 2026-05-25 manuscript and 2026-05-07 supplement as editable contextual sources; mark choice provisional.", "resolved_with_qualification", "5"],
        ["SCI-001", "164-IDP fresh rerun", "Historical artifacts are reconstructed but the 1,000-seed fit has not been freshly executed.", "Defer to Docker phase per coordinator direction; provide exact local/container protocol and retain pending release gate.", "resolved_with_limitation", "2"],
        ["SCI-002", "459-IDP parameters", "Notebook and manuscript evidence disagree and the raw matrix/model table are absent.", "Do not claim fresh reproduction; retain historical-only status.", "unresolved", "4"],
        ["DOC-001", "Extended search count", "Older Freeze 2 prose says 5,184; Freeze 3 code/config enumerate 1,728.", "Use executed Freeze 3 count of 1,728 and identify older value as a documentation defect.", "resolved", "1"],
        ["CIT-001", "Zhang/Yang/Zhao reviewer attribution", "Gemini dossier attributes genomic PCA/ICA literature collectively to Zhang, Yang, and Zhao without exact reviewer-source mapping.", "Verify identifiable primary works individually; do not describe them as reviewer-cited unless present in correspondence.", "unresolved_attribution", "5/6/7"],
    ]
    write_tsv(
        EVIDENCE / "02_authority_and_conflict_map.tsv",
        ["conflict_id", "topic", "conflict", "resolution_rule", "status", "controlling_authority"],
        conflicts,
    )

    missing = [
        ["MISS-001", "Git commit/tag metadata", "required for commit-level release identity", "Checksum manifest substitutes for this draft; Docker packaging should establish a versioned source identity.", "high", "open"],
        ["MISS-002", "Fresh full 164-IDP 1,000-seed execution", "scientific-freeze and fresh-reproduction claim", "Deferred until Docker by coordinator; exact protocol included.", "high", "deferred"],
        ["MISS-003", "Original 2,315-IDP raw matrix", "fresh primary-analysis reproduction", "Historical outputs only; no rerun claim.", "high", "open"],
        ["MISS-004", "Original 459-IDP raw matrix and unambiguous parameters", "fresh secondary-analysis reproduction", "Historical outputs only; resolve against original run directory/log.", "high", "open"],
        ["MISS-005", "Complete final editorial decision and remaining reviewer reports", "journal-response crosswalk", "Current textbook incorporates only materials present on build date.", "medium", "open"],
        ["MISS-006", "Cross-platform Docker/GCP/AWS validation", "container/cloud reproducibility claims", "Explicitly out of scope; handoff supplied.", "high", "deferred"],
    ]
    write_tsv(
        EVIDENCE / "03_missing_evidence_register.tsv",
        ["gap_id", "missing_evidence", "affected_claim_or_task", "bounded_handling", "priority", "status"],
        missing,
    )

    environment = f"""# Environment and repository snapshot

- Recorded: `{now.isoformat()}`
- Workspace: `{WORKSPACE}`
- Authoritative source tree: `{FREEZE3}`
- Operating system: `{platform.platform()}`
- Architecture: `{platform.machine()}`
- Build Python: `{platform.python_version()}`
- macOS system Python: `{run_text(['/usr/bin/python3', '--version'])}`
- Validated/bundled Python: `{run_text(['/Users/maxlam/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3', '--version'])}`
- Timezone: `Asia/Singapore`
- Storage: `{usage.free / (1024**3):.1f} GiB free of {usage.total / (1024**3):.1f} GiB`
- Package version: `3.0.0rc1` (from `pyproject.toml`)
- Git identity: unavailable; no usable Git metadata is present. File checksums are the identity record for this build.
- Existing Freeze 3 resource note: prior evidence records a 16 GB host and warns against unrestricted parallel UMAP fitting.
- Fresh 164-IDP full run: deliberately deferred until Docker packaging per coordinator direction.
- Docker/cloud scope: no Dockerfile, image, registry, GCP, or AWS action is performed by this documentation build.

## Repository state

The source and evidence trees are treated as an immutable scientific record. The manual build writes only under `DIMPLE-GWAS-freeze3/docs/manual/` and uniquely named tutorial output roots. Original inputs, manuscripts, reviewer files, historical outputs, and prior run evidence are not modified.

## Inventory result

The Phase-0 inventory records {len(files)} selected authoritative or supporting inputs. See `01_input_inventory.tsv`, `02_authority_and_conflict_map.tsv`, `03_missing_evidence_register.tsv`, and `04_source_checksums.tsv`.
"""
    (EVIDENCE / "00_environment_and_repository_snapshot.md").write_text(environment, encoding="utf-8")


if __name__ == "__main__":
    main()
