# 19. Fixed synthetic end-to-end analysis

*Guiding question:* **Can a fresh user complete the entire software path and account for every output?**

Prerequisites: 13–17.

## Why the question matters

A designed fixture can verify contracts quickly but cannot estimate production robustness or biological validity.

The fresh Edition 2 run uses one seed and one candidate, producing three designed groups of eight with no noise.

This chapter develops the question in the order needed for a reader to move from statistical principle to current implementation, retained evidence, and a defensible statement. Its central worked task is: Audit the 24-by-80 prepared shape, the selected model, its metric values, the output inventory, and all 24 validation checks.

## Learning objectives

After completing Chapter 19, the reader can:

1. define seed schedule and explain its role without exceeding the stated caution;
2. define noise label and explain its role without exceeding the stated caution;
3. define candidate identity and explain its role without exceeding the stated caution;
4. define silhouette and explain its role without exceeding the stated caution;
5. define trustworthiness and continuity and explain its role without exceeding the stated caution;
6. trace the relevant package functions and generated artifacts;
7. complete the worked task and distinguish observation from interpretation.

## Conceptual and mathematical development

### seed schedule

Deterministic list controlling repeated stochastic fits. A compact notation is `legacy: 1,...,S; current: r,...,r+S-1`. In practical terms, recorded seeds permit replay but do not guarantee cross-platform bitwise identity. [@reproduciblesum2015]

Within Freeze 3 RC1 the concept is connected to `ensemble_seeds` and is visible through `embedding_manifest.json`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### noise label

Label -1 for points unassigned under a fitted density model. A compact notation is `label_i=-1`. In practical terms, noise is algorithmic and parameter-conditional, never a biological-null statement. [@campello2015hdbscan]

Within Freeze 3 RC1 the concept is connected to `fit_hdbscan` and is visible through `labels.tsv`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### candidate identity

Deterministic hash and ordinal for a resolved parameter combination. A compact notation is `model_id=H(canonical parameters)`. In practical terms, identity supports replay; it is not a quality score.

Within Freeze 3 RC1 the concept is connected to `candidate_identity` and is visible through `search_space.tsv; model_table.csv`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### silhouette

Within-versus-nearest-other-cluster separation under a configured metric. A compact notation is `s(i)=(b(i)-a(i))/max(a(i),b(i))`. In practical terms, freeze 3 can exclude noise and supplies the configured HDBSCAN metric. [@rousseeuw1987]

Within Freeze 3 RC1 the concept is connected to `evaluate_candidate` and is visible through `model_table.csv`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### trustworthiness and continuity

Directed neighborhood-retention diagnostics. A compact notation is `T(k)=1-c sum_i sum_(j in U_k(i))(r(i,j)-k)`. In practical terms, freeze 3 computes both through directed calls to sklearn trustworthiness under Euclidean geometry. [@venna2010]

Within Freeze 3 RC1 the concept is connected to `embedding_quality_metrics` and is visible through `run_summary.json`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### legacy_dimple score

Population-relative weighted combination of normalized silhouette, clusters, and optionally noise. A compact notation is `raw=w_s s/max(s)+w_k k/max(k)-w_n n/max(n)`. In practical terms, weights are raw dynamic ranges divided by their sum; final scores are min-max scaled.

Within Freeze 3 RC1 the concept is connected to `legacy_dimple_score` and is visible through `scoring_manifest.json; model_table.csv`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### validation ladder

Separate software, technical, structural, statistical, biological, external, and cross-platform evidence. A compact notation is `E_software != E_biological`. In practical terms, passing tests or exact fixture replay cannot substitute for external biological validation.

Within Freeze 3 RC1 the concept is connected to `run_validation` and is visible through `validation_report.json`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

## Reconstructed operational foundation

Edition 1 contained the following verified operational material in separate short notes. Edition 2 consolidates it here and subjects it to the concept and evidence boundaries above.

### Evidence retained from former Chapter 13

### Operational foundation

The shortest verified run starts in the Freeze 3 repository root with the installed RC1 entry point. Inspect first, enumerate second, fit third, and use a new output root.

