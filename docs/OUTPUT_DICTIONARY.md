# Output dictionary

## Topology run root

| Artifact | Meaning |
| --- | --- |
| `resolved_config.yaml` | Complete built-in + YAML + CLI configuration used. |
| `search_space_manifest.tsv/json` | Complete deterministic candidate enumeration and counts. |
| `run_manifest.json` | Version/source/config/input/output hashes, runtime, seeds, threads, backend, status, warnings/failures. |
| `stage02_hdbscan_gridsearch_results.csv` | Compatibility alias of all candidate rows. |
| `stage03_optimized_cluster_solutions.csv` | Compatibility alias of ranked candidate rows. |
| `stage09_umap_vizdata_with_clusters.csv` | Selected retained IDs, labels, and visualization coordinates. |
| `stage09b_umap_vizdata_with_annotations.csv` | Optional annotation join for the selected model. |

## `models/`

| Artifact | Meaning |
| --- | --- |
| `all_models.tsv` | Every success, invalid topology, and failure; candidate order preserved. |
| `all_models.parquet` | Supplementary columnar copy when enabled. |
| `ranked_models.tsv` | Candidate table ordered by rank then candidate order. |
| `top_models.tsv` | Requested retained top-N eligible models. |
| `best_model.json` | Selected row, parameters, and resolved configuration. |
| `model_selection_manifest.json` | Formula, realized weights/ranges, counts, tie order, selected model. |
| `pareto_front.tsv` | Supplementary non-dominated set; not an alternate truth label. |
| `family_summaries.tsv` | Per-parameter-family candidate/success/failure/metric summaries. |
| `top_model_artifacts/<id>/labels.tsv` | Exact `feature_id`, label, and visualization coordinates. |
| `top_model_artifacts/<id>/summary.json` | Versioned native explanation contract and label hash. |
| `top_model_artifacts/<id>/reproduce.yaml` | One-model fixed reproduction configuration. |

Candidate tables contain parameter identity, embedding-quality fields, cluster/noise/size metrics, silhouette/DBCV/CH/DB fields and scopes, persistence summaries, status/error/runtime, seeds, raw/final score, profile, and rank. Exact columns are authoritative in the TSV header.

## `logs/`

`run.log` is the execution narrative. `model_failures.tsv` retains failed candidate rows and error text; failures are never silently dropped.

## Interpretation directory

| Artifact | Meaning |
| --- | --- |
| `original_space_similarity.tsv.gz` | Complete ordered vector-by-vector Pearson/Spearman table when enabled. |
| `heatmap_order.tsv` | 1-based order, exact ID, label/noise flag, and coordinates. |
| `cluster_cutpoints.tsv` | Zero- and one-based inclusive block boundaries and sizes. |
| `cluster_summary.tsv` | Within/between original-space similarity by cluster/noise block. |
| `projection_quality.tsv` | Trustworthiness/continuity of supplied visualization coordinates. |
| `coordinate_associations.tsv` | Optional descriptive original-dimension/coordinate correlations. |
| `exclusions.tsv` | Every unmatched or noise-policy-excluded ID; header exists even when empty. |
| `original_space_heatmap.png/html` | Static and self-contained human-readable render. |
| `interpretation_manifest.json` | Sources/hashes, data contract, options, counts, warnings/exclusions, output hashes. |
| `README.md` | Scope and interpretation caveats for the artifact directory. |

## Comparison directory

`comparison_summary.json`, `membership_comparison.tsv`, `cluster_sizes.tsv`, `label_confusion.tsv`, `optimal_label_mapping.tsv`, and `comparison_manifest.json` separate structural concordance from numeric labels.

## Validation directory

`validation_checks.tsv` contains one pass/warn/fail row per check. `validation_report.json` contains counts/status. `validation_manifest.json` records the validation environment and output hashes.
