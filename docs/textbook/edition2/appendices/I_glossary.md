# Appendix I — Glossary

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

## GWAS-derived vector

**effect estimates or association statistics for one phenotype across matched variants.** A vector is a statistical summary, not a person or causal mechanism.

## identifier alignment

**a one-to-one correspondence between vector or feature identifiers across artifacts.** Order is not identity; normalize and validate keys before joining.

## distance and similarity

**geometry chosen to compare vectors or embedded points.** The metric defines which differences count as close.

## scaling and transformation

**changes to marginal scale before geometric analysis.** Transformation changes geometry; it does not create independent evidence.

## RINT ties and missingness

**average ranks with missing values retained during ranking.** Freeze 3 rejects missing analysis cells before the pipeline and applies RINT column-wise before transpose.

## high-dimensional concentration

**relative contrast among common distances can weaken as dimension grows.** The phenomenon depends on distribution and norm; it is not a universal collapse theorem.

## linear dimension reduction

**projection onto directions satisfying a linear objective.** PCA/ICA are comparators, not hidden Freeze 3 preprocessing.

## nearest-neighbor graph

**local graph connecting points under an input-space metric.** Neighbor identity depends on metric, scale, k, and ties.

## UMAP fuzzy membership

**locally calibrated edge strength in a fuzzy graph.** This is an educational form of delegated UMAP behavior, not reimplemented code.

## UMAP cross-entropy

**low-dimensional layout objective balancing represented and absent fuzzy edges.** Optimization is stochastic and coordinates are non-identifiable up to layout symmetries.

## densMAP regularization

**additional objective encouraging agreement of local density radii.** Density preservation trades against the base layout objective and does not make density biologically true.

## seed schedule

**deterministic list controlling repeated stochastic fits.** Recorded seeds permit replay but do not guarantee cross-platform bitwise identity.

## concatenated geometry

**horizontal concatenation of S embeddings with q components.** Squared Euclidean distances add across runs, so unaligned rotations/scales influence the aggregate.

## core distance

**distance from a point to its min_samples-th neighbor.** Larger min_samples changes the density scale and may increase unassigned points.

## mutual reachability

**density-aware dissimilarity used by HDBSCAN.** It smooths single-linkage effects without removing parameter dependence.

## HDBSCAN stability

**persistence of a cluster through the density hierarchy.** The library computes the hierarchy; Freeze 3 records persistence summaries.

## noise label

**label -1 for points unassigned under a fitted density model.** Noise is algorithmic and parameter-conditional, never a biological-null statement.

## Cartesian search

**product of enumerated parameter families.** The standard grid is 45 x 18 x 3 = 2,430 for one UMAP family.

## candidate identity

**deterministic hash and ordinal for a resolved parameter combination.** Identity supports replay; it is not a quality score.

## Calinski-Harabasz

**between-cluster to within-cluster dispersion ratio.** The implementation uses non-noise embedded points and Euclidean centroid geometry.

## Davies-Bouldin

**average worst within/between centroid scatter ratio.** Lower is better; Euclidean centroid assumptions can mismatch density geometry.

## trustworthiness and continuity

**directed neighborhood-retention diagnostics.** Freeze 3 computes both through directed calls to sklearn trustworthiness under Euclidean geometry.

## legacy_dimple score

**population-relative weighted combination of normalized silhouette, clusters, and optionally noise.** Weights are raw dynamic ranges divided by their sum; final scores are min-max scaled.

## eligibility and ties

**rules deciding which candidates receive scores and stable rank order.** Ties resolve deterministically through configured sort keys and candidate identity.

## adjusted Rand index

**chance-adjusted pairwise partition agreement.** Permutation invariant; a value of 1 does not imply coordinate identity.

## normalized mutual information

**normalized information shared by two labelings.** Normalization conventions matter; Freeze 3 uses the sklearn convention recorded in code.

## noise Jaccard

**overlap of the two sets labeled -1.** It isolates agreement about unassigned membership, not all clusters.

## Pearson association

**linear association in original input dimensions.** Post-selection descriptive only; undefined constant vectors follow configured policy.

## Spearman association

**Pearson correlation of marginal ranks.** Ties receive average ranks; monotonic association is not mechanism.

## circular analysis

**reuse of discovery data for apparently confirmatory inference.** Same-data heatmaps and correlations are descriptive; independent or selective-inference designs are needed for confirmatory claims.

## validation ladder

**separate software, technical, structural, statistical, biological, external, and cross-platform evidence.** Passing tests or exact fixture replay cannot substitute for external biological validation.

## floating-point reproducibility

**dependence of finite-precision results on operation order and platform.** Pinned dependencies improve control but do not guarantee universal bitwise equality.
