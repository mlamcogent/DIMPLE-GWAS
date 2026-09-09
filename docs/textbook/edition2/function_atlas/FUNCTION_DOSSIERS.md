# Complete Tier A/B function dossiers

All **78 Tier A/B symbols** have all **20 required dossier fields**. This generated reference supplements the chapter-level dossiers; Tier C contracts remain in `function_inventory.tsv`.

## `cli.build_parser` (Tier A)

- **Name And Scientific Purpose:** `cli.build_parser`: Construct the complete user-facing command and flag grammar, including the interpret alias. Its documented role is command dispatch and user contract.
- **Workflow Position:** Called by cli.main; depends on cli._add_config_source; cli._add_run_options. Planned treatment: 13–17; Appendix A.
- **Plain Language Intuition:** It performs one auditable step of command dispatch and user contract; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: control plane; no independent estimator. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/cli.py:146; callers: cli.main; package dependencies: cli._add_config_source; cli._add_run_options.
- **Inputs And Shapes:** Signature `class construction/data container`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–3. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–3 command records. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–3 command records. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `argparse.ArgumentParser`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of command dispatch and user contract. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_freeze3_comparison_validation.py::test_cli_exposes_new_commands_and_alias. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli.main to cli._add_config_source; cli._add_run_options; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `cli._inspect` (Tier A)

- **Name And Scientific Purpose:** `cli._inspect`: Implementation callable for inspect. Its documented role is command dispatch and user contract.
- **Workflow Position:** Called by cli.main; depends on cli._resolved; search_space.count_candidates. Planned treatment: 13–17; Appendix A.
- **Plain Language Intuition:** It performs one auditable step of command dispatch and user contract; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: control plane; no independent estimator. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/cli.py:240; callers: cli.main; package dependencies: cli._resolved; search_space.count_candidates.
- **Inputs And Shapes:** Signature `args: argparse.Namespace`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–3. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–3 command records. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–3 command records. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `int`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of command dispatch and user contract. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: writes files/directories. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli.main to cli._resolved; search_space.count_candidates; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `cli._show` (Tier A)

- **Name And Scientific Purpose:** `cli._show`: Implementation callable for show. Its documented role is command dispatch and user contract.
- **Workflow Position:** Called by cli.main; depends on cli._resolved; io.json_safe; reporting.write_search_space; search_space.count_candidates; search_space.enumerate_candidates; search_space.flatten_candidate. Planned treatment: 13–17; Appendix A.
- **Plain Language Intuition:** It performs one auditable step of command dispatch and user contract; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: control plane; no independent estimator. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/cli.py:254; callers: cli.main; package dependencies: cli._resolved; io.json_safe; reporting.write_search_space; search_space.count_candidates; search_space.enumerate_candidates; search_space.flatten_candidate.
- **Inputs And Shapes:** Signature `args: argparse.Namespace`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–3. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–3 command records. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–3 command records. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `int`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of command dispatch and user contract. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli.main to cli._resolved; io.json_safe; reporting.write_search_space; search_space.count_candidates; search_space.enumerate_candidates; search_space.flatten_candidate; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `cli._score` (Tier A)

- **Name And Scientific Purpose:** `cli._score`: Implementation callable for score. Its documented role is command dispatch and user contract.
- **Workflow Position:** Called by cli.main; depends on config.resolve_config; io.atomic_json_dump; io.json_safe; io.read_model_table; ranking.rank_models; scoring.apply_scoring; scoring.normalize_model_table_schema. Planned treatment: 13–17; Appendix A.
- **Plain Language Intuition:** It performs one auditable step of command dispatch and user contract; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: control plane; no independent estimator. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/cli.py:265; callers: cli.main; package dependencies: config.resolve_config; io.atomic_json_dump; io.json_safe; io.read_model_table; ranking.rank_models; scoring.apply_scoring; scoring.normalize_model_table_schema.
- **Inputs And Shapes:** Signature `args: argparse.Namespace`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–3. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–3 command records. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–3 command records. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `int`. Direct canonical artifacts: rescored_table.tsv; rescored_table.tsv.manifest.json.
- **Result Interpretation:** Interpret results at the level of command dispatch and user contract. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: writes files/directories. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli.main to config.resolve_config; io.atomic_json_dump; io.json_safe; io.read_model_table; ranking.rank_models; scoring.apply_scoring; scoring.normalize_model_table_schema; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `cli._summarize` (Tier A)

- **Name And Scientific Purpose:** `cli._summarize`: Implementation callable for summarize. Its documented role is command dispatch and user contract.
- **Workflow Position:** Called by cli.main; depends on io.atomic_json_dump; io.read_model_table; ranking.family_summaries; ranking.pareto_front; ranking.rank_models; ranking.top_models. Planned treatment: 13–17; Appendix A.
- **Plain Language Intuition:** It performs one auditable step of command dispatch and user contract; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: control plane; no independent estimator. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/cli.py:284; callers: cli.main; package dependencies: io.atomic_json_dump; io.read_model_table; ranking.family_summaries; ranking.pareto_front; ranking.rank_models; ranking.top_models.
- **Inputs And Shapes:** Signature `args: argparse.Namespace`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–3. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–3 command records. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–3 command records. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `int`. Direct canonical artifacts: family_summaries.tsv; pareto_front.tsv; top_models.tsv; summary.json.
- **Result Interpretation:** Interpret results at the level of command dispatch and user contract. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: writes files/directories. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli.main to io.atomic_json_dump; io.read_model_table; ranking.family_summaries; ranking.pareto_front; ranking.rank_models; ranking.top_models; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `cli._reproduce` (Tier A)

- **Name And Scientific Purpose:** `cli._reproduce`: Implementation callable for reproduce. Its documented role is command dispatch and user contract.
- **Workflow Position:** Called by cli.main; depends on config.resolve_config; config.validate_config; pipeline.run_search. Planned treatment: 13–17; Appendix A.
- **Plain Language Intuition:** It performs one auditable step of command dispatch and user contract; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: control plane; no independent estimator. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/cli.py:301; callers: cli.main; package dependencies: config.resolve_config; config.validate_config; pipeline.run_search.
- **Inputs And Shapes:** Signature `args: argparse.Namespace`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–3. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–3 command records. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–3 command records. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `int`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of command dispatch and user contract. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli.main to config.resolve_config; config.validate_config; pipeline.run_search; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `cli._explain` (Tier A)

- **Name And Scientific Purpose:** `cli._explain`: Implementation callable for explain. Its documented role is command dispatch and user contract.
- **Workflow Position:** Called by cli.main; depends on config.resolve_config; config.validate_config; interpretation.run_explanation. Planned treatment: 13–17; Appendix A.
- **Plain Language Intuition:** It performs one auditable step of command dispatch and user contract; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: control plane; no independent estimator. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/cli.py:323; callers: cli.main; package dependencies: config.resolve_config; config.validate_config; interpretation.run_explanation.
- **Inputs And Shapes:** Signature `args: argparse.Namespace`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–3. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–3 command records. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–3 command records. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `int`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of command dispatch and user contract. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli.main to config.resolve_config; config.validate_config; interpretation.run_explanation; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `cli._compare` (Tier A)

- **Name And Scientific Purpose:** `cli._compare`: Implementation callable for compare. Its documented role is command dispatch and user contract.
- **Workflow Position:** Called by cli.main; depends on comparison.run_comparison. Planned treatment: 13–17; Appendix A.
- **Plain Language Intuition:** It performs one auditable step of command dispatch and user contract; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: control plane; no independent estimator. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/cli.py:376; callers: cli.main; package dependencies: comparison.run_comparison.
- **Inputs And Shapes:** Signature `args: argparse.Namespace`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–3. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–3 command records. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–3 command records. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `int`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of command dispatch and user contract. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli.main to comparison.run_comparison; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `cli._validate` (Tier A)

- **Name And Scientific Purpose:** `cli._validate`: Implementation callable for validate. Its documented role is command dispatch and user contract.
- **Workflow Position:** Called by cli.main; depends on validation.run_validation. Planned treatment: 13–17; Appendix A.
- **Plain Language Intuition:** It performs one auditable step of command dispatch and user contract; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: control plane; no independent estimator. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/cli.py:391; callers: cli.main; package dependencies: validation.run_validation.
- **Inputs And Shapes:** Signature `args: argparse.Namespace`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–3. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–3 command records. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–3 command records. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `int`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of command dispatch and user contract. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli.main to validation.run_validation; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `cli.main` (Tier A)

- **Name And Scientific Purpose:** `cli.main`: Dispatch the command-line interface and return a process exit status. Its documented role is command dispatch and user contract.
- **Workflow Position:** Called by CLI/import/direct caller or no package caller detected; depends on cli._compare; cli._explain; cli._inspect; cli._reproduce; cli._resolved; cli._score; cli._show; cli._summarize; cli._validate; cli.build_parser; pipeline.run_search. Planned treatment: 13–17; Appendix A.
- **Plain Language Intuition:** It performs one auditable step of command dispatch and user contract; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: control plane; no independent estimator. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/cli.py:403; callers: CLI/import/direct caller or no package caller detected; package dependencies: cli._compare; cli._explain; cli._inspect; cli._reproduce; cli._resolved; cli._score; cli._show; cli._summarize; cli._validate; cli.build_parser; pipeline.run_search.
- **Inputs And Shapes:** Signature `argv: list[str] | None=None`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–3. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–3 command records. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–3 command records. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `int`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of command dispatch and user contract. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_freeze3_comparison_validation.py::test_cli_compare_end_to_end. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects CLI/import/direct caller or no package caller detected to cli._compare; cli._explain; cli._inspect; cli._reproduce; cli._resolved; cli._score; cli._show; cli._summarize; cli._validate; cli.build_parser; pipeline.run_search; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `comparison.run_comparison` (Tier A)

