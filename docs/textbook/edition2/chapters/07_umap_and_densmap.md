# 7. UMAP and densMAP: from neighborhood graph to stochastic layout

## The question behind the embedding

After preprocessing, DIMPLE-GWAS represents each phenotype-associated vector as one point described by a very large number of variant-level values. The immediate difficulty is not simply that this matrix is wide. It is that no analyst can inspect thousands or millions of coordinates directly, and common distances may become hard to discriminate in high dimension. A useful representation must compress the matrix without pretending that compression is neutral.

This chapter asks a precise question: **what relationship does the DIMPLE-GWAS embedding try to preserve, how is that relationship encoded, and what uncertainty is introduced by the layout?** The answer matters because HDBSCAN operates on the resulting representation. An embedding is therefore not decoration added after clustering. It is part of the fitted analytical geometry.

By the end of the chapter, a reader should be able to:

1. explain how a metric and a neighbor count induce a local graph;
2. interpret UMAP's locally calibrated fuzzy memberships and low-dimensional cross-entropy objective;
3. distinguish ordinary UMAP from the density-regularized densMAP variant;
4. trace each configured parameter through DIMPLE-GWAS into `umap.UMAP`;
5. read the embedding-related output artifacts without assigning biological meaning to coordinate axes; and
6. diagnose parameter, scale, stochastic, and small-sample failure modes.

The prerequisites are the input orientation from Chapter 6 and the distance and scaling concepts from Chapter 3. Chapter 8 will use the present chapter's single-run representation as the building block for repeated seeded embeddings.

## From a matrix to a neighborhood question

Let (X\in\mathbb{R}^{p\times v}) denote the prepared DIMPLE-GWAS analysis matrix: (p) phenotype vectors in rows and (v) retained variant dimensions in columns. For two rows (x_i) and (x_j), a metric (d(x_i,x_j)) defines proximity. Under the default configuration this metric is Euclidean for UMAP, but the software accepts several alternatives after validation. Metric selection is substantive. Euclidean distance responds to absolute coordinate differences; cosine distance emphasizes direction; correlation distance removes location and scale in a different way. These choices can produce different neighbor sets even before optimization begins.

UMAP begins from local rather than global questions: Which points are among the nearest neighbors of (i)? At what distance does the local neighborhood around (i) become populated? How strongly should an edge from (i) to (j) be represented? The use of local neighborhoods is one response to the difficulty of global distance comparison in high dimensions, but it does not make the difficulty vanish. Neighbor sets still depend on the input scale, metric, sample size, ties, and approximate-neighbor implementation [@aggarwal2001; @mcinnes2018umap].

The configured `n_neighbors` controls the size of this local lens. A smaller value emphasizes very local relations and can fragment broad structure. A larger value asks the graph to carry information across a wider region and may smooth narrow structures. It is tempting to equate this setting with a biological scale, but DIMPLE-GWAS has no evidence for that interpretation. It is an analytical resolution parameter.

### A four-point distance example

Consider four hypothetical vectors after preprocessing, shown here in only two dimensions so that the arithmetic is visible:

| Vector | (x_1) | (x_2) |
| --- | ---: | ---: |
| A | 0 | 0 |
| B | 1 | 0 |
| C | 0 | 2 |
| D | 4 | 3 |

The Euclidean distance from A to B is (1), from A to C is (2), and from A to D is (5). If `n_neighbors=2`, A's visible neighbor set is therefore ({B,C}). For B, the distances to C and D are (sqrt{5}\approx2.236) and (sqrt{18}\approx4.243), so B's set is ({A,C}). The neighbor relation is directed at this stage: if a sample were more crowded, (j) could be among the nearest neighbors of (i) without the reverse being true.

Now rescale the second dimension by a factor of one tenth. The A–C distance becomes (0.2), while A–B remains (1). The closest ordering around A changes. Nothing about the labels A–D changed; only the coordinate scale did. This tiny calculation explains why Chapter 3 treats scaling and transformation as geometry-changing decisions rather than clerical preprocessing.

The real DIMPLE-GWAS matrix has many more dimensions, and `umap-learn` performs the neighbor search. DIMPLE-GWAS does not reimplement nearest-neighbor search or expose the graph as a standalone primary output. The graph construction described here is delegated library behavior, while the exact parameters passed to that behavior are directly auditable in `dimple_gwas.umap_runner._fit_one`.

