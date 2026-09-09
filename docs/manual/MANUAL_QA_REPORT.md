# Manual QA report

Result: **PASS**. Checks: 19; pass: 17; pass with limitation: 2; fail: 0.

| ID | Area | Status | Evidence | Result / remediation |
| --- | --- | --- | --- | --- |
| ED-001 | editorial | `pass` | `chapters/` | Found 46 modular chapters. |
| ED-002 | editorial | `pass` | `appendices/` | Found 8 appendices. |
| ED-003 | editorial | `pass` | `DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.md` | Compiled edition contains 46 unique numbered chapter headings and 20778 whitespace-delimited words. |
| ED-004 | pedagogy | `pass` | `chapters/` | Every chapter contains the teaching contract. |
| TECH-001 | links | `pass` | `build/qa/manual_qa.json` | Checked 73 local Markdown asset/navigation links; broken=0. |
| TECH-002 | commands | `pass` | `evidence/command_and_flag_matrix.tsv; build/logs/cli_help/` | All 9 canonical commands appear in the implementation-derived matrix; interpret alias is recorded with explain. |
| TECH-003 | tutorials | `pass` | `evidence/tutorial_execution_manifest.tsv; tutorials/*/execution_manifest.json` | Tutorials 1–3 contain 12 executed steps and all recorded exit codes are zero; Tutorials 4–5 are explicitly historical/protocol-only. |
| TECH-004 | outputs | `pass` | `evidence/output_producer_consumer_map.tsv; evidence/output_atlas.tsv` | All 35 producer-map artifact patterns appear in the atlas; three in-memory non-artifacts are also documented. |
| TECH-005 | configuration | `pass` | `evidence/configuration_key_reference.tsv` | Implementation-derived reference contains 57 configuration keys/rows. |
| TECH-006 | tests | `pass` | `build/logs/pytest_full.log; evidence/test_execution_report.md` | Fresh isolated suite reports 45 passed and four visible warnings. |
| SCI-001 | scientific language | `pass` | `compiled manual; evidence/claim_evidence_register.tsv` | High-risk interpretation boundaries are present. |
| SCI-002 | scientific scan | `pass` | `compiled manual` | Unsafe affirmative-pattern hits: {'axes_as_loadings': 0, 'noise_nonpleiotropic': 0, 'dbcv_default_score': 0, 'pinned_guarantee': 0, 'fresh_164_claim': 0}. |
| CIT-001 | citations | `pass` | `references/dimple_gwas_manual.bib; evidence/citation_verification_log.tsv` | BibTeX entries=15; brace balance=True; verified citation rows=18; DOI rows=15. |
| CIT-002 | reviewer attribution | `pass_with_limitation` | `evidence/reviewer_reference_crosswalk.tsv; references/VERIFIED_BIBLIOGRAPHY.md` | Oblong/Zhang attribution is corrected. Exact Yang/Zhao reviewer works remain unresolved and are not guessed. |
| RENDER-001 | figures | `pass` | `evidence/figure_source_manifest.tsv` | Verified 26 figure/diagram source or rendered rows; mismatches=[]. |
| RENDER-002 | PDF | `pass` | `DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.pdf; build/qa/pdf_pages_v4; build/qa/pdf_contacts_v4` | Latest PDF is 122 A4 pages; every page rendered to PNG and all pages were visually inspected across 11 numbered contact sheets. No clipping, overflow, broken image, margin collision, or blank failure was observed. |
| RENDER-003 | HTML | `pass` | `DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.html; build/logs/manual_html_build_v4.log` | Self-contained HTML embeds CSS and images and contains no developer absolute path. |
| PRIV-001 | privacy | `pass` | `published Markdown/HTML source set` | Published-edition scan hits: {'developer_path': 0, 'developer_name': 0, 'secret_assignment': 0}. |
| PRIV-002 | privacy | `pass_with_limitation` | `tutorials/ executed evidence` | Raw/internal executed evidence contains 66 local absolute-path occurrences required for provenance. Exclude or sanitize this evidence layer in any public distribution while retaining checksums/private originals; the rendered manual is clean. |

## Visual inspection

The latest 122-page A4 PDF was rendered at 110 dpi into one PNG per page. All pages were inspected in eleven numbered contact sheets. Title/contents, part dividers, 46 chapters, code blocks, diagrams, quantitative figures, mathematical appendix, bibliography, tables, clean page margins, and final appendices render without clipping, overlap, or broken images. Sparse pages are deliberate part/appendix dividers or short completion pages; none is an unintended blank failure.

## Named limitations

- Exact Yang/Zhao reviewer-cited works cannot be identified from the supplied Reviewer #2 register and remain unresolved rather than inferred.
- Raw executed tutorial evidence retains local absolute paths for private provenance. The Markdown/HTML/PDF edition is clean; a public package must exclude or deliberately sanitize raw evidence while preserving private originals and checksums.
- The fresh full 164-IDP 1,000-seed run and Docker/Linux/GCP/AWS validation are pending by design.
- The PDF renderer reports benign Type-3-glyph bounding-box warnings for mathematical glyphs; every affected page rendered visibly and legibly.
