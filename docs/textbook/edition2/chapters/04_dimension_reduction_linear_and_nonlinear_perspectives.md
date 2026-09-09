# 4. Dimension reduction: linear and nonlinear perspectives

*Guiding question:* **What is gained and lost when a high-dimensional relationship is represented with fewer coordinates?**

Prerequisites: 2–3.

## Why the question matters

A low-dimensional display can clarify neighborhoods while obscuring global scale, uncertainty, and coordinate identity.

Freeze 3 has no user-visible PCA, SVD, or ICA pre-reducer; comparator methods answer different questions and are not implemented stages.

This chapter develops the question in the order needed for a reader to move from statistical principle to current implementation, retained evidence, and a defensible statement. Its central worked task is: Project a centered three-variable toy matrix onto one stated linear direction, then contrast that operation with neighborhood preservation.

## Learning objectives

After completing Chapter 4, the reader can:

1. define high-dimensional concentration and explain its role without exceeding the stated caution;
2. define linear dimension reduction and explain its role without exceeding the stated caution;
3. define nearest-neighbor graph and explain its role without exceeding the stated caution;
4. define UMAP cross-entropy and explain its role without exceeding the stated caution;
5. trace the relevant package functions and generated artifacts;
6. complete the worked task and distinguish observation from interpretation.

## Conceptual and mathematical development

### high-dimensional concentration

Relative contrast among common distances can weaken as dimension grows. A compact notation is `contrast=(d_max-d_min)/d_min`. In practical terms, the phenomenon depends on distribution and norm; it is not a universal collapse theorem. [@aggarwal2001]

Within Freeze 3 RC1 the concept is connected to `run_repeated_umap` and is visible through `embedding.npy`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### linear dimension reduction

Projection onto directions satisfying a linear objective. A compact notation is `Z=XW`. In practical terms, pCA/ICA are comparators, not hidden Freeze 3 preprocessing. [@oblong2024]

Within Freeze 3 RC1 the concept is connected to `not implemented` and is visible through `none`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### nearest-neighbor graph

Local graph connecting points under an input-space metric. A compact notation is `N_k(i)`. In practical terms, neighbor identity depends on metric, scale, k, and ties. [@mcinnes2018umap]

Within Freeze 3 RC1 the concept is connected to `_fit_one (umap-learn delegate)` and is visible through `embedding_manifest.json`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### UMAP cross-entropy

Low-dimensional layout objective balancing represented and absent fuzzy edges. A compact notation is `C=sum_ij [w_ij log(w_ij/v_ij)+(1-w_ij)log((1-w_ij)/(1-v_ij))]`. In practical terms, optimization is stochastic and coordinates are non-identifiable up to layout symmetries. [@mcinnes2018umap]

Within Freeze 3 RC1 the concept is connected to `_fit_one` and is visible through `visualization_embedding.tsv`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

## Reconstructed operational foundation

Edition 1 contained the following verified operational material in separate short notes. Edition 2 consolidates it here and subjects it to the concept and evidence boundaries above.

### Evidence retained from former Chapter 6

### Operational foundation

UMAP is a nonlinear neighborhood-based embedding method; densMAP augments its objective to encourage correspondence in local density. DIMPLE-GWAS repeats seeded embeddings because one stochastic optimization can be sensitive to initialization. It concatenates the repeated coordinates so HDBSCAN receives information from all executed repeats. Density clustering is attractive because it can represent irregular clusters and explicitly leave low-density observations unassigned.

The rationale is empirical, not a mathematical guarantee. Concatenation does not prove that stochasticity has vanished, that Euclidean distances estimate an exact expectation, that ‘true topology’ has been recovered, or that a formal consensus partition has been computed. Base parameters, number and sequence of seeds, implementation versions, numerical libraries, hardware, threads, and the input matrix all remain part of the result.

### Retained evidence

Edition 2 Lab 1 uses one repeated seed for speed; Edition 2 Lab 2 uses two. The production standard declares 1,000. These are tutorial value, tutorial value, and configuration default—not interchangeable recommendations.

### Output-reading checkpoint

Inspect the resolved UMAP parameters, `random_seeds`, package versions, thread settings, projection-quality fields, and HDBSCAN metric in the manifest/candidate table.

### Misinterpretations to avoid

Do not interpret a clean 2D plot as proof that the concatenated representation is stable. Do not increase repeats without estimating compute and storage consequences. Do not call label `-1` a failed phenotype.

### Boundary inherited from Edition 1

Nonlinear embeddings can distort global distances, and density clustering is parameter dependent. Empirical stability should be assessed across justified perturbations and, for scientific conclusions, external or held-out evidence.


## Evidence and references

