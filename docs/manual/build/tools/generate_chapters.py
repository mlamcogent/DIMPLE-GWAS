#!/usr/bin/env python3
"""Generate the modular first-draft textbook chapters and appendices."""

from __future__ import annotations

import csv
import json
from pathlib import Path


FREEZE3 = Path(__file__).resolve().parents[4]
MANUAL = FREEZE3 / "docs" / "manual"
CHAPTER_DIR = MANUAL / "chapters"
APPENDIX_DIR = MANUAL / "appendices"
EVIDENCE = MANUAL / "evidence"


def detail(core: str, example: str, outputs: str, mistakes: str, limitations: str, check: str, references: str = "") -> dict[str, str]:
    return {"core": core, "example": example, "outputs": outputs, "mistakes": mistakes, "limitations": limitations, "check": check, "references": references}


DETAILS: dict[int, dict[str, str]] = {}

DETAILS.update({
    1: detail(
        "DIMPLE-GWAS Stage 1 groups phenotype-associated vectors according to structure in their genetic association profiles. It accepts a variant-by-vector matrix, creates a nonlinear representation, fits density-based partitions, ranks declared candidates, and preserves selected labels and provenance. It does not run a GWAS, identify causal variants, perform enrichment, fine mapping, PRS, QTL analysis, Genomic SEM, genomic PCA/ICA, MTAG, PLEIO, or MOSTest. Those may be upstream, downstream, or comparator methods, but they are not hidden Freeze 3 features.\n\nThe unit clustered is a vector/IDP, not a person and not a variant. A cluster is an algorithmic grouping conditional on input construction, preprocessing, metric, embedding parameters, seeds, HDBSCAN settings, candidate population, and selection rule. Treat it as a testable descriptive structure rather than a biological truth label.",
        "Read `pyproject.toml`, run `dimple-gwas --version`, and inspect `evidence/software_truth_report.md`. All identify package `3.0.0rc1`; the evidence report also names pending scientific and cross-platform gates.",
        "Start with `run_manifest.json`, `models/model_selection_manifest.json`, retained `labels.tsv`, and the claim/evidence register. Together they answer what was run, what was selected, and how strongly it may be interpreted.",
        "Do not describe the software as a multivariate association test or an automatic biological-discovery engine. Do not collapse Stage 1 clustering and later scientific validation into one claim.",
        "The current build proves local software behavior and bounded fixture reproduction. It does not prove that any real-data cluster is stable, causal, clinically useful, or externally replicated.",
        "In one sentence, name the clustered unit, the implemented output, and one task the software does not perform. Then label the release correctly as RC1.",
    ),
    2: detail(
        "Suppose each phenotype or imaging-derived phenotype (IDP) is represented by association values across a common set of variants. Two vectors can be near one another when their association profiles are similar under the chosen preprocessing and metric. DIMPLE-GWAS asks whether the collection contains density structure that can be summarized as clusters plus unassigned observations.\n\nThis framing is deliberately matrix-level. It does not require predefined phenotype groups, but it does require comparable columns: aligned variant rows, consistent alleles and scales upstream, stable identifiers, and an explicit metadata prefix. Shared structure may reflect biology, linkage disequilibrium, sample overlap, technical effects, phenotype construction, or combinations of these. The clustering result begins a scientific investigation; it does not identify which explanation is correct.",
        "The synthetic fixture has 80 variant rows, four metadata columns, and 24 trait vectors arranged into three known generator groups. It is useful because shape and expected engineering structure are known, not because it imitates every property of GWAS data.",
        "Inspect the input header and dimensions before any embedding. Later, inspect `labels.tsv` alongside the exact `feature_id` values rather than assuming spreadsheet column order remained unchanged.",
        "A high original-space correlation is not necessarily a shared mechanism; a visually close 2D point pair is not necessarily close in the full concatenated representation; a cluster is not a set of variants.",
        "Input provenance and upstream QC remain the analyst's responsibility. Freeze 3 verifies numeric shape and identifiers but cannot reconstruct omitted allele harmonization, population structure, covariate design, or study overlap.",
        "Sketch a 6-variant by 3-vector table. Mark the variant axis, vector axis, metadata prefix, and the unit that becomes one HDBSCAN observation.",
    ),
    3: detail(
        "Release language is an evidence statement. ‘Software-complete RC1’ means the intended commands and local contracts are present and the bounded test evidence passes. ‘Scientifically frozen’ would additionally require the agreed full scientific reconstruction and resolution of material scientific issues. ‘Cross-platform validated’ would require evidenced execution and comparison on the target Docker/Linux/cloud platforms.\n\nFreeze 3 therefore has four evidence classes: fresh local evidence; historical-only evidence; protocol-only pending work; and out-of-scope methods. The 45-test result and synthetic tutorials are fresh local evidence. Historical 164-IDP counts and the manual row-16 selection are historical. The fresh 1,000-seed 164-IDP run and Docker/GCP/AWS work are pending. Stage 2 and other association tools are outside the executable core.",
        "Use Appendix G as a validation matrix. Notice that a pass at the software layer does not change the pending status of biological or cross-platform validation.",
        "The environment snapshot, missing-evidence register, test report, tutorial manifests, and Docker handoff are the release-status evidence set.",
        "Avoid ‘fully reproducible,’ ‘platform independent,’ ‘Freeze 3 final,’ or ‘validated’ without naming the validation layer and platform. Do not use historical adaptation as shorthand for a fresh rerun.",
        "This status can change only when new artifacts directly meet a named gate. Editorial confidence or dependency pinning cannot substitute for execution evidence.",
        "Classify each statement—‘45 tests passed,’ ‘five historical clusters,’ ‘works on AWS,’ and ‘biologically distinct’—as fresh, historical, pending, or unsupported.",
    ),
    4: detail(
        "The Stage 1 workflow is a producer–consumer chain. Freeze 3 reads the table, removes the declared leading metadata columns, optionally applies RINT to analysis columns, and transposes to vectors by input variables. For each UMAP parameter family it generates repeated seeded UMAP/densMAP embeddings and concatenates them horizontally. It then evaluates the complete declared HDBSCAN Cartesian product, retains success, invalid-topology, and failure rows, calculates diagnostics, applies the declared score, ranks eligible candidates, and refits retained models to preserve labels.\n\nDownstream commands do different work. `reproduce-model` refits one retained parameterization. `explain` does not refit; it matches exact IDs and returns to original input-vector space. `compare` measures structural and optional coordinate concordance. `validate` checks files, schemas, counts, readability, and recorded hashes. No PCA, SVD, or ICA reducer is silently inserted before UMAP.",
        "Follow `assets/diagrams/diagram_01_stage1_workflow.mmd` from input to downstream utilities. Each arrow corresponds to an implementation module named in `evidence/source_to_manual_traceability.tsv`.",
        "At the run root, inspect `resolved_config.yaml`, the search-space manifests, `models/`, `run_manifest.json`, and `logs/run.log`. Chapter 41 maps every named output to its producer and consumer.",
        "Do not treat `stage09_*` display coordinates as the full concatenated embedding. Do not expect cleaned inputs or individual repeated embeddings on disk; current Freeze 3 keeps them in memory.",
        "A workflow diagram explains control and data flow, not scientific validity. Every transformation can change geometry, and the selected model remains conditional on the declared search and score.",
        "Given an artifact name, identify its producer and whether it refits data. Verify your answer in `output_producer_consumer_map.tsv`.",
    ),
    5: detail(
        "A GWAS summary statistic is a result indexed by a genetic variant and phenotype. A vector is the ordered set of analysis values for one phenotype across the aligned variant rows. A distance metric maps two vectors—or two embedded observations—to a nonnegative dissimilarity. A partition assigns observations to groups; HDBSCAN may also leave observations unassigned with label `-1`.\n\nInternal clustering metrics summarize geometric properties of the same representation used to fit or assess the partition. Silhouette contrasts an observation's mean within-cluster distance with its nearest other-cluster mean distance. DBCV evaluates density connectedness and separation. Neither asks whether a cluster is biologically meaningful. Projection metrics such as trustworthiness and continuity assess neighborhood preservation, not labels or mechanism.\n\nPleiotropy is a biological/statistical concept about genetic effects across traits. A density cluster among phenotype vectors can generate hypotheses about shared structure, but cluster membership is not itself proof of pleiotropy or its cause.",
        "For three points, compute within- and between-cluster distances under two metrics. The exercise shows why a metric choice is part of the scientific definition of neighborhood rather than a cosmetic option.",
        "Candidate tables contain topology counts, cluster-size summaries, silhouette, DBCV, Calinski–Harabasz, Davies–Bouldin, HDBSCAN persistence, projection metrics, status, warnings, and errors. Check each metric's scope and metric columns.",
        "Do not compare metric values calculated under undocumented metrics or representations. Do not treat a large score as an external p-value. Do not call every input column a ‘feature’ when the clustered observation is the vector/IDP.",
        "Distance concentration, correlations among variants, scaling, missingness, and finite sample size can alter geometry. Internal metrics can reward a representation-specific structure that fails to reproduce externally.",
        "Define vector, metric, partition, candidate model, and noise label without using any biological conclusion in the definition.",
        "See Rousseeuw (1987), DOI 10.1016/0377-0427(87)90125-7, and Moulavi et al. (2014), DOI 10.1137/1.9781611973440.96.",
    ),
    6: detail(
        "UMAP is a nonlinear neighborhood-based embedding method; densMAP augments its objective to encourage correspondence in local density. DIMPLE-GWAS repeats seeded embeddings because one stochastic optimization can be sensitive to initialization. It concatenates the repeated coordinates so HDBSCAN receives information from all executed repeats. Density clustering is attractive because it can represent irregular clusters and explicitly leave low-density observations unassigned.\n\nThe rationale is empirical, not a mathematical guarantee. Concatenation does not prove that stochasticity has vanished, that Euclidean distances estimate an exact expectation, that ‘true topology’ has been recovered, or that a formal consensus partition has been computed. Base parameters, number and sequence of seeds, implementation versions, numerical libraries, hardware, threads, and the input matrix all remain part of the result.",
        "Tutorial 1 uses one repeated seed for speed; Tutorial 2 uses two. The production standard declares 1,000. These are tutorial value, tutorial value, and configuration default—not interchangeable recommendations.",
        "Inspect the resolved UMAP parameters, `random_seeds`, package versions, thread settings, projection-quality fields, and HDBSCAN metric in the manifest/candidate table.",
        "Do not interpret a clean 2D plot as proof that the concatenated representation is stable. Do not increase repeats without estimating compute and storage consequences. Do not call label `-1` a failed phenotype.",
        "Nonlinear embeddings can distort global distances, and density clustering is parameter dependent. Empirical stability should be assessed across justified perturbations and, for scientific conclusions, external or held-out evidence.",
        "Explain in two sentences why repeats are used and then name three guarantees the implementation does not make.",
        "See McInnes et al. (2018), DOI 10.21105/joss.00861; Narayan et al. (2021), DOI 10.1038/s41587-020-00801-7; and Campello et al. (2015), DOI 10.1145/2733381.",
    ),
    7: detail(
        "Methods are comparable only after their questions and outputs are aligned. PCA provides orthogonal linear variance components and loadings; ICA seeks statistically independent linear components; k-means creates exhaustive centroid-based groups; hierarchical clustering supplies a nested grouping; mixture models provide probabilistic components. UMAP is a representation method, while HDBSCAN is the clustering stage. DBCV is a diagnostic, not a clustering algorithm.\n\nGenomic SEM models multivariate genetic covariance, MTAG estimates trait-specific multi-trait associations, PLEIO provides joint pleiotropic-locus tests, and MOSTest is an omnibus multivariate association approach. These methods do not all accept the same inputs or return the same scientific object as DIMPLE-GWAS. They may be alternatives for a different question or complementary stages, but they are not implemented by Freeze 3.\n\nNo method is universally ‘completely ineffective.’ PCA/ICA components can be useful and reproducible without becoming automatically causal biological mechanisms.",
        "Use `evidence/comparator_matrix.tsv` to select a method for three questions: reduce a matrix linearly, identify omnibus associated loci, and cluster phenotype vectors with an unassigned-noise option.",
        "The comparator matrix records purpose, input, output, assumptions, noise handling, interpretability, strengths, limitations, relationship to DIMPLE-GWAS, and implementation status.",
        "Do not rank unlike methods with a single ‘best’ score. Do not imply that the manual executed a comparator marked `implemented_in_freeze3=no`. Correctly attribute the genomic PCA/ICA paper to Oblong et al., not to an inferred reviewer author.",
        "Conceptual comparisons do not establish empirical superiority. A fair benchmark would need common data, preregistered objectives, suitable metrics, and evidence for each implementation.",
        "For one planned analysis, write the input, desired output, and validation target before naming a method.",
        "See Oblong et al. (2024), DOI 10.1111/gbb.12876; Grotzinger et al. (2019), DOI 10.1038/s41562-019-0566-x; MTAG DOI 10.1038/s41588-017-0009-4; MOSTest DOI 10.1038/s41467-020-17368-1; and PLEIO DOI 10.1016/j.ajhg.2020.11.017.",
    ),
    8: detail(
        "When the same data choose a representation, select a partition, and then supply the evidence used to declare that partition meaningful, naive inferential statements can be circular. Internal scores are useful for navigation within a declared candidate population, but they do not become independent hypothesis tests. Original-space correlations computed after selecting labels are descriptive conditional summaries.\n\nA validation ladder keeps claims calibrated. Software validation checks code contracts. Technical validation checks whether an analysis and its artifacts can be rerun or compared under stated conditions. Statistical validation studies stability, uncertainty, multiplicity, and selection. Biological validation uses independent data, domain evidence, or an appropriately designed external analysis. Cross-platform validation tests the packaged workflow on the claimed systems.\n\nThe safe pattern is: describe what was selected and why, report sensitivity and uncertainty, reserve inferential claims for methods that address the selection process, and seek held-out or independent validation.",
        "The synthetic comparison has ARI=NMI=noise Jaccard=mapped membership=1. That establishes bounded structural concordance for the fixture; it does not validate the biological interpretation of real IDPs.",
        "Inspect the score/selection manifest, comparison summary, validation report, exclusions, and any independent validation artifacts. Record which validation layer each supports.",
        "Do not perform an ANOVA on the same matrix and labels and present the p-value as independent cluster confirmation. Do not turn an internal score into biological effect size or uncertainty.",
        "Selective-inference literature establishes the general problem, but the cited hierarchical-clustering procedure is not a turnkey inferential solution for the complete UMAP+HDBSCAN selection pipeline.",
        "Rewrite ‘clusters were validated by strong within-cluster correlations’ so that it is accurate, conditional, and descriptive.",
        "See Gao, Bien & Witten (2024), DOI 10.1080/01621459.2022.2116331. The scope difference from DIMPLE-GWAS is explicit.",
    ),
})

