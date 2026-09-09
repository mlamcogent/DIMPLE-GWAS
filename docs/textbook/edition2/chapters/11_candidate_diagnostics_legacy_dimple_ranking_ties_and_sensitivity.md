# 11. Candidate diagnostics, legacy_dimple, ranking, ties, and sensitivity

*Guiding question:* **How should heterogeneous diagnostics be combined without disguising their assumptions?**

Prerequisites: 5,9–10.

## Why the question matters

A deterministic score is reproducible yet remains population-relative and sensitive to component ranges and candidate composition.

`legacy_dimple` uses silhouette and cluster count plus an optional subtracted noise term; DBCV, CH, DB, persistence, and projection diagnostics are not default score components.

This chapter develops the question in the order needed for a reader to move from statistical principle to current implementation, retained evidence, and a defensible statement. Its central worked task is: Compute both Lab 0 score profiles from the three-row candidate table and explain why cluster count dominates when its raw range is larger.

## Learning objectives

After completing Chapter 11, the reader can:

1. define silhouette and explain its role without exceeding the stated caution;
2. define Calinski-Harabasz and explain its role without exceeding the stated caution;
3. define Davies-Bouldin and explain its role without exceeding the stated caution;
4. define DBCV and explain its role without exceeding the stated caution;
5. define trustworthiness and continuity and explain its role without exceeding the stated caution;
6. trace the relevant package functions and generated artifacts;
7. complete the worked task and distinguish observation from interpretation.

## Conceptual and mathematical development

### silhouette

Within-versus-nearest-other-cluster separation under a configured metric. A compact notation is `s(i)=(b(i)-a(i))/max(a(i),b(i))`. In practical terms, freeze 3 can exclude noise and supplies the configured HDBSCAN metric. [@rousseeuw1987]

Within Freeze 3 RC1 the concept is connected to `evaluate_candidate` and is visible through `model_table.csv`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### Calinski-Harabasz

Between-cluster to within-cluster dispersion ratio. A compact notation is `CH=[tr(B)/(k-1)]/[tr(W)/(n-k)]`. In practical terms, the implementation uses non-noise embedded points and Euclidean centroid geometry. [@calinski1974]

Within Freeze 3 RC1 the concept is connected to `evaluate_candidate` and is visible through `model_table.csv`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### Davies-Bouldin

Average worst within/between centroid scatter ratio. A compact notation is `DB=(1/k)sum_i max_(j!=i)(S_i+S_j)/M_ij`. In practical terms, lower is better; Euclidean centroid assumptions can mismatch density geometry. [@davies1979]

Within Freeze 3 RC1 the concept is connected to `evaluate_candidate` and is visible through `model_table.csv`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### DBCV

Density-based validity index. A compact notation is `weighted cluster validity in [-1,1]`. In practical terms, it is optional and supplementary under legacy_dimple, not the default score component. [@moulavi2014dbcv]

Within Freeze 3 RC1 the concept is connected to `evaluate_candidate` and is visible through `model_table.csv`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### trustworthiness and continuity

Directed neighborhood-retention diagnostics. A compact notation is `T(k)=1-c sum_i sum_(j in U_k(i))(r(i,j)-k)`. In practical terms, freeze 3 computes both through directed calls to sklearn trustworthiness under Euclidean geometry. [@venna2010]

Within Freeze 3 RC1 the concept is connected to `embedding_quality_metrics` and is visible through `run_summary.json`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### legacy_dimple score

Population-relative weighted combination of normalized silhouette, clusters, and optionally noise. A compact notation is `raw=w_s s/max(s)+w_k k/max(k)-w_n n/max(n)`. In practical terms, weights are raw dynamic ranges divided by their sum; final scores are min-max scaled.

Within Freeze 3 RC1 the concept is connected to `legacy_dimple_score` and is visible through `scoring_manifest.json; model_table.csv`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### eligibility and ties

Rules deciding which candidates receive scores and stable rank order. A compact notation is `eligible=(status=success) and finite silhouette`. In practical terms, ties resolve deterministically through configured sort keys and candidate identity.

Within Freeze 3 RC1 the concept is connected to `rank_models` and is visible through `ranked_models.csv`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

## Reconstructed operational foundation

Edition 1 contained the following verified operational material in separate short notes. Edition 2 consolidates it here and subjects it to the concept and evidence boundaries above.

