# 2. GWAS-derived phenotype vectors and high-dimensional geometry

*Guiding question:* **How does a table of association summaries become a geometry among phenotypes?**

Prerequisites: 1.

## Why the question matters

A vector can carry shared biological signal and shared technical or sampling structure at the same time.

DIMPLE-GWAS receives upstream summaries; it does not estimate LD, correct sample overlap, or rerun the contributing GWAS.

This chapter develops the question in the order needed for a reader to move from statistical principle to current implementation, retained evidence, and a defensible statement. Its central worked task is: Use three five-variant vectors to calculate two distances, then identify how a shared scale factor and one outlying variant alter the ordering.

## Learning objectives

After completing Chapter 2, the reader can:

1. define GWAS-derived vector and explain its role without exceeding the stated caution;
2. define identifier alignment and explain its role without exceeding the stated caution;
3. define distance and similarity and explain its role without exceeding the stated caution;
4. define high-dimensional concentration and explain its role without exceeding the stated caution;
5. trace the relevant package functions and generated artifacts;
6. complete the worked task and distinguish observation from interpretation.

## Conceptual and mathematical development

### GWAS-derived vector

Effect estimates or association statistics for one phenotype across matched variants. A compact notation is `X in R^(p x v)`. In practical terms, a vector is a statistical summary, not a person or causal mechanism. [@elliott2018; @buliksullivan2015]

Within Freeze 3 RC1 the concept is connected to `prepare_analysis_matrix` and is visible through `input matrix`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### identifier alignment

A one-to-one correspondence between vector or feature identifiers across artifacts. A compact notation is `I_A = I_B`. In practical terms, order is not identity; normalize and validate keys before joining.

Within Freeze 3 RC1 the concept is connected to `validated_identifiers; align_rows` and is visible through `labels.tsv; coordinates.tsv`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### distance and similarity

Geometry chosen to compare vectors or embedded points. A compact notation is `d_2(x,y)=sqrt(sum_j (x_j-y_j)^2)`. In practical terms, the metric defines which differences count as close. [@aggarwal2001]

Within Freeze 3 RC1 the concept is connected to `evaluate_candidate; compute_similarity` and is visible through `model_table.csv; similarity_matrix.csv`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

### high-dimensional concentration

Relative contrast among common distances can weaken as dimension grows. A compact notation is `contrast=(d_max-d_min)/d_min`. In practical terms, the phenomenon depends on distribution and norm; it is not a universal collapse theorem. [@aggarwal2001]

Within Freeze 3 RC1 the concept is connected to `run_repeated_umap` and is visible through `embedding.npy`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.

## Reconstructed operational foundation

Edition 1 contained the following verified operational material in separate short notes. Edition 2 consolidates it here and subjects it to the concept and evidence boundaries above.

### Evidence retained from former Chapter 2

### Operational foundation

Suppose each phenotype or imaging-derived phenotype (IDP) is represented by association values across a common set of variants. Two vectors can be near one another when their association profiles are similar under the chosen preprocessing and metric. DIMPLE-GWAS asks whether the collection contains density structure that can be summarized as clusters plus unassigned observations.

This framing is deliberately matrix-level. It does not require predefined phenotype groups, but it does require comparable columns: aligned variant rows, consistent alleles and scales upstream, stable identifiers, and an explicit metadata prefix. Shared structure may reflect biology, linkage disequilibrium, sample overlap, technical effects, phenotype construction, or combinations of these. The clustering result begins a scientific investigation; it does not identify which explanation is correct.

### Retained evidence

The synthetic fixture has 80 variant rows, four metadata columns, and 24 trait vectors arranged into three known generator groups. It is useful because shape and expected engineering structure are known, not because it imitates every property of GWAS data.

### Output-reading checkpoint

Inspect the input header and dimensions before any embedding. Later, inspect `labels.tsv` alongside the exact `feature_id` values rather than assuming spreadsheet column order remained unchanged.

### Misinterpretations to avoid

A high original-space correlation is not necessarily a shared mechanism; a visually close 2D point pair is not necessarily close in the full concatenated representation; a cluster is not a set of variants.

### Boundary inherited from Edition 1

