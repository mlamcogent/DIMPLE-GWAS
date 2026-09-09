# DIMPLE-GWAS Freeze 3 RC1 output atlas

This atlas contains **35 produced artifact patterns** and **3 important non-artifacts**. Fresh Edition 2 Labs 1–3 verify 34 patterns; 1 optional pattern remains unexecuted and is labeled accordingly. The machine-readable contract is `output_atlas.tsv`.

An output is meaningful only with its producer, creation condition, schema, identifier rules, ordering, checksum, and evidence status. Native manifests may contain absolute paths and host details; publish only sanitized excerpts.

## `run` artifacts

| Pattern | Purpose | Condition | Verification |
| --- | --- | --- | --- |
| `resolved_config.yaml` | resolved configuration | always | verified |
| `run_manifest.json` | software/input/config/runtime/artifact provenance | complete run | verified |
| `logs/run.log` | execution narrative | always | verified |
| `models/all_models.tsv` | all candidates in candidate order | always | verified |
| `models/ranked_models.tsv` | eligible candidates ranked with failures retained | always | verified |
| `models/all_models.parquet` | supplementary columnar candidate table | optional; failure recorded | verified |
| `models/top_models.tsv` | retained top-N eligible models | always; may be empty | verified |
| `models/best_model.json` | selected row, parameters, resolved config | always; null model possible | verified |
| `models/model_selection_manifest.json` | formula, realized weights, counts, tie ordering | always | verified |
| `models/pareto_front.tsv` | supplementary non-dominated candidate set | always | verified |
| `models/family_summaries.tsv` | parameter-family success/failure/metric summaries | always | verified |
| `models/top_model_artifacts/<id>/labels.tsv` | exact IDs, labels, display coordinates | successful retained refit | verified |
| `models/top_model_artifacts/<id>/summary.json` | native retained-model contract and label hash | successful retained refit | verified |
| `models/top_model_artifacts/<id>/reproduce.yaml` | one-model fixed configuration | successful retained refit | verified |
| `stage02_hdbscan_gridsearch_results.csv` | legacy-compatible all-candidate alias | always | verified |
| `stage03_optimized_cluster_solutions.csv` | legacy-compatible ranked alias | always | verified |
| `stage09_umap_vizdata_with_clusters.csv` | selected labels and display coordinates | selected retained refit | verified |
| `stage09b_umap_vizdata_with_annotations.csv` | selected labels joined to annotations | valid annotation join | verified |

## `run/show-search-space` artifacts

| Pattern | Purpose | Condition | Verification |
| --- | --- | --- | --- |
| `search_space_manifest.tsv/json` | complete deterministic enumeration | always when command succeeds | verified |

## `score-existing` artifacts

| Pattern | Purpose | Condition | Verification |
| --- | --- | --- | --- |
| `<output> + <output>.manifest.json` | rescored/ranked table and scoring schema record | always | verified |

## `summarize-models` artifacts

| Pattern | Purpose | Condition | Verification |
| --- | --- | --- | --- |
| `family_summaries.tsv, pareto_front.tsv, top_models.tsv, summary.json` | post hoc model summaries | always | verified |

## `explain` artifacts

| Pattern | Purpose | Condition | Verification |
| --- | --- | --- | --- |
| `original_space_similarity.tsv.gz` | ordered full similarity matrix | when enabled | verified |
| `heatmap_order.tsv` | exact plotted order, label, noise flag, coordinates | always | verified |
| `cluster_cutpoints.tsv` | zero/one-based block boundaries | always | verified |
| `cluster_summary.tsv` | within/between descriptive similarity summaries | always | verified |
| `projection_quality.tsv` | trustworthiness/continuity of supplied coordinates | when coordinates are usable | verified |
| `coordinate_associations.tsv` | opt-in descriptive coordinate correlations | opt-in only | optional_not_executed |
| `exclusions.tsv` | unmatched/noise-policy exclusions | always, header when empty | verified |
| `original_space_heatmap.png/html` | static and interactive ordered heatmaps | always within safeguards | verified |
| `interpretation_manifest.json + README.md` | scope, hashes, options, caveats | always | verified |

## `compare` artifacts

| Pattern | Purpose | Condition | Verification |
| --- | --- | --- | --- |
| `comparison_summary.json` | ARI/NMI/VI/noise/membership/coordinate metrics | always | verified |
| `membership_comparison.tsv, cluster_sizes.tsv, label_confusion.tsv, optimal_label_mapping.tsv` | ID-level and cluster-level concordance | always | verified |
| `comparison_manifest.json` | sources/options/output hashes | always | verified |

## `validate` artifacts

| Pattern | Purpose | Condition | Verification |
| --- | --- | --- | --- |
| `validation_checks.tsv` | one pass/warn/fail row per contract check | always | verified |
| `validation_report.json + validation_manifest.json` | aggregate status and provenance | always | verified |

## Important non-artifacts

- **cleaned/transformed input matrix:** Prepared in memory. Do not assume the original input was rewritten.
- **individual repeated UMAP embeddings:** Computed and cached in memory by UMAP family. Do not invent per-seed embedding files.
- **concatenated embedding matrix:** Computed and cached in memory for HDBSCAN. Visualization coordinates are not the full concatenated embedding.

## Reading rules

A `model_id` is a deterministic candidate identity, not a scientific label. Candidate tables retain failed and invalid candidates. Rank is descending score, then descending raw score, then ascending model ID. HDBSCAN label `-1` is unassigned under a fitted representation and parameter set. The selected display coordinates are not the full repeated concatenated embedding. Original-space similarities are descriptive and conditional on the selected partition.
