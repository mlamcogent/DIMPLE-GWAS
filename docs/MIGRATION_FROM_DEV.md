# Migration from Dev

## Minimal migration

Historical execution remains available only from the preserved Dev/Freeze 2 evidence tree:

```bash
python DIMPLEGWAS.py --datainput matrix.tsv --outdir outputs/legacy ...
```

The supported Freeze 3 starting point is:

```bash
python -m dimple_gwas run \
  --input matrix.tsv \
  --search-mode standard \
  --scoring-profile legacy_dimple \
  --output-dir outputs/freeze3
```

Standard mode is intentionally large: 2,430 HDBSCAN candidates after a 1,000-run UMAP ensemble. Inspect first with `show-search-space`, and use fixed/custom settings for smoke tests.

## Move parameters into YAML

Start from `configs/legacy_dev.yaml`, then convert a fixed value to a list only when that dimension belongs in the scientific search. For example:

```yaml
umap:
  metric: [euclidean, cosine]
hdbscan:
  cluster_selection_method: [eom, leaf]
  max_cluster_size: [0, 100]
```

Run `inspect-config` to verify precedence and `show-search-space` to see the complete product before computing.

## Output migration

Use `models/ranked_models.tsv` rather than assuming stage03 contains the only meaningful solution. Use `models/best_model.json` for the declared winner, `models/top_models.tsv` for alternatives, and per-model `reproduce.yaml` files for exact reruns. Failed candidates are data, not lost exceptions.

The stage09 best-model table names remain available. Annotation columns now use generic feature IDs and are also retained within each top-model artifact.

## Reproduction

```bash
python -m dimple_gwas reproduce-model \
  --model-json outputs/freeze3/models/best_model.json \
  --output-dir outputs/reproduced
```

Pass `--input` if the recorded path is no longer valid.

## Deprecated terminology

`--idp_key` is accepted as an alias but new workflows should use `--annotation-file` and `--annotation-index-col`. No pQTL, IDP, imaging, or modality name appears in default topology selection.