DETAILS.update({
    37: detail(
        "The entry point is `dimple-gwas`; `python -m dimple_gwas` is equivalent. `run` fits the declared UMAP/HDBSCAN search. `inspect-config` resolves/validates settings. `show-search-space` enumerates without fitting. `score-existing` applies a declared score to a native or adapted historical table. `summarize-models` creates family/Pareto/top summaries. `reproduce-model` refits one retained parameterization. `explain` (alias `interpret`) summarizes retained labels in original space without refitting. `compare` compares exact-ID artifacts. `validate` checks a run contract and hashes.\n\nUse `dimple-gwas COMMAND --help` as the runtime authority. Common run precedence is `--search-mode`, optional `--config`, then explicit input/UMAP/HDBSCAN/execution/scoring overrides. Run aliases support selected Dev spellings, but new work should prefer canonical hyphenated flags. Downstream commands have their own required inputs; they do not inherit a current run implicitly.\n\nMinimal patterns:\n\n```bash\ndimple-gwas inspect-config --search-mode MODE --config CONFIG.yaml\ndimple-gwas show-search-space --search-mode MODE --config CONFIG.yaml --output-dir NEW_DIR\ndimple-gwas run --search-mode MODE --config CONFIG.yaml --output-dir NEW_DIR\ndimple-gwas score-existing --models TABLE --output SCORED.tsv\ndimple-gwas summarize-models --models TABLE --output-dir NEW_DIR\ndimple-gwas reproduce-model --model-json SUMMARY.json --output-dir NEW_DIR\ndimple-gwas explain --model-json SUMMARY.json --output-dir NEW_DIR\ndimple-gwas compare --left A --right B --output-dir NEW_DIR\ndimple-gwas validate --run-dir RUN --output-dir NEW_DIR\n```",
        "All top-level and subcommand help text was freshly captured in `build/logs/cli_help/`. The implementation-derived matrix has one row per action, flag alias, destination, default, choice, requirement, help text, and source.",
        "Inspect `evidence/command_and_flag_matrix.tsv` for the complete flag list and captured help for formatting. Then verify output effects in the producer–consumer map.",
        "Do not assume a flag accepted by `run` is accepted by `explain`. Do not omit required output roots. Do not rely on an alias when publishing a new canonical protocol without documenting it.",
        "CLI `--help` proves interface availability, not scientific appropriateness. Some options can create very large searches or expose private paths in manifests.",
        "For each command, state whether it fits UMAP/HDBSCAN, reads an existing model table, and writes a new directory or file.",
    ),
    38: detail(
        "Configuration has seven top-level groups. `input` contains path, metadata-prefix count, separator, transform, and annotation join. `umap` contains twelve searchable embedding fields. `hdbscan` contains nine searchable density-clustering fields. `execution` contains repeats, threads, retention, safeguards, subsampling, seed, Parquet, DBCV, and strictness. `scoring` selects legacy/custom behavior. `interpretation` controls original-space similarity, order, noise, matching, figure safeguards, and optional coordinate associations. `search_mode` chooses the built-in base.\n\nStandard defaults include four metadata columns, no transform, UMAP neighbors 30/min-dist 0/three components/Euclidean/densMAP true/base seed 42, HDBSCAN min-cluster-size 5:50, min-samples 2:20, epsilon 0:3, EOM/Euclidean, 1,000 repeats, `n_jobs=-1`, one candidate job, 20 retained models, DBCV and Parquet enabled, non-strict execution, legacy score excluding noise, and Pearson cluster-then-hclust explanation with exact matching. Stop values are exclusive.\n\nValidation enforces finite values, supported metrics, min-dist≤spread, positive rates/sizes, EOM/leaf, valid maximum sizes, nonzero candidate jobs, valid score rules, and enumerated interpretation choices. The complete exact default/value reference is generated from source into `configuration_key_reference.tsv`.",
        "Run `inspect-config` for standard, extended, fixed, and the tutorial custom YAML, then diff only the resolved values. This distinguishes mode defaults from overlays.",
        "Inspect source YAML, resolved YAML, configuration hash, config-reference row, CLI exposure, validation errors, and search count.",
        "Do not infer a default from an example. Do not forget that `max_cluster_size` is EOM-specific. Do not enable coordinate associations or large matrices without acknowledging their output and privacy cost.",
        "The package validates syntax/ranges, not scientific choice. A permitted metric or parameter range may still be inappropriate for a specific data-generating process.",
        "Choose five keys and label each value in a report as default, tutorial, historical, or recommendation.",
    ),
    39: detail(
        "Freeze 3 enumerates the full Cartesian product of normalized UMAP and HDBSCAN parameter values. Candidate ordinals and stable hashes make enumeration auditable. It does not silently sample. `execution.max_candidate_models` is a hard safety ceiling; zero means unlimited. `warn_candidate_count` is a warning threshold.\n\nMode counts in this source are: standard 2,430 candidates (one UMAP family × 45 × 18 × 3 HDBSCAN values); fixed one candidate when all searched fields are scalar; Tutorial 2 custom 32; shipped extended 1,728. Extended crosses multiple UMAP and HDBSCAN fields, and its count must be derived from the current source rather than older planning documents.\n\nSearch work can reuse one repeated embedding across many HDBSCAN candidates sharing `umap_id`. Therefore candidate count, UMAP-family count, repeat count, sample/vector count, input width, metric, and thread settings all matter.",
        "`show-search-space` writes the full flattened rows plus JSON counts. Compare the number of unique `umap_id` and `hdbscan_id` values with total candidate rows.",
        "Inspect candidate ordinal/model/family IDs, every flattened parameter, declared enumeration note, safety settings, and checksum.",
        "Do not multiply only visibly changed YAML keys while ignoring inherited lists. Do not describe a truncated preview as the full manifest. Do not change the grid after examining desired labels without disclosure.",
        "Enumeration completeness is a software property, not a claim that the grid covers all meaningful models or that rank one is unique.",
        "Derive the standard and Tutorial 2 counts by hand and reconcile them with manifests; then calculate UMAP fit count separately.",
    ),
    40: detail(
        "The model table is the authoritative candidate ledger. It preserves parameter identity, embedding diagnostics, topology and size summaries, clustering metrics/scopes, persistence, status/errors/runtime/seeds, score values/profile, and rank. Scoring schema normalization supports historical notebook column names while preserving source columns with a `source_` prefix.\n\n`legacy_dimple` uses normalized silhouette and cluster count and optionally subtracts normalized noise. `custom` applies declared weights/directions. Ranking uses score, raw score, and model ID. `family_summaries.tsv` aggregates parameter-family outcomes; `pareto_front.tsv` shows nondominated candidates; neither overrides the selected rule. `score-existing` can rescore a table but cannot recreate embeddings or labels absent from the source artifacts.\n\nA selection audit reports the eligible population, exclusions, failures, metric ranges, realized weights, noise-term switch, ties, selected ID/parameters, and any manual decision.",
        "Tutorial 3 rescored the fixed one-row table. Its zero score range maps the final score to 1 by definition. Tutorial 2 shows population-relative bands and ties.",
        "Inspect all/ranked/top tables, scoring manifest, model-selection manifest, family/Pareto summaries, best model, source-column migration, and failure table.",
        "Do not treat one-row score 1 as superior performance. Do not remove failure rows before reporting denominator. Do not confuse Pareto inclusion with validation.",
        "Score normalization can change with the candidate population, and no formula encodes a universal biological optimum. Manual selections require an explicit rationale and status.",
        "Audit one selected model from raw metrics through normalized components, weight realization, tie order, and retained JSON.",
    ),
    41: detail(
        "The output atlas classifies 35 produced artifact patterns plus three important non-artifacts. Run-root contracts are `resolved_config.yaml`, search manifests, `run_manifest.json`, and logs. Candidate/model contracts live in `models/`: all/ranked/top tables, optional Parquet, best/selection JSON, Pareto/family summaries, and per-retained-model labels/summary/reproduction YAML. Compatibility aliases use `stage02`, `stage03`, and `stage09` names.\n\nDownstream families are separate: scoring creates a table plus manifest; summarization creates family/Pareto/top/count files; explanation creates similarity/order/cutpoint/summary/projection/association/exclusion/heatmap/manifest/README artifacts; comparison creates summary, membership, sizes, confusion, mapping, and manifest; validation creates check rows, report, and manifest.\n\nCurrent Freeze 3 does **not** write the cleaned/transformed input, individual repeated embeddings, or full concatenated embedding. They are in-memory intermediates. Selected display coordinates are not the full concatenated representation. The machine-readable `output_atlas.tsv` records producer, condition, format, schema excerpt, identifiers, label convention, ordering, safe inspection, health checks, consumers, authority, privacy, example, checksum, and verification status for every item.",
        "Use Tutorial 2 for run artifacts and Tutorial 3 for downstream artifacts. Each verified atlas example has a SHA-256 and software version. Optional coordinate associations are correctly marked not executed.",
        "For every artifact: confirm producer, creation condition, encoding, row/key schema, identifier uniqueness, label `-1`, rank/order semantics, status/missingness, consumer, privacy, and checksum.",
        "Do not hunt for nonexistent embedding files. Do not read CSV aliases when the native TSV/JSON contract is needed. Do not publish logs/manifests without reviewing paths and study identifiers.",
        "Exact candidate-table columns are authoritative in the actual header. Future source changes require regenerating the atlas before updating prose.",
        "Select one artifact from each family—run, model, explain, compare, validate—and verify it against its atlas row and tutorial checksum.",
    ),
    42: detail(
        "A reproducible run is a chain of identities and decisions: source hash/version; input path/size/hash and upstream provenance; source and resolved configuration/hash; exact command; Python/platform/package versions; backends; seeds; threads; timestamps/runtime; candidate counts/statuses; selected model and formula; every artifact hash; warnings/exclusions/failures; and comparison criteria. `run_manifest.json` captures much of this; tutorial execution manifests and checksum tables close the documentation chain.\n\nExact comparison is appropriate for bytes, schemas, IDs, declared parameters, counts, and sometimes labels. Tolerances or invariant metrics are appropriate for floating-point metrics and aligned embeddings across platforms. Plots should be compared through source tables and structural/render checks, not byte identity alone. Dependency pinning improves traceability but cannot guarantee identical numerics across OS, architecture, hardware, BLAS/OpenMP, threads, or compiler/runtime versions.\n\nWith no Git metadata in this snapshot, use the package-source SHA-256 and complete file registers; the Docker stage should establish a versioned source identity.",
        "The executed Tutorial 2 manifest records package-source and input hashes, configuration hash, exact package versions, seeds 42/43, jobs, backend names, runtime, counts, selected ID, and artifact hashes.",
        "Inspect runtime environment, resolved dependencies, source/input/artifact checksum registers, run/selection/tutorial manifests, logs, comparison and validation evidence.",
        "Do not equate a pinned requirements file with a complete environment. Do not compare floating-point PNG bytes as scientific equality. Do not sanitize the only retained provenance copy.",
        "Provenance can contain protected paths and identifiers; maintain a private complete record and a deliberately sanitized publication record with linked hashes.",
        "Using `assets/diagrams/diagram_09_provenance_lineage.mmd`, trace one plotted value back to its source table, configuration, input, source code, and execution log.",
    ),
    43: detail(
        "Troubleshoot by preserving evidence and narrowing the contract. Configuration errors include unknown keys, invalid metrics/ranges, custom mode without YAML, list values in fixed mode, min-dist greater than spread, invalid sizes, or a zero candidate job. Input errors include missing path, separator mistakes, nonnumeric analysis columns, wrong metadata-prefix count, duplicate/whitespace IDs, ambiguous orientation, missing labels, or undefined correlations. Execution issues include large candidate/repeat counts, backend errors, invalid topologies, optional Parquet failure, annotations skipped, and nonempty output roots for commands that require an absent/empty directory. Validation can flag missing files, unreadable schemas, count mismatch, or hash mismatch.\n\nRecovery order: copy the exact error and command; inspect the log/manifest; run `inspect-config`; run `show-search-space`; verify input header/dimensions/IDs/checksum; reproduce on the fixed fixture; reduce only explicitly safe compute settings in a new config; create a new output root; and keep the failed candidate/run evidence. Use `--strict` when a workflow must abort on candidate failures, understanding the operational consequence.\n\nA code defect should be documented with the smallest reproducer; do not edit scientific code just to make prose pass.",
        "Tutorial 1's annotation warning was resolved by inspecting the annotation header (`index`), correcting YAML, and rerunning to a new directory. No historical output was overwritten.",
        "Inspect stderr/stdout capture, `logs/run.log`, `model_failures.tsv`, status/error/warning columns, resolved config, input contract, issue register, and validation checks.",
        "Do not delete a failed output before recording it. Do not set `undefined_correlation=zero` merely to suppress an unexplained constant vector. Do not increase parallelism as the first remedy for memory pressure.",
        "Not every warning invalidates clustering; not every exit-zero run is scientifically acceptable. Classify impact and resolution explicitly.",
        "Diagnose: annotation skipped, candidate count unexpectedly 100× larger, duplicate ID, and validation hash mismatch. For each, name the first read-only check.",
    ),
    44: detail(
        "Workload has two nested scales: UMAP families × repeated seeds, then HDBSCAN candidates per family. Concatenated width is components × repeats; embedding storage in memory grows with vector count and that width. Original-space explanation may create a quadratic vector-by-vector similarity matrix and large heatmap. Candidate tables grow with the Cartesian product. JIT compilation makes first small runs slower than steady-state work.\n\nUse `inspect-config`/`show-search-space` before execution. Start with the fixed fixture, then a bounded scientific pilot that preserves the intended method. Set `n_jobs` and `candidate_jobs` deliberately: when candidates run in parallel, Freeze 3 constrains HDBSCAN core-distance jobs to one to avoid nested oversubscription. Thread environment variables and numerical backends belong in provenance. Use the full-heatmap limit and avoid forcing large matrices without memory/privacy review.\n\nThe historical note records a 16-GB host caution. Current storage had ample space, but that is not a production resource recommendation. The executed 10.7-second/32-candidate and 273.47-second historical MNIST values are configuration-specific evidence, not scaling laws.",
        "Estimate candidate count, UMAP-family count, concatenated width, model-table rows, and similarity-matrix cells for a proposed run. Then compare available memory/storage and choose one job setting before starting.",
        "Inspect preflight counts, free storage, vector/input width, repeat/component counts, jobs/threads, UMAP/candidate runtimes, failure rates, Parquet status, and explanation matrix safeguards.",
        "Do not run the 164 1,000-seed workflow as an undocumented first smoke test. Do not set both job layers to unrestricted parallelism. Do not infer linear runtime from tiny fixtures.",
        "No fresh full-IDP runtime/memory benchmark exists yet. Docker profiling must precede cloud sizing and preserve scientific settings.",
        "Create a bounded-run worksheet with exact formulas and mark every quantity measured, configured, or still unknown.",
    ),
    45: detail(
        "Freeze 3 retains selected legacy CLI aliases and stage filenames so existing users can transition, but its native contracts are manifests, TSV/JSON model tables, stable IDs, per-model summaries, and explicit downstream utilities. Historical notebook columns such as `Silhouette_avg`, `Clusters`, `Noise_points`, `Epsilon`, `Min_samples`, and `Min_cluster_size` can be normalized by `score-existing`; source score columns are preserved with `source_` prefixes.\n\nMigration should preserve the historical environment/configuration and labels before adaptation. Map old flags to canonical names, inspect the resolved Freeze 3 config, enumerate counts, rescore without refitting, compare exact IDs and permutation-invariant labels, and only then decide whether a fresh fixed/full run is authorized. Compatibility aliases do not prove that the new implementation recreated every intermediate byte.\n\nThe default path still matches the declared Dev-style standard search where verified, but Freeze 3 adds comprehensive manifests, failures, metrics/scopes, stable artifacts, explanation, comparison, and validation. Shipped extended count is 1,728, so older 5,184 planning statements must not migrate into new reports.",
        "Use the historical 164 adapter as the pattern: immutable historical rows/labels are read, canonical score behavior is applied, manual row-16 status remains explicit, and fresh execution is not implied.",
        "Inspect migration/backward-compatibility docs, alias help, schema-migration manifest, source-prefixed columns, historical checksums, comparison metrics, and new provenance.",
        "Do not rewrite historical spreadsheets in place. Do not call an adapted table a fresh model fit. Do not assume stage aliases contain every new native field.",
        "Some original inputs/parameters remain missing or ambiguous; those migrations stay historical-only until authoritative evidence is supplied.",
        "Build a two-column legacy-to-native map for one run and mark each item exact, adapted, deprecated alias, or unavailable.",
    ),
    46: detail(
        "Current open release issues are visible, not buried. There is no usable Git commit/tag identity; checksums substitute. The full fresh 164-IDP 1,000-seed run is deferred until Docker. Original 2,315-IDP and 459-IDP raw inputs/parameters are incomplete or unresolved. Docker/Linux/GCP/AWS execution and security validation are absent. Exact Yang/Zhao reviewer citations are unresolved in the supplied correspondence. Optional coordinate associations were not executed in the tutorials. Only macOS arm64 has fresh test/tutorial evidence.\n\nScientific limitations are equally important: nonlinear embeddings and density clusters are parameter dependent; repeated concatenation has no stated topology-recovery theorem; internal metrics are not biological validation; legacy scoring is candidate-population relative; selection can create circular inference; UMAP axes are not loadings; original-space correlations are conditional descriptors; noise is algorithmic; numerical determinism is platform dependent; and original-IDP interpretations may change with ongoing development.\n\nOperational limitations include optional Parquet dependencies/failure handling, large similarity matrices, thread oversubscription, first-run JIT overhead, strict absent/empty output roots for safety, and manifests that can expose paths or identifiers. Use `evidence/03_missing_evidence_register.tsv`, `evidence/tutorial_issue_register.tsv`, and the Docker handoff as living registers.",
        "The manual labels itself an RC1 first draft with named limitations rather than hiding Gate I/J dependencies. Appendix G shows which layers pass, are bounded, are historical, or are pending.",
        "Inspect missing-evidence, authority/conflict, claim/correction, citation-gap, tutorial-issue, QA, build-report, and Docker-handoff records before release language changes.",
        "Do not close an issue by changing prose alone. Do not infer missing reviewer references. Do not present original IDP material as final when development may change it.",
        "Some gates need new authority/data/compute rather than documentation. They remain named blockers with exact completion protocols.",
        "Select one open software, scientific, historical, and platform limitation; state the artifact needed to close each.",
    ),
})

