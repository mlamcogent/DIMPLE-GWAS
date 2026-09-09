# Backward Compatibility

## Compatibility boundary

The authoritative dev script remains preserved in the upstream Dev/Freeze 2 evidence trees; it is intentionally excluded from the clean Freeze 3 source. The supported Freeze 3 interface is `python -m dimple_gwas` or the installed `dimple-gwas` command.

`standard` mode reproduces the dev declarations:

- drop four metadata columns;
- no RINT unless requested;
- densMAP on;
- UMAP neighbors 30, minimum distance 0, three components, Euclidean metric;
- 1,000 repeated embeddings with seeds 1 through 1,000;
- HDBSCAN epsilon `0,1,2`, minimum samples `2..19`, minimum cluster size `5..49`;
- EOM, persistence 0, alpha 1, no single cluster, unlimited maximum size, Euclidean metric;
- legacy DIMPLE scoring with default noise exclusion.

## Regression result

The copied dev script and Freeze 2 were previously run on the same deterministic 80-variant × 24-feature GWAS-shaped matrix with one UMAP/HDBSCAN configuration. Freeze 3 retains those inherited tests and adds a fresh Freeze 2 versus Freeze 3 fixed-run comparison.

| Quantity | Dev | Freeze 2 | Status |
|---|---:|---:|---|
| Clusters | 3 | 3 | exact |
| Noise points | 0 | 0 | exact |
| Labels | — | — | exactly equal |
| Silhouette | 0.9585651253 | 0.9585650563 | absolute difference `6.90e-08` |

The declared tolerance is `1e-6`. The small silhouette difference comes from dev writing the float32 repeated embedding to CSV and re-reading it before grid scoring, whereas Freeze 2 evaluates the in-memory float32 array. Labels are exact.

The Freeze 3 evidence bundle is outside the source tree at `freeze3_workspace/`; its fixed-run comparison reports exact labels, ARI/NMI/noise Jaccard of 1.0, and effectively zero Procrustes disparity.

## CLI mappings

| Dev spelling | Freeze 3 spelling | Notes |
|---|---|---|
| `--datainput` | `run --input` | old alias accepted |
| `--outdir` | `--output-dir` | old alias accepted |
| `--n_neighbors` | `--umap-n-neighbors` | underscore alias accepted |
| `--min_dist` | `--umap-min-dist` | underscore alias accepted |
| `--n_components` | `--umap-n-components` | underscore alias accepted |
| `--grid_eps` | `--hdbscan-cluster-selection-epsilon` | old alias accepted |
| `--grid_min_samples` | `--hdbscan-min-samples` | old alias accepted |
| `--grid_min_cluster_size` | `--hdbscan-min-cluster-size` | old alias accepted |
| `--idp_key` | `--annotation-file` | deprecated generic alias accepted |
| `--fit_include_noise` | `--fit-include-noise` | semantics preserved |

Old per-stage output path overrides remain features of the archived `DIMPLEGWAS.py`; Freeze 3 uses a structured output contract. `stage02` and `stage03` CSV aliases plus best-model stage09 tables are written where practical.

## Intentional additions

UMAP/HDBSCAN metrics, maximum cluster size, and the remaining scientifically meaningful parameters can be searched. All candidate rows are retained, statuses are explicit, formula manifests are written, top-N labels are reproducible, and grouped/Pareto summaries are added. These additions do not change standard-mode parameter defaults.
