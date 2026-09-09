#!/usr/bin/env python3
"""Generate a deterministic GWAS-shaped matrix for smoke and regression tests."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--annotation-output")
    args = parser.parse_args()
    rng = np.random.default_rng(20260722)
    variants = 80
    x = np.linspace(0, 4 * np.pi, variants)
    templates = [
        np.sin(x),
        np.cos(x),
        np.where(np.arange(variants) < variants // 2, -1.0, 1.0),
    ]
    data = {
        "CHR": np.ones(variants, dtype=int),
        "BP": np.arange(variants),
        "A1": ["A"] * variants,
        "A2": ["G"] * variants,
    }
    feature_ids = []
    for group, template in enumerate(templates):
        for member in range(8):
            feature = f"trait_g{group}_{member}"
            feature_ids.append(feature)
            data[feature] = template + rng.normal(0, 0.06, variants)
    destination = Path(args.output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(data).to_csv(destination, sep="\t", index=False)
    if args.annotation_output:
        annotation = Path(args.annotation_output)
        annotation.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame({
            "index": feature_ids,
            "feature_group": [feature.split("_")[1] for feature in feature_ids],
        }).to_csv(annotation, index=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

