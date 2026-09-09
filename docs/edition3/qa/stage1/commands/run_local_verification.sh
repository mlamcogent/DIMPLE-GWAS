#!/bin/sh
set -eu

PYTHON_BIN="../DIMPLE-GWAS-freeze2/.venv/bin/python"
QA_ROOT="docs/edition3/qa/stage1"
LOG_DIR="$QA_ROOT/logs"
TEST_DIR="$QA_ROOT/test_results"
GEN_DIR="$QA_ROOT/generated"

export MPLCONFIGDIR="$GEN_DIR/matplotlib-cache"
export NUMBA_CACHE_DIR="$GEN_DIR/numba-cache"
export XDG_CACHE_HOME="$GEN_DIR/xdg-cache"
mkdir -p "$MPLCONFIGDIR" "$NUMBA_CACHE_DIR" "$XDG_CACHE_HOME"

run_capture() {
  name="$1"
  shift
  started_at=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
  set +e
  "$@" >"$LOG_DIR/$name.stdout.log" 2>"$LOG_DIR/$name.stderr.log"
  status=$?
  set -e
  ended_at=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
  {
    echo "name=$name"
    echo "started_at_utc=$started_at"
    echo "ended_at_utc=$ended_at"
    echo "exit_status=$status"
    printf 'command='
    printf '%s ' "$@"
    printf '\n'
  } >"$LOG_DIR/$name.command.txt"
  if [ "$status" -ne 0 ]; then
    return "$status"
  fi
}

run_capture environment "$PYTHON_BIN" -c "import json, platform; import dimple_gwas, numpy, pandas, scipy, sklearn, umap, hdbscan, yaml, joblib, matplotlib, pyarrow, pytest; print(json.dumps({'python':platform.python_version(),'platform':platform.platform(),'dimple_gwas':dimple_gwas.__version__,'numpy':numpy.__version__,'pandas':pandas.__version__,'scipy':scipy.__version__,'scikit_learn':sklearn.__version__,'umap_learn':umap.__version__,'hdbscan':getattr(hdbscan,'__version__','not_exposed'),'pyyaml':yaml.__version__,'joblib':joblib.__version__,'matplotlib':matplotlib.__version__,'pyarrow':pyarrow.__version__,'pytest':pytest.__version__}, indent=2, sort_keys=True))"
run_capture pip_check "$PYTHON_BIN" -m pip check
run_capture cli_version "$PYTHON_BIN" -m dimple_gwas --version
run_capture cli_root_help "$PYTHON_BIN" -m dimple_gwas --help

for command_name in run inspect-config show-search-space score-existing summarize-models reproduce-model explain interpret compare validate; do
  run_capture "cli_${command_name}_help" "$PYTHON_BIN" -m dimple_gwas "$command_name" --help
done

for config_path in configs/*.yaml; do
  config_stem=$(basename "$config_path" .yaml)
  run_capture "inspect_${config_stem}" "$PYTHON_BIN" -m dimple_gwas inspect-config --config "$config_path"
done

run_capture search_space_standard "$PYTHON_BIN" -m dimple_gwas show-search-space --search-mode standard --show-first 0
run_capture search_space_extended "$PYTHON_BIN" -m dimple_gwas show-search-space --search-mode extended --show-first 0
run_capture search_space_fixed "$PYTHON_BIN" -m dimple_gwas show-search-space --config docs/textbook/edition2/labs/01_fixed_synthetic/tutorial_config.yaml --show-first 1

run_capture pytest_full "$PYTHON_BIN" -m pytest -q --junitxml="$TEST_DIR/freeze3_pytest.xml"

run_capture fixed_run "$PYTHON_BIN" -m dimple_gwas run \
  --config docs/textbook/edition2/labs/01_fixed_synthetic/tutorial_config.yaml \
  --output-dir "$GEN_DIR/fixed_run"

MODEL_SUMMARY="$GEN_DIR/fixed_run/models/top_model_artifacts/model_060fac0208bb58e2/summary.json"
run_capture fixed_explain "$PYTHON_BIN" -m dimple_gwas explain \
  --model-json "$MODEL_SUMMARY" \
  --outdir "$GEN_DIR/fixed_explanation"
run_capture fixed_reproduce "$PYTHON_BIN" -m dimple_gwas reproduce-model \
  --model-json "$MODEL_SUMMARY" \
  --output-dir "$GEN_DIR/fixed_reproduction" \
  --n-jobs 1
run_capture fixed_compare "$PYTHON_BIN" -m dimple_gwas compare \
  --left "$MODEL_SUMMARY" \
  --right "$GEN_DIR/fixed_reproduction/models/top_model_artifacts/model_060fac0208bb58e2/summary.json" \
  --output-dir "$GEN_DIR/fixed_comparison" \
  --require-same-order
run_capture fixed_validate "$PYTHON_BIN" -m dimple_gwas validate \
  --run-dir "$GEN_DIR/fixed_run" \
  --output-dir "$GEN_DIR/fixed_validation"
run_capture fixed_summarize "$PYTHON_BIN" -m dimple_gwas summarize-models \
  --models "$GEN_DIR/fixed_run/models/all_models.tsv" \
  --output-dir "$GEN_DIR/fixed_summaries" \
  --top-n-models 1

run_capture score_historical_164 "$PYTHON_BIN" -m dimple_gwas score-existing \
  --models ../freeze3_workspace/comparisons/idp_runs/historical_tables/original_164_model_table.tsv \
  --config configs/original_idp_164_historical_search.yaml \
  --fit-include-noise \
  --output "$GEN_DIR/fresh_rescored_164_models.tsv"

