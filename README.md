# DIMPLE-GWAS Freeze 3 release candidate

DIMPLE-GWAS Freeze 3 is one modular Python package for repeated UMAP, HDBSCAN topology search, transparent DIMPLE fit-score ranking, original-input-space interpretation, run validation, and structural comparison. Version `3.0.0rc1` is a software-complete release candidate: local code, regression, documentation, and recovered-output checks pass, while a fresh 1,000-seed reconstruction of the historical 164-IDP clustering remains pending.

The `dimple_gwas` package and `dimple-gwas` command are authoritative. Historical monolithic scripts and the standalone cluster prototype are evidence only and are not included in this distributable tree.

## Install

Python 3.10 or newer is required. From this directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
python -m pip check
```

The validated local environment used Python 3.12.13. Docker, image security testing, registry publication, and cloud execution are subsequent phases and have not been performed.

## Quick start

Inspect configuration and the complete search size before fitting:

```bash
dimple-gwas inspect-config --search-mode fixed \
  --config configs/reproduce_single_model.yaml

dimple-gwas show-search-space --search-mode custom \
  --config configs/leaf_vs_eom.yaml --show-first 3
```

Run one fixed model in a new output directory:

```bash
dimple-gwas run --search-mode fixed \
  --config configs/reproduce_single_model.yaml \
  --output-dir outputs/fixed_run
```

Explain a retained native model without re-clustering:

```bash
dimple-gwas explain \
  --model-json outputs/fixed_run/models/top_model_artifacts/MODEL_ID/summary.json \
  --outdir outputs/fixed_run_explanation
```

Explain a legacy table with explicit identity and orientation:

```bash
dimple-gwas explain \
  --legacy-table historical_labels.xlsx --legacy-sheet Results \
  --input matrix.csv --outdir outputs/legacy_explanation \
  --matrix-orientation variants_by_vectors \
  --vector-id-source matrix_columns --drop-first-n-cols 4 \
  --id-column feature_id --label-column label \
  --coordinate-columns UMAP_1,UMAP_2,UMAP_3
```

Validate and compare retained outputs:

```bash
dimple-gwas validate --run-dir outputs/fixed_run \
  --output-dir outputs/fixed_run_validation

dimple-gwas compare --left left/summary.json --right right/summary.json \
  --output-dir outputs/comparison