- **Name And Scientific Purpose:** `comparison.run_comparison`: Compare two label artifacts using exact IDs, permutation-invariant structure, noise sets, mapping, and optional coordinates. Its documented role is ID-safe structural comparison.
- **Workflow Position:** Called by cli._compare; depends on comparison._columns; comparison._resolve_labels; comparison._variation_of_information; interpretation.detect_coordinate_columns; interpretation.is_noise_label; interpretation.label_sort_key; io.atomic_json_dump; io.ensure_empty_output_dir; io.json_safe; io.validated_identifiers; provenance.base_manifest; provenance.file_record; provenance.utc_now. Planned treatment: 12, 16, 21, 23.
- **Plain Language Intuition:** It performs one auditable step of ID-safe structural comparison; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: ARI/NMI/VI, noise-set overlap, label assignment, and coordinate alignment. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/comparison.py:65; callers: cli._compare; package dependencies: comparison._columns; comparison._resolve_labels; comparison._variation_of_information; interpretation.detect_coordinate_columns; interpretation.is_noise_label; interpretation.label_sort_key; io.atomic_json_dump; io.ensure_empty_output_dir; io.json_safe; io.validated_identifiers; provenance.base_manifest; provenance.file_record; provenance.utc_now.
- **Inputs And Shapes:** Signature `left_source: str | Path, right_source: str | Path, output_dir: str | Path, *, id_column: str='feature_id', label_column: str='label', require_same_order: bool=False, command: list[str] | None=None`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 0 and 3. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 0 label example and Lab 3 comparison. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 0 label example and Lab 3 comparison. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict[str, Any]`. Direct canonical artifacts: comparison_summary.json; membership_comparison.tsv; cluster_sizes.tsv; label_confusion.tsv; optimal_label_mapping.tsv; comparison_manifest.json.
- **Result Interpretation:** Interpret results at the level of ID-safe structural comparison. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_freeze3_comparison_validation.py::test_comparison_rejects_duplicate_ids; tests/test_freeze3_comparison_validation.py::test_comparison_requires_identical_id_sets; tests/test_freeze3_comparison_validation.py::test_label_permutation_comparison_is_structurally_equal. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: writes files/directories. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli._compare to comparison._columns; comparison._resolve_labels; comparison._variation_of_information; interpretation.detect_coordinate_columns; interpretation.is_noise_label; interpretation.label_sort_key; io.atomic_json_dump; io.ensure_empty_output_dir; io.json_safe; io.validated_identifiers; provenance.base_manifest; provenance.file_record; provenance.utc_now; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `config.builtin_config` (Tier B)

- **Name And Scientific Purpose:** `config.builtin_config`: Implementation callable for builtin config. Its documented role is configuration resolution and validation.
- **Workflow Position:** Called by config.resolve_config; depends on config._base_config. Planned treatment: 6, 10, 14; Appendix B.
- **Plain Language Intuition:** It performs one auditable step of configuration resolution and validation; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: deterministic precedence and Cartesian parameter specification. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/config.py:128; callers: config.resolve_config; package dependencies: config._base_config.
- **Inputs And Shapes:** Signature `mode: str`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 1 inspect-config/show-search-space. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–2 inspect-config. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–2 inspect-config. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict[str, Any]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of configuration resolution and validation. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects config.resolve_config to config._base_config; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `config.deep_merge` (Tier B)

- **Name And Scientific Purpose:** `config.deep_merge`: Implementation callable for deep merge. Its documented role is configuration resolution and validation.
- **Workflow Position:** Called by config.resolve_config; depends on No package-defined dependency detected. Planned treatment: 6, 10, 14; Appendix B.
- **Plain Language Intuition:** It performs one auditable step of configuration resolution and validation; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: deterministic precedence and Cartesian parameter specification. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/config.py:164; callers: config.resolve_config; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `base: Mapping[str, Any], overlay: Mapping[str, Any]`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 1 inspect-config/show-search-space. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–2 inspect-config. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–2 inspect-config. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict[str, Any]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of configuration resolution and validation. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects config.resolve_config to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `config.load_yaml` (Tier B)

- **Name And Scientific Purpose:** `config.load_yaml`: Implementation callable for load yaml. Its documented role is configuration resolution and validation.
- **Workflow Position:** Called by config.resolve_config; depends on No package-defined dependency detected. Planned treatment: 6, 10, 14; Appendix B.
- **Plain Language Intuition:** It performs one auditable step of configuration resolution and validation; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: deterministic precedence and Cartesian parameter specification. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/config.py:174; callers: config.resolve_config; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `path: str | Path`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 1 inspect-config/show-search-space. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–2 inspect-config. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–2 inspect-config. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict[str, Any]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of configuration resolution and validation. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: FileNotFoundError; RuntimeError; ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects config.resolve_config to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `config.set_dotted` (Tier B)

- **Name And Scientific Purpose:** `config.set_dotted`: Implementation callable for set dotted. Its documented role is configuration resolution and validation.
- **Workflow Position:** Called by config.resolve_config; depends on No package-defined dependency detected. Planned treatment: 6, 10, 14; Appendix B.
- **Plain Language Intuition:** It performs one auditable step of configuration resolution and validation; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: deterministic precedence and Cartesian parameter specification. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/config.py:191; callers: config.resolve_config; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `config: dict[str, Any], dotted: str, value: Any`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 1 inspect-config/show-search-space. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–2 inspect-config. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–2 inspect-config. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `None`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of configuration resolution and validation. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects config.resolve_config to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `config.resolve_config` (Tier A)

- **Name And Scientific Purpose:** `config.resolve_config`: Implementation callable for resolve config. Its documented role is configuration resolution and validation.
- **Workflow Position:** Called by cli._explain; cli._reproduce; cli._resolved; cli._score; depends on config.builtin_config; config.deep_merge; config.load_yaml; config.set_dotted; config.validate_config. Planned treatment: 6, 10, 14; Appendix B.
- **Plain Language Intuition:** It performs one auditable step of configuration resolution and validation; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: deterministic precedence and Cartesian parameter specification. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/config.py:203; callers: cli._explain; cli._reproduce; cli._resolved; cli._score; package dependencies: config.builtin_config; config.deep_merge; config.load_yaml; config.set_dotted; config.validate_config.
- **Inputs And Shapes:** Signature `mode: str, config_path: str | Path | None=None, overrides: Mapping[str, Any] | None=None`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 1 inspect-config/show-search-space. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–2 inspect-config. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–2 inspect-config. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict[str, Any]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of configuration resolution and validation. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_config.py::test_cli_override_precedence; tests/test_config.py::test_fixed_mode_rejects_lists; tests/test_config.py::test_invalid_combinations_rejected; tests/test_config.py::test_standard_defaults_match_dev_declarations; tests/test_freeze3_interpretation.py::test_interpretation_defaults_are_additive; tests/test_freeze3_interpretation.py::test_invalid_interpretation_configuration_fails; tests/test_freeze3_interpretation.py::test_legacy_incomplete_matching_writes_exclusions; tests/test_freeze3_interpretation.py::test_native_explanation_end_to_end; tests/test_freeze3_interpretation.py::test_native_explanation_refuses_nonempty_output; tests/test_search_space.py::test_search_enumeration_and_stable_ids; tests/test_search_space.py::test_search_limit_never_silently_samples. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli._explain; cli._reproduce; cli._resolved; cli._score to config.builtin_config; config.deep_merge; config.load_yaml; config.set_dotted; config.validate_config; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `config.as_list` (Tier B)

- **Name And Scientific Purpose:** `config.as_list`: Implementation callable for as list. Its documented role is configuration resolution and validation.
- **Workflow Position:** Called by config.normalized_parameter_space; depends on config._coerce_bool; config._range_values; config._string_sequence. Planned treatment: 6, 10, 14; Appendix B.
- **Plain Language Intuition:** It performs one auditable step of configuration resolution and validation; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: deterministic precedence and Cartesian parameter specification. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/config.py:277; callers: config.normalized_parameter_space; package dependencies: config._coerce_bool; config._range_values; config._string_sequence.
- **Inputs And Shapes:** Signature `value: Any, cast: type | None=None`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 1 inspect-config/show-search-space. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–2 inspect-config. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–2 inspect-config. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `list[Any]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of configuration resolution and validation. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_config.py::test_scalar_list_and_range_handling. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects config.normalized_parameter_space to config._coerce_bool; config._range_values; config._string_sequence; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `config.normalized_parameter_space` (Tier A)

- **Name And Scientific Purpose:** `config.normalized_parameter_space`: Implementation callable for normalized parameter space. Its documented role is configuration resolution and validation.
- **Workflow Position:** Called by config.validate_config; search_space.count_candidates; search_space.enumerate_candidates; depends on config.as_list. Planned treatment: 6, 10, 14; Appendix B.
- **Plain Language Intuition:** It performs one auditable step of configuration resolution and validation; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: deterministic precedence and Cartesian parameter specification. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/config.py:298; callers: config.validate_config; search_space.count_candidates; search_space.enumerate_candidates; package dependencies: config.as_list.
- **Inputs And Shapes:** Signature `config: Mapping[str, Any]`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 1 inspect-config/show-search-space. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–2 inspect-config. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–2 inspect-config. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict[str, dict[str, list[Any]]]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of configuration resolution and validation. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_config.py::test_cli_override_precedence. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects config.validate_config; search_space.count_candidates; search_space.enumerate_candidates to config.as_list; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `config.validate_config` (Tier A)

- **Name And Scientific Purpose:** `config.validate_config`: Implementation callable for validate config. Its documented role is configuration resolution and validation.
- **Workflow Position:** Called by cli._explain; cli._reproduce; config.resolve_config; depends on config._finite; config.normalized_parameter_space. Planned treatment: 6, 10, 14; Appendix B.
- **Plain Language Intuition:** It performs one auditable step of configuration resolution and validation; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: deterministic precedence and Cartesian parameter specification. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/config.py:343; callers: cli._explain; cli._reproduce; config.resolve_config; package dependencies: config._finite; config.normalized_parameter_space.
- **Inputs And Shapes:** Signature `config: Mapping[str, Any]`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 1 inspect-config/show-search-space. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–2 inspect-config. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–2 inspect-config. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `None`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of configuration resolution and validation. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli._explain; cli._reproduce; config.resolve_config to config._finite; config.normalized_parameter_space; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `config.config_as_json` (Tier B)

- **Name And Scientific Purpose:** `config.config_as_json`: Implementation callable for config as json. Its documented role is configuration resolution and validation.
- **Workflow Position:** Called by CLI/import/direct caller or no package caller detected; depends on No package-defined dependency detected. Planned treatment: 6, 10, 14; Appendix B.
- **Plain Language Intuition:** It performs one auditable step of configuration resolution and validation; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: deterministic precedence and Cartesian parameter specification. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/config.py:489; callers: CLI/import/direct caller or no package caller detected; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `config: Mapping[str, Any]`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 1 inspect-config/show-search-space. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–2 inspect-config. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–2 inspect-config. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `str`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of configuration resolution and validation. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects CLI/import/direct caller or no package caller detected to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `hdbscan_runner.estimator_kwargs` (Tier B)

- **Name And Scientific Purpose:** `hdbscan_runner.estimator_kwargs`: Implementation callable for estimator kwargs. Its documented role is density-clustering execution.
- **Workflow Position:** Called by hdbscan_runner.fit_hdbscan; depends on No package-defined dependency detected. Planned treatment: 9.
- **Plain Language Intuition:** It performs one auditable step of density-clustering execution; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: core distance, mutual reachability, hierarchy, stability, and noise assignment. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/hdbscan_runner.py:15; callers: hdbscan_runner.fit_hdbscan; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `parameters: Mapping[str, Any], core_dist_n_jobs: int=1`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–2 candidate fitting. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–2 candidate fits. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–2 candidate fits. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict[str, Any]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of density-clustering execution. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects hdbscan_runner.fit_hdbscan to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `hdbscan_runner.fit_hdbscan` (Tier A)

