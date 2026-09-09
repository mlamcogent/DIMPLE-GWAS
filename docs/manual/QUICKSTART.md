# DIMPLE-GWAS Freeze 3 RC1 — Quickstart

> RC1 is software-complete under local/fixed-fixture evidence. It is not scientifically frozen or cross-platform validated.

This is the shortest verified novice workflow. Start in a terminal, replace `/path/to/DIMPLE-GWAS-freeze3` with the repository location, and choose output directory names that do not already exist.

## 1. Create and verify an isolated environment

```bash
cd /path/to/DIMPLE-GWAS-freeze3
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[test,plots]'
dimple-gwas --version
python -m pip check
```

Expected version: `3.0.0rc1`. If it differs, stop and record the installed source/version before using this edition.

## 2. Inspect and enumerate before fitting

```bash
dimple-gwas inspect-config   --search-mode fixed   --config docs/manual/tutorials/01_fixed_synthetic/tutorial_config.yaml

dimple-gwas show-search-space   --search-mode fixed   --config docs/manual/tutorials/01_fixed_synthetic/tutorial_config.yaml   --output-dir docs/manual/tutorials/01_fixed_synthetic/search_space_NEW
```

The fixture configuration must enumerate one candidate. `NEW` is a placeholder: use a unique name.

## 3. Run the bounded fixture

```bash
dimple-gwas run   --search-mode fixed   --config docs/manual/tutorials/01_fixed_synthetic/tutorial_config.yaml   --output-dir docs/manual/tutorials/01_fixed_synthetic/run_NEW
```

## 4. Inspect before interpreting

Check these files in `run_NEW`:

- `run_manifest.json`: status, version, source/input/config hashes, seeds, threads, backends, counts, selected model;
- `search_space_manifest.tsv`: exactly one candidate;
- `models/all_models.tsv`: one retained candidate row with visible status/errors;
- `models/model_selection_manifest.json`: formula, counts, tie order, selected model;
- `models/top_model_artifacts/<model_id>/labels.tsv`: 24 unique fixture IDs;
- `logs/run.log` and `logs/model_failures.tsv`.

For this designed fixture, the verified run yielded three clusters of eight and no noise. That is a structural smoke-test assertion, not a production target or biological claim.

## 5. Validate your new run

```bash
dimple-gwas validate   --run-dir docs/manual/tutorials/01_fixed_synthetic/run_NEW   --output-dir docs/manual/tutorials/01_fixed_synthetic/validation_NEW
```

Read every row of `validation_checks.tsv`; do not rely only on the exit code.

Next: Chapters 10–14 explain the contract; Chapters 18–23 explain model search/selection/reproduction; Chapters 24–30 explain safe interpretation.
