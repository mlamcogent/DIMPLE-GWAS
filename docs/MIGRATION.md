# Migration to Freeze 3

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
