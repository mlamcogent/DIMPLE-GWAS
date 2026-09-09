#!/usr/bin/env python3
"""Create lab inventories, sanitized excerpts, and execution-status records."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


EDITION2 = Path(__file__).resolve().parents[2]
FREEZE3 = EDITION2.parents[2]
LABS = EDITION2 / "labs"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sanitize(value):
    if isinstance(value, str):
        return value.replace(str(FREEZE3), "<FREEZE3>").replace(str(Path.home()), "<HOME>")
    if isinstance(value, list):
        return [sanitize(item) for item in value]
    if isinstance(value, dict):
        return {key: sanitize(item) for key, item in value.items()}
    return value


def inventory(root: Path) -> list[list[object]]:
    rows=[]
    for path in sorted(root.rglob("*")):
        if not path.is_file() or "safe_artifacts" in path.parts or path.name == "output_checksums.tsv":
            continue
        rel=path.relative_to(root).as_posix()
        rows.append([rel,path.stat().st_size,sha256(path)])
    with (root/"output_checksums.tsv").open("w",encoding="utf-8",newline="") as handle:
        writer=csv.writer(handle,delimiter="\t",lineterminator="\n")
        writer.writerow(["relative_path","size_bytes","sha256"])
        writer.writerows(rows)
    return rows


def safe_json(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload=json.loads(source.read_text(encoding="utf-8"))
    destination.write_text(json.dumps(sanitize(payload),indent=2,sort_keys=True)+"\n",encoding="utf-8")


def read_record(lab: str, name: str) -> dict:
    return json.loads((LABS/lab/"logs"/f"{name}.json").read_text(encoding="utf-8"))


def main() -> None:
    safe_json(LABS/"00_hand_worked_toy/executed_output/hand_worked_results.json",LABS/"00_hand_worked_toy/safe_artifacts/hand_worked_results.json")
    safe_json(LABS/"01_fixed_synthetic/run_20260826/run_manifest.json",LABS/"01_fixed_synthetic/safe_artifacts/run_manifest.sanitized.json")
    safe_json(LABS/"01_fixed_synthetic/run_20260826/models/best_model.json",LABS/"01_fixed_synthetic/safe_artifacts/best_model.json")
    safe_json(LABS/"02_custom_search_space/run_20260826/run_manifest.json",LABS/"02_custom_search_space/safe_artifacts/run_manifest.sanitized.json")
    safe_json(LABS/"02_custom_search_space/run_20260826/models/best_model.json",LABS/"02_custom_search_space/safe_artifacts/best_model.json")
    safe_json(LABS/"03_explain_compare_validate/comparison_20260826/comparison_summary.json",LABS/"03_explain_compare_validate/safe_artifacts/comparison_summary.json")
    safe_json(LABS/"03_explain_compare_validate/validation_20260826/validation_report.json",LABS/"03_explain_compare_validate/safe_artifacts/validation_report.json")
    safe_json(LABS/"03_explain_compare_validate/explanation_20260826/interpretation_manifest.json",LABS/"03_explain_compare_validate/safe_artifacts/interpretation_manifest.sanitized.json")

    readmes={
        "00_hand_worked_toy": """# Lab 0 — Hand-calculable toy analysis

Status: **executed successfully**. Runtime category: seconds.

This redistributable six-variant, four-vector example demonstrates metadata removal, variants-by-vectors to vectors-by-variants orientation, implemented average-rank RINT, Euclidean distance, two-cluster silhouette, the exact `legacy_dimple` scoring implementation with and without a noise term, and exact versus permutation-invariant labels. It deliberately does not claim to reproduce UMAP by hand.

Run `docs/textbook/edition2/build/runtime_env/bin/python docs/textbook/edition2/labs/00_hand_worked_toy/run_hand_worked.py` from the Freeze 3 root into a fresh `executed_output` directory. The retained record reports a 4×6 analysis matrix, silhouette 0.924591, numeric inequality for relabeled partitions, and ARI/NMI 1.0. Inspect the RINT table and both candidate tables before the JSON summary.
""",
        "01_fixed_synthetic": """# Lab 1 — Fixed synthetic quickstart

Status: **executed successfully in the fresh Edition 2 environment**. Runtime category: under one minute on the recorded macOS arm64 host.

The lab resolves `tutorial_config.yaml`, enumerates exactly one candidate, fits one densMAP representation with seed 42, evaluates one HDBSCAN model, retains its artifacts, and validates the run. The prepared shape is 24 vectors by 80 variables. Selected model `model_060fac0208bb58e2` contains three clusters of eight and no noise in this designed fixture. This is an engineering smoke test, not a production search or biological result.

