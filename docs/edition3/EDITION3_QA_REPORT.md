# Documentation Edition 3 QA report

## Decision

**Reader-draft QA: PASS WITH RELEASE LIMITATIONS.** The documentation artifacts are internally coherent, readable, traceable to Stage 1, and suitable for author read-through. This decision does not upgrade the scientific or cross-platform release boundary.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| Stage 1 authority | Pass with limitations | `evidence/13_STAGE1_GATE_REPORT.md` |
| Content and citation resolution | Pass | 32 used citation keys resolved; no unresolved keys; no duplicate substantive paragraphs |
| Contents integrity | Pass | 43 entries across two pages; every displayed page number remapped against and confirmed by the final 105-page PDF |
| Mathematical notation | Pass | 159 inline expressions and 31 display equations declared; 196 Word mathematical objects; 190 HTML MathML elements; no raw TeX tokens in PDF text |
| Figure and link integrity | Pass | Five figures found and embedded; no missing figures, private paths, tool tokens, tracking parameters, or placeholders |
| HTML integrity | Pass | Populated navigation contents; five embedded images; ten semantic tables; 190 MathML elements; blue code styling; zero replacement characters |
| DOCX structure and privacy | Pass | Real heading styles; five inline figures; 196 native math objects; 236 inline-code runs; 43 contents leaders; no tables after compatibility transformation; privacy scrub completed |
| Accessibility | Pass | Zero high, medium, or low findings in the final DOCX audit |
| Page rendering | Pass | 105 pages measured; zero near-blank or edge-touch flags; six contact sheets and targeted full pages reviewed |
| PDF integrity | Pass | Tagged 105-page Letter PDF; 24,769 extractable words; zero raw TeX, stray converter-marker, placeholder, private-path, or replacement-character hits |
| Software regression | Pass with one optional skip | 44 passed, 1 optional XLSX test skipped because `openpyxl` is absent, 5 warnings preserved |
| Package source identity | Pass | Digest stability test retained `df87825992ab51dc016c673cf420a978ba5c161bd6c755e00a5199ead310e65b` |

## Visual review finding and correction

The first DOCX render exposed a severe compatibility defect: Pandoc tables appeared as sparse content with empty grids and spill pages under the available LibreOffice renderer. Adding table borders made the defect visible but did not fix pagination. The final build therefore converts the ten tables to compact labelled rows only for DOCX/PDF compilation. The final corrected render is 105 pages, removes blank spill pages, retains every cell value, and passes the repeated full-page review. Markdown and HTML retain their native tables.

## Reader-correction validation

The contents section was generated in two passes: headings were first located in the rendered PDF, their physical page numbers were written into the source, and the final PDF was remapped. The before/after page-map digest was identical on the final verification pass. Inline notation and display equations were independently checked in the source, DOCX XML, HTML, rendered pages, and PDF extraction. Software parameters retain monospace styling and use the same restrained blue as the hierarchy. The DOCX/PDF build deliberately unwraps Word hyperlinks because the available LibreOffice renderer exposed their bookmarks as visible `X` glyphs; URLs remain printed, and HTML keeps live links.

## Release limitations carried forward

- The fresh historical 164-IDP 1,000-seed rerun remains pending.
- Raw matrices for the 2,315- and 459-object manuscript analyses remain absent; the 459 parameter record conflicts.
- Real-data stability, independent biological validation, and matched method benchmarks remain incomplete.
- Docker, Linux, x86-64, cloud, and cross-library qualification remain untested.
- The optional XLSX test remains skipped in the retained environment.
- There is no Git commit or signed release tag.

The complete reader-facing list is `KNOWN_LIMITATIONS_AND_PENDING_VALIDATION.md`; machine-readable build identities are in `EDITION3_BUILD_MANIFEST.json`.
