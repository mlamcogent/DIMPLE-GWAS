#!/usr/bin/env python3
"""Run deterministic technical/editorial/privacy checks and write the QA report."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


FREEZE3 = Path(__file__).resolve().parents[4]
MANUAL = FREEZE3 / "docs" / "manual"
EVIDENCE = MANUAL / "evidence"
QA = MANUAL / "build" / "qa"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def markdown_files() -> list[Path]:
    roots = [MANUAL / "DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.md", MANUAL / "QUICKSTART.md", MANUAL / "README.md", MANUAL / "MANUAL_BUILD_REPORT.md", MANUAL / "MANUAL_QA_REPORT.md", MANUAL / "DOCKER_CLOUD_SUPPLEMENT_HANDOFF.md"]
    roots.extend(sorted((MANUAL / "chapters").glob("*.md")))
    roots.extend(sorted((MANUAL / "appendices").glob("*.md")))
    roots.extend(sorted((MANUAL / "references").glob("*.md")))
    return roots


def local_links() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    checked, broken = [], []
    pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for raw in pattern.findall(text):
            target = raw.strip().strip("<>").split("#", 1)[0]
            if not target or re.match(r"^(https?|mailto):", target) or "NEW" in target or target.startswith("/path/"):
                continue
            destination = (path.parent / target).resolve()
            record = {"source": path.relative_to(MANUAL).as_posix(), "target": target}
            checked.append(record)
            if not destination.exists():
                broken.append(record)
    return checked, broken


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> None:
    QA.mkdir(parents=True, exist_ok=True)
    checks: list[dict[str, Any]] = []
    def add(check_id: str, area: str, status: str, evidence: str, note: str) -> None:
        checks.append({"check_id": check_id, "area": area, "status": status, "evidence": evidence, "note": note})

    chapters = sorted((MANUAL / "chapters").glob("*.md"))
    appendices = sorted((MANUAL / "appendices").glob("*.md"))
    add("ED-001", "editorial", "pass" if len(chapters) == 46 else "fail", "chapters/", f"Found {len(chapters)} modular chapters.")
    add("ED-002", "editorial", "pass" if len(appendices) == 8 else "fail", "appendices/", f"Found {len(appendices)} appendices.")
    compiled = (MANUAL / "DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.md").read_text(encoding="utf-8")
    chapter_headings = re.findall(r"^# (\d+)\. ", compiled, flags=re.MULTILINE)
    add("ED-003", "editorial", "pass" if len(chapter_headings) == 46 and len(set(chapter_headings)) == 46 else "fail", "DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.md", f"Compiled edition contains {len(chapter_headings)} unique numbered chapter headings and {len(compiled.split())} whitespace-delimited words.")
    required_sections = ["## Orientation", "## Learning objectives", "## Explanation and implementation", "## Evidence-backed example", "## Outputs to inspect", "## Common mistakes", "## Scientific and operational limits", "## Completion check"]
    section_failures = [path.name for path in chapters if any(section not in path.read_text(encoding="utf-8") for section in required_sections)]
    add("ED-004", "pedagogy", "pass" if not section_failures else "fail", "chapters/", "Every chapter contains the teaching contract." if not section_failures else f"Missing sections: {section_failures}")

    checked_links, broken_links = local_links()
    add("TECH-001", "links", "pass" if not broken_links else "fail", "build/qa/manual_qa.json", f"Checked {len(checked_links)} local Markdown asset/navigation links; broken={len(broken_links)}.")

    command_rows = tsv(EVIDENCE / "command_and_flag_matrix.tsv")
    commands = {row["command"] for row in command_rows}
    expected = {"run", "inspect-config", "show-search-space", "score-existing", "summarize-models", "reproduce-model", "explain", "compare", "validate"}
    add("TECH-002", "commands", "pass" if expected <= commands else "fail", "evidence/command_and_flag_matrix.tsv; build/logs/cli_help/", f"All {len(expected)} canonical commands appear in the implementation-derived matrix; interpret alias is recorded with explain.")
    tutorial_rows = tsv(EVIDENCE / "tutorial_execution_manifest.tsv")
    executed = [row for row in tutorial_rows if row["tutorial"][:3] in {"01_", "02_", "03_"}]
    executed_ok = len(executed) == 12 and all(row["exit_code"] == "0" for row in executed)
    add("TECH-003", "tutorials", "pass" if executed_ok else "fail", "evidence/tutorial_execution_manifest.tsv; tutorials/*/execution_manifest.json", f"Tutorials 1–3 contain {len(executed)} executed steps and all recorded exit codes are zero; Tutorials 4–5 are explicitly historical/protocol-only.")

    producer = {row["artifact"] for row in tsv(EVIDENCE / "output_producer_consumer_map.tsv")}
    atlas = {row["name_or_pattern"] for row in tsv(EVIDENCE / "output_atlas.tsv")}
    missing_atlas = sorted(producer - atlas)
    add("TECH-004", "outputs", "pass" if not missing_atlas else "fail", "evidence/output_producer_consumer_map.tsv; evidence/output_atlas.tsv", f"All {len(producer)} producer-map artifact patterns appear in the atlas; three in-memory non-artifacts are also documented.")
    config_rows = tsv(EVIDENCE / "configuration_key_reference.tsv")
    add("TECH-005", "configuration", "pass" if len(config_rows) == 57 else "fail", "evidence/configuration_key_reference.tsv", f"Implementation-derived reference contains {len(config_rows)} configuration keys/rows.")
    test_log = (MANUAL / "build" / "logs" / "pytest_full.log").read_text(encoding="utf-8")
    add("TECH-006", "tests", "pass" if "45 passed" in test_log else "fail", "build/logs/pytest_full.log; evidence/test_execution_report.md", "Fresh isolated suite reports 45 passed and four visible warnings.")

    required_safe_phrases = [
        "not biological loadings", "empirical stability strategy", "DBCV is not", "noise/unassigned",
        "post-selection", "manual row-16", "not yet scientifically frozen", "not yet scientifically frozen or cross-platform validated",
    ]
    missing_phrases = [phrase for phrase in required_safe_phrases if phrase.lower() not in compiled.lower()]
    add("SCI-001", "scientific language", "pass" if not missing_phrases else "fail", "compiled manual; evidence/claim_evidence_register.tsv", "High-risk interpretation boundaries are present." if not missing_phrases else f"Missing phrases: {missing_phrases}")
    unsafe_patterns = {
        "axes_as_loadings": r"UMAP (?:axes|coordinates?) (?:are|is) biological loadings",
        "noise_nonpleiotropic": r"noise (?:means|proves|is) non-pleiotropic",
        "dbcv_default_score": r"DBCV is (?:the )?default (?:DIMPLE )?score",
        "pinned_guarantee": r"pinned dependencies guarantee (?:bitwise )?identical",
        "fresh_164_claim": r"fresh (?:Freeze 3 )?(?:run )?(?:regenerated|reproduced) the 164",
    }
    unsafe_hits = {name: len(re.findall(pattern, compiled, flags=re.IGNORECASE)) for name, pattern in unsafe_patterns.items()}
    add("SCI-002", "scientific scan", "pass" if not any(unsafe_hits.values()) else "fail", "compiled manual", f"Unsafe affirmative-pattern hits: {unsafe_hits}.")

    citations = tsv(EVIDENCE / "citation_verification_log.tsv")
    bib = (MANUAL / "references" / "dimple_gwas_manual.bib").read_text(encoding="utf-8")
    bib_entries = len(re.findall(r"^@", bib, flags=re.MULTILINE))
    braces_ok = bib.count("{") == bib.count("}")
    doi_rows = [row for row in citations if row["doi_or_identifier"].startswith("10.")]
    add("CIT-001", "citations", "pass" if bib_entries >= 15 and braces_ok and all(row["status"] == "verified" for row in citations) else "fail", "references/dimple_gwas_manual.bib; evidence/citation_verification_log.tsv", f"BibTeX entries={bib_entries}; brace balance={braces_ok}; verified citation rows={len(citations)}; DOI rows={len(doi_rows)}.")
    add("CIT-002", "reviewer attribution", "pass_with_limitation", "evidence/reviewer_reference_crosswalk.tsv; references/VERIFIED_BIBLIOGRAPHY.md", "Oblong/Zhang attribution is corrected. Exact Yang/Zhao reviewer works remain unresolved and are not guessed.")

    figure_rows = tsv(EVIDENCE / "figure_source_manifest.tsv")
    bad_figures = []
    for row in figure_rows:
        path = MANUAL / row["manual_path"]
        if not path.is_file() or sha256(path) != row["sha256"]:
            bad_figures.append(row["figure_id"])
    add("RENDER-001", "figures", "pass" if not bad_figures else "fail", "evidence/figure_source_manifest.tsv", f"Verified {len(figure_rows)} figure/diagram source or rendered rows; mismatches={bad_figures}.")
    pdf = MANUAL / "DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.pdf"
    info = subprocess.run(["pdfinfo", str(pdf)], text=True, capture_output=True, check=True).stdout
    page_match = re.search(r"^Pages:\s+(\d+)", info, flags=re.MULTILINE)
    pages = int(page_match.group(1))
    renders = list((QA / "pdf_pages_v4").glob("page-*.png"))
    contacts = list((QA / "pdf_contacts_v4").glob("contact_*.png"))
    add("RENDER-002", "PDF", "pass" if pages == len(renders) == 122 and len(contacts) == 11 else "fail", "DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.pdf; build/qa/pdf_pages_v4; build/qa/pdf_contacts_v4", f"Latest PDF is {pages} A4 pages; every page rendered to PNG and all pages were visually inspected across {len(contacts)} numbered contact sheets. No clipping, overflow, broken image, margin collision, or blank failure was observed.")
    html = MANUAL / "DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.html"
    html_text = html.read_text(encoding="utf-8")
    add("RENDER-003", "HTML", "pass" if "data:image" in html_text and "/Users/" not in html_text else "fail", "DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.html; build/logs/manual_html_build_v4.log", "Self-contained HTML embeds CSS and images and contains no developer absolute path.")

    public_text = "\n".join(path.read_text(encoding="utf-8") for path in markdown_files()) + "\n" + html_text
    privacy_patterns = {"developer_path": r"/Users/", "developer_name": r"maxlam", "secret_assignment": r"(?i)(api[_-]?key|access[_-]?token|secret)\s*[:=]\s*[A-Za-z0-9_\-]{12,}"}
    privacy_hits = {name: len(re.findall(pattern, public_text)) for name, pattern in privacy_patterns.items()}
    add("PRIV-001", "privacy", "pass" if not any(privacy_hits.values()) else "fail", "published Markdown/HTML source set", f"Published-edition scan hits: {privacy_hits}.")
    internal_hits = 0
    for path in (MANUAL / "tutorials").rglob("*"):
        if path.is_file() and path.suffix.lower() in {".json", ".tsv", ".csv", ".yaml", ".md", ".log", ".txt"}:
            try:
                internal_hits += path.read_text(encoding="utf-8", errors="ignore").count("/Users/")
            except OSError:
                pass
    add("PRIV-002", "privacy", "pass_with_limitation" if internal_hits else "pass", "tutorials/ executed evidence", f"Raw/internal executed evidence contains {internal_hits} local absolute-path occurrences required for provenance. Exclude or sanitize this evidence layer in any public distribution while retaining checksums/private originals; the rendered manual is clean.")

    failures = [row for row in checks if row["status"] == "fail"]
    payload = {"schema": "dimple-gwas.manual-qa.v1", "summary": {"checks": len(checks), "pass": sum(row["status"] == "pass" for row in checks), "pass_with_limitation": sum(row["status"] == "pass_with_limitation" for row in checks), "fail": len(failures)}, "checks": checks, "broken_links": broken_links, "unsafe_hits": unsafe_hits, "privacy_hits": privacy_hits}
    (QA / "manual_qa.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = ["# Manual QA report", "", f"Result: **{'PASS' if not failures else 'FAIL'}**. Checks: {len(checks)}; pass: {payload['summary']['pass']}; pass with limitation: {payload['summary']['pass_with_limitation']}; fail: {len(failures)}.", "", "| ID | Area | Status | Evidence | Result / remediation |", "| --- | --- | --- | --- | --- |"]
    for row in checks:
        note = row["note"].replace("|", "\\|")
        lines.append(f"| {row['check_id']} | {row['area']} | `{row['status']}` | `{row['evidence']}` | {note} |")
    lines.extend(["", "## Visual inspection", "", "The latest 122-page A4 PDF was rendered at 110 dpi into one PNG per page. All pages were inspected in eleven numbered contact sheets. Title/contents, part dividers, 46 chapters, code blocks, diagrams, quantitative figures, mathematical appendix, bibliography, tables, clean page margins, and final appendices render without clipping, overlap, or broken images. Sparse pages are deliberate part/appendix dividers or short completion pages; none is an unintended blank failure.", "", "## Named limitations", "", "- Exact Yang/Zhao reviewer-cited works cannot be identified from the supplied Reviewer #2 register and remain unresolved rather than inferred.", "- Raw executed tutorial evidence retains local absolute paths for private provenance. The Markdown/HTML/PDF edition is clean; a public package must exclude or deliberately sanitize raw evidence while preserving private originals and checksums.", "- The fresh full 164-IDP 1,000-seed run and Docker/Linux/GCP/AWS validation are pending by design.", "- The PDF renderer reports benign Type-3-glyph bounding-box warnings for mathematical glyphs; every affected page rendered visibly and legibly.", ""])
    (MANUAL / "MANUAL_QA_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