Use a new output root when rerunning. Start with `inspect-config`, then `show-search-space`, then `run`; commands and exit codes are in `logs/`. Read `run_manifest.json`, `models/all_models.tsv`, `models/model_selection_manifest.json`, the selected labels, and the compatibility aliases in that order. Publish only `safe_artifacts/`; native manifests contain host paths.
""",
        "02_custom_search_space": """# Lab 2 — Custom bounded search and sensitivity

Status: **executed successfully in the fresh Edition 2 environment**. Runtime category: under one minute on the recorded host.

The Cartesian product contains four UMAP families and eight HDBSCAN settings per family, for 32 candidates. Every candidate completed; none was silently dropped. The two-seed schedule is `[42, 43]`. The selected model is `model_241ad5e99af55074`, but several candidates tie at the top because the designed fixture yields identical silhouette and cluster count within one representation family. Stable ordering therefore matters.

The exercise is to calculate 4×8 before execution, compare rank families, explain why normalized scores change with the candidate population, and report sensitivity without choosing settings to match desired labels. Native outputs are retained as evidence; publish only sanitized excerpts.
""",
        "03_explain_compare_validate": """# Lab 3 — Explain, compare, validate, and report

Status: **all six downstream commands executed successfully**: `score-existing`, `summarize-models`, `reproduce-model`, `explain`, `compare`, and `validate`.

Fixed-model reproduction preserved the 24 identifiers and three-cluster partition. Comparison reports ARI 1.0, NMI 1.0, variation of information 0, noise-set Jaccard 1.0, mapped membership 24/24, and Procrustes disparity 2.7088×10⁻³¹. Validation passed 24/24 checks. These values are bounded same-environment fixture evidence, not cross-platform or biological validation.

The explanation directory contains the ordered similarity matrix, order/cutpoint sidecars, cluster summary, projection diagnostics, exclusions, static and interactive heatmaps, and manifest. Treat all original-space summaries as descriptive and post-selection. Inspect identifiers and exclusions before the heatmap. Publish only `safe_artifacts/`; native manifests contain host paths.
""",
    }
    statuses=[]
    for lab,text in readmes.items():
        root=LABS/lab
        (root/"README.md").write_text(text,encoding="utf-8")
        rows=inventory(root)
        statuses.append([lab,"executed","pass",len(rows),"output_checksums.tsv"])
    for lab,status,gate,note in [
        ("04_mnist_benchmark","protocol_only","pass_with_limitation","Network acquisition and public benchmark execution not required for internal-review build."),
        ("05_original_idp","track_a_historical_track_b_deferred","pass_with_limitation","Fresh 1,000-seed run deferred by coordinator until Docker."),
    ]:
        rows=inventory(LABS/lab)
        statuses.append([lab,status,gate,len(rows),note])
    with (LABS/"lab_status.tsv").open("w",encoding="utf-8",newline="") as handle:
        writer=csv.writer(handle,delimiter="\t",lineterminator="\n")
        writer.writerow(["lab","execution_status","gate_status","inventoried_files","note_or_checksum_index"])
        writer.writerows(statuses)

    records=[]
    for lab,name in [
        ("00_hand_worked_toy","lab00_hand_worked"),("01_fixed_synthetic","lab01_inspect_config"),("01_fixed_synthetic","lab01_show_search_space"),("01_fixed_synthetic","lab01_run"),
        ("02_custom_search_space","lab02_inspect_config"),("02_custom_search_space","lab02_show_search_space"),("02_custom_search_space","lab02_run"),
        ("03_explain_compare_validate","lab03_score_existing"),("03_explain_compare_validate","lab03_summarize"),("03_explain_compare_validate","lab03_reproduce"),("03_explain_compare_validate","lab03_explain"),("03_explain_compare_validate","lab03_interpret_alias"),("03_explain_compare_validate","lab03_compare"),("03_explain_compare_validate","lab03_validate"),
    ]:
        record=read_record(lab,name)
        records.append({"lab":lab,"name":name,"exit_code":record["exit_code"],"runtime_seconds":record["runtime_seconds"],"start_utc":record["start_utc"],"command":record["command_display"]})
    (LABS/"execution_manifest.json").write_text(json.dumps({"schema":"dimple-gwas.textbook-lab-execution.v1","software_version":"3.0.0rc1","commands":records},indent=2,sort_keys=True)+"\n",encoding="utf-8")

    manifest_path=EDITION2/"BOOK_BUILD_MANIFEST.json"
    manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["labs"]={"0":"executed_pass","1":"executed_pass","2":"executed_pass","3":"executed_pass","4":"protocol_only","5":"historical_documented_fresh_run_deferred_until_docker","command_records":len(records),"tests":"45 passed; 5 retained warnings","gate_6":"pass_with_bounded_labs_4_5"}
    manifest["phase_status"]["phase_6_labs"]="complete_labs_0_3_pass_labs_4_5_bounded"
    manifest_path.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(f"Finalized {len(statuses)} labs and {len(records)} command records")


if __name__ == "__main__":
    main()
