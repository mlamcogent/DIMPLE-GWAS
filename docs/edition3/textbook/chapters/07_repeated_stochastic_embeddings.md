# Repeated stochastic embeddings as a multi-view representation

A single UMAP result is one optimized realization of a stochastic procedure. DIMPLE-GWAS does not hide this fact. It fits several seeded embeddings and exposes HDBSCAN to all of their coordinate blocks at once. The intuition is appealing: a relationship that appears across several views may be less dependent on one optimization path. The exact operation, however, is concatenation—not averaging, alignment, bootstrapping, or formal consensus clustering.

![The same prepared matrix is embedded under several seeds. Coordinate blocks are concatenated for clustering; the first block is retained for display.](assets/figures/repeated_embeddings.png){#fig-repeated width=94%}

## The implemented construction

Let $f_s(Y)\in\mathbb{R}^{p\times d}$ be the UMAP or densMAP embedding under seed $s$. For seeds $s_1,\ldots,s_r$, Freeze 3 constructs

$$
Z=[f_{s_1}(Y)\mid f_{s_2}(Y)\mid\cdots\mid f_{s_r}(Y)]
\in\mathbb{R}^{p\times rd}.
$$

HDBSCAN is fitted to rows of $Z$. If it uses Euclidean distance, then the squared distance between objects $i$ and $j$ is

$$
\|Z_i-Z_j\|_2^2
=\sum_{t=1}^{r}\|f_{s_t}(Y)_i-f_{s_t}(Y)_j\|_2^2.
$$

This equation gives the most honest interpretation of concatenated distance: it aggregates coordinate separation across the declared seeded views. It is not automatically an unbiased estimate of expected biological proximity. Coordinate scale, dependence among runs, the embedding objective, and the number of blocks all affect it.

## A hand calculation

Suppose two two-dimensional embeddings give object-pair differences ((1,0)) and ((0,2)). The concatenated difference is ((1,0,0,2)), with distance

$$
\sqrt{1^2+0^2+0^2+2^2}=\sqrt{5}.
$$

The second view contributes four fifths of the squared distance. If its coordinates were scaled by two, it would contribute sixteen units instead. Concatenation therefore makes coordinate scaling part of the metric, even when every view was produced by the same algorithm.

UMAP coordinates are not naturally aligned across seeds. One run may rotate, reflect, or reorganize global regions relative to another. Euclidean distances *within* each coordinate block are invariant to rotations and reflections, so concatenated pairwise distances do not require the axes to have the same names. But other stochastic differences—local rearrangements, changed gaps, and scale—still matter.

## What repetition does not do

A cluster ensemble usually aggregates several partitions, often using voting, co-association, or another formal rule [@strehl2002ensembles]. Consensus clustering often uses resampling and a consensus matrix to examine stability [@monti2003consensus]. Freeze 3's fit path does neither. It concatenates representations before one HDBSCAN fit.

That distinction has practical consequences. The final labels do not tell us how often two objects were neighbors across seeds. They do not provide a per-object stability probability. They do not reveal whether one coordinate block dominates. A thousand blocks increase representation dimension and computation, but the count alone does not create a theorem of convergence to “true topology.”

## Seed schedules and provenance

For $r$ random states, legacy seed mode uses seeds 1 through $r$. Modern mode begins at a configured random state. The resolved configuration and run manifest preserve the schedule. Supplying seeds supports controlled local replay, but exact results can still depend on package versions, thread scheduling, floating-point behavior, architecture, and native libraries [@umap_reproducibility_docs; @collange2015numeric].

Stage 1 used one seed in the fixed fixture. It observed byte-identical labels during local reproduction under the recorded environment. That is useful regression evidence. It does not test the claimed benefit or cost of many repeated embeddings.

The historical 164-IDP analysis used 1,000 seeds according to the retained reconstruction. The fresh Freeze 3 refit of that analysis has not been run. Documentation must therefore say “historical selected configuration” or “retained labels,” not “freshly reproduced by 1,000-seed fitting.”

## How to evaluate a repeated-view strategy

A useful study separates at least four questions.

**Marginal seed variability.** Fit single-seed representations or partitions and measure pairwise neighborhood and partition agreement. This estimates how much one realization varies.

**Aggregation behavior.** Compare concatenations built from increasing numbers of seeds. Track whether distances, selected partitions, noise sets, and candidate rankings stabilize.

**Block influence.** Examine whether coordinate blocks have comparable dispersion and whether a small subset dominates concatenated distance. Any normalization should be prespecified because it changes the implemented method.

**External transport.** Repeat the entire construction on independent or meaningfully perturbed data. Agreement only among seeds of one dataset does not establish biological generalization.

The study should retain all seed schedules and candidate populations. Selecting the most stable-looking subset of seeds after inspecting results creates another layer of selection.

## Display coordinates and analytical coordinates

Freeze 3 retains the first embedding as visualization coordinates. The displayed scatterplot therefore shows $d$ coordinates, while HDBSCAN may have used $rd$. A pair that appears close in the display can be separated in later blocks, and vice versa. The plot is a view of the analysis, not a literal drawing of the full clustering space.

This is one reason original-space explanation matters. A cluster should be examined in the original association-profile coordinates and across sensitivity analyses rather than named from the position of one displayed island.

## Computational consequences

Repeated embeddings increase runtime and memory approximately with the number of views, though caching and library behavior affect exact scaling. The concatenated matrix grows from $p\times d$ to $p\times rd$. Standard mode declares 1,000 seeds, so a consequential full run needs explicit resource planning, thread control, environment capture, and a fresh output root. Edition 3 does not launch that run without user authorization.

## The decision created by this chapter

Repeated embeddings are defensible when described as an empirical representation strategy whose stability must be measured. They become misleading when the number of seeds is used as a substitute for sensitivity evidence. The next chapter asks how HDBSCAN converts this representation into a density hierarchy and why some observations remain unassigned.

**Evidence trail.** Claims UMA-002, UMA-004, SCI-164P, SLM-005 and SLM-016; coverage COV-006; gap G-004.

## Questions for the reader

1. If one of ten coordinate blocks has five times the scale of the others, what happens to concatenated Euclidean distance?
2. Distinguish representation concatenation, partition ensembles, and consensus clustering.
3. Name two results required before saying that increasing from 100 to 1,000 seeds improved robustness.

\newpage
