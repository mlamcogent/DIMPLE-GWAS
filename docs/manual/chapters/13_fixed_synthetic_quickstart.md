# 13. Fixed synthetic quickstart

> **Release status.** DIMPLE-GWAS Freeze 3 RC1 (`3.0.0rc1`) is software-complete under local and fixed-fixture evidence. It is not yet scientifically frozen or cross-platform validated.

## Orientation

This chapter belongs to **Part II — Installation, data preparation, and the first successful run**. It separates observed Freeze 3 behavior from scientific interpretation, historical evidence, and pending release work.

## Learning objectives

After this chapter, you can:

- Execute the canonical bounded run without overwriting prior outputs.
- identify the evidence artifact that supports the behavior or boundary;
- describe one common misuse in language appropriate for a methods report.

Prerequisites: 9-12.

## Explanation and implementation

The shortest verified run starts in the Freeze 3 repository root with the installed RC1 entry point. Inspect first, enumerate second, fit third, and use a new output root.

```bash
dimple-gwas inspect-config \
  --search-mode fixed \
  --config docs/manual/tutorials/01_fixed_synthetic/tutorial_config.yaml

dimple-gwas show-search-space \
  --search-mode fixed \
  --config docs/manual/tutorials/01_fixed_synthetic/tutorial_config.yaml \
  --output-dir docs/manual/tutorials/01_fixed_synthetic/search_space_new

dimple-gwas run \
  --search-mode fixed \
  --config docs/manual/tutorials/01_fixed_synthetic/tutorial_config.yaml \
  --output-dir docs/manual/tutorials/01_fixed_synthetic/run_new
```

Replace `*_new` with unique names. The canonical documented output is `run_20260825_v2`; do not overwrite it. The fixture is small and repository-owned. It demonstrates execution structure, not production adequacy.

## Evidence-backed example

The executed canonical run prepared 24 vectors by 80 variables, evaluated one candidate, selected `model_060fac0208bb58e2`, found three clusters of eight, and assigned no noise. Exit status was zero.

## Outputs to inspect

Confirm `run_manifest.json` status, one-row search manifest, one candidate table row, selected-model JSON, label row count/uniqueness, annotation join, log, and validation output when run.

## Common mistakes

Do not copy an example output path unchanged. Do not jump directly to the plot before checking the manifest. Do not generalize ‘three clusters’ from the designed fixture to real data.

## Scientific and operational limits

One seed and one candidate make this a smoke test. They do not represent standard production compute or a robust model-selection study.

## Completion check

Run the three commands in a fresh named root and write five structural assertions that avoid exact floating-point promises.

<p class="xref"><strong>Operational cross-reference:</strong> Chapter 37 covers commands, Chapter 38 configuration, Chapter 41 artifact schemas, Chapter 42 provenance, and Chapter 46 current limitations.</p>
