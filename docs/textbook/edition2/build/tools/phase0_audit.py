#!/usr/bin/env python3
"""Reconstruct and audit the immutable Edition 1 baseline for Textbook Edition 2."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import re
from collections import Counter
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader


EDITION2 = Path(__file__).resolve().parents[2]
FREEZE3 = EDITION2.parents[2]
WORKSPACE = FREEZE3.parent
EDITION1 = FREEZE3 / "docs" / "manual"
EVIDENCE = EDITION2 / "evidence"
QA = EDITION2 / "qa"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_tsv(path: Path, header: list[str], rows: Iterable[Iterable[object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def inventory() -> None:
    rows = read_tsv(EDITION1 / "evidence" / "01_input_inventory.tsv")
    known = {row["path"] for row in rows}
    additions = [
        (WORKSPACE / "DIMPLE_GWAS_FREEZE3_RC1_TEXTBOOK_EDITION2_CODEX_RUN_MACRO.md", "edition2 specification", "7", "coordinator specification", "internal working document"),
        (EDITION1 / "DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.md", "edition1 baseline", "6", "immutable documentation baseline", "public-safe edition"),
        (EDITION1 / "DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.pdf", "edition1 baseline", "6", "immutable rendered baseline", "public-safe edition"),
        (EDITION1 / "MANUAL_BUILD_REPORT.md", "edition1 evidence", "2", "fresh Edition 1 build evidence", "internal build record"),
        (EDITION1 / "MANUAL_QA_REPORT.md", "edition1 evidence", "2", "Edition 1 QA record subject to red-team audit", "internal build record"),
        (WORKSPACE / "first-review-nat-comm-email.pdf", "reviewer correspondence", "5", "confidential reviewer/editorial source", "restricted - confidential email and personal identifiers"),
        (WORKSPACE / "nature_communications_preliminary_reviewer_2_action_register.md", "reviewer action register", "5", "sanitized reviewer-response planning source", "internal unpublished review material"),
    ]
    for path, role, level, note, sensitivity in additions:
        rel = path.relative_to(WORKSPACE).as_posix()
        if rel in known or not path.is_file():
            continue
        stat = path.stat()
        rows.append({
            "path": rel,
            "type": path.suffix.lower().lstrip(".") or "file",
            "role": role,
            "size_bytes": str(stat.st_size),
            "modified_sgt": datetime.fromtimestamp(stat.st_mtime, timezone.utc).astimezone().isoformat(),
            "sha256": sha256(path),
            "authority_level": level,
            "authority_note": note,
            "sensitivity": sensitivity,
        })
    rows.sort(key=lambda row: row["path"])
    write_tsv(EVIDENCE / "01_input_inventory.tsv", list(rows[0]), ([row[key] for key in rows[0]] for row in rows))

    selected = []
    for row in rows:
        if row["authority_level"] in {"1", "2"} or row["role"] in {
            "edition2 specification", "edition1 baseline", "reviewer correspondence", "reviewer action register", "scientific narrative"
        }:
            selected.append([row["path"], row["sha256"], row["role"], row["authority_level"], row["sensitivity"]])
    write_tsv(EVIDENCE / "04_source_checksums.tsv", ["path", "sha256", "role", "authority_level", "sensitivity"], selected)


def snapshot() -> None:
    source_hash = sha256(FREEZE3 / "pyproject.toml")
    text = f"""# Edition 2 repository and environment snapshot

- Recorded: `{datetime.now(timezone.utc).astimezone().isoformat()}`
- Workspace: `{WORKSPACE.resolve()}`
- Freeze 3 source: `{FREEZE3.resolve()}`
- Edition 1 baseline: `{EDITION1.resolve()}`
- Edition 2 tree: `{EDITION2.resolve()}`
- Platform: `{platform.platform()}`
- Architecture: `{platform.machine()}`
- Audit Python: `{platform.python_version()}`
- Package version: `3.0.0rc1` (verified from `pyproject.toml` and Edition 1 runtime evidence)
- Git identity: unavailable; neither workspace nor Freeze 3 is a Git repository.
- Identity fallback: package metadata/checksum plus `04_source_checksums.tsv`; `pyproject.toml` SHA-256 `{source_hash}`.
- Documentation status: internal review; publication-ready drafting target; Docker validation and team adjudication pending.
- Fresh 164-IDP 1,000-seed run: deferred until Docker by coordinator direction.