Input provenance and upstream QC remain the analyst's responsibility. Freeze 3 verifies numeric shape and identifiers but cannot reconstruct omitted allele harmonization, population structure, covariate design, or study overlap.

### Evidence retained from former Chapter 4

### Operational foundation

The Stage 1 workflow is a producer–consumer chain. Freeze 3 reads the table, removes the declared leading metadata columns, optionally applies RINT to analysis columns, and transposes to vectors by input variables. For each UMAP parameter family it generates repeated seeded UMAP/densMAP embeddings and concatenates them horizontally. It then evaluates the complete declared HDBSCAN Cartesian product, retains success, invalid-topology, and failure rows, calculates diagnostics, applies the declared score, ranks eligible candidates, and refits retained models to preserve labels.

Downstream commands do different work. `reproduce-model` refits one retained parameterization. `explain` does not refit; it matches exact IDs and returns to original input-vector space. `compare` measures structural and optional coordinate concordance. `validate` checks files, schemas, counts, readability, and recorded hashes. No PCA, SVD, or ICA reducer is silently inserted before UMAP.

## Evidence diagram or figure

```mermaid

flowchart LR
  A["Variants × vectors input"] --> B["Drop declared metadata columns"]
  B --> C["Optional RINT"]
  C --> D["Transpose: vectors × variants"]
  D --> E["Repeated seeded UMAP / densMAP"]
  E --> F["Concatenated embedding"]
  F --> G["Enumerated HDBSCAN candidates"]
  G --> H["Metrics and declared score"]
  H --> I["Ranked and retained models"]
  I --> J["Explain / compare / validate"]

```



*Stage 1 producer–consumer workflow. Editable source: `assets/diagrams/diagram_01_stage1_workflow.mmd`.*

### Retained evidence

Follow `assets/diagrams/diagram_01_stage1_workflow.mmd` from input to downstream utilities. Each arrow corresponds to an implementation module named in `evidence/source_to_manual_traceability.tsv`.

### Output-reading checkpoint

At the run root, inspect `resolved_config.yaml`, the search-space manifests, `models/`, `run_manifest.json`, and `logs/run.log`. Appendix D maps every named output to its producer and consumer.

### Misinterpretations to avoid

Do not treat `stage09_*` display coordinates as the full concatenated embedding. Do not expect cleaned inputs or individual repeated embeddings on disk; current Freeze 3 keeps them in memory.

### Boundary inherited from Edition 1

A workflow diagram explains control and data flow, not scientific validity. Every transformation can change geometry, and the selected model remains conditional on the declared search and score.

### Evidence retained from former Chapter 5

### Operational foundation

A GWAS summary statistic is a result indexed by a genetic variant and phenotype. A vector is the ordered set of analysis values for one phenotype across the aligned variant rows. A distance metric maps two vectors—or two embedded observations—to a nonnegative dissimilarity. A partition assigns observations to groups; HDBSCAN may also leave observations unassigned with label `-1`.

Internal clustering metrics summarize geometric properties of the same representation used to fit or assess the partition. Silhouette contrasts an observation's mean within-cluster distance with its nearest other-cluster mean distance. DBCV evaluates density connectedness and separation. Neither asks whether a cluster is biologically meaningful. Projection metrics such as trustworthiness and continuity assess neighborhood preservation, not labels or mechanism.

Pleiotropy is a biological/statistical concept about genetic effects across traits. A density cluster among phenotype vectors can generate hypotheses about shared structure, but cluster membership is not itself proof of pleiotropy or its cause.

### Retained evidence

For three points, compute within- and between-cluster distances under two metrics. The exercise shows why a metric choice is part of the scientific definition of neighborhood rather than a cosmetic option.

### Output-reading checkpoint

Candidate tables contain topology counts, cluster-size summaries, silhouette, DBCV, Calinski–Harabasz, Davies–Bouldin, HDBSCAN persistence, projection metrics, status, warnings, and errors. Check each metric's scope and metric columns.

### Misinterpretations to avoid

Do not compare metric values calculated under undocumented metrics or representations. Do not treat a large score as an external p-value. Do not call every input column a ‘feature’ when the clustered observation is the vector/IDP.

### Boundary inherited from Edition 1

Distance concentration, correlations among variants, scaling, missingness, and finite sample size can alter geometry. Internal metrics can reward a representation-specific structure that fails to reproduce externally.