```bash
dimple-gwas inspect-config \
  --search-mode fixed \
  --config docs/textbook/edition2/labs/01_fixed_synthetic/tutorial_config.yaml

dimple-gwas show-search-space \
  --search-mode fixed \
  --config docs/textbook/edition2/labs/01_fixed_synthetic/tutorial_config.yaml \
  --output-dir docs/textbook/edition2/labs/01_fixed_synthetic/search_space_new

dimple-gwas run \
  --search-mode fixed \
  --config docs/textbook/edition2/labs/01_fixed_synthetic/tutorial_config.yaml \
  --output-dir docs/textbook/edition2/labs/01_fixed_synthetic/run_new
```

Replace `*_new` with unique names. The canonical documented output is `run_20260826`; do not overwrite it. The fixture is small and repository-owned. It demonstrates execution structure, not production adequacy.

### Retained evidence

The executed canonical run prepared 24 vectors by 80 variables, evaluated one candidate, selected `model_060fac0208bb58e2`, found three clusters of eight, and assigned no noise. Exit status was zero.

### Output-reading checkpoint

Confirm `run_manifest.json` status, one-row search manifest, one candidate table row, selected-model JSON, label row count/uniqueness, annotation join, log, and validation output when run.

### Misinterpretations to avoid

Do not copy an example output path unchanged. Do not jump directly to the plot before checking the manifest. Do not generalize ‘three clusters’ from the designed fixture to real data.

### Boundary inherited from Edition 1

One seed and one candidate make this a smoke test. They do not represent standard production compute or a robust model-selection study.

### Evidence retained from former Chapter 14

### Operational foundation

`run_manifest.json` is the primary run-level audit record. It names the schema, software/version, command, start/finish status, platform, architecture, Python and package versions, package-source hash, input record, resolved configuration and its hash, input contract, seeds, threads, backends, search size, runtime, selected model, scoring formula/profile, artifacts, Parquet outcome, warnings, exclusions, and failures.

A healthy manifest has `status=complete`, but completion alone is not enough. Reconcile candidate counts with search manifests, failed counts with `logs/model_failures.tsv`, selected model with `model_selection_manifest.json` and `best_model.json`, and artifact hashes with files. `git_commit` is null in this source snapshot; the package-source SHA-256 and file registers substitute for build identity in this draft.

### Retained evidence

Edition 2 Lab 2 records 32 search candidates, 32 completed models, zero failed models, four UMAP configurations, two random seeds (42,43), contrib HDBSCAN and umap-learn backends, and an approximately 10.713-second manifest runtime in its local environment.

### Output-reading checkpoint

Inspect `run_manifest.json`, `resolved_config.yaml`, both search-space manifests, `models/model_selection_manifest.json`, `logs/run.log`, and `logs/model_failures.tsv` as a set.

### Misinterpretations to avoid

Do not interpret a null Git commit as a random run; use the source hash. Do not ignore a recorded optional-Parquet failure. Do not assume a complete run had no invalid topologies.

### Boundary inherited from Edition 1

Manifests can disclose local paths, input hashes, platform information, and commands. Sanitize public copies without changing the retained private audit record.

### Evidence retained from former Chapter 32

### Operational foundation

Edition 2 Lab 1 is the canonical novice path. Its configuration fixes every searched field, uses the repository synthetic matrix and annotation table, one seed, three components, one HDBSCAN candidate, one job, and a new output root. The correct annotation join is `index`. Preflight proves one candidate before fitting.

The executed canonical directory is `tutorials/01_fixed_synthetic/run_20260826`. It prepared 24 vectors by 80 variables, selected `model_060fac0208bb58e2`, and produced three clusters of eight with no unassigned observations. Parquet writing succeeded. The validation utility later passed all 24 run-contract checks.

The earlier `run_20260825` is intentionally retained: clustering succeeded, but the original join key was absent and annotations were skipped with a warning. The canonical rerun demonstrates the evidence-preserving response—correct source configuration, write a new output root, and retain the prior attempt.

## Evidence diagram or figure





### Retained evidence