### Evidence retained from former Chapter 19

### Operational foundation

Candidate metrics serve different purposes. Topology fields describe non-noise cluster count, noise count/fraction, and cluster sizes. Silhouette uses the configured HDBSCAN metric and the declared sampling scope. DBCV is optionally computed as a density-aware diagnostic. Calinski–Harabasz and Davies–Bouldin are supplied with explicit metric/context fields. HDBSCAN persistence summaries describe retained clusters. Trustworthiness and continuity belong to the embedding family, not to one HDBSCAN extraction.

Metrics can be missing when a topology is invalid, a calculation is undefined, a backend cannot support a metric, or a candidate fails. Read `status`, scope, sampled flags, sample sizes, and `metric_warnings` before comparing numbers. The candidate table is deliberately wide so these qualifications are not hidden.

### Retained evidence

The selected Edition 2 Lab 2 candidate has silhouette about 0.970354 and DBCV about 0.976386, with three equal clusters and no noise. These values describe the designed fixture under Euclidean geometry; they are not expected production targets.

### Output-reading checkpoint

Inspect metric value plus its metric/scope/sampled/sample-size columns, topology counts, persistence, warnings, and the run's compute flags.

### Misinterpretations to avoid

Do not call silhouette inherently Euclidean; Freeze 3 supplies the configured metric. Do not compare a sampled score with a full score without noting scope. Do not call DBCV the universal best metric.

### Boundary inherited from Edition 1

All internal metrics are conditional on representation and candidate population. They lack independent biological evidence and can disagree legitimately.


## Evidence and references

See Rousseeuw (1987), DOI 10.1016/0377-0427(87)90125-7, and Moulavi et al. (2014), DOI 10.1137/1.9781611973440.96.

### Evidence retained from former Chapter 20

### Operational foundation

`legacy_dimple` is the default compatibility score. Among eligible candidates, each included component is divided by its maximum. Its weight is the component's raw observed range divided by the sum of included ranges. Raw score adds normalized silhouette and normalized non-noise cluster count and, only when `fit_include_noise=true`, subtracts normalized noise count. The raw score is finally scaled to [0,1] over the eligible candidate population; a zero range maps to 1.

This is population-relative: adding or removing candidates can change maxima, ranges, weights, and final scores even if an existing candidate's own metrics do not change. DBCV may be present in the table but is not a legacy-score term. No preferred cluster band, noise ceiling, largest-cluster target, or biological label is embedded.

The `custom` profile accepts explicitly declared metric weights and maximize/minimize directions. It should represent a preregistered analytic objective, not weights tuned after viewing a desired partition.

### Retained evidence

In Edition 2 Lab 2, all candidates have the same cluster count and no noise, so UMAP-family silhouette differences drive four score levels and eight-way ties within families. The selection manifest records realized formula and tie order.

### Output-reading checkpoint

Inspect `raw_score`, `score`, compatibility aliases, scoring profile, noise-fit flag, realized weights/ranges, eligible counts, and tie order in `model_selection_manifest.json`.

### Misinterpretations to avoid

Do not say DBCV selected the model when profile is legacy. Do not compare normalized scores across candidate populations as though absolute. Do not introduce outcome-informed custom weights.

### Boundary inherited from Edition 1

A heuristic rank is not a probability, confidence, p-value, or guarantee of stability. Scientific selection should combine transparent objectives, sensitivity, and external evidence.

### Evidence retained from former Chapter 21

### Operational foundation

Ranking begins after statuses and scores exist. Eligible successful rows are ordered by final score descending, raw score descending, then stable `model_id` ascending. `top_models.tsv` retains the requested number; `best_model.json` and the selection manifest identify rank one. Pareto membership and family summaries are supplementary views, not alternate truth labels.

Choosing a model should be traceable to an objective declared before inspecting preferred biological labels. Review failure/invalid rates, parameter-family patterns, tied or near-tied solutions, noise and size trade-offs, stability checks, and domain-independent constraints. A rank-one row is the implementation's selected model under the declared rule, not proof that the cluster count is uniquely correct.

Target leakage includes choosing parameters because their labels resemble a published solution when those parameters were not recovered from the historical method. The 164-IDP manual row-16 selection is disclosed rather than retroactively portrayed as automatic rank one.