See McInnes et al. (2018), DOI 10.21105/joss.00861; Narayan et al. (2021), DOI 10.1038/s41587-020-00801-7; and Campello et al. (2015), DOI 10.1145/2733381.

### Evidence retained from former Chapter 7

### Operational foundation

Methods are comparable only after their questions and outputs are aligned. PCA provides orthogonal linear variance components and loadings; ICA seeks statistically independent linear components; k-means creates exhaustive centroid-based groups; hierarchical clustering supplies a nested grouping; mixture models provide probabilistic components. UMAP is a representation method, while HDBSCAN is the clustering stage. DBCV is a diagnostic, not a clustering algorithm.

Genomic SEM models multivariate genetic covariance, MTAG estimates trait-specific multi-trait associations, PLEIO provides joint pleiotropic-locus tests, and MOSTest is an omnibus multivariate association approach. These methods do not all accept the same inputs or return the same scientific object as DIMPLE-GWAS. They may be alternatives for a different question or complementary stages, but they are not implemented by Freeze 3.

No method is universally ‘completely ineffective.’ PCA/ICA components can be useful and reproducible without becoming automatically causal biological mechanisms.

### Retained evidence

Use `evidence/comparator_matrix.tsv` to select a method for three questions: reduce a matrix linearly, identify omnibus associated loci, and cluster phenotype vectors with an unassigned-noise option.

### Output-reading checkpoint

The comparator matrix records purpose, input, output, assumptions, noise handling, interpretability, strengths, limitations, relationship to DIMPLE-GWAS, and implementation status.

### Misinterpretations to avoid

Do not rank unlike methods with a single ‘best’ score. Do not imply that the manual executed a comparator marked `implemented_in_freeze3=no`. Correctly attribute the genomic PCA/ICA paper to Oblong et al., not to an inferred reviewer author.

### Boundary inherited from Edition 1

Conceptual comparisons do not establish empirical superiority. A fair benchmark would need common data, preregistered objectives, suitable metrics, and evidence for each implementation.


## Evidence and references

See Oblong et al. (2024), DOI 10.1111/gbb.12876; Grotzinger et al. (2019), DOI 10.1038/s41562-019-0566-x; MTAG DOI 10.1038/s41588-017-0009-4; MOSTest DOI 10.1038/s41467-020-17368-1; and PLEIO DOI 10.1016/j.ajhg.2020.11.017.

### Evidence retained from former Chapter 24

### Operational foundation

A loading in a linear component model has a defined relationship to an observed variable and component. A UMAP coordinate instead comes from a nonlinear, stochastic neighborhood-preservation optimization. Axis orientation, sign, rotation, scale, and even apparent global layout can vary without changing the underlying scientific identity of points. Freeze 3's display columns are therefore descriptive coordinates, not effects, loadings, mechanisms, or causal axes.

Concatenated repeated coordinates are the density-clustering representation. Selected `UMAP_1`–`UMAP_3` columns are visualization coordinates and must not be substituted for the full concatenated matrix. Correlating input dimensions with a display coordinate can be a descriptive diagnostic when explicitly enabled, but it does not turn the coordinate into a biological component.

### Retained evidence

The fresh Lab 1 display in Chapter 19 shows three separated synthetic groups. Its axis titles deliberately say ‘display coordinate,’ and its caption states that axes are not biological loadings.

### Output-reading checkpoint

Inspect display-coordinate columns, parameter/seed manifest, projection-quality table, optional coordinate-association table, and interpretation warnings.

### Misinterpretations to avoid

Do not name a coordinate ‘brain-size axis’ or infer direction of effect from its sign. Do not compare unaligned coordinates across runs. Do not equate a 2D picture with the HDBSCAN fit space.

### Boundary inherited from Edition 1

Coordinates can still be useful for visualization and diagnosing local structure, but claims should be invariant to arbitrary orientation and supported in original space or independent evidence.


## Evidence and references

See McInnes et al. (2018), DOI 10.21105/joss.00861.

## Implementation trace

