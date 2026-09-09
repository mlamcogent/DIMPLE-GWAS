#!/usr/bin/env python3
"""Create the redistributable TE2 hand-worked evidence using implemented functions."""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, silhouette_score

from dimple_gwas.preprocessing import prepare_analysis_matrix
from dimple_gwas.scoring import legacy_dimple_score


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "executed_output"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=False)
    raw = pd.DataFrame({
        "chromosome": [1, 1, 1, 2, 2, 2],
        "position": [101, 202, 303, 404, 505, 606],
        "effect": ["A", "C", "G", "T", "A", "C"],
        "other": ["G", "T", "A", "C", "T", "G"],
        "V_A": [1.0, 2.0, 2.0, 4.0, 5.0, 6.0],
        "V_B": [1.2, 2.1, 2.0, 4.2, 5.1, 6.0],
        "V_C": [6.0, 5.0, 5.0, 3.0, 2.0, 1.0],
        "V_D": [5.8, 4.9, 5.1, 2.9, 2.2, 0.8],
    })
    raw_path = ROOT / "toy_variants_by_vectors.tsv"
    raw.to_csv(raw_path, sep="\t", index=False)
    analysis = prepare_analysis_matrix(raw, {"drop_first_n_cols": 4, "zscore_transform": "rint"})
    analysis.to_csv(OUTPUT / "rint_vectors_by_variants.tsv", sep="\t")
    distance_ab = float(np.linalg.norm(analysis.loc["V_A"] - analysis.loc["V_B"]))
    distance_ac = float(np.linalg.norm(analysis.loc["V_A"] - analysis.loc["V_C"]))
    labels = np.array([0, 0, 1, 1])
    silhouette = float(silhouette_score(analysis.to_numpy(), labels, metric="euclidean"))
    candidates = pd.DataFrame({
        "model_id": ["toy_A", "toy_B", "toy_C"],
        "candidate_ordinal": [1, 2, 3],
        "status": ["success", "success", "success"],
        "silhouette": [0.70, 0.50, 0.60],
        "number_of_clusters": [2, 3, 4],
        "number_of_noise_points": [0, 1, 2],
    })
    scored_no_noise, manifest_no_noise = legacy_dimple_score(candidates, fit_include_noise=False)
    scored_with_noise, manifest_with_noise = legacy_dimple_score(candidates, fit_include_noise=True)
    scored_no_noise.to_csv(OUTPUT / "toy_candidates_excluding_noise.tsv", sep="\t", index=False)
    scored_with_noise.to_csv(OUTPUT / "toy_candidates_including_noise.tsv", sep="\t", index=False)
    left = np.array([0, 0, 1, 1, -1])
    permuted = np.array([7, 7, 4, 4, -1])
    changed = np.array([7, 4, 4, 4, -1])
    results = {
        "schema": "dimple-gwas.textbook-hand-toy.v1",
        "software_version": "3.0.0rc1",
        "python": platform.python_version(),
        "input_sha256": digest(raw_path),
        "raw_shape": list(raw.shape),
        "analysis_shape": list(analysis.shape),
        "rint_convention": "average ranks by input analysis column; quantile=(rank-0.5)/nonmissing_count",
        "distance_VA_VB": distance_ab,
        "distance_VA_VC": distance_ac,
        "silhouette_four_vectors_two_clusters": silhouette,
        "legacy_excluding_noise": manifest_no_noise,
        "legacy_including_noise": manifest_with_noise,
        "label_comparison": {
            "numeric_exact_left_vs_permuted": bool(np.array_equal(left, permuted)),
            "ari_left_vs_permuted": float(adjusted_rand_score(left, permuted)),
            "nmi_left_vs_permuted": float(normalized_mutual_info_score(left, permuted)),
            "ari_left_vs_changed": float(adjusted_rand_score(left, changed)),
        },
        "pedagogical_boundary": "No UMAP fit is performed by hand; the lab executes valid preprocessing, diagnostic, scoring, and label-comparison paths.",
    }
    (OUTPUT / "hand_worked_results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
