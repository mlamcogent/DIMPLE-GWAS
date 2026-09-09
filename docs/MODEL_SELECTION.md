# Model Selection and Ranked Landscape

Freeze 3 reports a landscape rather than one opaque winner.

## Eligibility and ordering

Candidates are scored only when fitting succeeds, at least two non-noise clusters exist, and every metric required by the profile is available. Unscored rows stay in the complete table. Deterministic rank order is:

1. score descending;
2. raw score descending;
3. stable model identifier ascending.

`top_n_models` controls retained label and reproduction artifacts; it does not remove lower-ranked rows.

## Model outputs

- `all_models.tsv`: all candidates in enumeration order, including failures.
- `all_models.parquet`: optional columnar equivalent.
- `ranked_models.tsv`: scored rows first, then unscored/failed rows.
- `top_models.tsv`: top-N eligible models.
- `best_model.json`: best row, exact parameters, and resolved run configuration.
- `model_selection_manifest.json`: formula, realized weights, counts, ordering, selected ID, and Pareto disclaimer.
- `top_model_artifacts/<model_id>/`: labels, annotations where available, summary, and fixed reproduction YAML.

## Model-family comparisons

`family_summaries.tsv` groups the landscape independently by selection method, UMAP metric, HDBSCAN metric, maximum cluster size, major UMAP controls, and major HDBSCAN controls. It reports candidate/success/failure counts plus best and median scores and component metrics.

These group summaries compare declared parameter families; they do not imply causal effects because other search dimensions may be imbalanced.

## Pareto front

The supplementary non-dominance calculation maximizes silhouette and cluster count while minimizing noise fraction and largest-cluster fraction. A candidate is retained if no other successful candidate is at least as good on every objective and strictly better on at least one.

Cluster count is included because the legacy framework values retained topology, not because more clusters are universally preferable. Pareto membership represents unresolved trade-offs and is never a unique scientific truth.