DETAILS.update({
    32: detail(
        "Tutorial 1 is the canonical novice path. Its configuration fixes every searched field, uses the repository synthetic matrix and annotation table, one seed, three components, one HDBSCAN candidate, one job, and a new output root. The correct annotation join is `index`. Preflight proves one candidate before fitting.\n\nThe executed canonical directory is `tutorials/01_fixed_synthetic/run_20260825_v2`. It prepared 24 vectors by 80 variables, selected `model_060fac0208bb58e2`, and produced three clusters of eight with no unassigned observations. Parquet writing succeeded. The validation utility later passed all 24 run-contract checks.\n\nThe earlier `run_20260825` is intentionally retained: clustering succeeded, but the original join key was absent and annotations were skipped with a warning. The canonical rerun demonstrates the evidence-preserving response—correct source configuration, write a new output root, and retain the prior attempt.",
        "Follow Chapters 11–14 using the actual YAML. Then use Chapter 22 to reproduce the selected summary, Chapter 23 to compare it, and Chapter 25 to explain it. The complete commands and timings are in `tutorial_execution_manifest.tsv`.",
        "Inspect the config, preflight manifests, canonical run manifest, candidate tables, selection manifest, labels/annotations, logs, reproduction, comparison, explanation, and validation.",
        "Do not delete the noncanonical first run. Do not call the designed grouping discovery evidence. Do not use the fixed quickstart to choose production parameters.",
        "This fixture is a smoke test with deliberately clear structure. Runtime and accuracy are not a guarantee for large correlated GWAS inputs.",
        "From only the artifacts, reconstruct input shape, candidate count, selected ID, cluster sizes, noise count, annotation status, and validation result.",
    ),
    33: detail(
        "Tutorial 2 teaches workload and family comparison without searching toward a biological target. Its custom YAML crosses two neighbor values, two minimum-distance values, two minimum-cluster sizes, two min-samples values, and two epsilon values; scalar fields contribute one. Four UMAP families × eight HDBSCAN configurations = 32 candidates. Two repeated seeds keep the example bounded.\n\nAll 32 completed successfully. The selected `model_241ad5e99af55074` has three equal clusters, no noise, silhouette about 0.970354, and DBCV about 0.976386. Eight candidates within its UMAP family tie at final score 1 because the designed fixture produces the same topology/score components for those HDBSCAN settings. The deterministic tie rule selects one ID. Figure 2 makes the four family-level score bands visible.\n\nThis is a tuning lesson about declared parameter families and compute; it is not permission to expand a grid until a desired label vector appears.",
        "Compare `search_space_manifest.tsv` with `models/ranked_models.tsv`. Group by `umap_id`, inspect repeated embedding metrics, then compare HDBSCAN parameters within each group.",
        "Inspect candidate count/family IDs, statuses, metrics and scopes, score ties, family summaries, Pareto table, selected parameters, runtime, seeds, and annotation output.",
        "Do not report rank-one as unique when eight rows tie. Do not interpret DBCV as the selection term. Do not extrapolate a 10.7-second local runtime to the 1,000-seed production run.",
        "The fixture has no noise and strong designed clusters, so it does not exercise every failure or uncertainty mode. A real tuning plan needs preregistered objectives and resource pilots.",
        "Calculate 32 candidates, explain why there are only four UMAP fits, and identify the exact field that breaks final ties.",
    ),
    34: detail(
        "Tutorial 3 begins with real native outputs rather than rerunning the entire search. `score-existing` normalizes and ranks an existing model table while preserving a scoring manifest. `summarize-models` writes family, Pareto, top-model, and count summaries. `reproduce-model` performs one fixed refit. `explain` produces original-space descriptive artifacts without refitting. `compare` evaluates exact-ID structural and coordinate concordance. `validate` checks the original run contract.\n\nAll six executed commands exited zero. The same-environment fixed rerun has 24 exact IDs; ARI, NMI, noise Jaccard, and optimally mapped membership are 1; variation of information is zero; Procrustes disparity is 2.7088204667806472×10^-31. The canonical Tutorial 1 run passes 24/24 validation checks. Original-space within-cluster means are near 0.993–0.996 on the designed fixture.\n\nEach result answers a different question. Scoring is not refitting; reproducing is not explaining; comparison is not schema validation; descriptive similarity is not biological inference.",
        "Run the six commands from the exact command JSON in `tutorial_execution_manifest.tsv`, substituting new output roots. Verify the generated file set against Chapter 41.",
        "Inspect rescoring manifest, summary counts, fixed rerun manifest, explanation manifest/sidecars, all comparison files, all validation files, and command logs.",
        "Do not overwrite the original run. Do not compare label integers directly. Do not treat an exit-zero command as sufficient without checking its semantic assertions.",
        "The tutorial uses a small, same-platform fixture and does not test legacy incomplete matching, large heatmap safeguards, cross-hardware numerics, or biological replication.",
        "For each of the six commands, write ‘refits: yes/no’ and the scientific question it cannot answer.",
    ),
    35: detail(
        "MNIST is a known-label image dataset used here as historical software-benchmark evidence. It tests whether a pipeline can produce and compare structure when class labels exist and inputs are unrelated to GWAS biology. The verified prior benchmark artifacts are retained under the Freeze 3 evidence/quarantine workspace; this manual build did not redownload data or rerun the benchmark. The historical full runtime was 273.47 seconds under its recorded environment and configuration.\n\nA benchmark may report engineering measures such as cluster/label concordance, noise, or runtime. It does not show that genetic association vectors have the same geometry, that IDP clusters are biologically meaningful, or that production resources match. Dataset licensing/acquisition, preprocessing, and environment must travel with any rerun.\n\nTutorial 4 is therefore evidence-backed but bounded: it documents the existing verified outputs and the approved rerun path without fabricating fresh results.",
        "Read `benchmarks/mnist/MNIST_BENCHMARK_REPORT.md` and `docs/MNIST_BENCHMARK.md`, then locate the historical output checksums in the broader Freeze 3 evidence inventory. Compare every benchmark claim to its manifest.",
        "Inspect acquisition/source note, input shape, known-label mapping, configuration, seeds/threads, cluster/noise metrics, runtime, environment, and artifact hashes.",
        "Do not present MNIST accuracy as biological validation, a universal runtime, or a production default. Do not fetch new data silently during a reproducibility build.",
        "The benchmark is historical prior evidence in this manual edition. A fresh container benchmark belongs to the Docker stage and must record dataset identity and license.",
        "Write one engineering claim supported by MNIST and three biological claims it cannot support.",
    ),
    36: detail(
        "The original 164-IDP case has two tracks. Track A is historical reconstruction: the authoritative record contains 164 IDPs, 102 HDBSCAN-noise assignments, and five assigned clusters of sizes 9, 13, 15, 14, and 11. The published historical solution used epsilon 0, min-samples 4, and min-cluster-size 6 and was manually selected from sorted row 16—not automatic rank one. One historical `UMAP_3` cell is missing, while labels are complete. Freeze 3 can adapt and rescore the immutable historical artifacts; that is not a new 1,000-seed fit.\n\nTrack B is the pending fresh protocol. Use the authoritative input checksum and `configs/original_idp_164_historical_search.yaml`, run `inspect-config` and complete enumeration, preflight storage/threads, then execute standard-scale 1,000 repeated seeds in a new mounted output root inside the later Docker workflow. Preserve source, input, resolved config, command, environment, seeds, thread settings, logs, failures, all candidate rows, retained artifacts, explanation, comparison to historical labels, and validation. Do not tune toward the published labels.\n\nOriginal material is permitted in the project, but scientific content is provisional because development has advanced; this manual shows aggregate historical counts and protocols rather than claiming a final interpretation.",
        "Figure 5 separates the historical count panel from a prominent ‘fresh run pending’ panel. The protocol config and historical selected config are source artifacts; no fresh outputs are implied.",
        "Track A: historical workbook/table, row-16 record, exact label vector, adaptation/rescoring manifests and counts. Track B: authoritative input/config hashes, preflight, complete run, comparison/validation, and Docker platform record.",
        "Do not say ‘reproduced the 164 analysis’ when only labels were adapted/rescored. Do not choose a new candidate because it most resembles historical labels. Do not fill missing fresh metrics with historical numbers.",
        "The original raw 2,315- and 459-IDP inputs remain incomplete/unresolved in this workspace. Fresh 164 execution and cross-platform acceptance are named release gates.",
        "Write two results paragraphs: one strictly historical and one future-tense protocol. Highlight every verb that distinguishes them.",
    ),
})

