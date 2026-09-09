# Appendix G — Migration from Dev and Freeze 2

## From Dev

Use `dimple-gwas`, not `DIMPLEGWAS.py`. The Dev defaults are represented by `standard`/`legacy_dimple`; legacy flag aliases such as `--datainput`, `--drop_first_n_cols`, and `--idp_key` remain accepted. `--idp_key` maps to generic annotation input and does not impose IDP-specific semantics.

Dev candidate outputs remain available as stage-number aliases, while native model tables add explicit status, parameter identity, metric scope, raw/final score, and provenance fields.

## From Freeze 2

All Freeze 2 commands and configuration sections remain. Version changes from `2.0.0` to `3.0.0rc1`. The additive `interpretation` section does not affect model IDs, topology fitting, or ranking.

New commands are `explain` (`interpret` alias), `compare`, and `validate`. Run manifests use schema `dimple-gwas.provenance.v3`; top summaries bind `labels.tsv` by SHA-256.

Freeze 3 corrects the documented extended-search count from 5,184 to the enumerated 1,728. No candidate definition changed to make this correction.

## From the standalone explanation prototype

| Prototype concept | Freeze 3 | Decision |
| --- | --- | --- |
| `--matrix` | `--input` | One package input spelling. |
| `--umap` | native `--model-json` or `--legacy-table` | Native retained artifacts preferred. |
| `--corr-method` | `--similarity-metric` | Original-space diagnostic naming. |
| `--include-noise` | `--noise-policy` | Separate/include/exclude semantics. |
| `--write-correlation-matrix` | `--write-similarity` | Complete table optional, default on. |
| `--methods` | `--coordinate-associations` | Coordinate correlations only; ANOVA deferred. |
| duplicate fit-score command | `score-existing` | Canonical package score only. |

The prototype CLI, its manifest schema, and its parallel reader/scoring implementation are not shipped.

## Historical model tables

`score-existing` recognizes notebook columns `Silhouette_avg`, `Clusters`, `Noise_points`, `Epsilon`, `Min_samples`, and `Min_cluster_size`. It preserves input score fields with `source_` prefixes and records migrations in the scoring manifest.

## Deliberately excluded

The historical monolith, Modded scikit-learn-HDBSCAN/soft-target experiment, Dockerfile, prior outputs, virtual environments, caches, egg metadata, and cluster prototype are preserved outside the Freeze 3 source tree. They are not production entry points.


# Migration from Dev

## Minimal migration

Historical execution remains available only from the preserved Dev/Freeze 2 evidence tree:

```bash
python DIMPLEGWAS.py --datainput matrix.tsv --outdir outputs/legacy ...
```

The supported Freeze 3 starting point is:

```bash
python -m dimple_gwas run \
  --input matrix.tsv \
  --search-mode standard \
  --scoring-profile legacy_dimple \
  --output-dir outputs/freeze3
```

Standard mode is intentionally large: 2,430 HDBSCAN candidates after a 1,000-run UMAP ensemble. Inspect first with `show-search-space`, and use fixed/custom settings for smoke tests.

## Move parameters into YAML

Start from `configs/legacy_dev.yaml`, then convert a fixed value to a list only when that dimension belongs in the scientific search. For example:

```yaml
umap:
  metric: [euclidean, cosine]
hdbscan:
  cluster_selection_method: [eom, leaf]
  max_cluster_size: [0, 100]
```

Run `inspect-config` to verify precedence and `show-search-space` to see the complete product before computing.

## Output migration

Use `models/ranked_models.tsv` rather than assuming stage03 contains the only meaningful solution. Use `models/best_model.json` for the declared winner, `models/top_models.tsv` for alternatives, and per-model `reproduce.yaml` files for exact reruns. Failed candidates are data, not lost exceptions.

The stage09 best-model table names remain available. Annotation columns now use generic feature IDs and are also retained within each top-model artifact.

## Reproduction

```bash
python -m dimple_gwas reproduce-model \
  --model-json outputs/freeze3/models/best_model.json \
  --output-dir outputs/reproduced
```

Pass `--input` if the recorded path is no longer valid.

## Deprecated terminology

`--idp_key` is accepted as an alias but new workflows should use `--annotation-file` and `--annotation-index-col`. No pQTL, IDP, imaging, or modality name appears in default topology selection.


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