- **Name And Scientific Purpose:** `hdbscan_runner.fit_hdbscan`: Fit contributed HDBSCAN with normalized Freeze 3 parameters. Its documented role is density-clustering execution.
- **Workflow Position:** Called by pipeline._evaluate_one; pipeline.run_search; depends on hdbscan_runner.estimator_kwargs. Planned treatment: 9.
- **Plain Language Intuition:** It performs one auditable step of density-clustering execution; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: core distance, mutual reachability, hierarchy, stability, and noise assignment. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/hdbscan_runner.py:34; callers: pipeline._evaluate_one; pipeline.run_search; package dependencies: hdbscan_runner.estimator_kwargs.
- **Inputs And Shapes:** Signature `embedding, parameters: Mapping[str, Any], core_dist_n_jobs: int=1`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–2 candidate fitting. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–2 candidate fits. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–2 candidate fits. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict[str, Any]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of density-clustering execution. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_failure_and_provenance.py::test_failed_candidate_is_retained. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: fits numerical model. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects pipeline._evaluate_one; pipeline.run_search to hdbscan_runner.estimator_kwargs; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `interpretation.is_noise_label` (Tier B)

- **Name And Scientific Purpose:** `interpretation.is_noise_label`: Implementation callable for is noise label. Its documented role is post-selection original-space description.
- **Workflow Position:** Called by comparison.run_comparison; interpretation.calculate_cluster_summary; interpretation.label_sort_key; interpretation.run_explanation; depends on No package-defined dependency detected. Planned treatment: 17, 21.
- **Plain Language Intuition:** It performs one auditable step of post-selection original-space description; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: Pearson/Spearman association, ordering, heatmaps, and circularity safeguards. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/interpretation.py:30; callers: comparison.run_comparison; interpretation.calculate_cluster_summary; interpretation.label_sort_key; interpretation.run_explanation; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `value: Any`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 3 explanation. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 3 explanation. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 3 explanation. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `bool`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of post-selection original-space description. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects comparison.run_comparison; interpretation.calculate_cluster_summary; interpretation.label_sort_key; interpretation.run_explanation to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `interpretation.label_sort_key` (Tier B)

- **Name And Scientific Purpose:** `interpretation.label_sort_key`: Implementation callable for label sort key. Its documented role is post-selection original-space description.
- **Workflow Position:** Called by comparison.run_comparison; interpretation.compute_order; depends on interpretation.is_noise_label. Planned treatment: 17, 21.
- **Plain Language Intuition:** It performs one auditable step of post-selection original-space description; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: Pearson/Spearman association, ordering, heatmaps, and circularity safeguards. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/interpretation.py:35; callers: comparison.run_comparison; interpretation.compute_order; package dependencies: interpretation.is_noise_label.
- **Inputs And Shapes:** Signature `value: Any`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 3 explanation. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 3 explanation. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 3 explanation. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `tuple[int, float | str]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of post-selection original-space description. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects comparison.run_comparison; interpretation.compute_order to interpretation.is_noise_label; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `interpretation.detect_coordinate_columns` (Tier B)

- **Name And Scientific Purpose:** `interpretation.detect_coordinate_columns`: Implementation callable for detect coordinate columns. Its documented role is post-selection original-space description.
- **Workflow Position:** Called by comparison.run_comparison; interpretation.run_explanation; depends on No package-defined dependency detected. Planned treatment: 17, 21.
- **Plain Language Intuition:** It performs one auditable step of post-selection original-space description; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: Pearson/Spearman association, ordering, heatmaps, and circularity safeguards. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/interpretation.py:44; callers: comparison.run_comparison; interpretation.run_explanation; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `frame, requested: Sequence[str] | str | None=None`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 3 explanation. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 3 explanation. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 3 explanation. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `list[str]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of post-selection original-space description. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_freeze3_interpretation.py::test_coordinate_detection_is_numeric_suffix_order. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects comparison.run_comparison; interpretation.run_explanation to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `interpretation.compute_similarity` (Tier A)

- **Name And Scientific Purpose:** `interpretation.compute_similarity`: Implementation callable for compute similarity. Its documented role is post-selection original-space description.
- **Workflow Position:** Called by interpretation.run_explanation; depends on No package-defined dependency detected. Planned treatment: 17, 21.
- **Plain Language Intuition:** It performs one auditable step of post-selection original-space description; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: Pearson/Spearman association, ordering, heatmaps, and circularity safeguards. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/interpretation.py:145; callers: interpretation.run_explanation; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `analysis, *, method: str, undefined_policy: str`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 3 explanation. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 3 explanation. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 3 explanation. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `not annotated`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of post-selection original-space description. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_freeze3_interpretation.py::test_similarity_undefined_fails_by_default. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects interpretation.run_explanation to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `interpretation.compute_order` (Tier A)

- **Name And Scientific Purpose:** `interpretation.compute_order`: Implementation callable for compute order. Its documented role is post-selection original-space description.
- **Workflow Position:** Called by interpretation.run_explanation; depends on interpretation._hierarchical_order; interpretation.label_sort_key. Planned treatment: 17, 21.
- **Plain Language Intuition:** It performs one auditable step of post-selection original-space description; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: Pearson/Spearman association, ordering, heatmaps, and circularity safeguards. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/interpretation.py:184; callers: interpretation.run_explanation; package dependencies: interpretation._hierarchical_order; interpretation.label_sort_key.
- **Inputs And Shapes:** Signature `correlation, labels: Sequence[Any], *, method: str, noise_policy: str`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 3 explanation. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 3 explanation. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 3 explanation. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `list[int]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of post-selection original-space description. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_freeze3_interpretation.py::test_cluster_order_is_numeric_and_noise_last. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects interpretation.run_explanation to interpretation._hierarchical_order; interpretation.label_sort_key; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `interpretation.calculate_cutpoints` (Tier B)

- **Name And Scientific Purpose:** `interpretation.calculate_cutpoints`: Implementation callable for calculate cutpoints. Its documented role is post-selection original-space description.
- **Workflow Position:** Called by interpretation.run_explanation; depends on No package-defined dependency detected. Planned treatment: 17, 21.
- **Plain Language Intuition:** It performs one auditable step of post-selection original-space description; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: Pearson/Spearman association, ordering, heatmaps, and circularity safeguards. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/interpretation.py:209; callers: interpretation.run_explanation; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `labels: Sequence[Any]`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 3 explanation. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 3 explanation. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 3 explanation. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `not annotated`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of post-selection original-space description. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_freeze3_interpretation.py::test_cutpoint_indices_are_auditable. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects interpretation.run_explanation to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `interpretation.calculate_cluster_summary` (Tier B)

- **Name And Scientific Purpose:** `interpretation.calculate_cluster_summary`: Implementation callable for calculate cluster summary. Its documented role is post-selection original-space description.
- **Workflow Position:** Called by interpretation.run_explanation; depends on interpretation.is_noise_label. Planned treatment: 17, 21.
- **Plain Language Intuition:** It performs one auditable step of post-selection original-space description; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: Pearson/Spearman association, ordering, heatmaps, and circularity safeguards. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/interpretation.py:233; callers: interpretation.run_explanation; package dependencies: interpretation.is_noise_label.
- **Inputs And Shapes:** Signature `correlation, labels: Sequence[Any]`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 3 explanation. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 3 explanation. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 3 explanation. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `not annotated`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of post-selection original-space description. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects interpretation.run_explanation to interpretation.is_noise_label; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `interpretation.coordinate_association_table` (Tier A)

- **Name And Scientific Purpose:** `interpretation.coordinate_association_table`: Implementation callable for coordinate association table. Its documented role is post-selection original-space description.
- **Workflow Position:** Called by interpretation.run_explanation; depends on No package-defined dependency detected. Planned treatment: 17, 21.
- **Plain Language Intuition:** It performs one auditable step of post-selection original-space description; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: Pearson/Spearman association, ordering, heatmaps, and circularity safeguards. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/interpretation.py:262; callers: interpretation.run_explanation; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `analysis, coordinates, *, methods: Sequence[str], top_n: int`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 3 explanation. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 3 explanation. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 3 explanation. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `not annotated`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of post-selection original-space description. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects interpretation.run_explanation to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `interpretation.run_explanation` (Tier A)

- **Name And Scientific Purpose:** `interpretation.run_explanation`: Return to original input space, align IDs, calculate similarities/summaries, order a heatmap, and record a non-refitting explanation manifest. Its documented role is post-selection original-space description.
- **Workflow Position:** Called by cli._explain; depends on interpretation._align_inputs; interpretation._native_sources; interpretation._resolve_column; interpretation._write_readme; interpretation.calculate_cluster_summary; interpretation.calculate_cutpoints; interpretation.compute_order; interpretation.compute_similarity; interpretation.coordinate_association_table; interpretation.detect_coordinate_columns; interpretation.is_noise_label; io.atomic_json_dump; io.ensure_empty_output_dir; io.json_safe; io.read_table; io.validated_identifiers; metrics.embedding_quality_metrics; preprocessing.infer_explanation_orientation; preprocessing.prepare_explanation_matrix; provenance.base_manifest; provenance.file_record; provenance.utc_now; visualization.render_heatmap. Planned treatment: 17, 21.
- **Plain Language Intuition:** It performs one auditable step of post-selection original-space description; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: Pearson/Spearman association, ordering, heatmaps, and circularity safeguards. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/interpretation.py:307; callers: cli._explain; package dependencies: interpretation._align_inputs; interpretation._native_sources; interpretation._resolve_column; interpretation._write_readme; interpretation.calculate_cluster_summary; interpretation.calculate_cutpoints; interpretation.compute_order; interpretation.compute_similarity; interpretation.coordinate_association_table; interpretation.detect_coordinate_columns; interpretation.is_noise_label; io.atomic_json_dump; io.ensure_empty_output_dir; io.json_safe; io.read_table; io.validated_identifiers; metrics.embedding_quality_metrics; preprocessing.infer_explanation_orientation; preprocessing.prepare_explanation_matrix; provenance.base_manifest; provenance.file_record; provenance.utc_now; visualization.render_heatmap.
- **Inputs And Shapes:** Signature `*, output_dir: str | Path, interpretation_config: Mapping[str, Any], model_json: str | Path | None=None, legacy_table: str | Path | None=None, input_path: str | Path | None=None, input_sep: str | None=None, input_sheet: str | int=0, legacy_sheet: str | int=0, matrix_orientation: str='auto', vector_id_source: str='auto', drop_first_n_cols: int | None=None, zscore_transform: str | None=None, id_column: str | None=None, label_column: str | None=None, coordinate_columns: Sequence[str] | str | None=None, command: list[str] | None=None`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 3 explanation. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 3 explanation. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 3 explanation. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict[str, Any]`. Direct canonical artifacts: original_space_similarity.tsv.gz; heatmap_order.tsv; cluster_cutpoints.tsv; cluster_summary.tsv; projection_quality.tsv; coordinate_associations.tsv; exclusions.tsv; original_space_heatmap.png; original_space_heatmap.html; interpretation_manifest.json; README.md.
- **Result Interpretation:** Interpret results at the level of post-selection original-space description. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_freeze3_interpretation.py::test_legacy_incomplete_matching_writes_exclusions; tests/test_freeze3_interpretation.py::test_native_explanation_end_to_end; tests/test_freeze3_interpretation.py::test_native_explanation_refuses_nonempty_output. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: writes files/directories. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli._explain to interpretation._align_inputs; interpretation._native_sources; interpretation._resolve_column; interpretation._write_readme; interpretation.calculate_cluster_summary; interpretation.calculate_cutpoints; interpretation.compute_order; interpretation.compute_similarity; interpretation.coordinate_association_table; interpretation.detect_coordinate_columns; interpretation.is_noise_label; io.atomic_json_dump; io.ensure_empty_output_dir; io.json_safe; io.read_table; io.validated_identifiers; metrics.embedding_quality_metrics; preprocessing.infer_explanation_orientation; preprocessing.prepare_explanation_matrix; provenance.base_manifest; provenance.file_record; provenance.utc_now; visualization.render_heatmap; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `io.resolve_separator` (Tier B)