DETAILS.update({
    24: detail(
        "A loading in a linear component model has a defined relationship to an observed variable and component. A UMAP coordinate instead comes from a nonlinear, stochastic neighborhood-preservation optimization. Axis orientation, sign, rotation, scale, and even apparent global layout can vary without changing the underlying scientific identity of points. Freeze 3's display columns are therefore descriptive coordinates, not effects, loadings, mechanisms, or causal axes.\n\nConcatenated repeated coordinates are the density-clustering representation. Selected `UMAP_1`–`UMAP_3` columns are visualization coordinates and must not be substituted for the full concatenated matrix. Correlating input dimensions with a display coordinate can be a descriptive diagnostic when explicitly enabled, but it does not turn the coordinate into a biological component.",
        "Figure 1 shows three separated synthetic groups. Its axis titles deliberately say ‘display coordinate,’ and its caption states that axes are not biological loadings.",
        "Inspect display-coordinate columns, parameter/seed manifest, projection-quality table, optional coordinate-association table, and interpretation warnings.",
        "Do not name a coordinate ‘brain-size axis’ or infer direction of effect from its sign. Do not compare unaligned coordinates across runs. Do not equate a 2D picture with the HDBSCAN fit space.",
        "Coordinates can still be useful for visualization and diagnosing local structure, but claims should be invariant to arbitrary orientation and supported in original space or independent evidence.",
        "Rewrite a caption that says ‘UMAP1 loading reveals mechanism X’ into a descriptive, noncausal caption.",
        "See McInnes et al. (2018), DOI 10.21105/joss.00861.",
    ),
    25: detail(
        "`explain` returns to the original matrix after a partition has been retained. It loads native summary/labels or a legacy table, resolves input orientation, validates/strips identifiers, rejects duplicates, enforces complete matching by default, applies the recorded preprocessing contract, and computes original-space similarity without refitting UMAP or HDBSCAN.\n\nNative mode usually needs only `--model-json`; `--input` can override a stale recorded path. Legacy mode requires a label table, original input, explicit output root, and often explicit orientation/ID/label/coordinate options. The noise policy can place unassigned vectors last, include them in ordering, or exclude them with a recorded reason.\n\n```bash\ndimple-gwas explain \\\n  --model-json RUN/models/top_model_artifacts/MODEL/summary.json \\\n  --output-dir explanation_new\n```",
        "Tutorial 3 matches all 24 synthetic feature IDs, excludes none, writes the complete similarity table, and produces ordered heatmap/summary/projection artifacts without changing labels.",
        "Inspect interpretation manifest sources/hashes, orientation, ID counts, exclusions, `heatmap_order.tsv`, similarity table, summaries, projection quality, README, and figure sidecars.",
        "Do not let auto-orientation replace an explicit contract when both axes could overlap. Do not accept incomplete matching silently. Do not describe explanation as a refit or independent validation.",
        "Original-space summaries remain conditional on a selected partition and input construction. They can reveal descriptive coherence or contradictions but cannot establish causal mechanism.",
        "Given a legacy table with duplicate IDs and one unmatched ID, predict the default outcome and the effect of allowing incomplete matching.",
    ),
    26: detail(
        "Pearson correlation summarizes linear association after centering/scaling; Spearman correlates ranks and summarizes monotone association. Freeze 3 uses the configured method to build a vector-by-vector similarity table in original input-variable space. It then summarizes within-block and between-block pairs after applying the declared order/noise policy.\n\nUndefined correlation can arise from constant or insufficiently variable vectors. The safe default is `error`; the opt-in `zero` policy replaces undefined values and records the choice. This replacement is a computational convention, not evidence of no association. Coordinate associations, when enabled, are ranked descriptive correlations between original dimensions and supplied coordinates.\n\nNeither correlation supplies a causal effect, an unbiased post-selection p-value, or independent replication.",
        "Tutorial 3's three synthetic clusters have within-cluster Pearson means approximately 0.9963, 0.9930, and 0.9928; between-cluster means are about 0.0033–0.0047. Figure 3 labels these as post-selection descriptive summaries.",
        "Inspect similarity method, pair counts, means/medians, between summaries, exclusions, undefined-correlation policy, and optional association method/top-N settings.",
        "Do not attach naive p-values to the same selected pairs. Do not interpret zero replacement as observed zero correlation. Do not compare Pearson and Spearman without explaining the different question.",
        "Shared sample, LD, preprocessing, technical structure, and selection can drive correlations. Independent evidence is required for biological interpretation.",
        "For one cluster-summary row, explain denominator/pair count and why the mean is conditional on retained membership.",
    ),
    27: detail(
        "The explanation heatmap is a rendered view of an auditable order. `heatmap_order.tsv` records 1-based display order, exact feature ID, cluster label/noise flag, and supplied coordinates. `cluster_cutpoints.tsv` records zero- and one-based inclusive block boundaries and sizes. Within a cluster, `cluster_then_hclust` applies hierarchical ordering to the original-space similarity-derived distance; other choices are cluster, hclust, or input order.\n\nAnnotations come from an optional table joined by the declared index column. The initial tutorial configuration used the wrong join key and produced a warning; the source YAML was corrected to `index` and Tutorial 1 rerun as `run_20260825_v2`. The earlier output remains as evidence of the mistake. Figure interpretation should always use sidecars, not inferred pixel positions.",
        "Figure 6 is copied byte-for-byte from Tutorial 3's `original_space_heatmap.png`; its source checksum and script/manifest are in `figure_source_manifest.tsv`. The synthetic groups are designed, and the image is unrestricted fixture evidence.",
        "Inspect heatmap PNG/HTML, exact order, cutpoints, cluster summary, exclusions, annotations, manifest hash, and README caveats.",
        "Do not reorder the image manually and leave sidecars unchanged. Do not assume coloured blocks are statistically significant. Do not publish annotations without checking privacy/access status.",
        "Large matrices are protected by thresholds and optional forcing. A full-resolution heatmap can be unreadable or disclose identifiers; use aggregate summaries and controlled access when appropriate.",
        "Reconstruct the first cluster's row interval using both zero- and one-based cutpoints, and match it to `heatmap_order.tsv`.",
    ),
    28: detail(
        "HDBSCAN label `-1` means that the fitted hierarchy/extraction did not assign an observation to a retained cluster under the current representation, metric, density parameters, and selection method. It is an algorithmic status, not a biological category. Changing UMAP parameters, seed aggregation, min-cluster-size, min-samples, epsilon, metric, or selection method can change the noise set.\n\nInspect unassigned observations rather than discarding them rhetorically. Report count/fraction, exact IDs, probabilities/persistence when available, original-space relationships, stability across justified settings, and transitions in comparison outputs. Use ‘unassigned’ or ‘HDBSCAN noise’ with the condition attached. Avoid ‘non-pleiotropic,’ ‘failed IDP,’ ‘irrelevant,’ or ‘no shared structure.’",
        "The synthetic tutorials have zero noise. The historical 164-IDP record has 102 unassigned and 62 assigned across five clusters; this is historical evidence and does not imply 102 biologically irrelevant IDPs.",
        "Inspect label tables, noise count/fraction, candidate parameters, membership comparison, changed-noise status, exclusions under noise policy, and historical source status.",
        "Do not drop noise before reporting its magnitude. Do not compare noise labels without exact IDs. Do not treat absence of assigned cluster as absence of any genetic correlation.",
        "Freeze 3 does not provide a calibrated biological uncertainty interval for each label. Stability and external data must be studied separately.",
        "Write a results sentence for 102 historical noise assignments that includes parameters/evidence status and makes no biological-negation claim.",
        "See Campello et al. (2015), DOI 10.1145/2733381.",
    ),
    29: detail(
        "‘Double dipping’ occurs when data-dependent choices are ignored in a later inferential statement. DIMPLE-GWAS uses the matrix to create an embedding, enumerate/extract partitions, and select one using internal metrics. Testing separation or correlation on the same matrix as though the partition were fixed in advance can yield overconfident evidence. Multiple candidate models and analyst inspection add further selection.\n\nSafe outputs in Freeze 3 are descriptive summaries with explicit conditioning. For inference, plan held-out variables, independent cohorts, preregistered replication, sample splitting, perturbation/stability designs, or a selective-inference method whose assumptions actually match the pipeline. Report effect sizes and uncertainty appropriate to the validation design. Never describe an omitted p-value as a flaw: the explanation utility intentionally avoids cluster ANOVA and post-selection significance.",
        "Tutorial 3 reports within/between similarities and a heatmap but no ANOVA p-values. That is a deliberate boundary, not missing validation.",
        "Inspect candidate population, selection rule, all exploratory views used, independent validation plan, comparison/stability evidence, and whether any test data were held out before selection.",
        "Do not call high within-cluster correlation a validation test. Do not choose external outcomes after seeing the partition without disclosure. Do not cite a general selective-inference paper as if it implemented this exact pipeline.",
        "Independent validation may still inherit sample overlap, ancestry, measurement, or harmonization biases. The design—not the word ‘replication’—determines evidential strength.",
        "Design one descriptive analysis and one genuinely external validation for the same retained partition; identify which data enter selection.",
        "See Gao, Bien & Witten (2024), DOI 10.1080/01621459.2022.2116331, with the scope limitation stated above.",
    ),
    30: detail(
        "Validation is layered. Software validation covers tests and schemas. Technical reproducibility covers source/input/configuration identity, reruns, hashes, labels, and numeric tolerance. Structural concordance uses ARI/NMI/noise/mapped membership. Statistical validation addresses parameter sensitivity, instability, selection, uncertainty, and multiplicity. Biological validation asks whether groupings recur or predict independent domain evidence. Cross-platform validation tests the claimed package on Docker/Linux/cloud environments.\n\nA result should be reported at the strongest layer actually supported. Forty-five tests support software. Twenty-four artifact checks support one run contract. Perfect fixture concordance supports bounded same-platform technical structure. MNIST supports known-label engineering behavior. None proves the historical IDP clusters biologically distinct. The fresh 164-IDP and Docker/cloud layers remain pending.",
        "Use `assets/diagrams/diagram_10_validation_ladder.mmd` and Appendix G to classify every manual evidence item. No arrow can be skipped by renaming a lower layer.",
        "Inspect test JUnit/logs, validation checks, comparison metrics, source/input/config hashes, historical evidence, external-study design, and platform matrices separately.",
        "Do not write ‘validated’ without an object, method, dataset, platform, and criterion. Do not let a checksum pass stand in for scientific replication.",
        "Statistical and biological validation protocols are context dependent and may require data or governance outside this package. This manual does not invent those results.",
        "Create a five-row validation table for your run with evidence path, criterion, result, and remaining uncertainty.",
    ),
    31: detail(
        "A complete report states: software/version/source identity; input cohort and upstream GWAS construction; matrix shape/orientation/metadata prefix; preprocessing; UMAP/densMAP parameters, repeat/seed sequence, and metric; HDBSCAN search space and backend; candidate counts/failures; all calculated metrics; scoring formula/profile/noise term; selection/ties/manual decisions; retained cluster/noise counts; original-space descriptive summaries; sensitivity/comparison evidence; validation layer; and limitations.\n\nUse conditional language: ‘under the specified representation and HDBSCAN parameters, the selected model assigned…’. Separate implementation results from interpretation and hypotheses. Disclose the historical manual row-16 choice. Name unassigned observations neutrally. If results come from adapted historical labels, say so. Include exact artifact identifiers/checksums in supplements or repositories permitted by data policy.\n\nMethods should be reproducible without claiming bitwise platform independence; results should be readable without turning internal scores into biological proof.",
        "A safe synthetic sentence is: ‘In the 24-vector fixed fixture, the one-candidate RC1 run assigned three clusters of eight and no noise; a same-environment fixed rerun had ARI and NMI 1. These engineering checks do not establish biological validity.’",
        "Report from resolved config, run/selection manifests, all/ranked models, retained summary/labels, explanation/comparison/validation manifests, source/input hashes, and issue register.",
        "Do not omit failed candidates, ties, noise, manual selection, or pending gates. Do not present display axes as biological components. Do not claim causal mechanisms from correlations.",
        "Journal word limits may require a concise main text; place complete contracts and machine-readable evidence in a suitable supplement without exposing restricted data.",
        "Draft a methods paragraph and results paragraph for Tutorial 2, then highlight every phrase supported only by internal rather than external evidence.",
    ),
})

