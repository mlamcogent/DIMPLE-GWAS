#!/usr/bin/env python3
"""Run the full 70,000-sample MNIST comparison without label-guided tuning."""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from sklearn.datasets import fetch_openml
from sklearn.metrics import (
    adjusted_rand_score,
    completeness_score,
    homogeneity_score,
    normalized_mutual_info_score,
    v_measure_score,
)

from dimple_gwas.hdbscan_runner import fit_hdbscan
from dimple_gwas.io import atomic_json_dump, json_safe
from dimple_gwas.metrics import evaluate_candidate
from dimple_gwas.provenance import base_manifest, sha256_file
from dimple_gwas.scoring import legacy_dimple_score
from dimple_gwas.search_space import stable_identifier
from dimple_gwas.umap_runner import run_repeated_umap


HDB_KEYS = (
    "min_cluster_size", "min_samples", "cluster_selection_epsilon",
    "cluster_selection_persistence", "cluster_selection_method", "alpha",
    "allow_single_cluster", "max_cluster_size", "metric",
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(Path(__file__).with_name("benchmark_config.yaml")))
    parser.add_argument("--output-dir", default=str(Path(__file__).with_name("outputs")))
    parser.add_argument("--data-home", default=str(Path(__file__).with_name("data")))
    return parser.parse_args()


def weighted_purity(targets, labels):
    labels = np.asarray(labels)
    targets = np.asarray(targets)
    clustered = labels != -1
    matches = 0
    for cluster in np.unique(labels[clustered]):
        counts = np.bincount(targets[labels == cluster], minlength=10)
        matches += int(counts.max())
    count = int(clustered.sum())
    return matches, count, matches / count if count else float("nan")


def posthoc_metrics(targets, labels):
    matches, clustered, purity = weighted_purity(targets, labels)
    labels = np.asarray(labels)
    return {
        "clustered_samples": clustered,
        "majority_digit_matches": matches,
        "weighted_purity": purity,
        "adjusted_rand_index": float(adjusted_rand_score(targets, labels)),
        "normalized_mutual_information": float(normalized_mutual_info_score(targets, labels)),
        "homogeneity": float(homogeneity_score(targets, labels)),
        "completeness": float(completeness_score(targets, labels)),
        "v_measure": float(v_measure_score(targets, labels)),
    }


def fit_unsupervised(name, family_name, embedding, hdb_params, execution, ordinal):
    started = time.perf_counter()
    model_id = stable_identifier("mnist", {"umap_family": family_name, "hdbscan": hdb_params})
    try:
        fitted = fit_hdbscan(embedding, hdb_params, core_dist_n_jobs=int(execution["n_jobs"]))
        metrics = evaluate_candidate(
            embedding,
            fitted["labels"],
            fitted["clusterer"],
            silhouette_metric=hdb_params["metric"],
            fit_include_noise=bool(execution["fit_include_noise"]),
            compute_dbcv=False,
            max_samples_silhouette=int(execution["silhouette_sample_size"]),
            silhouette_seed=int(execution["silhouette_seed"]),
        )
        row = {
            "candidate_ordinal": ordinal,
            "model_id": model_id,
            "configuration": name,
            "umap_family": family_name,
            "status": "success" if metrics["number_of_clusters"] >= 2 else "invalid_topology",
            "error_message": "",
            "runtime_seconds": time.perf_counter() - started,
            **{f"hdbscan_{key}": value for key, value in hdb_params.items()},
            **metrics,
        }
        return row, fitted["labels"]
    except Exception as exc:
        return {
            "candidate_ordinal": ordinal,
            "model_id": model_id,
            "configuration": name,
            "umap_family": family_name,
            "status": "failed",
            "error_message": f"{type(exc).__name__}: {exc}",
            "runtime_seconds": time.perf_counter() - started,
            **{f"hdbscan_{key}": value for key, value in hdb_params.items()},
        }, None


def expanded_parameters(config):
    keys = ("umap_family",) + HDB_KEYS
    for values in itertools.product(*(config[key] for key in keys)):
        mapping = dict(zip(keys, values))
        family = mapping.pop("umap_family")
        yield family, mapping


