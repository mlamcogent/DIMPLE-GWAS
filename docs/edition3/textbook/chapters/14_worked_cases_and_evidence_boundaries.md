# Worked DIMPLE-GWAS cases and their evidence boundaries

The DIMPLE-GWAS archive contains several analyses that are easy to conflate because they share software, terminology, or files. Their counts cannot be combined. Each case answers a different question and carries a different evidence status.

![The 2,315-, 459-, 164-, 356-row and synthetic artifacts occupy distinct analysis and evidence levels.](assets/figures/analysis_hierarchy.png){#fig-analysis-hierarchy width=96%}

## Case 1: the fresh fixed synthetic baseline

The Stage 1 fixture contains 24 vectors and 80 numeric variables after metadata removal. It fits one three-dimensional densMAP view using `n_neighbors=10`, `min_dist=0`, Euclidean metric and seed 42. HDBSCAN uses minimum cluster size 5, minimum samples 2, epsilon 0, EOM selection and Euclidean distance.

The run produced one successful candidate, three clusters and no noise. Silhouette was approximately 0.9424, DBCV 0.9452, trustworthiness 0.8676, continuity 0.8779, Calinski-Harabasz 3642.25 and Davies-Bouldin 0.0721. Reproduction produced byte-identical labels; comparison was structurally exact under the reported metrics; validation passed 24/24 checks.

**Supported conclusion:** the bounded current software path executed consistently under the recorded macOS arm64 environment.

**Not supported:** that three clusters are expected in IDP data, that one seed is robust, that score 1 is absolute validity, or that the fixture establishes biological performance.

## Case 2: the primary 2,315-IDP analysis

The manuscript reports 2,315 IDPs, 15 clusters and 153 noise assignments. A retained 2,430-row candidate table allows exact forensic reapplication of the historical score, with maximum discrepancy around numerical rounding. The raw matrix is absent.

**Supported conclusion:** the reported result and retained candidate-score structure can be documented; the historical score can be reconstructed from the retained table.

**Not supported:** that Stage 1 freshly refitted the representation or labels. A score reconstruction does not recreate UMAP/densMAP coordinates or HDBSCAN membership.

## Case 3: the 459-IDP diffusion/white-matter analysis

The manuscript and supplement report 459 IDPs, six clusters, 16 noise assignments, and non-noise cluster sizes 24, 41, 31, 44, 272 and 31. The arithmetic closes: 443 non-noise plus 16 noise equals 459. The raw matrix and full model table are absent, and parameter records conflict.

**Supported conclusion:** these are reported secondary-analysis counts with an unresolved configuration conflict.

**Not supported:** an authoritative reproduction YAML. Selecting one conflicting record without an execution artifact would fabricate certainty.

## Case 4: the retained historical 164-IDP analysis

The exact historical input contains 86,885 variant rows, four metadata columns and 164 analysis columns. Retained labels contain five non-noise clusters of sizes 9, 13, 15, 14 and 11, plus 102 noise assignments (62.19%). The reconstructed selected parameters are epsilon 0, minimum samples 4, minimum cluster size 6, EOM selection, densMAP and 1,000 seeds, with noise included in the historical score.

The selected historical row was manually chosen at sorted position 16, not rank one. That fact prevents a clean retrospective story in which the score automatically discovered one uniquely optimal solution.

Freeze 3 exactly adapted the 164 identifiers and labels to the current explanation schema and re-scored all 333 retained model rows with maximum score difference zero. It did not rerun the 1,000 seeded embeddings or refit HDBSCAN.

**Supported conclusion:** exact retained membership, schema adaptation, original-space descriptive explanation and score reconstruction.

**Not supported:** fresh clustering reproduction, real-data seed stability, or a claim that the manual selection was the unique score optimum.

One historical third-coordinate value is missing for `IDP_2143`. The label is present. Two-coordinate retained diagnostics can be reported with that limitation; silent imputation is not allowed.

## Case 5: the 356-row validation workbook

The 356-row workbook is a distinct retained validation artifact. It is not an alternative count for the 164-IDP analysis. Joining or summarizing the two without an explicit transformation record would mix analysis populations.

This case illustrates a broader provenance rule: a familiar column name such as `Cluster` does not make two files commensurate. Counts require identities, source population, generation method, and analysis level.

## Case 6: MNIST and other demonstrations

MNIST and hand-worked toy data can teach representation, clustering, and diagnostic behavior because their structure is easy to inspect. They are not evidence for imaging-genetic biology. High purity can coexist with fragmentation, noise, parameter dependence, or a mismatch between the benchmark target and the scientific problem.

Use benchmarks to test software contracts or a clearly stated methodological property. Do not transfer their cluster counts, tuning choices, or apparent performance to IDP analyses.

## The pending 164-IDP 1,000-seed run

The fresh full refit is computationally consequential and was intentionally not launched in Stage 1. A valid execution needs the immutable historical input, the reconstructed configuration, an approved environment, explicit threads and jobs, a fresh output root, retained logs, complete manifests, comparison to the historical labels, and predeclared acceptance criteria.

The outcome could match the retained result exactly, agree structurally but not bytewise, or differ materially. Each possibility is scientifically informative. The protocol should not define success solely as recovery of the old labels; doing so would convert validation into confirmation seeking.

## A case-study reporting template

Every case should state: analysis level; input size and identity; configuration and seed provenance; environment; whether it was freshly executed; output status; supported conclusion; unsupported conclusions; and the next evidence needed. This template is useful because it prevents the most common historical error—merging a retained result, an adapter, a rescore and a fresh refit under one word: “reproduced.”

## The decision created by this chapter

The archive supports a strong local software story and a carefully bounded historical story. It does not yet support a complete scientific freeze. The final chapter positions that exploratory topology story among other multivariate genetic methods without claiming a benchmark that has not been performed.

**Evidence trail.** Claims SCI-2315, SCI-459, SCI-164, SCI-164P, SCI-164R, SCI-356, QA-003 and QA-004; gaps G-001 to G-004 and G-013 to G-014.

## Questions for the reader

1. For each case, identify whether the evidence is fresh, retained, reconstructed, illustrative, or protocol-only.
2. Why does exact re-scoring of 333 rows not reproduce a clustering?
3. What acceptance criterion for the fresh 164 run would avoid defining success as agreement with the historical result?

\newpage