## Evidence and references

See Rousseeuw (1987), DOI 10.1016/0377-0427(87)90125-7, and Moulavi et al. (2014), DOI 10.1137/1.9781611973440.96.

## Implementation trace

**`io.resolve_separator`** is defined at `dimple_gwas/io.py:10` with signature `path: str | Path, override: str | None=None`. Implementation callable for resolve separator. It is reached from io.read_model_table; io.read_table and connects to No package-defined dependency detected. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`io.read_table`** is defined at `dimple_gwas/io.py:16` with signature `path: str | Path, sep: str | None=None, *, sheet: str | int=0, nrows: int | None=None`. Implementation callable for read table. It is reached from comparison._resolve_labels; interpretation.run_explanation; pipeline._annotation_frame; pipeline.run_search; validation.run_validation and connects to io.resolve_separator. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is FileNotFoundError; RuntimeError. Test evidence is recorded as tests/test_freeze3_interpretation.py::test_reader_supports_excel_sheet. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`io.read_model_table`** is defined at `dimple_gwas/io.py:45` with signature `path: str | Path`. Implementation callable for read model table. It is reached from cli._score; cli._summarize; validation.run_validation and connects to io.resolve_separator. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`io.ensure_empty_output_dir`** is defined at `dimple_gwas/io.py:54` with signature `path: str | Path`. Create an output directory, refusing to mix with existing artifacts. It is reached from comparison.run_comparison; interpretation.run_explanation; validation.run_validation and connects to No package-defined dependency detected. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is ValueError. Test evidence is recorded as tests/test_freeze3_interpretation.py::test_empty_output_directory_helper. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`io.normalize_identifier`** is defined at `dimple_gwas/io.py:68` with signature `value: Any`. Return the exact string identity after removing surrounding whitespace. It is reached from io.validated_identifiers; preprocessing._unique_feature_names; preprocessing.infer_explanation_orientation and connects to No package-defined dependency detected. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`io.validated_identifiers`** is defined at `dimple_gwas/io.py:81` with signature `values, *, context: str`. Normalize identifiers and reject missing or duplicate identities. It is reached from comparison.run_comparison; interpretation._align_inputs; interpretation.run_explanation; preprocessing.infer_explanation_orientation; preprocessing.prepare_explanation_matrix and connects to io.normalize_identifier. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is ValueError. Test evidence is recorded as tests/test_freeze3_interpretation.py::test_validated_identifiers_strip_but_reject_duplicates. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`io.atomic_json_dump`** is defined at `dimple_gwas/io.py:99` with signature `value: Any, path: str | Path`. Implementation callable for atomic json dump. It is reached from cli._score; cli._summarize; comparison.run_comparison; interpretation.run_explanation; reporting._top_artifact; reporting.write_model_outputs; reporting.write_search_space; validation.run_validation and connects to No package-defined dependency detected. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`io.json_safe`** is defined at `dimple_gwas/io.py:109` with signature `value: Any`. Implementation callable for json safe. It is reached from cli._score; cli._show; comparison.run_comparison; interpretation.run_explanation; reporting._top_artifact; reporting.write_model_outputs; reporting.write_search_space; validation.run_validation and connects to No package-defined dependency detected. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`preprocessing.ExplanationMatrix`** is defined at `dimple_gwas/preprocessing.py:12` with signature `class construction/data container`. Implementation callable for ExplanationMatrix. It is reached from preprocessing.prepare_explanation_matrix and connects to No package-defined dependency detected. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is No explicit raise in this symbol; delegated calls may raise.. Test evidence is recorded as No direct symbol-name test reference; assess through caller/integration coverage. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`preprocessing.rank_inverse_normal_transform`** is defined at `dimple_gwas/preprocessing.py:19` with signature `frame`. Apply the implementation's rank-based inverse-normal transform to numeric analysis columns. It is reached from preprocessing.prepare_analysis_matrix; preprocessing.prepare_explanation_matrix and connects to No package-defined dependency detected. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is ValueError. Test evidence is recorded as tests/test_preprocessing_metrics.py::test_rint_and_numeric_matrix. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`preprocessing.prepare_analysis_matrix`** is defined at `dimple_gwas/preprocessing.py:34` with signature `frame, config: Mapping[str, Any]`. Validate the input contract, remove metadata, transform if requested, transpose, and return vector-by-variant analysis data. It is reached from pipeline.run_search and connects to preprocessing.rank_inverse_normal_transform. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is ValueError. Test evidence is recorded as tests/test_preprocessing_metrics.py::test_rint_and_numeric_matrix. This is a A-tier contract, so the complete 20-field dossier is retained in the function atlas.

