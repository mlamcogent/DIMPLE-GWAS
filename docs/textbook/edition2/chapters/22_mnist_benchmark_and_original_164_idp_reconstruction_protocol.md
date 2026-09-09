# 22. MNIST benchmark and original 164-IDP reconstruction protocol

*Guiding question:* **How should public engineering evidence and protected historical scientific evidence coexist in one validation program?**

Prerequisites: 12–21.

## Why the question matters

MNIST can stress software without validating genetics; historical reconstruction can preserve provenance without becoming a fresh run.

MNIST remains protocol-only here. The fresh 164-IDP 1,000-seed run is explicitly deferred until Docker; only historical outputs and acceptance criteria are described.

This chapter develops the question in the order needed for a reader to move from statistical principle to current implementation, retained evidence, and a defensible statement. Its central worked task is: Build a two-column evidence table separating historical reconstruction from fresh computation, including the disclosed row-16 selection and pending Docker requirements.

## Learning objectives

After completing Chapter 22, the reader can:

1. define seed schedule and explain its role without exceeding the stated caution;
2. define adjusted Rand index and explain its role without exceeding the stated caution;
3. define normalized mutual information and explain its role without exceeding the stated caution;
4. define noise Jaccard and explain its role without exceeding the stated caution;
5. define Procrustes disparity and explain its role without exceeding the stated caution;
6. trace the relevant package functions and generated artifacts;
7. complete the worked task and distinguish observation from interpretation.

## Conceptual and mathematical development

### seed schedule

Deterministic list controlling repeated stochastic fits. A compact notation is `legacy: 1,...,S; current: r,...,r+S-1`. In practical terms, recorded seeds permit replay but do not guarantee cross-platform bitwise identity. [@reproduciblesum2015]

Within Freeze 3 RC1 the concept is connected to `ensemble_seeds` and is visible through `embedding_manifest.json`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### adjusted Rand index

Chance-adjusted pairwise partition agreement. A compact notation is `ARI=(RI-E[RI])/(max(RI)-E[RI])`. In practical terms, permutation invariant; a value of 1 does not imply coordinate identity. [@hubert1985]

Within Freeze 3 RC1 the concept is connected to `compare_partitions` and is visible through `comparison_summary.json`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### normalized mutual information

Normalized information shared by two labelings. A compact notation is `NMI=2I(U;V)/(H(U)+H(V))`. In practical terms, normalization conventions matter; Freeze 3 uses the sklearn convention recorded in code. [@vinh2010]

Within Freeze 3 RC1 the concept is connected to `compare_partitions` and is visible through `comparison_summary.json`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### noise Jaccard

Overlap of the two sets labeled -1. A compact notation is `J(A,B)=|A intersect B|/|A union B|`. In practical terms, it isolates agreement about unassigned membership, not all clusters.

Within Freeze 3 RC1 the concept is connected to `noise_jaccard` and is visible through `comparison_summary.json`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### Procrustes disparity

Residual after centering, scaling, and orthogonal alignment. A compact notation is `min_R ||X_c R-Y_c||_F^2`. In practical terms, low disparity supports aligned coordinate similarity under the chosen transformation, not biological replication. [@gower1975]

Within Freeze 3 RC1 the concept is connected to `compare_coordinates` and is visible through `comparison_summary.json`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### validation ladder

Separate software, technical, structural, statistical, biological, external, and cross-platform evidence. A compact notation is `E_software != E_biological`. In practical terms, passing tests or exact fixture replay cannot substitute for external biological validation.

Within Freeze 3 RC1 the concept is connected to `run_validation` and is visible through `validation_report.json`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### floating-point reproducibility

Dependence of finite-precision results on operation order and platform. A compact notation is `fl((a+b)+c) may differ from fl(a+(b+c))`. In practical terms, pinned dependencies improve control but do not guarantee universal bitwise equality. [@reproduciblesum2015]

Within Freeze 3 RC1 the concept is connected to `capture_environment` and is visible through `environment.json`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

## Reconstructed operational foundation

Edition 1 contained the following verified operational material in separate short notes. Edition 2 consolidates it here and subjects it to the concept and evidence boundaries above.

### Evidence retained from former Chapter 35

### Operational foundation

MNIST is a known-label image dataset used here as historical software-benchmark evidence. It tests whether a pipeline can produce and compare structure when class labels exist and inputs are unrelated to GWAS biology. The verified prior benchmark artifacts are retained under the Freeze 3 evidence/quarantine workspace; this manual build did not redownload data or rerun the benchmark. The historical full runtime was 273.47 seconds under its recorded environment and configuration.

