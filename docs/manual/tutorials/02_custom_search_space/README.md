# Tutorial 2 — Custom bounded search space

This tutorial varies a transparent subset of parameters: two UMAP neighbor values, two minimum distances, two minimum-cluster sizes, two min-samples values, and two epsilon values. The complete product is four UMAP families × eight HDBSCAN configurations = 32 candidates.

```bash
dimple-gwas inspect-config \
  --search-mode custom \
  --config docs/manual/tutorials/02_custom_search_space/tutorial_config.yaml

dimple-gwas show-search-space \
  --search-mode custom \
  --config docs/manual/tutorials/02_custom_search_space/tutorial_config.yaml \
  --output-dir docs/manual/tutorials/02_custom_search_space/search_space_NEW

dimple-gwas run \
  --search-mode custom \
  --config docs/manual/tutorials/02_custom_search_space/tutorial_config.yaml \
  --output-dir docs/manual/tutorials/02_custom_search_space/run_NEW
```

The executed build evaluated 32/32 candidates, selected `model_241ad5e99af55074`, and exposed eight-way score ties within each UMAP family. Those exact labels and metrics belong to the repository synthetic fixture. The lesson is enumeration, workload, metric scope, and tie-aware selection—not tuning toward a desired biological grouping.