- **Name And Scientific Purpose:** `io.resolve_separator`: Implementation callable for resolve separator. Its documented role is validated tabular and atomic artifact I/O.
- **Workflow Position:** Called by io.read_model_table; io.read_table; depends on No package-defined dependency detected. Planned treatment: 6, 13–17.
- **Plain Language Intuition:** It performs one auditable step of validated tabular and atomic artifact I/O; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: identifier integrity and transactional file writing. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/io.py:10; callers: io.read_model_table; io.read_table; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `path: str | Path, override: str | None=None`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 0–3. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–3 artifacts. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–3 artifacts. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `str`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of validated tabular and atomic artifact I/O. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects io.read_model_table; io.read_table to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `io.read_table` (Tier A)

- **Name And Scientific Purpose:** `io.read_table`: Implementation callable for read table. Its documented role is validated tabular and atomic artifact I/O.
- **Workflow Position:** Called by comparison._resolve_labels; interpretation.run_explanation; pipeline._annotation_frame; pipeline.run_search; validation.run_validation; depends on io.resolve_separator. Planned treatment: 6, 13–17.
- **Plain Language Intuition:** It performs one auditable step of validated tabular and atomic artifact I/O; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: identifier integrity and transactional file writing. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/io.py:16; callers: comparison._resolve_labels; interpretation.run_explanation; pipeline._annotation_frame; pipeline.run_search; validation.run_validation; package dependencies: io.resolve_separator.
- **Inputs And Shapes:** Signature `path: str | Path, sep: str | None=None, *, sheet: str | int=0, nrows: int | None=None`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 0–3. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–3 artifacts. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–3 artifacts. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `not annotated`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of validated tabular and atomic artifact I/O. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_freeze3_interpretation.py::test_reader_supports_excel_sheet. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: FileNotFoundError; RuntimeError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects comparison._resolve_labels; interpretation.run_explanation; pipeline._annotation_frame; pipeline.run_search; validation.run_validation to io.resolve_separator; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `io.read_model_table` (Tier B)

- **Name And Scientific Purpose:** `io.read_model_table`: Implementation callable for read model table. Its documented role is validated tabular and atomic artifact I/O.
- **Workflow Position:** Called by cli._score; cli._summarize; validation.run_validation; depends on io.resolve_separator. Planned treatment: 6, 13–17.
- **Plain Language Intuition:** It performs one auditable step of validated tabular and atomic artifact I/O; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: identifier integrity and transactional file writing. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/io.py:45; callers: cli._score; cli._summarize; validation.run_validation; package dependencies: io.resolve_separator.
- **Inputs And Shapes:** Signature `path: str | Path`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 0–3. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–3 artifacts. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–3 artifacts. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `not annotated`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of validated tabular and atomic artifact I/O. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli._score; cli._summarize; validation.run_validation to io.resolve_separator; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `io.ensure_empty_output_dir` (Tier B)

- **Name And Scientific Purpose:** `io.ensure_empty_output_dir`: Create an output directory, refusing to mix with existing artifacts. Its documented role is validated tabular and atomic artifact I/O.
- **Workflow Position:** Called by comparison.run_comparison; interpretation.run_explanation; validation.run_validation; depends on No package-defined dependency detected. Planned treatment: 6, 13–17.
- **Plain Language Intuition:** It performs one auditable step of validated tabular and atomic artifact I/O; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: identifier integrity and transactional file writing. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/io.py:54; callers: comparison.run_comparison; interpretation.run_explanation; validation.run_validation; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `path: str | Path`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 0–3. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–3 artifacts. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–3 artifacts. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `Path`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of validated tabular and atomic artifact I/O. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_freeze3_interpretation.py::test_empty_output_directory_helper. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: writes files/directories. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects comparison.run_comparison; interpretation.run_explanation; validation.run_validation to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `io.normalize_identifier` (Tier B)

- **Name And Scientific Purpose:** `io.normalize_identifier`: Return the exact string identity after removing surrounding whitespace. Its documented role is validated tabular and atomic artifact I/O.
- **Workflow Position:** Called by io.validated_identifiers; preprocessing._unique_feature_names; preprocessing.infer_explanation_orientation; depends on No package-defined dependency detected. Planned treatment: 6, 13–17.
- **Plain Language Intuition:** It performs one auditable step of validated tabular and atomic artifact I/O; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: identifier integrity and transactional file writing. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/io.py:68; callers: io.validated_identifiers; preprocessing._unique_feature_names; preprocessing.infer_explanation_orientation; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `value: Any`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 0–3. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–3 artifacts. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–3 artifacts. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `str`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of validated tabular and atomic artifact I/O. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects io.validated_identifiers; preprocessing._unique_feature_names; preprocessing.infer_explanation_orientation to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `io.validated_identifiers` (Tier A)

