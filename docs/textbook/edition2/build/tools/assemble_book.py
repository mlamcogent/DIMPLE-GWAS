#!/usr/bin/env python3
"""Assemble the modular Edition 2 textbook and resolve verified citations."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path


EDITION2 = Path(__file__).resolve().parents[2]
FREEZE3 = EDITION2.parents[2]
OUTPUT = EDITION2 / "DIMPLE_GWAS_FREEZE3_RC1_ACADEMIC_TEXTBOOK_EDITION2.md"

PARTS = [
    ("Part I", "Evidence, phenotype-vector geometry, and validation boundaries", range(1, 6)),
    ("Part II", "The implemented representation, clustering, selection, and replay method", range(6, 13)),
    ("Part III", "The analyst workflow from installation to explanation", range(13, 18)),
    ("Part IV", "Worked and executable analyses", range(18, 23)),
    ("Part V", "Validation, reporting, and responsible release", range(23, 25)),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_inventory() -> list[dict[str, str]]:
    with (EDITION2 / "qa/figure_inventory.tsv").open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def bibliography_index() -> tuple[dict[str, str], dict[str, str]]:
    text = (EDITION2 / "references/VERIFIED_BIBLIOGRAPHY.md").read_text(encoding="utf-8")
    labels: dict[str, str] = {}
    entries: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"- \*\*([^.]+)\.\*\*\s+(.+)", line)
        if not match:
            continue
        key, entry = match.groups()
        year_match = re.search(r"\((\d{4})\)", entry)
        author_field = entry.split("(", 1)[0].strip().rstrip(".")
        surname = author_field.split(",", 1)[0]
        multiple = ";" in author_field or " et al." in author_field
        year = year_match.group(1) if year_match else "n.d."
        labels[key] = f"{surname}{' et al.' if multiple else ''} ({year})"
        entries[key] = line
    return labels, entries


def resolve_citations(text: str, labels: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        keys = [value.strip().lstrip("@") for value in match.group(1).split(";")]
        missing = [key for key in keys if key not in labels]
        if missing:
            raise ValueError(f"Unresolved citation keys: {missing}")
        return "[" + "; ".join(f"[{labels[key]}](#ref-{key})" for key in keys) + "]"
    return re.sub(r"\[(@[^\]]+)\]", replace, text)


def anchor_bibliography(text: str) -> str:
    return re.sub(r"^- \*\*([^.]+)\.\*\*", lambda m: f'<a id="ref-{m.group(1)}"></a>\n\n- **{m.group(1)}.**', text, flags=re.M)


def number_tables_and_equations(text: str) -> tuple[str, int, int]:
    """Add deterministic, visible captions to Markdown tables and display equations."""
    lines = text.splitlines()
    out: list[str] = []
    heading = "Reference table"
    in_fence = False
    table_number = 0
    equation_number = 0
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith("```"):
            in_fence = not in_fence
        heading_match = re.match(r"^#{1,4}\s+(.+)$", line)
        if heading_match and not in_fence:
            heading = re.sub(r"[*`#]", "", heading_match.group(1)).strip()
        is_table = (
            not in_fence and line.lstrip().startswith("|") and index + 1 < len(lines)
            and re.match(r"^\s*\|?\s*:?-{3,}", lines[index + 1])
        )
        if is_table:
            table_number += 1
            out += [f'<p class="table-caption" id="table-{table_number}"><strong>Table {table_number}.</strong> {heading}.</p>', ""]
        out.append(line)
        if not in_fence and line.strip() == r"\]":
            equation_number += 1
            out += [f'<p class="equation-number" id="equation-{equation_number}"><strong>Equation {equation_number}.</strong></p>']
        index += 1
    return "\n".join(out), table_number, equation_number


def figure_block(row: dict[str, str]) -> str:
    alt = row["caption"].rstrip(".")
    return (
        f'\n\n<figure id="fig-{row["figure_id"].lower()}">\n\n'
        f'![{alt}]({row["file"]}){{fig-alt="{alt}"}}\n\n'
        f'<figcaption><strong>Figure {row["display_number"]}.</strong> {row["caption"]} '
        f'<em>Interpretive boundary:</em> {row["caution"]}</figcaption>\n\n'
        f'</figure>\n\n'
    )


def insert_after_section(text: str, rows: list[dict[str, str]], late: bool = False) -> str:
    block = "".join(figure_block(row) for row in rows)
    if late:
        marker = "## Reading the generated evidence"
        if marker in text:
            return text.replace(marker, block + marker, 1)
    headings = list(re.finditer(r"^## ", text, flags=re.M))
    if len(headings) >= 2:
        return text[:headings[1].start()] + block + text[headings[1].start():]
    return text + block


def part_page(part: str, title: str, chapters: range) -> str:
    return f'''<div class="part-break"></div>

# {part}

## {title}

Chapters {chapters.start}–{chapters.stop - 1}

<div class="part-page-rule"></div>
'''


def main() -> None:
    labels, _ = bibliography_index()
    figures = read_inventory()
    original_order = {row["figure_id"]: index for index, row in enumerate(figures)}
    display_order = sorted(figures, key=lambda row: (int(row["chapter"]), original_order[row["figure_id"]]))
    for number, row in enumerate(display_order, 1):
        row["display_number"] = str(number)
    with (EDITION2 / "qa/figure_reference_audit.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["display_number", "figure_id", "chapter", "file"], delimiter="\t")
        writer.writeheader()
        for row in display_order:
            writer.writerow({key: row[key] for key in writer.fieldnames})
    by_chapter: dict[int, list[dict[str, str]]] = {}
    for row in figures:
        by_chapter.setdefault(int(row["chapter"]), []).append(row)

    chapter_paths = {int(path.name[:2]): path for path in (EDITION2 / "chapters").glob("*.md")}
    appendix_paths = sorted((EDITION2 / "appendices").glob("*.md"))
    chapter_titles = {number: re.search(r"^#\s+(.+)$", path.read_text(encoding="utf-8"), re.M).group(1) for number, path in chapter_paths.items()}
    appendix_titles = {path.name[0]: re.search(r"^#\s+(.+)$", path.read_text(encoding="utf-8"), re.M).group(1) for path in appendix_paths}

    contents = ["# Contents", "", "- [Editorial and evidence status](#editorial-status)", "- [Preface and reader paths](#preface)", "- [How to use this internal review edition](#how-to-use)"]
    for part, title, chapter_numbers in PARTS:
        anchor = part.lower().replace(" ", "-")
        contents += [f"- [{part}: {title}](#{anchor})"]
        for chapter in chapter_numbers:
            contents += [f"  - [{chapter_titles[chapter]}](#chapter-{chapter})"]
    contents += ["- [Appendices](#appendices)"]
    for letter, title in appendix_titles.items():
        contents += [f"  - [{title}](#appendix-{letter.lower()})"]
    contents.append("")

    chunks: list[str] = []
    title_path = EDITION2 / "front_matter/00_title_and_authors.md"
    chunks.append(title_path.read_text(encoding="utf-8") + "\n<div class=\"title-page-break\"></div>\n")
    chunks.append("\n".join(contents) + "\n<div class=\"title-page-break\"></div>\n")
    chunks.append('<a id="editorial-status"></a>\n\n' + (EDITION2 / "front_matter/01_editorial_and_evidence_status.md").read_text(encoding="utf-8"))
    chunks.append('<a id="preface"></a>\n\n' + (EDITION2 / "front_matter/02_preface_and_reader_paths.md").read_text(encoding="utf-8"))

    chunks.append('''<a id="how-to-use"></a>

# How to use this internal review edition

This assembled source is the authoritative Edition 2 reading copy. The modular chapter, atlas, lab, and QA files remain the audit trail. Every displayed claim should be read at the layer named in its wording: implemented, freshly executed and bounded, historical, literature-supported, or pending. Figure captions state both the visible relationship and the inference that must not be made.

The HTML and PDF are deterministic presentation builds from this source. The source checksum inventory replaces unavailable Git metadata for this freeze. The Docker image, fresh original 164-IDP 1,000-seed execution, team adjudication, and public release metadata remain outside this documentation build.
''')

    for part, title, chapter_numbers in PARTS:
        chunks.append(part_page(part, title, chapter_numbers))
        for chapter in chapter_numbers:
            text = chapter_paths[chapter].read_text(encoding="utf-8")
            rows = by_chapter.get(chapter, [])
            if rows:
                early = rows[:1]
                late = rows[1:]
                text = insert_after_section(text, early)
                if late:
                    text = insert_after_section(text, late, late=True)
            chunks.append(f'<div class="chapter-break"></div>\n\n<a id="chapter-{chapter}"></a>\n\n' + text)

    chunks.append('<div class="part-break"></div>\n\n# Appendices\n')
    for path in appendix_paths:
        text = path.read_text(encoding="utf-8")
        if path.name == "K_verified_bibliography.md":
            text = anchor_bibliography(text)
        letter = path.name[0].lower()
        chunks.append(f'<div class="appendix-break"></div>\n\n<a id="appendix-{letter}"></a>\n\n' + text)

    assembled, table_count, equation_count = number_tables_and_equations("\n\n".join(chunks))
    assembled = resolve_citations(assembled, labels)
    if re.search(r"\[@", assembled):
        raise ValueError("Unresolved citation syntax remains")
    OUTPUT.write_text(assembled.rstrip() + "\n", encoding="utf-8")

    used_keys = sorted(set(re.findall(r"#ref-([a-zA-Z0-9_.-]+)", assembled)))
    stats = {
        "assembled_markdown": str(OUTPUT.relative_to(FREEZE3)),
        "sha256": sha256(OUTPUT),
        "bytes": OUTPUT.stat().st_size,
        "word_count_regex": len(re.findall(r"\b[\w'-]+\b", assembled)),
        "chapters": len(chapter_paths),
        "appendices": len(list((EDITION2 / "appendices").glob("*.md"))),
        "figures": len(figures),
        "tables": table_count,
        "numbered_display_equations": equation_count,
        "resolved_citation_keys": len(used_keys),
        "unresolved_citation_tokens": len(re.findall(r"\[@", assembled)),
    }
    (EDITION2 / "build/assembly_stats.json").write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
