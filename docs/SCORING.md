# Scoring

## Legacy DIMPLE profile

`legacy_dimple` is the default. It preserves the authoritative dev calculation and its edge-case handling.

For eligible candidate (i), define:

\[
\tilde{s}_i = s_i / \max(s), \quad
\tilde{c}_i = c_i / \max(c), \quad
\tilde{n}_i = n_i / \max(n).
\]

If a component maximum is zero, its normalized values are zero. Raw ranges are:

\[
r_s = \max(s)-\min(s),\quad
r_c = \max(c)-\min(c),\quad
r_n = \max(n)-\min(n).
\]

When their sum is positive, each weight is its range divided by the range sum. Otherwise, active components receive equal weights. The raw score is:

\[
R_i = w_s\tilde{s}_i + w_c\tilde{c}_i - w_n\tilde{n}_i.
\]

Finally:

\[
Score_i = \frac{R_i - \min(R)}{\max(R)-\min(R)}.
\]

If the final range is zero, every eligible score is one.

With default `fit_include_noise: false`, `n_i` is set to zero for scoring and `w_n=0`; observed noise remains reported. With `fit_include_noise: true`, silhouette includes the noise label and the noise-count penalty is active. The manifest records scope, raw ranges, realized weights, formula, and edge cases.

The legacy formula combines ranges in their native units. As the full MNIST benchmark demonstrates, cluster-count range can dominate silhouette range. Freeze 3 preserves this for compatibility but exposes every component so users can declare a different scientific objective.

## Custom scoring

Custom YAML names each metric, a non-negative weight, and a direction:

```yaml
scoring:
  profile: custom
  custom:
    silhouette: {weight: 0.45, direction: maximize}
    noise_fraction: {weight: 0.25, direction: minimize}
    largest_cluster_fraction: {weight: 0.20, direction: minimize}
    hdbscan_persistence_mean: {weight: 0.10, direction: maximize}
```

Freeze 3 validates metric availability and requires every active metric to be finite for an eligible model. Each metric is min-max normalized, minimized components are inverted, declared weights are normalized to sum to one, and the weighted raw result is rescaled to `[0,1]`. Zero-range components contribute zero.

No preferred cluster-count band, noise ceiling, largest-cluster threshold, pQTL rule, or biological target is hidden in either profile.
