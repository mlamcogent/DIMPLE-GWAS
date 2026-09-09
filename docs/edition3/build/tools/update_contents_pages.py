#!/usr/bin/env python3
"""Map each static contents entry to its physical page in a rendered PDF."""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "DIMPLE_GWAS_FREEZE3_RC1_DOCUMENTATION_EDITION3.md"
OUTPUT = ROOT / "build/contents_page_numbers.json"


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).lower()
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def headings() -> list[str]:
    titles: list[str] = []
    for line in MASTER.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            title = re.sub(r"\s+\{\.unnumbered\}\s*$", "", line[2:]).strip()
            if not title.startswith("Contents"):
                titles.append(title)
    return titles


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: update_contents_pages.py RENDERED.pdf")
    pdf_path = Path(sys.argv[1])
    reader = PdfReader(pdf_path)
    page_text = [normalize(page.extract_text() or "") for page in reader.pages]
    mapping: dict[str, int] = {}
    missing: list[str] = []
    for title in headings():
        needle = normalize(title)
        page_number = next(
            (index + 1 for index, text in enumerate(page_text) if index >= 3 and needle in text),
            None,
        )
        if page_number is None:
            missing.append(title)
        else:
            mapping[title] = page_number
    if missing:
        raise SystemExit("Missing contents headings in PDF: " + "; ".join(missing))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(mapping, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Mapped {len(mapping)} contents entries across {len(reader.pages)} pages: {OUTPUT}")


if __name__ == "__main__":
    main()
