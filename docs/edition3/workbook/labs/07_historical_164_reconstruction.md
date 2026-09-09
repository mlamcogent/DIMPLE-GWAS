# Lab 7 - Retained historical 164-IDP reconstruction

**Evidence status:** retained historical labels plus fresh Stage 1 schema/score reconstruction; no fresh clustering fit.

Begin with the analysis hierarchy. Record the 164-IDP input identity, retained five-cluster/102-noise result, reconstructed selected parameters, and manual sorted-row-16 decision.

Reapply the historical score without refitting:

```bash
python -m dimple_gwas score-existing \
  --models ../freeze3_workspace/comparisons/idp_runs/historical_tables/original_164_model_table.tsv \
  --config configs/original_idp_164_historical_search.yaml \
  --fit-include-noise \
  --output docs/edition3/labs/executed/lab07_rescored_164.tsv
```

Stage 1 joined all 333 rows and observed maximum absolute score difference zero. Compare source and reconstructed score columns, but do not use the result to claim new labels.

Read the retained-adapter explanation artifacts and confirm exact ID matching. Document the missing third coordinate for `IDP_2143` without imputing it.

**Decision checkpoint:** write three separate statements for retained membership, score reconstruction, and pending refit. If any sentence uses “reproduced,” qualify exactly what was reproduced.

\newpage
