# 16. UMAP and densMAP fundamentals

> **Release status.** DIMPLE-GWAS Freeze 3 RC1 (`3.0.0rc1`) is software-complete under local and fixed-fixture evidence. It is not yet scientifically frozen or cross-platform validated.

## Orientation

This chapter belongs to **Part III — The complete DIMPLE-GWAS workflow**. It separates observed Freeze 3 behavior from scientific interpretation, historical evidence, and pending release work.

## Learning objectives

After this chapter, you can:

- Relate configured UMAP parameters to the implementation without interpreting axes as loadings.
- identify the evidence artifact that supports the behavior or boundary;
- describe one common misuse in language appropriate for a methods report.

Prerequisites: 5-6, 15.

## Explanation and implementation

Freeze 3 passes the full prepared matrix to umap-learn. The searched UMAP keys are `n_neighbors`, `min_dist`, `n_components`, `metric`, `spread`, `learning_rate`, `repulsion_strength`, `negative_sample_rate`, `local_connectivity`, `set_op_mix_ratio`, `random_state`, and `densmap`. The standard defaults are 30 neighbors, minimum distance 0, three dimensions per repeat, Euclidean metric, and densMAP enabled.

`n_neighbors` influences the local-versus-broader neighborhood balance. `min_dist` and `spread` shape allowed packing in the embedded space. The metric defines neighbor dissimilarity in the prepared input space. densMAP adds density preservation pressure. Optimizer parameters affect the fitted representation. `n_components` is per repeat; it is not necessarily the number of coordinates later used for a display plot.

No user-visible PCA, SVD, or ICA pre-reducer exists in the production path. UMAP's internal initialization should not be misreported as an explicit preprocessing stage.

## Evidence-backed example

Tutorial 2 varies neighbors (10,15) and min_dist (0,0.1), giving four UMAP families. Candidate-score groups reflect those families, while the eight HDBSCAN variants within a family share the same embedding metrics.

## Outputs to inspect

Inspect flattened UMAP fields, `umap_id`, trustworthiness/continuity, seeds, runtime, and selected display coordinates. Compare the resolved config to the default reference.

## Common mistakes

Do not interpret UMAP_1/2/3 as effect directions or loadings. Do not compare coordinates from unaligned runs pointwise. Do not say densMAP preserves all global distances.

## Scientific and operational limits

UMAP behavior is stochastic and parameter/metric/data dependent. Projection diagnostics are bounded summaries, and a visually persuasive layout does not establish a unique topology.

## Completion check

Choose one UMAP parameter and describe the implementation-visible change you would audit without predicting a biologically preferred result.

## Evidence and references

See McInnes et al. (2018), DOI 10.21105/joss.00861; Narayan et al. (2021), DOI 10.1038/s41587-020-00801-7; and official UMAP parameter documentation.

<p class="xref"><strong>Operational cross-reference:</strong> Chapter 37 covers commands, Chapter 38 configuration, Chapter 41 artifact schemas, Chapter 42 provenance, and Chapter 46 current limitations.</p>