## Preservation boundary

`docs/manual/` is the immutable Edition 1 baseline. Edition 2 writes only under `docs/textbook/edition2/` and newly named laboratory roots within that tree. Manuscripts, reviewer correspondence, historical outputs, and the Freeze 3 implementation are read-only inputs.

## Confidentiality boundary

The first-review email is private evidence and contains contact details plus an explicit confidentiality notice. It may inform a sanitized reviewer-action crosswalk, but it must not be copied into publishable artifacts. Complete private provenance is retained by path and SHA-256; public-facing evidence uses bounded paraphrase without personal identifiers.
"""
    (EVIDENCE / "00_repository_environment_snapshot.md").write_text(text, encoding="utf-8")


def conflicts_and_missing() -> None:
    conflicts = [
        ["AUTH-001", "Git commit/tag requested by macro", "No Git repository metadata exists", "current filesystem checksums", "Use package/source SHA-256 and record Git as unavailable; establish versioned Git identity before Docker release."],
        ["AUTH-002", "Edition 1 QA states zero visual overlap", "Full-resolution review shows overlapping input-orientation and provenance nodes plus an orphaned search-space diagram", "rendered Edition 1 pages at 100%", "Treat Edition 1 QA as incomplete; Edition 2 requires source-level and page-level figure QA."],
        ["AUTH-003", "Reviewer/Gemini references to Yang or Zhao works", "Neither supplied Reviewer #2 email nor action register identifies such papers", "actual confidential reviewer email and action register", "Keep as unresolved evidence gap; do not attribute or cite a guessed paper."],
        ["AUTH-004", "Edition 1 describes itself as complete first draft", "Edition 2 macro diagnoses inadequate textbook depth", "Edition 2 coordinator specification", "Preserve Edition 1 as a verified operational baseline, not as the target academic treatment."],
        ["AUTH-005", "Manuscript scientific interpretation", "Some claims extend beyond Stage 1 implementation evidence", "executable source and fresh bounded runs", "Use manuscript for context only; separately label downstream biological claims and validation evidence."],
        ["AUTH-006", "Every discovered callable", "Static enumeration can include nested closures and mechanical helpers", "package-defined module symbols", "Inventory all package-defined module functions and class methods; list nested closures separately and exclude imported third-party callables."],
    ]
    write_tsv(EVIDENCE / "02_authority_conflict_map.tsv", ["conflict_id", "source_or_expectation", "conflict", "authority_applied", "resolution"], conflicts)

    missing = [
        ["MISS-001", "Git commit, branch, tag, and remotes", "release/source identity", "Use SHA-256 identity for TE2; establish Git identity before Docker/public release.", "high", "open"],
        ["MISS-002", "Fresh 164-IDP 1,000-seed execution", "fresh scientific reproduction", "Deferred until Docker; retain exact protocol and do not claim fresh results.", "high", "deferred"],
        ["MISS-003", "Original 2,315-IDP raw matrix", "fresh primary analysis", "Historical-only discussion; do not select a substitute.", "high", "open"],
        ["MISS-004", "Original 459-IDP raw matrix and unambiguous configuration", "fresh secondary analysis", "Historical-only discussion pending exact data/config identity.", "high", "open"],
        ["MISS-005", "Complete editorial decision and Reviewer #1 report", "complete journal-response crosswalk", "Edition 2 uses only supplied Reviewer #2 material and labels the set incomplete.", "medium", "open"],
        ["MISS-006", "Exact Yang- and Zhao-attributed reviewer papers", "reviewer bibliography attribution", "No such citations occur in the supplied reviewer email/action register; keep unresolved and uncited.", "medium", "open"],
        ["MISS-007", "Docker/Linux/GCP/AWS execution and security evidence", "cross-platform and release validation", "Explicitly pending; use the documentation handoff only.", "high", "deferred"],
        ["MISS-008", "Team-approved textbook authorship styling beyond manuscript order", "final publication metadata", "Use manuscript author order and degree convention for internal review; adjudicate affiliation/contribution typography before public release.", "low", "bounded"],
        ["MISS-009", "Book distribution licence and DOI/ISBN/publisher metadata", "public release packaging", "Omit identifiers and label internal review; add only after team decision.", "medium", "open"],
    ]
    write_tsv(EVIDENCE / "03_missing_evidence_register.tsv", ["gap_id", "missing_evidence", "affected_claim_or_task", "bounded_handling", "priority", "status"], missing)


def chapter_sections(text: str) -> list[tuple[int, str, str]]:
    matches = list(re.finditer(r"^# (\d+)\. (.+)$", text, flags=re.MULTILINE))
    rows = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else text.find("\n# Appendices", match.end())
        if end < 0:
            end = len(text)
        rows.append((int(match.group(1)), match.group(2).strip(), text[match.start():end]))
    return rows


def content_audit() -> None:
    md_path = EDITION1 / "DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.md"
    pdf_path = EDITION1 / "DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.pdf"
    text = md_path.read_text(encoding="utf-8")
    reader = PdfReader(pdf_path)
    page_words = [word_count(page.extract_text() or "") for page in reader.pages]
    chapters = chapter_sections(text)
    chapter_rows = []
    teaching_headings = [
        "Orientation", "Learning objectives", "Explanation and implementation", "Evidence-backed example",
        "Outputs to inspect", "Common mistakes", "Scientific and operational limits", "Completion check",
    ]
    for number, title, body in chapters:
        chapter_rows.append([
            number, title, word_count(body),
            len(re.findall(r"^## ", body, flags=re.MULTILINE)),
            len(re.findall(r"```", body)) // 2,
            len(re.findall(r"!\[[^]]*\]\([^)]+\)", body)),
            sum(heading in body for heading in teaching_headings),
            body.count("Release status."),
        ])
    write_tsv(QA / "edition1_chapter_metrics.tsv", ["chapter", "title", "words", "h2_sections", "code_blocks", "figures", "teaching_scaffold_sections", "release_banner_count"], chapter_rows)

    page_rows = [[index, words, "yes" if words < 100 else "no", "yes" if words < 150 else "no", "yes" if words < 200 else "no"] for index, words in enumerate(page_words, 1)]
    write_tsv(QA / "edition1_page_density.tsv", ["page", "extracted_words", "below_100", "below_150", "below_200"], page_rows)

    paragraphs = []
    for number, title, body in chapters:
        for paragraph in re.split(r"\n\s*\n", body):
            cleaned = re.sub(r"\s+", " ", re.sub(r"[`*_>#-]", "", paragraph)).strip()
            if word_count(cleaned) >= 12:
                paragraphs.append((number, title, cleaned))
    exact = Counter(paragraph for _, _, paragraph in paragraphs)
    duplicate_rows = []
    for paragraph, count in exact.most_common():
        if count < 2:
            break
        locations = [str(number) for number, _, value in paragraphs if value == paragraph]
        duplicate_rows.append(["exact", count, ",".join(locations), paragraph[:500]])
    # Detect high-similarity chapter opening/scaffold paragraphs after removing part/chapter labels.
    sampled = [(n, t, p) for n, t, p in paragraphs if any(key in p for key in ["This chapter belongs", "After this chapter", "Operational cross-reference"])]
    seen_pairs = set()
    for i, (n1, _, p1) in enumerate(sampled):
        for n2, _, p2 in sampled[i + 1:]:
            if n1 == n2 or (n1, n2) in seen_pairs:
                continue
            ratio = SequenceMatcher(None, p1, p2).ratio()
            if ratio >= 0.84:
                duplicate_rows.append([f"near_{ratio:.3f}", 2, f"{n1},{n2}", p1[:500]])
                seen_pairs.add((n1, n2))
    write_tsv(QA / "edition1_duplicate_passages.tsv", ["match_type", "occurrences", "chapter_locations", "representative_text"], duplicate_rows)

    metrics = {
        "schema": "dimple-gwas.edition1-baseline-metrics.v1",
        "pdf_pages": len(reader.pages),
        "markdown_words": word_count(text),
        "pdf_extracted_words": sum(page_words),
        "chapters": len(chapters),
        "appendices": len(list((EDITION1 / "appendices").glob("*.md"))),
        "image_references": len(re.findall(r"!\[[^]]*\]\([^)]+\)", text)),
        "code_blocks": len(re.findall(r"^```", text, flags=re.MULTILINE)) // 2,
        "display_math_blocks": len(re.findall(r"\\\[.*?\\\]", text, flags=re.DOTALL)),
        "inline_math_spans": len(re.findall(r"\\\(.*?\\\)", text, flags=re.DOTALL)),
        "markdown_table_separators": len(re.findall(r"^\|\s*---", text, flags=re.MULTILINE)),
        "release_banner_occurrences": text.count("Release status."),
        "operational_cross_reference_occurrences": text.count("Operational cross-reference:"),
        "pages_below_100_words": sum(value < 100 for value in page_words),
        "pages_below_150_words": sum(value < 150 for value in page_words),
        "pages_below_200_words": sum(value < 200 for value in page_words),
        "percent_pages_below_100_words": round(100 * sum(value < 100 for value in page_words) / len(page_words), 2),
        "percent_pages_below_150_words": round(100 * sum(value < 150 for value in page_words) / len(page_words), 2),
        "percent_pages_below_200_words": round(100 * sum(value < 200 for value in page_words) / len(page_words), 2),
        "median_chapter_words": sorted(row[2] for row in chapter_rows)[len(chapter_rows) // 2],
        "minimum_chapter_words": min(row[2] for row in chapter_rows),
        "maximum_chapter_words": max(row[2] for row in chapter_rows),
        "exact_or_near_duplicate_rows": len(duplicate_rows),
    }
    (QA / "edition1_content_metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    summary = f"""# Edition 1 content audit