DETAILS.update({
    15: detail(
        "Preprocessing defines the geometry presented to UMAP. Freeze 3 removes `input.drop_first_n_cols` leading columns, validates that analysis columns are numeric, optionally applies rank inverse normal transformation to each analysis column before transpose, and then transposes to vectors by input variables. With `zscore_transform=none`, values are not RINT-transformed. The historical option name is retained although the implemented alternative is `rint`.\n\nFor a column with ranks, RINT maps rank-based probabilities through the standard-normal quantile function. It can reduce marginal scale differences and the influence of extreme values, but it also changes the scientific quantity and does not repair upstream harmonization or dependence. The configuration default is `none`; enable RINT only with a documented rationale that matches the intended historical or prospective protocol.",
        "The preprocessing tests cover RINT and numeric-matrix behavior. Both executed synthetic tutorials use `none`, so their values remain on the fixture's generated scale.",
        "Inspect the input config, resolved transform, input-contract manifest, prepared-shape log line, identifier set, and any preprocessing warnings. Record upstream transformations separately.",
        "Do not describe RINT as row-wise without naming the table orientation: implementation applies it to analysis columns before transpose. Do not call it z-scoring or assume it creates independence.",
        "RINT can alter ties, correlations, distances, and downstream partitions. The manual makes no universal recommendation between transformed and untransformed analyses.",
        "Given a 5-row analysis column with a tie, explain what information ranks retain and discard, then state where transpose occurs.",
    ),
    16: detail(
        "Freeze 3 passes the full prepared matrix to umap-learn. The searched UMAP keys are `n_neighbors`, `min_dist`, `n_components`, `metric`, `spread`, `learning_rate`, `repulsion_strength`, `negative_sample_rate`, `local_connectivity`, `set_op_mix_ratio`, `random_state`, and `densmap`. The standard defaults are 30 neighbors, minimum distance 0, three dimensions per repeat, Euclidean metric, and densMAP enabled.\n\n`n_neighbors` influences the local-versus-broader neighborhood balance. `min_dist` and `spread` shape allowed packing in the embedded space. The metric defines neighbor dissimilarity in the prepared input space. densMAP adds density preservation pressure. Optimizer parameters affect the fitted representation. `n_components` is per repeat; it is not necessarily the number of coordinates later used for a display plot.\n\nNo user-visible PCA, SVD, or ICA pre-reducer exists in the production path. UMAP's internal initialization should not be misreported as an explicit preprocessing stage.",
        "Tutorial 2 varies neighbors (10,15) and min_dist (0,0.1), giving four UMAP families. Candidate-score groups reflect those families, while the eight HDBSCAN variants within a family share the same embedding metrics.",
        "Inspect flattened UMAP fields, `umap_id`, trustworthiness/continuity, seeds, runtime, and selected display coordinates. Compare the resolved config to the default reference.",
        "Do not interpret UMAP_1/2/3 as effect directions or loadings. Do not compare coordinates from unaligned runs pointwise. Do not say densMAP preserves all global distances.",
        "UMAP behavior is stochastic and parameter/metric/data dependent. Projection diagnostics are bounded summaries, and a visually persuasive layout does not establish a unique topology.",
        "Choose one UMAP parameter and describe the implementation-visible change you would audit without predicting a biologically preferred result.",
        "See McInnes et al. (2018), DOI 10.21105/joss.00861; Narayan et al. (2021), DOI 10.1038/s41587-020-00801-7; and official UMAP parameter documentation.",
    ),
    17: detail(
        "For each UMAP family, Freeze 3 derives a deterministic sequence of integer seeds from the configured base state and repeat count. It executes one embedding per seed and horizontally concatenates the resulting `n_components` coordinates. With 1,000 repeats and three components, the HDBSCAN input has 3,000 coordinates per vector. A smaller display embedding is retained separately for selected-model visualization.\n\nRepeats multiply UMAP work and concatenated-memory width. Standard mode uses the historical ensemble seed behavior and 1,000 repeats; the tutorials set one or two for bounded execution. `n_jobs`, Numba behavior, BLAS/OpenMP libraries, architecture, and thread scheduling can affect runtime and numerical detail. Reproducing seeds is necessary but not sufficient for bitwise cross-platform identity.\n\nThe representation is an empirical aggregation. It is not averaged coordinates, a formal consensus cluster, or a proof of expected-distance estimation.",
        "Tutorial 2's manifest lists seeds 42 and 43, three components per repeat, and four UMAP families. Each family therefore supplies a 24×6 concatenated matrix in memory; this matrix is not written to disk.",
        "Inspect `random_seeds`, `umap_seeds`, `n_random_states`, `legacy_ensemble_seeds`, UMAP runtime, package versions, thread settings, and source hash.",
        "Do not confuse the three display columns with all repeated coordinates. Do not publish a runtime estimate by linearly scaling a JIT-heavy smoke test without qualification. Do not promise identical floating-point embeddings across machines.",
        "The full 164-IDP 1,000-seed run is pending Docker. Cross-platform acceptance should use exact label/schema checks where appropriate and tolerances/alignment for floating-point coordinates.",
        "Calculate concatenated width for 1, 2, 10, and 1,000 repeats at three dimensions; identify which output file does not exist in current Freeze 3.",
    ),
    18: detail(
        "Freeze 3 fits the contributed `hdbscan` package to each concatenated embedding. `min_cluster_size` sets the smallest extracted group, while `min_samples` affects core distances and conservativeness. `cluster_selection_epsilon` can merge fine structure below a distance threshold. `cluster_selection_method` is `eom` or `leaf`; `max_cluster_size` has no effect for leaf selection and is recorded with a parameter note when set. Other exposed controls are persistence, alpha, single-cluster permission, maximum cluster size, and metric.\n\nThe standard grid uses min-cluster-size 5 through 49, min-samples 2 through 19, and epsilon 0,1,2: 2,430 candidates. Candidate identity also includes UMAP family. Every evaluation becomes `success`, `invalid_topology` when fewer than two non-noise clusters are found, or `failed` with an error. Failure rows are retained, not removed.",
        "Tutorial 2 evaluates min-cluster-size 4/6, min-samples 2/4, epsilon 0/0.05, and scalar EOM/Euclidean settings across four UMAP families. All 32 candidates succeeded and produced three clusters with no noise.",
        "Inspect `hdbscan_id`, flattened parameters, status, error message, cluster/noise counts, persistence summaries, metric warnings, candidate runtime, and `model_failures.tsv`.",
        "Do not interpret increasing `min_samples` as universally better. Do not use numeric cluster labels as stable identity across fits. Do not call noise observations false or biologically irrelevant.",
        "Density structure depends on the concatenated representation and metric. A grid can expose sensitivity but does not identify a uniquely correct biological scale.",
        "For a failed candidate, verify that its ordinal, model ID, parameters, status, and error remain present in `all_models.tsv`.",
        "See Campello et al. (2015), DOI 10.1145/2733381; McInnes et al. (2017), DOI 10.21105/joss.00205; and official hdbscan API documentation.",
    ),
    19: detail(
        "Candidate metrics serve different purposes. Topology fields describe non-noise cluster count, noise count/fraction, and cluster sizes. Silhouette uses the configured HDBSCAN metric and the declared sampling scope. DBCV is optionally computed as a density-aware diagnostic. Calinski–Harabasz and Davies–Bouldin are supplied with explicit metric/context fields. HDBSCAN persistence summaries describe retained clusters. Trustworthiness and continuity belong to the embedding family, not to one HDBSCAN extraction.\n\nMetrics can be missing when a topology is invalid, a calculation is undefined, a backend cannot support a metric, or a candidate fails. Read `status`, scope, sampled flags, sample sizes, and `metric_warnings` before comparing numbers. The candidate table is deliberately wide so these qualifications are not hidden.",
        "The selected Tutorial 2 candidate has silhouette about 0.970354 and DBCV about 0.976386, with three equal clusters and no noise. These values describe the designed fixture under Euclidean geometry; they are not expected production targets.",
        "Inspect metric value plus its metric/scope/sampled/sample-size columns, topology counts, persistence, warnings, and the run's compute flags.",
        "Do not call silhouette inherently Euclidean; Freeze 3 supplies the configured metric. Do not compare a sampled score with a full score without noting scope. Do not call DBCV the universal best metric.",
        "All internal metrics are conditional on representation and candidate population. They lack independent biological evidence and can disagree legitimately.",
        "Choose two candidates and write a comparison that mentions representation, metric, scope, topology, and warnings before selecting any score.",
        "See Rousseeuw (1987), DOI 10.1016/0377-0427(87)90125-7, and Moulavi et al. (2014), DOI 10.1137/1.9781611973440.96.",
    ),
    20: detail(
        "`legacy_dimple` is the default compatibility score. Among eligible candidates, each included component is divided by its maximum. Its weight is the component's raw observed range divided by the sum of included ranges. Raw score adds normalized silhouette and normalized non-noise cluster count and, only when `fit_include_noise=true`, subtracts normalized noise count. The raw score is finally scaled to [0,1] over the eligible candidate population; a zero range maps to 1.\n\nThis is population-relative: adding or removing candidates can change maxima, ranges, weights, and final scores even if an existing candidate's own metrics do not change. DBCV may be present in the table but is not a legacy-score term. No preferred cluster band, noise ceiling, largest-cluster target, or biological label is embedded.\n\nThe `custom` profile accepts explicitly declared metric weights and maximize/minimize directions. It should represent a preregistered analytic objective, not weights tuned after viewing a desired partition.",
        "In Tutorial 2, all candidates have the same cluster count and no noise, so UMAP-family silhouette differences drive four score levels and eight-way ties within families. The selection manifest records realized formula and tie order.",
        "Inspect `raw_score`, `score`, compatibility aliases, scoring profile, noise-fit flag, realized weights/ranges, eligible counts, and tie order in `model_selection_manifest.json`.",
        "Do not say DBCV selected the model when profile is legacy. Do not compare normalized scores across candidate populations as though absolute. Do not introduce outcome-informed custom weights.",
        "A heuristic rank is not a probability, confidence, p-value, or guarantee of stability. Scientific selection should combine transparent objectives, sensitivity, and external evidence.",
        "Using Appendix B, explain why the same model can receive a different normalized score after the candidate set expands.",
    ),
    21: detail(
        "Ranking begins after statuses and scores exist. Eligible successful rows are ordered by final score descending, raw score descending, then stable `model_id` ascending. `top_models.tsv` retains the requested number; `best_model.json` and the selection manifest identify rank one. Pareto membership and family summaries are supplementary views, not alternate truth labels.\n\nChoosing a model should be traceable to an objective declared before inspecting preferred biological labels. Review failure/invalid rates, parameter-family patterns, tied or near-tied solutions, noise and size trade-offs, stability checks, and domain-independent constraints. A rank-one row is the implementation's selected model under the declared rule, not proof that the cluster count is uniquely correct.\n\nTarget leakage includes choosing parameters because their labels resemble a published solution when those parameters were not recovered from the historical method. The 164-IDP manual row-16 selection is disclosed rather than retroactively portrayed as automatic rank one.",
        "Tutorial 2's first eight models tie at score 1 because their HDBSCAN choices yield the same metrics within the best UMAP family. Stable model ID breaks remaining ties; this is an engineering rule, not a biological preference.",
        "Inspect ranked/all/top tables, family summaries, Pareto table, model selection manifest, best-model JSON, failures, and exact parameter records.",
        "Do not hide ties or failed candidates. Do not select solely from a pretty plot. Do not use knowledge of desired labels to redefine the search or score and then call it replication.",
        "Internal selection uncertainty is not automatically quantified. Report sensitivity and the conditional nature of the chosen population.",
        "Write a selection note for Tutorial 2 that names the rule, tie, selected ID, candidate population, and why no biological conclusion follows.",
    ),
    22: detail(
        "A retained native `summary.json` contains the exact UMAP/HDBSCAN parameters, resolved run configuration, label-file hash, input record when available, and feature count. `reproduce-model` converts that contract to fixed mode, optionally overrides a stale input path, and performs one new fit in a new output directory. It refits; it does not copy labels.\n\n```bash\ndimple-gwas reproduce-model \\\n  --model-json docs/manual/tutorials/01_fixed_synthetic/run_20260825_v2/models/top_model_artifacts/model_060fac0208bb58e2/summary.json \\\n  --input benchmarks/synthetic/synthetic_matrix.tsv \\\n  --output-dir docs/manual/tutorials/03_explain_compare_validate/reproduced_new \\\n  --n-jobs 1\n```\n\nAfter the rerun, use `compare` rather than assuming numeric label equality or coordinate alignment.",
        "The executed reproduction selected the same stable model ID on the same fixture and environment. Comparison found exact ID order/set, ARI/NMI/noise Jaccard/mapped membership 1, and Procrustes disparity 2.7088×10^-31.",
        "Inspect source summary/hash, reproduced resolved config and run manifest, new labels, comparison outputs, and validation checks.",
        "Do not use the original output directory. Do not call label-number equality the only correctness measure. Do not claim cross-platform determinism from a same-platform fixture.",
        "One fixed rerun tests an already selected parameterization; it does not reproduce the uncertainty or selection process of a full search.",
        "Reproduce the tutorial model into a unique directory and compare it. Explain any difference separately for identifiers, membership, noise, and coordinates.",
    ),
    23: detail(
        "`compare` accepts two native summaries or label tables, requires unique exact ID sets, and can require the same order. It reports adjusted Rand index, normalized mutual information, variation of information, noise-set Jaccard, optimal label mapping, mapped membership, changed noise status, cluster sizes, and optional Procrustes disparity. Numeric labels are local names, so structural metrics are primary.\n\n`validate` inspects one run directory for required artifacts, readable JSON/YAML, enumeration counts, ranked schema, selected artifacts, and recorded hashes. It writes one pass/warn/fail row per check and returns exit code one on failure. Validation does not refit or compare biology.\n\n```bash\ndimple-gwas compare --left LEFT/summary.json --right RIGHT/summary.json --output-dir comparison_new\ndimple-gwas validate --run-dir RUN --output-dir validation_new\n```",
        "Tutorial 3 comparison uses 24 IDs, three clusters, no noise, perfect structural metrics, zero variation of information, and near-zero aligned coordinate disparity. Validation reports 24/24 pass with no warnings or failures.",
        "Inspect `comparison_summary.json`, membership table, size table, confusion, mapping, comparison manifest, `validation_checks.tsv`, report, and validation manifest.",
        "Do not compare raw numeric labels across fits. Do not ignore changed noise status. Do not interpret Procrustes as membership agreement. Do not call hash/schema checks biological validation.",
        "Exact label equality is stringent and environment-sensitive; permutation-invariant equality is structural. Coordinate comparison needs alignment and tolerances. Scientific conclusions need higher-layer validation.",
        "Describe a case with ARI=1 but different numeric labels, and a different case with similar coordinates but changed memberships.",
    ),
})