**`metrics.effective_neighbor_count`** is defined at `dimple_gwas/metrics.py:9` with signature `n_samples: int, requested: int`. Implementation callable for effective neighbor count. It is reached from metrics.embedding_quality_metrics and connects to No package-defined dependency detected. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as tests/test_preprocessing_metrics.py::test_effective_neighbor_edge_cases. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`metrics.embedding_quality_metrics`** is defined at `dimple_gwas/metrics.py:15` with signature `original, embedding, requested_k: int, max_samples: int, seed: int`. Calculate bounded trustworthiness and continuity diagnostics for an embedding. It is reached from interpretation.run_explanation; pipeline.run_search and connects to metrics.effective_neighbor_count. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as tests/test_preprocessing_metrics.py::test_optimized_trustworthiness_and_continuity. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`metrics.evaluate_candidate`** is defined at `dimple_gwas/metrics.py:60` with signature `embedding, labels, clusterer, silhouette_metric: str, fit_include_noise: bool, compute_dbcv: bool, max_samples_silhouette: int=0, silhouette_seed: int=42`. Compute cluster counts, persistence, silhouette, CH, DB, optional DBCV, and validity status for one candidate. It is reached from pipeline._evaluate_one and connects to metrics._cluster_sizes. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`metrics.is_finite_number`** is defined at `dimple_gwas/metrics.py:165` with signature `value: Any`. Implementation callable for is finite number. It is reached from CLI/import/direct caller or no package caller detected and connects to No package-defined dependency detected. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`umap_runner.ensemble_seeds`** is defined at `dimple_gwas/umap_runner.py:32` with signature `parameters: Mapping[str, Any], repeats: int, legacy_sequence: bool`. Generate the exact repeated-embedding seed sequence under current or legacy scheduling. It is reached from umap_runner.run_repeated_umap and connects to No package-defined dependency detected. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`umap_runner.run_repeated_umap`** is defined at `dimple_gwas/umap_runner.py:39` with signature `matrix, parameters: Mapping[str, Any], repeats: int, n_jobs: int, legacy_sequence: bool`. Fit repeated UMAP/densMAP representations and concatenate their coordinates. It is reached from pipeline.run_search and connects to umap_runner._fit_one; umap_runner.ensemble_seeds. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is ValueError. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

## Claim adjudication notebook

The following statements are admitted to the draft only in their safe form:

- **PIPE-001 (verified):** The current production path passes the prepared matrix directly to UMAP and has no user-visible PCA/SVD/ICA pre-reducer. [@oblong2024] Limitation: UMAP internals do not constitute a documented preprocessing reducer. Implementation evidence: `pipeline.py; umap_runner.py`.

- **CMP-001 (reject):** K-means targets centroid-based partitions and may mismatch irregular density structure; it is not universally ineffective. Limitation: Performance depends on representation and objective. Implementation evidence: `not implemented`.

- **CMP-002 (reject):** Genomic PCA/ICA provide linear components; reproducible components do not by themselves establish mechanisms or a gold standard. [@oblong2024] Limitation: These tools answer different questions from DIMPLE-GWAS Stage 1. Implementation evidence: `not implemented`.

## Worked reasoning and evidence exercise

Project a centered three-variable toy matrix onto one stated linear direction, then contrast that operation with neighborhood preservation.

A complete Chapter 4 answer must expose its intermediate reasoning, name the source or output used for `Dimension reduction: linear and nonlinear perspectives`, and finish with separate support and non-support statements. Applying that discipline to the question “What is gained and lost when a high-dimensional relationship is represented with fewer coordinates?” prevents a calculation, a software observation, and a scientific interpretation from collapsing into one claim.

## Assumptions, diagnostics, and recovery

The Chapter 4 analysis assumes the stated unit and inputs, the recorded configuration and software identity, and a diagnostic that addresses the claimed property rather than a convenient surrogate. Its decisive boundary is: Freeze 3 has no user-visible PCA, SVD, or ICA pre-reducer; comparator methods answer different questions and are not implemented stages.

If the Chapter 4 route fails, retain its log and candidate status before deciding whether the cause is input, configuration, dependency, compute, identifier alignment, or output-root state. Correct an operational failure by writing a new result directory. Treat instability in `Dimension reduction: linear and nonlinear perspectives` as sensitivity evidence: report it and identify the independent evidence needed instead of relabeling ambiguity as a software exception.

## Chapter synthesis

A low-dimensional display can clarify neighborhoods while obscuring global scale, uncertainty, and coordinate identity. The implementation trace makes the current behavior auditable, but the evidence boundary remains part of the result. Chapter 5 introduces the density and validation problems that arise after representation.

## Exercises

1. For `Dimension reduction: linear and nonlinear perspectives`, name the unit of analysis and one plausible but invalid substitute.
2. Reconstruct the notation for high-dimensional concentration; define its dimensions or denominator and interpret every term.
3. Choose a Tier A function mapped to Chapter 4; identify its caller and direct output, then propose a topic-specific edge case.
4. Select one Chapter 4 artifact from the output atlas and state three integrity checks that must precede scientific reading.
5. Convert a tempting `Dimension reduction: linear and nonlinear perspectives` overclaim into one observed statement followed by its limitation.
6. Project a centered three-variable toy matrix onto one stated linear direction, then contrast that operation with neighborhood preservation.

Appendix J gives the Chapter 4 adjudication guide. Its further-reading keys supply statistical context; no external paper is treated as automatic validation of the current software or dataset.
