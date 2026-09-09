#!/usr/bin/env python3
"""External validation driver. Scientific work runs only in an installed container.

Every invocation gets an empty output directory. This driver never edits a
package, adjusts an acceptance threshold, or imports a source-tree checkout.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import resource
import shutil
import subprocess
import sys
import time
import traceback


CRITERIA_SHA256 = "ddb9488380abb0f1782ea496fbbac3723a5a030e1c70141285a6b8c29f8fbd28"
SUBCOMMANDS = ["run", "inspect-config", "show-search-space", "score-existing",
               "summarize-models", "reproduce-model", "explain", "interpret", "compare", "validate"]
ENV_KEYS = ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
            "NUMBA_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "PYTHONHASHSEED"]


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def clean(value):
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(v) for v in value]
    if hasattr(value, "item"):
        return clean(value.item())
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, Path):
        return str(value)
    return value


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(clean(value), stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")


def utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class Harness:
    def __init__(self, args):
        self.args = args
        self.input = Path(args.input).resolve(strict=True)
        self.output = Path(args.output).resolve()
        if self.output.exists() and (not self.output.is_dir() or any(self.output.iterdir())):
            raise ValueError(f"Output must be an empty directory: {self.output}")
        self.output.mkdir(parents=True, exist_ok=True)
        if self.input == self.output or self.input in self.output.parents:
            raise ValueError("Input and output must be separate sibling mount roles")
        criteria_path = self.input / "preregistered_acceptance_criteria.json"
        if digest(criteria_path) != CRITERIA_SHA256:
            raise ValueError("Sealed preregistration digest mismatch; refusing execution")
        self.criteria = json.loads(criteria_path.read_text())
        self.records = []
        self.started = utc()
        import dimple_gwas
        origin = str(Path(dimple_gwas.__file__).resolve())
        if origin.startswith(("/data/", "/validation/")) or "site-packages" not in origin:
            raise RuntimeError(f"Installed distribution required; found {origin}")
        self.environment = {
            "python": sys.version, "executable": sys.executable, "package_origin": origin,
            "platform": platform.platform(), "machine": platform.machine(),
            "thread_environment": {key: os.environ.get(key) for key in ENV_KEYS},
            "packages": {d.metadata["Name"]: d.version for d in importlib.metadata.distributions()},
            "criteria_sha256": CRITERIA_SHA256,
            "harness_sha256": digest(__file__),
            "installed_package_source_hashes": {str(p.relative_to(Path(origin).parent)): digest(p)
                                                 for p in sorted(Path(origin).parent.rglob("*.py"))},
        }
        write_json(self.output / "environment.json", self.environment)
        # Prepared fixtures must remain byte-identical across images and processes.
        manifest = self.input / "fixture_manifest.json"
        if manifest.is_file():
            fixture = json.loads(manifest.read_text())
            for name, sha in fixture["files"].items():
                if digest(self.input / name) != sha:
                    raise ValueError(f"Shared fixture digest mismatch: {name}")

    def record(self, name, passed, detail=None, status=None):
        self.records.append({"name": name, "status": status or ("PASS" if passed else "FAIL"),
                             "detail": clean(detail)})

    def cli(self, name, arguments, expected_failure=False, diagnostic=None):
        command = [sys.executable, "-m", "dimple_gwas", *map(str, arguments)]
        logs = self.output / "commands"
        logs.mkdir(exist_ok=True)
        outpath, errpath = logs / (name + ".stdout.log"), logs / (name + ".stderr.log")
        start, wall = utc(), time.monotonic()
        before = resource.getrusage(resource.RUSAGE_CHILDREN)
        timed_out = False
        with outpath.open("x") as out, errpath.open("x") as err:
            try:
                result = subprocess.run(command, stdout=out, stderr=err, cwd="/tmp",
                                        timeout=self.args.command_timeout, check=False)
                code = result.returncode
            except subprocess.TimeoutExpired:
                code, timed_out = 124, True
        after = resource.getrusage(resource.RUSAGE_CHILDREN)
        text = outpath.read_text(errors="replace") + "\n" + errpath.read_text(errors="replace")
        meaningful = bool(text.strip())
        recognized = diagnostic is None or any(word.lower() in text.lower() for word in diagnostic)
        passed = (code != 0 and not timed_out and meaningful and recognized) if expected_failure else code == 0
        record = {"command": command, "start_utc": start, "end_utc": utc(), "exit_code": code,
                  "timeout": timed_out, "wall_seconds": time.monotonic() - wall,
                  "child_user_seconds": after.ru_utime - before.ru_utime,
                  "child_system_seconds": after.ru_stime - before.ru_stime,
                  "child_maxrss_process_highwater_kib": after.ru_maxrss,
                  "expected_failure": expected_failure, "diagnostic_recognized": recognized,
                  "stdout": str(outpath), "stderr": str(errpath)}
        write_json(logs / (name + ".json"), record)
        self.record(name, passed, record)
        return code

    def finish(self):
        failures = [r for r in self.records if r["status"] == "FAIL"]
        unknown = [r for r in self.records if r["status"] in {"INCOMPLETE", "NOT_EMITTED", "UNASSESSABLE"}]
        report = {"mode": self.args.mode, "start_utc": self.started, "end_utc": utc(),
                  "status": "FAIL" if failures else "PASS_WITH_LIMITATIONS" if unknown else "PASS",
                  "criteria_sha256": CRITERIA_SHA256, "records": self.records,
                  "failure_count": len(failures), "limitations_count": len(unknown),
                  "scope": "Current-image engineering checks; exact historical A/B parity is not established"}
        write_json(self.output / "harness_report.json", report)
        print(json.dumps({"status": report["status"], "failures": len(failures), "report": str(self.output / "harness_report.json")}))
        return 1 if failures else 0


def prepare(h):
    import numpy as np
    import pandas as pd
    import yaml
    rng = np.random.default_rng(20260722)
    variants = 80
    x = np.linspace(0, 4 * np.pi, variants)
    templates = [np.sin(x), np.cos(x), np.where(np.arange(variants) < 40, -1.0, 1.0)]
    data = {"CHR": np.ones(variants, dtype=int), "BP": np.arange(variants),
            "A1": ["A"] * variants, "A2": ["G"] * variants}
    for group, template in enumerate(templates):
        for member in range(8):
            data[f"trait_g{group}_{member}"] = template + rng.normal(0, .06, variants)
    frame = pd.DataFrame(data)
    frame.to_csv(h.output / "synthetic.tsv", sep="\t", index=False)
    stress = frame.copy()
    stress["isolated_ramp"] = 100 * (np.arange(variants) - 40)
    stress["tied_g0_0"] = frame["trait_g0_0"]
    stress.to_csv(h.output / "synthetic_stress.tsv", sep="\t", index=False)
    fixture = next(f for f in h.criteria["fixtures"] if f["id"] == "synthetic_native24")
    config = {}
    for dotted, value in fixture["configuration"].items():
        if "." in dotted:
            section, key = dotted.split(".", 1)
            config.setdefault(section, {})[key] = value
        else:
            config[dotted] = value
    config["input"].update(path="/data/input/synthetic.tsv", sep="\t", annotation_file=None)
    config["scoring"] = {"profile": "legacy_dimple", "fit_include_noise": False}
    with (h.output / "synthetic.yaml").open("x") as stream:
        yaml.safe_dump(config, stream, sort_keys=True)
    stress_config = copy.deepcopy(config)
    stress_config["input"]["path"] = "/data/input/synthetic_stress.tsv"
    with (h.output / "synthetic_stress.yaml").open("x") as stream:
        yaml.safe_dump(stress_config, stream, sort_keys=True)
    metadata = {"CHR": [1] * 4, "BP": [1, 2, 3, 4], "A1": ["A"] * 4, "A2": ["G"] * 4}
    pd.DataFrame({**metadata, "a": [1, 2, 2, 4], "b": [4, 2, 2, 1], "c": [5] * 4}).to_csv(
        h.output / "analytic_preprocess.tsv", sep="\t", index=False)
    pd.DataFrame({"candidate_ordinal": [1, 2, 3, 4], "model_id": ["m1", "m2", "m3", "m4"],
                  "status": ["success"] * 3 + ["failed"], "silhouette": [.2, .5, .4, np.nan],
                  "number_of_clusters": [3, 2, 5, np.nan], "number_of_noise_points": [1, 3, 2, np.nan],
                  "noise_fraction": [.1, .3, .2, np.nan], "largest_cluster_fraction": [.5, .4, .3, np.nan],
                  "error_message": ["", "", "", "intentional fixture failure"]}).to_csv(
        h.output / "analytic_models.tsv", sep="\t", index=False)
    bad = h.output / "failure_fixtures"
    bad.mkdir()
    for name, value in [("non_numeric", "abc"), ("nan", np.nan), ("positive_inf", np.inf), ("negative_inf", -np.inf)]:
        changed = frame.astype(object)
        changed.iloc[0, 4] = value
        changed.to_csv(bad / f"{name}.tsv", sep="\t", index=False)
    frame.iloc[:0].to_csv(bad / "header_only.tsv", sep="\t", index=False)
    (bad / "zero_byte.tsv").touch()
    frame.iloc[:, :4].to_csv(bad / "metadata_only.tsv", sep="\t", index=False)
    frame.iloc[:, :6].to_csv(bad / "too_small.tsv", sep="\t", index=False)
    duplicate = frame.copy()
    duplicate.columns = [*frame.columns[:5], frame.columns[4], *frame.columns[6:]]
    duplicate.to_csv(bad / "duplicate_headers.tsv", sep="\t", index=False)
    pd.DataFrame({"feature_id": ["a", "a"], "label": [0, 1]}).to_csv(bad / "duplicate_labels.tsv", sep="\t", index=False)
    pd.DataFrame({"feature_id": ["a", "b"], "label": [0, 1]}).to_csv(bad / "valid_labels.tsv", sep="\t", index=False)
    pd.DataFrame({"feature_id": ["a", "b"]}).to_csv(bad / "missing_label.tsv", sep="\t", index=False)
    # Manual orientation oracle: IDs occur in matrix columns, never in metadata rows.
    pd.DataFrame({"feature_id": list(frame.columns[4:]), "label": [i // 8 for i in range(24)]}).to_csv(
        bad / "orientation_labels.tsv", sep="\t", index=False)
    paths = [p for p in h.output.rglob("*") if p.is_file() and p.name != "environment.json"]
    write_json(h.output / "fixture_manifest.json", {"authority": "analytic conformance plus implementation regression",
               "generating_command": sys.argv, "generating_environment": h.environment,
               "files": {str(p.relative_to(h.output)): digest(p) for p in sorted(paths)}})
    h.record("prepared_shared_fixture", True, {"rows": 80, "vectors": 24, "stress_vectors": 26})


def checks(h):
    import importlib
    import re
    import numpy as np
    import pandas as pd
    from scipy.stats import norm
    from dimple_gwas.preprocessing import prepare_analysis_matrix
    from dimple_gwas.umap_runner import ensemble_seeds
    # Inspect the image's declared runtime lock, not an assumption that every
    # optional extra was requested. Current release profile is core/Pillow.
    profile_lock = next((p for p in [Path("/opt/dimple/runtime.lock"), Path("/staging/locks/runtime.lock")]
                         if p.is_file()), None)
    locked_distributions = set()
    if profile_lock:
        locked_distributions = {re.split(r"==", line.strip(), maxsplit=1)[0].lower().replace("_", "-")
                                for line in profile_lock.read_text().splitlines()
                                if re.match(r"^[A-Za-z0-9_.-]+==", line.strip())}
        h.record("declared_runtime_profile", True,
                 {"runtime_lock": str(profile_lock), "sha256": digest(profile_lock),
                  "optional_plotting_distributions": sorted(locked_distributions & {"matplotlib", "plotly"}),
                  "core_visualization": "Pillow"})
    else:
        h.record("declared_runtime_profile", False, "Runtime lock not available inside image", "INCOMPLETE")
    for module in ["numpy", "pandas", "scipy", "sklearn", "umap", "hdbscan", "numba", "llvmlite",
                   "joblib", "yaml", "pyarrow", "openpyxl", "xlrd", "PIL", "matplotlib", "plotly"]:
        try:
            loaded = importlib.import_module(module)
            h.record("import_" + module, True, {"origin": getattr(loaded, "__file__", None),
                     "version": getattr(loaded, "__version__", "see distribution inventory")})
        except ModuleNotFoundError as error:
            if module in {"matplotlib", "plotly"} and profile_lock and module not in locked_distributions and error.name == module:
                h.record("import_" + module, True,
                         {"reason": "Optional plotting extra excluded from declared core runtime profile",
                          "profile_evidence": str(profile_lock)}, "NOT_INSTALLED_OPTIONAL")
            else:
                h.record("import_" + module, False, {"type": type(error).__name__, "message": str(error)})
        except Exception as error:
            h.record("import_" + module, False, {"type": type(error).__name__, "message": str(error)})
    h.cli("version", ["--version"])
    h.cli("help", ["--help"])
    for command in SUBCOMMANDS:
        h.cli("help_" + command, [command, "--help"])
    paths = sorted((h.input / "configs").glob("*.yaml"))
    h.record("seven_configs_present", len(paths) == 7, [p.name for p in paths])
    import yaml
    for path in paths:
        mode = yaml.safe_load(path.read_text()).get("search_mode", "standard")
        options = ["--config", path, "--search-mode", mode]
        h.cli("inspect_" + path.stem, ["inspect-config", *options])
        h.cli("enumerate_" + path.stem, ["show-search-space", *options, "--show-first", "0",
                                        "--output-dir", h.output / "grids" / path.stem])
    h.cli("enumerate_synthetic", ["show-search-space", "--search-mode", "fixed", "--config", h.input / "synthetic.yaml",
                                  "--show-first", "0", "--output-dir", h.output / "grids" / "synthetic"])
    frame = pd.read_csv(h.input / "analytic_preprocess.tsv", sep="\t")
    expected = frame.iloc[:, 4:].astype(float).T
    actual = prepare_analysis_matrix(frame, {"drop_first_n_cols": 4, "zscore_transform": "none"})
    h.record("analytic_none_transpose", np.array_equal(actual.values, expected.values) and list(actual.index) == ["a", "b", "c"])
    transformed = prepare_analysis_matrix(frame, {"drop_first_n_cols": 4, "zscore_transform": "rint"})
    q = norm.ppf([.125, .5, .5, .875])
    h.record("analytic_tied_rint", np.allclose(transformed.values, [q, q[::-1], np.zeros(4)], rtol=0, atol=1e-12))
    reordered = frame.iloc[::-1][[*frame.columns[:4], "c", "a", "b"]]
    observed = prepare_analysis_matrix(reordered, {"drop_first_n_cols": 4, "zscore_transform": "none"})
    h.record("analytic_reordering", np.array_equal(observed.loc[["a", "b", "c"]].values[:, ::-1], expected.values))
    h.record("seed_schedule", ensemble_seeds({"random_state": 42}, 2, False) == [42, 43]
             and ensemble_seeds({"random_state": 42}, 3, True) == [1, 2, 3])
    destination = h.output / "analytic_rescored.tsv"
    if h.cli("analytic_score", ["score-existing", "--models", h.input / "analytic_models.tsv",
                                "--fit-include-noise", "--output", destination]) == 0:
        scored = pd.read_csv(destination, sep="\t").set_index("model_id")
        h.record("analytic_raw_scores", np.allclose(scored.loc[["m1", "m2", "m3"], "raw_score"],
                 [188 / 795, -5 / 53, 286 / 795], rtol=0, atol=1e-12))
        h.record("analytic_normalized_scores", np.allclose(scored.loc[["m1", "m2", "m3"], "score"],
                 [263 / 361, 0, 1], rtol=0, atol=1e-12))
        h.record("analytic_ranking_failure_retained", list(scored.index[:3]) == ["m3", "m1", "m2"]
                 and scored.loc["m4", "status"] == "failed" and pd.isna(scored.loc["m4", "rank"]))
        h.cli("analytic_summarize", ["summarize-models", "--models", destination, "--output-dir", h.output / "analytic_summary"])
    from dimple_gwas.scoring import legacy_dimple_score
    singleton = pd.read_csv(h.input / "analytic_models.tsv", sep="\t").iloc[:1]
    score, manifest = legacy_dimple_score(singleton, fit_include_noise=False)
    h.record("analytic_zero_range_noise_exclusion", score.iloc[0]["score"] == 1 and manifest["weights"]["number_of_noise_points"] == 0)


def capture_run(h, run):
    import pandas as pd
    import numpy as np
    from dimple_gwas.preprocessing import prepare_analysis_matrix
    manifest = json.loads((run / "run_manifest.json").read_text())
    frame = pd.read_csv(h.input / "synthetic.tsv", sep="\t")
    matrix = prepare_analysis_matrix(frame, manifest["configuration"]["input"])
    matrix.to_csv(h.output / "preprocessed_matrix.tsv", sep="\t", index=True)
    rows = pd.read_csv(run / "models/all_models.tsv", sep="\t")
    h.record("candidate_grid_fixed_one", len(rows) == 1 and manifest["search_space_size"] == 1)
    h.record("all_candidates_successful", rows["status"].eq("success").all(), rows["status"].value_counts().to_dict())
    selected = manifest.get("selected_model")
    h.record("selected_model_present", bool(selected), selected)
    if selected:
        labels = pd.read_csv(run / "models/top_model_artifacts" / selected / "labels.tsv", sep="\t")
        h.record("ordered_vector_ids", labels["feature_id"].tolist() == matrix.index.tolist())
        coords = sorted([x for x in labels if x.startswith("UMAP_")], key=lambda x: int(x.split("_")[-1]))
        h.record("single_seed_complete_embedding", manifest["random_seeds"] == [42] and len(coords) == 2,
                 "Full clustering coordinates equal the visualization only because fixture has one seed")
        h.record("finite_coordinates", bool(np.isfinite(labels[coords].values).all()))
    for item in ["membership_probabilities", "outlier_scores", "per_cluster_persistence", "condensed_tree"]:
        h.record(item, False, "Native public run artifacts do not emit this auxiliary; scientific parity for it is unassessed", "NOT_EMITTED")


def fit(h):
    run = h.output / "run"
    if h.cli("fixed_run", ["run", "--search-mode", "fixed", "--config", h.input / "synthetic.yaml", "--output-dir", run]) == 0:
        h.cli("validate", ["validate", "--run-dir", run, "--output-dir", h.output / "validation"])
        capture_run(h, run)


def rho(a, b):
    import numpy as np
    from scipy.stats import spearmanr
    a, b = np.asarray(a), np.asarray(b)
    if len(a) == 0:
        return None
    if np.array_equal(a, b) and (len(a) == 1 or np.ptp(a) == 0):
        return 1.0
    answer = float(spearmanr(a, b).statistic)
    return answer if math.isfinite(answer) else None


def compare(h):
    import numpy as np
    import pandas as pd
    from scipy.spatial import procrustes
    from scipy.spatial.distance import pdist, squareform
    from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
    from sklearn.manifold import trustworthiness
    left, right = Path(h.args.left).resolve(strict=True), Path(h.args.right).resolve(strict=True)
    environments = [json.loads((root.parent / "environment.json").read_text()) for root in [left, right]]
    h.record("installed_source_identity", environments[0]["installed_package_source_hashes"] == environments[1]["installed_package_source_hashes"])
    if h.args.comparison_class == "same_image":
        h.record("environment_identity", all(environments[0][key] == environments[1][key]
                 for key in ["python", "packages", "thread_environment", "machine"]))
    preprocessing = [pd.read_csv(root.parent / "preprocessed_matrix.tsv", sep="\t", index_col=0) for root in [left, right]]
    preprocessing_exact = preprocessing[0].equals(preprocessing[1])
    preprocessed_close = (list(preprocessing[0].index) == list(preprocessing[1].index)
                         and list(preprocessing[0].columns) == list(preprocessing[1].columns)
                         and np.allclose(preprocessing[0], preprocessing[1], rtol=0, atol=1e-12))
    h.record("preprocessed_matrix_identity", preprocessed_close,
             {"exact": preprocessing_exact, "max_abs_difference": float(np.max(np.abs(preprocessing[0].values - preprocessing[1].values)))})
    if h.args.comparison_class != "same_image":
        h.record("historical_boundary", False, "Compatibility image is not exact historical Lane B; comparison is exploratory and confounded", "UNASSESSABLE")
    lm, rm = [json.loads((root / "run_manifest.json").read_text()) for root in [left, right]]
    lb, rb = [json.loads((root / "models/best_model.json").read_text()) for root in [left, right]]
    h.record("input_hash_identity", lm["input"]["sha256"] == rm["input"]["sha256"])
    h.record("configuration_identity", lm["configuration"] == rm["configuration"])
    h.record("seed_identity", lm["random_seeds"] == rm["random_seeds"] == [42])
    h.record("candidate_grid_identity", digest(left / "search_space_manifest.tsv") == digest(right / "search_space_manifest.tsv"))
    h.record("selected_model_identity", lm["selected_model"] == rm["selected_model"] and lb["parameters"] == rb["parameters"])
    if not lm.get("selected_model") or not rm.get("selected_model"):
        h.record("scientific_comparison", False, "No selected model; cannot compare geometry or labels")
        return
    lt, rt = [pd.read_csv(root / "models/top_model_artifacts" / manifest["selected_model"] / "labels.tsv", sep="\t")
              for root, manifest in [(left, lm), (right, rm)]]
    ids = lt["feature_id"].tolist()
    identity = ids == rt["feature_id"].tolist() and len(ids) == len(set(ids))
    h.record("ordered_id_identity", identity)
    if not identity:
        return
    a, b = lt["label"].to_numpy(), rt["label"].to_numpy()
    na, nb = a == -1, b == -1
    union = int((na | nb).sum())
    nj = float((na & nb).sum() / union) if union else 1.
    ari, nmi = adjusted_rand_score(a, b), normalized_mutual_info_score(a, b, average_method="arithmetic")
    metrics = {"ari": ari, "nmi": nmi, "noise_jaccard": nj, "noise_fraction_abs_difference": abs(na.mean() - nb.mean()),
               "cluster_count_left": len(set(a) - {-1}), "cluster_count_right": len(set(b) - {-1}),
               "cluster_sizes_left": sorted(int((a == label).sum()) for label in set(a) - {-1}),
               "cluster_sizes_right": sorted(int((b == label).sum()) for label in set(b) - {-1})}
    h.record("clustering_repeatability", ari == 1 and nmi == 1 and np.array_equal(na, nb), metrics)
    coords = sorted([c for c in lt if c.startswith("UMAP_")], key=lambda x: int(x.split("_")[-1]))
    A, B = lt[coords].to_numpy(float), rt[coords].to_numpy(float)
    h.record("raw_coordinate_repeatability", np.array_equal(A, B), {"max_abs": float(np.max(np.abs(A - B)))})
    dist_a, dist_b = pdist(A), pdist(B)
    k = h.criteria["measurement"]["knn"]["k"]
    neighbors = []
    for distances in [dist_a, dist_b]:
        square = squareform(distances)
        np.fill_diagonal(square, np.inf)
        neighbors.append([set(sorted(range(len(ids)), key=lambda j: (square[i, j], str(ids[j])))[:k]) for i in range(len(ids))])
    overlap = float(np.mean([len(x & y) / k for x, y in zip(*neighbors)]))
    original = pd.read_csv(h.input / "synthetic.tsv", sep="\t").iloc[:, 4:].astype(float).T.values
    disparity = float(procrustes(A, B)[2])
    metrics.update(pairwise_spearman=rho(dist_a, dist_b), knn_overlap=overlap, procrustes_disparity=disparity,
                   trustworthiness_left=float(trustworthiness(original, A, n_neighbors=k)),
                   trustworthiness_right=float(trustworthiness(original, B, n_neighbors=k)))
    metrics["trustworthiness_abs_difference"] = abs(metrics["trustworthiness_left"] - metrics["trustworthiness_right"])
    h.record("geometry_repeatability", np.array_equal(dist_a, dist_b) and overlap == 1 and metrics["trustworthiness_abs_difference"] == 0, metrics)
    # The complete one-seed representation is available. Multi-seed public output
    # is only visualization, so never silently apply this method to many seeds.
    h.record("geometry_scope", lm["random_seeds"] == rm["random_seeds"] == [42], "One complete seed block only")
    frames = [pd.read_csv(root / "models/all_models.tsv", sep="\t").set_index("model_id") for root in [left, right]]
    lf, rf = frames
    schema_same = list(lf.columns) == list(rf.columns) and list(lf.index) == list(rf.index)
    h.record("candidate_schema_join", schema_same)
    deltas = {}
    if schema_same:
        h.record("candidate_status_mask", lf["status"].equals(rf["status"]))
        deltas, non_numeric = {}, {}
        for col in lf.columns:
            if "runtime" in col:
                continue
            if pd.api.types.is_numeric_dtype(lf[col]) and pd.api.types.is_numeric_dtype(rf[col]):
                va, vb = lf[col].to_numpy(float), rf[col].to_numpy(float)
                masks_match = (np.array_equal(np.isnan(va), np.isnan(vb))
                               and np.array_equal(np.isfinite(va), np.isfinite(vb))
                               and np.array_equal(va[np.isinf(va)], vb[np.isinf(vb)]))
                delta = float(np.max(np.abs(va[np.isfinite(va)] - vb[np.isfinite(va)]))) if masks_match and np.isfinite(va).any() else 0. if masks_match else math.inf
                deltas[col] = delta
            else:
                non_numeric[col] = lf[col].fillna("<NA>").equals(rf[col].fillna("<NA>"))
        h.record("per_candidate_numeric_maximum", all(v <= 1e-12 for v in deltas.values()), deltas)
        h.record("per_candidate_categorical_identity", all(non_numeric.values()), non_numeric)
        metrics["score_rank_spearman"] = rho(lf.loc[lf.status.eq("success"), "score"], rf.loc[rf.status.eq("success"), "score"])
    ranked = [pd.read_csv(root / "models/ranked_models.tsv", sep="\t") for root in [left, right]]
    h.record("ranking_identity", ranked[0]["model_id"].tolist() == ranked[1]["model_id"].tolist())
    top = [frame.loc[frame.status.eq("success"), "model_id"].tolist()[:10] for frame in ranked]
    metrics["top_k_overlap"] = len(set(top[0]) & set(top[1])) / len(top[0]) if top[0] else None
    inventories = [sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()) for root in [left, right]]
    h.record("run_output_inventory", inventories[0] == inventories[1], {"left": inventories[0], "right": inventories[1]})
    for relative in inventories[0]:
        if relative in inventories[1] and Path(relative).suffix in {".tsv", ".csv"}:
            sep = "\t" if relative.endswith("tsv") else ","
            ltab, rtab = [pd.read_csv(root / relative, sep=sep) for root in [left, right]]
            h.record("schema_" + relative, list(ltab.columns) == list(rtab.columns) and ltab.shape == rtab.shape)
    h.cli("native_compare", ["compare", "--left", left / "models/top_model_artifacts" / lm["selected_model"] / "summary.json",
                            "--right", right / "models/top_model_artifacts" / rm["selected_model"] / "summary.json",
                            "--require-same-order", "--output-dir", h.output / "native_compare"])
    metrics["classification"] = ("DIVERGENT" if any(r["status"] == "FAIL" for r in h.records)
                                 else "EXACT_PARITY" if preprocessing_exact and all(v == 0 for v in deltas.values())
                                 else "COMPATIBLE_WITHIN_PREREGISTERED_TOLERANCE")
    metrics["comparison_scope"] = "Emitted outputs of fixed single-seed fixture only; not complete scientific or historical parity"
    metrics["limitations"] = ["No emitted membership/outlier/per-cluster persistence/condensed-tree artifacts",
                              "Fixed one-candidate fixture cannot test selection across competing candidates",
                              "Historical A:B and B:C remain unassessed"]
    write_json(h.output / "comparison_metrics.json", metrics)
    h.record("unemitted_auxiliary_scope", False, metrics["limitations"], "NOT_EMITTED")


def postprocess(h):
    import numpy as np
    import pandas as pd
    run = Path(h.args.left or (h.input / "c1/run"))
    manifest = json.loads((run / "run_manifest.json").read_text())
    selected = manifest.get("selected_model")
    if not selected:
        h.record("postprocess_selected", False, "Input run has no selected model")
        return
    summary = run / "models/top_model_artifacts" / selected / "summary.json"
    destination = h.output / "rescored.tsv"
    if h.cli("rescore", ["score-existing", "--models", run / "models/all_models.tsv", "--output", destination]) == 0:
        original = pd.read_csv(run / "models/all_models.tsv", sep="\t").set_index("model_id")
        scored = pd.read_csv(destination, sep="\t").set_index("model_id").reindex(original.index)
        h.record("score_reproduction", np.allclose(original[["score", "raw_score"]], scored[["score", "raw_score"]], rtol=0, atol=1e-12, equal_nan=True))
        h.cli("summarize", ["summarize-models", "--models", destination, "--output-dir", h.output / "summary"])
    reproduced = h.output / "reproduced"
    if h.cli("reproduce", ["reproduce-model", "--model-json", summary, "--input", h.input / "synthetic.tsv",
                           "--n-jobs", "1", "--output-dir", reproduced]) == 0:
        h.cli("validate_reproduced", ["validate", "--run-dir", reproduced, "--output-dir", h.output / "reproduced_validation"])
        payload = json.loads((reproduced / "run_manifest.json").read_text())
        h.record("reproduced_selection", payload.get("selected_model") == selected)
        if payload.get("selected_model"):
            h.cli("compare_reproduced", ["compare", "--left", summary,
                  "--right", reproduced / "models/top_model_artifacts" / payload["selected_model"] / "summary.json",
                  "--require-same-order", "--output-dir", h.output / "reproduced_comparison"])
            original_labels = pd.read_csv(summary.parent / "labels.tsv", sep="\t")
            reproduced_labels = pd.read_csv(reproduced / "models/top_model_artifacts" / payload["selected_model"] / "labels.tsv", sep="\t")
            h.record("reproduced_labels_and_coordinates", original_labels.equals(reproduced_labels))
    for metric in ["pearson", "spearman"]:
        explanation = h.output / ("explanation_" + metric)
        if h.cli("explain_" + metric, ["explain", "--model-json", summary, "--input", h.input / "synthetic.tsv",
              "--similarity-metric", metric, "--write-similarity", "--outdir", explanation]) == 0:
            matrix_path = explanation / "original_space_similarity.tsv.gz"
            if matrix_path.is_file():
                observed = pd.read_csv(matrix_path, sep="\t", index_col=0)
                expected = pd.read_csv(h.input / "synthetic.tsv", sep="\t").iloc[:, 4:].corr(method=metric)
                expected = expected.loc[observed.index, observed.columns]
                h.record("original_space_" + metric + "_oracle", np.allclose(observed, expected, rtol=0, atol=1e-12),
                         {"max_abs_difference": float(np.max(np.abs(observed.values - expected.values)))})
            else:
                h.record("original_space_" + metric + "_oracle", False, "Requested full similarity matrix not emitted", "INCOMPLETE")
    stress = h.output / "stress_run"
    stress_code = h.cli("stress_dense_isolated_tied_command", ["run", "--search-mode", "fixed", "--config",
                       h.input / "synthetic_stress.yaml", "--output-dir", stress])
    inspect_stress_outcome(h, stress, stress_code)
    h.record("native_multi_candidate_tests", False, "45-case native suite is executed and reported separately by coordinator; includes four-candidate EOM/leaf and max-size coverage", "UNASSESSABLE")


def inspect_stress_outcome(h, run, command_exit):
    """Assess bookkeeping/validity, without asserting a desired clustering."""
    import pandas as pd
    required = [run / "models/all_models.tsv", run / "run_manifest.json",
                run / "search_space_manifest.json", run / "logs/model_failures.tsv"]
    absent = [str(path.relative_to(run)) for path in required if not path.is_file()]
    if absent:
        h.record("stress_dense_isolated_tied", False,
                 {"command_exit": command_exit, "missing_artifacts": absent,
                  "reason": "A zero command exit is insufficient without candidate and provenance artifacts"})
        return
    manifest = json.loads((run / "run_manifest.json").read_text())
    grid = json.loads((run / "search_space_manifest.json").read_text())
    candidates = pd.read_csv(run / "models/all_models.tsv", sep="\t")
    failure_ledger = pd.read_csv(run / "logs/model_failures.tsv", sep="\t")
    schema = {"model_id", "status", "error_message"}
    missing_columns = sorted(schema - set(candidates.columns))
    if missing_columns or "model_id" not in failure_ledger.columns:
        h.record("stress_dense_isolated_tied", False,
                 {"missing_candidate_columns": missing_columns, "failure_ledger_columns": list(failure_ledger.columns)})
        return
    counts = candidates["status"].value_counts().to_dict()
    failures = candidates.loc[candidates.status.eq("failed")]
    invalid = candidates.loc[candidates.status.eq("invalid_topology")]
    successes = candidates.loc[candidates.status.eq("success")]
    errors = candidates.loc[~candidates.status.eq("success"), ["model_id", "status", "error_message"]].fillna("").to_dict("records")
    valid_statuses = set(counts).issubset({"success", "failed", "invalid_topology"})
    failure_ids = failures.model_id.tolist()
    selected = manifest.get("selected_model")
    bookkeeping = {
        "nonempty_unique_candidate_ids": len(candidates) > 0 and candidates.model_id.notna().all()
                                         and candidates.model_id.is_unique,
        "declared_candidate_count": len(candidates) == grid.get("candidate_models") == manifest.get("search_space_size"),
        "known_candidate_statuses": valid_statuses,
        "failed_count_matches_manifest": len(failures) == manifest.get("failed_models"),
        "completed_count_matches_manifest": len(successes) + len(invalid) == manifest.get("completed_models"),
        "failure_ledger_exact": sorted(failure_ids) == sorted(failure_ledger.model_id.tolist()),
        "unsuccessful_candidates_have_diagnostics": all(bool(row["error_message"].strip()) for row in errors),
        "selected_model_valid_if_present": selected in successes.model_id.tolist() if selected else len(successes) == 0,
        "manifest_complete": manifest.get("status") == "complete",
    }
    h.record("stress_candidate_bookkeeping", all(bookkeeping.values()),
             {"checks": bookkeeping, "candidate_status_counts": counts, "candidate_errors": errors,
              "selected_model": selected})
    validation_dir = h.output / "stress_validation"
    validation_exit = h.cli("stress_validate_command", ["validate", "--run-dir", run, "--output-dir", validation_dir])
    result_path = validation_dir / "validation_report.json"
    validation_result = json.loads(result_path.read_text()) if result_path.is_file() else {"status": "MISSING"}
    artifact_integrity = validation_exit == 0 and validation_result.get("status") == "pass" and validation_result.get("failures") == 0
    h.record("stress_artifact_integrity", artifact_integrity, validation_result)
    detail = {"command_exit": command_exit, "candidate_status_counts": counts,
              "candidate_errors": errors, "validation": validation_result,
              "interpretation": "No required cluster count, noise count, or scientific score was imposed"}
    if command_exit != 0 or not all(bookkeeping.values()) or not artifact_integrity or len(failures):
        h.record("stress_dense_isolated_tied", False, detail)
    elif len(invalid):
        detail["reason"] = "Native candidate validity reports invalid topology; artifacts can be intact but this is not a successful stress fit"
        h.record("stress_dense_isolated_tied", False, detail, "INCOMPLETE")
    else:
        h.record("stress_dense_isolated_tied", True, detail)


def failures(h):
    bad = h.input / "failure_fixtures"
    def fail(name, arguments, words):
        return h.cli(name, arguments, expected_failure=True, diagnostic=words)
    for name, words in [("non_numeric", ["numeric", "missing"]), ("nan", ["numeric", "missing"]),
                        ("positive_inf", ["infinity", "finite", "large"]), ("negative_inf", ["infinity", "finite", "large"]),
                        ("header_only", ["sample", "empty", "shape", "minimum"]), ("zero_byte", ["empty", "columns"]),
                        ("metadata_only", ["columns"]), ("too_small", ["small", "sample", "neighbor", "k must"]),
                        ("duplicate_headers", ["duplicate", "unique", "identifier"])]:
        fail("bad_" + name, ["run", "--search-mode", "fixed", "--config", h.input / "synthetic.yaml",
                            "--input", bad / (name + ".tsv"), "--output-dir", h.output / ("bad_" + name)], words)
    for name in ["duplicate_labels", "missing_label"]:
        fail(name, ["compare", "--left", bad / (name + ".tsv"), "--right", bad / "valid_labels.tsv",
                    "--output-dir", h.output / name], ["duplicate", "missing", "column"])
    fail("wrong_orientation", ["explain", "--legacy-table", bad / "orientation_labels.tsv", "--input", h.input / "synthetic.tsv",
          "--matrix-orientation", "vectors_by_variants", "--vector-id-source", "column:CHR", "--drop-first-n-cols", "4",
          "--outdir", h.output / "wrong_orientation"], ["duplicate", "orientation", "matching", "identifier"])
    invalids = [("min_dist", ["--umap-min-dist", "2", "--umap-spread", "1"], ["min_dist"]),
                ("max_size", ["--hdbscan-min-cluster-size", "5", "--hdbscan-max-cluster-size", "4"], ["max_cluster_size"]),
                ("method", ["--hdbscan-cluster-selection-method", "ward"], ["eom", "leaf"]),
                ("fixed_list", ["--hdbscan-min-samples", "2,3"], ["fixed"])]
    for name, options, words in invalids:
        fail("config_" + name, ["inspect-config", "--search-mode", "fixed", "--config", h.input / "synthetic.yaml", *options], words)
    source = Path(h.args.left or (h.input / "c1/run"))
    if source.is_dir():
        tampered = h.output / "tampered_run"
        shutil.copytree(source, tampered)
        # Remap only path metadata in this disposable test copy, then corrupt a
        # labels file. Original input/run evidence stays read-only and untouched.
        manifest_path = tampered / "run_manifest.json"
        manifest = json.loads(manifest_path.read_text())
        for record in manifest.get("artifacts", {}).values():
            if isinstance(record, dict):
                original = Path(record["path"])
                suffix = str(original).split("/run/", 1)[-1]
                record["path"] = str(tampered / suffix)
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        target = next((tampered / "models/top_model_artifacts").glob("*/labels.tsv"))
        with target.open("a") as stream:
            stream.write("\n")
        fail("tampered_checksum", ["validate", "--run-dir", tampered, "--output-dir", h.output / "tampered_validation"], ["fail"])
        report = h.output / "tampered_validation/validation_checks.tsv"
        h.record("tamper_is_hash_mismatch", report.is_file() and "hash mismatch" in report.read_text())
    else:
        h.record("tampered_checksum", False, "No successful run available", "INCOMPLETE")


MODES = {"prepare": prepare, "checks": checks, "fit": fit, "compare": compare,
         "postprocess": postprocess, "failures": failures}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=MODES)
    parser.add_argument("--input", default="/data/input")
    parser.add_argument("--output", default="/data/output")
    parser.add_argument("--left")
    parser.add_argument("--right")
    parser.add_argument("--comparison-class", choices=["same_image", "compatibility_exploratory"], default="same_image")
    parser.add_argument("--command-timeout", type=int, default=1800)
    args = parser.parse_args()
    if args.mode == "compare" and (not args.left or not args.right):
        parser.error("compare requires --left and --right")
    h = Harness(args)
    try:
        MODES[args.mode](h)
    except Exception as error:
        (h.output / "harness_exception.log").write_text(traceback.format_exc())
        h.record("harness_exception", False, {"type": type(error).__name__, "message": str(error)})
    return h.finish()


if __name__ == "__main__":
    raise SystemExit(main())
