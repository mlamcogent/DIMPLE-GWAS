# Technical reference: function atlas

The complete implementation-truth register is `evidence/02_IMPLEMENTATION_TRUTH_REGISTER.tsv`. It is the concise authoritative atlas for this reader draft: 45 records spanning CLI dispatch, configuration, I/O, preprocessing, UMAP/densMAP, HDBSCAN, search enumeration, metrics, scoring, ranking, pipeline orchestration, reporting, provenance, interpretation, visualization, comparison, validation and standard defaults.

## Workflow call path

`cli.main` dispatches a command. For `run`, configuration is resolved and validated, the input table is read and prepared, candidate families are enumerated, repeated embeddings are fitted and concatenated, HDBSCAN candidates are evaluated, scoring and ranking are applied, top/family/Pareto summaries are formed, artifacts are written, and provenance is finalized.

## Core analytical functions

| Module / function | Role | Important contract |
|---|---|---|
| `preprocessing.prepare_analysis_matrix` | build vectors-by-variables working matrix | metadata removal, numeric validation, optional column-wise RINT, transpose; no PCA/imputation |
| `umap_runner.fit_repeated_umap` | construct representation | one seeded UMAP/densMAP block per seed; horizontal concatenation; first view for display |
| `hdbscan_runner.fit_hdbscan` | fit density hierarchy | contributed `hdbscan`; label `-1` is noise; fit errors retained by pipeline |
| `search_space.enumerate_candidates` | declare candidate population | complete deterministic Cartesian product; stable IDs; hard limit can reject |
| `metrics.embedding_quality` | neighborhood diagnostics | trustworthiness/continuity with bounded $k$ and deterministic sampling |
| `metrics.evaluate_clustering` | candidate diagnostics | metric- and noise-scoped values; fewer than two non-noise clusters is invalid topology |
| `scoring.legacy_dimple_score` | compatibility score | maximum normalization, raw-range weights, optional noise penalty, final zero-range fallback to 1 |
| `scoring.custom_score` | declared multi-metric score | direction-aware min-max components and normalized weights |
| `ranking.rank_models` | deterministic order | score desc, raw score desc, model ID asc; sequential ranks for ties |
| `ranking.pareto_front` | supplementary trade-off set | objective-dependent nondominance; not a truth set |
| `pipeline.run_search` | end-to-end orchestration | complete run tree, failure retention, explicit randomness and parallelism |
| `interpretation.run_explanation` | post hoc original-space description | identity checks, no refit/rerank, exact IDs by default |
| `comparison.run_comparison` | structural run comparison | exact ID alignment, permutation-invariant metrics, conditional Procrustes |
| `validation.run_validation` | artifact integrity audit | required files, schemas, counts and hashes; not biological validation |

## Dossier fields

For exact signatures, inputs, outputs, defaults/precedence, randomness, side effects, files read and written, errors, source locations, test evidence and evidence status, use the implementation-truth register. Edition 2's complete 20-field dossiers are preserved unchanged as a deeper audit source. The final public Edition 3 reference should mechanically regenerate complete dossiers from the current source rather than duplicate hand-maintained values.

\newpage
