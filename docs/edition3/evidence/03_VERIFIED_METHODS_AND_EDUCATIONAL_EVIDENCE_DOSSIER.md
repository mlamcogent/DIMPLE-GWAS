# Verified methods and educational evidence dossier

## Reading rule

This dossier separates three questions: what the software does, what methodological literature supports, and what neither can establish. “Supported” below means appropriate context for a bounded claim; it never means that a citation validates the DIMPLE-GWAS biological results. Citation keys resolve in `06_VERIFIED_BIBLIOGRAPHY.bib`.

## 1. Linear and nonlinear dimension reduction

**Implementation truth.** Freeze 3 sends the fully prepared vectors-by-variant matrix directly to UMAP. It does not run PCA, ICA, SVD, or MDS first. Repeated UMAP embeddings are concatenated horizontally, not aligned or averaged. The first embedding supplies visualization coordinates.

**Evidence.** PCA identifies orthogonal directions ordered by explained variance [jolliffe2002pca]; ICA seeks statistically independent latent sources under stronger model assumptions [hyvarinen2000ica]. UMAP is a stochastic nonlinear neighborhood-graph embedding [mcinnes2018umap]. These methods answer different questions.

**Safe conclusion.** DIMPLE-GWAS offers a nonlinear topology-search representation complementary to linear decompositions. Nonlinearity does not imply biological superiority, causal recovery, or a truer latent mechanism. Comparator analyses are required for empirical performance claims.

## 2. UMAP and densMAP geometry

**Implementation truth.** The configuration exposes `n_neighbors`, `min_dist`, dimension, metric, spread, learning rate, repulsion, negative sampling, local connectivity, fuzzy-set mix ratio, seed, and `densmap`. Standard mode uses 30 neighbors, three components, Euclidean metric, zero minimum distance, and densMAP enabled.

**Evidence.** UMAP constructs a low-dimensional representation from a fuzzy neighborhood graph [mcinnes2018umap]. densMAP adds a density-correlation objective intended to preserve more information about local density [narayan2021densmap]. Official UMAP documentation states that UMAP is stochastic and that exact reproduction depends on fixed random state and execution conditions [umap_reproducibility_docs].

**Safe conclusion.** densMAP encourages—not guarantees—local density correspondence. Neither UMAP nor densMAP preserves all global distances, proves that displayed gaps are real classes, or makes a three-dimensional plot the ground truth.

## 3. HDBSCAN and density topology

**Implementation truth.** Freeze 3 uses the contributed `hdbscan` package, with `-1` as noise. It exposes minimum cluster size, minimum samples, epsilon, persistence, EOM/leaf selection, alpha, single-cluster permission, maximum cluster size, and metric. For a documented set of metrics it forces the generic algorithm. Under leaf selection the maximum-cluster-size parameter has no effective pruning role and is annotated.

**Evidence.** HDBSCAN builds a hierarchy of density-connected components and extracts stable clusters [campello2015hdbscan; mcinnes2017hdbscan]. The minimum cluster-size and minimum-samples parameters affect granularity and conservatism; “noise” is algorithmic non-membership under the fitted density model.

**Safe conclusion.** An HDBSCAN label is not a biological taxon. Noise is not automatically error, a non-pleiotropic phenotype, or an independent mechanism. It is appropriate to inspect noise, stability, and sensitivity separately.

## 4. Internal validation and DBCV

**Implementation truth.** Eligible topologies require at least two non-noise clusters. Freeze 3 reports silhouette, Calinski–Harabasz, Davies–Bouldin, optional DBCV, cluster persistence, trustworthiness, continuity, cluster sizes, and noise. Silhouette follows the configured HDBSCAN metric and a declared noise policy. Calinski–Harabasz and Davies–Bouldin are Euclidean and non-noise. DBCV uses the HDBSCAN validity implementation with the configured clustering metric.

**Evidence.** Silhouette summarizes within-versus-nearest-cluster separation [rousseeuw1987silhouette]; Calinski–Harabasz and Davies–Bouldin encode compactness/separation under their geometries [calinski1974; davies1979]; DBCV was designed for density-based cluster validation [moulavi2014dbcv].

**Safe conclusion.** These metrics are diagnostics with different geometries, not interchangeable truth scores. A high value does not establish biological validity, generalization, or a uniquely correct cluster count. DBCV is reported but is not part of the legacy DIMPLE score.