DETAILS.update({
    9: detail(
        "Use a supported Python in an isolated environment so package resolution is auditable and does not alter system Python. This manual build used Python 3.12.13 on macOS arm64 and installed the package editable with its `test` and `plots` extras. The exact resolved package list is retained in `evidence/resolved_dependencies.txt`; `pip check` reported no broken requirements.\n\nFrom the Freeze 3 root, a portable setup pattern is:\n\n```bash\npython3 -m venv .venv\n. .venv/bin/activate\npython -m pip install --upgrade pip\npython -m pip install -e '.[test,plots]'\ndimple-gwas --version\npython -m pip check\n```\n\nThe `.venv` name is an example. Keep it out of release artifacts. On Windows, use the platform's activation command. For restricted networks, acquire dependencies through the institution's approved package process and record their hashes.",
        "The documentation build used `docs/manual/build/runtime_env`, then passed the absolute environment interpreter to every captured command. The runtime manifest reports exact scientific-library versions and a package-source SHA-256.",
        "Check the printed version, `pip check`, `python -m pip freeze`, the CLI top-level help, and available storage before choosing a search scale.",
        "Do not install into macOS system Python; do not assume `python` and `pip` point to the same environment; do not commit the environment directory; do not publish manifests containing unnecessary private paths.",
        "A working local installation is not a Docker or security validation. Native build requirements and numerical backends can differ on Linux or x86_64.",
        "Open a new shell, activate the environment, and prove that `which python`, `python -m pip --version`, and `dimple-gwas --version` all refer to the intended environment.",
    ),
    10: detail(
        "The standard run contract is a CSV/TSV table with variants in rows, a declared leading metadata prefix, and vectors/IDPs in the remaining columns. The default `drop_first_n_cols` is 4. Analysis columns must be numeric after parsing. Their column names become `feature_id` values after transpose, so they must be stable and unique. The original row axis supplies the variables across which vectors are compared.\n\nFreeze 3 reads the separator explicitly when configured or through its table reader, drops the prefix, optionally transforms analysis columns, and transposes. The native explanation path expects exact retained IDs and the original matrix. Legacy explanation can infer orientation only through exact overlap and should use explicit orientation/ID options when ambiguity exists. Missing, nonnumeric, constant, duplicate, or mismatched values can make preprocessing or correlations undefined.\n\nThe input-orientation diagram at `assets/diagrams/diagram_02_input_orientation.mmd` is the safest mental model.",
        "The fixture `benchmarks/synthetic/synthetic_matrix.tsv` has 80 rows and 28 columns: four metadata plus 24 vectors. After the prefix is dropped and data are transposed, the analysis matrix is 24 vectors by 80 variables.",
        "Before a run, inspect header uniqueness, first rows, dimensions, numeric conversion, missing counts, separator, and the annotation join column. After a run, confirm the manifest's `input_contract` and input SHA-256.",
        "Do not set `drop_first_n_cols` by guessing. Do not use annotation row number as vector identity. Do not let spreadsheet software rewrite scientific notation or identifiers. Do not silently impute missing values outside an approved upstream protocol.",
        "Freeze 3 cannot determine whether upstream variants are allele-aligned, comparable across phenotypes, or scientifically eligible. Protected study matrices should not be copied into the manual or image.",
        "For a prospective input, record row count, metadata columns, vector count, separator, missingness rule, upstream harmonization provenance, and the expected feature-ID set.",
    ),
    11: detail(
        "Configuration resolution is deterministic: start with a built-in search mode, deep-merge a YAML mapping, then apply only explicit CLI values. The result is validated and written as `resolved_config.yaml`. Therefore a YAML value can differ from the run value when a CLI override is present; the resolved file, not memory or the source overlay alone, is authoritative for that run.\n\nThe four modes are `standard`, `extended`, `custom`, and `fixed`. `custom` requires a YAML file. `fixed` requires one value for every searched UMAP and HDBSCAN parameter. Scalar values produce one choice; lists produce choices; numeric `{start, stop, step}` mappings are stop-exclusive; supported CLI strings may also encode comma lists or ranges. Unknown top-level or interpretation keys and invalid combinations fail validation.\n\n```bash\ndimple-gwas inspect-config \\\n  --search-mode custom \\\n  --config docs/manual/tutorials/02_custom_search_space/tutorial_config.yaml\n```",
        "Tutorial 2 declares two values each for `umap.n_neighbors`, `umap.min_dist`, `hdbscan.min_cluster_size`, `hdbscan.min_samples`, and epsilon; other searched fields are scalar. The resolved file records two repeated states and one candidate job.",
        "Compare the source YAML, captured `inspect-config` output, and run `resolved_config.yaml`. Use `evidence/configuration_key_reference.tsv` for every default and exposure.",
        "Do not call a tutorial value a default. Do not edit a resolved output and assume the past run changed. Do not use a range's `stop` as though it were included. Do not mix `custom` with no YAML.",
        "Configuration validity means fields satisfy software constraints, not that the scientific search is appropriate. Candidate-count safety and parameter justification remain analyst responsibilities.",
        "Predict the resolved value when built-in `n_jobs=-1`, YAML sets `n_jobs=2`, and CLI supplies `--n-jobs 1`. Confirm using `inspect-config`.",
    ),
    12: detail(
        "`inspect-config` resolves and validates configuration and prints candidate counts without fitting. `show-search-space` enumerates the complete deterministic Cartesian product and can retain full TSV/JSON manifests. These commands are mandatory preflight tools: they expose accidental explosions, invalid fields, and misunderstood ranges before UMAP consumes compute.\n\n```bash\ndimple-gwas show-search-space \\\n  --search-mode custom \\\n  --config docs/manual/tutorials/02_custom_search_space/tutorial_config.yaml \\\n  --output-dir docs/manual/tutorials/02_custom_search_space/search_space_new \\\n  --show-first 5\n```\n\nChoose a new output directory name; the manual's executed directory is evidence, not a scratch target. Standard mode proves 45 min-cluster-size choices × 18 min-samples choices × 3 epsilon choices = 2,430 candidates for one UMAP family. Shipped extended mode has 1,728 candidates, not the older provisional 5,184 number.",
        "Executed Tutorial 1 enumerated one candidate; Tutorial 2 enumerated 32: four UMAP families times eight HDBSCAN configurations. Both counts appear in stdout and complete manifests.",
        "Inspect `candidate_models`, UMAP/HDBSCAN family counts, candidate ordinals, stable IDs, and the first/last parameter rows. Retain config and manifest checksums together.",
        "Do not estimate workload from HDBSCAN choices alone when UMAP parameters also vary. Do not silently sample a large Cartesian product; Freeze 3's safety ceiling raises rather than sampling.",
        "Candidate count is not runtime by itself: repeated UMAP families dominate some workloads while HDBSCAN candidate fits dominate others. Pilot evidence is still needed.",
        "Calculate the Tutorial 2 count from the YAML without executing it, then match each factor to the manifest.",
    ),
    13: detail(
        "The shortest verified run starts in the Freeze 3 repository root with the installed RC1 entry point. Inspect first, enumerate second, fit third, and use a new output root.\n\n```bash\ndimple-gwas inspect-config \\\n  --search-mode fixed \\\n  --config docs/manual/tutorials/01_fixed_synthetic/tutorial_config.yaml\n\ndimple-gwas show-search-space \\\n  --search-mode fixed \\\n  --config docs/manual/tutorials/01_fixed_synthetic/tutorial_config.yaml \\\n  --output-dir docs/manual/tutorials/01_fixed_synthetic/search_space_new\n\ndimple-gwas run \\\n  --search-mode fixed \\\n  --config docs/manual/tutorials/01_fixed_synthetic/tutorial_config.yaml \\\n  --output-dir docs/manual/tutorials/01_fixed_synthetic/run_new\n```\n\nReplace `*_new` with unique names. The canonical documented output is `run_20260825_v2`; do not overwrite it. The fixture is small and repository-owned. It demonstrates execution structure, not production adequacy.",
        "The executed canonical run prepared 24 vectors by 80 variables, evaluated one candidate, selected `model_060fac0208bb58e2`, found three clusters of eight, and assigned no noise. Exit status was zero.",
        "Confirm `run_manifest.json` status, one-row search manifest, one candidate table row, selected-model JSON, label row count/uniqueness, annotation join, log, and validation output when run.",
        "Do not copy an example output path unchanged. Do not jump directly to the plot before checking the manifest. Do not generalize ‘three clusters’ from the designed fixture to real data.",
        "One seed and one candidate make this a smoke test. They do not represent standard production compute or a robust model-selection study.",
        "Run the three commands in a fresh named root and write five structural assertions that avoid exact floating-point promises.",
    ),
    14: detail(
        "`run_manifest.json` is the primary run-level audit record. It names the schema, software/version, command, start/finish status, platform, architecture, Python and package versions, package-source hash, input record, resolved configuration and its hash, input contract, seeds, threads, backends, search size, runtime, selected model, scoring formula/profile, artifacts, Parquet outcome, warnings, exclusions, and failures.\n\nA healthy manifest has `status=complete`, but completion alone is not enough. Reconcile candidate counts with search manifests, failed counts with `logs/model_failures.tsv`, selected model with `model_selection_manifest.json` and `best_model.json`, and artifact hashes with files. `git_commit` is null in this source snapshot; the package-source SHA-256 and file registers substitute for build identity in this draft.",
        "Tutorial 2 records 32 search candidates, 32 completed models, zero failed models, four UMAP configurations, two random seeds (42,43), contrib HDBSCAN and umap-learn backends, and an approximately 10.713-second manifest runtime in its local environment.",
        "Inspect `run_manifest.json`, `resolved_config.yaml`, both search-space manifests, `models/model_selection_manifest.json`, `logs/run.log`, and `logs/model_failures.tsv` as a set.",
        "Do not interpret a null Git commit as a random run; use the source hash. Do not ignore a recorded optional-Parquet failure. Do not assume a complete run had no invalid topologies.",
        "Manifests can disclose local paths, input hashes, platform information, and commands. Sanitize public copies without changing the retained private audit record.",
        "Write an audit note that independently reconciles software version, input hash, configuration hash, candidate count, failure count, selected model, and backend names.",
    ),
})


