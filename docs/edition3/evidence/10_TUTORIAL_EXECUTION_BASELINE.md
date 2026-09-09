# Tutorial execution baseline

## Outcome

The smallest authoritative tutorial path is executable end to end in the audited local environment. It is safe to use as the Edition 3 teaching baseline after the Stage 1 gate. It is a synthetic software exercise, not a reproduction of a manuscript analysis.

## Environment

- Date: 2026-08-26, Asia/Singapore; recorded run timestamps are UTC.
- Platform: macOS 26.5.1, arm64.
- Python: 3.12.13.
- DIMPLE-GWAS: 3.0.0rc1.
- Core packages: NumPy 2.4.6, pandas 3.0.3, SciPy 1.18.0, scikit-learn 1.9.0, umap-learn 0.5.12, hdbscan 0.8.44, PyYAML 6.0.3, joblib 1.5.3, Matplotlib 3.11.1, PyArrow 25.0.0.
- Environment provenance: Freeze 3 contains no `.venv`; the retained Freeze 2 `.venv` was used while the working directory and imported package source were Freeze 3. No packages were installed or upgraded.
- Optional packages absent: `openpyxl`, `xlrd`; therefore one XLSX-specific test skipped.

## Sources and immutable identities

| Item | Identity |
|---|---|
| Tutorial config | `docs/textbook/edition2/labs/01_fixed_synthetic/tutorial_config.yaml`, SHA-256 `16406ec39de81f87493c6bc6cbe28252a607ab85c429195af4b9924154d6e8ff` |
| Synthetic matrix | `benchmarks/synthetic/synthetic_matrix.tsv`, SHA-256 `77d1956fd074da9d82ce0d6a9c896446895a5e22b2fc6da85417169d13b9bb01` |
| Annotations | `benchmarks/synthetic/synthetic_annotations.csv`, SHA-256 `39a8abf9426723ee812e0ff9463add0e04a25768245cf5ca630fd907a70974bd` |
| Package source | SHA-256 `df87825992ab51dc016c673cf420a978ba5c161bd6c755e00a5199ead310e65b` |
| Resolved run config | SHA-256 `67b5f18293839440de6c04fc8cc171bf2f349d83900fa0092c50ba79e7e14ef9` |
| Selected model | `model_060fac0208bb58e2` |
| Labels | SHA-256 `5b7ba37a542efcceebd5d39a69342279e44565f017c2c099e36060c3eb0496ee` |

## Configuration

The fixture contains 24 analysis vectors and 80 numeric input variables after four metadata columns are removed. It performs one three-dimensional densMAP embedding using `n_neighbors=10`, `min_dist=0`, Euclidean distance, and seed 42. HDBSCAN uses minimum cluster size 5, minimum samples 2, epsilon 0, EOM selection, Euclidean distance, and no maximum cluster size. It evaluates one candidate, uses one worker, requests one top model, includes DBCV, excludes noise from the legacy score, writes Parquet, and enables strict mode.

## Executed path

The command record is `qa/stage1/commands/run_local_verification.sh`; each invocation has a command/status record plus separate stdout and stderr logs.

1. Recorded environment versions and package integrity.
2. Ran version, root help, and help for `run`, `inspect-config`, `show-search-space`, `score-existing`, `summarize-models`, `reproduce-model`, `explain`, the `interpret` alias, `compare`, and `validate`.
3. Resolved all seven shipped YAML configurations.
4. Enumerated standard (2,430), extended (1,728), and fixed (1) search spaces without fitting the large grids.
5. Ran the full test suite.
6. Ran the fixed synthetic candidate.
7. Explained the selected native artifact without refitting.
8. Reproduced the selected model from its retained summary.
9. Compared the original and reproduced partitions with an exact-ID-order requirement.
10. Validated the original run and generated model summaries.
11. Reapplied the legacy score to the retained 333-row historical 164 model table.

## Results

| Check | Result |
|---|---|
| Logged commands | 31/31 exit status 0 |
| Test suite | 44 passed; 1 skipped; 5 warnings; 10.70 seconds |
| Optional skipped coverage | XLSX loading, because `openpyxl` is absent |
| Fixed search | 1 successful; 0 invalid; 0 failed |
| Prepared matrix | 24 vectors × 80 input variables |
| Selected clustering | 3 clusters; 0 noise |
| Silhouette | 0.9423990249633789, Euclidean, non-noise, all 24 |
| DBCV | 0.945233343654039, Euclidean |
| Trustworthiness | 0.8676470588235294, k=10 |
| Continuity | 0.8779411764705882, k=10 |
| Calinski–Harabasz | 3642.2452975977503, Euclidean |
| Davies–Bouldin | 0.07207102433886971, Euclidean |
| Reproduction | Same model ID and byte-identical label file |
| Comparison | ARI/NMI/noise Jaccard/mapped fraction = 1; VI = 0; Procrustes `2.7088204667806472e-31` |
| Validation | 24 checks passed; 0 failed; 0 warnings |
| Historical 164 re-score | 333 rows joined; maximum absolute `score` difference = 0 |

## Warnings and interpretation

- UMAP notes that supplying a random state constrains its parallelism; this is expected and supports the fixed-seed fixture.
- Joblib could not query the physical-core count in the sandbox and fell back to logical cores. The fixture uses one worker, so this did not alter its declared work allocation.
- Pip disabled an unwritable user cache; package integrity still passed.
- A NumPy undefined-correlation warning occurs in the unit test that deliberately verifies the default failure behavior.
- These warnings are preserved in logs and do not invalidate the bounded results.

## Tutorial acceptance criteria

A future Edition 3 exercise may reuse this baseline only if it:

- begins with an explicit prediction about expected files and counts;
- uses a new empty output directory;
- inspects `resolved_config.yaml`, `search_space_manifest`, `model_selection_manifest`, top-model summary, and run manifest;
- distinguishes metric scope from biological interpretation;
- runs `validate` and `compare` rather than relying on screenshots;
- states that the one-candidate legacy score is 1 because of the zero-range fallback, not because the model achieved perfect external validity; and
- never presents the synthetic three-cluster result as evidence for the manuscript.

## Privacy and path safety

The generated runtime manifests contain absolute local paths. They remain inside the local QA tree and must be sanitized before publication. The evidence documents use workspace-relative paths. No secrets, tokens, email addresses, or restricted participant data were copied into the Edition 3 evidence files.
