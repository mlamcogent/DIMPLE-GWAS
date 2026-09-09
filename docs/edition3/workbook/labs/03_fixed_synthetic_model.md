# Lab 3 - Small fixed synthetic model

**Evidence status:** freshly executed in Stage 1; synthetic software evidence only.

**Prerequisites:** Labs 0-2; dependencies available; fresh empty output roots.

Predict one candidate, 24 prepared vectors, 80 variables, and a complete manifest/model tree. Then run:

```bash
python -m dimple_gwas show-search-space \
  --search-mode fixed \
  --config docs/textbook/edition2/labs/01_fixed_synthetic/tutorial_config.yaml \
  --output-dir docs/edition3/labs/executed/lab03_search

python -m dimple_gwas run \
  --config docs/textbook/edition2/labs/01_fixed_synthetic/tutorial_config.yaml \
  --output-dir docs/edition3/labs/executed/lab03_run
```

**Runtime class:** bounded local smoke run; do not extrapolate its time to manuscript-scale analysis.

Inspect `resolved_config.yaml`, both search manifests, `run_manifest.json`, `models/all_models.tsv`, `models/model_selection_manifest.json`, the top-model summary, labels, annotations, and log. Reconcile declared, successful, invalid, and failed counts.

Stage 1 expectation: model `model_060fac0208bb58e2`, three designed groups, no noise. Treat a different result as a diagnostic event requiring environment/source/config comparison, not as permission to overwrite evidence.

Validate into another fresh directory. State why 24 passed artifact checks would still not establish biological validity.

\newpage
