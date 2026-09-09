#!/usr/bin/env python3
"""Extract auditable plain-text views of PDF and DOCX source records.

The original files are never modified. Output is deliberately simple text so it
can be searched, checksummed, and cited in the manual evidence registers.
"""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from docx import Document
from pypdf import PdfReader


W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def safe_name(path: Path) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", path.name).strip("_")


def normalize_extracted_text(text: str) -> str:
    """Collapse extraction-driven line breaks while preserving page/table markers."""
    blocks = re.split(r"(===== [^=]+ =====)", text)
    normalized: list[str] = []
    for block in blocks:
        if block.startswith("====="):
            normalized.append(f"\n\n{block.strip()}\n\n")
        else:
            compact = re.sub(r"\s+", " ", block).strip()
            if compact:
                normalized.append(compact)
    return "".join(normalized).strip() + "\n"


def extract_pdf(path: Path) -> tuple[str, dict[str, object]]:
    reader = PdfReader(str(path))
    pages: list[str] = []
    for page_no, page in enumerate(reader.pages, start=1):
        pages.append(f"\n\n===== PAGE {page_no} =====\n\n{page.extract_text() or ''}")
    metadata = {
        "format": "pdf",
        "pages": len(reader.pages),
        "encrypted": bool(reader.is_encrypted),
        "document_metadata": {str(k): str(v) for k, v in (reader.metadata or {}).items()},
    }
    return "".join(pages).strip() + "\n", metadata


def extract_comments(path: Path) -> list[dict[str, str]]:
    comments: list[dict[str, str]] = []
    with zipfile.ZipFile(path) as archive:
        if "word/comments.xml" not in archive.namelist():
            return comments
        root = ET.fromstring(archive.read("word/comments.xml"))
        for comment in root.findall(f"{W_NS}comment"):
            text = "".join(node.text or "" for node in comment.iter(f"{W_NS}t"))
            comments.append(
                {
                    "id": comment.attrib.get(f"{W_NS}id", ""),
                    "author": comment.attrib.get(f"{W_NS}author", ""),
                    "date": comment.attrib.get(f"{W_NS}date", ""),
                    "text": text,
                }
            )
    return comments


def extract_docx(path: Path) -> tuple[str, dict[str, object]]:
    document = Document(str(path))
    chunks: list[str] = []
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:
            chunks.append(text)
    for table_no, table in enumerate(document.tables, start=1):
        chunks.append(f"\n===== TABLE {table_no} =====")
        for row in table.rows:
            chunks.append("\t".join(cell.text.replace("\n", " ").strip() for cell in row.cells))
    comments = extract_comments(path)
    if comments:
        chunks.append("\n===== COMMENTS =====")
        for comment in comments:
            chunks.append(
                f"COMMENT {comment['id']} | {comment['author']} | {comment['date']}\n{comment['text']}"
            )
    metadata = {
        "format": "docx",
        "paragraphs": len(document.paragraphs),
        "tables": len(document.tables),
        "inline_shapes": len(document.inline_shapes),
        "comments": len(comments),
        "core_properties": {
            "title": document.core_properties.title or "",
            "subject": document.core_properties.subject or "",
            "author": document.core_properties.author or "",
            "last_modified_by": document.core_properties.last_modified_by or "",
            "created": str(document.core_properties.created or ""),
            "modified": str(document.core_properties.modified or ""),
        },
    }
    return "\n\n".join(chunks).strip() + "\n", metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("inputs", nargs="+", type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    index: list[dict[str, object]] = []
    for input_path in args.inputs:
        resolved = input_path.resolve()
        suffix = resolved.suffix.lower()
        if suffix == ".pdf":
            text, metadata = extract_pdf(resolved)
        elif suffix == ".docx":
            text, metadata = extract_docx(resolved)
        else:
            raise ValueError(f"Unsupported source format: {resolved}")
        output_path = args.output_dir / f"{safe_name(resolved)}.txt"
        output_path.write_text(text, encoding="utf-8")
        normalized_path = args.output_dir / f"{safe_name(resolved)}.normalized.txt"
        normalized_path.write_text(normalize_extracted_text(text), encoding="utf-8")
        index.append(
            {
                "source": str(resolved),
                "extracted_text": str(output_path.resolve()),
                "normalized_text": str(normalized_path.resolve()),
                **metadata,
            }
        )

    (args.output_dir / "extraction_index.json").write_text(
        json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