- **Name And Scientific Purpose:** `io.validated_identifiers`: Normalize identifiers and reject missing or duplicate identities. Its documented role is validated tabular and atomic artifact I/O.
- **Workflow Position:** Called by comparison.run_comparison; interpretation._align_inputs; interpretation.run_explanation; preprocessing.infer_explanation_orientation; preprocessing.prepare_explanation_matrix; depends on io.normalize_identifier. Planned treatment: 6, 13–17.
- **Plain Language Intuition:** It performs one auditable step of validated tabular and atomic artifact I/O; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: identifier integrity and transactional file writing. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/io.py:81; callers: comparison.run_comparison; interpretation._align_inputs; interpretation.run_explanation; preprocessing.infer_explanation_orientation; preprocessing.prepare_explanation_matrix; package dependencies: io.normalize_identifier.
- **Inputs And Shapes:** Signature `values, *, context: str`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 0–3. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–3 artifacts. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–3 artifacts. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `list[str]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of validated tabular and atomic artifact I/O. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_freeze3_interpretation.py::test_validated_identifiers_strip_but_reject_duplicates. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects comparison.run_comparison; interpretation._align_inputs; interpretation.run_explanation; preprocessing.infer_explanation_orientation; preprocessing.prepare_explanation_matrix to io.normalize_identifier; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `io.atomic_json_dump` (Tier B)

- **Name And Scientific Purpose:** `io.atomic_json_dump`: Implementation callable for atomic json dump. Its documented role is validated tabular and atomic artifact I/O.
- **Workflow Position:** Called by cli._score; cli._summarize; comparison.run_comparison; interpretation.run_explanation; reporting._top_artifact; reporting.write_model_outputs; reporting.write_search_space; validation.run_validation; depends on No package-defined dependency detected. Planned treatment: 6, 13–17.
- **Plain Language Intuition:** It performs one auditable step of validated tabular and atomic artifact I/O; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: identifier integrity and transactional file writing. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/io.py:99; callers: cli._score; cli._summarize; comparison.run_comparison; interpretation.run_explanation; reporting._top_artifact; reporting.write_model_outputs; reporting.write_search_space; validation.run_validation; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `value: Any, path: str | Path`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 0–3. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–3 artifacts. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–3 artifacts. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `None`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of validated tabular and atomic artifact I/O. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: writes files/directories. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli._score; cli._summarize; comparison.run_comparison; interpretation.run_explanation; reporting._top_artifact; reporting.write_model_outputs; reporting.write_search_space; validation.run_validation to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `io.json_safe` (Tier B)

- **Name And Scientific Purpose:** `io.json_safe`: Implementation callable for json safe. Its documented role is validated tabular and atomic artifact I/O.
- **Workflow Position:** Called by cli._score; cli._show; comparison.run_comparison; interpretation.run_explanation; reporting._top_artifact; reporting.write_model_outputs; reporting.write_search_space; validation.run_validation; depends on No package-defined dependency detected. Planned treatment: 6, 13–17.
- **Plain Language Intuition:** It performs one auditable step of validated tabular and atomic artifact I/O; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: identifier integrity and transactional file writing. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/io.py:109; callers: cli._score; cli._show; comparison.run_comparison; interpretation.run_explanation; reporting._top_artifact; reporting.write_model_outputs; reporting.write_search_space; validation.run_validation; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `value: Any`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 0–3. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–3 artifacts. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–3 artifacts. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `Any`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of validated tabular and atomic artifact I/O. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli._score; cli._show; comparison.run_comparison; interpretation.run_explanation; reporting._top_artifact; reporting.write_model_outputs; reporting.write_search_space; validation.run_validation to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `metrics.effective_neighbor_count` (Tier B)

- **Name And Scientific Purpose:** `metrics.effective_neighbor_count`: Implementation callable for effective neighbor count. Its documented role is candidate and representation diagnostics.
- **Workflow Position:** Called by metrics.embedding_quality_metrics; depends on No package-defined dependency detected. Planned treatment: 7, 9, 11.
- **Plain Language Intuition:** It performs one auditable step of candidate and representation diagnostics; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: silhouette, CH, DB, DBCV, trustworthiness, continuity, persistence, and cluster-size summaries. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/metrics.py:9; callers: metrics.embedding_quality_metrics; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `n_samples: int, requested: int`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 0 hand calculation; Lab 2 executed diagnostics. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 0 silhouette and Labs 1–2 model tables. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 0 silhouette and Labs 1–2 model tables. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `int`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of candidate and representation diagnostics. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_preprocessing_metrics.py::test_effective_neighbor_edge_cases. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects metrics.embedding_quality_metrics to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `metrics.embedding_quality_metrics` (Tier A)

- **Name And Scientific Purpose:** `metrics.embedding_quality_metrics`: Calculate bounded trustworthiness and continuity diagnostics for an embedding. Its documented role is candidate and representation diagnostics.
- **Workflow Position:** Called by interpretation.run_explanation; pipeline.run_search; depends on metrics.effective_neighbor_count. Planned treatment: 7, 9, 11.
- **Plain Language Intuition:** It performs one auditable step of candidate and representation diagnostics; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: silhouette, CH, DB, DBCV, trustworthiness, continuity, persistence, and cluster-size summaries. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/metrics.py:15; callers: interpretation.run_explanation; pipeline.run_search; package dependencies: metrics.effective_neighbor_count.
- **Inputs And Shapes:** Signature `original, embedding, requested_k: int, max_samples: int, seed: int`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 0 hand calculation; Lab 2 executed diagnostics. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 0 silhouette and Labs 1–2 model tables. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 0 silhouette and Labs 1–2 model tables. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict[str, Any]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of candidate and representation diagnostics. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_preprocessing_metrics.py::test_optimized_trustworthiness_and_continuity. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects interpretation.run_explanation; pipeline.run_search to metrics.effective_neighbor_count; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `metrics.evaluate_candidate` (Tier A)

- **Name And Scientific Purpose:** `metrics.evaluate_candidate`: Compute cluster counts, persistence, silhouette, CH, DB, optional DBCV, and validity status for one candidate. Its documented role is candidate and representation diagnostics.
- **Workflow Position:** Called by pipeline._evaluate_one; depends on metrics._cluster_sizes. Planned treatment: 7, 9, 11.
- **Plain Language Intuition:** It performs one auditable step of candidate and representation diagnostics; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: silhouette, CH, DB, DBCV, trustworthiness, continuity, persistence, and cluster-size summaries. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/metrics.py:60; callers: pipeline._evaluate_one; package dependencies: metrics._cluster_sizes.
- **Inputs And Shapes:** Signature `embedding, labels, clusterer, silhouette_metric: str, fit_include_noise: bool, compute_dbcv: bool, max_samples_silhouette: int=0, silhouette_seed: int=42`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 0 hand calculation; Lab 2 executed diagnostics. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 0 silhouette and Labs 1–2 model tables. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 0 silhouette and Labs 1–2 model tables. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict[str, Any]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of candidate and representation diagnostics. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects pipeline._evaluate_one to metrics._cluster_sizes; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `metrics.is_finite_number` (Tier B)

- **Name And Scientific Purpose:** `metrics.is_finite_number`: Implementation callable for is finite number. Its documented role is candidate and representation diagnostics.
- **Workflow Position:** Called by CLI/import/direct caller or no package caller detected; depends on No package-defined dependency detected. Planned treatment: 7, 9, 11.
- **Plain Language Intuition:** It performs one auditable step of candidate and representation diagnostics; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: silhouette, CH, DB, DBCV, trustworthiness, continuity, persistence, and cluster-size summaries. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/metrics.py:165; callers: CLI/import/direct caller or no package caller detected; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `value: Any`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 0 hand calculation; Lab 2 executed diagnostics. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 0 silhouette and Labs 1–2 model tables. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 0 silhouette and Labs 1–2 model tables. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `bool`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of candidate and representation diagnostics. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects CLI/import/direct caller or no package caller detected to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `pipeline.setup_logger` (Tier B)

- **Name And Scientific Purpose:** `pipeline.setup_logger`: Implementation callable for setup logger. Its documented role is end-to-end analytical orchestration.
- **Workflow Position:** Called by pipeline.run_search; depends on No package-defined dependency detected. Planned treatment: 8–12, 15.
- **Plain Language Intuition:** It performs one auditable step of end-to-end analytical orchestration; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: prepared matrix → repeated embedding → density candidates → scoring → retained model. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/pipeline.py:25; callers: pipeline.run_search; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `output_dir: str | Path`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–2. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–2 runs and Lab 3 reproduction. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–2 runs and Lab 3 reproduction. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `logging.Logger`. Direct canonical artifacts: logs/run.log.
- **Result Interpretation:** Interpret results at the level of end-to-end analytical orchestration. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: writes files/directories; emits logs. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects pipeline.run_search to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `pipeline.run_search` (Tier A)

- **Name And Scientific Purpose:** `pipeline.run_search`: Execute preprocessing, repeated embeddings, candidate evaluation, scoring, retention, reporting, and provenance for one run. Its documented role is end-to-end analytical orchestration.
- **Workflow Position:** Called by cli._reproduce; cli.main; depends on hdbscan_runner.fit_hdbscan; io.read_table; metrics.embedding_quality_metrics; pipeline._annotation_frame; pipeline._evaluate_one; pipeline._failed_row; pipeline.setup_logger; preprocessing.prepare_analysis_matrix; provenance.base_manifest; provenance.file_record; ranking.family_summaries; ranking.pareto_front; ranking.rank_models; ranking.top_models; reporting.write_model_outputs; reporting.write_resolved_config; reporting.write_search_space; scoring.apply_scoring; search_space.enumerate_candidates; search_space.stable_identifier; umap_runner.run_repeated_umap. Planned treatment: 8–12, 15.
- **Plain Language Intuition:** It performs one auditable step of end-to-end analytical orchestration; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: prepared matrix → repeated embedding → density candidates → scoring → retained model. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/pipeline.py:130; callers: cli._reproduce; cli.main; package dependencies: hdbscan_runner.fit_hdbscan; io.read_table; metrics.embedding_quality_metrics; pipeline._annotation_frame; pipeline._evaluate_one; pipeline._failed_row; pipeline.setup_logger; preprocessing.prepare_analysis_matrix; provenance.base_manifest; provenance.file_record; ranking.family_summaries; ranking.pareto_front; ranking.rank_models; ranking.top_models; reporting.write_model_outputs; reporting.write_resolved_config; reporting.write_search_space; scoring.apply_scoring; search_space.enumerate_candidates; search_space.stable_identifier; umap_runner.run_repeated_umap.
- **Inputs And Shapes:** Signature `config: Mapping[str, Any], output_dir: str | Path, command: list[str] | None=None`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–2. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–2 runs and Lab 3 reproduction. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–2 runs and Lab 3 reproduction. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict[str, Any]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of end-to-end analytical orchestration. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_pipeline_integration.py::test_custom_leaf_eom_metric_and_max_size_run; tests/test_pipeline_integration.py::test_fixed_model_reproduction. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: RuntimeError; ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: writes files/directories; emits logs. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli._reproduce; cli.main to hdbscan_runner.fit_hdbscan; io.read_table; metrics.embedding_quality_metrics; pipeline._annotation_frame; pipeline._evaluate_one; pipeline._failed_row; pipeline.setup_logger; preprocessing.prepare_analysis_matrix; provenance.base_manifest; provenance.file_record; ranking.family_summaries; ranking.pareto_front; ranking.rank_models; ranking.top_models; reporting.write_model_outputs; reporting.write_resolved_config; reporting.write_search_space; scoring.apply_scoring; search_space.enumerate_candidates; search_space.stable_identifier; umap_runner.run_repeated_umap; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `preprocessing.ExplanationMatrix` (Tier B)

- **Name And Scientific Purpose:** `preprocessing.ExplanationMatrix`: Implementation callable for ExplanationMatrix. Its documented role is input orientation and transformation.
- **Workflow Position:** Called by preprocessing.prepare_explanation_matrix; depends on No package-defined dependency detected. Planned treatment: 3, 6, 18.
- **Plain Language Intuition:** It performs one auditable step of input orientation and transformation; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: numeric coercion, missingness rejection, transpose, RINT, and explanation orientation. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/preprocessing.py:12; callers: preprocessing.prepare_explanation_matrix; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `class construction/data container`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 0 hand-worked matrix; Lab 1 executed fixture. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 0 RINT and Lab 1 input contract. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 0 RINT and Lab 1 input contract. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `not annotated`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of input orientation and transformation. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects preprocessing.prepare_explanation_matrix to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `preprocessing.rank_inverse_normal_transform` (Tier A)

- **Name And Scientific Purpose:** `preprocessing.rank_inverse_normal_transform`: Apply the implementation's rank-based inverse-normal transform to numeric analysis columns. Its documented role is input orientation and transformation.
- **Workflow Position:** Called by preprocessing.prepare_analysis_matrix; preprocessing.prepare_explanation_matrix; depends on No package-defined dependency detected. Planned treatment: 3, 6, 18.
- **Plain Language Intuition:** It performs one auditable step of input orientation and transformation; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: numeric coercion, missingness rejection, transpose, RINT, and explanation orientation. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/preprocessing.py:19; callers: preprocessing.prepare_analysis_matrix; preprocessing.prepare_explanation_matrix; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `frame`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 0 hand-worked matrix; Lab 1 executed fixture. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 0 RINT and Lab 1 input contract. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 0 RINT and Lab 1 input contract. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `not annotated`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of input orientation and transformation. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_preprocessing_metrics.py::test_rint_and_numeric_matrix. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects preprocessing.prepare_analysis_matrix; preprocessing.prepare_explanation_matrix to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `preprocessing.prepare_analysis_matrix` (Tier A)

- **Name And Scientific Purpose:** `preprocessing.prepare_analysis_matrix`: Validate the input contract, remove metadata, transform if requested, transpose, and return vector-by-variant analysis data. Its documented role is input orientation and transformation.
- **Workflow Position:** Called by pipeline.run_search; depends on preprocessing.rank_inverse_normal_transform. Planned treatment: 3, 6, 18.
- **Plain Language Intuition:** It performs one auditable step of input orientation and transformation; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: numeric coercion, missingness rejection, transpose, RINT, and explanation orientation. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/preprocessing.py:34; callers: pipeline.run_search; package dependencies: preprocessing.rank_inverse_normal_transform.
- **Inputs And Shapes:** Signature `frame, config: Mapping[str, Any]`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 0 hand-worked matrix; Lab 1 executed fixture. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 0 RINT and Lab 1 input contract. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 0 RINT and Lab 1 input contract. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `not annotated`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of input orientation and transformation. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_preprocessing_metrics.py::test_rint_and_numeric_matrix. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects pipeline.run_search to preprocessing.rank_inverse_normal_transform; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `preprocessing.infer_explanation_orientation` (Tier B)

- **Name And Scientific Purpose:** `preprocessing.infer_explanation_orientation`: Infer orientation only when one exact ID source is uniquely supported. Its documented role is input orientation and transformation.
- **Workflow Position:** Called by interpretation.run_explanation; depends on io.normalize_identifier; io.validated_identifiers. Planned treatment: 3, 6, 18.
- **Plain Language Intuition:** It performs one auditable step of input orientation and transformation; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: numeric coercion, missingness rejection, transpose, RINT, and explanation orientation. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/preprocessing.py:67; callers: interpretation.run_explanation; package dependencies: io.normalize_identifier; io.validated_identifiers.
- **Inputs And Shapes:** Signature `frame, expected_vector_ids, *, drop_first_n_cols: int`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 0 hand-worked matrix; Lab 1 executed fixture. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 0 RINT and Lab 1 input contract. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 0 RINT and Lab 1 input contract. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `tuple[str, str]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of input orientation and transformation. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_freeze3_interpretation.py::test_orientation_inference_uses_exact_overlap. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects interpretation.run_explanation to io.normalize_identifier; io.validated_identifiers; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `preprocessing.prepare_explanation_matrix` (Tier A)