## Evidence diagram or figure

```mermaid

flowchart LR
  A["All candidate rows"] --> B["Eligibility + metrics"]
  B --> C["Declared score"]
  C --> D["Rank + tie order"]
  D --> E["best_model.json"]
  E --> F["reproduce-model fixed rerun"]
  F --> G["compare membership and coordinates"]

```



*Scoring, selection, and fixed reproduction. Editable source: `assets/diagrams/diagram_06_selection_reproduction.mmd`.*

### Retained evidence

Edition 2 Lab 2's first eight models tie at score 1 because their HDBSCAN choices yield the same metrics within the best UMAP family. Stable model ID breaks remaining ties; this is an engineering rule, not a biological preference.

### Output-reading checkpoint

Inspect ranked/all/top tables, family summaries, Pareto table, model selection manifest, best-model JSON, failures, and exact parameter records.

### Misinterpretations to avoid

Do not hide ties or failed candidates. Do not select solely from a pretty plot. Do not use knowledge of desired labels to redefine the search or score and then call it replication.

### Boundary inherited from Edition 1

Internal selection uncertainty is not automatically quantified. Report sensitivity and the conditional nature of the chosen population.

### Evidence retained from former Chapter 40

### Operational foundation

The model table is the authoritative candidate ledger. It preserves parameter identity, embedding diagnostics, topology and size summaries, clustering metrics/scopes, persistence, status/errors/runtime/seeds, score values/profile, and rank. Scoring schema normalization supports historical notebook column names while preserving source columns with a `source_` prefix.

`legacy_dimple` uses normalized silhouette and cluster count and optionally subtracts normalized noise. `custom` applies declared weights/directions. Ranking uses score, raw score, and model ID. `family_summaries.tsv` aggregates parameter-family outcomes; `pareto_front.tsv` shows nondominated candidates; neither overrides the selected rule. `score-existing` can rescore a table but cannot recreate embeddings or labels absent from the source artifacts.

A selection audit reports the eligible population, exclusions, failures, metric ranges, realized weights, noise-term switch, ties, selected ID/parameters, and any manual decision.

### Retained evidence

Edition 2 Lab 3 rescored the fixed one-row table. Its zero score range maps the final score to 1 by definition. Edition 2 Lab 2 shows population-relative bands and ties.

### Output-reading checkpoint

Inspect all/ranked/top tables, scoring manifest, model-selection manifest, family/Pareto summaries, best model, source-column migration, and failure table.

### Misinterpretations to avoid

Do not treat one-row score 1 as superior performance. Do not remove failure rows before reporting denominator. Do not confuse Pareto inclusion with validation.

### Boundary inherited from Edition 1

Score normalization can change with the candidate population, and no formula encodes a universal biological optimum. Manual selections require an explicit rationale and status.

## Implementation trace

