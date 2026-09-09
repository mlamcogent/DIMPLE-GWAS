# MNIST Benchmark Report

Date: 2026-07-22

This benchmark uses all 70,000 `mnist_784` samples. Digit labels were withheld from UMAP, HDBSCAN, the expanded grid, the legacy fit score, and winner selection. Labels were converted to integers only after the expanded-search winner was fixed, then used for the post-hoc metrics below.

The historical result supplied in the Freeze 2 macro (140 clusters, 51,676 noise samples, and 98.29% weighted purity among 18,324 clustered samples) is retained as a reported comparison row. Its exact original parameter manifest was not available. The `reported_pqtl_inspired` rerun therefore uses the auditable reference-branch defaults: EOM, `min_samples=3`, `min_cluster_size=10`, and restrictive `max_cluster_size=300` on the primary dev-style UMAP family. It is a representative rerun, not a claim of exact reconstruction.

## Results

| configuration | number_of_clusters | number_of_noise_points | noise_fraction | weighted_purity | adjusted_rand_index | normalized_mutual_information | homogeneity | completeness | v_measure | largest_cluster_size | runtime_seconds |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Jibin reported result (historical; not rerun row) | 140 | 51676 | 0.7382 | 0.9829 | NA | NA | NA | NA | NA | NA | NA |
| reported_pqtl_inspired | 1394 | 38057 | 0.5437 | 0.9720 | 0.0019 | 0.3250 | 0.4376 | 0.2585 | 0.3250 | 263 | 2.8251 |
| dev_compatible_baseline | 3281 | 21160 | 0.3023 | 0.9687 | 0.2193 | 0.4291 | 0.6837 | 0.3127 | 0.4291 | 7971 | 1.6195 |
| eom_restrictive_max | 440 | 48176 | 0.6882 | 0.9709 | 0.0018 | 0.2877 | 0.2966 | 0.2793 | 0.2877 | 257 | 0.9329 |
| leaf_unrestricted | 493 | 50443 | 0.7206 | 0.9700 | 0.0008 | 0.2665 | 0.2657 | 0.2673 | 0.2665 | 221 | 0.9157 |
| eom_unrestricted | 8 | 224 | 0.0032 | 0.6026 | 0.5436 | 0.7660 | 0.6622 | 0.9083 | 0.7660 | 21088 | 0.9128 |
| expanded_search_selected_by_legacy_dimple | 1541 | 40434 | 0.5776 | 0.9720 | 0.0016 | 0.3097 | 0.4060 | 0.2503 | 0.3097 | 93 | 1.1695 |

Weighted purity is calculated only among non-noise samples. ARI, NMI, homogeneity, completeness, and V-measure are calculated across all 70,000 samples with noise retained as label `-1`. Silhouette used for unsupervised scoring is a fixed-seed sample of 2,000 eligible points per candidate; the sample size and sampling flag are recorded in the expanded model table.

## Interpretation

Local purity asks whether each retained cluster is internally dominated by one digit. Global class recovery asks whether the complete ten-class partition is recovered, which is better reflected by ARI/NMI/V-measure. Fragmentation appears as many more than ten clusters. Noise rejection appears as the excluded fraction. Consequently, high weighted purity can coexist with weak global recovery, severe fragmentation, and high noise, as the historical result demonstrates.

The expanded-search winner is selected only by the declared `legacy_dimple` objective. It is not automatically the unique or biologically correct topology, and the benchmark labels do not alter its rank.