PART_LABELS = {
    range(1, 9): "Part I — Orientation and conceptual foundations",
    range(9, 15): "Part II — Installation, data preparation, and the first successful run",
    range(15, 24): "Part III — The complete DIMPLE-GWAS workflow",
    range(24, 32): "Part IV — Explainability and responsible interpretation",
    range(32, 37): "Part V — Worked case studies",
    range(37, 47): "Part VI — Operational reference",
}


VISUALS = {
    4: [("diagram", "diagram_01_stage1_workflow.mmd", "Stage 1 producer–consumer workflow")],
    10: [("diagram", "diagram_02_input_orientation.mmd", "Input orientation and transposition")],
    11: [("diagram", "diagram_03_config_precedence.mmd", "Configuration precedence")],
    17: [("diagram", "diagram_04_repeated_embeddings.mmd", "Repeated embeddings and concatenation")],
    18: [("diagram", "diagram_05_search_space.mmd", "Complete search-space enumeration")],
    21: [("diagram", "diagram_06_selection_reproduction.mmd", "Scoring, selection, and fixed reproduction")],
    23: [("diagram", "diagram_08_compare_validate.mmd", "Comparison and validation paths")],
    25: [("diagram", "diagram_07_original_space_explanation.mmd", "Original-space explanation without refitting")],
    27: [("figure", "figure_06_original_space_heatmap.png", "Figure 6. Ordered original-space Pearson heatmap from the executed synthetic explanation. Descriptive, post-selection evidence.")],
    30: [("diagram", "diagram_10_validation_ladder.mmd", "Validation ladder; each layer requires its own evidence")],
    32: [("figure", "figure_01_synthetic_embedding.png", "Figure 1. Selected synthetic display coordinates; axes are not biological loadings.")],
    33: [("figure", "figure_02_candidate_score_rank.png", "Figure 2. Candidate score by deterministic rank in the 32-candidate tutorial.")],
    34: [("figure", "figure_03_original_space_summary.png", "Figure 3. Post-selection descriptive within/between original-space similarity."), ("figure", "figure_04_partition_comparison.png", "Figure 4. Same-environment structural comparison of the fixed reproduction.")],
    36: [("figure", "figure_05_historical_idp_status.png", "Figure 5. Historical 164-IDP counts separated from the pending fresh-run track.")],
    42: [("diagram", "diagram_09_provenance_lineage.mmd", "Provenance and artifact lineage")],
}


