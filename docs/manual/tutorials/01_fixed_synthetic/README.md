# Tutorial 1 — Fixed synthetic quickstart

Run from the Freeze 3 repository root inside an isolated environment. Choose new directory names; `run_20260825_v2` is retained build evidence.

```bash
dimple-gwas inspect-config \
  --search-mode fixed \
  --config docs/manual/tutorials/01_fixed_synthetic/tutorial_config.yaml

dimple-gwas show-search-space \
  --search-mode fixed \
  --config docs/manual/tutorials/01_fixed_synthetic/tutorial_config.yaml \
  --output-dir docs/manual/tutorials/01_fixed_synthetic/search_space_NEW

dimple-gwas run \
  --search-mode fixed \
  --config docs/manual/tutorials/01_fixed_synthetic/tutorial_config.yaml \
  --output-dir docs/manual/tutorials/01_fixed_synthetic/run_NEW
```

Expected structural checks: one candidate, exit zero, `run_manifest.json` status `complete`, 24 unique retained IDs, three non-noise clusters of eight in the designed fixture, zero failed candidates, and a present annotation join. These are fixture-specific engineering checks, not production targets.

The initial `run_20260825` is retained because an incorrect annotation join key caused annotations to be skipped. The corrected configuration uses `annotation_index_col: index`; `run_20260825_v2` is canonical.