## Local calibration: ρ and σ

Raw neighbor distances are not directly used as globally comparable edge weights. UMAP assigns each point (i) a local connectivity offset ($\rho_i$) and a scale ($\sigma_i$). In a commonly used pedagogical form, the directed membership strength from (i) to a neighbor (j) is

\[
w_{i\mid j}=\exp\left[-\frac{\max(0,d(x_i,x_j)-\rho_i)}{\sigma_i}\right].
\]

The offset ($\rho_i$) ensures a specified degree of local connectivity: at least the nearest relation can receive maximal strength rather than being attenuated merely because distances happen to be large in that region. The scale ($\sigma_i$) is chosen so that the effective membership mass matches the requested neighborhood scale. Consequently, the same raw distance can imply different membership strengths in a sparse and a crowded region.

This adaptive calibration is central to UMAP's local interpretation. It should not be paraphrased as “UMAP preserves all distances.” It deliberately replaces global raw distance with locally scaled fuzzy membership. The precise construction, treatment of ties, approximate search, and optimization details belong to the installed `umap-learn` implementation [@mcinnes2018umap]. The equation above is a faithful learning device, not code copied from DIMPLE-GWAS.

Directed memberships are then combined into an undirected fuzzy graph. For the usual fuzzy union, an edge can be written

\[
w_{ij}=w_{i\mid j}+w_{j\mid i}-w_{i\mid j}w_{j\mid i}.
\]

This is the probabilistic-sum form: an edge is strong when either direction supplies strong evidence, with the product preventing simple double counting. The `set_op_mix_ratio` parameter interpolates between union-like and intersection-like behavior in `umap-learn`. The default value passed by DIMPLE-GWAS is `1.0`, the union end of that interpolation. Lower values demand more reciprocal support and may disconnect marginal relations.

`local_connectivity`, also passed directly, controls the locally assumed connected neighborhood. Its default is `1.0`. The interaction between this value, duplicated observations, tied distances, and a small number of phenotype vectors deserves caution. When only a few vectors are available, a nominally modest `n_neighbors` may already involve a large fraction of the dataset. Parameters should therefore be interpreted relative to (p), not as context-free constants.

## Building a low-dimensional fuzzy graph

UMAP next constructs a membership model in an embedding with (q) components. Let (y_i\in\mathbb{R}^q) be the coordinate assigned to vector (i). A common description of low-dimensional membership is

\[
v_{ij}=\frac{1}{1+a\lVert y_i-y_j\rVert^{2b}},
\]

where (a) and (b) are selected to approximate a curve governed by `min_dist` and `spread`. Nearby embedded points have membership near one; membership decays with separation. The layout seeks agreement between the high-dimensional fuzzy graph (W=(w_{ij})) and low-dimensional graph (V=(v_{ij})).

One way to express the fuzzy cross-entropy is

\[
\mathcal{C}(W,V)=\sum_{i<j}\left[
w_{ij}\log\frac{w_{ij}}{v_{ij}} +
(1-w_{ij})\log\frac{1-w_{ij}}{1-v_{ij}}
\right].
\]

The first term penalizes representing a high-membership edge too weakly; it produces an attractive force for neighbors. The second penalizes placing absent or weak edges too close; it produces repulsion. Software minimizes a stochastic approximation to this objective rather than evaluating every non-edge on every step. Negative sampling, learning rate, initialization, epochs, and random state consequently influence the path to a layout [@mcinnes2018umap].

Cross-entropy does not give each pairwise distance equal status. It prioritizes agreement in fuzzy adjacency. A visually large separation between two clusters is therefore not a calibrated effect size. Nor does axis 1 name a stable biological direction: rotations, reflections, translations, local compromises, and different stochastic trajectories can produce visually different coordinates that encode similar neighborhoods.

### Optimization is a route, not just an answer

The distinction between an objective and its numerical optimization is important. Two fits may nominally minimize the same loss yet follow different sequences of sampled edges and negative examples. An attractive update moves the endpoints of a represented edge toward one another, while a repulsive update discourages arbitrary non-neighbors from occupying the same region. `negative_sample_rate` controls how many repulsive examples accompany an attractive example; `repulsion_strength` changes their influence; and `learning_rate` changes update size. These parameters affect the compromise that the optimizer reaches, not merely how quickly an identical endpoint is found.

