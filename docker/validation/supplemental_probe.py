#!/usr/bin/env python3
"""RT-006 supplemental engineering coverage; independent of original results."""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import resource
import sys
import time
import traceback


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def safe(value):
    if isinstance(value, dict):
        return {str(k): safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [safe(v) for v in value]
    if hasattr(value, "item"):
        return safe(value.item())
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, Path):
        return str(value)
    return value


def save(path, obj):
    with Path(path).open("x") as stream:
        json.dump(safe(obj), stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write("\n")


def utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class Probe:
    def __init__(self, args):
        self.args = args
        self.input = Path(args.input).resolve(strict=True)
        self.output = Path(args.output).resolve()
        if self.input == self.output or self.input in self.output.parents:
            raise ValueError("Input/output must be separate mount roles")
        if self.output.exists() and (not self.output.is_dir() or any(self.output.iterdir())):
            raise ValueError("Supplemental output must be empty")
        self.output.mkdir(parents=True, exist_ok=True)
        spec_path = self.input / "supplemental_spec.json"
        if sha(spec_path) != args.spec_sha256:
            raise ValueError("Supplemental specification seal mismatch")
        self.spec = json.loads(spec_path.read_text())
        if self.spec["probe_sha256"] != sha(__file__):
            raise ValueError("Supplemental probe implementation hash mismatch")
        if sha(self.input / "synthetic.tsv") != self.spec["fixture_sha256"]:
            raise ValueError("Shared synthetic fixture changed")
        if sha(self.input / "synthetic.yaml") != self.spec["baseline_config_sha256"]:
            raise ValueError("Baseline synthetic config changed")
        import dimple_gwas
        origin = Path(dimple_gwas.__file__).resolve()
        if "site-packages" not in str(origin) or str(origin).startswith(("/data/", "/validation/")):
            raise ValueError("Installed application package required")
        embedded_wheel = Path("/opt/dimple/wheel/dimple_gwas-3.0.0rc1-py3-none-any.whl")
        if not embedded_wheel.is_file() or sha(embedded_wheel) != self.spec["application_wheel_sha256"]:
            raise ValueError("Frozen application wheel identity mismatch")
        self.records = []
        self.started = utc()
        self.environment = {
            "python": sys.version, "machine": platform.machine(), "platform": platform.platform(),
            "package_origin": str(origin), "probe_sha256": sha(__file__), "spec_sha256": args.spec_sha256,
            "application_wheel_sha256": sha(embedded_wheel),
            "runtime_lock_sha256": sha("/opt/dimple/runtime.lock"),
            "package_source_hashes": {p.name: sha(p) for p in sorted(origin.parent.glob("*.py"))},
            "distributions": {d.metadata["Name"]: d.version for d in importlib.metadata.distributions()},
            "thread_environment": {k: os.environ.get(k) for k in ["OMP_NUM_THREADS", "MKL_NUM_THREADS",
                "OPENBLAS_NUM_THREADS", "NUMBA_NUM_THREADS", "NUMEXPR_NUM_THREADS", "PYTHONHASHSEED"]},
        }
        save(self.output / "supplemental_environment.json", self.environment)

    def check(self, name, passed, detail=None, status=None):
        self.records.append({"name": name, "status": status or ("PASS" if passed else "FAIL"), "detail": safe(detail)})

    def call(self, name, description, callback):
        start = utc()
        tick = time.monotonic()
        before = resource.getrusage(resource.RUSAGE_SELF)
        error = None
        result = None
        with (self.output / (name + ".stdout.log")).open("x") as out, (self.output / (name + ".stderr.log")).open("x") as err:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                try:
                    result = callback()
                except Exception as exc:
                    error = {"type": type(exc).__name__, "message": str(exc)}
                    traceback.print_exc()
        after = resource.getrusage(resource.RUSAGE_SELF)
        record = {"api_call": description, "entry_command": sys.argv, "start_utc": start, "end_utc": utc(),
                  "wall_seconds": time.monotonic() - tick, "self_user_seconds": after.ru_utime - before.ru_utime,
                  "self_system_seconds": after.ru_stime - before.ru_stime, "maxrss_highwater_kib": after.ru_maxrss,
                  "exception": error}
        save(self.output / (name + ".invocation.json"), record)
        self.check(name, error is None, record)
        return result

    def finish(self):
        failures = sum(x["status"] == "FAIL" for x in self.records)
        incomplete = sum(x["status"] == "INCOMPLETE" for x in self.records)
        report = {"status": "FAIL" if failures else "PASS_WITH_LIMITATIONS" if incomplete else "PASS",
                  "start_utc": self.started, "end_utc": utc(), "records": self.records,
                  "failure_count": failures, "incomplete_count": incomplete,
                  "spec_sha256": self.args.spec_sha256,
                  "scope": "Supplemental densMAP/DBCV/Parquet/two-seed engineering coverage only",
                  "original_failures_waived": False, "historical_parity_claimed": False}
        save(self.output / "supplemental_report.json", report)
        print(json.dumps({"status": report["status"], "failures": failures}))
        return 1 if failures else 0


def run_probe(p):
    import numpy as np
    import pandas as pd
    import yaml
    from dimple_gwas.config import resolve_config
    from dimple_gwas.pipeline import run_search
    from dimple_gwas.preprocessing import prepare_analysis_matrix
    from dimple_gwas.umap_runner import run_repeated_umap
    from dimple_gwas.validation import run_validation

    config = resolve_config("fixed", p.input / "synthetic.yaml", p.spec["overrides"])
    config["input"]["path"] = str(p.input / "synthetic.tsv")
    save(p.output / "supplemental_config.json", config)
    frame = pd.read_csv(p.input / "synthetic.tsv", sep="\t")
    matrix = prepare_analysis_matrix(frame, config["input"])
    p.check("unchanged_original_matrix_no_pre_reduction", matrix.shape == (24, 80)
            and np.array_equal(matrix.values, frame.iloc[:, 4:].astype(float).T.values)
            and config["input"]["zscore_transform"] == "none")
    np.save(p.output / "analysis_matrix.npy", matrix.to_numpy())
    save(p.output / "ordered_ids.json", matrix.index.tolist())

    # Observe calls without patching any estimator/scientific function. A guard
    # violation stops the operation and is reported, not silently bypassed.
    reducer_calls = []
    def no_reducer_guard(frame, event, arg):
        module = frame.f_globals.get("__name__", "")
        if event == "call" and module.startswith("sklearn.decomposition.") and frame.f_code.co_name in {"fit", "fit_transform", "partial_fit"}:
            reducer_calls.append({"module": module, "function": frame.f_code.co_name})
            raise RuntimeError("Unexpected pre-UMAP decomposition call: " + module + "." + frame.f_code.co_name)

    run = p.output / "run"
    def pipeline_call():
        sys.setprofile(no_reducer_guard)
        try:
            return run_search(config, run, command=sys.argv)
        finally:
            sys.setprofile(None)
    p.call("pipeline", "installed dimple_gwas.pipeline.run_search(config)", pipeline_call)

    # The public CLI exports only the first visualization block. Capture the
    # complete two-seed representation by calling the unchanged installed
    # runner separately, then check its first block against retained CLI data.
    # This is source-linked API coverage; it does not claim the pipeline exports
    # all seed blocks or invent unobserved historical artifacts.
    def embedding_call():
        sys.setprofile(no_reducer_guard)
        try:
            return run_repeated_umap(matrix, config["umap"], repeats=2, n_jobs=1, legacy_sequence=False)
        finally:
            sys.setprofile(None)
    result = p.call("full_embedding_api", "installed dimple_gwas.umap_runner.run_repeated_umap(..., repeats=2)", embedding_call)
    p.check("no_decomposition_estimator_called", not reducer_calls,
            {"observed_calls": reducer_calls, "guard": "sys.setprofile observes sklearn.decomposition fit/fit_transform/partial_fit; no scientific bindings patched"})
    if result is not None:
        embedding = result["embedding"]
        visualization = result["visualization_embedding"]
        p.check("exact_seed_order", result["seeds"] == [42, 43], result["seeds"])
        p.check("full_concatenation_layout", embedding.shape == (24, 4) and embedding.dtype == np.float32,
                {"shape": list(embedding.shape), "dtype": str(embedding.dtype)})
        p.check("visualization_is_first_seed_block", np.array_equal(visualization, embedding[:, :2]))
        p.check("finite_full_embedding", np.isfinite(embedding).all())
        np.save(p.output / "embedding_full.npy", embedding)
        np.save(p.output / "embedding_seed42.npy", embedding[:, :2])
        np.save(p.output / "embedding_seed43.npy", embedding[:, 2:4])
        np.save(p.output / "visualization.npy", visualization)
        save(p.output / "seed_block_mapping.json", {"seeds": [42, 43], "components_per_seed": 2,
            "column_slices_zero_based_half_open": {"42": [0, 2], "43": [2, 4]}, "scaling": "none",
            "origin": "Separate unchanged installed runner API; linked to pipeline through retained first-block identity"})
    manifest_path = run / "run_manifest.json"
    table_path = run / "models/all_models.tsv"
    if not manifest_path.is_file() or not table_path.is_file():
        p.check("complete_run_artifacts", False, "Pipeline did not emit candidate table/manifest")
        return
    manifest = json.loads(manifest_path.read_text())
    rows = pd.read_csv(table_path, sep="\t")
    statuses = rows["status"].value_counts().to_dict()
    p.check("native_candidate_validity", len(rows) == 1 and rows.status.eq("success").all(),
            {"statuses": statuses, "errors": rows[["model_id", "status", "error_message"]].fillna("").to_dict("records")})
    p.check("recorded_active_features", manifest["configuration"]["umap"]["densmap"] is True
            and manifest["configuration"]["execution"]["compute_dbcv"] is True
            and manifest["configuration"]["execution"]["write_parquet"] is True)
    p.check("pipeline_seed_order", manifest["random_seeds"] == [42, 43]
            and all(json.loads(x) == [42, 43] for x in rows["umap_seeds"]), rows["umap_seeds"].tolist())
    dbcv = pd.to_numeric(rows["dbcv"], errors="coerce").to_numpy()
    p.check("dbcv_available_finite", len(dbcv) == 1 and np.isfinite(dbcv).all(),
            {"dbcv": dbcv.tolist(), "metric_warnings": rows["metric_warnings"].fillna("").tolist(),
             "interpretation": "Finite availability check only; no minimum quality or desired sign"})
    parquet_path = run / "models/all_models.parquet"
    p.check("parquet_emitted", parquet_path.is_file() and manifest["parquet_output"]["written"] is True,
            manifest["parquet_output"])
    if parquet_path.is_file():
        parquet = pd.read_parquet(parquet_path)
        try:
            pd.testing.assert_frame_equal(rows, parquet.reset_index(drop=True), check_dtype=False,
                                          check_exact=False, rtol=0, atol=1e-12)
            p.check("parquet_tsv_roundtrip", True)
        except AssertionError as error:
            p.check("parquet_tsv_roundtrip", False, str(error))
    selected = manifest.get("selected_model")
    p.check("selected_native_valid_model", bool(selected) and selected in rows.loc[rows.status.eq("success"), "model_id"].tolist(), selected)
    if selected:
        labels_path = run / "models/top_model_artifacts" / selected / "labels.tsv"
        labels = pd.read_csv(labels_path, sep="\t")
        coords = [x for x in labels if x.startswith("UMAP_")]
        p.check("pipeline_visualization_schema", coords == ["UMAP_1", "UMAP_2"]
                and labels.feature_id.tolist() == matrix.index.tolist() and labels.feature_id.is_unique)
        if result is not None and len(coords) == 2:
            p.check("pipeline_visualization_matches_separate_full_api", np.array_equal(
                    labels[coords].to_numpy(dtype=np.float32), result["visualization_embedding"]))
    validation = p.call("validate", "installed dimple_gwas.validation.run_validation(run)",
                        lambda: run_validation(run, p.output / "validation", command=sys.argv))
    p.check("native_artifact_validator", validation is not None and validation.get("status") == "pass"
            and validation.get("failures") == 0, validation)


def compare_probe(p):
    import numpy as np
    import pandas as pd
    from scipy.spatial import procrustes
    from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
    left, right = Path(p.args.left), Path(p.args.right)
    envs = [json.loads((root / "supplemental_environment.json").read_text()) for root in [left, right]]
    p.check("environment_identity", all(envs[0][key] == envs[1][key] for key in
            ["python", "machine", "distributions", "runtime_lock_sha256", "application_wheel_sha256",
             "package_source_hashes", "thread_environment", "spec_sha256", "probe_sha256"]))
    configs = [json.loads((root / "supplemental_config.json").read_text()) for root in [left, right]]
    p.check("configuration_identity", configs[0] == configs[1])
    for filename in ["ordered_ids.json", "seed_block_mapping.json"]:
        p.check("identity_" + filename, json.loads((left / filename).read_text()) == json.loads((right / filename).read_text()))
    block_metrics = {}
    for name in ["analysis_matrix", "embedding_full", "embedding_seed42", "embedding_seed43", "visualization"]:
        a, b = [np.load(root / (name + ".npy"), allow_pickle=False) for root in [left, right]]
        p.check("exact_repeatability_" + name, np.array_equal(a, b),
                {"shape_left": list(a.shape), "shape_right": list(b.shape), "max_abs_difference": float(np.max(np.abs(a - b)))})
        if name in {"embedding_seed42", "embedding_seed43"}:
            block_metrics[name] = {"exact": bool(np.array_equal(a, b)), "separately_aligned_procrustes_disparity": float(procrustes(a, b)[2])}
    manifests = [json.loads((root / "run/run_manifest.json").read_text()) for root in [left, right]]
    p.check("selected_model_identity", manifests[0]["selected_model"] == manifests[1]["selected_model"])
    labels = [pd.read_csv(root / "run/models/top_model_artifacts" / manifest["selected_model"] / "labels.tsv", sep="\t")
              for root, manifest in zip([left, right], manifests)]
    p.check("label_identifier_order", labels[0].feature_id.tolist() == labels[1].feature_id.tolist())
    a, b = [frame.label.to_numpy() for frame in labels]
    ari = adjusted_rand_score(a, b)
    nmi = normalized_mutual_info_score(a, b, average_method="arithmetic")
    p.check("clustering_repeatability", ari == 1 and nmi == 1 and np.array_equal(a == -1, b == -1),
            {"ari": ari, "nmi": nmi, "noise_masks_identical": bool(np.array_equal(a == -1, b == -1))})
    tables = [pd.read_csv(root / "run/models/all_models.tsv", sep="\t") for root in [left, right]]
    columns = [x for x in tables[0] if "runtime" not in x]
    try:
        pd.testing.assert_frame_equal(tables[0][columns], tables[1][columns], check_dtype=False,
                                      check_exact=False, rtol=0, atol=1e-12)
        p.check("candidate_metric_score_schema_repeatability", True)
    except AssertionError as error:
        p.check("candidate_metric_score_schema_repeatability", False, str(error))
    save(p.output / "per_seed_comparison.json", {"separate_seed_blocks": block_metrics,
         "interpretation": "Per-block alignment reported separately; exact raw repeatability required before concatenated comparison",
         "historical_or_stability_claim": False})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["run", "compare"])
    parser.add_argument("--input", default="/data/input")
    parser.add_argument("--output", default="/data/output")
    parser.add_argument("--spec-sha256", required=True)
    parser.add_argument("--left")
    parser.add_argument("--right")
    args = parser.parse_args()
    if args.mode == "compare" and (not args.left or not args.right):
        parser.error("compare requires --left and --right")
    p = Probe(args)
    try:
        (run_probe if args.mode == "run" else compare_probe)(p)
    except Exception as error:
        (p.output / "supplemental_exception.log").write_text(traceback.format_exc())
        p.check("probe_exception", False, {"type": type(error).__name__, "message": str(error)})
    return p.finish()


if __name__ == "__main__":
    raise SystemExit(main())