Edition 1 is a useful verified operational baseline but not a graduate-level textbook. The compiled Markdown contains **{metrics['markdown_words']:,} words** across **{metrics['chapters']} chapters** and **{metrics['appendices']} appendices**; the PDF contains **{metrics['pdf_pages']} A4 pages** and approximately **{metrics['pdf_extracted_words']:,} extractable words**. The median chapter has **{metrics['median_chapter_words']:,} words** (range {metrics['minimum_chapter_words']:,}–{metrics['maximum_chapter_words']:,}).

## Density and structure

- {metrics['pages_below_100_words']} pages ({metrics['percent_pages_below_100_words']}%) contain fewer than 100 extracted words.
- {metrics['pages_below_150_words']} pages ({metrics['percent_pages_below_150_words']}%) contain fewer than 150 extracted words.
- {metrics['pages_below_200_words']} pages ({metrics['percent_pages_below_200_words']}%) contain fewer than 200 extracted words.
- The same eight-section teaching scaffold appears in all 46 chapters.
- A large release-status box appears {metrics['release_banner_occurrences']} times and the same operational cross-reference appears {metrics['operational_cross_reference_occurrences']} times.
- The edition contains {metrics['image_references']} image references, {metrics['code_blocks']} fenced code blocks, {metrics['display_math_blocks']} display-math blocks, and {metrics['markdown_table_separators']} Markdown tables.

