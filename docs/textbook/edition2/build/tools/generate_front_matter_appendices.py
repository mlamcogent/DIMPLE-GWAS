#!/usr/bin/env python3
"""Generate TE2 front matter, appendices, and exercise solutions."""

from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path


EDITION2=Path(__file__).resolve().parents[2]
FREEZE3=EDITION2.parents[2]
FRONT=EDITION2/"front_matter"
APP=EDITION2/"appendices"
PY=EDITION2/"build/runtime_env/bin/python"
CLI=EDITION2/"build/runtime_env/bin/dimple-gwas"


def read_tsv(path):
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle,delimiter="\t"))


def help_text(command=None):
    argv=[str(CLI)] + ([command] if command else []) + ["--help"]
    return subprocess.run(argv,cwd=FREEZE3,text=True,capture_output=True,check=True).stdout.rstrip()


def main():
    FRONT.mkdir(parents=True,exist_ok=True); APP.mkdir(parents=True,exist_ok=True)
    title="""# DIMPLE-GWAS Freeze 3 RC1

## Academic Textbook and Analyst Reference

### Edition 2

**Internal review draft — prepared to public-facing editorial standard, not for external release**

Upasana Bhattacharyya, PhD  
Jibin John, PhD  
Zhong, Yuanxin, PhD  
Michael Preuss, PhD  
Tian Ge, PhD  
Todd Lencz, PhD  
Max Lam, PhD

Software version: `3.0.0rc1`  
Documentation date: 26 August 2026

> DIMPLE-GWAS Freeze 3 RC1 is a software-complete release candidate under current local and fixed-fixture evidence. It is not yet a scientifically frozen or cross-platform validated release.

The author order and degree convention follow the current manuscript. Affiliations, contribution statements, licensing, publisher metadata, DOI/ISBN, Docker validation, and final team adjudication remain pending for a public edition.
"""
    (FRONT/"00_title_and_authors.md").write_text(title,encoding="utf-8")
    status="""# Editorial and evidence status

Edition 2 is a documentation edition, not Freeze 4. It preserves the software identity and rebuilds the educational treatment from the current source, tests, fresh bounded teaching runs, historical evidence, and verified primary literature. The document is internally reviewable as a near-public manuscript, but it must not be represented as a public release while Docker, team adjudication, and cross-platform validation remain open.

Fresh Edition 2 evidence was produced on macOS arm64 with Python 3.12.13. The isolated suite passed 45 tests. Labs 0–3 passed; the fixed fixture passed 24 of 24 artifact checks and reproduced its partition exactly under ARI, NMI, noise-set Jaccard, and mapped membership, with near-zero Procrustes disparity. MNIST remains a protocol-only engineering benchmark. The fresh original 164-IDP 1,000-seed run is deferred until Docker by coordinator decision.

Private reviewer correspondence informed a sanitized method crosswalk only. No confidential text, private contact, protected identifier, or guessed reviewer citation belongs in the publication artifact. The exact Yang- and Zhao-attributed papers remain unresolved because the supplied record does not identify them. The genomic-components paper is correctly attributed to Oblong et al. (2024).

## What the status permits

Readers may use this draft to test pedagogy, inspect the complete software and output contracts, rehearse the bounded labs, review methods wording, and adjudicate scientific caveats. The draft supports no claim that Docker/Linux/cloud work is complete, that historical evidence is a fresh result, or that internal clustering diagnostics establish biological validity.
"""
    (FRONT/"01_editorial_and_evidence_status.md").write_text(status,encoding="utf-8")
    paths="""# Preface: four ways through the book

This book serves four readers without asking them to accept the same entry point. A newcomer should read Parts I and II before attempting Lab 1. An analyst familiar with statistical learning can begin with Chapters 6, 10, and 13–17, returning to the method chapters as questions arise. A statistics learner should follow the equations, hand calculations, and exercises through Chapters 3–12 and 18. A methods reviewer may begin with Chapters 1, 11, 12, 23, and 24, then use the function, output, claim, and reviewer crosswalk appendices.

The recurring movement is from question to geometry, from geometry to implementation, from implementation to retained output, and from output to a deliberately bounded statement. Commands are not isolated recipes. Each one sits in a provenance chain. Equations are not decoration. Each one is interpreted and connected to the behavior it helps explain. Figures are descriptive instruments whose captions state what not to infer.

## Conventions

`Freeze 3`, `Freeze 3 RC1`, and version `3.0.0rc1` refer to the software snapshot. `Edition 1` refers to the archived Analyst Manual. `Edition 2` or `TE2` refers to this textbook. “Current” means the checksummed source used for this build, not an unversioned online state. “Executed” means a retained local command record exists. “Historical” means the result was reconstructed from preserved artifacts rather than freshly fitted.

Paths in commands are relative to the Freeze 3 repository root. `<FREEZE3>` in an excerpt is an intentional sanitization token. Every example uses a new output directory because the software correctly refuses to overwrite a nonempty analytical result.
"""
    (FRONT/"02_preface_and_reader_paths.md").write_text(paths,encoding="utf-8")

    # Appendix A: exact CLI help, captured from the fresh environment.
    commands=["inspect-config","show-search-space","run","score-existing","summarize-models","reproduce-model","explain","interpret","compare","validate"]
    lines=["# Appendix A — Complete command-line reference","", "The following grammar was captured from the fresh Edition 2 environment. `interpret` is a compatibility alias for `explain`; both were executed in Lab 3. `python -m dimple_gwas` reaches the same dispatcher.","", "## Top-level dispatcher","", "```text",help_text(),"```"]
    for command in commands:
        lines += ["",f"## `{command}`","","```text",help_text(command),"```"]
    (APP/"A_complete_cli_reference.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

    config_rows=read_tsv(FREEZE3/"docs/manual/evidence/configuration_key_reference.tsv")
    lines=["# Appendix B — Complete configuration reference","", "Precedence is built-in mode, then recursively merged YAML, then explicit CLI values. The resolved configuration—not the overlay alone—is the executed method. Numeric ranges are half-open in the implemented expansion (`start` included, `stop` excluded).","", "| Key | Standard | Extended | Fixed | Custom | Meaning | CLI |", "| --- | --- | --- | --- | --- | --- | :---: |"]
    for r in config_rows:
        lines.append(f"| `{r['key']}` | `{r['standard_default']}` | `{r['extended_default']}` | `{r['fixed_default']}` | `{r['custom_default']}` | {r['meaning']} | {r['cli_exposure']} |")
    lines += ["", "Configuration validation checks modes, types, ranges, metrics, search ceilings, interpretation options, and incompatible settings. `inspect-config` is the authoritative preflight; `show-search-space` establishes candidate identity before fitting."]
    (APP/"B_complete_configuration_reference.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

    functions=read_tsv(EDITION2/"function_atlas/function_inventory.tsv")
    lines=["# Appendix C — Function atlas","", "The audited denominator is 110 package-defined symbols: 42 Tier A, 36 Tier B, and 32 Tier C. Every Tier A/B symbol has a complete 20-field dossier in `function_atlas/FUNCTION_DOSSIERS.md`; every Tier C symbol has a concise source/caller/input/output/error/test contract here and in the machine-readable table.","", "| Symbol | Tier | Source | Purpose | Signature | Direct output |", "| --- | :---: | --- | --- | --- | --- |"]
    for r in functions:
        lines.append(f"| `{r['qualified_symbol']}` | {r['tier']} | `{r['source_path']}:{r['source_line']}` | {r['purpose']} | `{r['input_signature']}` | {r['direct_outputs']} |")
    lines += ["", "Imported third-party callables are excluded from the denominator. Delegated behavior remains described in the statistical chapters and pinned environment. Zero direct symbol-name matches in tests are not automatically untested because integration routes can reach helpers through public callers."]
    (APP/"C_function_atlas.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

    output_text=(EDITION2/"output_atlas/OUTPUT_ATLAS.md").read_text(encoding="utf-8").replace("# DIMPLE-GWAS Freeze 3 RC1 output atlas","# Appendix D — Output atlas and schemas",1)
    (APP/"D_output_atlas_and_schemas.md").write_text(output_text,encoding="utf-8")

    troubleshooting=(FREEZE3/"docs/manual/chapters/43_error_messages_troubleshooting_and_recovery.md").read_text(encoding="utf-8")
    troubleshooting=re.sub(r"^# .*?\n", "# Appendix E — Errors, troubleshooting, and recovery\n",troubleshooting,count=1)
    troubleshooting += "\n## Recovery principle\n\nNever erase a failed run to make the record look clean. Preserve logs and failed candidate rows, correct the cause, and write to a new output directory. A statistical sensitivity is reported; it is not repaired as though it were a software exception.\n"
    (APP/"E_errors_troubleshooting_recovery.md").write_text(troubleshooting,encoding="utf-8")

    performance=(FREEZE3/"docs/manual/chapters/44_performance_memory_threading_and_bounded_run_guidance.md").read_text(encoding="utf-8")
    performance=re.sub(r"^# .*?\n", "# Appendix F — Performance, memory, and threading\n",performance,count=1)
    performance += "\n## Edition 2 measured teaching runs\n\nThe fixed one-candidate run and 32-candidate custom run both completed in under one minute on the recorded macOS arm64 host, but first-call JIT and library initialization dominated the tiny workload. Those runtimes cannot be linearly extrapolated to a 1,000-seed 164-IDP analysis. Preflight, bounded pilots, and explicit nested-thread controls are required before Docker sizing.\n"
    (APP/"F_performance_memory_threading.md").write_text(performance,encoding="utf-8")

    migration="\n\n".join((FREEZE3/p).read_text(encoding="utf-8") for p in [Path("docs/MIGRATION.md"),Path("docs/MIGRATION_FROM_DEV.md"),Path("docs/BACKWARD_COMPATIBILITY.md")])
    migration=re.sub(r"^# .*?\n","# Appendix G — Migration from Dev and Freeze 2\n",migration,count=1)
    (APP/"G_migration_from_dev_and_freeze2.md").write_text(migration,encoding="utf-8")

    concepts=read_tsv(EDITION2/"evidence/statistical_concept_coverage.tsv")
    lines=["# Appendix H — Mathematical notation","", "The main chapters derive the core expressions; this appendix provides a compact index.","", "| Concept | Notation or equation | Interpretation boundary |", "| --- | --- | --- |"]
    for r in concepts:
        lines.append(f"| {r['concept']} | `{r['equation_or_notation']}` | {r['interpretation_and_caution']} |")
    (APP/"H_mathematical_notation.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

    glossary=(FREEZE3/"docs/manual/appendices/A_glossary.md").read_text(encoding="utf-8")
    glossary=glossary.replace("# Appendix A — Glossary","# Appendix I — Glossary",1)
    existing=set(re.findall(r"^## (.+)$",glossary,re.M))
    for r in concepts:
        if r["concept"] not in existing:
            glossary += f"\n## {r['concept']}\n\n**{r['definition']}.** {r['interpretation_and_caution']}\n"
    (APP/"I_glossary.md").write_text(glossary,encoding="utf-8")

    chapter_specs={s[0]:s for s in __import__("draft_main_chapters").SPECS}
    lines=["# Appendix J — Exercise solutions and adjudication guide","", "Solutions emphasize reasoning and evidence boundaries. Equivalent calculations or commands are acceptable when they preserve the declared contract and reach the same defensible interpretation."]
    for chapter in range(1,25):
        if chapter==7:
            title="UMAP and densMAP"
            concept="fuzzy neighborhood graph"
            boundary="Coordinates remain descriptive, stochastic, and non-identifiable; densMAP regularizes density rather than proving biological density."
            worked="A valid answer recalculates distances or memberships, distinguishes delegated library behavior, and proposes a sensitivity design with fixed inputs and predeclared comparisons."
        else:
            spec=chapter_specs[chapter]
            title=spec[1]; concept=spec[7][0] if spec[7] else "workflow contract"; boundary=spec[5]; worked=spec[9]
        lines += ["",f"## Chapter {chapter}: {title}","",f"1. The unit must match the chapter definition; substituting people, variants, axes, or numeric label values for phenotype vectors is invalid unless the exercise explicitly changes scope.","",f"2. The notation answer must define every symbol for `{concept}` and state dimensions or denominators. Algebra without an interpretation earns incomplete credit.","",f"3. The source-trace answer names the exact callable, source location, caller, output, explicit/delegated error surface, and one edge-case test. Consult the function atlas rather than guessing.","",f"4. A correct artifact audit checks schema/version, row and identifier integrity, creation condition, status/failures, checksum/provenance, and privacy before reading substantive values.","",f"5. A defensible rewrite separates observed behavior from interpretation and includes this boundary: {boundary}","",f"6. Worked task: {worked} The solution must show intermediate values or retained command evidence and end with separate support and non-support statements."]
    (APP/"J_exercise_solutions.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

    bibliography=(EDITION2/"references/VERIFIED_BIBLIOGRAPHY.md").read_text(encoding="utf-8").replace("# Verified bibliography for Textbook Edition 2","# Appendix K — Verified bibliography",1)
    (APP/"K_verified_bibliography.md").write_text(bibliography,encoding="utf-8")

    claims=read_tsv(EDITION2/"evidence/claim_evidence_register.tsv")
    lines=["# Appendix L — Claim and evidence index","", "The TSV register is authoritative. Rejected wording appears here only so reviewers can see its disposition.","", "| Claim | Classification | Safe wording | Limitation | Location | Status |", "| --- | --- | --- | --- | --- | --- |"]
    for r in claims:
        lines.append(f"| {r['claim_id']} | {r['classification']} | {r['proposed_safe_wording']} | {r['limitation_or_counterpoint']} | {r['book_location']} | {r['status']} |")
    (APP/"L_claim_evidence_index.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

    reviewer="""# Appendix M — Sanitized reviewer-method crosswalk

The private reviewer record is evidence, not publishable correspondence. This crosswalk states only the method changes needed for team adjudication.

| Method issue | Edition 2 response | Evidence location | Remaining decision |
| --- | --- | --- | --- |
| Position Stage 1 among multivariate methods | Chapters 1, 4, and 24 compare questions and outputs without universal rankings. | Claim CMP-002/003; verified comparator papers | Team wording for manuscript alignment |
| Explain UMAP repetition and coordinate dependence | Chapters 7–8 derive the delegated objective, seed schedule, raw concatenation, distance identity, and limitations. | Source `umap_runner.py`; Labs 1–2 | Fresh 164-IDP sensitivity after Docker |
| Justify HDBSCAN settings and unassigned IDPs | Chapters 9–11 separate hierarchy, parameters, diagnostics, score, and `-1` interpretation. | Source/tests; output atlas | Scientific characterization in external data |
| Disclose selection | Chapters 11, 22, and 24 state that the historical solution was manually selected at sorted row 16, not automatic rank 1. | Checksummed historical reconstruction | Team adjudication of final language |
| Add practical workflow | Chapters 13–21 and Labs 0–3 provide executed commands, outputs, checksums, and interpretation. | Lab execution manifest | Cross-platform rerun |
| Separate technical and biological validation | Chapters 5 and 23 use a layered ladder and circularity safeguards. | Claim/validation registers | External biological design |
| Correct citations | Oblong et al. (2024) is correctly attributed; Zhang et al. (2023) is distinct. Yang/Zhao attributions remain unresolved and uncited. | Citation log and missing-evidence register | Exact papers, if intended, from team/reviewer record |

No confidential quotation, email address, reviewer identity, or private attachment path is reproduced.
"""
    (APP/"M_reviewer_method_crosswalk.md").write_text(reviewer,encoding="utf-8")

    status_matrix="""# Appendix N — Release-status and validation matrix

| Layer | Edition 2 evidence | Status |
| --- | --- | --- |
| Source identity | Package version and source/checksum inventory; Git metadata absent | pass with checksum fallback |
| Unit/integration tests | Fresh isolated run: 45 passed, five retained warnings | pass |
| Hand-worked implementation paths | Lab 0 preprocessing, RINT, silhouette, score, label comparison | pass |
| Fixed-fixture execution | One candidate, 24 vectors, three groups of eight, no candidate failure | pass, bounded |
| Bounded sensitivity | 32 candidates across four UMAP and eight HDBSCAN settings; all retained | pass, bounded |
| Reproduction/comparison | ARI/NMI/noise Jaccard/mapped membership 1; VI 0; Procrustes ~2.7e-31 | pass, same environment |
| Artifact validation | 24/24 checks | pass, bounded |
| Output atlas | 34/35 patterns freshly verified; opt-in coordinate associations not executed | pass with limitation |
| MNIST | Public engineering protocol only | bounded |
| Historical 164 IDPs | Counts and manual row-16 selection reconstructed | historical only |
| Fresh 164-IDP 1,000-seed run | Deferred until Docker by coordinator | pending |
| Docker/Linux/GCP/AWS | Not built or executed in this documentation task | pending |
| Statistical/biological/external validation | Not established by internal metrics/tutorials | pending external work |

No lower layer substitutes for a higher layer.
"""
    (APP/"N_release_status_validation_matrix.md").write_text(status_matrix,encoding="utf-8")

    docker=(FREEZE3/"docs/manual/DOCKER_CLOUD_SUPPLEMENT_HANDOFF.md").read_text(encoding="utf-8").replace("# Docker and cloud supplement handoff","# Appendix O — Docker and cloud handoff",1)
    docker=docker.replace("docs/manual/tutorials/01_fixed_synthetic/tutorial_config.yaml","docs/textbook/edition2/labs/01_fixed_synthetic/tutorial_config.yaml")
    (APP/"O_docker_cloud_handoff.md").write_text(docker,encoding="utf-8")
    print(f"Generated {len(list(FRONT.glob('*.md')))} front-matter and {len(list(APP.glob('*.md')))} appendix files")


if __name__=="__main__":
    main()
