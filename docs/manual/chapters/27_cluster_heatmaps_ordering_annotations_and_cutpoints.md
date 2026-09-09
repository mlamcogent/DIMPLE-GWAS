# 27. Cluster heatmaps, ordering, annotations, and cutpoints

> **Release status.** DIMPLE-GWAS Freeze 3 RC1 (`3.0.0rc1`) is software-complete under local and fixed-fixture evidence. It is not yet scientifically frozen or cross-platform validated.

## Orientation

This chapter belongs to **Part IV — Explainability and responsible interpretation**. It separates observed Freeze 3 behavior from scientific interpretation, historical evidence, and pending release work.

## Learning objectives

After this chapter, you can:

- Reconstruct heatmap order and read cutpoints and annotations safely.
- identify the evidence artifact that supports the behavior or boundary;
- describe one common misuse in language appropriate for a methods report.

Prerequisites: 25-26.

## Explanation and implementation

The explanation heatmap is a rendered view of an auditable order. `heatmap_order.tsv` records 1-based display order, exact feature ID, cluster label/noise flag, and supplied coordinates. `cluster_cutpoints.tsv` records zero- and one-based inclusive block boundaries and sizes. Within a cluster, `cluster_then_hclust` applies hierarchical ordering to the original-space similarity-derived distance; other choices are cluster, hclust, or input order.

Annotations come from an optional table joined by the declared index column. The initial tutorial configuration used the wrong join key and produced a warning; the source YAML was corrected to `index` and Tutorial 1 rerun as `run_20260825_v2`. The earlier output remains as evidence of the mistake. Figure interpretation should always use sidecars, not inferred pixel positions.

## Evidence diagram or figure

![Figure 6. Ordered original-space Pearson heatmap from the executed synthetic explanation. Descriptive, post-selection evidence.](../assets/figures/figure_06_original_space_heatmap.png)



*Figure 6. Ordered original-space Pearson heatmap from the executed synthetic explanation. Descriptive, post-selection evidence. Source and checksum: `evidence/figure_source_manifest.tsv`.*

## Evidence-backed example

Figure 6 is copied byte-for-byte from Tutorial 3's `original_space_heatmap.png`; its source checksum and script/manifest are in `figure_source_manifest.tsv`. The synthetic groups are designed, and the image is unrestricted fixture evidence.

## Outputs to inspect

Inspect heatmap PNG/HTML, exact order, cutpoints, cluster summary, exclusions, annotations, manifest hash, and README caveats.

## Common mistakes

Do not reorder the image manually and leave sidecars unchanged. Do not assume coloured blocks are statistically significant. Do not publish annotations without checking privacy/access status.

## Scientific and operational limits

Large matrices are protected by thresholds and optional forcing. A full-resolution heatmap can be unreadable or disclose identifiers; use aggregate summaries and controlled access when appropriate.

## Completion check

Reconstruct the first cluster's row interval using both zero- and one-based cutpoints, and match it to `heatmap_order.tsv`.

<p class="xref"><strong>Operational cross-reference:</strong> Chapter 37 covers commands, Chapter 38 configuration, Chapter 41 artifact schemas, Chapter 42 provenance, and Chapter 46 current limitations.</p>
