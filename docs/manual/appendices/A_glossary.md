# Appendix A — Glossary

## GWAS

**genome-wide association study.** A study that tests associations between genetic variants and a phenotype. Do not confuse a GWAS association with causation.

## summary statistic

**statistical result for one variant–phenotype test.** In the input matrix, an analysis value indexed by a variant row and vector column. The exact measure and harmonization must be documented upstream.

## vector / IDP

**one phenotype-associated column across variants.** The unit clustered after the input matrix is prepared and transposed. IDP is a domain-specific vector label, not a generic feature.

## feature_id

**stable retained vector identifier.** Identifier written with labels and used for exact matching. Whitespace and duplicates are validation concerns.

## RINT

**rank inverse normal transformation.** Optional rank-based normalization applied before transpose as implemented. Off by default; it changes the analysis values.

## UMAP

**Uniform Manifold Approximation and Projection.** Nonlinear neighborhood-based embedding used by the pipeline. Axes are not biological loadings.

## densMAP

**density-augmented UMAP.** UMAP mode adding a density-correlation objective. Density preservation is not biological validation.

## seed

**pseudorandom initializer.** Base or derived integer controlling a repeated embedding. A fixed seed does not ensure cross-platform bitwise equality.

## concatenated embedding

**horizontal concatenation of repeated embeddings.** The high-dimensional representation supplied to HDBSCAN. An empirical stability strategy, not a true-topology estimator.

## HDBSCAN

**hierarchical density-based spatial clustering of applications with noise.** Density-clustering backend used to label vectors. Freeze 3 uses the contributed hdbscan package.

## candidate model

**one UMAP-family and HDBSCAN-parameter combination.** A complete enumerated configuration that produces a retained success, invalid topology, or failure row. A candidate is not necessarily eligible for ranking.

## selected model

**rank-one retained eligible candidate.** The candidate named in best_model.json and the selection manifest. Selection is heuristic and conditional on the searched population.

## noise label -1

**HDBSCAN noise/unassigned status.** Algorithmic non-membership under one representation and parameterization. Not biological irrelevance or absence of pleiotropy.

## silhouette

**within-versus-nearest-cluster separation diagnostic.** Metric-aware internal partition score used by legacy_dimple. Geometry dependent; not biological validation.

## DBCV

**density-based clustering validation.** Optional density-aware diagnostic recorded by Freeze 3. Not a legacy_dimple score component.

## ARI

**adjusted Rand index.** Permutation-invariant pairwise partition concordance metric. Does not test biological validity.

## NMI

**normalized mutual information.** Permutation-invariant information overlap between partitions. Numeric label values need not match.

## Procrustes disparity

**shape discrepancy after alignment.** Coordinate-only comparison diagnostic when both artifacts supply coordinates. Separate from membership concordance.

## structural concordance

**agreement in partition structure.** Comparison of labels/noise sets invariant to label renaming. Not exact computational reproduction.

## biological validation

**external evidence that a grouping reflects meaningful biology.** A later evidence layer beyond software and internal metrics. Not established by passing tests or MNIST.

## provenance

**record of source, inputs, settings, environment, commands, and artifacts.** Evidence required to interpret and reproduce a run. A dependency list alone is insufficient.