**`preprocessing.infer_explanation_orientation`** is defined at `dimple_gwas/preprocessing.py:67` with signature `frame, expected_vector_ids, *, drop_first_n_cols: int`. Infer orientation only when one exact ID source is uniquely supported. It is reached from interpretation.run_explanation and connects to io.normalize_identifier; io.validated_identifiers. Its direct artifact contract is No direct canonical artifact; in-memory/supporting result; its explicit error surface is ValueError. Test evidence is recorded as tests/test_freeze3_interpretation.py::test_orientation_inference_uses_exact_overlap. This is a B-tier contract, so the complete 20-field dossier is retained in the function atlas.

## Claim adjudication notebook

The following statements are admitted to the draft only in their safe form:

- **DATA-001 (implementation_specific):** Production input has variants in rows, four declared metadata columns by default, and vector/IDP columns; preprocessing drops the prefix and transposes to vectors by variants. Limitation: Explanation mode also permits an explicit vectors-by-variants orientation. Implementation evidence: `preprocessing.py; io.py`.

- **GWAS-001 (verified_with_qualification):** Vector geometry can reflect shared biology, LD structure, sample overlap, scale, confounding, and preprocessing; DIMPLE-GWAS does not separate these causes. [@buliksullivan2015] Limitation: Interpretation requires upstream harmonization and independent evidence. Implementation evidence: `scope and input only`.

## Worked reasoning and evidence exercise

Use three five-variant vectors to calculate two distances, then identify how a shared scale factor and one outlying variant alter the ordering.

A complete Chapter 2 answer must expose its intermediate reasoning, name the source or output used for `GWAS-derived phenotype vectors and high-dimensional geometry`, and finish with separate support and non-support statements. Applying that discipline to the question “How does a table of association summaries become a geometry among phenotypes?” prevents a calculation, a software observation, and a scientific interpretation from collapsing into one claim.

## Assumptions, diagnostics, and recovery

The Chapter 2 analysis assumes the stated unit and inputs, the recorded configuration and software identity, and a diagnostic that addresses the claimed property rather than a convenient surrogate. Its decisive boundary is: DIMPLE-GWAS receives upstream summaries; it does not estimate LD, correct sample overlap, or rerun the contributing GWAS.

If the Chapter 2 route fails, retain its log and candidate status before deciding whether the cause is input, configuration, dependency, compute, identifier alignment, or output-root state. Correct an operational failure by writing a new result directory. Treat instability in `GWAS-derived phenotype vectors and high-dimensional geometry` as sensitivity evidence: report it and identify the independent evidence needed instead of relabeling ambiguity as a software exception.

## Chapter synthesis

A vector can carry shared biological signal and shared technical or sampling structure at the same time. The implementation trace makes the current behavior auditable, but the evidence boundary remains part of the result. Chapter 3 makes the metric, scaling, and transformation choices explicit.

## Exercises

1. For `GWAS-derived phenotype vectors and high-dimensional geometry`, name the unit of analysis and one plausible but invalid substitute.
2. Reconstruct the notation for GWAS-derived vector; define its dimensions or denominator and interpret every term.
3. Choose a Tier A function mapped to Chapter 2; identify its caller and direct output, then propose a topic-specific edge case.
4. Select one Chapter 2 artifact from the output atlas and state three integrity checks that must precede scientific reading.
5. Convert a tempting `GWAS-derived phenotype vectors and high-dimensional geometry` overclaim into one observed statement followed by its limitation.
6. Use three five-variant vectors to calculate two distances, then identify how a shared scale factor and one outlying variant alter the ordering.

Appendix J gives the Chapter 2 adjudication guide. Its further-reading keys supply statistical context; no external paper is treated as automatic validation of the current software or dataset.