- **Name And Scientific Purpose:** `preprocessing.prepare_explanation_matrix`: Prepare vectors × original dimensions for post-run interpretation. Its documented role is input orientation and transformation.
- **Workflow Position:** Called by interpretation.run_explanation; depends on io.validated_identifiers; preprocessing.ExplanationMatrix; preprocessing._unique_feature_names; preprocessing.rank_inverse_normal_transform. Planned treatment: 3, 6, 18.
- **Plain Language Intuition:** It performs one auditable step of input orientation and transformation; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: numeric coercion, missingness rejection, transpose, RINT, and explanation orientation. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/preprocessing.py:112; callers: interpretation.run_explanation; package dependencies: io.validated_identifiers; preprocessing.ExplanationMatrix; preprocessing._unique_feature_names; preprocessing.rank_inverse_normal_transform.
- **Inputs And Shapes:** Signature `frame, *, orientation: str, drop_first_n_cols: int, vector_id_source: str='matrix_columns', zscore_transform: str='none'`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 0 hand-worked matrix; Lab 1 executed fixture. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 0 RINT and Lab 1 input contract. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 0 RINT and Lab 1 input contract. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `ExplanationMatrix`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of input orientation and transformation. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_freeze3_interpretation.py::test_variants_by_vectors_preserves_vector_ids; tests/test_freeze3_interpretation.py::test_vectors_by_variants_explicit_id_column. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects interpretation.run_explanation to io.validated_identifiers; preprocessing.ExplanationMatrix; preprocessing._unique_feature_names; preprocessing.rank_inverse_normal_transform; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `provenance.sha256_file` (Tier B)

- **Name And Scientific Purpose:** `provenance.sha256_file`: Implementation callable for sha256 file. Its documented role is source, environment, command, and file identity.
- **Workflow Position:** Called by interpretation._native_sources; provenance.file_record; reporting._top_artifact; validation.run_validation; depends on No package-defined dependency detected. Planned treatment: 12, 15, 23, 24.
- **Plain Language Intuition:** It performs one auditable step of source, environment, command, and file identity; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: checksums and manifests establish traceability, not scientific truth. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/provenance.py:17; callers: interpretation._native_sources; provenance.file_record; reporting._top_artifact; validation.run_validation; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `path: str | Path`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through All executed labs. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** all recorded labs. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: all recorded labs. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `str`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of source, environment, command, and file identity. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_failure_and_provenance.py::test_authoritative_source_hash_unchanged. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects interpretation._native_sources; provenance.file_record; reporting._top_artifact; validation.run_validation to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `provenance.package_versions` (Tier B)

- **Name And Scientific Purpose:** `provenance.package_versions`: Implementation callable for package versions. Its documented role is source, environment, command, and file identity.
- **Workflow Position:** Called by provenance.base_manifest; depends on No package-defined dependency detected. Planned treatment: 12, 15, 23, 24.
- **Plain Language Intuition:** It performs one auditable step of source, environment, command, and file identity; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: checksums and manifests establish traceability, not scientific truth. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/provenance.py:25; callers: provenance.base_manifest; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `names: Iterable[str] | None=None`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through All executed labs. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** all recorded labs. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: all recorded labs. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict[str, str | None]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of source, environment, command, and file identity. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects provenance.base_manifest to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `provenance.utc_now` (Tier B)

- **Name And Scientific Purpose:** `provenance.utc_now`: Implementation callable for utc now. Its documented role is source, environment, command, and file identity.
- **Workflow Position:** Called by comparison.run_comparison; interpretation.run_explanation; provenance.base_manifest; reporting.write_model_outputs; validation.run_validation; depends on No package-defined dependency detected. Planned treatment: 12, 15, 23, 24.
- **Plain Language Intuition:** It performs one auditable step of source, environment, command, and file identity; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: checksums and manifests establish traceability, not scientific truth. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/provenance.py:40; callers: comparison.run_comparison; interpretation.run_explanation; provenance.base_manifest; reporting.write_model_outputs; validation.run_validation; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `class construction/data container`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through All executed labs. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** all recorded labs. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: all recorded labs. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `str`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of source, environment, command, and file identity. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects comparison.run_comparison; interpretation.run_explanation; provenance.base_manifest; reporting.write_model_outputs; validation.run_validation to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `provenance.file_record` (Tier B)

- **Name And Scientific Purpose:** `provenance.file_record`: Implementation callable for file record. Its documented role is source, environment, command, and file identity.
- **Workflow Position:** Called by comparison.run_comparison; interpretation.run_explanation; pipeline.run_search; reporting._top_artifact; reporting.write_model_outputs; validation.run_validation; depends on comparison._columns.<locals>.resolve; provenance.sha256_file. Planned treatment: 12, 15, 23, 24.
- **Plain Language Intuition:** It performs one auditable step of source, environment, command, and file identity; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: checksums and manifests establish traceability, not scientific truth. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/provenance.py:44; callers: comparison.run_comparison; interpretation.run_explanation; pipeline.run_search; reporting._top_artifact; reporting.write_model_outputs; validation.run_validation; package dependencies: comparison._columns.<locals>.resolve; provenance.sha256_file.
- **Inputs And Shapes:** Signature `path: str | Path`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through All executed labs. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** all recorded labs. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: all recorded labs. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict[str, str | int]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of source, environment, command, and file identity. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects comparison.run_comparison; interpretation.run_explanation; pipeline.run_search; reporting._top_artifact; reporting.write_model_outputs; validation.run_validation to comparison._columns.<locals>.resolve; provenance.sha256_file; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `provenance.package_source_digest` (Tier A)

- **Name And Scientific Purpose:** `provenance.package_source_digest`: Compute a stable hash over package source files for non-Git source identity. Its documented role is source, environment, command, and file identity.
- **Workflow Position:** Called by provenance.base_manifest; depends on comparison._columns.<locals>.resolve. Planned treatment: 12, 15, 23, 24.
- **Plain Language Intuition:** It performs one auditable step of source, environment, command, and file identity; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: checksums and manifests establish traceability, not scientific truth. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/provenance.py:53; callers: provenance.base_manifest; package dependencies: comparison._columns.<locals>.resolve.
- **Inputs And Shapes:** Signature `class construction/data container`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through All executed labs. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** all recorded labs. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: all recorded labs. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `str`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of source, environment, command, and file identity. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_freeze3_comparison_validation.py::test_package_source_digest_is_stable. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects provenance.base_manifest to comparison._columns.<locals>.resolve; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `provenance.base_manifest` (Tier A)

- **Name And Scientific Purpose:** `provenance.base_manifest`: Implementation callable for base manifest. Its documented role is source, environment, command, and file identity.
- **Workflow Position:** Called by comparison.run_comparison; interpretation.run_explanation; pipeline.run_search; validation.run_validation; depends on provenance.package_source_digest; provenance.package_versions; provenance.utc_now. Planned treatment: 12, 15, 23, 24.
- **Plain Language Intuition:** It performs one auditable step of source, environment, command, and file identity; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: checksums and manifests establish traceability, not scientific truth. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/provenance.py:66; callers: comparison.run_comparison; interpretation.run_explanation; pipeline.run_search; validation.run_validation; package dependencies: provenance.package_source_digest; provenance.package_versions; provenance.utc_now.
- **Inputs And Shapes:** Signature `command: list[str] | None=None`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through All executed labs. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** all recorded labs. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: all recorded labs. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of source, environment, command, and file identity. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects comparison.run_comparison; interpretation.run_explanation; pipeline.run_search; validation.run_validation to provenance.package_source_digest; provenance.package_versions; provenance.utc_now; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `ranking.rank_models` (Tier A)

- **Name And Scientific Purpose:** `ranking.rank_models`: Apply deterministic eligibility, score, and tie ordering to candidate rows. Its documented role is deterministic ranking and summaries.
- **Workflow Position:** Called by cli._score; cli._summarize; pipeline.run_search; depends on No package-defined dependency detected. Planned treatment: 11, 16, 20.
- **Plain Language Intuition:** It performs one auditable step of deterministic ranking and summaries; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: stable score ordering, Pareto non-domination, and family aggregation. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/ranking.py:8; callers: cli._score; cli._summarize; pipeline.run_search; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `frame`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 0 and 2. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 2 tied candidate ranking. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 2 tied candidate ranking. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `not annotated`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of deterministic ranking and summaries. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_scoring_ranking.py::test_custom_scoring_ranking_top_n_and_pareto. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli._score; cli._summarize; pipeline.run_search to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `ranking.top_models` (Tier B)

- **Name And Scientific Purpose:** `ranking.top_models`: Implementation callable for top models. Its documented role is deterministic ranking and summaries.
- **Workflow Position:** Called by cli._summarize; pipeline.run_search; depends on No package-defined dependency detected. Planned treatment: 11, 16, 20.
- **Plain Language Intuition:** It performs one auditable step of deterministic ranking and summaries; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: stable score ordering, Pareto non-domination, and family aggregation. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/ranking.py:23; callers: cli._summarize; pipeline.run_search; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `frame, n: int`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 0 and 2. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 2 tied candidate ranking. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 2 tied candidate ranking. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `not annotated`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of deterministic ranking and summaries. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_scoring_ranking.py::test_custom_scoring_ranking_top_n_and_pareto. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli._summarize; pipeline.run_search to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `ranking.pareto_front` (Tier A)

- **Name And Scientific Purpose:** `ranking.pareto_front`: Implementation callable for pareto front. Its documented role is deterministic ranking and summaries.
- **Workflow Position:** Called by cli._summarize; pipeline.run_search; depends on No package-defined dependency detected. Planned treatment: 11, 16, 20.
- **Plain Language Intuition:** It performs one auditable step of deterministic ranking and summaries; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: stable score ordering, Pareto non-domination, and family aggregation. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/ranking.py:27; callers: cli._summarize; pipeline.run_search; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `frame`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 0 and 2. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 2 tied candidate ranking. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 2 tied candidate ranking. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `not annotated`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of deterministic ranking and summaries. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_pipeline_integration.py::test_custom_leaf_eom_metric_and_max_size_run; tests/test_scoring_ranking.py::test_custom_scoring_ranking_top_n_and_pareto. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli._summarize; pipeline.run_search to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `ranking.family_summaries` (Tier A)

- **Name And Scientific Purpose:** `ranking.family_summaries`: Implementation callable for family summaries. Its documented role is deterministic ranking and summaries.
- **Workflow Position:** Called by cli._summarize; pipeline.run_search; depends on No package-defined dependency detected. Planned treatment: 11, 16, 20.
- **Plain Language Intuition:** It performs one auditable step of deterministic ranking and summaries; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: stable score ordering, Pareto non-domination, and family aggregation. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/ranking.py:71; callers: cli._summarize; pipeline.run_search; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `frame, columns: Iterable[str]=DEFAULT_FAMILY_COLUMNS`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 0 and 2. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 2 tied candidate ranking. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 2 tied candidate ranking. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `not annotated`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of deterministic ranking and summaries. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_pipeline_integration.py::test_custom_leaf_eom_metric_and_max_size_run. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli._summarize; pipeline.run_search to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `reporting.write_resolved_config` (Tier B)

- **Name And Scientific Purpose:** `reporting.write_resolved_config`: Implementation callable for write resolved config. Its documented role is authoritative output serialization.
- **Workflow Position:** Called by pipeline.run_search; depends on No package-defined dependency detected. Planned treatment: 12, 15; output atlas.
- **Plain Language Intuition:** It performs one auditable step of authoritative output serialization; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: schemas and atomic writes preserve candidate failures and selected artifacts. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/reporting.py:18; callers: pipeline.run_search; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `config: Mapping[str, Any], output_dir: str | Path`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–3 output walk-throughs. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** output atlas and Labs 1–3. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: output atlas and Labs 1–3. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `Path`. Direct canonical artifacts: resolved_config.yaml.
- **Result Interpretation:** Interpret results at the level of authoritative output serialization. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: writes files/directories. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects pipeline.run_search to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `reporting.write_search_space` (Tier B)