**`metrics.effective_neighbor_count`** is defined at `dimple_gwas/metrics.py:9` with signature `n_samples: int, requested: int`. Implementation callable for effective neighbor count. It is reached from metrics.embedding_quality_metrics and connects to No package-defined dependency detected. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as tests/test_preprocessing_metrics.py::test_effective_neighbor_edge_cases. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`metrics.embedding_quality_metrics`** is defined at `dimple_gwas/metrics.py:15` with signature `original, embedding, requested_k: int, max_samples: int, seed: int`. Calculate bounded trustworthiness and continuity diagnostics for an embedding. It is reached from interpretation.run_explanation; pipeline.run_search and connects to metrics.effective_neighbor_count. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as tests/test_preprocessing_metrics.py::test_optimized_trustworthiness_and_continuity. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`metrics.evaluate_candidate`** is defined at `dimple_gwas/metrics.py:60` with signature `embedding, labels, clusterer, silhouette_metric: str, fit_include_noise: bool, compute_dbcv: bool, max_samples_silhouette: int=0, silhouette_seed: int=42`. Compute cluster counts, persistence, silhouette, CH, DB, optional DBCV, and validity status for one candidate. It is reached from pipeline._evaluate_one and connects to metrics._cluster_sizes. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`metrics.is_finite_number`** is defined at `dimple_gwas/metrics.py:165` with signature `value: Any`. Implementation callable for is finite number. It is reached from CLI/import/direct caller or no package caller detected and connects to No package-defined dependency detected. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`pipeline.setup_logger`** is defined at `dimple_gwas/pipeline.py:25` with signature `output_dir: str | Path`. Implementation callable for setup logger. It is reached from pipeline.run_search and connects to No package-defined dependency detected. Its direct artifact contract is logs/run.log; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`pipeline.run_search`** is defined at `dimple_gwas/pipeline.py:130` with signature `config: Mapping[str, Any], output_dir: str | Path, command: list[str] | None=None`. Execute preprocessing, repeated embeddings, candidate evaluation, scoring, retention, reporting, and provenance for one run. It is reached from cli._reproduce; cli.main and connects to hdbscan_runner.fit_hdbscan; io.read_table; metrics.embedding_quality_metrics; pipeline._annotation_frame; pipeline._evaluate_one; pipeline._failed_row; pipeline.setup_logger; preprocessing.prepare_analysis_matrix; provenance.base_manifest; provenance.file_record; ranking.family_summaries; ranking.pareto_front; ranking.rank_models; ranking.top_models; reporting.write_model_outputs; reporting.write_resolved_config; reporting.write_search_space; scoring.apply_scoring; search_space.enumerate_candidates; search_space.stable_identifier; umap_runner.run_repeated_umap. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is RuntimeError; ValueError. Test evidence is recorded as tests/test_pipeline_integration.py::test_custom_leaf_eom_metric_and_max_size_run; tests/test_pipeline_integration.py::test_fixed_model_reproduction. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`ranking.rank_models`** is defined at `dimple_gwas/ranking.py:8` with signature `frame`. Apply deterministic eligibility, score, and tie ordering to candidate rows. It is reached from cli._score; cli._summarize; pipeline.run_search and connects to No package-defined dependency detected. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as tests/test_scoring_ranking.py::test_custom_scoring_ranking_top_n_and_pareto. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`ranking.top_models`** is defined at `dimple_gwas/ranking.py:23` with signature `frame, n: int`. Implementation callable for top models. It is reached from cli._summarize; pipeline.run_search and connects to No package-defined dependency detected. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as tests/test_scoring_ranking.py::test_custom_scoring_ranking_top_n_and_pareto. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`ranking.pareto_front`** is defined at `dimple_gwas/ranking.py:27` with signature `frame`. Implementation callable for pareto front. It is reached from cli._summarize; pipeline.run_search and connects to No package-defined dependency detected. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as tests/test_pipeline_integration.py::test_custom_leaf_eom_metric_and_max_size_run; tests/test_scoring_ranking.py::test_custom_scoring_ranking_top_n_and_pareto. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`ranking.family_summaries`** is defined at `dimple_gwas/ranking.py:71` with signature `frame, columns: Iterable[str]=DEFAULT_FAMILY_COLUMNS`. Implementation callable for family summaries. It is reached from cli._summarize; pipeline.run_search and connects to No package-defined dependency detected. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as tests/test_pipeline_integration.py::test_custom_leaf_eom_metric_and_max_size_run. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`scoring.normalize_model_table_schema`** is defined at `dimple_gwas/scoring.py:28` with signature `frame`. Adapt the historical notebook table schema without discarding source fields. It is reached from cli._score and connects to No package-defined dependency detected. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is ValueError. Test evidence is recorded as tests/test_freeze3_comparison_validation.py::test_historical_notebook_model_schema_is_adapted. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`scoring.legacy_dimple_score`** is defined at `dimple_gwas/scoring.py:80` with signature `frame, fit_include_noise: bool=False`. Reproduce the compatibility score using observed dynamic-range weights and population-dependent normalization. It is reached from scoring.apply_scoring and connects to scoring._safe_divide_by_max; scoring._scale_final. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as tests/test_scoring_ranking.py::test_legacy_formula_matches_literal_reference; tests/test_scoring_ranking.py::test_zero_variance_and_noise_exclusion. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

## Claim adjudication notebook

The following statements are admitted to the draft only in their safe form:

- **SCORE-001 (reject):** DBCV is an optional diagnostic; legacy_dimple ranks with normalized silhouette and cluster count and optionally subtracts a noise component. [@moulavi2014dbcv] Limitation: Computing a diagnostic does not make it part of the ranking objective. Implementation evidence: `metrics.py; scoring.py`.

