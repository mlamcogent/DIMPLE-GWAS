# Original-space interpretation

## Scope

Freeze 3 explanation is post-run. It consumes retained labels and visualization coordinates and never fits UMAP/HDBSCAN, changes membership, or changes ranking.

## Similarity

For analysis vectors `x_i` across original input dimensions, the default table contains pairwise Pearson correlations `corr(x_i, x_j)`. Spearman is explicit. Constant vectors produce undefined correlations and fail by default. `undefined_correlation: zero` explicitly replaces affected off-diagonal values with zero, restores the diagonal to one, and records the affected cell count and warning.

This is original-input-space similarity after declared preprocessing—not correlation between UMAP coordinates.

## Ordering and noise

Default `cluster_then_hclust` sorts label blocks numerically/textually, places noise last, and applies average-linkage hierarchy within each block using `1-correlation` distance. Other explicit orders are `cluster`, `hclust`, and `input`. Noise policies are:

- `separate_last` (default): retain as a final block;
- `include`: retain in the selected ordering method; and
- `exclude`: remove and record every excluded noise ID.

`heatmap_order.tsv` and `cluster_cutpoints.tsv` make matrix/figure alignment auditable.

## Cluster summaries

For each cluster/noise block, Freeze 3 reports size, singleton status, pair counts, mean/median within-block similarity, and mean between-block similarity. Singleton within-similarity is undefined rather than invented.

## Projection diagnostics

Bounded trustworthiness and continuity compare the original-space matrix with supplied visualization coordinates. They evaluate only that visualization projection, not HDBSCAN validity or biological correctness.

## Rendering

The PNG uses a blue–white–red correlation scale and a label track. The HTML embeds the PNG as base64 and has no network dependency. If vectors exceed `max_full_heatmap`, only rendering is block-preserving sampled; complete order, summaries, cutpoints, and similarity remain machine-readable. At least one representative per consecutive block is retained.

## Coordinate associations

Opt-in coordinate associations correlate each original dimension with each supplied UMAP coordinate. They are descriptive and may be unstable under rotation, reflection, stochastic variation, or hyperparameter change. They are not feature loadings, drivers, mechanisms, causal effects, or post-selection inferential tests.

Cluster ANOVA, permutation p-values, surrogate classifiers, parametric UMAP, and causal attribution are not part of Freeze 3.
