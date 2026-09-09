#!/usr/bin/env bash
# Current-image execution, with explicit incomplete exact historical lanes.
set -euo pipefail
if [[ $# -ne 3 ]]; then
  echo 'Usage: run_three_lane_validation.sh CURRENT_IMAGE ABS_BOOTSTRAP_INPUT ABS_NEW_OUTPUT_ROOT' >&2
  echo 'Bootstrap input contains harness.py, sealed criteria JSON, and configs/ (seven shipped YAMLs).' >&2
  exit 64
fi
current_image=$1
bootstrap_root=$2
validation_root=$3
script_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
[[ "$bootstrap_root" == /* && "$validation_root" == /* && -d "$bootstrap_root" && ! -e "$validation_root" ]] || {
  echo 'Absolute bootstrap and unused absolute output root required.' >&2; exit 64;
}
mkdir -p -- "$validation_root/dispatch_logs"
printf 'mode\texit_code\n' > "$validation_root/dispatch_status.tsv"
overall=0
run_mode() {
  local mode_name=$1 mode=$2
  shift 2
  local result=0
  "$script_root/run_smoke_tests.sh" "$current_image" "$validation_root/shared" \
    "$validation_root/$mode_name" "$mode" "$@" \
    > "$validation_root/dispatch_logs/$mode_name.stdout.log" \
    2> "$validation_root/dispatch_logs/$mode_name.stderr.log" || result=$?
  printf '%s\t%s\n' "$mode_name" "$result" >> "$validation_root/dispatch_status.tsv"
  if [[ $result -ne 0 ]]; then overall=1; fi
}
mkdir -- "$validation_root/shared"
cp -- "$bootstrap_root/harness.py" "$bootstrap_root/preregistered_acceptance_criteria.json" "$validation_root/shared/"
cp -R -- "$bootstrap_root/configs" "$validation_root/shared/configs"
run_mode preparation prepare
[[ -f "$validation_root/preparation/fixture_manifest.json" ]] || {
  echo 'Preparation did not finish; remaining lanes are incomplete.' >&2; exit 1;
}
# Copy only fixture deliverables. Command reports are preserved in preparation/.
cp -- "$validation_root/preparation/"*.tsv "$validation_root/preparation/"*.yaml \
  "$validation_root/preparation/fixture_manifest.json" "$validation_root/shared/"
cp -R -- "$validation_root/preparation/failure_fixtures" "$validation_root/shared/failure_fixtures"
run_mode checks checks
# These are independent fresh containers; no warmed process or mutable cache is shared.
run_mode c1 fit
run_mode c2 fit
for repeat_name in c1 c2; do
  if [[ -f "$validation_root/$repeat_name/run/run_manifest.json" ]]; then
    cp -R -- "$validation_root/$repeat_name" "$validation_root/shared/$repeat_name"
  fi
done
if [[ -f "$validation_root/shared/c1/run/run_manifest.json" && -f "$validation_root/shared/c2/run/run_manifest.json" ]]; then
  run_mode comparison compare --left /data/input/c1/run --right /data/input/c2/run
else
  printf 'comparison\tINCOMPLETE\n' >> "$validation_root/dispatch_status.tsv"
  overall=1
fi
if [[ -f "$validation_root/shared/c1/run/run_manifest.json" ]]; then
  run_mode postprocess postprocess --left /data/input/c1/run
fi
run_mode failures failures --left /data/input/c1/run
cat > "$validation_root/lane_boundaries.json" <<'JSON'
{
  "A_Dev_exact_legacy": "INCOMPLETE: exact historical composite environment unavailable",
  "B_Freeze3_exact_legacy": "INCOMPLETE: Python3.9 metadata and hdbscan0.8.37 API incompatible",
  "C_Freeze3_current": "See dispatch_status.tsv and each harness_report.json; no inferred pass",
  "A_to_B": "UNASSESSABLE",
  "B_to_C": "UNASSESSABLE",
  "native_45_tests": "Coordinator-owned separate locked test overlay and read-only validation mount",
  "fresh_164_1000_seed": "NOT_RUN; retained data not included in this fixture bundle",
  "canonical_native_AMD64": "Separate from Docker Desktop emulation evidence"
}
JSON
exit "$overall"
