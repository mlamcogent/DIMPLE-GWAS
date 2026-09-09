# densMAP and relative local density

Standard UMAP is principally concerned with neighborhood relationships. Yet density matters for the next stage of DIMPLE-GWAS: HDBSCAN will interpret dense and sparse regions of the representation. If the embedding compresses one region and expands another, density clustering can see a landscape that differs from the original local structure. densMAP was designed to preserve more information about relative local density while retaining UMAP's graph objective [@narayan2021densmap].

## What density can mean in a neighborhood graph

In a simple Euclidean space, local density might be estimated from the radius required to reach $k$ neighbors. Let $r_i^{\mathrm{orig}}$ summarize a local radius around object $i$ in the original space and $r_i^{\mathrm{emb}}$ the corresponding radius in the embedding. A density-preserving objective encourages the pattern of these radii to correspond across spaces.

The exact densMAP implementation uses local radius proxies and a correlation-oriented regularization inside the optimization. A useful conceptual objective is

$$
\mathcal{L}_{\text{densMAP}}
=\mathcal{L}_{\text{UMAP}}
+\lambda\,\mathcal{L}_{\text{density}},
$$

where $\lambda$ is controlled by a density-weight parameter. The density term is not a claim that either radius equals true biological density. It is a penalty encouraging the low-dimensional representation to retain more of a chosen local-density ordering.

## A compression example

Imagine two groups with the same number of observations. Group A occupies a small original-space neighborhood; group B is spread over a much larger region. Standard UMAP may draw both as similarly compact islands if doing so preserves their neighbor graphs. HDBSCAN would then receive misleadingly similar apparent densities. densMAP penalizes this particular loss of relative density information, making it more likely that A remains visually and numerically denser than B.

Now change the metric or the feature scaling. The original neighborhood radii change, so the density target changes. densMAP cannot escape the geometry declared upstream. It preserves information about density *under that construction*.

## Parameters and trade-offs

The density regularization competes with the ordinary UMAP objective. Increasing its weight can improve relative-density correspondence while changing local adjacency or visual compactness. The fraction of training epochs during which the density term is active and the density neighborhood scale also affect the result. There is no parameter setting that guarantees simultaneous preservation of all neighborhoods, global distances, densities, and cluster boundaries.

This trade-off is scientifically relevant in DIMPLE-GWAS because HDBSCAN is downstream. A densMAP setting that changes the persistence of a density component has changed the selected clustering problem, not merely the appearance of a plot.

## “Density preserving” needs a careful object

Three unsafe shortcuts are common.

First, “densMAP preserves the true density of the data.” It does not. It adds an objective for correspondence of local density proxies between declared spaces.

Second, “a dense embedded region is a biological subtype.” Density can reflect biological coherence, but also scale, duplicated information, LD, sample overlap, technical correlation, or transformation choices.

Third, “densMAP makes HDBSCAN valid.” It can reduce a particular representation mismatch, but cluster validity still depends on parameter sensitivity, candidate selection, and external evidence.

The safe statement is narrower: densMAP is intended to retain more information about relative local density than standard UMAP, and its consequences should be measured in the actual analysis.

## The implementation and the missing comparison

Freeze 3 exposes a Boolean `densmap` setting and the relevant UMAP parameters through resolved configuration. Standard mode enables densMAP. The Stage 1 fixed tutorial also used densMAP and produced one clear synthetic partition. No current Stage 1 benchmark systematically compared densMAP against standard UMAP on the real IDP analyses. The documentation therefore describes the implemented option and the method's rationale without claiming that densMAP improved the manuscript results.

A useful comparison would hold preprocessing, metric, seeds, and HDBSCAN search as constant as possible; fit both representation families; report trustworthiness, continuity, local-radius correspondence, cluster and noise stability, candidate failures, and the sensitivity of selected partitions. Because selection is performed within each family, the comparison should also disclose candidate populations and avoid treating different table-relative scores as absolute cross-family measurements.

## A diagnostic thought experiment

Suppose densMAP produces a higher DBCV and more noise than standard UMAP. One interpretation is that preserving relative density exposed sharper dense cores and left transition observations unassigned. Another is that the regularization exaggerated density contrasts that are unstable to seed or metric. Internal metrics alone cannot choose between those stories. Seed stability, alternative preprocessing, original-space inspection, and external evidence are needed.

This illustrates a general rule: a method designed around density does not turn density into truth. It changes which structural property the representation prioritizes.

## From one stochastic fit to several

Even with parameters fixed, UMAP and densMAP use stochastic optimization. DIMPLE-GWAS addresses dependence on a single realization by fitting repeated seeded views and concatenating their coordinates. The next chapter explains exactly what that operation computes—and why it should be called an empirical multi-view representation rather than a proven consensus estimator.

**Evidence trail.** Claims UMA-003, SLM-003 and SLM-008; coverage COV-005; gap COV-005's absent densMAP-versus-UMAP benchmark.

## Questions for the reader

1. Why does changing the original-space metric also change the density object densMAP tries to preserve?
2. Give two explanations for a higher DBCV under densMAP that do not imply better biological validity.
3. Design a fair densMAP-versus-UMAP comparison without comparing table-relative legacy scores as absolute values.

\newpage