## 5. Ensemble stochastic geometry

**Implementation truth.** For `n_random_states = r`, Freeze 3 fits `r` UMAP embeddings and horizontally concatenates the coordinate blocks. Legacy seed mode uses seeds 1 through `r`; modern mode starts from the configured random state. There is no Procrustes alignment, consensus partition, co-association matrix, or bootstrap resampling in the fit path.

**Evidence.** Cluster-ensemble and consensus-clustering research formalizes aggregation of partitions or resamples [strehl2002ensembles; monti2003consensus]. UMAP’s own documentation treats seed sensitivity as something to examine, not something automatically removed by repetition [umap_reproducibility_docs].

**Safe conclusion.** Concatenation exposes HDBSCAN to several stochastic views; it does not “bypass randomness,” mathematically average geometry, or guarantee stable neighborhoods. A stability study would need explicit between-seed or resampling estimands.

## 6. Model selection and post-selection inference

**Implementation truth.** Search spaces are complete deterministic Cartesian products. Standard mode has 2,430 candidates; extended mode has 1,728. Ranking sorts by score, raw score, then stable model ID. Reported ties are deterministically ordered rather than assigned equal ranks. The legacy score is population-relative because normalization and weights depend on the evaluated candidate table.

**Evidence.** Repeated optimization of a noisy selection criterion can overfit the criterion and bias subsequent evaluation [cawley2010selection; varma2006bias]. Reusing selected data for inferential characterization can create circularity [kriegeskorte2009double]. Formal selective inference for hierarchical clustering requires machinery not implemented here [gao2024selective].

**Safe conclusion.** The top-ranked candidate is the winner under a declared search and score, not the globally or biologically optimal clustering. Post-selection association tables are descriptive unless evaluated with independent data or a valid selection-aware design.

## 7. Rank-based inverse normal transformation

**Implementation truth.** Optional RINT is applied column-wise before transposition with average ranks and quantiles `(rank - 0.5) / n`. Missing values are not imputed; all-missing columns and remaining missing/non-numeric values fail.

**Evidence.** RINT can improve some distributional properties but is not universally merited and can change interpretation [beasley2009rint].

**Safe conclusion.** RINT is an explicit sensitivity choice. It does not repair allele errors, unequal uncertainty, LD, ancestry structure, batch effects, or invalid harmonization.

## 8. High-dimensional distances and neighborhood instability

**Implementation truth.** UMAP operates on the full prepared variant dimension, and original-space explanation correlates vectors across those same dimensions. Trustworthiness and continuity use bounded deterministic sampling when configured; the effective neighbor count is capped at half the sample size.

**Evidence.** Distance contrast can degrade in high-dimensional spaces [aggarwal2001distance], and some observations may become hubs that occur unusually often in nearest-neighbor lists [radovanovic2010hubness]. Trustworthiness and continuity quantify retrieval-like neighborhood errors rather than biological correctness [venna2010trust].

**Safe conclusion.** Neighborhood metrics are useful diagnostics, but good values do not remove the need for perturbation, resampling, metric, and feature-set sensitivity analyses.

## 9. GWAS summary-statistic geometry

**Implementation truth.** The software treats numeric summary-statistic columns as coordinates after dropping a declared metadata prefix. It does not model per-entry standard errors, LD, sample overlap, allele alignment, ancestry, genomic control, or phenotype covariance. Those are upstream data-contract responsibilities.

**Evidence.** GWAS inflation can reflect both polygenicity and confounding [buliksullivan2015ldsc]. Cross-trait genetic correlation and sample overlap require explicit statistical treatment [buliksullivan2015rg]. Summary-statistic harmonization requires allele, frequency, sample-size, and quality checks [winkler2014qc]. UK Biobank IDP GWAS require extensive genetic and imaging confound control [elliott2018idp]. Cross-ancestry portability is not automatic [martin2019portability].

**Safe conclusion.** Geometric proximity of effect-size vectors is an exploratory similarity, not proof of shared causal variants, genetic correlation, or mechanism. Input comparability must be established before clustering.

## 10. Multivariate genetics comparators