The installed library also selects initialization and epoch-related behavior not named in `_fit_one`. Because Freeze 3 does not pass `init` or `n_epochs`, those choices follow the installed `umap-learn` defaults. This is why the environment manifest is part of the scientific record. “We used DIMPLE-GWAS 3.0.0rc1” is incomplete if the report omits the resolved configuration and dependency versions that determine delegated behavior.

An optimizer can reach a low-dimensional layout in which a local relation is well represented while a distant relation is visually distorted. That is not necessarily a software error: the graph objective weights relations unevenly, and compression forces compromises. Conversely, an appealing layout is not evidence that the objective preserved the neighborhoods most relevant to the scientific question. Diagnostics must be connected to the intended use.

### A membership calculation

Suppose A has two neighbors at distances 1 and 2, and use the simplified local values ($\rho_A=1$) and ($\sigma_A=1.5$). The directed strength to the nearest neighbor is

\[
w_{A\mid B}=\exp[-\max(0,1-1)/1.5]=1,
\]

whereas the strength to C is

\[
w_{A\mid C}=\exp[-(2-1)/1.5]\approx0.513.
\]

If the reverse strength (w_{C\mid A}) were (0.30), fuzzy union would give

\[
w_{AC}=0.513+0.30-(0.513)(0.30)\approx0.659.
\]

This example is intentionally not a manual reproduction of `umap-learn`: the library estimates local scales from the complete neighbor structure and has careful rules for connectivity and ties. The calculation isolates the logic that local calibration and symmetrization turn distance into edge strength. It also shows why reading a graph weight as a probability of shared biology would be a category error.

### `min_dist` and `spread`

`min_dist` controls how tightly points may be packed in the low-dimensional representation after their local relation is established. Smaller values permit compact groups; larger values keep nearby points more dispersed. DIMPLE-GWAS currently defaults to `0.0`, which permits tight local packing. That default can be useful for density separation, but it also makes the downstream density landscape conditional on a strong packing choice.

`spread` establishes the broader scale on which embedded distances decay and defaults to `1.0`. These two parameters interact through the curve used for low-dimensional membership. It is misleading to describe `min_dist` as a literal minimum Euclidean separation: it shapes the target curve rather than enforcing a hard constraint between every pair.

### Components and display coordinates

DIMPLE-GWAS defaults to `n_components=3`. A single fitted run therefore returns (p\times3) coordinates. The pipeline retains the first run as the visualization embedding, while Chapter 8 will show that the analytical embedding can concatenate multiple (p\times3) runs into (p\times(3S)). The first-run display coordinates are not a projection of the concatenated space and are not loadings from a linear model. They are a retained view for visualization.

Changing `n_components` changes both the capacity of each representation and, after concatenation, the dimensionality supplied to HDBSCAN. It can also change optimization behavior. A three-component default should therefore be reported as a verified software default, not a universal optimum.

## What densMAP adds

Ordinary UMAP focuses on neighborhood structure and may allocate display area in a way that does not reflect original local density. A dense input-space region and a diffuse region can receive visually similar area. densMAP augments the optimization with information about local radii, encouraging relative local density in the source data to be reflected in the embedding [@narayan2021densmap]. At a schematic level,

\[
\mathcal{L}_{\text{densMAP}}
=\mathcal{L}_{\text{UMAP}}+\lambda\,\mathcal{L}_{\text{density}}.
\]

The coefficient and library-specific construction create a trade-off: improving density agreement can make the neighborhood layout differ from ordinary UMAP. It is inaccurate to say that densMAP “preserves density exactly.” It regularizes toward a density relationship while still solving a stochastic, finite-sample optimization problem.

Freeze 3 RC1 passes `densmap=True` by default. This is a verified implementation fact from `_base_config` and `_fit_one`; it is not a general recommendation that every dataset use densMAP. The primary densMAP paper demonstrates the method in single-cell transcriptomic visualization. That paper supports the algorithmic background, not biological validation in GWAS-derived imaging vectors. DIMPLE-GWAS users must assess whether the induced geometry is stable and useful for their analysis rather than importing conclusions from a different domain.

