# Command reference

The installed entry point is `dimple-gwas`; `python -m dimple_gwas` is equivalent.

## `run`

Fits every enumerated UMAP/HDBSCAN candidate and writes model, selection, and provenance artifacts.

Required in resolved configuration: `input.path`. Important CLI fields include `--search-mode`, `--config`, `--input`, `--output-dir`, UMAP/HDBSCAN parameter overrides, execution limits, and scoring profile. CLI values override YAML values.

## `inspect-config`

Resolves built-in mode, YAML, and CLI overrides; validates all fields; prints YAML and candidate counts. `--output` optionally retains the resolved YAML. No model is fitted.

## `show-search-space`

Enumerates the complete deterministic Cartesian product. `--output-dir` writes TSV/JSON; `--show-first N` controls stdout preview. No model is fitted.

## `score-existing`

Applies the canonical score to a native model table or historical notebook columns (`Silhouette_avg`, `Clusters`, `Noise_points`, `Epsilon`, `Min_samples`, `Min_cluster_size`). Historical source score columns are preserved with a `source_` prefix. Use `--fit-include-noise` only for candidate populations whose score historically included the noise term.

## `summarize-models`

Writes family summaries, a Pareto table, top models, and summary counts from an existing native model table. It ranks only when rank is absent.

## `reproduce-model`

Reads retained UMAP/HDBSCAN parameters from native JSON and performs a one-candidate fixed rerun. `--input` overrides a stale recorded path. This command refits; `explain` does not.

## `explain` / `interpret`

Exactly one source is required:

- `--model-json`: native top-model `summary.json`; or
- `--legacy-table` plus `--input`: legacy labels/coordinates.

Important options: orientation/ID columns, similarity (`pearson`/`spearman`), ordering, noise policy, undefined-correlation policy, complete matching, figure size, similarity-table writing, and opt-in coordinate associations. Native default output is a sibling `interpretation/`; legacy mode requires `--outdir`.

## `compare`

`--left` and `--right` accept native summary JSON or tabular labels. Exact ID sets are required. It reports ARI, NMI, variation of information, noise Jaccard, optimal label mapping/confusion, changed membership/noise status, cluster sizes, and optional coordinate Procrustes disparity. Numeric label values are not assumed to identify the same cluster.

## `validate`

Checks required files, JSON/YAML readability, search-space counts, ranked schema, selected model artifacts, and recorded hashes. Default output is `<run-dir>/validation`; `--output-dir` selects another absent/empty directory. Exit status is one on validation failure.

## Search modes

- `standard`: one Dev-compatible UMAP family × 2,430 HDBSCAN candidates.
- `extended`: 1,728 declared UMAP/HDBSCAN combinations.
- `custom`: YAML-defined scalar/list/range fields.
- `fixed`: one complete UMAP/HDBSCAN configuration.

Every scientifically meaningful option is visible in `dimple-gwas <command> --help` or the resolved YAML.
