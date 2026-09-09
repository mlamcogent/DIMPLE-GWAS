# Tutorial 3 — Explain, compare, and validate existing outputs

Define shell variables after verifying the paths from the Freeze 3 repository root:

```bash
SOURCE_RUN=docs/manual/tutorials/01_fixed_synthetic/run_20260825_v2
MODEL_ID=model_060fac0208bb58e2
MODEL_JSON="$SOURCE_RUN/models/top_model_artifacts/$MODEL_ID/summary.json"
```

Use new output names when repeating the steps:

```bash
dimple-gwas score-existing \
  --models "$SOURCE_RUN/models/all_models.tsv" \
  --output docs/manual/tutorials/03_explain_compare_validate/scored_NEW.tsv

dimple-gwas summarize-models \
  --models "$SOURCE_RUN/models/ranked_models.tsv" \
  --output-dir docs/manual/tutorials/03_explain_compare_validate/summaries_NEW

dimple-gwas reproduce-model \
  --model-json "$MODEL_JSON" \
  --input benchmarks/synthetic/synthetic_matrix.tsv \
  --output-dir docs/manual/tutorials/03_explain_compare_validate/reproduced_NEW \
  --n-jobs 1

dimple-gwas explain \
  --model-json "$MODEL_JSON" \
  --output-dir docs/manual/tutorials/03_explain_compare_validate/explanation_NEW

dimple-gwas compare \
  --left "$MODEL_JSON" \
  --right docs/manual/tutorials/03_explain_compare_validate/reproduced_NEW/models/top_model_artifacts/$MODEL_ID/summary.json \
  --output-dir docs/manual/tutorials/03_explain_compare_validate/comparison_NEW \
  --require-same-order

dimple-gwas validate \
  --run-dir "$SOURCE_RUN" \
  --output-dir docs/manual/tutorials/03_explain_compare_validate/validation_NEW
```

The executed build had exact identifier/order equality, ARI/NMI/noise Jaccard/mapped membership of 1, near-zero Procrustes disparity, and 24/24 validation checks passing. This is bounded same-environment fixture evidence. Original-space correlations and heatmaps are descriptive and post-selection.
