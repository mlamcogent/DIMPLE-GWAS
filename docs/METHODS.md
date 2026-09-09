# Methods

## Analysis unit and preprocessing

DIMPLE-GWAS accepts a rectangular GWAS summary-statistics matrix. Rows represent variants and analyzed columns represent features or traits. The configured metadata prefix is removed, remaining cells are coerced to numeric, missing/non-numeric cells are rejected, and the matrix is transposed so each feature is represented by its genome-wide summary-statistic profile.

The default preprocessing profile leaves values unchanged. Optional `rint` assigns average ranks within each feature vector and maps `(rank - 0.5) / n` through the standard-normal quantile function. Generic feature annotations are joined only after clustering and never enter embedding or model selection.

## Repeated UMAP

For each unique UMAP parameter configuration, Freeze 3 performs the declared number of seeded fits and horizontally concatenates their components. HDBSCAN therefore operates on a repeated-embedding representation rather than one visualization draw. One component set is retained for top-model visualization coordinates.

The following UMAP controls may each be fixed or searched: `n_neighbors`, `min_dist`, `n_components`, `metric`, `spread`, `learning_rate`, `repulsion_strength`, `negative_sample_rate`, `local_connectivity`, `set_op_mix_ratio`, `random_state`, and the preserved `densmap` switch.

Standard mode uses the dev seed sequence `1..n_random_states`. Other modes begin at the declared UMAP `random_state`, making random state a genuine search dimension. All seeds are recorded.

## HDBSCAN topology search

Freeze 3 retains `scikit-learn-contrib/hdbscan`, the estimator used by the dev and Freeze 2 bases. Current versions expose all required controls, including `max_cluster_size`. This avoids the implementation-semantic change that would result from silently switching to `sklearn.cluster.HDBSCAN`.

Each combination of `min_cluster_size`, `min_samples`, `cluster_selection_epsilon`, `cluster_selection_persistence`, `cluster_selection_method`, `alpha`, `allow_single_cluster`, `max_cluster_size`, and `metric` is fit for every UMAP family. `max_cluster_size=0` means unlimited. The estimator documents that maximum cluster size affects EOM selection but not leaf selection; Freeze 3 records that condition as a parameter note rather than pretending it changes leaf results.

Cosine, correlation, and other non-tree metrics use the contrib estimator's generic algorithm. The metric name remains explicit in every candidate row.

## Candidate evaluation

Every candidate is retained with one of three statuses:

- `success`: fit completed with at least two non-noise clusters;
- `invalid_topology`: fit completed but produced fewer than two non-noise clusters;
- `failed`: fitting raised an exception, which is recorded without terminating the default search.

For each candidate Freeze 3 calculates cluster/noise counts and fractions, smallest/largest/median/mean cluster size, cluster-size coefficient of variation, HDBSCAN persistence summaries, silhouette, Calinski-Harabasz, and Davies-Bouldin. DBCV is attempted when enabled. Metric failures become explicit warnings and `NaN`; no metric is silently substituted.

Silhouette uses the configured HDBSCAN metric and the declared noise scope. Calinski-Harabasz and Davies-Bouldin retain their standard Euclidean geometry, which is recorded in companion columns. For very large datasets, silhouette can use a fixed-seed bounded sample; the sampling flag and realized sample size are recorded.

Trustworthiness and continuity use scikit-learn's optimized implementation. They are computed once per UMAP family under explicitly recorded Euclidean geometry with reproducible bounded subsampling. Freeze 3 does not construct custom dense rank matrices.

## Interpretation layer

Interpretation begins only after labels have been selected or supplied. It does not refit UMAP/HDBSCAN, change labels, or participate in ranking. Original-space Pearson and Spearman similarity are calculated within the declared feature-vector geometry, with explicit undefined-value handling. Average-linkage ordering is a display operation only. Heatmaps use a deterministic, block-preserving sample when the full matrix exceeds the configured display bound; the manifest records the selected IDs and sampling policy.

Optional trustworthiness/continuity summaries describe supplied visualization coordinates relative to original feature space. They are embedding diagnostics, not evidence that a clustering is biologically valid. Optional covariate associations are descriptive and are reported separately from topology selection.

## Ranking

Metric evaluation finishes before scoring begins. The default `legacy_dimple` profile is applied across eligible candidates, after which ranks use score descending, raw score descending, and stable model identifier ascending. Top-N model labels and reproduction configurations are refit from their cached embedding family.

See the official [UMAP parameter documentation](https://umap-learn.readthedocs.io/en/latest/parameters.html) and [contrib-HDBSCAN API](https://hdbscan.readthedocs.io/en/latest/api.html) for estimator-level definitions.