Use Chapters 14–15 with the actual YAML, Chapter 16 to reproduce the selected summary, Chapter 21 to compare it, and Chapter 17 to explain it. The complete commands and timings are in `docs/textbook/edition2/labs/execution_manifest.json`.

### Output-reading checkpoint

Inspect the config, preflight manifests, canonical run manifest, candidate tables, selection manifest, labels/annotations, logs, reproduction, comparison, explanation, and validation.

### Misinterpretations to avoid

Do not delete the noncanonical first run. Do not call the designed grouping discovery evidence. Do not use the fixed quickstart to choose production parameters.

### Boundary inherited from Edition 1

This fixture is a smoke test with deliberately clear structure. Runtime and accuracy are not a guarantee for large correlated GWAS inputs.

### Evidence retained from former Chapter 41

### Operational foundation

The output atlas classifies 35 produced artifact patterns plus three important non-artifacts. Run-root contracts are `resolved_config.yaml`, search manifests, `run_manifest.json`, and logs. Candidate/model contracts live in `models/`: all/ranked/top tables, optional Parquet, best/selection JSON, Pareto/family summaries, and per-retained-model labels/summary/reproduction YAML. Compatibility aliases use `stage02`, `stage03`, and `stage09` names.

Downstream families are separate: scoring creates a table plus manifest; summarization creates family/Pareto/top/count files; explanation creates similarity/order/cutpoint/summary/projection/association/exclusion/heatmap/manifest/README artifacts; comparison creates summary, membership, sizes, confusion, mapping, and manifest; validation creates check rows, report, and manifest.

Current Freeze 3 does **not** write the cleaned/transformed input, individual repeated embeddings, or full concatenated embedding. They are in-memory intermediates. Selected display coordinates are not the full concatenated representation. The machine-readable `output_atlas.tsv` records producer, condition, format, schema excerpt, identifiers, label convention, ordering, safe inspection, health checks, consumers, authority, privacy, example, checksum, and verification status for every item.

### Retained evidence

Use Edition 2 Lab 2 for run artifacts and Edition 2 Lab 3 for downstream artifacts. Each verified atlas example has a SHA-256 and software version. Optional coordinate associations are correctly marked not executed.

### Output-reading checkpoint

For every artifact: confirm producer, creation condition, encoding, row/key schema, identifier uniqueness, label `-1`, rank/order semantics, status/missingness, consumer, privacy, and checksum.

### Misinterpretations to avoid

Do not hunt for nonexistent embedding files. Do not read CSV aliases when the native TSV/JSON contract is needed. Do not publish logs/manifests without reviewing paths and study identifiers.

### Boundary inherited from Edition 1

Exact candidate-table columns are authoritative in the actual header. Future source changes require regenerating the atlas before updating prose.

## Implementation trace