def slug(title: str) -> str:
    clean = "".join(character.lower() if character.isalnum() else "_" for character in title)
    return "_".join(part for part in clean.split("_") if part)


def part_for(number: int) -> str:
    return next(label for numbers, label in PART_LABELS.items() if number in numbers)


def visual_block(number: int) -> str:
    blocks: list[str] = []
    for kind, filename, caption in VISUALS.get(number, []):
        if kind == "diagram":
            source = (MANUAL / "assets" / "diagrams" / filename).read_text(encoding="utf-8").strip()
            blocks.extend(["```mermaid", source, "```", "", f"*{caption}. Editable source: `assets/diagrams/{filename}`.*"])
        else:
            blocks.extend([f"![{caption}](../assets/figures/{filename})", "", f"*{caption} Source and checksum: `evidence/figure_source_manifest.tsv`.*"])
    return "\n\n## Evidence diagram or figure\n\n" + "\n\n".join(blocks) if blocks else ""


def curriculum() -> list[dict[str, str]]:
    with (EVIDENCE / "learning_objectives.tsv").open(encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def render_chapter(row: dict[str, str]) -> str:
    number = int(row["chapter"])
    item = DETAILS[number]
    visual = visual_block(number)
    references = f"\n\n## Evidence and references\n\n{item['references']}" if item["references"] else ""
    return f"""# {number}. {row['title']}

> **Release status.** DIMPLE-GWAS Freeze 3 RC1 (`3.0.0rc1`) is software-complete under local and fixed-fixture evidence. It is not yet scientifically frozen or cross-platform validated.

## Orientation

This chapter belongs to **{part_for(number)}**. It separates observed Freeze 3 behavior from scientific interpretation, historical evidence, and pending release work.

## Learning objectives

After this chapter, you can:

- {row['observable_learning_objective']}
- identify the evidence artifact that supports the behavior or boundary;
- describe one common misuse in language appropriate for a methods report.

Prerequisites: {row['prerequisites']}.

## Explanation and implementation

{item['core']}{visual}

## Evidence-backed example

{item['example']}

## Outputs to inspect

{item['outputs']}

## Common mistakes

{item['mistakes']}

## Scientific and operational limits

{item['limitations']}

## Completion check

{item['check']}{references}

<p class="xref"><strong>Operational cross-reference:</strong> Chapter 37 covers commands, Chapter 38 configuration, Chapter 41 artifact schemas, Chapter 42 provenance, and Chapter 46 current limitations.</p>
"""


def write_appendices() -> None:
    glossary_rows = []
    with (EVIDENCE / "glossary_source.tsv").open(encoding="utf-8") as stream:
        glossary_rows = list(csv.DictReader(stream, delimiter="\t"))
    glossary = ["# Appendix A — Glossary", ""]
    for row in glossary_rows:
        glossary.extend([f"## {row['term']}", "", f"**{row['expanded_form_or_type']}.** {row['definition']} {row['boundary_note']}", ""])
    (APPENDIX_DIR / "A_glossary.md").write_text("\n".join(glossary), encoding="utf-8")

    math = r"""# Appendix B — Mathematical notation and equations

Let the prepared analysis matrix be \(X \in \mathbb{R}^{p \times v}\), with \(p\) vectors/IDPs and \(v\) input variables/variants after the declared metadata prefix is removed and the table is transposed. For repeated embeddings \(U_s \in \mathbb{R}^{p \times d}\), the HDBSCAN input is the horizontal concatenation \(Z=[U_1|\cdots|U_R] \in \mathbb{R}^{p \times dR}\). This is an implementation identity, not a theorem about true topology.

For an observation \(i\), silhouette is \(s(i)=(b(i)-a(i))/\max\{a(i),b(i)\}\), where \(a(i)\) is its mean within-cluster distance and \(b(i)\) is the smallest mean distance to another cluster under the configured metric. Freeze 3 summarizes eligible non-noise observations.

For each legacy-score component \(x\), Freeze 3 computes \(x'=x/\max(x)\) over the eligible candidate population. Component weights are their observed raw dynamic ranges divided by the sum of included ranges. The raw score is

\[S_{raw}=w_s s' + w_c c' - w_n n'.\]

Here \(s\) is silhouette, \(c\) is non-noise cluster count, and \(n\) is noise count. When `fit_include_noise=false`, \(w_n=0\). The final score rescales \(S_{raw}\) to [0,1] over the same candidate population; a zero range maps to 1. DBCV is not a term in this formula.

ARI and NMI compare partitions invariant to numeric label permutation. Noise-set Jaccard is \(|N_A \cap N_B|/|N_A \cup N_B|\), with the implementation-defined convention for two empty noise sets. These are concordance diagnostics, not tests of biological validity.
"""
    (APPENDIX_DIR / "B_mathematical_notation.md").write_text(math, encoding="utf-8")

    bibliography = (MANUAL / "references" / "VERIFIED_BIBLIOGRAPHY.md").read_text(encoding="utf-8")
    (APPENDIX_DIR / "C_verified_bibliography.md").write_text("# Appendix C — Verified bibliography\n\n" + bibliography.replace("# Verified bibliography\n", "", 1), encoding="utf-8")

    crosswalk = """# Appendix D — Reviewer-method crosswalk

The machine-readable crosswalk is `evidence/reviewer_reference_crosswalk.tsv`. The draft adopts the reviewer requests for clearer method positioning, parameter guidance, a practical tutorial, cautious treatment of unassigned IDPs, and separation of technical from biological validation. The supplied action register does not identify exact Yang or Zhao works, so no paper is attributed to those reviewers by inference. The PCA/ICA paper named in the manuscript is correctly attributed to Oblong et al. (2024), while Zhang et al. (2023) is a different pleiotropy paper.
"""
    (APPENDIX_DIR / "D_reviewer_method_crosswalk.md").write_text(crosswalk, encoding="utf-8")

    claim_index = """# Appendix E — Claim and evidence index

The authoritative first-draft index is `evidence/claim_evidence_register.tsv`. Each row records original wording, safe wording, implementation and internal evidence, external citations, strength, limitation, reviewer relevance, and resolution. The paired `gemini_claim_correction_ledger.tsv` isolates known high-risk corrections. These registers should be updated before prose whenever software or evidence changes.
"""
    (APPENDIX_DIR / "E_claim_evidence_index.md").write_text(claim_index, encoding="utf-8")

    tutorial = """# Appendix F — Tutorial checksums and environment

The canonical per-command record is `evidence/tutorial_execution_manifest.tsv`; each tutorial also contains `execution_manifest.json`. The isolated environment is described in `evidence/runtime_environment.md`, exact installed packages in `evidence/resolved_dependencies.txt`, and manual/tutorial artifact hashes in `evidence/artifact_checksums.tsv`. Tutorial 1's canonical output is `run_20260825_v2`; the earlier directory is retained to make the corrected annotation-join mistake auditable.
"""
    (APPENDIX_DIR / "F_tutorial_checksums_environment.md").write_text(tutorial, encoding="utf-8")

    validation = """# Appendix G — Release-status and validation matrix

| Layer | Current evidence | Status |
| --- | --- | --- |
| Software | 45 tests pass in the isolated macOS environment | pass |
| Fixed-fixture technical rerun | ARI, NMI, noise Jaccard, and mapped membership are 1; Procrustes is near zero | pass, bounded |
| Artifact validation | 24/24 checks pass for Tutorial 1 v2 | pass, bounded |
| Historical 164-IDP reconstruction | Exact recorded counts, manual row-16 selection, historical adaptation/rescoring | historical only |
| Fresh 164-IDP 1,000-seed search | Not executed in this build | pending Docker phase |
| Statistical/biological validation | Not established by internal metrics or tutorials | pending external work |
| Docker/Linux/GCP/AWS | Not built or tested | pending |

No lower layer substitutes for a higher layer.
"""
    (APPENDIX_DIR / "G_release_validation_matrix.md").write_text(validation, encoding="utf-8")

    docker = """# Appendix H — Docker/cloud-stage handoff synopsis

Package source identified by `package_source_sha256` and the manual source checksum registers. Use the synthetic fixed configuration for the container smoke test and the authoritative `configs/original_idp_164_historical_search.yaml` for the later full scientific run after input and resource preflight. The complete handoff is `DOCKER_CLOUD_SUPPLEMENT_HANDOFF.md`; this documentation build creates no Dockerfile, image, registry, bucket, credential, or cloud resource.
"""
    (APPENDIX_DIR / "H_docker_cloud_handoff.md").write_text(docker, encoding="utf-8")


def main() -> None:
    CHAPTER_DIR.mkdir(parents=True, exist_ok=True)
    APPENDIX_DIR.mkdir(parents=True, exist_ok=True)
    if set(DETAILS) != set(range(1, 47)):
        missing = sorted(set(range(1, 47)) - set(DETAILS))
        raise SystemExit(f"Missing chapter detail records: {missing}")
    for row in curriculum():
        number = int(row["chapter"])
        path = CHAPTER_DIR / f"{number:02d}_{slug(row['title'])}.md"
        path.write_text(render_chapter(row), encoding="utf-8")
    write_appendices()


if __name__ == "__main__":
    main()
