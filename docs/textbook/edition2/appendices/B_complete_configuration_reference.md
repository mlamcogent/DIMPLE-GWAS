# Appendix B — Complete configuration reference

Precedence is built-in mode, then recursively merged YAML, then explicit CLI values. The resolved configuration—not the overlay alone—is the executed method. Numeric ranges are half-open in the implemented expansion (`start` included, `stop` excluded).

| Key | Standard | Extended | Fixed | Custom | Meaning | CLI |
| --- | --- | --- | --- | --- | --- | :---: |
| `execution.candidate_jobs` | `1` | `1` | `1` | `1` | Parallel HDBSCAN candidates; core-distance jobs become one when parallelized. | yes |
| `execution.compute_dbcv` | `true` | `true` | `true` | `true` | Compute DBCV diagnostic when possible. | yes |
| `execution.legacy_ensemble_seeds` | `true` | `false` | `false` | `false` | Use historical repeated-seed sequence. | yes |
| `execution.max_candidate_models` | `0` | `0` | `0` | `0` | Hard safety ceiling; zero means unlimited. | yes |
| `execution.max_samples_silhouette` | `0` | `0` | `0` | `0` | Maximum samples used for silhouette; zero means all. | yes |
| `execution.max_samples_trust` | `3000` | `3000` | `3000` | `3000` | Maximum samples used for embedding trust/continuity; zero means all. | yes |
| `execution.n_jobs` | `-1` | `-1` | `-1` | `-1` | Parallel jobs for repeated UMAP and HDBSCAN core distances. | yes |
| `execution.n_random_states` | `1000` | `10` | `1` | `1000` | Number of repeated seeded embeddings per UMAP family. | yes |
| `execution.silhouette_seed` | `42` | `42` | `42` | `42` | Subsampling seed for silhouette. | yes |
| `execution.strict` | `false` | `false` | `false` | `false` | Abort when a UMAP family or candidate fails. | yes |
| `execution.top_n_models` | `20` | `20` | `20` | `20` | Number of eligible ranked models retained. | yes |
| `execution.trust_k` | `30` | `30` | `30` | `30` | Requested neighborhood size for trustworthiness/continuity. | yes |
| `execution.trust_seed` | `42` | `42` | `42` | `42` | Subsampling seed for embedding-quality metrics. | yes |
| `execution.warn_candidate_count` | `5000` | `5000` | `5000` | `5000` | Candidate-count warning threshold. | yes |
| `execution.write_parquet` | `true` | `true` | `true` | `true` | Attempt supplementary Parquet model table. | yes |
| `hdbscan.allow_single_cluster` | `false` | `false` | `false` | `false` | Permit a one-cluster result. | yes |
| `hdbscan.alpha` | `1.0` | `1.0` | `1.0` | `1.0` | Robust single-linkage scaling parameter. | yes |
| `hdbscan.cluster_selection_epsilon` | `{"start": 0, "step": 1, "stop": 3}` | `[0.0, 0.05]` | `0.0` | `{"start": 0, "step": 1, "stop": 3}` | Distance threshold used when extracting clusters. | yes |
| `hdbscan.cluster_selection_method` | `"eom"` | `["eom", "leaf"]` | `"eom"` | `"eom"` | EOM or leaf extraction. | yes |
| `hdbscan.cluster_selection_persistence` | `0.0` | `0.0` | `0.0` | `0.0` | Minimum persistence threshold. | yes |
| `hdbscan.max_cluster_size` | `0` | `[0, 100]` | `0` | `0` | EOM-only maximum size; zero means unlimited. | yes |
| `hdbscan.metric` | `"euclidean"` | `["euclidean", "cosine"]` | `"euclidean"` | `"euclidean"` | Distance metric supplied to contrib hdbscan and silhouette. | yes |
| `hdbscan.min_cluster_size` | `{"start": 5, "step": 1, "stop": 50}` | `[5, 10, 20]` | `5` | `{"start": 5, "step": 1, "stop": 50}` | Smallest permitted cluster size. | yes |
| `hdbscan.min_samples` | `{"start": 2, "step": 1, "stop": 20}` | `[2, 5, 10]` | `5` | `{"start": 2, "step": 1, "stop": 20}` | Density conservativeness/core-distance neighborhood. | yes |
| `input.annotation_file` | `null` | `null` | `null` | `null` | Optional vector annotation table. | yes |
| `input.annotation_index_col` | `"index"` | `"index"` | `"index"` | `"index"` | Annotation join column matched to retained feature_id. | yes |
| `input.drop_first_n_cols` | `4` | `4` | `4` | `4` | Leading metadata columns excluded before transpose. | yes |
| `input.path` | `null` | `null` | `null` | `null` | Variants-by-vectors CSV/TSV input path. | yes |
| `input.sep` | `null` | `null` | `null` | `null` | Optional explicit input separator; otherwise inferred. | yes |
| `input.zscore_transform` | `"none"` | `"none"` | `"none"` | `"none"` | Optional column-wise rank inverse normal transformation before transpose. | yes |
| `interpretation.coordinate_associations` | `false` | `false` | `false` | `false` | Opt in to descriptive coordinate associations. | yes |
| `interpretation.coordinate_methods` | `["pearson"]` | `["pearson"]` | `["pearson"]` | `["pearson"]` | Pearson and/or Spearman coordinate association methods. | yes |
| `interpretation.force_large_matrix` | `false` | `false` | `false` | `false` | Override large-matrix protection. | yes |
| `interpretation.max_full_heatmap` | `1200` | `1200` | `1200` | `1200` | Full heatmap size threshold. | yes |
| `interpretation.noise_policy` | `"separate_last"` | `"separate_last"` | `"separate_last"` | `"separate_last"` | Place noise last, include it in ordering, or exclude it. | yes |
| `interpretation.order` | `"cluster_then_hclust"` | `"cluster_then_hclust"` | `"cluster_then_hclust"` | `"cluster_then_hclust"` | Heatmap ordering: cluster_then_hclust, cluster, hclust, or input. | yes |
| `interpretation.require_complete_match` | `true` | `true` | `true` | `true` | Require exact source/label identifier sets. | yes |
| `interpretation.similarity_metric` | `"pearson"` | `"pearson"` | `"pearson"` | `"pearson"` | Pearson or Spearman similarity in the original variable space. | yes |
| `interpretation.top_n_associations` | `100` | `100` | `100` | `100` | Maximum retained coordinate associations. | yes |
| `interpretation.undefined_correlation` | `"error"` | `"error"` | `"error"` | `"error"` | Fail or replace undefined correlation with zero. | yes |
| `interpretation.write_similarity` | `true` | `true` | `true` | `true` | Write the complete original-space similarity table. | yes |
| `scoring.custom` | `{}` | `{}` | `{}` | `{}` | Metric rules with weight and maximize/minimize direction. | YAML only |
| `scoring.fit_include_noise` | `false` | `false` | `false` | `false` | Include noise count in legacy dynamic-range fitting. | yes |
| `scoring.profile` | `"legacy_dimple"` | `"legacy_dimple"` | `"legacy_dimple"` | `"legacy_dimple"` | legacy_dimple or explicit custom weighted score. | yes |
| `search_mode` | `"standard"` | `"extended"` | `"fixed"` | `"custom"` | Built-in enumeration family: standard, extended, custom, or fixed. | yes |
| `umap.densmap` | `true` | `true` | `true` | `true` | Enable density-augmented UMAP objective. | yes |
| `umap.learning_rate` | `1.0` | `1.0` | `1.0` | `1.0` | UMAP optimizer initial learning rate. | yes |
| `umap.local_connectivity` | `1.0` | `1.0` | `1.0` | `1.0` | Expected locally connected nearest neighbors. | yes |
| `umap.metric` | `"euclidean"` | `["euclidean", "cosine"]` | `"euclidean"` | `"euclidean"` | Metric used by UMAP to construct the neighbor graph. | yes |
| `umap.min_dist` | `0.0` | `[0.0, 0.1]` | `0.0` | `0.0` | UMAP minimum embedding distance; searchable. | yes |
| `umap.n_components` | `3` | `3` | `3` | `3` | Dimensions per repeated embedding; concatenated across repeats. | yes |
| `umap.n_neighbors` | `30` | `[15, 30, 50]` | `30` | `30` | UMAP neighborhood size; searchable scalar/list/range. | yes |
| `umap.negative_sample_rate` | `5` | `5` | `5` | `5` | Negative samples per positive optimization sample. | yes |
| `umap.random_state` | `42` | `42` | `42` | `42` | Base seed used to derive repeated embedding seeds. | yes |
| `umap.repulsion_strength` | `1.0` | `1.0` | `1.0` | `1.0` | UMAP negative-sample repulsion weight. | yes |
| `umap.set_op_mix_ratio` | `1.0` | `1.0` | `1.0` | `1.0` | Fuzzy-set union/intersection interpolation. | yes |
| `umap.spread` | `1.0` | `1.0` | `1.0` | `1.0` | Scale parameter paired with min_dist. | yes |

Configuration validation checks modes, types, ranges, metrics, search ceilings, interpretation options, and incompatible settings. `inspect-config` is the authoritative preflight; `show-search-space` establishes candidate identity before fitting.
