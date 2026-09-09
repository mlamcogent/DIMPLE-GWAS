# Analysis hierarchy and golden runs

## Purpose

This record prevents results from different sample spaces, artifacts, and validation roles from being merged. Counts are interpreted only inside their own row.

| Level | Analysis or artifact | Input/size | Result retained or reported | Parameter identity | Stage 1 evidential status |
|---|---|---|---|---|---|
| 1 | Primary manuscript analysis | 2,315 IDPs | 15 clusters; 153 noise | Reported epsilon 0, min_samples 4, min_cluster_size 41 | Primary reported result. Full 2,430-row model table is retained and rescored; raw matrix is absent, so no fresh fit. |
| 2 | Secondary dMRI/white-matter analysis | 459 IDPs | 6 clusters; 16 noise; cluster sizes 24, 41, 31, 44, 272, 31 | Conflicting notebook/manuscript records; one report describes epsilon 2, min_samples 2, min_cluster_size 23 | Reported result with unresolved parameter conflict. Raw matrix and model table are absent. No reproduction YAML may be issued. |
| 3 | Secondary resting-state analysis | 164 IDPs | 5 clusters; 102 noise (62.19%); non-noise sizes 9, 13, 15, 14, 11 | epsilon 0; min_samples 4; min_cluster_size 6; EOM; densMAP; 1,000 seeds; noise included in historical score | Exact historical input and retained labels/model table exist. The selected row is manual sorted row 16, not score rank 1. |
| 4 | Freeze 3 historical-164 adapter/explanation | 164/164 exact ID match | Same memberships and noise as Level 3; original-space explanation artifacts | Reads retained labels and input; no refit | Exact schema adaptation and descriptive explanation. It must not be called a fresh clustering reproduction. |
| 5 | 356-row validation workbook | 356 labels | Separate validation output | Distinct source/workbook | Separate artifact. It is not a 164-IDP result and must not be combined with Level 3. |
| 6 | Freeze 2 versus Freeze 3 fixed regression | fixed one-seed test fixture | Same model ID; byte-identical labels; ARI/NMI/noise Jaccard 1; near-zero Procrustes disparity | fixed synthetic configuration | Bounded software compatibility evidence, not manuscript-scale evidence. |
| 7 | Fresh Stage 1 fixed synthetic run | 24 vectors × 80 numeric variables after metadata removal | 3 clusters, 0 noise; selected model `model_060fac0208bb58e2` | n_neighbors 10; 3D densMAP; seed 42; HDBSCAN min_cluster_size 5, min_samples 2, epsilon 0, EOM | Fresh local execution baseline. Reproduction labels have SHA-256 `5b7ba37a542efcceebd5d39a69342279e44565f017c2c099e36060c3eb0496ee`. |
| 8 | Toy/synthetic/MNIST demonstrations | dataset-specific | Tutorial or benchmark outputs | dataset-specific | Educational/technical only. Never evidence for IDP biology. |
| 9 | Fresh 164-IDP 1,000-seed Freeze 3 run | historical exact 164 matrix | pending | reconstructed Level 3 configuration | Explicitly not run in Stage 1; computationally consequential and requires separate user approval. |

## Golden software facts

- Version: `3.0.0rc1`.
- Fresh package source digest: `df87825992ab51dc016c673cf420a978ba5c161bd6c755e00a5199ead310e65b`.
- Fresh fixed config digest: `67b5f18293839440de6c04fc8cc171bf2f349d83900fa0092c50ba79e7e14ef9`.
- Fixed input SHA-256: `77d1956fd074da9d82ce0d6a9c896446895a5e22b2fc6da85417169d13b9bb01`.
- Fresh fixed selected model: `model_060fac0208bb58e2`.
- Fixed label SHA-256: `5b7ba37a542efcceebd5d39a69342279e44565f017c2c099e36060c3eb0496ee` for both run and reproduction.
- Fresh comparison: ARI 1.0; NMI 1.0; noise-set Jaccard 1.0; mapped membership fraction 1.0; variation of information 0; Procrustes disparity `2.7088204667806472e-31`.
- Fresh validation: 24 passed, 0 failed, 0 warnings.
- Historical 164 model table SHA-256: `78600f27b1ebc580327e409e30634acde92ff6089575a5818c81adc3d9edeb88`.
- Fresh and retained rescored-164 tables contain 333 rows and have maximum absolute `score` difference 0.

## Primary 2,315 result

The full historical 2,430-row candidate table permits exact score forensics. Retained Freeze 3 evidence reports a maximum numerical difference of approximately `9.99e-16` when the historical formula is reapplied. This establishes score reconstruction, not label refitting, because the 2,315-vector source matrix is absent.

## Secondary 459 result

The reported cluster membership counts sum to 443 non-noise plus 16 noise = 459. That internal arithmetic is consistent. Reproduction is nevertheless blocked by absent raw/model files and conflicting parameters. Until resolved, documentation may state counts as reported but must not emit a single “authoritative” parameter block.

## Secondary and adapted 164 result

The exact historical input contains 86,885 variant rows, four metadata columns, and 164 analysis columns; its SHA-256 is `0cc17db052e28e3c1cd7600f7140f9b929b9e2d2a5b4f9ded3ebf4df3e032f96`. The ID-key SHA-256 is `b664e6139e18305168327c5420c1a1af8379312f3ce0645f5f42dbcc394febc4`. One legacy coordinate column lacks a value for `IDP_2143`, while the label is present; this affects coordinate completeness, not membership count.

The Freeze 3 adapter achieved exact ID-set matching and unchanged labels/noise. Because it did not fit UMAP/HDBSCAN, the correct verb is “adapted” or “retained,” not “reproduced by refitting.”

## Separation rule for Edition 3

Every table, plot, and exercise must carry an analysis-level label from this document. A value may not move between levels without a traceable transformation record. In particular:

- do not attach 164 parameters to 2,315 or 459 results;
- do not use 356 as an alternative 164 count;
- do not call fixed-fixture equality a full-data reproduction;
- do not call score reapplication a clustering rerun; and
- do not merge historical and fresh results under a single unqualified “DIMPLE result.”
