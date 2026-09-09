# The scientific problem and the complete pipeline

Imagine that a research programme has estimated genetic association profiles for hundreds or thousands of imaging-derived phenotypes. Each phenotype now has a long vector of association statistics over a common set of variants. The immediate scientific question is not whether any single variant is associated with a phenotype; that work has already happened upstream. The new question is whether the *profiles* show repeatable structure. Do some phenotypes occupy similar regions of this high-dimensional association space? Are there dense groups, diffuse transitions, and observations that do not belong to any sufficiently persistent group?

DIMPLE-GWAS is an exploratory answer to that question. It prepares the profile matrix, creates several seeded UMAP or densMAP representations, concatenates their coordinates, fits HDBSCAN candidates, evaluates the resulting partitions, ranks eligible models, and preserves selected labels with enough provenance to reconstruct what happened. This sounds like a single algorithm. In practice it is a chain of scientific choices. Changing the input construction, transformation, distance metric, neighborhood scale, seed schedule, density parameters, candidate population, or score changes the object being selected.

![The DIMPLE-GWAS workflow and its evidence boundary. Upstream GWAS quality and downstream biological confirmation are connected to, but not performed by, the core pipeline.](assets/figures/pipeline_and_evidence_boundary.png){#fig-pipeline width=95%}

## What is being clustered?

The rows supplied to HDBSCAN ultimately represent phenotype-associated vectors or IDPs. They are not participants, variants, brain voxels, or individual GWAS records. If $p$ phenotype vectors are measured over $v$ aligned variant coordinates, the working matrix is

$$
Y = \begin{bmatrix}
\mathbf{y}_1^{\mathsf T}\\
\vdots\\
\mathbf{y}_p^{\mathsf T}
\end{bmatrix}\in\mathbb{R}^{p\times v},
$$

where row $\mathbf{y}_i$ is the association profile for phenotype $i$. The pipeline seeks a partition of these $p$ rows after nonlinear representation. A label therefore means “this phenotype vector was assigned to this density component under this declared construction.” It does not mean “these people form a subtype” or “these variants share one mechanism.”

That distinction is easy to state and surprisingly easy to lose. A cluster label is compact. The chain of assumptions that created it is not. Responsible reporting keeps the chain visible.

## A first end-to-end example

The fixed synthetic fixture contains 24 analysis vectors and 80 numeric variables after four metadata columns are removed. Its configuration fits one three-dimensional densMAP representation with seed 42 and then one HDBSCAN candidate. Stage 1 executed the complete route and observed three clusters, no noise, and selected model `model_060fac0208bb58e2`. Reproducing the retained model produced the same model identifier and a byte-identical label file. Comparison reported ARI and NMI of 1, noise-set Jaccard of 1, mapped membership fraction of 1, variation of information of 0, and Procrustes disparity of approximately $2.71\times10^{-31}$. Validation passed 24 of 24 artifact checks.

Those are strong software facts and weak scientific facts. The synthetic groups were deliberately clear, the search contained one candidate, and the run used one seed. The example shows that a reader can traverse the input, configuration, fit, retention, reproduction, comparison, and validation contracts. It does not show that real IDP structure is stable, that three is a privileged cluster count, or that the method outperforms an alternative.

This example also exposes an important property of the legacy score. With only one eligible candidate, table-relative component ranges collapse. The implementation uses a documented zero-range fallback and the candidate receives a final score of 1. The number does not mean perfect external validity; it means the candidate is the only eligible point in the table-relative scoring problem.

## Seven decisions hidden inside “run the pipeline”

First, the analyst decides what the profile coordinates mean. Effect estimates, $Z$-scores, signed statistics, or another aligned quantity create different geometries. Variant alignment, allele orientation, LD structure, study overlap, uncertainty, ancestry, and imaging confounds remain upstream responsibilities. DIMPLE-GWAS validates shape and numeric content; it cannot repair invalid summary statistics.

Second, the input contract separates metadata from analysis columns and transposes the matrix. Optional rank-based inverse normal transformation changes each analysis column before that transpose. No PCA, ICA, SVD, or MDS is silently inserted before UMAP.

Third, UMAP defines neighborhoods under the selected metric and constructs a stochastic low-dimensional representation. Standard mode currently uses three output components, Euclidean metric, zero minimum distance, and densMAP enabled. These are defaults, not universal scientific recommendations.

Fourth, repeated embeddings create several coordinate blocks. Freeze 3 concatenates them horizontally. It does not align them, average them, create a co-association matrix, or fit a formal consensus partition. The resulting distance aggregates separation over the declared coordinate blocks; its meaning depends on their construction and scale.

Fifth, HDBSCAN turns the concatenated representation into a density hierarchy and extracts clusters by EOM or leaf selection. Label `-1` is an unassigned result under that fit. It is neither a quality-control verdict nor a biological-null class.

Sixth, the pipeline evaluates and ranks a complete declared candidate population. Standard and extended search modes currently enumerate 2,430 and 1,728 candidates respectively; the fixed tutorial enumerates one. Metrics have different geometries and noise rules. The legacy score is table-relative and DBCV is supplementary rather than part of that score.

Seventh, selected outputs return the analyst to the evidence. Manifests, resolved configuration, candidate tables, failures, labels, original-space similarities, comparison metrics, and validation reports make different claims. Reading a plot before reading those artifacts reverses the intended order.

## The evidence ladder

The word *validated* is incomplete unless it names a level. Artifact validation asks whether files exist, parse, agree in row counts, and match hashes. Software regression asks whether tests and bounded fixtures behave as expected. Structural comparison asks whether two partitions agree after label permutation, whether their noise sets match, or whether compatible coordinates align. Statistical validation asks how conclusions change under seeds, parameters, metrics, features, or resampling. Biological validation asks whether an independently supported scientific interpretation survives. Cross-platform qualification asks whether the method behaves within declared tolerances across environments.

![Validation levels are cumulative questions. Passing a lower software layer does not confer a higher biological or platform claim.](assets/figures/validation_ladder.png){#fig-validation-ladder width=90%}

Stage 1 supplies strong local evidence at the lower levels. It does not complete the real-data stability, biological, Docker, Linux, or cloud layers. This is why the release boundary is not a ceremonial warning. It is a map of what the current results can bear.

## Why the next chapter starts with the matrix

Every downstream quantity inherits the scientific meaning and defects of the profile coordinates. Before learning UMAP or HDBSCAN, we therefore need to understand how a collection of GWAS-derived columns becomes a geometry among phenotype vectors—and why proximity in that geometry is an exploratory statement rather than a genetic mechanism.

**Evidence trail.** Stage 1 claims AUTH-001 to AUTH-003, QA-001 to QA-004, REL-001, SLM-001, SLM-010, SLM-018, SLM-022 and SLM-023; analysis levels 6-7 in `08_ANALYSIS_HIERARCHY_AND_GOLDEN_RUNS.md`.

## Questions for the reader

1. In one sentence, identify the unit clustered by DIMPLE-GWAS and two units it does not cluster.
2. Why can exact fixed-fixture agreement establish software evidence without establishing scientific validity?
3. A report says “the validate command proved the clusters are biologically valid.” Rewrite the statement so that it matches the command's actual scope.

\newpage
