# Technical reference: output atlas

## Run root

`resolved_config.yaml` records the actual specification. `search_space_manifest.tsv` and `.json` record complete enumeration. `run_manifest.json` records software, source/input/config identities, environment, seeds, threads, counts, runtime, warnings, failures, selected model and artifact links. `logs/run.log` and `logs/model_failures.tsv` preserve execution history.

## Model tables and selection

`models/all_models.tsv` contains every candidate, including failed and invalid rows. Optional `all_models.parquet` is a columnar equivalent. `ranked_models.tsv` orders scored rows first; `top_models.tsv` contains the retained top subset. `best_model.json` and `model_selection_manifest.json` preserve the selected row, exact parameters, score formula, realized weights, ordering and identifiers. `pareto_front.tsv` and `family_summaries.tsv` expose trade-offs and parameter-family summaries.

Each retained top model has `top_model_artifacts/<model_id>/labels.tsv`, `summary.json`, optional annotations, and `reproduce.yaml`. The label file uses exact `feature_id` identity and `-1` for noise. Top-only retention does not preserve labels for every candidate.

Compatibility aliases beginning `stage02`, `stage03` and `stage09` exist for historical workflows. Native TSV/JSON artifacts are preferred when exact current schemas are needed.

## Explanation outputs

The explanation family includes an interpretation manifest, README, cluster summaries, exact or sampled similarity artifacts, order and cutpoint tables, projection-quality diagnostics, optional coordinate associations, exclusions, and static/interactive heatmaps. Ordering and display sampling do not change memberships. Native mode verifies retained identities; legacy mode records adaptation decisions.

## Comparison outputs

Comparison writes a summary, membership comparison, cluster sizes, confusion matrix, optimal label mapping, and manifest. Read label mapping before comparing numeric label values. Procrustes appears only when compatible coordinate arrays exist.

## Validation outputs

Validation writes `validation_checks.tsv`, `validation_report.json`, and `validation_manifest.json`. These document artifact/schema/count/hash status, not biological validity.

## Important non-artifacts

The cleaned/transformed input matrix, individual repeated embeddings, and full concatenated embedding are in-memory intermediates in the current run contract. Their absence is not a failed run. The first embedding's display coordinates are not the complete (rd)-dimensional clustering representation.

## Universal inspection fields

For every file confirm: producer; creation condition; format and schema; row identity/join keys; ordering; label/noise convention; missingness; source and input hashes; downstream consumers; privacy exposure; and whether the example is fresh, retained, reconstructed, illustrative or protocol-only.

The exhaustive machine-readable Edition 2 output atlas remains a verified salvage source. Edition 3's final reference pass should regenerate its 35 patterns directly from current source and Stage 1 evidence before public release.

\newpage
