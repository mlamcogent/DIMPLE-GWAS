# UMAP: from neighborhood graphs to coordinates

UMAP is often encountered as a two-dimensional scatterplot. In DIMPLE-GWAS, the important object comes earlier: a weighted graph describing local relationships in the prepared phenotype-vector space. The coordinates are an optimized representation of that graph, not direct measurements and not biological loadings.

## Step 1: find local neighbors

For each object $i$, UMAP identifies a set of nearest neighbors under the selected metric. The parameter `n_neighbors` controls the local scale at which this graph is built. A small value emphasizes fine local relations and can fragment broader structure. A large value mixes information over a wider region and can smooth small groups. The setting does not directly specify a cluster count; it defines which relationships the representation tries hardest to retain.

High-dimensional neighbor search is already sensitive to preprocessing and metric choice. UMAP cannot recover a metric-independent neighborhood graph because no such graph has been supplied. Its local construction begins after those choices.

## Step 2: calibrate distance locally

Objects can occupy regions of different sampling density. A raw distance of 0.4 may be very close in a sparse region and ordinary in a dense one. UMAP gives each object a local connectivity offset $\rho_i$ and a local scale $\sigma_i$. A pedagogical form of the directed membership strength from $i$ to neighbor $j$ is

$$
p_{j\mid i}=\exp\left[-\frac{\max(0,d(i,j)-\rho_i)}{\sigma_i}\right].
$$

Distances within the local-connectivity offset receive maximal membership; distances beyond it decay relative to the local scale. The library chooses $\sigma_i$ numerically to satisfy a target effective neighborhood mass. DIMPLE-GWAS delegates those internals to `umap-learn`; it does not reimplement the solver.

For intuition, let $\rho_i=0.2$, $\sigma_i=0.5$, and $d(i,j)=0.7$. Then

$$
p_{j\mid i}=\exp[-(0.7-0.2)/0.5]=e^{-1}\approx0.368.
$$

If $j$'s neighborhood has a different scale, $p_{i\mid j}$ need not equal this value. The graph is initially directed.

## Step 3: symmetrize the fuzzy graph

UMAP combines the two directed memberships with a fuzzy union:

$$
p_{ij}=p_{j\mid i}+p_{i\mid j}-p_{j\mid i}p_{i\mid j}.
$$

If both directions are 0.368, the union is approximately $0.601$. The `set_op_mix_ratio` parameter can blend union-like and intersection-like behavior. The result is a weighted undirected relation: high $p_{ij}$ means the high-dimensional graph considers the pair strongly connected under the local construction.

This is not a probability that the two phenotype vectors share a biological mechanism. It is a graph membership strength induced by the chosen data, metric, neighbor count, and local calibration.

## Step 4: define low-dimensional relationships

UMAP places coordinate vectors $\mathbf{z}_i\in\mathbb{R}^d$ in a low-dimensional space. A common pedagogical form for low-dimensional membership is

$$
q_{ij}=\frac{1}{1+a\|\mathbf{z}_i-\mathbf{z}_j\|^{2b}},
$$

where $a$ and $b$ are chosen from `min_dist` and `spread`. Close points have high $q_{ij}$; distant points have lower membership. Smaller `min_dist` permits tighter packing of strongly connected points. It does not guarantee more truthful clusters.

## Step 5: optimize a cross-entropy-like objective

The coordinates are optimized so that $q_{ij}$ resembles $p_{ij}$. Conceptually, the loss contains attractive terms for strong graph edges and repulsive terms for non-edges:

$$
\mathcal{L}=\sum_{i<j}\left[p_{ij}\log\frac{p_{ij}}{q_{ij}}+(1-p_{ij})\log\frac{1-p_{ij}}{1-q_{ij}}\right].
$$

Implementations use stochastic optimization and negative sampling rather than enumerating every non-edge. `learning_rate`, `repulsion_strength`, `negative_sample_rate`, initialization, and the random seed affect the optimization path. Supplying a fixed random state improves bounded reproducibility but can constrain parallelism, as the Stage 1 warning record shows.

## Why global distance is unsafe to read literally

The optimization emphasizes fuzzy local relationships, not exact preservation of every high-dimensional pairwise distance. Two regions can be placed far apart because there are few graph edges between them, but the amount and direction of empty space are not calibrated scientific measures. Rotations, reflections, and other changes can preserve relevant structure. Stochastic runs can also change global arrangement.

This is why UMAP axes are unnamed descriptive coordinates. Correlating an axis with original variables can be a descriptive exploratory calculation, but the axis is not a loading, a causal gradient, or a stable effect size.

## Parameters as questions

`n_neighbors` asks how local the graph should be. `min_dist` and `spread` shape the low-dimensional packing curve. The metric defines high-dimensional proximity. `n_components` sets representation capacity. `local_connectivity`, `set_op_mix_ratio`, learning rate, repulsion, and negative sampling alter graph construction or optimization. The seed controls a stochastic realization but does not fix differences caused by dependencies, threading, or hardware.

Parameter values should therefore be justified as a family of plausible questions. A sensitivity study should compare graph or partition structure, not merely choose the plot with the clearest gaps.

## Freeze 3 implementation

Freeze 3 passes the full prepared matrix directly to `umap-learn`. Standard mode currently resolves to `n_neighbors=30`, `min_dist=0`, three components, Euclidean metric, and densMAP enabled; custom configurations can override those values. The runner creates one embedding per declared seed and converts the coordinate blocks to `float32` before concatenation. The first view supplies display coordinates, while HDBSCAN uses the full concatenated representation.

The run manifest and model records preserve resolved parameters, seed lists, versions, and representation identifiers. The package does not write every individual embedding or the complete concatenated array as a canonical output. Absence of those files is a current contract, not evidence of a failed run.

## Diagnostics without overclaiming

Trustworthiness measures how often low-dimensional neighbors are unexpected relative to the original space; continuity measures how often original neighbors are missing from the embedding. Both depend on $k$, sampling, and the original metric [@venna2010trust]. In the fixed Stage 1 run, trustworthiness was about 0.868 and continuity about 0.878 at $k=10$. These values describe neighborhood retention for the synthetic fixture. They do not validate its three groups biologically.

The next chapter adds densMAP's density-related objective. That addition changes what the representation tries to preserve, but it does not remove the interpretive limits just developed.

**Evidence trail.** Claims UMA-001, UMA-003, UMA-004, MET-001 and SLM-004; coverage COV-004 and COV-009; primary sources [@mcinnes2018umap; @umap_reproducibility_docs].

## Questions for the reader

1. Calculate the fuzzy union when the two directed memberships are 0.2 and 0.7.
2. Explain why rotating a UMAP plot can preserve its relevant geometry while changing axis values.
3. What would you compare across two `n_neighbors` settings if visual appeal were excluded from the decision?

\newpage
