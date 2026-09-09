# Documentation Edition 3 build report

## Outcome

The reader draft built successfully from the Stage 1 evidence pack and unchanged Freeze 3 RC1 package source. The final set contains Markdown, self-contained HTML, privacy-scrubbed DOCX, and PDF editions. This is a documentation build; it does not modify scientific code, tests, configurations, retained analyses, Edition 2, or Stage 1 evidence.

## Authority and release boundary

- Stage 1 gate: `PASS_WITH_LIMITATIONS`.
- Package: DIMPLE-GWAS `3.0.0rc1`.
- Package-source SHA-256: `df87825992ab51dc016c673cf420a978ba5c161bd6c755e00a5199ead310e65b`.
- Documentation master SHA-256 before compilation: `05cf1c4b5de638d00f751c603a834c6e325d39b377267386e8b8a0ceeb98eefb`.
- Source identity remained stable under the package digest regression test.

## Build profile

- 15 academic textbook chapters.
- 9 analyst workbook labs plus troubleshooting and solutions.
- 6 technical reference modules and 2 appendices.
- Approximately 21,900 whitespace-counted words in the Markdown source; 24,769 words extractable from the compiled PDF, including the populated contents section, mathematical notation, running matter, labels, and bibliography.
- 5 original diagrams.
- 10 semantic Markdown/HTML tables, represented as compact labelled rows in DOCX/PDF for renderer compatibility.
- 159 inline mathematical expressions and 31 display equations; 196 native Word mathematical objects after compilation.
- 43 verified contents entries across two pages.
- 105 rendered Letter pages.

## Build route

1. Assemble the ordered modular Markdown sources.
2. Resolve citations against the verified Stage 1 BibTeX library.
3. Build self-contained HTML with embedded figures and stylesheet.
4. Prepare a DOCX-safe source in which complex tables become labelled rows and the contents section is materialized with verified physical page numbers.
5. Compile with the Edition 3 reference document, native equation objects, and blue monospace software parameters; then apply the narrative-proposal style.
6. Remove revision-session, personal, and custom Word metadata.
7. Render the DOCX to 105 page PNGs and emit the PDF.
8. Inspect every page through six contact sheets and targeted full-page views.
9. Run content, accessibility, image, heading, style, PDF-text, privacy, and software checks.

## Delivered reader files

- `DIMPLE_GWAS_FREEZE3_RC1_DOCUMENTATION_EDITION3.md`
- `DIMPLE_GWAS_FREEZE3_RC1_DOCUMENTATION_EDITION3.html`
- `DIMPLE_GWAS_FREEZE3_RC1_DOCUMENTATION_EDITION3.docx`
- `DIMPLE_GWAS_FREEZE3_RC1_DOCUMENTATION_EDITION3.pdf`

Exact sizes and SHA-256 values are recorded in `EDITION3_BUILD_MANIFEST.json`.

## Rebuild note

The maintainable sources are the files under `textbook/`, `workbook/`, and `reference/`. `build/tools/assemble_edition3.py` creates the master Markdown. The HTML and DOCX use different table representations only at compile time; the underlying cell content is the same. Build intermediates and rendered QA pages remain under `build/` and `qa/`.
