# Lab 6 - Original-space explanation and heatmaps

**Evidence status:** freshly executed on the fixed fixture in Stage 1.

Run the native explanation route without refitting:

```bash
python -m dimple_gwas explain \
  --model-json docs/edition3/labs/executed/lab03_run/models/top_model_artifacts/model_060fac0208bb58e2/summary.json \
  --outdir docs/edition3/labs/executed/lab06_explanation
```

Confirm that the manifest records the retained input and label identity. Inspect cluster summaries, similarity output, order and cutpoints, exclusions, static and interactive heatmaps, and README. Verify that the display order changes presentation, not membership.

For each cluster, write:

- one observed original-space pattern;
- one plausible scientific hypothesis;
- one alternative technical or design explanation;
- the independent evidence needed to discriminate them.

Inspect noise rather than omitting it. Ask whether noise observations form gradients, weak similarities, small blocks, or isolated patterns.

**Decision checkpoint:** explain why this command is post hoc description and not a refit, reranking, or independent validation.

\newpage
