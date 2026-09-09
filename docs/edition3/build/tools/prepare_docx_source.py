#!/usr/bin/env python3
"""Create a DOCX-safe manuscript with a static contents section and labelled rows."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "DIMPLE_GWAS_FREEZE3_RC1_DOCUMENTATION_EDITION3.md"
OUTPUT = ROOT / "build/edition3_docx_source.md"
PAGE_MAP = ROOT / "build/contents_page_numbers.json"
SEPARATOR = re.compile(r"^:?-{3,}:?$")


def cells(line: str) -> list[str]:
    return [part.strip() for part in line.strip().strip("|").split("|")]


def is_separator(row: list[str]) -> bool:
    return bool(row) and all(SEPARATOR.match(item.replace(" ", "")) for item in row)


def heading_entries(lines: list[str]) -> list[tuple[str, str]]:
    """Return major manuscript headings as (contents level, display title)."""
    entries: list[tuple[str, str]] = []
    for line in lines:
        if not line.startswith("# "):
            continue
        title = re.sub(r"\s+\{\.unnumbered\}\s*$", "", line[2:]).strip()
        if title.startswith("Contents"):
            continue
        level = "TOC1" if title.startswith("Part ") or title in {
            "Editorial and evidence status",
            "Preface: three ways through one method",
        } else "TOC2"
        entries.append((level, title))
    return entries


def contents_lines(entries: list[tuple[str, str]]) -> list[str]:
    pages = json.loads(PAGE_MAP.read_text(encoding="utf-8")) if PAGE_MAP.is_file() else {}
    split_index = next(index for index, (_, title) in enumerate(entries) if title.startswith("Part V"))

    def rows(group: list[tuple[str, str]]) -> list[str]:
        rendered: list[str] = []
        for level, title in group:
            rendered.extend([f"{level}|{title}|{pages.get(title, '000')}", ""])
        return rendered

    return [
        "",
        "# Contents {.unnumbered}",
        "",
        *rows(entries[:split_index]),
        "",
        "# Contents (continued) {.unnumbered}",
        "",
        *rows(entries[split_index:]),
        "",
    ]


def main() -> None:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    entries = heading_entries(lines)
    yaml_end = next(index for index in range(1, len(lines)) if lines[index] == "---")
    for index in range(yaml_end + 1):
        if lines[index].strip() == "toc: true":
            lines[index] = "toc: false"
    lines = lines[: yaml_end + 1] + contents_lines(entries) + lines[yaml_end + 1 :]
    output: list[str] = []
    converted = 0
    index = 0
    while index < len(lines):
        if not lines[index].startswith("|"):
            output.append(lines[index])
            index += 1
            continue

        block: list[str] = []
        while index < len(lines) and lines[index].startswith("|"):
            block.append(lines[index])
            index += 1
        parsed = [cells(line) for line in block]
        if len(parsed) < 2 or not is_separator(parsed[1]):
            output.extend(block)
            continue

        headers = parsed[0]
        rows = parsed[2:]
        output.append("")
        for row in rows:
            padded = row + [""] * max(0, len(headers) - len(row))
            fields = [f"**{header}:** {value}" for header, value in zip(headers, padded) if value]
            output.append("- " + "; ".join(fields))
        output.append("")
        converted += 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")
    print(
        f"Inserted {len(entries)} static contents entries and converted {converted} "
        f"Markdown tables for DOCX compatibility: {OUTPUT}"
    )


if __name__ == "__main__":
    main()