## Source-of-sparsity diagnosis

The generation system treated every topic as an identically shaped two-page unit. Short parameter descriptions, scientific cautions, command fragments, and completion prompts were spread across 46 forced chapter openings. Repeated banners, boilerplate prerequisites, generic evidence language, and part-divider pages consumed pagination without developing the underlying mathematics or examples. The chapter generator optimized structural coverage—every topic received the same headings—but did not budget depth by conceptual difficulty. Reference-like content was mixed into the main narrative, while function contracts, formula derivations, hand-worked calculations, exercises, and output schemas remained too compressed.

The remedy is architectural rather than cosmetic: merge the 46 notes into 24 substantial chapters, move lookup material to function/output atlases, draft by conceptual dependency, require method-specific dossiers and worked calculations, and permit chapter structures to vary. Edition 2 must measure substantive words after removing front matter, code-only listings, bibliography, and generated schema tables so visual length cannot substitute for explanatory depth.

## Evidence files

- `edition1_chapter_metrics.tsv`: chapter-level density and scaffold counts.
- `edition1_page_density.tsv`: page-level extracted-word counts.
- `edition1_duplicate_passages.tsv`: exact and high-similarity boilerplate evidence.
- `edition1_content_metrics.json`: machine-readable baseline.
"""
    (QA / "edition1_content_audit.md").write_text(summary, encoding="utf-8")


def pedagogical_audit() -> None:
    text = (EDITION1 / "DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.md").read_text(encoding="utf-8")
    chapters = chapter_sections(text)
    method_core = {5, 6, 8, 15, 16, 17, 18, 19, 20, 23, 24, 25, 26, 28, 29, 30, 40}
    case_studies = {13, 32, 33, 34, 35, 36}
    operational = set(range(9, 15)) | set(range(37, 47))
    rows = []
    for number, title, body in chapters:
        scores = {
            "motivation": 2 if number <= 8 or number in {28, 29, 30, 31, 36, 46} else 1,
            "intuition": 2 if number in method_core else 1,
            "formal_statistics": 1 if number in method_core else 0,
            "implementation": 2 if number in operational or number in method_core else 1,
            "executable_use": 3 if number in case_studies else (2 if number in operational else 1),
            "output_interpretation": 3 if number in {14, 21, 23, 25, 27, 28, 31, 34, 41} else 1,
            "assumptions_limits": 2,
            "diagnostics_failure_modes": 2 if number in {18, 19, 20, 21, 23, 28, 29, 30, 43, 44, 46} else 1,
            "worked_example": 2 if number in case_studies else 1,
            "exercises_checks": 1,
            "citations_traceability": 2 if "Evidence and references" in body else 1,
            "chapter_connections": 1,
        }
        total = sum(scores.values())
        action = "rewrite from zero" if number in method_core else ("merge and expand" if number < 37 else "move core lookup material to reference atlas and retain narrative essentials")
        rows.append([number, title, *scores.values(), total, action])
    header = ["chapter", "title", *scores.keys(), "total_of_36", "edition2_action"]
    write_tsv(QA / "edition1_chapter_gap_matrix.tsv", header, rows)

    report = """# Edition 1 pedagogical red-team report

