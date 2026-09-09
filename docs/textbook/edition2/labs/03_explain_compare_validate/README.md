# Lab 3 — Explain, compare, validate, and report

Status: **all six downstream commands executed successfully**: `score-existing`, `summarize-models`, `reproduce-model`, `explain`, `compare`, and `validate`.

Fixed-model reproduction preserved the 24 identifiers and three-cluster partition. Comparison reports ARI 1.0, NMI 1.0, variation of information 0, noise-set Jaccard 1.0, mapped membership 24/24, and Procrustes disparity 2.7088×10⁻³¹. Validation passed 24/24 checks. These values are bounded same-environment fixture evidence, not cross-platform or biological validation.

The explanation directory contains the ordered similarity matrix, order/cutpoint sidecars, cluster summary, projection diagnostics, exclusions, static and interactive heatmaps, and manifest. Treat all original-space summaries as descriptive and post-selection. Inspect identifiers and exclusions before the heatmap. Publish only `safe_artifacts/`; native manifests contain host paths.
