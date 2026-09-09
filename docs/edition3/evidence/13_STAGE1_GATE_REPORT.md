# Stage 1 gate report

## Decision

**PASS_WITH_LIMITATIONS**

The evidence-closure stage is complete enough to begin Edition 3 authoring, provided every carried limitation remains visible and the textbook does not represent retained/adapted results as fresh scientific reproductions.

## Twelve-gate assessment

| Gate | Requirement | Result | Evidence | Limitation carried forward |
|---|---|---|---|---|
| G1 | Source inventory and immutable identities | Met | 91 local sources are checksum-inventoried; web literature has DOI or authoritative URL identity. | No Git commit exists. |
| G2 | Authority, lineage, and release boundary | Met | `01_AUTHORITY_LINEAGE_AND_RELEASE_BOUNDARY.md` resolves precedence and rejected/accepted lineage. | Software-complete is bounded to local and retained evidence. |
| G3 | Implementation truth | Met | `02_IMPLEMENTATION_TRUTH_REGISTER.tsv` records command/function contracts, defaults, randomness, side effects, I/O, errors, and tests. | Public behavior outside inspected source is not inferred. |
| G4 | Prior-claim audit and claim ledger | Met | `04_PRIOR_REPORT_CLAIM_AUDIT.tsv` and `05_CLAIM_EVIDENCE_REGISTER.tsv` distinguish verified, reported, obsolete, contradicted, and unresolved claims. | Scientific claims with missing inputs remain reported only. |
| G5 | Methods and educational literature | Met | `03_VERIFIED_METHODS_AND_EDUCATIONAL_EVIDENCE_DOSSIER.md` covers 14 required domains; `06_VERIFIED_BIBLIOGRAPHY.bib` records verified metadata. | Citations contextualize; they do not validate DIMPLE results. |
| G6 | Reviewer-literature mapping | Met | `07_REVIEWER_LITERATURE_CROSSWALK.md` maps requests to evidence and corrects the comparator to Oblong et al. 2024. | Several reviewer analyses remain unperformed. |
| G7 | Analysis hierarchy and golden runs | Met | `08_ANALYSIS_HIERARCHY_AND_GOLDEN_RUNS.md` separates 2,315, 459, 164, 356, adapters, regression fixtures, and tutorials. | 2,315/459 raw matrices absent; 459 parameters conflict; fresh 164 full run pending. |
| G8 | Function-concept-output coverage | Met | `09_FUNCTION_CONCEPT_OUTPUT_COVERAGE.tsv` maps 25 capabilities to concepts, artifacts, tests, and gaps. | Optional XLSX and cross-platform paths are not freshly covered. |
| G9 | Safe language and misconceptions | Met | `11_SAFE_LANGUAGE_AND_MISCONCEPTION_REGISTER.tsv` supplies 24 mandatory wording corrections. | Biological interpretation still requires independent evidence. |
| G10 | CLI, configuration, and unit/integration validation | Met with limitation | All 31 logged commands exited zero; every help surface and all seven configs resolved; 44 tests passed. | One XLSX test skipped because `openpyxl` is absent; 5 warnings preserved. |
| G11 | Bounded end-to-end tutorial execution | Met | One fixed run, explain, reproduce, compare, validate, summarize, and historical rescore completed; 24/24 validation checks and exact partition concordance. | Synthetic and table-rescore results are not manuscript-scale refits. |
| G12 | Manifest, checksum, privacy, and unresolved-gap closure | Met with limitation | Manifest and generated checksums cover delivered artifacts; path/privacy review completed; 18 gaps explicitly recorded. | Generated private QA manifests contain absolute local paths and need sanitized publication copies. |

## Fresh evidence summary

- DIMPLE-GWAS `3.0.0rc1`; package-source SHA-256 `df87825992ab51dc016c673cf420a978ba5c161bd6c755e00a5199ead310e65b`.
- macOS arm64, Python 3.12.13, recorded dependency versions.
- Test result: 44 passed, 1 skipped, 5 warnings in 10.70 seconds.
- Search-space dry enumeration: standard 2,430; extended 1,728; fixed 1.
- Fixed run: one successful candidate; model `model_060fac0208bb58e2`; label SHA-256 `5b7ba37a542efcceebd5d39a69342279e44565f017c2c099e36060c3eb0496ee`.
- Fixed reproduction: same model ID and byte-identical label file.
- Fixed comparison: ARI, NMI, noise-set Jaccard, and mapped membership fraction all 1.0; variation of information 0; Procrustes disparity approximately `2.71e-31`.
- Fixed validation: 24 passed, 0 failed, 0 warnings.
- Historical 164 table: 333/333 rows joined; fresh versus retained `score` maximum absolute difference 0.

## Conditions on Edition 3 authoring

1. Cite the claim IDs and analysis levels in this evidence pack during drafting.
2. Preserve the release-boundary sentence verbatim or with equally restrictive meaning.
3. Teach the fixed synthetic baseline as software evidence only.
4. Keep the historical 164 adapter distinct from a fresh 1,000-seed refit.
5. Do not issue a 459 reproduction configuration until its source conflict is resolved.
6. Mark post-selection biological analyses descriptive unless independent or selection-aware evidence exists.
7. Sanitize absolute paths from any QA artifact copied into a publishable build.
8. Re-run the complete QA suite in the final authoring environment, including the optional XLSX test if the dependency is added.

## Work explicitly not performed

Stage 1 did not write textbook chapters, run the consequential 164-IDP 1,000-seed job, reconstruct absent 2,315/459 matrices, modify Docker/cloud configuration, install global dependencies, or perform new reviewer-requested scientific analyses.
