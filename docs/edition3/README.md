# DIMPLE-GWAS Freeze 3 RC1 - Documentation Edition 3

Documentation Edition 3 is a reader-first reconstruction of the DIMPLE-GWAS documentation. It is organized as three coordinated reading modes:

1. `textbook/` develops the statistical and scientific ideas as a continuous 15-chapter narrative.
2. `workbook/` turns those ideas into a progressive analyst journey with nine evidence-labelled labs.
3. `reference/` provides exact command, configuration, function, output, error, and provenance contracts.

The continuous reader-facing build is assembled as:

- `DIMPLE_GWAS_FREEZE3_RC1_DOCUMENTATION_EDITION3.md`
- `DIMPLE_GWAS_FREEZE3_RC1_DOCUMENTATION_EDITION3.html`
- `DIMPLE_GWAS_FREEZE3_RC1_DOCUMENTATION_EDITION3.pdf`
- `DIMPLE_GWAS_FREEZE3_RC1_DOCUMENTATION_EDITION3.docx`

Start with `QUICKSTART.md` if the immediate goal is to run the fixed synthetic learning path. Start with textbook Chapter 1 if the goal is to understand the method before using it.

## Status

This is a documentation draft for scientific and editorial review. DIMPLE-GWAS Freeze 3 RC1 (`3.0.0rc1`) is a software-complete release candidate under the available local tests, fixed-fixture regression, and retained-output evidence. It is not yet a final scientific freeze or a fully qualified cross-platform release. The fresh historical 164-IDP 1,000-seed rerun and Docker/Linux/GCP/AWS qualification remain separate gates.

Stage 1 evidence is preserved under `evidence/`. Authoring proceeds under its `PASS_WITH_LIMITATIONS` decision. The main unresolved limits are collected in `KNOWN_LIMITATIONS_AND_PENDING_VALIDATION.md`.

## Build policy

The modular Markdown files are the maintainable source. Build products are generated from one ordered source list. Scientific code, configurations, tests, Edition 2, historical evidence, and reviewer materials are not modified by this documentation build.