A benchmark may report engineering measures such as cluster/label concordance, noise, or runtime. It does not show that genetic association vectors have the same geometry, that IDP clusters are biologically meaningful, or that production resources match. Dataset licensing/acquisition, preprocessing, and environment must travel with any rerun.

Edition 2 Lab 4 is therefore evidence-backed but bounded: it documents the existing verified outputs and the approved rerun path without fabricating fresh results.

### Retained evidence

Read `benchmarks/mnist/MNIST_BENCHMARK_REPORT.md` and `docs/MNIST_BENCHMARK.md`, then locate the historical output checksums in the broader Freeze 3 evidence inventory. Compare every benchmark claim to its manifest.

### Output-reading checkpoint

Inspect acquisition/source note, input shape, known-label mapping, configuration, seeds/threads, cluster/noise metrics, runtime, environment, and artifact hashes.

### Misinterpretations to avoid

Do not present MNIST accuracy as biological validation, a universal runtime, or a production default. Do not fetch new data silently during a reproducibility build.

### Boundary inherited from Edition 1

The benchmark is historical prior evidence in this manual edition. A fresh container benchmark belongs to the Docker stage and must record dataset identity and license.

### Evidence retained from former Chapter 36

### Operational foundation

The original 164-IDP case has two tracks. Track A is historical reconstruction: the authoritative record contains 164 IDPs, 102 HDBSCAN-noise assignments, and five assigned clusters of sizes 9, 13, 15, 14, and 11. The published historical solution used epsilon 0, min-samples 4, and min-cluster-size 6 and was manually selected from sorted row 16—not automatic rank one. One historical `UMAP_3` cell is missing, while labels are complete. Freeze 3 can adapt and rescore the immutable historical artifacts; that is not a new 1,000-seed fit.

Track B is the pending fresh protocol. Use the authoritative input checksum and `configs/original_idp_164_historical_search.yaml`, run `inspect-config` and complete enumeration, preflight storage/threads, then execute standard-scale 1,000 repeated seeds in a new mounted output root inside the later Docker workflow. Preserve source, input, resolved config, command, environment, seeds, thread settings, logs, failures, all candidate rows, retained artifacts, explanation, comparison to historical labels, and validation. Do not tune toward the published labels.

Original material is permitted in the project, but scientific content is provisional because development has advanced; this manual shows aggregate historical counts and protocols rather than claiming a final interpretation.

## Evidence diagram or figure





### Retained evidence

The Edition 2 evidence-status graphic in Chapter 22 separates historical evidence from a prominent fresh-run-pending status. The protocol config and historical selected config are source artifacts; no fresh outputs are implied.

### Output-reading checkpoint

Track A: historical workbook/table, row-16 record, exact label vector, adaptation/rescoring manifests and counts. Track B: authoritative input/config hashes, preflight, complete run, comparison/validation, and Docker platform record.

### Misinterpretations to avoid

Do not say ‘reproduced the 164 analysis’ when only labels were adapted/rescored. Do not choose a new candidate because it most resembles historical labels. Do not fill missing fresh metrics with historical numbers.

### Boundary inherited from Edition 1

The original raw 2,315- and 459-IDP inputs remain incomplete/unresolved in this workspace. Fresh 164 execution and cross-platform acceptance are named release gates.

## Implementation trace

