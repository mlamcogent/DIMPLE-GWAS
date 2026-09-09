# Software truth report

## Authority and method

For commands, defaults, accepted values, schemas, algorithms, and artifact production, executable Freeze 3 source is authoritative. Existing documentation and manuscript material provide context but do not override implementation. The generated TSVs are implementation-derived as of this source checksum freeze.

## Confirmed behavior

- The public entry point exposes `run`, `inspect-config`, `show-search-space`, `score-existing`, `summarize-models`, `reproduce-model`, `explain`/`interpret`, `compare`, and `validate`.
- Configuration precedence is built-in mode, then YAML overlay, then explicit CLI override.
- The standard input is variants by vectors with a four-column metadata prefix by default. Prepared analysis data are transposed to vectors by variants.
- Repeated seeded UMAP/densMAP embeddings are concatenated. No PCA/SVD/ICA pre-reducer exists in the production path.
- Clustering uses contributed `hdbscan`; all candidate rows, including failures and invalid topology, are retained.
- Standard enumeration is `45 x 18 x 3 = 2,430` candidates. The shipped extended mode enumerates 1,728.
- `legacy_dimple` ranks with normalized silhouette plus normalized cluster count, and optionally subtracts normalized noise count. DBCV is an optional computed diagnostic, not a legacy-score component.
- Interpretation never refits. It verifies identifiers, summarizes original-space similarity, and labels its coordinate associations descriptive.
- Comparison requires exact identifier sets and does not equate numeric cluster labels across runs.
- Validation checks artifacts, schemas, counts, readability, and hashes; it is software validation, not biological validation.

## Boundaries

- This snapshot has no usable Git commit; SHA-256 source and artifact records are the release identity.
- The fresh test result is macOS/Apple Silicon only. Docker/Linux/cloud validation remains a release gate.
- The 164-IDP 1,000-seed search is deliberately deferred. Historical adaptation and exact rescoring are documented separately.
- Optional Parquet writing is best-effort and the outcome is recorded in the run manifest.
- Successful local deterministic comparison is bounded to the executed fixture and environment; no bitwise cross-platform claim is made.
