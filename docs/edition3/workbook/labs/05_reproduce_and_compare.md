# Lab 5 - Reproduce and compare two runs

**Evidence status:** freshly executed on the fixed fixture in Stage 1.

Reproduce the retained top model into a fresh directory:

```bash
python -m dimple_gwas reproduce-model \
  --model-json docs/edition3/labs/executed/lab03_run/models/top_model_artifacts/model_060fac0208bb58e2/summary.json \
  --output-dir docs/edition3/labs/executed/lab05_reproduction \
  --n-jobs 1
```

Then compare the two retained model summaries:

```bash
python -m dimple_gwas compare \
  --left docs/edition3/labs/executed/lab03_run/models/top_model_artifacts/model_060fac0208bb58e2/summary.json \
  --right docs/edition3/labs/executed/lab05_reproduction/models/top_model_artifacts/model_060fac0208bb58e2/summary.json \
  --output-dir docs/edition3/labs/executed/lab05_comparison \
  --require-same-order
```

Inspect exact ID agreement, label mapping, ARI, NMI, VI, noise Jaccard, mapped membership, cluster-size comparison, and Procrustes status. Stage 1 expectations were exact label-hash equality, ARI/NMI/noise Jaccard/mapped fraction 1, VI 0, and near-zero Procrustes disparity.

**Decision checkpoint:** label each observation as exact equivalence, structural equivalence, or neither. Write a separate sentence explaining why the result does not establish cross-platform or biological equivalence.

\newpage