- **Name And Scientific Purpose:** `reporting.write_search_space`: Implementation callable for write search space. Its documented role is authoritative output serialization.
- **Workflow Position:** Called by cli._show; pipeline.run_search; depends on io.atomic_json_dump; io.json_safe; reporting._write_tsv; search_space.flatten_candidate. Planned treatment: 12, 15; output atlas.
- **Plain Language Intuition:** It performs one auditable step of authoritative output serialization; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: schemas and atomic writes preserve candidate failures and selected artifacts. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/reporting.py:28; callers: cli._show; pipeline.run_search; package dependencies: io.atomic_json_dump; io.json_safe; reporting._write_tsv; search_space.flatten_candidate.
- **Inputs And Shapes:** Signature `candidates: list[Mapping[str, Any]], config: Mapping[str, Any], output_dir: str | Path`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–3 output walk-throughs. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** output atlas and Labs 1–3. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: output atlas and Labs 1–3. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict[str, Path]`. Direct canonical artifacts: search_space_manifest.tsv; search_space_manifest.json.
- **Result Interpretation:** Interpret results at the level of authoritative output serialization. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: writes files/directories. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli._show; pipeline.run_search to io.atomic_json_dump; io.json_safe; reporting._write_tsv; search_space.flatten_candidate; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `reporting.write_model_outputs` (Tier A)

- **Name And Scientific Purpose:** `reporting.write_model_outputs`: Write the complete candidate, ranking, selection, retained-model, compatibility, and manifest artifact family. Its documented role is authoritative output serialization.
- **Workflow Position:** Called by pipeline.run_search; depends on io.atomic_json_dump; io.json_safe; provenance.file_record; provenance.utc_now; reporting._top_artifact; reporting._write_tsv. Planned treatment: 12, 15; output atlas.
- **Plain Language Intuition:** It performs one auditable step of authoritative output serialization; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: schemas and atomic writes preserve candidate failures and selected artifacts. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/reporting.py:105; callers: pipeline.run_search; package dependencies: io.atomic_json_dump; io.json_safe; provenance.file_record; provenance.utc_now; reporting._top_artifact; reporting._write_tsv.
- **Inputs And Shapes:** Signature `ranked, top, pareto, families, candidates_by_id: Mapping[str, Mapping[str, Any]], labels_by_id: Mapping[str, Any], visualizations_by_umap: Mapping[str, Any], feature_ids, annotation_frame, config: Mapping[str, Any], scoring_manifest: Mapping[str, Any], run_manifest: Mapping[str, Any], output_dir: str | Path`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–3 output walk-throughs. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** output atlas and Labs 1–3. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: output atlas and Labs 1–3. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict[str, Any]`. Direct canonical artifacts: run_manifest.json; models/all_models.tsv; models/all_models.parquet; models/ranked_models.tsv; models/top_models.tsv; models/best_model.json; models/model_selection_manifest.json; models/pareto_front.tsv; models/family_summaries.tsv; stage02_hdbscan_gridsearch_results.csv; stage03_optimized_cluster_solutions.csv; stage09_umap_vizdata_with_clusters.csv; stage09b_umap_vizdata_with_annotations.csv.
- **Result Interpretation:** Interpret results at the level of authoritative output serialization. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: writes files/directories. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects pipeline.run_search to io.atomic_json_dump; io.json_safe; provenance.file_record; provenance.utc_now; reporting._top_artifact; reporting._write_tsv; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `scoring.normalize_model_table_schema` (Tier B)

- **Name And Scientific Purpose:** `scoring.normalize_model_table_schema`: Adapt the historical notebook table schema without discarding source fields. Its documented role is declared candidate scoring.
- **Workflow Position:** Called by cli._score; depends on No package-defined dependency detected. Planned treatment: 11, 18, 20.
- **Plain Language Intuition:** It performs one auditable step of declared candidate scoring; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: population-relative normalization, dynamic-range weighting, direction, eligibility, and final scaling. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/scoring.py:28; callers: cli._score; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `frame`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 0 score table; Lab 2 executed ranking. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 0 hand calculation and Lab 2 ranking. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 0 hand calculation and Lab 2 ranking. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `not annotated`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of declared candidate scoring. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_freeze3_comparison_validation.py::test_historical_notebook_model_schema_is_adapted. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli._score to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `scoring.legacy_dimple_score` (Tier A)

- **Name And Scientific Purpose:** `scoring.legacy_dimple_score`: Reproduce the compatibility score using observed dynamic-range weights and population-dependent normalization. Its documented role is declared candidate scoring.
- **Workflow Position:** Called by scoring.apply_scoring; depends on scoring._safe_divide_by_max; scoring._scale_final. Planned treatment: 11, 18, 20.
- **Plain Language Intuition:** It performs one auditable step of declared candidate scoring; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: population-relative normalization, dynamic-range weighting, direction, eligibility, and final scaling. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/scoring.py:80; callers: scoring.apply_scoring; package dependencies: scoring._safe_divide_by_max; scoring._scale_final.
- **Inputs And Shapes:** Signature `frame, fit_include_noise: bool=False`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 0 score table; Lab 2 executed ranking. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 0 hand calculation and Lab 2 ranking. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 0 hand calculation and Lab 2 ranking. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `not annotated`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of declared candidate scoring. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_scoring_ranking.py::test_legacy_formula_matches_literal_reference; tests/test_scoring_ranking.py::test_zero_variance_and_noise_exclusion. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects scoring.apply_scoring to scoring._safe_divide_by_max; scoring._scale_final; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `scoring.custom_score` (Tier A)

- **Name And Scientific Purpose:** `scoring.custom_score`: Apply a user-declared multi-component scoring profile with orientations and weights. Its documented role is declared candidate scoring.
- **Workflow Position:** Called by scoring.apply_scoring; depends on scoring._scale_final. Planned treatment: 11, 18, 20.
- **Plain Language Intuition:** It performs one auditable step of declared candidate scoring; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: population-relative normalization, dynamic-range weighting, direction, eligibility, and final scaling. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/scoring.py:146; callers: scoring.apply_scoring; package dependencies: scoring._scale_final.
- **Inputs And Shapes:** Signature `frame, rules: Mapping[str, Mapping[str, Any]]`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 0 score table; Lab 2 executed ranking. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 0 hand calculation and Lab 2 ranking. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 0 hand calculation and Lab 2 ranking. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `not annotated`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of declared candidate scoring. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_scoring_ranking.py::test_custom_scoring_ranking_top_n_and_pareto. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects scoring.apply_scoring to scoring._scale_final; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `scoring.apply_scoring` (Tier A)

- **Name And Scientific Purpose:** `scoring.apply_scoring`: Implementation callable for apply scoring. Its documented role is declared candidate scoring.
- **Workflow Position:** Called by cli._score; pipeline.run_search; depends on scoring.custom_score; scoring.legacy_dimple_score. Planned treatment: 11, 18, 20.
- **Plain Language Intuition:** It performs one auditable step of declared candidate scoring; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: population-relative normalization, dynamic-range weighting, direction, eligibility, and final scaling. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/scoring.py:195; callers: cli._score; pipeline.run_search; package dependencies: scoring.custom_score; scoring.legacy_dimple_score.
- **Inputs And Shapes:** Signature `frame, scoring_config: Mapping[str, Any]`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 0 score table; Lab 2 executed ranking. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 0 hand calculation and Lab 2 ranking. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 0 hand calculation and Lab 2 ranking. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `not annotated`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of declared candidate scoring. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli._score; pipeline.run_search to scoring.custom_score; scoring.legacy_dimple_score; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `search_space.canonical_json` (Tier B)

- **Name And Scientific Purpose:** `search_space.canonical_json`: Implementation callable for canonical json. Its documented role is deterministic candidate enumeration.
- **Workflow Position:** Called by search_space.stable_identifier; depends on No package-defined dependency detected. Planned treatment: 10, 14, 20.
- **Plain Language Intuition:** It performs one auditable step of deterministic candidate enumeration; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: Cartesian product and content-derived identity. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/search_space.py:16; callers: search_space.stable_identifier; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `value: Any`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–2 candidate enumeration. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–2 show-search-space. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–2 show-search-space. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `str`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of deterministic candidate enumeration. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects search_space.stable_identifier to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `search_space.stable_identifier` (Tier B)

- **Name And Scientific Purpose:** `search_space.stable_identifier`: Implementation callable for stable identifier. Its documented role is deterministic candidate enumeration.
- **Workflow Position:** Called by pipeline.run_search; search_space.enumerate_candidates; depends on search_space.canonical_json. Planned treatment: 10, 14, 20.
- **Plain Language Intuition:** It performs one auditable step of deterministic candidate enumeration; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: Cartesian product and content-derived identity. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/search_space.py:20; callers: pipeline.run_search; search_space.enumerate_candidates; package dependencies: search_space.canonical_json.
- **Inputs And Shapes:** Signature `prefix: str, value: Any, length: int=16`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–2 candidate enumeration. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–2 show-search-space. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–2 show-search-space. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `str`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of deterministic candidate enumeration. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects pipeline.run_search; search_space.enumerate_candidates to search_space.canonical_json; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `search_space.count_candidates` (Tier A)

- **Name And Scientific Purpose:** `search_space.count_candidates`: Implementation callable for count candidates. Its documented role is deterministic candidate enumeration.
- **Workflow Position:** Called by cli._inspect; cli._show; search_space.enumerate_candidates; depends on config.normalized_parameter_space. Planned treatment: 10, 14, 20.
- **Plain Language Intuition:** It performs one auditable step of deterministic candidate enumeration; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: Cartesian product and content-derived identity. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/search_space.py:25; callers: cli._inspect; cli._show; search_space.enumerate_candidates; package dependencies: config.normalized_parameter_space.
- **Inputs And Shapes:** Signature `config: Mapping[str, Any]`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–2 candidate enumeration. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–2 show-search-space. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–2 show-search-space. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict[str, int]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of deterministic candidate enumeration. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_config.py::test_standard_defaults_match_dev_declarations. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli._inspect; cli._show; search_space.enumerate_candidates to config.normalized_parameter_space; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `search_space.model_family` (Tier B)

- **Name And Scientific Purpose:** `search_space.model_family`: Implementation callable for model family. Its documented role is deterministic candidate enumeration.
- **Workflow Position:** Called by search_space.enumerate_candidates; depends on No package-defined dependency detected. Planned treatment: 10, 14, 20.
- **Plain Language Intuition:** It performs one auditable step of deterministic candidate enumeration; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: Cartesian product and content-derived identity. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/search_space.py:42; callers: search_space.enumerate_candidates; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `umap_params: Mapping[str, Any], hdbscan_params: Mapping[str, Any]`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–2 candidate enumeration. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–2 show-search-space. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–2 show-search-space. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `str`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of deterministic candidate enumeration. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects search_space.enumerate_candidates to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `search_space.enumerate_candidates` (Tier A)

