#!/usr/bin/env python3
"""Compare a one-model dev run with the equivalent Freeze 2 run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev-output", required=True)
    parser.add_argument("--freeze2-output", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    dev_root = Path(args.dev_output)
    freeze_root = Path(args.freeze2_output)
    dev = pd.read_csv(dev_root / "stage02_hdbscan_gridsearch_results.csv").iloc[0]
    freeze = pd.read_csv(freeze_root / "models" / "all_models.tsv", sep="\t").iloc[0]
    dev_labels = pd.read_csv(dev_root / "stage09_umap_vizdata_with_clusters.csv")["label"].to_numpy()
    freeze_labels = pd.read_csv(freeze_root / "stage09_umap_vizdata_with_clusters.csv")["label"].to_numpy()
    payload = {
        "clusters": {"dev": int(dev["Clusters"]), "freeze2": int(freeze["number_of_clusters"])},
        "noise_points": {"dev": int(dev["Noise_points"]), "freeze2": int(freeze["number_of_noise_points"])},
        "silhouette": {"dev": float(dev["Silhouette_avg"]), "freeze2": float(freeze["silhouette"])},
        "silhouette_absolute_difference": abs(float(dev["Silhouette_avg"]) - float(freeze["silhouette"])),
        "labels_exactly_equal": bool(np.array_equal(dev_labels, freeze_labels)),
        "status": "pass" if (
            int(dev["Clusters"]) == int(freeze["number_of_clusters"])
            and int(dev["Noise_points"]) == int(freeze["number_of_noise_points"])
            and abs(float(dev["Silhouette_avg"]) - float(freeze["silhouette"])) < 1e-6
            and np.array_equal(dev_labels, freeze_labels)
        ) else "fail",
    }
    destination = Path(args.report)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
