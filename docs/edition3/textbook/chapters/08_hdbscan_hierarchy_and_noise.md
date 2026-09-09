# HDBSCAN: from mutual reachability to persistent clusters

K-means asks for a fixed number of groups organized around centroids. HDBSCAN asks a different question: which connected regions remain sufficiently dense across a hierarchy of scales? This makes HDBSCAN attractive for irregular shapes, variable cluster counts, and explicit unassigned observations. It also means that cluster identity depends on the representation, metric, density parameters, and extraction rule.

## Core distance

For a chosen `min_samples` value $k$, the core distance of object $i$ is the distance to its $k$th nearest neighbor:

$$
c_k(i)=d(i,N_k(i)).
$$

In a dense region, $c_k(i)$ is small; in a sparse region, it is larger. Increasing `min_samples` generally makes the density criterion more conservative because a point must look dense over a broader neighborhood.

## Mutual-reachability distance

HDBSCAN transforms pairwise distance into

$$
d_{\mathrm{mreach},k}(i,j)=\max\{c_k(i),c_k(j),d(i,j)\}.
$$

This prevents two sparse points from appearing strongly connected merely because they are close to one another. The connection is no stronger than the sparser endpoint's core distance.

Suppose $c_k(A)=0.4$, $c_k(B)=0.7$, and $d(A,B)=0.3$. Then $d_{\mathrm{mreach}}(A,B)=0.7$. If $B$ lies in a sparse region, its local scale controls the edge even though the raw pairwise distance is small.

## From a spanning tree to a hierarchy

HDBSCAN constructs a minimum spanning tree under mutual-reachability distance and considers components as edges are removed from large distance to small density scale. It is convenient to express density level as $\lambda=1/d_{\mathrm{mreach}}$. As $\lambda$ increases, the hierarchy moves toward denser structure and components split.

The raw hierarchy contains many short-lived branches. A condensed tree applies `min_cluster_size`, removing branches that never contain enough observations and recording how points leave surviving components. A cluster's stability integrates its membership over the density interval in which it persists. In conceptual form,

$$
S(C)=\sum_{i\in C}(\lambda_i-\lambda_{\mathrm{birth},C}),
$$

where $\lambda_i$ is the level at which object $i$ leaves cluster $C$. The contributed `hdbscan` package handles the exact bookkeeping; DIMPLE-GWAS supplies declared parameters and retains outputs.

## EOM and leaf selection

Excess-of-mass (EOM) selection compares the stability of a parent cluster with the aggregate stability of descendants and chooses a non-overlapping set. Leaf selection chooses terminal branches of the condensed tree, often producing finer groups. Neither rule is universally correct. EOM favors stable coarser structure; leaf selection emphasizes local terminal density components.

Freeze 3 exposes both. It also records that maximum cluster size has no effective pruning role under leaf selection in the current backend mapping. This is a parameter-interaction fact, not a reason to treat the selection methods as interchangeable.

`cluster_selection_epsilon` can merge fine structure below a distance threshold; `alpha`, persistence thresholds, minimum cluster size, minimum samples, metric, single-cluster permission, and maximum cluster size further alter the extracted solution. Each should be visible in the resolved configuration and candidate table.

## Why label `-1` is valuable and easy to misuse

HDBSCAN assigns `-1` to observations not retained in a selected sufficiently persistent dense component. This is an algorithmic statement. An unassigned phenotype can lie between groups, occupy a sparse tail, be unstable under seeds, be affected by scale, or represent scientifically interesting uniqueness. It is not automatically error, non-heritability, absence of pleiotropy, or a failed phenotype.

The amount of noise also changes internal metrics. A model can improve non-noise silhouette by assigning difficult boundary points to `-1`. That may be appropriate, but it creates a trade-off between compact clusters and coverage. A score that includes or excludes noise encodes a scientific preference and must disclose it.

## A topology can be invalid for scoring without being a backend failure

Freeze 3 requires at least two non-noise clusters for an eligible clustering topology. A fit yielding one or zero non-noise clusters is retained as `invalid_topology` rather than silently discarded. A backend exception is recorded as a failure. This distinction preserves the search landscape: the analyst can see whether a parameter family was computationally invalid, structurally ineligible, or simply lower ranked.

Retaining these outcomes matters. If most candidates fail or collapse to one cluster, the chosen model may be a fragile survivor rather than strong evidence of natural grouping.

## Metrics and hierarchy answer different questions

Silhouette compares within-cluster cohesion with the nearest alternative cluster under a declared metric. DBCV evaluates a density-oriented relative validity structure. Cluster persistence comes from the HDBSCAN hierarchy. Calinski-Harabasz and Davies-Bouldin use Euclidean centroid geometry in the current implementation. Agreement among these diagnostics can be reassuring; disagreement is also informative because they reward different structure.

No internal metric identifies the biological origin of the separation. A high DBCV says that the partition fits a density-validity criterion under the representation. It does not say that the clusters are causal classes.

## K-means is a comparator, not a straw man

K-means minimizes within-cluster squared Euclidean distance around centroids. It can be effective for roughly convex, similar-variance groups and offers an interpretable objective. It may be poorly matched to irregular, hierarchical, or variable-density structure. Calling it “completely ineffective” replaces a design comparison with rhetoric. A fair study should choose methods based on the geometry and evaluate them under a matched target.

## What to inspect after a fit

Inspect the label counts, the number of non-noise clusters, the noise fraction, cluster sizes, probabilities or persistence summaries where retained, diagnostic scopes, and candidate status. Compare these across neighboring parameter settings. A selected cluster that vanishes when `min_samples` changes by one deserves a different claim from a persistent branch across a reasonable family.

The next chapter constructs that family explicitly. Search-space design is not merely a compute setting; it defines the alternatives against which the selected HDBSCAN model can win.

**Evidence trail.** Claims HDB-001 to HDB-003, MET-002 to MET-004, SLM-006, SLM-008 and SLM-009; coverage COV-007 and COV-010; primary sources [@campello2015hdbscan; @mcinnes2017hdbscan].

## Questions for the reader

1. Compute mutual-reachability distance for core distances 0.5 and 0.2 with raw distance 0.4.
2. Why can assigning more observations to noise increase non-noise silhouette?
3. Give a situation in which leaf selection is scientifically interesting but less stable than EOM.

\newpage
