# Technical reference: configuration

## Precedence and identity

Configuration resolves in this order: built-in search mode, YAML overlay, explicit command-line overrides. Nested mappings merge recursively; a supplied leaf replaces the prior value. The validated resolved configuration—not the template YAML—is the analysis specification and receives a stable digest in the run evidence.

Scalar values, lists, comma-separated sequences, exclusive-stop range strings such as `2:20:2`, and YAML range mappings `{start: 2, stop: 20, step: 2}` are normalized according to the field type. Fixed mode requires one value for every searched UMAP and HDBSCAN parameter.

## Input block

| Field | Standard default | Meaning |
|---|---|---|
| `path` | null | CSV/TSV/gzip matrix path; required for fitting |
| `drop_first_n_cols` | 4 | leading metadata columns removed before numeric analysis |
| `sep` | inferred/null | explicit delimiter override |
| `zscore_transform` | `none` | `none` or column-wise `rint` |
| `annotation_file` | null | optional annotation table |
| `annotation_index_col` | `index` | annotation join key |

## UMAP/densMAP block

| Field | Standard default | Constraint / interpretation |
|---|---:|---|
| `n_neighbors` | 30 | integer at least 2; local graph scale |
| `min_dist` | 0.0 | non-negative and not greater than spread |
| `n_components` | 3 | positive output dimension |
| `metric` | `euclidean` | one of the supported UMAP metrics |
| `spread` | 1.0 | positive packing scale |
| `learning_rate` | 1.0 | positive optimization rate |
| `repulsion_strength` | 1.0 | non-negative repulsive weighting |
| `negative_sample_rate` | 5 | positive integer |
| `local_connectivity` | 1.0 | non-negative local connectivity |
| `set_op_mix_ratio` | 1.0 | value in [0,1] |
| `random_state` | 42 | seed origin in modern mode |
| `densmap` | true | density-regularized UMAP toggle |

Supported metric names include Euclidean/L2, Manhattan/L1/cityblock, Chebyshev, Minkowski, Canberra, Bray-Curtis, cosine, correlation, Hamming, Jaccard, Dice, Russell-Rao, Sokal-Michener, Sokal-Sneath and Yule. Data/backend compatibility remains a runtime question.

## HDBSCAN block

| Field | Standard default | Constraint / interpretation |
|---|---|---|
| `min_cluster_size` | range 5:50:1 | integer at least 2 |
| `min_samples` | range 2:20:1 | integer at least 1 |
| `cluster_selection_epsilon` | range 0:3:1 | non-negative |
| `cluster_selection_persistence` | 0.0 | non-negative |
| `cluster_selection_method` | `eom` | `eom` or `leaf` |
| `alpha` | 1.0 | positive |
| `allow_single_cluster` | false | backend selection permission; topology eligibility still matters |
| `max_cluster_size` | 0 | 0 for unbounded; any nonzero value must not be below minimum size |
| `metric` | `euclidean` | supported clustering metric |

Under leaf selection, maximum cluster size has no effective pruning role in the current mapping and is annotated. Some nonstandard metrics force the contributed backend's generic algorithm.

## Execution block

| Field | Standard default | Meaning |
|---|---:|---|
| `n_random_states` | 1000 | number of seeded embedding blocks |
| `n_jobs` | -1 | jobs passed to supported operations |
| `candidate_jobs` | 1 | candidate-level parallelism |
| `top_n_models` | 20 | retained top artifacts |
| `warn_candidate_count` | 5000 | preflight warning threshold |
| `max_candidate_models` | 0 | 0 disables hard cap; positive rejects larger grids |
| `max_samples_trust` | 3000 | bounded sample size for neighborhood metrics |
| `max_samples_silhouette` | 0 | 0 means no configured silhouette sampling cap |
| `trust_k` | 30 | requested neighborhood size, bounded by data |
| `trust_seed` | 42 | deterministic diagnostic sampling seed |
| `silhouette_seed` | 42 | deterministic silhouette sampling seed |
| `legacy_ensemble_seeds` | true | seeds 1 through `n_random_states` |
| `write_parquet` | true | attempt optional Parquet output |
| `compute_dbcv` | true | compute optional density diagnostic |
| `strict` | false | error escalation policy |

Standard defaults can be computationally consequential; “default” is not “safe quickstart.” The fixed tutorial overrides the seed count and search to one.

## Scoring block

`profile` is `legacy_dimple` or `custom`; the default is legacy. `fit_include_noise` is false by default. A custom mapping names model-table metrics with positive weights and `maximize`/`minimize` direction. Missing active metrics, invalid directions or unusable weights fail validation or scoring.

## Interpretation block

Defaults are Pearson similarity, `cluster_then_hclust` order, noise `separate_last`, undefined-correlation `error`, complete ID matching, full-heatmap bound 1,200, similarity writing enabled, forced large matrices disabled, coordinate associations disabled, Pearson coordinate method and 100 top associations.

## Validation rules

The configuration rejects unknown top-level keys, empty or malformed ranges, zero steps, non-finite values, unsupported metrics, invalid parameter bounds, non-scalar fixed-mode search fields, invalid execution limits and undeclared custom-score directions. Data-dependent backend failures remain retained candidate failures in non-strict searches.

\newpage