**`comparison.run_comparison`** is defined at `dimple_gwas/comparison.py:65` with signature `left_source: str | Path, right_source: str | Path, output_dir: str | Path, *, id_column: str='feature_id', label_column: str='label', require_same_order: bool=False, command: list[str] | None=None`. Compare two label artifacts using exact IDs, permutation-invariant structure, noise sets, mapping, and optional coordinates. It is reached from cli._compare and connects to comparison._columns; comparison._resolve_labels; comparison._variation_of_information; interpretation.detect_coordinate_columns; interpretation.is_noise_label; interpretation.label_sort_key; io.atomic_json_dump; io.ensure_empty_output_dir; io.json_safe; io.validated_identifiers; provenance.base_manifest; provenance.file_record; provenance.utc_now. Its direct artifact contract is comparison_summary.json; membership_comparison.tsv; cluster_sizes.tsv; label_confusion.tsv; optimal_label_mapping.tsv; comparison_manifest.json; its explicit error surface is ValueError. Test evidence is recorded as tests/test_freeze3_comparison_validation.py::test_comparison_rejects_duplicate_ids; tests/test_freeze3_comparison_validation.py::test_comparison_requires_identical_id_sets; tests/test_freeze3_comparison_validation.py::test_label_permutation_comparison_is_structurally_equal. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`pipeline.setup_logger`** is defined at `dimple_gwas/pipeline.py:25` with signature `output_dir: str | Path`. Implementation callable for setup logger. It is reached from pipeline.run_search and connects to No package-defined dependency detected. Its direct artifact contract is logs/run.log; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`pipeline.run_search`** is defined at `dimple_gwas/pipeline.py:130` with signature `config: Mapping[str, Any], output_dir: str | Path, command: list[str] | None=None`. Execute preprocessing, repeated embeddings, candidate evaluation, scoring, retention, reporting, and provenance for one run. It is reached from cli._reproduce; cli.main and connects to hdbscan_runner.fit_hdbscan; io.read_table; metrics.embedding_quality_metrics; pipeline._annotation_frame; pipeline._evaluate_one; pipeline._failed_row; pipeline.setup_logger; preprocessing.prepare_analysis_matrix; provenance.base_manifest; provenance.file_record; ranking.family_summaries; ranking.pareto_front; ranking.rank_models; ranking.top_models; reporting.write_model_outputs; reporting.write_resolved_config; reporting.write_search_space; scoring.apply_scoring; search_space.enumerate_candidates; search_space.stable_identifier; umap_runner.run_repeated_umap. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is RuntimeError; ValueError. Test evidence is recorded as tests/test_pipeline_integration.py::test_custom_leaf_eom_metric_and_max_size_run; tests/test_pipeline_integration.py::test_fixed_model_reproduction. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`provenance.sha256_file`** is defined at `dimple_gwas/provenance.py:17` with signature `path: str | Path`. Implementation callable for sha256 file. It is reached from interpretation._native_sources; provenance.file_record; reporting._top_artifact; validation.run_validation and connects to No package-defined dependency detected. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as tests/test_failure_and_provenance.py::test_authoritative_source_hash_unchanged. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`provenance.package_versions`** is defined at `dimple_gwas/provenance.py:25` with signature `names: Iterable[str] | None=None`. Implementation callable for package versions. It is reached from provenance.base_manifest and connects to No package-defined dependency detected. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`provenance.utc_now`** is defined at `dimple_gwas/provenance.py:40` with signature `class construction/data container`. Implementation callable for utc now. It is reached from comparison.run_comparison; interpretation.run_explanation; provenance.base_manifest; reporting.write_model_outputs; validation.run_validation and connects to No package-defined dependency detected. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`provenance.file_record`** is defined at `dimple_gwas/provenance.py:44` with signature `path: str | Path`. Implementation callable for file record. It is reached from comparison.run_comparison; interpretation.run_explanation; pipeline.run_search; reporting._top_artifact; reporting.write_model_outputs; validation.run_validation and connects to comparison._columns.<locals>.resolve; provenance.sha256_file. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`provenance.package_source_digest`** is defined at `dimple_gwas/provenance.py:53` with signature `class construction/data container`. Compute a stable hash over package source files for non-Git source identity. It is reached from provenance.base_manifest and connects to comparison._columns.<locals>.resolve. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as tests/test_freeze3_comparison_validation.py::test_package_source_digest_is_stable. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`provenance.base_manifest`** is defined at `dimple_gwas/provenance.py:66` with signature `command: list[str] | None=None`. Implementation callable for base manifest. It is reached from comparison.run_comparison; interpretation.run_explanation; pipeline.run_search; validation.run_validation and connects to provenance.package_source_digest; provenance.package_versions; provenance.utc_now. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`validation.run_validation`** is defined at `dimple_gwas/validation.py:15` with signature `run_dir: str | Path, output_dir: str | Path | None=None, *, command: list[str] | None=None`. Audit a run directory against required files, schemas, counts, identities, hashes, and manifest contracts. It is reached from cli._validate and connects to comparison._columns.<locals>.resolve; io.atomic_json_dump; io.ensure_empty_output_dir; io.json_safe; io.read_model_table; io.read_table; provenance.base_manifest; provenance.file_record; provenance.sha256_file; provenance.utc_now; validation.run_validation.<locals>.record. Its direct artifact contract is validation_checks.tsv; validation_report.json; validation_manifest.json; its explicit error surface is FileNotFoundError. Test evidence is recorded as tests/test_freeze3_comparison_validation.py::test_validation_detects_hash_mismatch; tests/test_freeze3_comparison_validation.py::test_validation_passes_complete_contract. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

## Claim adjudication notebook

