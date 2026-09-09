# Known issues

## Open validation limitation

The fresh original 164-IDP 1,000-seed concatenated-UMAP run is pending. Impact: Freeze 3 is a software-complete release candidate, not scientifically frozen. Next action: execute `configs/original_idp_164_selected.yaml` in a controlled new output directory, then run `compare` and review named cluster membership.

## Historical provenance limitations

- The 164-IDP final solution was manually selected at sorted score row 16, not by the canonical top-rank rule. Freeze 3 records this and does not generalize the preference.
- Historical notebooks have out-of-order/stale execution state in some versions. The 164 and 459 contracts are corroborated by coherent executed output plus the final workbook; the broader 2,315/459 raw matrices are absent locally.
- One historical `UMAP_3` cell for `IDP_2143` is missing from both final workbooks. Two complete coordinates were used for projection diagnostics; original-space similarity is unaffected.
- Exact historical numerical dependency versions are not fully locked beyond evidence of Python 3.9 and warning paths. Current numerical versions are recorded in the resolved environment.

## Runtime considerations

- Repeated UMAP concatenates three dimensions per seed. Large repeat counts increase runtime and the HDBSCAN input width linearly.
- Spearman similarity adds ranking cost and a full vector-by-vector table scales quadratically. More than 10,000 vectors requires an explicit force flag.
- `validate` checks artifact/schema/hash integrity; it is not a biological or statistical validation.
- macOS joblib may warn when physical-core discovery returns an empty system value and will use logical cores.

## Deferred features

Cluster ANOVA/post-selection p-values, permutation tests, surrogate models, causal attribution, parametric UMAP, and container/cloud claims are outside Freeze 3.
