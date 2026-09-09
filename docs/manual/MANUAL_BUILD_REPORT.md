# DIMPLE-GWAS Freeze 3 RC1 manual-build report

## Coordinator summary

The complete first-draft textbook has been assembled in `DIMPLE-GWAS-freeze3/docs/manual/`. It is grounded in the supplied Freeze 3 implementation, fresh local tests and bounded tutorials, historical IDP evidence, reviewer correspondence, and verified primary literature. The edition is suitable for analyst review and iteration, but it deliberately does not claim scientific freeze or cross-platform validation.

| Identity item | Verified value |
| --- | --- |
| Repository | `DIMPLE-GWAS-freeze3` within the supplied workspace |
| Package | DIMPLE-GWAS `3.0.0rc1` |
| Manual edition | 25 August 2026 |
| Package-source SHA-256 | `df87825992ab51dc016c673cf420a978ba5c161bd6c755e00a5199ead310e65b` |
| Git commit/tag | Unavailable in the supplied snapshot; source and artifact checksums are used |
| Release label | Freeze 3 RC1, software-complete under local/fixed-fixture evidence; not scientifically frozen or cross-platform validated |

## Primary deliverables

- `DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.md`: maintainable compiled Markdown textbook.
- `DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.html`: self-contained navigable HTML edition.
- `DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.pdf`: 122-page A4 rendered edition.
- `QUICKSTART.md`: shortest verified novice workflow.
- `chapters/`: 46 modular teaching chapters.
- `appendices/`: eight appendices covering glossary, equations, bibliography, reviewer crosswalk, claims, checksums, status, and later handoff.
- `tutorials/`: five tutorial packages with executed or explicitly bounded status.
- `evidence/`: inventories, checksums, claim/citation registers, software maps, runtime evidence, output atlas, curriculum, and figure provenance.
- `MANUAL_QA_REPORT.md` and `build/qa/manual_qa.json`: human- and machine-readable acceptance results.
- `DOCKER_CLOUD_SUPPLEMENT_HANDOFF.md`: exact next-stage packaging and validation contract.

## Tutorial execution

| Tutorial | Status | Result |
| --- | --- | --- |
| 1 — fixed synthetic | Executed fresh | One fixed candidate; 24 vectors by 80 variables; selected `model_060fac0208bb58e2`; three clusters of eight; zero noise. The corrected canonical run is `run_20260825_v2`; the earlier annotation-join attempt is retained as provenance. |
| 2 — custom bounded search | Executed fresh | 32/32 candidates succeeded; selected `model_241ad5e99af55074`; three clusters; zero noise; four UMAP-family score bands with visible ties. |
| 3 — explain, compare, validate | Executed fresh | Six downstream commands exited zero. Partition comparison produced ARI, NMI, noise-set Jaccard, and mapped-membership agreement of 1; Procrustes disparity was approximately `2.71e-31`; validation passed 24/24 checks. |
| 4 — MNIST | Historical, bounded | Prior benchmark evidence is documented with its configuration and 273.47-second historical runtime. It was not rerun because it is a software benchmark rather than a release gate for this manual build. |
| 5 — original 164 IDPs | Historical/protocol-only | Historical labels and selection evidence are reconstructed; the fresh 1,000-seed run is deferred until the Docker stage at the user's direction. |

Every executed Tutorial 1–3 command is listed in `evidence/tutorial_execution_manifest.tsv`, with command, working directory, inputs/configuration, thread/seed settings, exit code, logs, artifacts, hashes, assertions, and manual use. Machine-readable manifests live within each tutorial.

## Tests and environment

- Fresh isolated editable install from `.[test,plots]` completed successfully.
- Full suite: **45 passed**, with four retained warnings and no test failures.
- `pip check`: clean.
- Host evidence: macOS arm64; Python 3.12.13.
- Principal resolved packages included NumPy 2.5.2, SciPy 1.18.1, pandas 3.0.5, scikit-learn 1.9.0, UMAP 0.5.12, hdbscan 0.8.44, Matplotlib 3.11.1, and Plotly 6.9.0.
- The isolated build runtime is intentionally ignored as a generated environment; its exact resolved dependency record is retained in `evidence/resolved_dependencies.txt`.

## Evidence and citation remediation

- Twenty-five material claims were classified and linked to implementation, internal evidence, limitations, and primary citations.
- Known high-risk Gemini statements were corrected: repeated UMAP is an empirical strategy rather than a topology/determinism theorem; HDBSCAN `-1` is algorithmic noise/unassigned status rather than a biological class; DBCV is a diagnostic rather than the `legacy_dimple` score; silhouette is metric-aware; UMAP axes are not loadings; original-space correlations are descriptive and post-selection; comparator methods are not universal winners or failures.
- The comparator matrix distinguishes clustering, dimensionality reduction, and multivariate association procedures instead of presenting unlike inferential tasks as direct competitors.
- The Oblong et al. (2024) PCA/ICA paper attribution was corrected and verified. Zhang et al. (2023) is recorded as a different pleiotropy work.
- The exact Yang- and Zhao-attributed reviewer papers cannot be identified from the supplied action register. They remain explicitly unresolved; no citation was guessed.
- Fifteen BibTeX records and 18 verified citation-log rows use primary/stable records where available.

