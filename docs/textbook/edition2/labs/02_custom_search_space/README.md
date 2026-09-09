# Lab 2 — Custom bounded search and sensitivity

Status: **executed successfully in the fresh Edition 2 environment**. Runtime category: under one minute on the recorded host.

The Cartesian product contains four UMAP families and eight HDBSCAN settings per family, for 32 candidates. Every candidate completed; none was silently dropped. The two-seed schedule is `[42, 43]`. The selected model is `model_241ad5e99af55074`, but several candidates tie at the top because the designed fixture yields identical silhouette and cluster count within one representation family. Stable ordering therefore matters.

The exercise is to calculate 4×8 before execution, compare rank families, explain why normalized scores change with the candidate population, and report sensitivity without choosing settings to match desired labels. Native outputs are retained as evidence; publish only sanitized excerpts.
