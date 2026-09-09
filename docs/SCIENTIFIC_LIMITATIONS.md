# Scientific Limitations

1. UMAP is stochastic. Fixed seeds improve reproduction but do not make an embedding a unique representation of the data.
2. HDBSCAN topology depends on distance geometry, density parameters, selection method, and maximum-size constraints. Different defensible settings can yield materially different partitions.
3. Repeated UMAP concatenation assesses multiple stochastic embeddings but is not a formal consensus-clustering guarantee.
4. Internal validation has no biological ground truth. Silhouette favors separated geometry and may disfavor valid non-convex density clusters. Calinski-Harabasz and Davies-Bouldin are Euclidean diagnostics even when HDBSCAN uses another metric.
5. DBCV can fail or be expensive for some metric/data combinations. Freeze 3 reports unavailability and never substitutes another number under the DBCV name.
6. Trustworthiness and continuity are embedding-level diagnostics, not cluster-validity scores. Bounded subsampling makes them scalable but introduces sampling variation.
7. The legacy score mixes native-unit dynamic ranges. A large cluster-count range can overwhelm silhouette, as observed in the 70,000-sample MNIST benchmark. It is retained for compatibility, not asserted as universally optimal.
8. Maximizing cluster count can reward fragmentation. Minimizing noise can reward broad heterogeneous clusters. Restrictive maximum size can manufacture fine granularity. These are objectives/trade-offs, not biological truths.
9. High local purity can coexist with fragmentation and high noise. On MNIST, several ~97% purity solutions had hundreds to thousands of clusters and near-zero all-sample ARI.
10. Pareto membership exposes non-dominated trade-offs; it does not identify one correct model.
11. Search breadth creates multiple-comparison and selection-instability concerns. Repeated data perturbation, external cohorts, and domain-specific validation remain necessary.
12. Annotation metadata are intentionally excluded from fitting. This protects agnostic discovery but means biological plausibility is assessed only after model selection.
13. Within-cluster Pearson/Spearman similarity describes concordance in the supplied original-space vectors. It is not a stability test, replication result, or causal interpretation.
14. Heatmap row/column ordering and deterministic downsampling are presentation choices. They do not alter membership, but they can affect visual emphasis.
15. Cluster summaries are conditional on the selected labels. Post hoc descriptions must not be read as evidence that the same annotations selected the topology.
16. The historical original-IDP workbooks contain only partial reconstruction evidence for some analyses. The complete 164-IDP input and labels are available; the 2,315- and 459-IDP raw matrices are not locally recoverable, and one 164-IDP visualization coordinate is missing in the source workbook.

No default cluster count, noise ceiling, largest-cluster limit, dataset type, visual attractiveness criterion, or MNIST label influences selection. Users remain responsible for external validation, sensitivity analysis, and biological interpretation.
