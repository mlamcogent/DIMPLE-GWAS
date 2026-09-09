# DIMPLE-GWAS in multivariate statistical genetics

DIMPLE-GWAS explores topology among phenotype-associated summary-statistic vectors. Its distinctive contribution is not a new association test or covariance model. It is a workflow for representing many profiles nonlinearly, exploring density structure, retaining unassigned observations, ranking declared candidates, and preserving enough evidence to interrogate the result.

This positions the method alongside, rather than above, a family of multivariate genetic approaches.

## Continuous axes and exploratory groups

Genomic PCA summarizes correlated genetic patterns through orthogonal variance directions. Genomic ICA seeks statistically independent sources. These approaches can reveal broad continuous structure and supply loadings or mixing patterns for interpretation. DIMPLE-GWAS instead asks whether a nonlinear representation contains persistent density components. A dataset can contain both: continuous axes with locally dense regions or hierarchical groups.

The appropriate comparison reports both kinds of structure. If DIMPLE clusters merely discretize one principal gradient, that is scientifically different from clusters capturing irregular relationships not summarized by a few linear axes. The comparison must be performed on matched, harmonized inputs and evaluated beyond visual impression.

## Covariance modelling and multivariate association

Genomic SEM specifies and estimates models of genetic covariance [@grotzinger2019genomicsem]. MTAG uses cross-trait covariance to improve trait-specific association estimates under its assumptions [@turley2018mtag]. MOSTest and PLEIO combine multivariate association evidence for locus discovery [@vandermeer2020mostest; @lee2021pleio]. These methods can answer confirmatory or discovery questions that DIMPLE-GWAS does not implement.

DIMPLE output could help generate hypotheses about sets of phenotypes for later covariance modelling or association testing. That downstream use should account for selection and avoid presenting data-derived groups as prespecified. Conversely, covariance-model results could provide external structure against which exploratory DIMPLE groupings are compared.

## What a fair benchmark would require

A fair benchmark begins with a shared target. Possible targets include recovery of simulated continuous factors, detection of simulated nonlinear groups, stability under sample or summary-statistic perturbation, prediction or replication in an independent release, interpretability under known annotations, or computational cost at fixed scale.

The benchmark should then hold input harmonization, phenotype population, feature set, tuning budget, and evaluation data constant where the methods permit. It should report failure modes and sensitivity, not only the best result. It should avoid using DIMPLE's own internal score as the sole outcome when comparing DIMPLE with a method that optimizes a different objective.

No such comprehensive current benchmark exists in the Stage 1 pack. Any statement of superiority, equivalence, or replacement would therefore exceed the evidence.

## Appropriate use cases

DIMPLE-GWAS is most defensible when the analyst has a well-harmonized collection of comparable phenotype-associated vectors; wants exploratory topology rather than a prespecified factor model or association test; can afford declared sensitivity analyses; will inspect original-space structure and noise; and can keep downstream interpretation descriptive until independent evidence arrives.

It is a poor fit when coordinates are incomparable or badly harmonized, uncertainty must be modelled explicitly but is ignored, the scientific target is a formal multivariate association test, a fixed cluster count is required by design, compute limits preclude even basic sensitivity work, or the analyst intends to treat UMAP axes and cluster labels as mechanisms.

## Research priorities

The strongest next methodological work is not another rhetorical defense of nonlinearity. It is empirical.

1. Complete the fresh 164-IDP refit in a controlled environment and compare exact, structural and scientific equivalence.
2. Run prespecified real-data seed, metric, transformation, feature and hyperparameter stability studies.
3. Compare single views, increasing concatenation sizes, and formal ensemble or consensus alternatives.
4. Benchmark linear, nonlinear, covariance-model and multivariate-association methods under matched targets.
5. Develop selection-aware or independent validation routes for biological characterization.
6. Qualify Docker, Linux, architectures and cloud environments with declared tolerances.
7. Preserve raw matrices, signed or tagged source identity, and immutable execution manifests.

## A defensible final method statement

DIMPLE-GWAS Freeze 3 RC1 implements a source-audited local pipeline for exploring density topology among aligned phenotype-associated summary-statistic vectors. It applies declared preprocessing, repeated seeded UMAP or densMAP embeddings, coordinate concatenation, contributed HDBSCAN candidate fitting, transparent scoring and ranking, artifact retention, original-space description, structural comparison, and integrity validation. Under the recorded Stage 1 macOS arm64 environment, the test suite and bounded synthetic workflow were internally consistent, and retained historical score calculations were reconstructed exactly. The current evidence does not establish manuscript-scale fresh reproduction, real-data stability, independent biological validity, universal method superiority, or cross-platform identity.

That statement is deliberately less exciting than “discovering the true genetic architecture.” It is also more useful. It tells readers what was built, what was observed, and which work can genuinely strengthen the scientific claim.

## Closing perspective

Exploratory topology methods are most valuable when they make uncertainty visible. Noise, parameter sensitivity, disagreement among representations, and manual historical choices are not blemishes to be edited away. They are information about the limits of the map.

The analyst's task is therefore dual: construct a representation that makes a scientifically motivated form of structure inspectable, and preserve enough evidence to know when that structure is contingent. The workbook now turns that responsibility into a reproducible sequence of actions. The technical reference then supplies the exact contracts needed when a concept becomes a command, a function, or a file.

**Evidence trail.** Claims SLM-001, SLM-002, REL-001 and BIO-001; dossier domain 10; gap G-010; comparator sources [@oblong2024components; @grotzinger2019genomicsem; @turley2018mtag; @vandermeer2020mostest; @lee2021pleio].

## Questions for the reader

1. Write a one-sentence use case in which DIMPLE-GWAS and genomic PCA are complementary.
2. Define a matched benchmark target that would make a nonlinear-versus-linear comparison meaningful.
3. Which clause in the final method statement would change after a successful cross-platform qualification, and which would remain scientifically unresolved?

\newpage
