#!/usr/bin/env python3
"""Assemble the modular manual, front matter, quickstart, and HTML source styling."""

from __future__ import annotations

import csv
import json
import re
from datetime import date
from pathlib import Path


FREEZE3 = Path(__file__).resolve().parents[4]
MANUAL = FREEZE3 / "docs" / "manual"
CHAPTERS = MANUAL / "chapters"
APPENDICES = MANUAL / "appendices"
EVIDENCE = MANUAL / "evidence"
EDITION = "25 August 2026"


PARTS = [
    (1, "Part I — Orientation and conceptual foundations"),
    (9, "Part II — Installation, data preparation, and the first successful run"),
    (15, "Part III — The complete DIMPLE-GWAS workflow"),
    (24, "Part IV — Explainability and responsible interpretation"),
    (32, "Part V — Worked case studies"),
    (37, "Part VI — Operational reference"),
]


def anchor(text: str) -> str:
    value = re.sub(r"[^a-z0-9 _-]", "", text.lower()).replace(" ", "-")
    return re.sub(r"-+", "-", value).strip("-")


def rows() -> list[dict[str, str]]:
    with (EVIDENCE / "learning_objectives.tsv").open(encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def compiled_chapter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    text = text.replace("](../assets/", "](assets/")
    pattern = re.compile(
        r"```mermaid\s+.*?```\s+\*([^*]+?)\. Editable source: `assets/diagrams/([^`]+\.mmd)`\.\*",
        flags=re.DOTALL,
    )
    def replacement(match: re.Match[str]) -> str:
        caption = match.group(1).strip()
        source = match.group(2)
        svg = str(Path(source).with_suffix(".svg"))
        return f"![{caption}](assets/diagrams/{Path(svg).name})\n\n*{caption}. Editable source: `assets/diagrams/{source}`.*"
    return pattern.sub(replacement, text)


def title_and_toc(chapter_rows: list[dict[str, str]], source_hash: str) -> str:
    toc = ["## Contents", ""]
    current_part = None
    part_by_start = dict(PARTS)
    for row in chapter_rows:
        number = int(row["chapter"])
        if number in part_by_start:
            current_part = part_by_start[number]
            toc.extend([f"- **{current_part}**"])
        title = f"{number}. {row['title']}"
        toc.append(f"  - [{title}](#{anchor(title)})")
    toc.extend(["- **Appendices**"])
    for path in sorted(APPENDICES.glob("*.md")):
        heading = path.read_text(encoding="utf-8").splitlines()[0].removeprefix("# ")
        toc.append(f"  - [{heading}](#{anchor(heading)})")
    return f"""---
title: "DIMPLE-GWAS Freeze 3 RC1 Analyst Manual"
subtitle: "First-draft textbook and operational reference"
date: "{EDITION}"
lang: en-GB
---

<div class="page-header">DIMPLE-GWAS Freeze 3 RC1 Analyst Manual</div>
<div class="page-footer">RC1 first draft · {EDITION}</div>

<div class="title-page">

# DIMPLE-GWAS Freeze 3 RC1 Analyst Manual

## First-draft textbook and operational reference

**Software version:** `3.0.0rc1`  
**Manual edition:** {EDITION}  
**Source identity:** package-source SHA-256 `{source_hash}`  
**Git identity:** unavailable in the supplied snapshot; checksum identity is used.

> **Release status**  
> **DIMPLE-GWAS Freeze 3 RC1 is a software-complete release candidate. It is not yet a scientifically frozen or cross-platform validated release.**

Fresh local evidence includes a 45-test pass, executed Tutorials 1–3, and bounded fixed-fixture comparison/validation. Historical 164-IDP reconstruction is separated from the pending fresh 1,000-seed run. Docker, Linux, GCP, and AWS packaging/validation are deliberately outside this build.

</div>

{chr(10).join(toc)}

## How to use this book

- New analysts: Chapters 1, 3–4, and 9–14, then the `QUICKSTART.md` workflow.
- Operators: Parts III and VI plus the machine-readable output atlas.
- Methods reviewers: Parts I and IV, the case-study boundaries, verified bibliography, and claim/evidence index.

Every chapter labels implementation behavior, evidence, mistakes, and limits. Defaults, tutorial settings, historical settings, and recommendations are not interchangeable.

## Pending validation at a glance

| Gate | Current status |
| --- | --- |
| Local software/tests | Pass: 45 tests, macOS arm64 |
| Fixed-fixture run/compare/validate | Pass, bounded to the executed fixture/environment |
| Historical 164-IDP reconstruction | Historical-only; manual row-16 choice disclosed |
| Fresh 164-IDP 1,000-seed search | Deferred until Docker phase |
| Statistical and biological validation | Not established by this manual build |
| Docker/Linux/GCP/AWS | Not built or tested |
"""


def quickstart() -> str:
    return """# DIMPLE-GWAS Freeze 3 RC1 — Quickstart

> RC1 is software-complete under local/fixed-fixture evidence. It is not scientifically frozen or cross-platform validated.

This is the shortest verified novice workflow. Start in a terminal, replace `/path/to/DIMPLE-GWAS-freeze3` with the repository location, and choose output directory names that do not already exist.

## 1. Create and verify an isolated environment

```bash
cd /path/to/DIMPLE-GWAS-freeze3
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[test,plots]'
dimple-gwas --version
python -m pip check
```

Expected version: `3.0.0rc1`. If it differs, stop and record the installed source/version before using this edition.

## 2. Inspect and enumerate before fitting

```bash
dimple-gwas inspect-config \
  --search-mode fixed \
  --config docs/manual/tutorials/01_fixed_synthetic/tutorial_config.yaml

dimple-gwas show-search-space \
  --search-mode fixed \
  --config docs/manual/tutorials/01_fixed_synthetic/tutorial_config.yaml \
  --output-dir docs/manual/tutorials/01_fixed_synthetic/search_space_NEW
```

The fixture configuration must enumerate one candidate. `NEW` is a placeholder: use a unique name.

## 3. Run the bounded fixture

```bash
dimple-gwas run \
  --search-mode fixed \
  --config docs/manual/tutorials/01_fixed_synthetic/tutorial_config.yaml \
  --output-dir docs/manual/tutorials/01_fixed_synthetic/run_NEW
```

## 4. Inspect before interpreting

Check these files in `run_NEW`:

- `run_manifest.json`: status, version, source/input/config hashes, seeds, threads, backends, counts, selected model;
- `search_space_manifest.tsv`: exactly one candidate;
- `models/all_models.tsv`: one retained candidate row with visible status/errors;
- `models/model_selection_manifest.json`: formula, counts, tie order, selected model;
- `models/top_model_artifacts/<model_id>/labels.tsv`: 24 unique fixture IDs;
- `logs/run.log` and `logs/model_failures.tsv`.

For this designed fixture, the verified run yielded three clusters of eight and no noise. That is a structural smoke-test assertion, not a production target or biological claim.

## 5. Validate your new run

```bash
dimple-gwas validate \
  --run-dir docs/manual/tutorials/01_fixed_synthetic/run_NEW \
  --output-dir docs/manual/tutorials/01_fixed_synthetic/validation_NEW
```

Read every row of `validation_checks.tsv`; do not rely only on the exit code.

Next: Chapters 10–14 explain the contract; Chapters 18–23 explain model search/selection/reproduction; Chapters 24–30 explain safe interpretation.
"""


def readme(chapter_rows: list[dict[str, str]]) -> str:
    chapter_links = []
    for row in chapter_rows:
        number = int(row["chapter"])
        match = next(CHAPTERS.glob(f"{number:02d}_*.md"))
        chapter_links.append(f"- [{number}. {row['title']}](chapters/{match.name})")
    return f"""# DIMPLE-GWAS Freeze 3 RC1 Analyst Manual sources

This directory contains the complete first-draft textbook, executable tutorial evidence, source-derived reference maps, figures/diagrams, and the later Docker/cloud handoff.

Primary navigation:

- [Quickstart](QUICKSTART.md)
- [Compiled Markdown manual](DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.md)
- `DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.html` — generated navigable edition
- `DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.pdf` — rendered edition after PDF QA
- [Build report](MANUAL_BUILD_REPORT.md)
- [QA report](MANUAL_QA_REPORT.md)
- [Docker/cloud handoff](DOCKER_CLOUD_SUPPLEMENT_HANDOFF.md)

## Modular chapters

{chr(10).join(chapter_links)}

## Maintenance workflow

1. Treat executable source and fresh artifacts as authority.
2. Update claim/software/output/citation evidence before changing authoritative prose.
3. Regenerate source maps, runtime evidence, figures, curriculum, chapters, and the compiled edition with the scripts under `build/tools/`.
4. Never overwrite a prior tutorial output; use a new root and regenerate manifests/checksums.
5. Rerun tests, command/output QA, privacy scans, link checks, and PDF page inspection.
6. Preserve the RC1 status banner until every corresponding release gate has direct evidence.

The isolated build environment under `build/runtime_env/` is ignored and is not a deliverable. Markdown is the maintainable authority; HTML/PDF are rendered products.
"""


CSS = """@page { size: A4; margin: 18mm 17mm 19mm 17mm; }
:root { --ink:#182635; --blue:#0b5f8a; --pale:#eaf3f8; --warn:#fff4d6; --line:#b6c4ce; }
html { background:#eef2f5; }
body { max-width: 920px; margin: 0 auto; background:white; color:var(--ink); font-family: Inter, Aptos, Arial, sans-serif; line-height:1.48; padding:42px 58px; }
h1,h2,h3 { color:#123d57; line-height:1.18; break-after:avoid-page; }
h1 { border-bottom:2px solid #6fa3bd; padding-bottom:.25em; margin-top:1.5em; }
h2 { margin-top:1.25em; }
p, li { orphans:3; widows:3; }
blockquote { margin:1em 0; padding:.7em 1em; border-left:5px solid #d79c00; background:var(--warn); }
code { font-family: "SFMono-Regular", Consolas, monospace; font-size:.88em; background:#f2f5f7; padding:.08em .25em; }
pre { background:#152534; color:#f5f8fa; padding:12px 14px; border-radius:5px; overflow-wrap:anywhere; white-space:pre-wrap; break-inside:avoid; }
pre code { background:transparent; color:inherit; padding:0; }
.xref { font-size:.86em; color:#52616b; border-top:1px dotted #c3cdd3; padding-top:.45em; break-inside:avoid; }
table { width:100%; border-collapse:collapse; font-size:.88em; break-inside:auto; }
th,td { border:1px solid var(--line); padding:6px 7px; vertical-align:top; }
th { background:var(--pale); text-align:left; }
tr { break-inside:avoid; }
img, svg { display:block; max-width:100%; height:auto; margin:12px auto; break-inside:avoid; }
a { color:var(--blue); }
.title-page { min-height:82vh; display:flex; flex-direction:column; justify-content:center; text-align:center; break-after:page; }
.title-page h1 { font-size:2.25em; border:0; }
.title-page blockquote { text-align:left; }
.page-header,.page-footer { display:none; }
hr { border:0; border-top:1px solid var(--line); margin:2em 0; }
@media print {
  html { background:white; }
  body { max-width:none; margin:0; padding:0; font-size:10.2pt; }
  .page-header,.page-footer { display:none !important; }
  h1 { break-before:page; }
  .title-page h1 { break-before:auto; }
  a { color:inherit; text-decoration:none; }
}
"""


def main() -> None:
    chapter_rows = rows()
    run = json.loads((MANUAL / "tutorials" / "02_custom_search_space" / "run_20260825" / "run_manifest.json").read_text(encoding="utf-8"))
    sections = [title_and_toc(chapter_rows, run["package_source_sha256"])]
    part_by_start = dict(PARTS)
    for row in chapter_rows:
        number = int(row["chapter"])
        if number in part_by_start:
            sections.extend(["\n<div class=\"part-page\"></div>\n", f"# {part_by_start[number]}"])
        path = next(CHAPTERS.glob(f"{number:02d}_*.md"))
        sections.append(compiled_chapter(path))
    sections.append("# Appendices")
    sections.extend(path.read_text(encoding="utf-8") for path in sorted(APPENDICES.glob("*.md")))
    compiled = "\n\n".join(sections).strip() + "\n"
    (MANUAL / "DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.md").write_text(compiled, encoding="utf-8")
    (MANUAL / "QUICKSTART.md").write_text(quickstart(), encoding="utf-8")
    (MANUAL / "README.md").write_text(readme(chapter_rows), encoding="utf-8")
    styles = MANUAL / "assets" / "styles"
    styles.mkdir(parents=True, exist_ok=True)
    (styles / "manual.css").write_text(CSS, encoding="utf-8")


if __name__ == "__main__":
    main()
