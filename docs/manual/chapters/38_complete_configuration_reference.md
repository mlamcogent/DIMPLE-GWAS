# 38. Complete configuration reference

> **Release status.** DIMPLE-GWAS Freeze 3 RC1 (`3.0.0rc1`) is software-complete under local and fixed-fixture evidence. It is not yet scientifically frozen or cross-platform validated.

## Orientation

This chapter belongs to **Part VI — Operational reference**. It separates observed Freeze 3 behavior from scientific interpretation, historical evidence, and pending release work.

## Learning objectives

After this chapter, you can:

- Look up every configuration key, default, constraint, and exposure.
- identify the evidence artifact that supports the behavior or boundary;
- describe one common misuse in language appropriate for a methods report.

Prerequisites: 11.

## Explanation and implementation

Configuration has seven top-level groups. `input` contains path, metadata-prefix count, separator, transform, and annotation join. `umap` contains twelve searchable embedding fields. `hdbscan` contains nine searchable density-clustering fields. `execution` contains repeats, threads, retention, safeguards, subsampling, seed, Parquet, DBCV, and strictness. `scoring` selects legacy/custom behavior. `interpretation` controls original-space similarity, order, noise, matching, figure safeguards, and optional coordinate associations. `search_mode` chooses the built-in base.

Standard defaults include four metadata columns, no transform, UMAP neighbors 30/min-dist 0/three components/Euclidean/densMAP true/base seed 42, HDBSCAN min-cluster-size 5:50, min-samples 2:20, epsilon 0:3, EOM/Euclidean, 1,000 repeats, `n_jobs=-1`, one candidate job, 20 retained models, DBCV and Parquet enabled, non-strict execution, legacy score excluding noise, and Pearson cluster-then-hclust explanation with exact matching. Stop values are exclusive.

Validation enforces finite values, supported metrics, min-dist≤spread, positive rates/sizes, EOM/leaf, valid maximum sizes, nonzero candidate jobs, valid score rules, and enumerated interpretation choices. The complete exact default/value reference is generated from source into `configuration_key_reference.tsv`.

## Evidence-backed example

Run `inspect-config` for standard, extended, fixed, and the tutorial custom YAML, then diff only the resolved values. This distinguishes mode defaults from overlays.

## Outputs to inspect

Inspect source YAML, resolved YAML, configuration hash, config-reference row, CLI exposure, validation errors, and search count.

## Common mistakes

Do not infer a default from an example. Do not forget that `max_cluster_size` is EOM-specific. Do not enable coordinate associations or large matrices without acknowledging their output and privacy cost.

## Scientific and operational limits

The package validates syntax/ranges, not scientific choice. A permitted metric or parameter range may still be inappropriate for a specific data-generating process.

## Completion check

Choose five keys and label each value in a report as default, tutorial, historical, or recommendation.

<p class="xref"><strong>Operational cross-reference:</strong> Chapter 37 covers commands, Chapter 38 configuration, Chapter 41 artifact schemas, Chapter 42 provenance, and Chapter 46 current limitations.</p>