def markdown_table(frame, columns):
    header = "| " + " | ".join(columns) + " |"
    divider = "|" + "|".join("---" for _ in columns) + "|"
    rows = [header, divider]
    for _, row in frame.iterrows():
        values = []
        for column in columns:
            value = row.get(column)
            if pd.isna(value):
                values.append("NA")
            elif isinstance(value, float):
                values.append(f"{value:.4f}")
            else:
                values.append(str(value))
        rows.append("| " + " | ".join(values) + " |")
    return "\n".join(rows)


def main():
    args = parse_args()
    config_path = Path(args.config)
    output = Path(args.output_dir)
    data_home = Path(args.data_home)
    output.mkdir(parents=True, exist_ok=True)
    data_home.mkdir(parents=True, exist_ok=True)
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    execution = config["execution"]
    started = time.perf_counter()

    # The target array is returned by OpenML but is deliberately not passed to any
    # embedding, clustering, grid construction, scoring, or selection function.
    X, target_strings = fetch_openml(
        config["dataset"]["openml_name"],
        version=config["dataset"]["version"],
        data_home=data_home,
        return_X_y=True,
        as_frame=False,
        parser="auto",
    )
    X = np.asarray(X, dtype=np.float32)
    if X.shape[0] != int(config["dataset"]["expected_samples"]):
        raise RuntimeError(f"Expected 70,000 samples; received {X.shape[0]}")
    if config["dataset"].get("scale_pixels_to_unit_interval", True):
        X /= 255.0

    embeddings = {}
    visualizations = {}
    embedding_runtimes = {}
    for family_name, parameters in config["umap_families"].items():
        print(f"Fitting UMAP family {family_name}", flush=True)
        fitted = run_repeated_umap(
            X,
            parameters,
            repeats=int(execution["umap_repeats"]),
            n_jobs=int(execution["n_jobs"]),
            legacy_sequence=False,
        )
        embeddings[family_name] = fitted["embedding"]
        visualizations[family_name] = fitted["visualization_embedding"]
        embedding_runtimes[family_name] = fitted["runtime_seconds"]

    named_rows = []
    named_labels = {}
    ordinal = 0
    for name, definition in config["named_configurations"].items():
        ordinal += 1
        definition = dict(definition)
        family = definition.pop("umap_family")
        print(f"Fitting named configuration {name}", flush=True)
        row, labels = fit_unsupervised(name, family, embeddings[family], definition, execution, ordinal)
        row["umap_runtime_seconds"] = embedding_runtimes[family]
        named_rows.append(row)
        if labels is not None:
            named_labels[name] = labels

    expanded_rows = []
    expanded_labels = {}
    for family, parameters in expanded_parameters(config["expanded_search"]):
        ordinal += 1
        name = f"expanded_{ordinal}"
        row, labels = fit_unsupervised(name, family, embeddings[family], parameters, execution, ordinal)
        row["umap_runtime_seconds"] = embedding_runtimes[family]
        expanded_rows.append(row)
        if labels is not None:
            expanded_labels[row["model_id"]] = labels
    expanded = pd.DataFrame(expanded_rows)
    expanded_scored, scoring_manifest = legacy_dimple_score(
        expanded,
        fit_include_noise=bool(execution["fit_include_noise"]),
    )
    expanded_scored = expanded_scored.sort_values(
        ["score", "model_id"], ascending=[False, True], na_position="last"
    )
    expanded_scored.insert(0, "rank", range(1, len(expanded_scored) + 1))
    expanded_scored.to_csv(output / "expanded_search_models.tsv", sep="\t", index=False)
    selected = expanded_scored.loc[expanded_scored["score"].notna()].iloc[0]
    selected_labels = expanded_labels[selected["model_id"]]

    # Label-based metrics begin only after the unsupervised winner is fixed.
    targets = np.asarray(target_strings, dtype=int)
    result_rows = []
    for row in named_rows:
        labels = named_labels.get(row["configuration"])
        if labels is not None:
            row.update(posthoc_metrics(targets, labels))
            np.save(output / f"{row['configuration']}_labels.npy", labels)
        result_rows.append(row)
    selected_row = selected.to_dict()
    selected_row["configuration"] = "expanded_search_selected_by_legacy_dimple"
    selected_row.update(posthoc_metrics(targets, selected_labels))
    np.save(output / "expanded_search_selected_labels.npy", selected_labels)
    result_rows.append(selected_row)
    results = pd.DataFrame(result_rows)
    results.to_csv(output / "benchmark_results.tsv", sep="\t", index=False)

    reported = pd.DataFrame([{
        "configuration": "Jibin reported result (historical; not rerun row)",
        "number_of_clusters": 140,
        "number_of_noise_points": 51676,
        "noise_fraction": 51676 / 70000,
        "clustered_samples": 18324,
        "majority_digit_matches": 18010,
        "weighted_purity": 18010 / 18324,
        "adjusted_rand_index": np.nan,
        "normalized_mutual_information": np.nan,
        "homogeneity": np.nan,
        "completeness": np.nan,
        "v_measure": np.nan,
        "largest_cluster_size": np.nan,
        "runtime_seconds": np.nan,
    }])
    display = pd.concat([reported, results], ignore_index=True, sort=False)
    columns = [
        "configuration", "number_of_clusters", "number_of_noise_points",
        "noise_fraction", "weighted_purity", "adjusted_rand_index",
        "normalized_mutual_information", "homogeneity", "completeness",
        "v_measure", "largest_cluster_size", "runtime_seconds",
    ]
    report = f"""# MNIST Benchmark Report

Date: 2026-07-22

This benchmark uses all 70,000 `mnist_784` samples. Digit labels were withheld from UMAP, HDBSCAN, the expanded grid, the legacy fit score, and winner selection. Labels were converted to integers only after the expanded-search winner was fixed, then used for the post-hoc metrics below.

The historical result supplied in the Freeze 2 macro (140 clusters, 51,676 noise samples, and 98.29% weighted purity among 18,324 clustered samples) is retained as a reported comparison row. Its exact original parameter manifest was not available. The `reported_pqtl_inspired` rerun therefore uses the auditable reference-branch defaults: EOM, `min_samples=3`, `min_cluster_size=10`, and restrictive `max_cluster_size=300` on the primary dev-style UMAP family. It is a representative rerun, not a claim of exact reconstruction.

## Results

{markdown_table(display, columns)}

Weighted purity is calculated only among non-noise samples. ARI, NMI, homogeneity, completeness, and V-measure are calculated across all 70,000 samples with noise retained as label `-1`. Silhouette used for unsupervised scoring is a fixed-seed sample of {execution['silhouette_sample_size']:,} eligible points per candidate; the sample size and sampling flag are recorded in the expanded model table.

## Interpretation

Local purity asks whether each retained cluster is internally dominated by one digit. Global class recovery asks whether the complete ten-class partition is recovered, which is better reflected by ARI/NMI/V-measure. Fragmentation appears as many more than ten clusters. Noise rejection appears as the excluded fraction. Consequently, high weighted purity can coexist with weak global recovery, severe fragmentation, and high noise, as the historical result demonstrates.

The expanded-search winner is selected only by the declared `legacy_dimple` objective. It is not automatically the unique or biologically correct topology, and the benchmark labels do not alter its rank.
"""
    (output / "MNIST_BENCHMARK_REPORT.md").write_text(report, encoding="utf-8")
    manifest = base_manifest(sys.argv)
    manifest.update({
        "config_path": str(config_path.resolve()),
        "config_sha256": sha256_file(config_path),
        "dataset": "OpenML mnist_784 version 1",
        "sample_count": int(X.shape[0]),
        "feature_count": int(X.shape[1]),
        "labels_used_for_selection": False,
        "expanded_candidates": int(len(expanded_scored)),
        "selected_model": selected["model_id"],
        "scoring": scoring_manifest,
        "umap_runtimes": embedding_runtimes,
        "runtime_seconds": time.perf_counter() - started,
    })
    atomic_json_dump(json_safe(manifest), output / "benchmark_manifest.json")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

