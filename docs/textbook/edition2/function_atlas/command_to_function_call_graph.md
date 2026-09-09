# Command-to-function call graph

This graph is a teaching-level view derived from the current CLI dispatch and package call graph. The complete symbol-level inventory and dependencies are in `function_inventory.tsv`.

```mermaid
flowchart LR
  shell["dimple-gwas / python -m dimple_gwas"] --> main["cli.main"]
  main --> inspect["inspect-config → cli._inspect"]
  main --> show["show-search-space → cli._show"]
  main --> run["run → pipeline.run_search"]
  main --> score["score-existing → cli._score"]
  main --> summarize["summarize-models → cli._summarize"]
  main --> reproduce["reproduce-model → pipeline.run_search (fixed)"]
  main --> explain["explain / interpret → interpretation.run_explanation"]
  main --> compare["compare → comparison.run_comparison"]
  main --> validate["validate → validation.run_validation"]

  inspect --> config["resolve_config → validate_config"]
  show --> enumerate["enumerate_candidates → write_search_space"]
  run --> prep["prepare_analysis_matrix"]
  run --> enumerate
  run --> umap["run_repeated_umap"]
  run --> hdb["fit_hdbscan"]
  run --> metrics["evaluate_candidate"]
  run --> scoring["apply_scoring → rank_models"]
  run --> report["write_model_outputs"]
  explain --> similarity["compute_similarity / compute_order"]
  explain --> heatmap["render_heatmap"]
```

The `interpret` spelling is a compatibility alias for `explain`, not a separate analytical implementation. `reproduce-model` resolves a one-candidate fixed configuration and enters the same audited search pipeline; it is not an unrecorded shortcut.
