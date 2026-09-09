# 37. Complete command reference

> **Release status.** DIMPLE-GWAS Freeze 3 RC1 (`3.0.0rc1`) is software-complete under local and fixed-fixture evidence. It is not yet scientifically frozen or cross-platform validated.

## Orientation

This chapter belongs to **Part VI — Operational reference**. It separates observed Freeze 3 behavior from scientific interpretation, historical evidence, and pending release work.

## Learning objectives

After this chapter, you can:

- Select the correct command and required inputs for each task.
- identify the evidence artifact that supports the behavior or boundary;
- describe one common misuse in language appropriate for a methods report.

Prerequisites: 9-14.

## Explanation and implementation

The entry point is `dimple-gwas`; `python -m dimple_gwas` is equivalent. `run` fits the declared UMAP/HDBSCAN search. `inspect-config` resolves/validates settings. `show-search-space` enumerates without fitting. `score-existing` applies a declared score to a native or adapted historical table. `summarize-models` creates family/Pareto/top summaries. `reproduce-model` refits one retained parameterization. `explain` (alias `interpret`) summarizes retained labels in original space without refitting. `compare` compares exact-ID artifacts. `validate` checks a run contract and hashes.

Use `dimple-gwas COMMAND --help` as the runtime authority. Common run precedence is `--search-mode`, optional `--config`, then explicit input/UMAP/HDBSCAN/execution/scoring overrides. Run aliases support selected Dev spellings, but new work should prefer canonical hyphenated flags. Downstream commands have their own required inputs; they do not inherit a current run implicitly.

Minimal patterns:

```bash
dimple-gwas inspect-config --search-mode MODE --config CONFIG.yaml
dimple-gwas show-search-space --search-mode MODE --config CONFIG.yaml --output-dir NEW_DIR
dimple-gwas run --search-mode MODE --config CONFIG.yaml --output-dir NEW_DIR
dimple-gwas score-existing --models TABLE --output SCORED.tsv
dimple-gwas summarize-models --models TABLE --output-dir NEW_DIR
dimple-gwas reproduce-model --model-json SUMMARY.json --output-dir NEW_DIR
dimple-gwas explain --model-json SUMMARY.json --output-dir NEW_DIR
dimple-gwas compare --left A --right B --output-dir NEW_DIR
dimple-gwas validate --run-dir RUN --output-dir NEW_DIR
```

## Evidence-backed example

All top-level and subcommand help text was freshly captured in `build/logs/cli_help/`. The implementation-derived matrix has one row per action, flag alias, destination, default, choice, requirement, help text, and source.

## Outputs to inspect

Inspect `evidence/command_and_flag_matrix.tsv` for the complete flag list and captured help for formatting. Then verify output effects in the producer–consumer map.

## Common mistakes

Do not assume a flag accepted by `run` is accepted by `explain`. Do not omit required output roots. Do not rely on an alias when publishing a new canonical protocol without documenting it.

## Scientific and operational limits

CLI `--help` proves interface availability, not scientific appropriateness. Some options can create very large searches or expose private paths in manifests.

## Completion check

For each command, state whether it fits UMAP/HDBSCAN, reads an existing model table, and writes a new directory or file.

<p class="xref"><strong>Operational cross-reference:</strong> Chapter 37 covers commands, Chapter 38 configuration, Chapter 41 artifact schemas, Chapter 42 provenance, and Chapter 46 current limitations.</p>