## Verdict

Edition 1 succeeds as a cautious analyst-manual skeleton: it names the implemented stages, gives portable command patterns, records fresh fixture evidence, and preserves important interpretation boundaries. It does not yet teach the method at graduate-textbook depth. The weakness is systemic, not confined to a handful of chapters.

## Principal failures

1. **Architecture fragments concepts.** Forty-six short chapters interrupt the conceptual arc. UMAP, repetition, HDBSCAN, diagnostics, scoring, selection, reproduction, comparison, and interpretation are introduced as adjacent checklists rather than developed as a connected inferential workflow.
2. **Mathematics is largely deferred.** The mathematical appendix contains several formulas, but main chapters rarely derive objectives, define edge cases, or connect equations to implementation behavior.
3. **Examples assert rather than teach.** Executed fixture results are real, but most chapters state one result instead of walking through a calculation, file excerpt, decision, and alternative interpretation.
4. **Function coverage is indirect.** Commands and configuration keys are mapped, but the reader cannot trace every core function through inputs, parameters, exceptions, outputs, tests, and computational behavior.
5. **Exercises do not assess objectives.** A one-sentence completion check appears in every chapter; there are no developed problem sets, calculation exercises, applied tasks, or separated solutions.
6. **Citations are too remote.** Bibliographic entries and occasional chapter references exist, but many statistical claims lack nearby citations and a reader cannot always see which statement a paper supports.
7. **Output education is centralized.** The atlas is useful, yet stage chapters rarely annotate representative rows/fields before sending the reader to a distant reference.
8. **Visual QA was too coarse.** Contact sheets established page presence but did not catch node overlap and figure-heading separation at full resolution.

## Edition 2 editorial disposition

- Merge the 46 notes into 24 substantial chapters organized by conceptual dependency.
- Rewrite core statistical and method chapters from zero.
- Retain verified commands, outputs, cautious language, and evidence identifiers as source material rather than prose templates.
- Move exhaustive command/configuration/function/output lookup content to structured appendices and atlases.
- Add a hand-calculable lab, executed labs, multi-step exercises, and a solutions appendix.
- Use a function dossier as a content-completeness contract, but integrate its fields into natural prose rather than repeating 20 visible headings.
- Audit every source figure independently and again on the composed page.

