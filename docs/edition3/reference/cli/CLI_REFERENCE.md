# Technical reference: command-line interface

The installed entry point is `dimple-gwas`; `python -m dimple_gwas` is equivalent. Always inspect the live help for the installed version. The reference below is curated from the verified `3.0.0rc1` parser and Stage 1 help captures.

## Command map

| Intent | Command | Fits a model? | Principal result |
|---|---|:---:|---|
| Run a candidate search | `run` | yes | complete run tree |
| Resolve settings | `inspect-config` | no | YAML to stdout or file |
| Enumerate candidates | `show-search-space` | no | counts and optional TSV/JSON manifests |
| Re-score a retained table | `score-existing` | no | scored table plus manifest |
| Summarize a model table | `summarize-models` | no | top, family, Pareto and count summaries |
| Refit one retained model | `reproduce-model` | yes | one-model run tree |
| Describe retained labels | `explain` / `interpret` | no | similarities, summaries, heatmaps and manifest |
| Compare two retained results | `compare` | no | partition/coordinate agreement artifacts |
| Validate a run contract | `validate` | no | check table, report and manifest |

## `run`

Resolves a built-in mode, YAML, and explicit overrides; validates the configuration; enumerates the complete candidate product; prepares the input; fits repeated UMAP/densMAP families; fits HDBSCAN candidates; evaluates, scores and ranks eligible results; retains failures; refits or retains top artifacts as implemented; and writes provenance.

Required through configuration or override: `input.path` and a fresh `output-dir`. Important option families are input and annotations, UMAP/densMAP, HDBSCAN, execution limits and jobs, scoring, and search mode. CLI overrides take precedence over YAML, which takes precedence over built-in mode defaults.

Operational rule: preflight with `inspect-config` and `show-search-space`; do not use `run` merely to discover the candidate count.

## `inspect-config`

Resolves and validates configuration without fitting. It prints the resolved YAML and candidate count; `--output` optionally retains the YAML. Use it to establish the actual analysis specification after precedence resolution.

## `show-search-space`

Enumerates the complete deterministic Cartesian product. `--output-dir` writes `search_space_manifest.tsv` and `.json`; `--show-first N` limits only the stdout preview. It never silently truncates the actual candidate set.

## `score-existing`

Reads a native or adapted historical CSV/TSV candidate table, applies `legacy_dimple` or a configured custom score, preserves source score columns with `source_` prefixes, and writes the scored table plus manifest. `--fit-include-noise` should be used only when it reflects the historical or prespecified score population. This command does not refit UMAP or HDBSCAN.

## `summarize-models`

Reads a native model table and writes top models, family summaries, a Pareto table, and summary counts. It ranks only when required. `--top-n-models` affects the summary output, not the original run.

## `reproduce-model`

Reads a native retained `summary.json`, reconstructs a fixed one-candidate configuration, and performs a fresh fit. `--input` can override a stale recorded path; `--n-jobs` controls requested jobs. Reproduction can be exact or structurally similar depending on environment and dependencies.

## `explain` and `interpret`

These names are aliases. Exactly one source is required:

- `--model-json` for a native top-model summary; or
- `--legacy-table` with an original `--input` for historical labels/coordinates.

Key options select matrix orientation, ID and label columns, optional coordinate columns, Pearson/Spearman similarity, ordering, noise policy, undefined-correlation behavior, exact/incomplete matching, heatmap bounds, similarity writing, and opt-in coordinate associations. Native mode verifies recorded hashes and identity where present. The command does not refit or rerank.

## `compare`

`--left` and `--right` accept native summaries or tabular labels. `--output-dir` must be fresh. Exact ID sets are required; `--require-same-order` additionally tests source order. The command reports ARI, NMI, variation of information, noise-set Jaccard, Hungarian label mapping, mapped membership, changed status, cluster sizes, and conditional Procrustes disparity.

## `validate`

`--run-dir` identifies the run; `--output-dir` optionally selects a separate fresh validation root. Checks cover required files, readability, schemas, counts, selected-model links and hashes. Failed checks produce failure status and a nonzero exit code. The command does not assess biological validity.

## Search modes

| Mode | Built-in purpose | Candidate count before YAML/CLI override |
|---|---|---:|
| `standard` | legacy-compatible UMAP family and HDBSCAN grid | 2,430 |
| `extended` | broader representation and clustering alternatives | 1,728 |
| `custom` | analyst-declared lists/ranges | configuration-dependent |
| `fixed` | one complete scalar configuration | 1 |

## Exit and mutation behavior

Parser and validation errors fail before fitting. Output-producing commands refuse unsafe occupied roots under their contract. Non-strict searches retain candidate errors and continue; strict behavior can promote errors. Preserve stderr/stdout, exit status, and the run's own logs and manifests.

\newpage
