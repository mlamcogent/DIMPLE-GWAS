# Data contract

## Production clustering input

`dimple-gwas run` accepts CSV, TSV, and gzip-compressed CSV/TSV. The production orientation is `variants_by_vectors`:

```text
CHR  BP  A1  A2  trait_a  trait_b  trait_c
1    …   A   G   z        z        z
```

1. Read the table using the explicit delimiter or the filename suffix.
2. Remove exactly `input.drop_first_n_cols` leading metadata columns (default four).
3. Coerce every remaining cell to numeric and fail on missing/non-numeric values.
4. If `input.zscore_transform: rint`, apply column-wise rank inverse-normal transformation.
5. Transpose to vectors × original dimensions. The analysis vector IDs are the remaining source column names.

No PCA, SVD, feature selection, imputation, or hidden standardization occurs.

## Identifier rules

Identifiers are converted to strings and surrounding whitespace is removed. Empty and duplicate identifiers fail. Case and internal whitespace remain significant: `IDP_1` and `idp_1` are different.

Native top-model labels contain `feature_id` in the exact matrix order. Native explanation requires the complete ID set. A changed label-table hash fails before analysis when the summary records one.

## Legacy explanation inputs

The legacy adapter reads CSV, TSV, CSV/TSV gzip, XLSX, and XLS. It supports:

- `variants_by_vectors`: vector IDs are analysis column names; and
- `vectors_by_variants`: vector IDs come from `column:<name>` or a real matrix index.

`auto` orientation is accepted only when one candidate has unambiguous ID overlap. Explicit orientation is recommended for archival work.

```bash
dimple-gwas explain --legacy-table labels.xlsx --input matrix.tsv \
  --outdir outputs/explain --matrix-orientation vectors_by_variants \
  --vector-id-source column:vector_id --drop-first-n-cols 1 \
  --id-column feature_id --label-column label \
  --coordinate-columns UMAP_1,UMAP_2,UMAP_3
```

Complete matching is default. `--allow-incomplete-match` retains the intersection in matrix order and writes every matrix-only or label-only ID to `exclusions.tsv` and the manifest. Noise exclusion is a separate, explicit policy.

## Coordinate and label rules

Labels must be present. `-1`, `-1.0`, and `noise` denote noise. Supplied UMAP coordinate columns must be numeric and complete. At least two are required for projection-quality diagnostics. Coordinates annotate the retained result; they are not inputs to original-space similarity.

## Missing data and RINT

Production and explanation matrices fail on missing analysis cells. Freeze 3 does not silently drop dimensions or impute values. RINT ranks observed values within each source analysis column before transpose; a column with no observations fails.

## Input immutability

All outputs are written beneath the user-selected output directory. Explain/compare/validate refuse nonempty output directories. Tests verify that an existing sentinel file remains unchanged after a refusal.