```

All `explain`, `compare`, and explicit validation output directories must be absent or empty. Input files are never overwritten.

## Commands

```text
run                fit, score, rank, and retain candidate models
inspect-config     resolve built-in + YAML + CLI configuration
show-search-space  enumerate the deterministic Cartesian product
score-existing     score native or historical-notebook model tables
summarize-models   create top, family, and Pareto summaries
reproduce-model    refit one retained native model
explain            original-space post-run diagnostics (alias: interpret)
compare            ID-safe, label-permutation-invariant comparison
validate           check a run contract, schemas, files, and hashes
```

Use `dimple-gwas <command> --help` for the audited option list. See [COMMAND_REFERENCE.md](docs/COMMAND_REFERENCE.md) for semantics and examples.

## Scientific defaults and guardrails

- `legacy_dimple` remains the default scoring profile.
- Production input remains variants × vectors: remove the declared metadata prefix, require numeric values, optionally apply column-wise RINT, then transpose.
- UMAP receives the full prepared original matrix. No PCA, SVD, or other hidden pre-UMAP reducer exists.
- The clustering backend remains the contrib `hdbscan` package, not scikit-learn HDBSCAN.
- `eom`, Euclidean UMAP/HDBSCAN metrics, DensMAP, 30 neighbours, zero minimum distance, and the Dev parameter ranges remain the standard defaults.
- Alternative metrics, `leaf`, maximum cluster size, custom scoring, RINT, Spearman similarity, coordinate associations, and relaxed ID matching are explicit options.
- UMAP coordinates are descriptive. They are neither feature loadings nor causal/mechanistic explanations.

The standard search contains 2,430 HDBSCAN candidates. The shipped extended example contains 1,728 candidates. Candidate enumeration is complete and is never silently sampled.

## Input contract

The production `run` input is CSV/TSV with variants in rows. Columns before `drop_first_n_cols` are metadata; remaining column names are exact vector IDs. Missing/non-numeric analysis cells fail. `zscore_transform: rint` is explicit and occurs before transpose.

Legacy explanation additionally supports XLSX/XLS and a second explicit `vectors_by_variants` orientation. IDs are stripped only of surrounding whitespace and must be nonempty and unique. Native explanation always requires complete identity. Legacy explanation requires complete matching by default; `--allow-incomplete-match` writes every exclusion.

See [DATA_CONTRACT.md](docs/DATA_CONTRACT.md) for examples and failure behavior.

## Search, scoring, and selection

The legacy DIMPLE raw score normalizes silhouette, cluster count, and—only when explicitly enabled—noise count by their maxima. Dynamic-range weights are calculated across the eligible candidate population. The noise component is subtracted. Freeze 3 also emits a final 0–1 normalized score and deterministic tie handling. Scores are population-relative; do not compare absolute scores from different candidate populations.

No preferred cluster-count band, preferred noise ceiling, preferred largest-cluster ceiling, pQTL target, or biological target appears in the default score. The Modded soft-target score is excluded.

See [SCORING.md](docs/SCORING.md), [MODEL_SELECTION.md](docs/MODEL_SELECTION.md), and [SEARCH_SPACE.md](docs/SEARCH_SPACE.md).

## Original-space interpretation

`explain` consumes retained labels and supplied visualization coordinates. It never runs UMAP/HDBSCAN or changes ranking. It calculates vector-by-vector Pearson similarity in the original analysis dimensions by default, orders label blocks with average-linkage hierarchy, retains noise as a final block, writes cutpoints and cluster summaries, and produces self-contained HTML/PNG. Machine-readable tables remain complete even when figure rendering is block-preserving sampled.

Undefined correlations fail by default. Coordinate associations are opt-in, descriptive correlations and are not loadings, drivers, mechanisms, or causal effects. Cluster ANOVA and post-selection p-values are intentionally absent.

See [EXPLAINABILITY.md](docs/EXPLAINABILITY.md) and [OUTPUT_DICTIONARY.md](docs/OUTPUT_DICTIONARY.md).

## Provenance and compatibility

Run/model/interpretation/comparison/validation manifests record source and configuration digests, input/output hashes and sizes, identity/orientation rules, versions, OS/architecture, seeds/threads, backend, timing/status, warnings, exclusions, and failures where applicable. Top-model summaries bind retained labels with SHA-256.

The fresh Freeze 2 versus Freeze 3 fixed regression retained the same model ID and byte-identical labels; ARI/NMI and noise Jaccard were 1.0, with effectively zero Procrustes disparity. Historical 164- and 2,315-IDP model tables were independently rescored with maximum raw-score deviations below `1e-15` and identical score-tie groups; Freeze 3 applies its documented deterministic model-ID ordering within ties. Historical 164-IDP labels were adapted—not reclustered—and retained exactly while original-space diagnostics were generated.

See [PROVENANCE.md](docs/PROVENANCE.md), [MIGRATION.md](docs/MIGRATION.md), and [ORIGINAL_IDP_REPRODUCTION.md](docs/ORIGINAL_IDP_REPRODUCTION.md).

## Verification

```bash
python -m pytest -q
python -m pip check
dimple-gwas validate --run-dir outputs/fixed_run \
  --output-dir outputs/fixed_run_validation
```

Clean local result: 45 tests passed after the historical-table adapter test was added; zero failures or skipped tests are expected. The final validation report and exact environment are in the external build evidence workspace.

## Scope and limitations

UMAP is stochastic, HDBSCAN topology is parameter-dependent, and DIMPLE scoring is an explicit heuristic—not proof of one biologically correct partition. The recovered historical 164-IDP manuscript solution was a human-selected rank-16 candidate under its historical score, not the top-scoring candidate. Freeze 3 preserves that choice only in the labelled compatibility configuration; it does not make it a default target.

The original 164-IDP input and final outputs were recovered, but a fresh 1,000-seed run is resource/time pending. Therefore this build is not labelled “scientifically frozen.” See [SCIENTIFIC_LIMITATIONS.md](docs/SCIENTIFIC_LIMITATIONS.md), [VALIDATION_SUMMARY.md](docs/VALIDATION_SUMMARY.md), and [KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md).