## Original-IDP status

The manual verifies and reports the historical record as historical evidence: 164 IDs, 102 historical noise assignments, and five non-noise clusters of 9, 13, 15, 14, and 11. It discloses the historical manual sorted-row-16 selection with epsilon 0, minimum samples 4, and minimum cluster size 6. One historical `UMAP_3` coordinate is missing, while labels are complete.

This is not a fresh Freeze 3 reconstruction. The full 164-IDP 1,000-seed search remains pending by design. The later run must use a checksum-verified authoritative matrix, a new output root, the documented configurations, complete candidate/failure retention, and predeclared comparison criteria. Historical resemblance must not be used to tune the fresh result.

## Acceptance gates

| Gate | Status | Evidence and boundary |
| --- | --- | --- |
| A — Evidence integrity | Pass | Source hierarchy, 346-row inventory, authority/conflict map, missing-evidence register, and SHA-256 source checksums are present. Missing Git identity and raw-data ambiguities remain named rather than inferred. |
| B — Claim/citation integrity | Pass with named limitation | Material claims and high-risk corrections are registered; primary citations are verified. Exact Yang/Zhao reviewer works remain unresolved. |
| C — Software truth | Pass | Nine canonical commands, the `interpret` alias, 206 command/action rows, 57 configuration rows, defaults, outputs, and test traceability were derived from source and CLI evidence. |
| D — Executable tutorials | Pass | Tutorials 1–3 executed successfully in the isolated environment; 12 recorded steps have exit code zero. Tutorials 4–5 have unmistakable bounded/historical status as permitted. |
| E — Scientific boundaries | Pass | Automated and editorial audits preserve UMAP, noise, DBCV, comparator, post-selection, historical/fresh, full-IDP, and cross-platform boundaries. |
| F — Output completeness | Pass | All 35 producer-map patterns appear in the machine-readable atlas, together with three documented in-memory non-artifacts and verified examples. |
| G — Pedagogy | Pass | Quickstart, progressive six-part structure, 46 learning-objective rows, teaching contract in every chapter, glossary, exercises/checks, and operational references are present. |
| H — Reproducibility/provenance | Pass | Environment, dependencies, inputs, configurations, seeds, threads, commands, logs, manifests, outputs, and checksums are captured; determinism wording is bounded. |
| I — Editorial/render quality | Pass | Links, figures, references, scientific-language scans, privacy scans, self-contained HTML, and the complete PDF passed QA. All 122 PDF pages were rendered and visually inspected in 11 numbered contact sheets. |
| J — Handoff readiness | Pass | This report states passed and pending work; the Docker/cloud handoff specifies packaging inputs, smoke/full-run contracts, security, platform comparisons, tolerances, and pass/fail criteria without creating infrastructure. |

## Remaining limitations and risks

1. The fresh 164-IDP 1,000-seed run is pending until after a controlled Docker smoke-test and resource profile.
2. No Docker image, Linux test, SBOM/security scan, GCP run, AWS run, or cross-hardware comparison has been performed.
3. Statistical, biological, causal, clinical, and external-replication validity is not established by the local software evidence.
4. Git history/commit identity was absent; packaging must establish a versioned source identity and reconcile it with `evidence/04_source_checksums.tsv`.
5. Exact Yang/Zhao reviewer references remain unresolved pending fuller bibliographic information.
6. The authoritative raw matrices for the broader 2,315- and 459-vector analyses are incomplete or ambiguous in the supplied evidence and must not be silently selected.
7. Raw internal tutorial evidence retains local absolute paths for private provenance. A public package must exclude or deliberately sanitize that evidence layer while retaining protected originals and checksums.
8. The PDF renderer emitted benign Type-3-glyph bounding-box warnings for mathematical glyphs; every page rendered visibly and legibly during full-page inspection.

## Exact next action

Establish a versioned source identity for the checksum-verified Freeze 3 tree, then author a minimal non-root Docker image without embedded data or credentials. Run the fixed synthetic `inspect-config`, `show-search-space`, `run`, `validate`, `reproduce-model`, `compare`, and `explain` smoke matrix locally and on controlled Linux using the same image digest and mounted checksums. Capture the SBOM, vulnerability scan, environment, resource/thread settings, manifests, schemas, labels, metrics, plots, logs, and exact-versus-tolerance comparisons. Profile a bounded scientific pilot before authorising the fresh 164-IDP 1,000-seed run, then repeat the declared comparison matrix on the approved GCP and AWS targets.

## Change summary

- Added a complete 46-chapter, eight-appendix analyst textbook and novice quickstart.
- Added verified Markdown, self-contained HTML, and fully inspected PDF editions.
- Added software-derived command/configuration/output/test maps and a complete output atlas.
- Added fresh Tutorials 1–3, bounded Tutorials 4–5, retained logs/manifests/checksums, and an explicit historical-versus-fresh IDP boundary.
- Added primary-source bibliography, claim/citation remediation, reviewer crosswalk, comparator matrix, glossary, quantitative figures, editable diagrams, curriculum maps, and traceability registers.
- Added automated editorial, technical, scientific-language, citation, figure, render, link, and privacy QA.
- Added the Docker/Linux/GCP/AWS packaging and validation handoff without starting the deferred infrastructure stage.
