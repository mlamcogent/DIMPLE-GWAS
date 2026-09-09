# 20. The legacy_dimple score and optional alternatives

> **Release status.** DIMPLE-GWAS Freeze 3 RC1 (`3.0.0rc1`) is software-complete under local and fixed-fixture evidence. It is not yet scientifically frozen or cross-platform validated.

## Orientation

This chapter belongs to **Part III — The complete DIMPLE-GWAS workflow**. It separates observed Freeze 3 behavior from scientific interpretation, historical evidence, and pending release work.

## Learning objectives

After this chapter, you can:

- Reconstruct the score, define dynamic-range weights, and distinguish computed metrics from score terms.
- identify the evidence artifact that supports the behavior or boundary;
- describe one common misuse in language appropriate for a methods report.

Prerequisites: 19.

## Explanation and implementation

`legacy_dimple` is the default compatibility score. Among eligible candidates, each included component is divided by its maximum. Its weight is the component's raw observed range divided by the sum of included ranges. Raw score adds normalized silhouette and normalized non-noise cluster count and, only when `fit_include_noise=true`, subtracts normalized noise count. The raw score is finally scaled to [0,1] over the eligible candidate population; a zero range maps to 1.

This is population-relative: adding or removing candidates can change maxima, ranges, weights, and final scores even if an existing candidate's own metrics do not change. DBCV may be present in the table but is not a legacy-score term. No preferred cluster band, noise ceiling, largest-cluster target, or biological label is embedded.

The `custom` profile accepts explicitly declared metric weights and maximize/minimize directions. It should represent a preregistered analytic objective, not weights tuned after viewing a desired partition.

## Evidence-backed example

In Tutorial 2, all candidates have the same cluster count and no noise, so UMAP-family silhouette differences drive four score levels and eight-way ties within families. The selection manifest records realized formula and tie order.

## Outputs to inspect

Inspect `raw_score`, `score`, compatibility aliases, scoring profile, noise-fit flag, realized weights/ranges, eligible counts, and tie order in `model_selection_manifest.json`.

## Common mistakes

Do not say DBCV selected the model when profile is legacy. Do not compare normalized scores across candidate populations as though absolute. Do not introduce outcome-informed custom weights.

## Scientific and operational limits

A heuristic rank is not a probability, confidence, p-value, or guarantee of stability. Scientific selection should combine transparent objectives, sensitivity, and external evidence.

## Completion check

Using Appendix B, explain why the same model can receive a different normalized score after the candidate set expands.

<p class="xref"><strong>Operational cross-reference:</strong> Chapter 37 covers commands, Chapter 38 configuration, Chapter 41 artifact schemas, Chapter 42 provenance, and Chapter 46 current limitations.</p>