- **SCORE-002 (reject):** Silhouette is defined relative to a distance; Freeze 3 passes the configured HDBSCAN metric to scikit-learn. [@rousseeuw1987] Limitation: Metric choice remains geometry-dependent; CH and DB use Euclidean centroid geometry. Implementation evidence: `metrics.evaluate_candidate`.

- **SCORE-003 (verified):** The default score has no biological label, pQTL target, preferred cluster band, or noise ceiling. Limitation: The population-relative heuristic still embeds trade-offs via ranges. Implementation evidence: `scoring.py; config.py`.

- **HIST-001 (historical_only):** The historical five-cluster solution was manually selected from sorted row 16, not the top automatic score. Limitation: The historical retained table contains 333 successful rows from a theoretical 2,430-candidate grid. Implementation evidence: `historical adapter/docs`.

- **METH-004 (implementation_specific):** Freeze 3 calculates CH and DB on non-noise embedded points using Euclidean centroid geometry; they are supplementary views that may disagree with density-based criteria. [@calinski1974; @davies1979] Limitation: Do not treat agreement as independent evidence after selection. Implementation evidence: `metrics.py`.

- **METH-005 (implementation_specific):** Freeze 3 obtains two directed neighborhood diagnostics by swapping original and projected spaces in sklearn's trustworthiness function. [@venna2010] Limitation: Both are computed with Euclidean geometry and possible sampling. Implementation evidence: `metrics.embedding_quality_metrics`.

## Reading the generated evidence

For Chapter 11, the `Candidate diagnostics, legacy_dimple, ranking, ties, and sensitivity` files are read as a provenance chain rather than as isolated results:

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

The output atlas supplies the complete schemas, checksums, conditions, consumers, and privacy notes for this Chapter 11 route. Native manifests can contain machine paths; the assembled textbook uses sanitized excerpts while restricted evidence retains the original provenance chain.

## Worked reasoning and evidence exercise

Compute both Lab 0 score profiles from the three-row candidate table and explain why cluster count dominates when its raw range is larger.

A complete Chapter 11 answer must expose its intermediate reasoning, name the source or output used for `Candidate diagnostics, legacy_dimple, ranking, ties, and sensitivity`, and finish with separate support and non-support statements. Applying that discipline to the question “How should heterogeneous diagnostics be combined without disguising their assumptions?” prevents a calculation, a software observation, and a scientific interpretation from collapsing into one claim.

## Assumptions, diagnostics, and recovery

The Chapter 11 analysis assumes the stated unit and inputs, the recorded configuration and software identity, and a diagnostic that addresses the claimed property rather than a convenient surrogate. Its decisive boundary is: `legacy_dimple` uses silhouette and cluster count plus an optional subtracted noise term; DBCV, CH, DB, persistence, and projection diagnostics are not default score components.

If the Chapter 11 route fails, retain its log and candidate status before deciding whether the cause is input, configuration, dependency, compute, identifier alignment, or output-root state. Correct an operational failure by writing a new result directory. Treat instability in `Candidate diagnostics, legacy_dimple, ranking, ties, and sensitivity` as sensitivity evidence: report it and identify the independent evidence needed instead of relabeling ambiguity as a software exception.

## Chapter synthesis

A deterministic score is reproducible yet remains population-relative and sensitive to component ranges and candidate composition. The implementation trace makes the current behavior auditable, but the evidence boundary remains part of the result. Chapter 12 freezes one selected model into a replayable artifact and compares results structurally.

## Exercises

1. For `Candidate diagnostics, legacy_dimple, ranking, ties, and sensitivity`, name the unit of analysis and one plausible but invalid substitute.
2. Reconstruct the notation for silhouette; define its dimensions or denominator and interpret every term.
3. Choose a Tier A function mapped to Chapter 11; identify its caller and direct output, then propose a topic-specific edge case.
4. Select one Chapter 11 artifact from the output atlas and state three integrity checks that must precede scientific reading.
5. Convert a tempting `Candidate diagnostics, legacy_dimple, ranking, ties, and sensitivity` overclaim into one observed statement followed by its limitation.
6. Compute both Lab 0 score profiles from the three-row candidate table and explain why cluster count dominates when its raw range is larger.

Appendix J gives the Chapter 11 adjudication guide. Its further-reading keys supply statistical context; no external paper is treated as automatic validation of the current software or dataset.
