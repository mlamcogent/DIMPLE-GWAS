# Linear and nonlinear views of multivariate structure

Dimension reduction is sometimes described as a race in which one method wins. That framing is usually wrong. A principal component, an independent component, a metric map, and a neighborhood embedding are different summaries of a high-dimensional object. The useful question is not “Which method is best?” but “Which relationship does this method try to preserve, and does that relationship match the scientific task?”

## PCA: directions of variance

For a centered data matrix $Y\in\mathbb{R}^{p\times v}$, principal component analysis seeks orthogonal directions $\mathbf{w}_k$ that maximize projected variance. The first component solves

$$
\mathbf{w}_1=\arg\max_{\|\mathbf{w}\|_2=1}\operatorname{Var}(Y\mathbf{w}),
$$

and subsequent components maximize variance subject to orthogonality. Equivalently, the loadings are eigenvectors of a covariance matrix or right singular vectors of the centered data.

PCA supplies linear axes, ordered variance, and loadings that can help identify which coordinates contribute to an axis. It is valuable when global continuous structure and linear combinations are the target. It does not automatically recover biological mechanisms, and a component can reflect technical variance or correlated error. Nevertheless, it is an important comparator precisely because it asks a clear, different question [@jolliffe2002pca].

## ICA: statistical independence under stronger assumptions

Independent component analysis represents observed data as mixtures of latent sources, often written

$$
Y = AS,
$$

where rows or columns of $S$ are sought to be statistically independent and $A$ is a mixing matrix. Identifiability requires assumptions such as non-Gaussianity and is generally only up to scaling and permutation. ICA can separate patterns that variance ordering alone does not distinguish, but an “independent component” remains a statistical construct requiring scientific validation [@hyvarinen2000ica].

Oblong and colleagues applied genomic PCA and ICA to 2,240 brain IDPs and explicitly evaluated reproducibility across UK Biobank releases [@oblong2024components]. That work is a relevant comparator and a reminder: reproducibility is an empirical analysis, not a property conferred by the name of a method.

## MDS and metric preservation

Classical multidimensional scaling begins from pairwise dissimilarities and seeks coordinates whose Euclidean distances approximate them. When the dissimilarities are Euclidean, classical MDS is closely connected to PCA. Non-metric MDS can instead preserve rank order. These methods foreground global pairwise relationships, whereas UMAP foregrounds a weighted neighborhood graph.

This difference explains why two valid representations can disagree. A method preserving global distance may sacrifice local density detail. A neighborhood method may retain local adjacency while distorting long-range distance. A visually separated pair of UMAP groups need not be far apart in the original metric, and a large principal-component separation need not define a persistent density cluster.

## UMAP: a graph and an optimization problem

UMAP constructs local neighborhoods, converts them into a fuzzy graph, and optimizes low-dimensional coordinates whose fuzzy relationships resemble that graph [@mcinnes2018umap]. The output axes are not loadings. Their sign, rotation, orientation, and precise positions can change across runs. The inferential object is closer to a neighborhood representation than to an ordered linear decomposition.

This makes UMAP useful for irregular local structure and exploratory visualization. It also creates familiar hazards: apparent global distances can be misleading, parameters alter the graph, and stochastic optimization adds variability. densMAP adds a density-related objective, but it does not turn the map into a calibrated physical or biological space [@narayan2021densmap].

## Multivariate genetic methods ask other questions

Genomic SEM models a specified multivariate genetic covariance structure [@grotzinger2019genomicsem]. MTAG combines information across traits to estimate trait-specific association effects [@turley2018mtag]. MOSTest and PLEIO are multivariate association methods designed to detect pleiotropic signal under their own assumptions [@vandermeer2020mostest; @lee2021pleio]. These are not alternative plotting algorithms. They estimate or test objects that DIMPLE-GWAS does not.

A fair comparison must therefore declare an estimand. If the target is locus discovery, a clustering purity score is irrelevant. If the target is recovery of a known continuous genetic factor, the evaluation should measure factor recovery rather than visual separation. If the target is exploratory grouping for follow-up, one might compare partition stability, neighborhood preservation, interpretability, and external replication under matched inputs and tuning budgets.

Stage 1 found no completed matched benchmark of this kind. Edition 3 uses “complementary” rather than “superior” for the current evidence.

## What Freeze 3 actually does

The active preprocessing-to-embedding path contains no PCA, ICA, SVD, or MDS. The full prepared vectors-by-variant matrix is passed directly to UMAP. This implementation fact should not be expanded into “no information is lost.” Metadata removal, optional RINT, metric construction, neighborhood selection, low-dimensional optimization, and concatenation all transform the relationships available downstream.

The absence of a linear reducer has two practical consequences. First, computation and neighborhood search operate on the full prepared variable dimension. Second, analysts cannot interpret the displayed UMAP coordinates as PCA-like loadings. If an explanation requires which original coordinates distinguish a group, the correct route is to return to the original matrix and to independent scientific follow-up, not to name an embedding axis.

## A comparator thought experiment

Suppose a dataset contains one broad linear gradient with two small, curved high-density regions. PCA may accurately summarize the dominant global gradient. UMAP may emphasize the local regions. HDBSCAN on the UMAP representation may call those regions clusters and treat the bridge as noise. None of these statements makes another method wrong. They answer different questions about variance, neighborhood, and density.

Now suppose the same apparent regions disappear when the metric changes or when participants from an independent cohort generate the summary statistics. The original plot remains a faithful output of its run, but the scientific interpretation weakens. Representation quality and biological transportability are separate claims.

## The decision created by this chapter

An analyst should be able to write a one-paragraph representation rationale before fitting: the structure of interest, the relationships to preserve, the role of linear comparators, the sensitivity analyses, and the claim that will be withheld unless external evidence arrives. That rationale is more important than declaring one method modern and another old.

The next two chapters open UMAP and densMAP so that the pipeline's nonlinear representation can be understood as a sequence of local graph decisions rather than a visual black box.

**Evidence trail.** Claims PRE-002, UMA-001, SLM-002 and SLM-024; dossier domains 1 and 10; gap G-010.

## Questions for the reader

1. Contrast the inferential objects of PCA and UMAP in two sentences.
2. Why would a matched benchmark against MOSTest require a different outcome than a benchmark of cluster stability?
3. Rewrite “DIMPLE is superior because it is nonlinear” as a bounded, testable research claim.

\newpage