- **Name And Scientific Purpose:** `search_space.enumerate_candidates`: Expand the declared UMAP-family and HDBSCAN Cartesian product into deterministically identified candidates. Its documented role is deterministic candidate enumeration.
- **Workflow Position:** Called by cli._show; pipeline.run_search; depends on config.normalized_parameter_space; search_space._dict_product; search_space.count_candidates; search_space.model_family; search_space.stable_identifier. Planned treatment: 10, 14, 20.
- **Plain Language Intuition:** It performs one auditable step of deterministic candidate enumeration; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: Cartesian product and content-derived identity. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/search_space.py:53; callers: cli._show; pipeline.run_search; package dependencies: config.normalized_parameter_space; search_space._dict_product; search_space.count_candidates; search_space.model_family; search_space.stable_identifier.
- **Inputs And Shapes:** Signature `config: Mapping[str, Any]`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–2 candidate enumeration. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–2 show-search-space. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–2 show-search-space. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `list[dict[str, Any]]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of deterministic candidate enumeration. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_failure_and_provenance.py::test_failed_candidate_is_retained; tests/test_search_space.py::test_search_enumeration_and_stable_ids; tests/test_search_space.py::test_search_limit_never_silently_samples. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli._show; pipeline.run_search to config.normalized_parameter_space; search_space._dict_product; search_space.count_candidates; search_space.model_family; search_space.stable_identifier; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `search_space.flatten_candidate` (Tier B)

- **Name And Scientific Purpose:** `search_space.flatten_candidate`: Implementation callable for flatten candidate. Its documented role is deterministic candidate enumeration.
- **Workflow Position:** Called by cli._show; pipeline._evaluate_one; pipeline._failed_row; reporting.write_search_space; depends on No package-defined dependency detected. Planned treatment: 10, 14, 20.
- **Plain Language Intuition:** It performs one auditable step of deterministic candidate enumeration; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: Cartesian product and content-derived identity. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/search_space.py:103; callers: cli._show; pipeline._evaluate_one; pipeline._failed_row; reporting.write_search_space; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `candidate: Mapping[str, Any]`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–2 candidate enumeration. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Labs 1–2 show-search-space. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Labs 1–2 show-search-space. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict[str, Any]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of deterministic candidate enumeration. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli._show; pipeline._evaluate_one; pipeline._failed_row; reporting.write_search_space to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `umap_runner.ensemble_seeds` (Tier A)

- **Name And Scientific Purpose:** `umap_runner.ensemble_seeds`: Generate the exact repeated-embedding seed sequence under current or legacy scheduling. Its documented role is repeated nonlinear representation.
- **Workflow Position:** Called by umap_runner.run_repeated_umap; depends on No package-defined dependency detected. Planned treatment: 7, 8.
- **Plain Language Intuition:** It performs one auditable step of repeated nonlinear representation; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: delegated UMAP/densMAP plus explicit seed schedule and raw concatenation. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/umap_runner.py:32; callers: umap_runner.run_repeated_umap; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `parameters: Mapping[str, Any], repeats: int, legacy_sequence: bool`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–2 repeated fixture representations. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Chapter 7 and Labs 1–2. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Chapter 7 and Labs 1–2. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `list[int]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of repeated nonlinear representation. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects umap_runner.run_repeated_umap to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `umap_runner.run_repeated_umap` (Tier A)

- **Name And Scientific Purpose:** `umap_runner.run_repeated_umap`: Fit repeated UMAP/densMAP representations and concatenate their coordinates. Its documented role is repeated nonlinear representation.
- **Workflow Position:** Called by pipeline.run_search; depends on umap_runner._fit_one; umap_runner.ensemble_seeds. Planned treatment: 7, 8.
- **Plain Language Intuition:** It performs one auditable step of repeated nonlinear representation; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: delegated UMAP/densMAP plus explicit seed schedule and raw concatenation. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/umap_runner.py:39; callers: pipeline.run_search; package dependencies: umap_runner._fit_one; umap_runner.ensemble_seeds.
- **Inputs And Shapes:** Signature `matrix, parameters: Mapping[str, Any], repeats: int, n_jobs: int, legacy_sequence: bool`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1–2 repeated fixture representations. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Chapter 7 and Labs 1–2. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Chapter 7 and Labs 1–2. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict[str, Any]`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of repeated nonlinear representation. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects pipeline.run_search to umap_runner._fit_one; umap_runner.ensemble_seeds; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `validation.run_validation` (Tier A)

- **Name And Scientific Purpose:** `validation.run_validation`: Audit a run directory against required files, schemas, counts, identities, hashes, and manifest contracts. Its documented role is artifact-contract validation.
- **Workflow Position:** Called by cli._validate; depends on comparison._columns.<locals>.resolve; io.atomic_json_dump; io.ensure_empty_output_dir; io.json_safe; io.read_model_table; io.read_table; provenance.base_manifest; provenance.file_record; provenance.sha256_file; provenance.utc_now; validation.run_validation.<locals>.record. Planned treatment: 12, 16, 21, 23.
- **Plain Language Intuition:** It performs one auditable step of artifact-contract validation; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: schema, count, identifier, hash, and manifest checks. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/validation.py:15; callers: cli._validate; package dependencies: comparison._columns.<locals>.resolve; io.atomic_json_dump; io.ensure_empty_output_dir; io.json_safe; io.read_model_table; io.read_table; provenance.base_manifest; provenance.file_record; provenance.sha256_file; provenance.utc_now; validation.run_validation.<locals>.record.
- **Inputs And Shapes:** Signature `run_dir: str | Path, output_dir: str | Path | None=None, *, command: list[str] | None=None`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Labs 1 and 3. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 3 validation. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 3 validation. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict[str, Any]`. Direct canonical artifacts: validation_checks.tsv; validation_report.json; validation_manifest.json.
- **Result Interpretation:** Interpret results at the level of artifact-contract validation. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_freeze3_comparison_validation.py::test_validation_detects_hash_mismatch; tests/test_freeze3_comparison_validation.py::test_validation_passes_complete_contract. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: FileNotFoundError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: writes files/directories. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects cli._validate to comparison._columns.<locals>.resolve; io.atomic_json_dump; io.ensure_empty_output_dir; io.json_safe; io.read_model_table; io.read_table; provenance.base_manifest; provenance.file_record; provenance.sha256_file; provenance.utc_now; validation.run_validation.<locals>.record; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `visualization.sample_block_preserving` (Tier B)

- **Name And Scientific Purpose:** `visualization.sample_block_preserving`: Return ordered indices, retaining every consecutive label block. Its documented role is selected-model visualization.
- **Workflow Position:** Called by visualization.render_heatmap; depends on No package-defined dependency detected. Planned treatment: 17, 21.
- **Plain Language Intuition:** It performs one auditable step of selected-model visualization; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: descriptive coordinate and cluster rendering. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/visualization.py:22; callers: visualization.render_heatmap; package dependencies: No package-defined dependency detected.
- **Inputs And Shapes:** Signature `labels: Sequence, maximum: int`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 3 heatmap. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 3 heatmap and run plots. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 3 heatmap and run plots. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `not annotated`. Direct canonical artifacts: No direct canonical artifact; in-memory/supporting result.
- **Result Interpretation:** Interpret results at the level of selected-model visualization. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: tests/test_freeze3_interpretation.py::test_block_sampling_preserves_tiny_cluster. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: ValueError. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: returns in-memory value; no direct file effect observed. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects visualization.render_heatmap to No package-defined dependency detected; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.

## `visualization.render_heatmap` (Tier A)

- **Name And Scientific Purpose:** `visualization.render_heatmap`: Render static and interactive original-space similarity heatmaps with block-preserving sampling. Its documented role is selected-model visualization.
- **Workflow Position:** Called by interpretation.run_explanation; depends on visualization._correlation_rgb; visualization._label_key; visualization.sample_block_preserving. Planned treatment: 17, 21.
- **Plain Language Intuition:** It performs one auditable step of selected-model visualization; callers should use its returned value or contract rather than infer unstated scientific meaning.
- **Statistical Background:** Relevant background: descriptive coordinate and cluster rendering. For mechanical/control functions, this is the statistical contract they preserve rather than a new estimator.
- **Mathematical Formulation:** Use the chapter equations mapped in statistical_concept_coverage.tsv. For this symbol, the authoritative implemented operation is its signature and source; no additional formula is invented.
- **Assumptions And Conditions:** Inputs must satisfy the declared data/configuration contract, identifier and shape requirements, and any delegated-library preconditions. Evidence status: current implementation.
- **Implementation Traceability:** dimple_gwas/visualization.py:71; callers: interpretation.run_explanation; package dependencies: visualization._correlation_rgb; visualization._label_key; visualization.sample_block_preserving.
- **Inputs And Shapes:** Signature `correlation, labels: Sequence, vector_ids: Sequence[str], *, png_path: str | Path, html_path: str | Path, maximum: int`. Shape semantics are determined by the function's chapter and producer contract; mappings/paths/tables must resolve before execution.
- **Parameters And Defaults:** Defaults visible in the signature are authoritative here; configuration-derived defaults resolve through config.resolve_config and are recorded in resolved_config.yaml.
- **How To Use:** Reach this callable through Lab 3 heatmap. Direct internal calls should preserve the same validation, fresh-output, and provenance rules as the CLI.
- **Hand Worked Example:** Lab 3 heatmap and run plots. If the symbol is control-plane or I/O-only, the hand example is its exact contract transition rather than an artificial calculation.
- **Executed Example:** Fresh Edition 2 evidence route: Lab 3 heatmap and run plots. Command records and checksums are under docs/textbook/edition2/labs/.
- **Outputs:** Return annotation: `dict`. Direct canonical artifacts: original_space_heatmap.png; original_space_heatmap.html.
- **Result Interpretation:** Interpret results at the level of selected-model visualization. Software success or a returned diagnostic does not establish biological truth.
- **Diagnostics And Validation:** Direct-name tests: No direct symbol-name test reference; assess through caller/integration coverage. Integration evidence is mapped in function_to_test_matrix.tsv and the fresh 45-test record.
- **Failure Modes And Recovery:** Explicit exceptions: No explicit raise in this symbol; delegated calls may raise.. Preserve the failed record, correct input/configuration/output-root conditions, and rerun into a new directory.
- **Computational Behavior:** State/provenance effect: writes files/directories. Complexity is input-, candidate-, and delegated-backend-dependent unless a chapter gives a tighter bound.
- **Connections:** Connects interpretation.run_explanation to visualization._correlation_rgb; visualization._label_key; visualization.sample_block_preserving; output consumers and file contracts are in output_atlas/output_atlas.tsv.
- **Exercises And Solutions:** Exercise route: inspect the source contract, trace one fresh lab call, identify an edge case, and verify the documented output; solution key is in Appendix J.
- **Evidence And Further Reading:** Source and test evidence are authoritative for implementation. Statistical citations are in the mapped chapter and VERIFIED_BIBLIOGRAPHY.md; evidence status is current implementation.