One implementation nuance is especially important: DIMPLE-GWAS passes the boolean `densmap` option but does not currently expose every densMAP-specific tuning parameter in its configuration schema. The installed library therefore supplies its own defaults for parameters not named in `_fit_one`. The resolved environment and package versions are part of the method specification.

### Choosing between UMAP and densMAP as a sensitivity question

The boolean choice should be framed as a comparison of analytical objectives. With `densmap=false`, ask whether local-neighborhood representation supports a useful and stable clustering geometry. With `densmap=true`, ask how density regularization changes neighborhoods, cluster persistence, noise membership, diagnostic values, and the selected candidate. A fair comparison holds the input matrix, metric, seed schedule, and downstream candidate grid fixed. It reports both results rather than choosing the setting that best matches a desired label set.

If the two settings give different partitions, the discrepancy is information about method dependence. It is not automatically evidence that one setting failed. Investigate which vectors move, whether changes concentrate near cluster boundaries, whether original-space summaries differ, and whether conclusions survive independent data. If densMAP makes a visually sparse region occupy less area, the correct description is that the density-regularized layout changed the representation; the software has not estimated a biological abundance.

## The exact Freeze 3 RC1 call

The analytical route is deliberately thin. `run_repeated_umap` derives a seed list and calls the private helper `_fit_one` once per seed. `_fit_one` imports `umap.umap_` when available, constructs `umap.UMAP`, and passes these resolved values:

| Parameter | Freeze 3 standard default | Role in the delegated fit |
| --- | ---: | --- |
| `n_neighbors` | 30 | local neighborhood scale |
| `min_dist` | 0.0 | permitted local packing in the layout |
| `n_components` | 3 | coordinates per run |
| `metric` | `euclidean` | input-space neighbor distance |
| `spread` | 1.0 | broader embedded-distance scale |
| `learning_rate` | 1.0 | stochastic optimization step scale |
| `repulsion_strength` | 1.0 | strength of repulsive updates |
| `negative_sample_rate` | 5 | negative samples per positive update |
| `local_connectivity` | 1.0 | assumed local connectedness |
| `set_op_mix_ratio` | 1.0 | fuzzy union/intersection mix |
| `random_state` | seed supplied by the schedule | stochastic control per run |
| `densmap` | `true` | enable density-regularized UMAP |

The returned array is converted to `float32`. This reduces storage relative to 64-bit coordinates and fixes the representation passed onward, but it also means the pipeline does not promise infinite-precision preservation of library output. The seed records and environment manifest are needed to interpret repeatability.

A schematic call path is:

```text
prepared vectors × variants matrix
    → run_repeated_umap(matrix, umap_parameters, repeats, n_jobs, legacy_sequence)
        → ensemble_seeds(...)
        → _fit_one(matrix, umap_parameters, seed) for each seed
            → umap.UMAP(..., random_state=seed, densmap=...)
            → fit_transform(matrix)
        → concatenate all run coordinates for analysis
        → retain run 1 coordinates for display
```

This is a shape-changing path. If there are (p=164) vectors, (v) retained variants, (q=3) components, and (S=1000) repeats, each delegated fit returns (164\times3), while concatenation would produce (164\times3000). The example states dimensionality only; it is not evidence that the fresh 164-IDP run has been executed. That execution remains deferred until the Docker stage.

### Function dossier: `_fit_one`

| Field | Verified contract |
| --- | --- |
| Purpose | Fit one UMAP or densMAP representation for one seed. |
| Scientific role | Convert prepared phenotype-vector geometry to a low-dimensional local-graph representation. |
| Source | `dimple_gwas/umap_runner.py`. |
| Caller | `run_repeated_umap`. |
| Signature | `_fit_one(matrix, parameters, seed)`. |
| Arguments | Numeric two-dimensional matrix; resolved UMAP mapping; integer seed. |
| Defaults | No local defaults; all named values come from resolved configuration and seed schedule. |
| Accepted types | Array-like matrix accepted by `umap-learn`; mapping values coercible as shown in source; integer-coercible seed. |
| Input shape | (p\times v), phenotype vectors by retained variant dimensions. |
| Output | NumPy `float32` array with shape (p\times q). |
| Side effects | Imports and executes third-party UMAP; may use compiled numerical kernels and emit library warnings. |
| Files | Writes no files directly; the pipeline serializes returned arrays and manifests. |
| Exceptions | Dependency import errors and any validation/fitting error from `umap-learn` propagate to the caller. |
| Warnings | Library warnings are not transformed into scientific conclusions. |
| Deterministic controls | One explicit `random_state`; determinism remains conditional on environment and numerical execution. |
| Complexity | Dominated by delegated neighbor search and stochastic optimization; no universal exact bound is claimed for all metrics/backends. |
| Tests | Reached through pipeline and UMAP-runner tests; direct-name and integration status are recorded in the function atlas. |
| Executed evidence | Edition 1 fixed-synthetic output is retained; a fresh Edition 2 lab will supersede it for the final text. |
| Chapter and example | This chapter and Labs 1–2. |
| Limitations | No graph, fitted reducer, or densMAP radii are returned by this helper; coordinates are not biological loadings. |