**Implementation truth.** Freeze 3 is not Genomic SEM, MTAG, MOSTest, PLEIO, genomic PCA, or genomic ICA. It does not estimate their parameters or reproduce their hypothesis tests.

**Evidence.** Genomic SEM models a specified multivariate genetic covariance structure [grotzinger2019genomicsem]; MTAG estimates trait-specific associations while using cross-trait covariance [turley2018mtag]; MOSTest combines signals across correlated traits for locus discovery [vandermeer2020mostest]; PLEIO tests pleiotropic association under a statistical model [lee2021pleio]; other scalable approaches characterize pleiotropy across many traits [zhang2023pleiotropy]. Oblong et al. apply genomic PCA/ICA to 2,240 IDPs and assess reproducibility across releases [oblong2024components].

**Safe conclusion.** DIMPLE-GWAS is best positioned as a complementary exploratory topology method. It may suggest groupings for follow-up, but it does not replace confirmatory multivariate GWAS methods.

## 11. Procrustes and structural concordance

**Implementation truth.** `compare` aligns IDs, maps cluster labels using the Hungarian assignment, and reports ARI, NMI, variation of information, noise Jaccard, mapped membership, and changed noise status. Procrustes is reported only when compatible coordinate arrays with at least two dimensions exist.

**Evidence.** ARI corrects pairwise partition agreement for chance [hubert1985ari]; NMI and related information measures have multiple normalizations [vinh2010nmi]; variation of information is an information distance [meila2007vi]; Procrustes evaluates geometric agreement after admissible transformations [gower1975procrustes].

**Safe conclusion.** Permutation-invariant agreement can establish retained partition equivalence. It cannot establish biological validity or transportability. A small Procrustes disparity is coordinate concordance under the chosen transformation, not proof of identical manifold topology.

## 12. Reproducibility across systems

**Implementation truth.** Manifests record versions, operating system, architecture, seeds, thread settings, source digest, config digest, inputs, outputs, failures, and warnings. Fixed local seeds produced byte-identical labels in the fresh bounded run. There is no Git commit and no Stage 1 Docker/Linux/cloud run.

**Evidence.** Stochastic UMAP and parallel execution have reproducibility limits [umap_reproducibility_docs]. Floating-point reductions can vary with order and architecture [collange2015numeric].

**Safe conclusion.** A fixed seed plus a manifest supports bounded local reproducibility. Cross-platform equality must be measured, preferably with structural metrics and tolerances as well as hashes.

## 13. Scientific language and biological interpretation

**Implementation truth.** `explain` never refits or reranks. It computes original-space Pearson or Spearman similarity, cluster summaries, hierarchical within-block order, heatmaps, and optional descriptive associations with supplied coordinates. Exact ID matching is the default.

**Evidence.** Selection and re-description on the same dataset can be circular [kriegeskorte2009double]. Cluster validation literature addresses mathematical separation, not causal biology.

**Safe conclusion.** Use “clustered together under this pipeline,” “showed higher original-space similarity,” or “was assigned noise.” Avoid “same mechanism,” “true subtype,” “causal cluster,” “non-pleiotropic noise,” and “validated biology” unless supported by independent experimental or genetic evidence.

## 14. Educational design

**Implementation requirement.** Edition 3 should teach with a traceable progression: concept, bounded worked example, learner prediction, execution, artifact inspection, misconception check, and transfer exercise. It should expose defaults and limitations before results interpretation.

**Evidence.** Worked examples can help novices acquire structured skills [atkinson2000examples], while excessive guidance may lose effectiveness as expertise increases [kalyuga2003expertise]. Authentic assessment should resemble the knowledge, skills, context, and criteria of professional practice [gulikers2004authentic]. Active learning improves average STEM performance across many studies, though implementation varies [freeman2014active].

**Safe conclusion.** A runnable tutorial is pedagogically valuable only when learners inspect provenance, failure modes, and alternative explanations. Educational literature supports the design pattern, not the scientific truth of a tutorial result.

## Evidence gaps that constrain all domains

The 2,315- and 459-IDP raw matrices are absent; the 459 parameters conflict; the fresh 164-IDP 1,000-seed run is pending; one optional XLSX test is unexecuted; and cross-platform/container validation is absent. These constraints are carried into `12_UNRESOLVED_EVIDENCE_GAPS.md` and the Stage 1 gate.
