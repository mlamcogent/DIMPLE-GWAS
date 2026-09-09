# Quick start: inspect, predict, run, verify

This route is deliberately small. It checks that a reader can move through the current software contract and account for the outputs. It does not reproduce any manuscript-scale IDP analysis.

## Before fitting

Work from the `DIMPLE-GWAS-freeze3/` directory in an environment containing the package dependencies. Confirm the identity first:

```bash
python -m dimple_gwas --version
python -m dimple_gwas --help
```

Expected software version: `3.0.0rc1`. Under the Stage 1 environment the package-source SHA-256 was `df87825992ab51dc016c673cf420a978ba5c161bd6c755e00a5199ead310e65b`.

The tutorial configuration is retained at:

```text
docs/textbook/edition2/labs/01_fixed_synthetic/tutorial_config.yaml
```

Before running it, predict the following: one candidate will be enumerated; the prepared matrix will contain 24 vectors and 80 numeric variables; a successful run will produce a resolved configuration, search-space manifests, model tables, retained labels, logs, and a run manifest.

## Inspect and enumerate

```bash
python -m dimple_gwas inspect-config \
  --search-mode fixed \
  --config docs/textbook/edition2/labs/01_fixed_synthetic/tutorial_config.yaml

python -m dimple_gwas show-search-space \
  --search-mode fixed \
  --config docs/textbook/edition2/labs/01_fixed_synthetic/tutorial_config.yaml \
  --output-dir docs/edition3/labs/executed/quickstart_search
```

Stop if the candidate count is not one or the output directory is already occupied. DIMPLE-GWAS intentionally protects existing result roots.

## Run the fixed model

```bash
python -m dimple_gwas run \
  --search-mode fixed \
  --config docs/textbook/edition2/labs/01_fixed_synthetic/tutorial_config.yaml \
  --output-dir docs/edition3/labs/executed/quickstart_run
```

Stage 1 observed one successful candidate, model `model_060fac0208bb58e2`, three clusters, and no noise. Those values are regression expectations for the recorded local environment, not biological targets.

## Verify before interpreting

```bash
python -m dimple_gwas validate \
  --run-dir docs/edition3/labs/executed/quickstart_run \
  --output-dir docs/edition3/labs/executed/quickstart_validation
```

Read in this order:

1. `run_manifest.json`: completion status, source/input/config identities, seed and dependency provenance, warnings, exclusions, and failures.
2. `resolved_config.yaml`: the actual analysis specification after precedence resolution.
3. `search_space_manifest.tsv`: the candidate population that was eligible for selection.
4. `models/model_selection_manifest.json`: score definition, rank logic, selected model, and artifact links.
5. `models/top_model_artifacts/model_060fac0208bb58e2/labels.tsv`: exact IDs and algorithmic labels.
6. the validation report: file, schema, count, and hash checks.

The one-candidate legacy score maps to 1 because the table-relative normalization has a zero-range fallback. It does not mean perfect external validity.

## What this quick start establishes

It establishes a bounded software path on a designed synthetic fixture. It does not establish real-data stability, biological validity, cross-platform identity, or completion of the fresh 164-IDP 1,000-seed run.

Continue with Workbook Labs 0-4 for a guided analysis journey. Read Textbook Chapters 1-3 before applying the pipeline to new summary-statistic matrices.
