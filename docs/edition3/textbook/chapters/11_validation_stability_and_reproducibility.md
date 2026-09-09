# Validation, stability, and reproducibility

Two runs can be “the same” in several incompatible senses. Their files may have the same hashes. Their numeric label codes may differ while the partition is identical. Their partitions may differ slightly but preserve the same broad structure. They may agree on one computer and diverge across architectures. And even perfect computational agreement says nothing by itself about biological truth.

## Artifact integrity

The `validate` command checks required artifact presence, readability, schemas, row counts, identifiers, selected-model links, and recorded hashes. A complete run should have internally reconcilable resolved configuration, search manifests, model tables, selected artifacts, and run manifest.

This is necessary evidence. It detects truncation, substitution, stale labels, broken joins, and missing files. It does not test whether the chosen representation or partition is scientifically appropriate. The command name should be read as *artifact validation*.

Stage 1 ran this route on the fixed synthetic result and passed 24 of 24 checks with no failures or warnings.

## Exact local reproduction

`reproduce-model` takes a retained model summary and refits one recorded model into a fresh output root. Under the Stage 1 environment, the fixed model reproduced the same model identifier and a byte-identical label file. This is exact local regression evidence for one fixture.

A fixed seed is important but not sufficient for universal bitwise reproducibility. UMAP's stochastic optimization, multithreading, BLAS/OpenMP reductions, native code, compiler choices, dependency versions, and architecture can change floating-point order or neighbor search [@umap_reproducibility_docs; @collange2015numeric]. A container controls much of the environment but does not guarantee identical arithmetic across every processor.

## Labels must be compared without trusting their names

Cluster labels are arbitrary symbols. A partition $(0,0,1,1)$ is structurally identical to $(7,7,3,3)$. Freeze 3 aligns exact identifier sets and uses permutation-invariant metrics and a Hungarian mapping rather than requiring equal numeric codes.

The adjusted Rand index counts pairwise agreements and corrects for chance [@hubert1985ari]. If $a$ counts pairs placed together in both partitions, $b$ pairs together only in the first, $c$ together only in the second, and $d$ separated in both, the unadjusted Rand logic uses $(a+d)/(a+b+c+d)$; ARI adjusts the expected value under a random-partition model.

Normalized mutual information expresses shared information between partitions under a stated normalization [@vinh2010nmi]. Variation of information,

$$
VI(U,V)=H(U)+H(V)-2I(U;V),
$$

is an information distance and equals zero for identical partitions [@meila2007vi]. Noise-set Jaccard compares which identifiers are `-1`. Mapped membership fraction reports agreement after label alignment.

Stage 1 observed ARI, NMI, noise-set Jaccard, and mapped membership fraction of 1 and variation of information 0 for the fixed original and reproduction.

## Coordinate comparison is conditional

When compatible coordinates with at least two dimensions exist, Procrustes analysis centers, scales, and rotates/reflection-aligns one configuration to another, then measures residual disparity [@gower1975procrustes]. A near-zero disparity establishes coordinate concordance under the allowed transformation. It does not establish identical manifold topology or biological validity.

Stage 1's fixed comparison reported disparity approximately $2.71\times10^{-31}$. The historical 164 artifact has one missing third coordinate for `IDP_2143`; two complete coordinates can support bounded retained diagnostics, but the missing value must not be silently imputed.

## Stability asks a different question

Reproduction holds the recorded conditions fixed. Stability deliberately perturbs conditions that are scientifically plausible. Useful perturbations include seeds, neighbor counts, metrics, densMAP state, RINT, feature sets, HDBSCAN parameters, and resampled or independent data.

A stability report should not collapse all perturbations into one average. Seed variation probes optimization dependence. Parameter variation probes specification dependence. Feature and metric variation probe the original geometry. Resampling probes data dependence. Independent cohorts probe transportability. Each has a different interpretation.

Stage 1 did not complete a real-data stability study. The retained historical 164 labels and score table cannot substitute for it.

## Exact, structural, and scientific equivalence

It is useful to state conclusions in a three-level form:

- **Exact equivalence:** specified files or arrays are byte-for-byte identical under a recorded environment.
- **Structural equivalence:** partitions, noise sets, neighborhoods, or coordinates agree within declared metrics and tolerances.
- **Scientific equivalence:** the substantive interpretation and downstream conclusion are supported under relevant data and design changes.

The first can fail while the second holds because of harmless floating-point differences or label permutation. The second can hold while the third fails because the same unstable or biased structure was reproduced perfectly.

## Cross-platform qualification

A cross-platform plan should run the same immutable fixture and configuration on each target, retain full manifests, compare artifact schemas, and define tolerances before looking at results. Hash equality is useful where expected. Structural metrics are needed where floating-point paths may differ. Runtime differences should be reported without mixing hardware performance with scientific output quality.

No Stage 1 Docker, Linux, x86-64, GCP, or AWS run exists. The present label is therefore local macOS arm64 evidence, not platform independence.

## The decision created by this chapter

Name the equivalence being claimed, use metrics that respect label symmetry, keep artifact integrity separate from biology, and design perturbations around specific uncertainty sources. The next chapter returns to the original summary-statistic matrix to ask what a selected partition looks like before nonlinear representation.

**Evidence trail.** Claims CMP-001, CMP-002, VAL-001, QA-003, SLM-016 to SLM-019; coverage COV-019 to COV-021; gaps G-006, G-012 and G-013.

## Questions for the reader

1. Why are $(0,0,1,1)$ and $(5,5,2,2)$ the same partition?
2. Give one example each of exact, structural, and scientific equivalence.
3. Design a platform comparison in which hash inequality is allowed but structural disagreement is not.

\newpage