**`pipeline.setup_logger`** is defined at `dimple_gwas/pipeline.py:25` with signature `output_dir: str | Path`. Implementation callable for setup logger. It is reached from pipeline.run_search and connects to No package-defined dependency detected. Its direct artifact contract is logs/run.log; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`pipeline.run_search`** is defined at `dimple_gwas/pipeline.py:130` with signature `config: Mapping[str, Any], output_dir: str | Path, command: list[str] | None=None`. Execute preprocessing, repeated embeddings, candidate evaluation, scoring, retention, reporting, and provenance for one run. It is reached from cli._reproduce; cli.main and connects to hdbscan_runner.fit_hdbscan; io.read_table; metrics.embedding_quality_metrics; pipeline._annotation_frame; pipeline._evaluate_one; pipeline._failed_row; pipeline.setup_logger; preprocessing.prepare_analysis_matrix; provenance.base_manifest; provenance.file_record; ranking.family_summaries; ranking.pareto_front; ranking.rank_models; ranking.top_models; reporting.write_model_outputs; reporting.write_resolved_config; reporting.write_search_space; scoring.apply_scoring; search_space.enumerate_candidates; search_space.stable_identifier; umap_runner.run_repeated_umap. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is RuntimeError; ValueError. Test evidence is recorded as tests/test_pipeline_integration.py::test_custom_leaf_eom_metric_and_max_size_run; tests/test_pipeline_integration.py::test_fixed_model_reproduction. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`reporting.write_resolved_config`** is defined at `dimple_gwas/reporting.py:18` with signature `config: Mapping[str, Any], output_dir: str | Path`. Implementation callable for write resolved config. It is reached from pipeline.run_search and connects to No package-defined dependency detected. Its direct artifact contract is resolved_config.yaml; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`reporting.write_search_space`** is defined at `dimple_gwas/reporting.py:28` with signature `candidates: list[Mapping[str, Any]], config: Mapping[str, Any], output_dir: str | Path`. Implementation callable for write search space. It is reached from cli._show; pipeline.run_search and connects to io.atomic_json_dump; io.json_safe; reporting._write_tsv; search_space.flatten_candidate. Its direct artifact contract is search_space_manifest.tsv; search_space_manifest.json; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`reporting.write_model_outputs`** is defined at `dimple_gwas/reporting.py:105` with signature `ranked, top, pareto, families, candidates_by_id: Mapping[str, Mapping[str, Any]], labels_by_id: Mapping[str, Any], visualizations_by_umap: Mapping[str, Any], feature_ids, annotation_frame, config: Mapping[str, Any], scoring_manifest: Mapping[str, Any], run_manifest: Mapping[str, Any], output_dir: str | Path`. Write the complete candidate, ranking, selection, retained-model, compatibility, and manifest artifact family. It is reached from pipeline.run_search and connects to io.atomic_json_dump; io.json_safe; provenance.file_record; provenance.utc_now; reporting._top_artifact; reporting._write_tsv. Its direct artifact contract is run_manifest.json; models/all_models.tsv; models/all_models.parquet; models/ranked_models.tsv; models/top_models.tsv; models/best_model.json; models/model_selection_manifest.json; models/pareto_front.tsv; models/family_summaries.tsv; stage02_hdbscan_gridsearch_results.csv; stage03_optimized_cluster_solutions.csv; stage09_umap_vizdata_with_clusters.csv; stage09b_umap_vizdata_with_annotations.csv; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`validation.run_validation`** is defined at `dimple_gwas/validation.py:15` with signature `run_dir: str | Path, output_dir: str | Path | None=None, *, command: list[str] | None=None`. Audit a run directory against required files, schemas, counts, identities, hashes, and manifest contracts. It is reached from cli._validate and connects to comparison._columns.<locals>.resolve; io.atomic_json_dump; io.ensure_empty_output_dir; io.json_safe; io.read_model_table; io.read_table; provenance.base_manifest; provenance.file_record; provenance.sha256_file; provenance.utc_now; validation.run_validation.<locals>.record. Its direct artifact contract is validation_checks.tsv; validation_report.json; validation_manifest.json; its explicit error surface is FileNotFoundError. Test evidence is recorded as tests/test_freeze3_comparison_validation.py::test_validation_detects_hash_mismatch; tests/test_freeze3_comparison_validation.py::test_validation_passes_complete_contract. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

## Claim adjudication notebook

The following statements are admitted to the draft only in their safe form:

- **VAL-002 (verified_with_qualification):** Within the prior same-environment fixture comparison, ARI, NMI, noise Jaccard, and mapped membership were 1 with near-zero Procrustes disparity. [@hubert1985; @vinh2010; @gower1975] Limitation: Does not generalize across platforms or all configurations. Implementation evidence: `comparison.py`.

## Reading the generated evidence

For Chapter 19, the `Fixed synthetic end-to-end analysis` files are read as a provenance chain rather than as isolated results:

