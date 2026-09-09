# Lab 1 — Fixed synthetic quickstart

Status: **executed successfully in the fresh Edition 2 environment**. Runtime category: under one minute on the recorded macOS arm64 host.

The lab resolves `tutorial_config.yaml`, enumerates exactly one candidate, fits one densMAP representation with seed 42, evaluates one HDBSCAN model, retains its artifacts, and validates the run. The prepared shape is 24 vectors by 80 variables. Selected model `model_060fac0208bb58e2` contains three clusters of eight and no noise in this designed fixture. This is an engineering smoke test, not a production search or biological result.

Use a new output root when rerunning. Start with `inspect-config`, then `show-search-space`, then `run`; commands and exit codes are in `logs/`. Read `run_manifest.json`, `models/all_models.tsv`, `models/model_selection_manifest.json`, the selected labels, and the compatibility aliases in that order. Publish only `safe_artifacts/`; native manifests contain host paths.