This dossier shows why a private helper still matters pedagogically. It is the boundary where verified DIMPLE-GWAS configuration becomes delegated statistical behavior.

## Reading the embedding evidence

The embedding should be read together with its manifest rather than as a free-floating scatterplot. The relevant questions are:

1. How many phenotype vectors entered the fit, and in what order?
2. Which input checksum and preprocessing configuration produced the matrix?
3. Which UMAP parameters and library version were resolved?
4. Which seeds were fitted, and was the legacy sequence used?
5. How many components were produced per run?
6. Is a displayed coordinate file the first-run visualization or the concatenated analytical representation?
7. What warnings, runtime, sampling decisions, and downstream candidate failures occurred?

A plot can show neighborhood patterns, compact regions, isolated vectors, and algorithmic labels. It cannot, by itself, show that an axis is a genetic pathway, that a gap is statistically significant, or that a compact cluster is biologically homogeneous. Those conclusions require external evidence and an analysis design not supplied by the layout.

### A bounded executed example

Edition 2 Lab 1 freshly executed the fixed synthetic fixture in its isolated Python 3.12.13 environment. The configured route used `densmap=true`, `n_neighbors=10`, three components, and seed 42. It produced one successful candidate, `model_060fac0208bb58e2`, over a prepared matrix of 24 vectors by 80 variables. HDBSCAN retained three clusters of eight and assigned no vector to noise. The recorded trustworthiness was 0.8676, continuity was 0.8779, and DBCV was 0.9452; these are fixture-specific diagnostics, not general performance or biological claims. The full command took 12.22 seconds on the recorded macOS arm64 host, of which the UMAP stage recorded 9.97 seconds, and all publication-facing excerpts come from the lab's sanitized artifacts.

This bounded result establishes an executable chain from checksummed input through resolved parameters and software identity to retained numeric output. It does not establish scaling to 1,000 seeds or the original 164-IDP material, cross-platform equivalence, or external validity. The representative embedding later in the chapter therefore identifies the visible designed separation while its caption explicitly withholds pathway, significance, and biological-homogeneity interpretations.

## Diagnostics before trusting the representation

UMAP has no single diagnostic that certifies a correct embedding. DIMPLE-GWAS instead records evidence that addresses narrower questions.

**Trustworthiness** asks whether points shown as neighbors in the representation were also neighbors in the original prepared space. In one common form, unexpected embedded neighbors are penalized by their original-space rank:

\[
T(k)=1-\frac{2}{pk(2p-3k-1)}
\sum_{i=1}^{p}\sum_{j\in U_k(i)}(r_X(i,j)-k).
\]

Here (U_k(i)) is the set of points that enter the embedded (k)-neighborhood of (i) but not its original (k)-neighborhood, and (r_X(i,j)) is the original-space rank. Values nearer one indicate fewer such intrusions.

**Continuity** reverses the direction: it asks whether original neighbors remain neighbors after projection. Freeze 3 implements the pair pragmatically by calling scikit-learn's trustworthiness calculation in each direction. Both calls use Euclidean geometry, regardless of the configured UMAP metric, and may use a deterministic subsample when `max_samples_trust` is exceeded. These are implementation-specific facts. The metrics illuminate different neighborhood errors; neither validates HDBSCAN labels or biological meaning [@venna2010].

