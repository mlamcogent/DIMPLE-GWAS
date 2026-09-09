# Lab 4 - Small search, candidate failures, and ranking

**Evidence status:** the 32-candidate Edition 2 tutorial is retained; Stage 1 verified current enumeration and scoring contracts. Repeat only into fresh Edition 3 roots.

Use the bounded custom-search tutorial configuration retained under Edition 2. Inspect it first and calculate the Cartesian count by hand. Then use `show-search-space` and reconcile the command's count with your calculation before fitting.

After the run, answer:

1. How many UMAP families were fitted and reused?
2. How many candidates succeeded, were invalid topologies, or failed?
3. What were the realized legacy or custom scoring ranges and weights?
4. Did any numerical scores tie, and how did the deterministic model-ID rule order them?
5. Which candidates are Pareto members, and which chosen objectives created that set?
6. Does the selected partition remain similar among near-top candidates?

Create summaries with:

```bash
python -m dimple_gwas summarize-models \
  --models <run-dir>/models/all_models.tsv \
  --output-dir docs/edition3/labs/executed/lab04_summaries \
  --top-n-models 10
```

**Decision checkpoint:** write two result sentences: “winner under this declared search” and “evidence still needed before a stability claim.”

\newpage