The following statements are admitted to the draft only in their safe form:

- **HIST-001 (historical_only):** The historical five-cluster solution was manually selected from sorted row 16, not the top automatic score. Limitation: The historical retained table contains 333 successful rows from a theoretical 2,430-candidate grid. Implementation evidence: `historical adapter/docs`.

- **HIST-002 (reject):** Freeze 3 adapted and rescored immutable historical outputs, but a fresh 1,000-seed 164-IDP fit remains deferred until Docker. Limitation: The book supplies a protocol and acceptance criteria, not fabricated results. Implementation evidence: `original-IDP configs`.

- **HIST-003 (historical_only):** The historical record contains 164 IDPs: 102 noise and five non-noise clusters of 9, 13, 15, 14, and 11. Limitation: Original material may change after current-development adjudication. Implementation evidence: `historical labels`.

## Reading the generated evidence

For Chapter 22, the `MNIST benchmark and original 164-IDP reconstruction protocol` files are read as a provenance chain rather than as isolated results:

| Artifact | Producer | What to verify before interpretation |
| --- | --- | --- |
| `comparison_summary.json` | `run_comparison` | Artifact exists under the new output root, is readable, and its checksum is recorded. |
| `membership_comparison.tsv, cluster_sizes.tsv, label_confusion.tsv, optimal_label_mapping.tsv` | `run_comparison` | Identifiers are unique and exactly match the intended input; label -1 is treated as noise/unassigned. |
| `comparison_manifest.json` | `run_comparison` | Artifact exists under the new output root, is readable, and its checksum is recorded. |
| `validation_checks.tsv` | `run_validation` | Every check is visible; aggregate status matches pass/warn/fail rows; a warning is not silently treated as a pass. |
| `validation_report.json + validation_manifest.json` | `run_validation` | Every check is visible; aggregate status matches pass/warn/fail rows; a warning is not silently treated as a pass. |

The output atlas supplies the complete schemas, checksums, conditions, consumers, and privacy notes for this Chapter 22 route. Native manifests can contain machine paths; the assembled textbook uses sanitized excerpts while restricted evidence retains the original provenance chain.

## Worked reasoning and evidence exercise

Build a two-column evidence table separating historical reconstruction from fresh computation, including the disclosed row-16 selection and pending Docker requirements.

A complete Chapter 22 answer must expose its intermediate reasoning, name the source or output used for `MNIST benchmark and original 164-IDP reconstruction protocol`, and finish with separate support and non-support statements. Applying that discipline to the question “How should public engineering evidence and protected historical scientific evidence coexist in one validation program?” prevents a calculation, a software observation, and a scientific interpretation from collapsing into one claim.

## Assumptions, diagnostics, and recovery

The Chapter 22 analysis assumes the stated unit and inputs, the recorded configuration and software identity, and a diagnostic that addresses the claimed property rather than a convenient surrogate. Its decisive boundary is: MNIST remains protocol-only here. The fresh 164-IDP 1,000-seed run is explicitly deferred until Docker; only historical outputs and acceptance criteria are described.

If the Chapter 22 route fails, retain its log and candidate status before deciding whether the cause is input, configuration, dependency, compute, identifier alignment, or output-root state. Correct an operational failure by writing a new result directory. Treat instability in `MNIST benchmark and original 164-IDP reconstruction protocol` as sensitivity evidence: report it and identify the independent evidence needed instead of relabeling ambiguity as a software exception.

## Chapter synthesis

MNIST can stress software without validating genetics; historical reconstruction can preserve provenance without becoming a fresh run. The implementation trace makes the current behavior auditable, but the evidence boundary remains part of the result. Part V generalizes these examples into a layered validation strategy.

## Exercises

1. For `MNIST benchmark and original 164-IDP reconstruction protocol`, name the unit of analysis and one plausible but invalid substitute.
2. Reconstruct the notation for seed schedule; define its dimensions or denominator and interpret every term.
3. Choose a Tier A function mapped to Chapter 22; identify its caller and direct output, then propose a topic-specific edge case.
4. Select one Chapter 22 artifact from the output atlas and state three integrity checks that must precede scientific reading.
5. Convert a tempting `MNIST benchmark and original 164-IDP reconstruction protocol` overclaim into one observed statement followed by its limitation.
6. Build a two-column evidence table separating historical reconstruction from fresh computation, including the disclosed row-16 selection and pending Docker requirements.

Appendix J gives the Chapter 22 adjudication guide. Its further-reading keys supply statistical context; no external paper is treated as automatic validation of the current software or dataset.