| Artifact | Producer | What to verify before interpretation |
| --- | --- | --- |
| `resolved_config.yaml` | `write_resolved_config` | Artifact exists under the new output root, is readable, and its checksum is recorded. |
| `run_manifest.json` | `write_model_outputs` | status=complete; source/input hashes present; failed count understood; selected model and artifact records resolve. |
| `logs/run.log` | `setup_logger` | Artifact exists under the new output root, is readable, and its checksum is recorded. |
| `models/all_models.tsv` | `write_model_outputs` | Candidate count agrees with enumeration; failures remain; ranks and score eligibility are internally consistent. |
| `models/ranked_models.tsv` | `write_model_outputs` | Candidate count agrees with enumeration; failures remain; ranks and score eligibility are internally consistent. |
| `models/all_models.parquet` | `write_model_outputs` | Candidate count agrees with enumeration; failures remain; ranks and score eligibility are internally consistent. |
| `models/top_models.tsv` | `write_model_outputs` | Artifact exists under the new output root, is readable, and its checksum is recorded. |
| `models/best_model.json` | `write_model_outputs` | Artifact exists under the new output root, is readable, and its checksum is recorded. |
| `models/model_selection_manifest.json` | `write_model_outputs` | Artifact exists under the new output root, is readable, and its checksum is recorded. |
| `models/pareto_front.tsv` | `write_model_outputs` | Artifact exists under the new output root, is readable, and its checksum is recorded. |
| `models/family_summaries.tsv` | `write_model_outputs` | Artifact exists under the new output root, is readable, and its checksum is recorded. |
| `models/top_model_artifacts/<id>/labels.tsv` | `_top_artifact` | Identifiers are unique and exactly match the intended input; label -1 is treated as noise/unassigned. |
| `models/top_model_artifacts/<id>/summary.json` | `_top_artifact` | Artifact exists under the new output root, is readable, and its checksum is recorded. |
| `models/top_model_artifacts/<id>/reproduce.yaml` | `_top_artifact` | Artifact exists under the new output root, is readable, and its checksum is recorded. |

The output atlas supplies the complete schemas, checksums, conditions, consumers, and privacy notes for this Chapter 19 route. Native manifests can contain machine paths; the assembled textbook uses sanitized excerpts while restricted evidence retains the original provenance chain.

## Worked reasoning and evidence exercise

Audit the 24-by-80 prepared shape, the selected model, its metric values, the output inventory, and all 24 validation checks.

A complete Chapter 19 answer must expose its intermediate reasoning, name the source or output used for `Fixed synthetic end-to-end analysis`, and finish with separate support and non-support statements. Applying that discipline to the question “Can a fresh user complete the entire software path and account for every output?” prevents a calculation, a software observation, and a scientific interpretation from collapsing into one claim.

## Assumptions, diagnostics, and recovery

The Chapter 19 analysis assumes the stated unit and inputs, the recorded configuration and software identity, and a diagnostic that addresses the claimed property rather than a convenient surrogate. Its decisive boundary is: The fresh Edition 2 run uses one seed and one candidate, producing three designed groups of eight with no noise.

If the Chapter 19 route fails, retain its log and candidate status before deciding whether the cause is input, configuration, dependency, compute, identifier alignment, or output-root state. Correct an operational failure by writing a new result directory. Treat instability in `Fixed synthetic end-to-end analysis` as sensitivity evidence: report it and identify the independent evidence needed instead of relabeling ambiguity as a software exception.

## Chapter synthesis

A designed fixture can verify contracts quickly but cannot estimate production robustness or biological validity. The implementation trace makes the current behavior auditable, but the evidence boundary remains part of the result. Chapter 20 expands the candidate population to reveal ranking and sensitivity behavior.

## Exercises

1. For `Fixed synthetic end-to-end analysis`, name the unit of analysis and one plausible but invalid substitute.
2. Reconstruct the notation for seed schedule; define its dimensions or denominator and interpret every term.
3. Choose a Tier A function mapped to Chapter 19; identify its caller and direct output, then propose a topic-specific edge case.
4. Select one Chapter 19 artifact from the output atlas and state three integrity checks that must precede scientific reading.
5. Convert a tempting `Fixed synthetic end-to-end analysis` overclaim into one observed statement followed by its limitation.
6. Audit the 24-by-80 prepared shape, the selected model, its metric values, the output inventory, and all 24 validation checks.

Appendix J gives the Chapter 19 adjudication guide. Its further-reading keys supply statistical context; no external paper is treated as automatic validation of the current software or dataset.
