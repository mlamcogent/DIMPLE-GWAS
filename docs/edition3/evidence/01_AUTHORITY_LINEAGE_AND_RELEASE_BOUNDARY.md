# Authority, lineage, and release boundary

## Stage 1 decision context

This record freezes the evidence hierarchy for the Edition 3 documentation stage. It is not a scientific result and does not begin the Edition 3 textbook.

## Authoritative implementation

`DIMPLE-GWAS-freeze3/` is the authoritative source for documented behavior. Its package reports version `3.0.0rc1`. The live directory is not a Git checkout: `git rev-parse HEAD` returns “not a git repository,” so no commit identifier exists. Source identity is therefore expressed through:

- package-source SHA-256 `df87825992ab51dc016c673cf420a978ba5c161bd6c755e00a5199ead310e65b` from the fresh fixed-run manifest;
- per-file SHA-256 values in `00_SOURCE_INVENTORY_AND_CHECKSUMS.tsv`;
- fresh resolved-configuration SHA-256 `67b5f18293839440de6c04fc8cc171bf2f349d83900fa0092c50ba79e7e14ef9` for the bounded tutorial run; and
- stable selected model ID `model_060fac0208bb58e2`.

The absence of Git is a traceability limitation, not a reason to substitute timestamps or an invented commit.

## Source precedence

| Priority | Source | Permitted use | Not permitted |
|---|---|---|---|
| 1 | Freeze 3 source, tests, configurations, fresh local outputs | Implementation truth and current CLI/output contracts | Biological validation by itself |
| 2 | `freeze3_workspace/` reports and retained artifacts | Principal audit evidence, historical reconstruction, bounded concordance | Reclassification as fresh full-data reruns |
| 3 | Freeze 2 | Audited software baseline and compatibility comparator | Override of Freeze 3 behavior |
| 4 | Development monolith | Legacy lineage; its main file is byte-identical to the Freeze 2 monolith | Current release authority |
| 5 | Cluster-optimization prototype | Audited source of the accepted original-space explanation design | Independent release authority |
| 6 | Modded variant | Reference-only record of considered parameter/backend changes | Adopted behavior; its soft biological target score is rejected |
| 7 | Manuscript, supplement, reviewer documents, prior generated prose | Scientific/reporting context and claims to test | Override of code, tests, config, or retained output |
| 8 | Primary literature | External method context and limitations | Proof that this implementation or these clusters are correct |

## Lineage decisions

- The Development and Freeze 2 monoliths share SHA-256 `c07bb1796066b1e97295945badc78568651255c0721f3f0b337221ad8a671123`.
- Freeze 3 modularizes and extends the audited Freeze 2 pipeline. It retains direct full-matrix UMAP, contributed `hdbscan`, the historical score option, complete deterministic candidate enumeration, and explicit provenance.
- Freeze 3 adds current interpretation, visualization, comparison, validation, schema adapters, and stronger manifest/hash handling.
- From the cluster-optimization prototype, Freeze 3 accepts original-space similarity, exact ID matching, block-preserving ordering and cutpoints, visual sampling, and optional descriptive coordinate association. It does not accept duplicate pipeline/scoring/input/provenance implementations.
- From the Modded branch, Freeze 3 accepts the idea that metric, selection method, and maximum cluster size should be configurable. It does not adopt the `sklearn.cluster.HDBSCAN` backend because that would break historical backend continuity. It rejects the soft target score favoring 10–20 clusters, about 300 noise points, and a largest cluster near 300 as biologically pre-committed selection.
- No PCA, ICA, SVD, or other linear reducer appears in the current pre-UMAP data path. PCA and ICA remain comparators, not hidden preprocessing.

## Release boundary

The defensible statement is:

> DIMPLE-GWAS Freeze 3 RC1 is software-complete within the retained source, test suite, fixed synthetic fixture, and local evidence reviewed in Stage 1.

This statement does **not** mean:

- a scientific freeze of the 2,315-, 459-, or 164-IDP analyses;
- a fresh 1,000-seed reproduction of the historical 164-IDP result;
- independent biological validation of cluster meanings;
- Docker, Linux, GCP, AWS, x86-64, or cross-library bitwise reproducibility;
- completeness of restricted or absent raw matrices; or
- completion of reviewer-requested new experiments.

## Fresh Stage 1 observation

The bounded run used the retained Freeze 2 environment only because Freeze 3 has no local virtual environment. It executed on macOS arm64 with Python 3.12.13. All 31 logged commands exited zero; 44 tests passed, one optional XLSX test was skipped because `openpyxl` is absent; one fixed synthetic model ran; its reproduction produced byte-identical label files and permutation-invariant agreement metrics of 1.0; validation passed 24/24 checks; and the 333-row historical 164 table rescored identically to the retained Freeze 3 table. These facts establish local execution readiness, not scientific generalization.

## Documentation rule

Edition 3 may describe behavior as implemented, tested, retained, reconstructed, reported, or unresolved. It must not silently collapse those categories. Any apparent conflict is resolved in favor of code/tests/config/output for software behavior and in favor of primary analysis artifacts for numerical scientific claims.
