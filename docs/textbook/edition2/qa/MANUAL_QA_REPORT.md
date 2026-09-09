# Edition 2 manual QA report

Date: 2026-08-26  
Status: internal review; prepared as close to public-facing as possible

## Outcome

All required QA artifacts were generated. There are no failed acceptance gates and no known post-remediation rendering defects. Gates B, E, F, G, H, I, and K pass with explicit limitations because Git identity is unavailable, two reviewer-attributed citations remain unidentified and uncited, bounded labs remain pending, one opt-in output was not freshly produced, and Docker/cross-platform/scientific adjudication are not complete.

## Quantitative checks

| Check | Result |
|---|---:|
| PDF pages rendered and visually inspected | 370/370 |
| Contact sheets inspected | 19 |
| Figures inspected | 21/21 |
| Known overlap, clipping, unreadable-label, or unresolved-reference defects | 0 |
| Chapters / appendices | 24 / 15 |
| Assembled regex word count | 109,808 |
| PDF extracted word count | 110,000 |
| Tables / numbered display equations | 35 / 9 |
| Function coverage rows passing | 110/110 |
| Tier A/B complete dossiers | 78/78 |
| Command interfaces verified | 13 |
| Used citation keys resolved | 23/23 |
| Verified bibliography records | 25 |
| Cross-reference failures | 0 |
| Publication-scope privacy findings across 44 files | 0 |
| Fresh isolated tests | 45 passed; 5 retained warnings |

## Visual remediation record

Edition 1's confirmed input-orientation, search-space, and provenance figure defects were replaced with bounded diagrams. During Edition 2 QA, Figure 16 initially read nonexistent comparison keys and displayed zeros; its data mapping was corrected, the PDF was rebuilt, and the final inspected figure shows four concordance values of 1.000. All 370 final pages were rasterized and reviewed through 19 contact sheets; all 21 figure sources and containing pages were also inspected.

## Editorial and scientific review

All 24 chapters meet the structural depth rubric (range 36–36 of 36), and the calibration chapter scored 99/100. The duplicate-prose audit found 265 normalized exact groups and 22 high-similarity pairs among 1296 substantive paragraphs. These are logged rather than hidden: much of the repetition is deliberate function-contract traceability, while optional compression remains a team-adjudication task. Scientific claims remain explicitly separated into implemented, freshly executed, historical, literature-supported, and pending categories.

## Acceptance gates

| Gate | Name | Status | Limitation / next step |
|---|---|---|---|
| A | Baseline diagnosis | pass | none |
| B | Evidence integrity | pass_with_limitation | No usable Git identity; SHA-256 identity is authoritative. Two reviewer-attributed sources remain unidentified and uncited. |
| C | Function completeness | pass | none |
| D | Statistical textbook depth | pass | Team scientific adjudication is still required before public release. |
| E | Executable learning | pass_with_limitation | Labs 0–3 executed. Lab 4 is protocol-only; Lab 5 fresh 164-IDP/1,000-seed execution is deferred until Docker. |
| F | Output completeness | pass_with_limitation | 35/35 patterns documented and 34/35 freshly verified; opt-in coordinate-association artifact was not executed. |
| G | Scientific calibration | pass_with_limitation | Text is calibrated; biological, Docker, and cross-platform validation remain pending. |
| H | Citation integrity | pass_with_limitation | 25 sources verified; Yang/Zhao attributions remain unresolved and are not cited. |
| I | Editorial coherence | pass_with_limitation | Repeated contract prose is retained for reference traceability; team adjudication should decide any final compression. |
| J | Visual and typesetting quality | pass | none; all 370 pages and 21 figures inspected after remediation |
| K | Reproducibility and handoff | pass_with_limitation | Build Docker image, rerun the full 164-IDP/1,000-seed protocol, and complete Linux/container/cross-platform validation. |

## Release boundary

This artifact is not yet a public release. Before release, the team should build the Docker image, run the retained 164-IDP/1,000-seed protocol in that image, complete Linux/container and any required cross-platform comparison, identify or formally retire the Yang/Zhao reviewer attributions, adjudicate the scientific text, and decide whether to compress repeated reference-contract prose.