The machine-readable rubric is `edition1_chapter_gap_matrix.tsv`. Scores describe the supplied Edition 1 baseline only; they are diagnostic planning evidence, not a publication-quality rating.
"""
    (QA / "edition1_red_team_report.md").write_text(report, encoding="utf-8")


def visual_audit() -> None:
    page_words = {int(row["page"]): int(row["extracted_words"]) for row in read_tsv(QA / "edition1_page_density.tsv")}
    defects = [
        ["VIS-001", 25, "input-orientation diagram", "Sibling metadata and phenotype-vector nodes overlap; labels visually collide at the shared boundary.", "high", "Automatic Mermaid layout plus mismatched node widths", "Rebuild as a measured two-column SVG with explicit gap, padding, and shape annotations.", "confirmed"],
        ["VIS-002", 44, "search-space diagram", "Diagram begins at the top of the continuation page while its generic section heading is stranded on the preceding page; caption/explanation are detached from the introduction.", "medium", "Figure block did not keep heading, figure, and caption together", "Use a composed figure block with keep-with-next rules or a dedicated landscape figure page.", "confirmed"],
        ["VIS-003", 102, "provenance diagram", "Five top-row source nodes overlap or touch, labels are cramped, and converging connectors create unnecessary congestion.", "high", "Too many peer nodes forced into a narrow automatic row", "Use two provenance lanes with measured SVG boxes, port-based connectors, and full-size page QA.", "confirmed"],
        ["VIS-004", 4, "Part I divider", "A single heading occupies a nearly empty page.", "low", "Forced part-page break without designed divider content", "Use an intentional part opener with a synopsis and dependency map, or omit the dedicated page.", "confirmed"],
        ["VIS-005", 103, "chapter 42 continuation", "Only a short cross-reference tail appears at the top of an otherwise empty page.", "medium", "Orphaned trailing block caused by rigid page breaks and keep rules", "Edit pagination and keep the completion/cross-reference block with preceding content.", "confirmed"],
        ["VIS-006", 112, "chapter 46 continuation", "A short closing section occupies a small fraction of the page immediately before a separate appendices divider.", "medium", "Repeated chapter scaffold plus forced appendix break", "Merge closing material and rebalance the appendix transition.", "confirmed"],
        ["VIS-007", 113, "Appendices divider", "A single heading creates a near-blank page without navigational or pedagogical content.", "low", "Undesigned forced divider", "Provide an appendix guide or remove the standalone divider page.", "confirmed"],
    ]
    for row in defects:
        row.append(page_words.get(row[1], ""))
    write_tsv(QA / "edition1_visual_defect_ledger.tsv", ["defect_id", "page", "object", "defect", "severity", "likely_cause", "edition2_remedy", "status", "page_extracted_words"], defects)

    report = """# Edition 1 page and figure audit

All 122 Edition 1 pages were available as 110-dpi page renders and in 11 contact sheets. The contact sheets were reviewed for global pagination and every suspected figure page was reopened at full resolution. Seven defects are recorded in `edition1_visual_defect_ledger.tsv`; three are material figure/layout failures.

The macro's starting examples are confirmed. Page 25 contains overlapping sibling nodes in the input-orientation diagram. Page 44 separates the search-space figure from its generic section heading. Page 102 compresses five provenance-source boxes into an overlapping row with congested connectors. These defects were not detected by the Edition 1 automated QA because it verified image hashes, page counts, and contact-sheet coverage but did not measure SVG bounding boxes or require a full-resolution checklist per source figure.

Edition 2 therefore adopts a two-level visual gate: each diagram must pass source SVG geometry checks before composition, and every containing page must pass full-resolution inspection after typesetting. Contact sheets remain useful for sequence and density but are not sufficient evidence of label or node clearance.
"""
    (QA / "edition1_page_figure_audit.md").write_text(report, encoding="utf-8")


def update_manifest() -> None:
    path = EDITION2 / "BOOK_BUILD_MANIFEST.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["phase_status"]["phase_0_baseline_audit"] = "complete"
    payload["baseline"] = {
        "edition1_markdown": "docs/manual/DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.md",
        "edition1_pdf": "docs/manual/DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.pdf",
        "pages": 122,
        "chapters": 46,
        "confirmed_material_visual_defects": ["VIS-001", "VIS-002", "VIS-003"],
        "audit_evidence": [
            "qa/edition1_content_audit.md",
            "qa/edition1_chapter_gap_matrix.tsv",
            "qa/edition1_red_team_report.md",
            "qa/edition1_visual_defect_ledger.tsv",
            "qa/edition1_page_figure_audit.md"
        ]
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    snapshot()
    inventory()
    conflicts_and_missing()
    content_audit()
    pedagogical_audit()
    visual_audit()
    update_manifest()
    print(f"Edition 1 Phase 0 audit complete: {EDITION2}")


if __name__ == "__main__":
    main()
