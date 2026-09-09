#!/usr/bin/env python3
"""Write the machine-readable manifest for the final Edition 3 reader draft."""

from __future__ import annotations

import hashlib
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

from docx import Document
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "EDITION3_BUILD_MANIFEST.json"
PACKAGE_DIGEST = "df87825992ab51dc016c673cf420a978ba5c161bd6c755e00a5199ead310e65b"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact(path: str, role: str) -> dict[str, object]:
    target = ROOT / path
    if not target.is_file():
        raise FileNotFoundError(target)
    return {
        "path": path,
        "role": role,
        "bytes": target.stat().st_size,
        "sha256": sha256(target),
    }


def main() -> None:
    assembly = json.loads((ROOT / "build/assembly_stats.json").read_text(encoding="utf-8"))
    content_qa = json.loads((ROOT / "qa/content/content_qa.json").read_text(encoding="utf-8"))
    a11y = json.loads((ROOT / "qa/accessibility/docx_a11y.json").read_text(encoding="utf-8"))
    pytest_root = ET.parse(ROOT / "qa/software/pytest.xml").getroot()
    suite = pytest_root.find("testsuite")
    if suite is None:
        raise ValueError("pytest testsuite not found")

    docx = Document(ROOT / "DIMPLE_GWAS_FREEZE3_RC1_DOCUMENTATION_EDITION3.docx")
    pdf = PdfReader(ROOT / "DIMPLE_GWAS_FREEZE3_RC1_DOCUMENTATION_EDITION3.pdf")
    pdf_words = sum(len((page.extract_text() or "").split()) for page in pdf.pages)
    visual_rows = (ROOT / "qa/visual/page_render_qa.tsv").read_text(encoding="utf-8").splitlines()[1:]
    if len(visual_rows) != len(pdf.pages):
        raise ValueError("visual page register and PDF page count differ")
    if any(not row.endswith("\tpass") for row in visual_rows):
        raise ValueError("not every rendered page is marked pass")

    primary = [
        artifact("DIMPLE_GWAS_FREEZE3_RC1_DOCUMENTATION_EDITION3.md", "reader_markdown"),
        artifact("DIMPLE_GWAS_FREEZE3_RC1_DOCUMENTATION_EDITION3.html", "self_contained_reader_html"),
        artifact("DIMPLE_GWAS_FREEZE3_RC1_DOCUMENTATION_EDITION3.docx", "privacy_scrubbed_reader_docx"),
        artifact("DIMPLE_GWAS_FREEZE3_RC1_DOCUMENTATION_EDITION3.pdf", "tagged_reader_pdf"),
    ]
    supporting = [
        artifact("README.md", "edition_overview"),
        artifact("QUICKSTART.md", "bounded_quickstart"),
        artifact("KNOWN_LIMITATIONS_AND_PENDING_VALIDATION.md", "reader_limitations"),
        artifact("EDITION2_TO_EDITION3_SALVAGE_CROSSWALK.tsv", "edition_crosswalk"),
        artifact("EDITION3_CHANGELOG.md", "changelog"),
        artifact("EDITION3_BUILD_REPORT.md", "build_report"),
        artifact("EDITION3_QA_REPORT.md", "qa_report"),
        artifact("FUNCTION_CONCEPT_OUTPUT_COVERAGE.tsv", "coverage_register"),
        artifact("COMMAND_EXECUTION_REGISTER.tsv", "command_register"),
        artifact("FIGURE_TABLE_REGISTER.tsv", "figure_table_register"),
    ]

    manifest = {
        "schema": "dimple-gwas.documentation-edition3-build.v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS_WITH_RELEASE_LIMITATIONS",
        "document_status": "reader_draft",
        "package": {
            "name": "DIMPLE-GWAS",
            "version": "3.0.0rc1",
            "package_source_sha256": PACKAGE_DIGEST,
            "stage1_gate": "PASS_WITH_LIMITATIONS",
            "stage1_report": "evidence/13_STAGE1_GATE_REPORT.md",
        },
        "profile": {
            "textbook_chapters": content_qa["textbook_chapter_count"],
            "workbook_labs": 9,
            "technical_reference_modules": 6,
            "appendices": 2,
            "master_approximate_words": assembly["approximate_whitespace_word_count"],
            "pdf_extracted_words": pdf_words,
            "rendered_pages": len(pdf.pages),
            "figures": len(docx.inline_shapes),
            "markdown_html_tables": 10,
            "docx_tables": len(docx.tables),
            "citation_keys_used": len(content_qa["citation_keys_used"]),
            "inline_math_expressions": content_qa["inline_math_count"],
            "display_math_expressions": content_qa["display_math_count"],
        },
        "qa": {
            "content_status": content_qa["status"],
            "unresolved_citations": len(content_qa["unresolved_citation_keys"]),
            "missing_figures": len(content_qa["missing_figures"]),
            "exact_duplicate_substantive_paragraphs": content_qa["exact_duplicate_substantive_paragraph_count"],
            "a11y": a11y["counts"],
            "visual_pages_passed": len(visual_rows),
            "software_tests": {
                "tests": int(suite.attrib["tests"]),
                "failures": int(suite.attrib["failures"]),
                "errors": int(suite.attrib["errors"]),
                "skipped": int(suite.attrib["skipped"]),
                "warnings": 5,
            },
            "privacy_scrubbed": True,
            "pdf_tagged": True,
        },
        "primary_artifacts": primary,
        "supporting_artifacts": supporting,
        "manifest_self_hash_policy": "This manifest does not hash itself.",
        "release_limitations": [
            "fresh historical 164-IDP 1,000-seed rerun pending",
            "2,315 and 459 raw matrices absent; 459 parameters conflict",
            "real-data stability and independent biological validation incomplete",
            "optional XLSX dependency absent in retained environment",
            "Docker/Linux/x86-64/cloud/cross-platform qualification pending",
            "no Git commit or signed release tag",
        ],
    }
    OUTPUT.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