Useful sensitivity analysis changes one decision family at a time and asks whether conclusions are structurally stable. Examples include comparing `n_neighbors`, `min_dist`, `metric`, `densmap`, or seed families; examining neighborhood diagnostics; comparing downstream partitions with permutation-invariant metrics; and checking whether a conclusion depends on a few borderline vectors. Settings must not be chosen merely because they recreate a desired historical label set.

## Common failures and their meaning

**Too few samples for the neighbor request.** A neighborhood of 30 has a different meaning for 40 phenotype vectors than for 4,000. The library may constrain behavior, warn, or fail. Reduce the request for a toy example and label that setting tutorial-specific.

**Non-finite or nonnumeric input.** Production preprocessing coerces analysis cells to numeric and rejects missingness before UMAP. A failure here is a data-contract failure, not an embedding result.

**Unsupported or mismatched metric.** Configuration validation restricts metric names. Some HDBSCAN metrics trigger the generic backend, and the UMAP and HDBSCAN metrics need not be the same. Report both; do not write “Euclidean pipeline” from only one setting.

**Disconnected or unstable neighborhoods.** Extreme local settings, duplicates, or sparse data can produce unstable layouts. Inspect warnings and sensitivity across seeds and parameter families. A stable-looking first-run plot is insufficient because downstream clustering uses the analytical embedding.

**Overinterpretation of layout scale.** Distances and areas in a nonlinear plot are not automatically calibrated. densMAP changes the density objective but does not turn area into a biological measurement.

**Apparent deterministic replay that fails elsewhere.** An explicit seed controls a stochastic input, but numerical libraries, operation ordering, thread scheduling, and hardware can affect finite-precision results. Exact equality is a local acceptance criterion only where the evidence supports it; elsewhere use named structural metrics and tolerances [@reproduciblesum2015].

**Attributing downstream clusters to UMAP alone.** The final partition reflects preprocessing, per-run UMAP parameters, seed schedule, concatenation, HDBSCAN parameters, candidate diagnostics, scoring, and selection. A causal statement about one stage requires a designed intervention, not inspection of a final plot.

## Why Chapter 8 follows

A single run exposes the stochastic and non-identifiable nature of nonlinear layout. DIMPLE-GWAS responds by fitting multiple seeded representations and horizontally concatenating them. This creates a new geometry whose squared Euclidean distance equals the sum of within-run squared distances. That identity is useful, but it also makes scale and alignment questions unavoidable. Chapter 8 derives the identity, verifies the exact seed schedules, and explains why concatenation is an empirical aggregate rather than formal consensus clustering.

## Summary

UMAP converts high-dimensional vector relationships into a fuzzy neighborhood graph and optimizes a low-dimensional graph to resemble it. densMAP adds a density-oriented regularization objective. DIMPLE-GWAS delegates both algorithms to `umap-learn`, but it controls and records the parameters, seeds, array precision, repetition, and downstream use. The representation is analytical infrastructure: important, inspectable, stochastic, and conditional. Its coordinates are not biological axes, and its plot is not validation.

## Exercises

1. Recalculate the four-point example after multiplying the first dimension by three. Which two neighbors does A retain, and what does the change imply about scaling?
2. Explain in words why fuzzy union can retain an edge that is strong in only one direction. Under what sampling pattern might that be useful or risky?
3. Compare the roles of `n_neighbors`, `min_dist`, and `local_connectivity`. Identify one interaction that cannot be understood by varying only a single setting.
4. A colleague writes, “densMAP preserves the true density of the phenotype landscape.” Rewrite the sentence so it is algorithmically and scientifically defensible.
5. Inspect `_fit_one` and the resolved standard configuration. Construct a parameter-to-source table and identify which densMAP-specific choices remain library defaults.
6. Suppose two seeded layouts differ only by rotation. What happens to within-run Euclidean distances? What happens after raw coordinate concatenation if another run differs by a scale factor of two?
7. Design a sensitivity analysis that separates seed sensitivity from metric sensitivity without selecting the result closest to a desired partition.
8. Read a retained embedding manifest and list the minimum evidence needed before its scatterplot can be used in a methods report.

Further reading begins with the UMAP software paper and algorithm description [@mcinnes2018umap], the densMAP primary paper [@narayan2021densmap], neighborhood-preservation work [@venna2010], and the high-dimensional distance analysis that motivates caution about geometry [@aggarwal2001].
