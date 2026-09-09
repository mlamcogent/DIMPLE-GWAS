from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "DIMPLE_GWAS_FREEZE3_RC1_DOCUMENTATION_EDITION3.md"
REPORT = ROOT / "qa" / "content" / "content_qa.json"
text = MASTER.read_text(encoding="utf-8")


def prose_outside_math(value: str) -> str:
    """Remove fenced code and declared math so raw TeX in prose remains detectable."""
    kept: list[str] = []
    in_fence = False
    in_display = False
    for line in value.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.strip() == "$$":
            in_display = not in_display
            continue
        if line.strip() == r"\[":
            in_display = True
            continue
        if line.strip() == r"\]":
            in_display = False
            continue
        if in_display:
            continue
        line = re.sub(r"(?<!\\)\$[^$\n]+(?<!\\)\$", "", line)
        line = line.replace(r"\newpage", "")
        kept.append(line)
    return "\n".join(kept)

forbidden = {
    "filecite": r"filecite",
    "turn_file_token": r"turn\d+file",
    "raw_mermaid_fence": r"```mermaid",
    "todo_placeholder": r"\b(?:TODO|TBD|FIXME)\b",
    "absolute_user_path": r"/Users/",
    "tracking_parameter": r"utm_source=",
    "control_character": r"[\x00-\x08\x0b\x0c\x0e-\x1f]",
}
hits = {name: len(re.findall(pattern, text, flags=re.IGNORECASE)) for name, pattern in forbidden.items()}
hits["raw_tex_outside_math"] = len(re.findall(r"\\[A-Za-z]+", prose_outside_math(text)))
cites = sorted(set(re.findall(r"@([A-Za-z0-9_:-]+)", text)))
bib = (ROOT / "evidence" / "06_VERIFIED_BIBLIOGRAPHY.bib").read_text(encoding="utf-8")
bibkeys = set(re.findall(r"^@[A-Za-z]+\{([^,]+),", bib, flags=re.MULTILINE))
unresolved_cites = sorted(set(cites) - bibkeys)
figures = re.findall(r"!\[[^\]]+\]\(([^)]+)\)", text)
missing_figures = sorted(path for path in figures if not (ROOT / path.split(" ", 1)[0]).is_file())
paragraphs = [re.sub(r"\s+", " ", p.strip()) for p in re.split(r"\n\s*\n", text) if len(p.split()) >= 25]
counts = Counter(paragraphs)
duplicate_paragraphs = {p: n for p, n in counts.items() if n > 1}
chapters = len(re.findall(r"^# (?:The |GWAS |Geometry |Linear |UMAP|densMAP|Repeated |HDBSCAN|Searching |Scoring |Validation,|Returning |From discovered|Worked |DIMPLE-GWAS in)", text, flags=re.MULTILINE))
result = {
    "status": "PASS" if not any(hits.values()) and not unresolved_cites and not missing_figures and not duplicate_paragraphs and chapters == 15 else "FAIL",
    "forbidden_hits": hits,
    "citation_keys_used": cites,
    "unresolved_citation_keys": unresolved_cites,
    "figure_references": figures,
    "missing_figures": missing_figures,
    "exact_duplicate_substantive_paragraph_count": len(duplicate_paragraphs),
    "textbook_chapter_count": chapters,
    "inline_math_count": len(re.findall(r"(?<!\\)\$[^$\n]+(?<!\\)\$", text)),
    "display_math_count": text.count("\n$$\n") // 2 if text.count("\n$$\n") % 2 == 0 else -1,
    "master_sha256": hashlib.sha256(MASTER.read_bytes()).hexdigest(),
}
REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["status"] == "PASS" else 1)
