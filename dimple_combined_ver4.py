#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DIMPLE-GWAS combined pipeline (single-file) ver4
# - Includes CLI + plotting utilities + grid search + optimization
# - Designed for distribution with toy/example data (generic output filenames)
#
# Core Python deps (pip): numpy, pandas, scikit-learn, umap-learn, hdbscan, joblib, plotly, matplotlib
# Optional speedups: pyarrow

import argparse
import sys
import os
import itertools
import numpy as np
import pandas as pd
import logging
import io
import warnings
import gc
from typing import Optional, List

# ---------- Plotting utilities (kept inline for single-file distribution) ----------
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import matplotlib.pyplot as plt

from sklearn.metrics import silhouette_samples, silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import euclidean_distances

import hdbscan
# Additional dependencies from the original notebook
from sklearn.datasets import fetch_openml, make_blobs
from sklearn.decomposition import PCA
import sklearn.cluster as cluster
from mpl_toolkits.mplot3d import Axes3D  # for 3D plotting support

# Prefer the optimized umap.umap_ API; fall back to plain `umap` if needed
try:
    import umap.umap_ as umap
except Exception:
    import umap
from joblib import Parallel, delayed

# =============================
# Stage 0: Paths & CLI
# =============================

def build_arg_parser():
    p = argparse.ArgumentParser(description="DIMPLE-GWAS single-file pipeline (ver4)")
    # Cell 1 defaults (from your notebook)
    p.add_argument("--datainput", default="example_input.tsv", help="Input matrix (.tsv/.csv); not affected by --outdir")
    p.add_argument(
        "--outdir",
        default="outputs",
        help="Output directory for all generated files (plots, tables, logs). Relative output paths are created under this directory."
    )
    p.add_argument("--prelim_umap", default="stage00_umap_preliminary.html")
    p.add_argument("--hdbscan_input", default="stage01_hdbscan_input.csv")
    p.add_argument("--screeinput", default="stage02_hdbscan_gridsearch_results.csv")
    p.add_argument("--optimized_out", default="stage03_optimized_cluster_solutions.csv")
    p.add_argument("--screeplot1", default="stage04_silhouette_vs_clusters.html")
    p.add_argument("--screeplot2", default="stage05_noise_vs_clusters.html")
    p.add_argument("--screeplot3", default="stage06_silhouette_vs_noise.html")
    p.add_argument("--silplot", default="stage07_silhouette_analysis.png")
    p.add_argument("--logfile", default="stage08_cluster_metrics.log")
    p.add_argument("--umapdataframe", default="stage09_umap_vizdata_with_clusters.csv")
    p.add_argument("--clusterplot1", default="stage10_cluster_solutions_3d.html")
    p.add_argument("--clusterplot2", default="stage11_modalities_3d.html")
    p.add_argument("--idp_key", default="IDP_KEY.csv", help="Path to IDP key CSV used to enrich UMAP output")
    p.add_argument("--merged_umap", default="stage09b_umap_vizdata_with_idpkey.csv",
                   help="Path to save merged UMAP+IDP key table")

    # General toggles / params (we'll wire these up as we add cells)
    p.add_argument("--drop_first_n_cols", type=int, default=4, help="Drop first N metadata columns before analysis")
    p.add_argument("--sep", default=None, help="CSV/TSV delimiter override; defaults: .tsv='\t', .csv=','")
    p.add_argument("--n_neighbors", type=int, default=30)
    p.add_argument("--min_dist", type=float, default=0.0)
    p.add_argument("--n_components", type=int, default=3)
    # densMAP: default ON (matches notebook/script behavior); can be disabled explicitly
    p.add_argument("--densmap", dest="densmap", action="store_true", help="Enable densMAP for UMAP")
    p.add_argument("--no-densmap", dest="densmap", action="store_false", help="Disable densMAP for UMAP")
    p.set_defaults(densmap=True)
    p.add_argument("--random_state", type=int, default=42)
    p.add_argument("--log_level", default="INFO",
                   choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                   help="Logging level for console/file output")
    p.add_argument("--n_random_states", type=int, default=1000,
                   help="Number of random states for parallel UMAP (each run adds n_components features). Use a small value for testing; increase for final runs.")
    p.add_argument("--n_jobs", type=int, default=-1,
                   help="Number of parallel jobs for UMAP runs (-1 uses all cores)")

    # Plot controls
    p.add_argument(
        "--no_plots",
        action="store_true",
        help="If set, skip all plot generation (HTML/PNG). Useful for fast runs or headless environments."
    )

    # O(n^2) metrics controls (trustworthiness/continuity)
    p.add_argument(
        "--max_samples_trust",
        type=int,
        default=3000,
        help="Maximum number of samples used for trustworthiness/continuity (O(n^2) memory). If the masked dataset exceeds this, metrics are computed on a random subsample. Set to 0 or negative to disable subsampling."
    )
    p.add_argument(
        "--trust_seed",
        type=int,
        default=42,
        help="Random seed used when subsampling for trustworthiness/continuity."
    )

    # Grid-search cap (runtime safeguard)
    p.add_argument(
        "--grid_max_evals",
        type=int,
        default=5000,
        help="Maximum number of HDBSCAN configurations evaluated in grid search. If the full grid exceeds this, a random subset is evaluated."
    )

    # Strict mode
    p.add_argument(
        "--strict",
        action="store_true",
        help="If set, abort on the first stage failure instead of continuing with best-effort fallbacks."
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Print resolved parameters, paths, and the planned pipeline stages, then exit. "
            "No computation is performed and no outputs are written."
        )
    )

    # Grid search params (accept CSV or range syntax start:stop[:step]; stop is exclusive)
    p.add_argument(
        "--grid_eps",
        default="0:3",
        help="Epsilon values for HDBSCAN cluster_selection_epsilon. "
             "Accepts comma-separated values or range 'start:stop[:step]'. "
             "Examples: '0:3' -> 0,1,2  | '0,0.5,1.0' -> 0.0,0.5,1.0"
    )
    p.add_argument(
        "--grid_min_samples",
        default="2:20",
        help="min_samples values. CSV or range 'start:stop[:step]'. "
             "Example: '2:20' -> 2..20"
    )
    p.add_argument(
        "--grid_min_cluster_size",
        default="5:50",
        help="min_cluster_size values. CSV or range 'start:stop[:step]'. "
             "Example: '5:50' -> 5..50"
    )

    p.add_argument(
        "--override_rank",
        type=int,
        default=None,
        help="If provided, use df_sorted.iloc[override_rank] as the chosen configuration after optimization."
    )
    # Metrics controls
    p.add_argument(
        "--metrics_space",
        choices=["hdbscan", "viz"],
        default="hdbscan",
        help="Feature space to compute cluster metrics on: 'hdbscan' (consolidated UMAP used for clustering) or 'viz' (3D UMAP)."
    )
    p.add_argument(
        "--metrics_include_noise",
        action="store_true",
        help="If set, include noise points (label = -1) when computing cluster indices. Default: exclude noise."
    )
    p.add_argument(
        "--trust_k",
        type=int,
        default=30,
        help="Neighborhood size (k) for trustworthiness/continuity."
    )
    p.add_argument(
        "--metrics_csv",
        default=None,
        help="Optional path to append a one-row CSV of computed fit statistics (if provided)."
    )
    return p

def resolve_sep(path: str, override: Optional[str]):
    if override:
        return override
    if path.lower().endswith(".tsv"):
        return "\t"
    return ","

def ensure_exists(path: str):
    if not os.path.isfile(path):
        print(f"[ERROR] File not found: {path}")
        sys.exit(1)


def ensure_parent_dir(path: str):
    """Create parent directory for a file path if needed."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def apply_outdir(outdir: str, path: str) -> str:
    """Prefix relative paths with outdir; keep absolute paths unchanged."""
    if path is None:
        return path
    if os.path.isabs(path):
        return path
    # Treat any relative path (including those with subdirectories) as under outdir
    return os.path.join(outdir, path)

def setup_console_logger(level: str = "INFO"):
    """Configure a console-only logger (no file output)."""
    logger = logging.getLogger("dimple")
    logger.handlers.clear()
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    ch.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.addHandler(ch)

    logger.propagate = False
    return logger

def setup_logger(log_path: str, level: str = "INFO"):
    """
    Configure a file + console logger and return it.
    """
    ensure_parent_dir(log_path)
    logger = logging.getLogger("dimple")
    # Reset handlers in case of repeated runs
    logger.handlers.clear()
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    # File handler
    fh = logging.FileHandler(log_path)
    fh.setFormatter(fmt)
    fh.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.addHandler(fh)
    # Console handler (stdout)
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    ch.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.addHandler(ch)

    logger.propagate = False
    return logger

def paths_from_args(args):
    # Route all relative output paths under --outdir
    outdir = getattr(args, "outdir", "outputs")

    paths = dict(
        datainput=args.datainput,
        prelim_umap=apply_outdir(outdir, args.prelim_umap),
        hdbscan_input=apply_outdir(outdir, args.hdbscan_input),
        screeinput=apply_outdir(outdir, args.screeinput),
        optimized_out=apply_outdir(outdir, args.optimized_out),
        screeplot1=apply_outdir(outdir, args.screeplot1),
        screeplot2=apply_outdir(outdir, args.screeplot2),
        screeplot3=apply_outdir(outdir, args.screeplot3),
        silplot=apply_outdir(outdir, args.silplot),
        logfile=apply_outdir(outdir, args.logfile),
        umapdataframe=apply_outdir(outdir, args.umapdataframe),
        clusterplot1=apply_outdir(outdir, args.clusterplot1),
        clusterplot2=apply_outdir(outdir, args.clusterplot2),
        idp_key=args.idp_key,
        merged_umap=apply_outdir(outdir, args.merged_umap),
    )

    # Optional outputs should also respect outdir if provided
    if getattr(args, "metrics_csv", None):
        args.metrics_csv = apply_outdir(outdir, args.metrics_csv)

    return paths

def _parse_seq_ints(spec: Optional[str]):
    """
    Parse a sequence spec into a list of ints.
    Supports:
      - CSV: "2,5,10"
      - Range: "start:stop[:step]" or "start-stop[:step]" (stop exclusive)
    """
    if not spec:
        return None
    out: List[int] = []
    for tok in spec.split(","):
        tok = tok.strip()
        if not tok:
            continue
        if ":" in tok:
            parts = [p.strip() for p in tok.split(":")]
            if len(parts) not in (2, 3):
                raise ValueError(f"Bad int range token '{tok}'")
            start = int(float(parts[0]))
            stop = int(float(parts[1]))
            step = int(float(parts[2])) if len(parts) == 3 else 1
            out.extend(list(range(start, stop, step)))
        else:
            out.append(int(tok))
    # Basic bounds checking for HDBSCAN integer hyperparameters
    if any(v < 1 for v in out):
        raise ValueError(f"Invalid integer sequence (values must be >= 1): {out}")
    return out

def _parse_seq_floats(spec: Optional[str]):
    """
    Parse a sequence spec into a list of floats.
    Supports:
      - CSV: "0,0.5,1.0"
      - Range: "start:stop[:step]" or "start-stop[:step]" (stop exclusive)
    """
    if not spec:
        return None
    out: List[float] = []
    for tok in spec.split(","):
        tok = tok.strip()
        if not tok:
            continue
        if ":" in tok:
            parts = [p.strip() for p in tok.split(":")]
            if len(parts) not in (2, 3):
                raise ValueError(f"Bad float range token '{tok}'")
            start = float(parts[0])
            stop = float(parts[1])
            step = float(parts[2]) if len(parts) == 3 else 1.0
            vals = list(np.arange(start, stop, step))
            out.extend([float(v) for v in vals])
        else:
            out.append(float(tok))
    # Basic bounds checking for epsilon
    if any(v < 0 for v in out):
        raise ValueError(f"Invalid float sequence (values must be >= 0): {out}")
    return out

def dependency_banner(logger):
    """
    Notebook parity: prints the dependency banner. We log it instead.
    """
    logger.info("General Dependencies for IDP Neuroimaging Clustering Pipeline Loaded")


def trustworthiness(X, X_embedded, n_neighbors: int):
    """
    Compute Trustworthiness of the embedding with respect to the original space.
    Mirrors the notebook implementation:
      - Builds NN in original and embedded spaces
      - Ranks neighbors and penalizes intrusions
    NOTE: This memory-inefficient implementation constructs n_samples x n_samples rank matrices,
    matching the original notebook semantics. For very large n, consider a batched/approx version.
    """
    n_samples = X.shape[0]

    # Guard: this implementation builds O(n^2) rank matrices.
    # For larger n, return NaN and warn rather than hard-failing.
    if n_samples > 5000:
        warnings.warn(
            f"trustworthiness/continuity O(n^2) implementation skipped for n_samples={n_samples} (>5000).",
            RuntimeWarning,
        )
        return float("nan")

    # Nearest neighbors in original space
    nn_orig = NearestNeighbors(n_neighbors=n_neighbors + 1).fit(X)
    _, ind_orig = nn_orig.kneighbors(X)

    # Nearest neighbors in embedded space
    nn_embedded = NearestNeighbors(n_neighbors=n_neighbors + 1).fit(X_embedded)
    _, ind_embedded = nn_embedded.kneighbors(X_embedded)

    # Remove self neighbor
    ind_orig = ind_orig[:, 1:]
    ind_embedded = ind_embedded[:, 1:]

    # Rank matrices
    rank_orig = np.zeros((n_samples, n_samples))
    rank_embedded = np.zeros((n_samples, n_samples))

    for i in range(n_samples):
        rank_orig[i, ind_orig[i]] = np.arange(1, n_neighbors + 1)
        rank_embedded[i, ind_embedded[i]] = np.arange(1, n_neighbors + 1)

    # Trustworthiness
    U = np.zeros(n_samples)
    for i in range(n_samples):
        U[i] = np.sum((rank_orig[i, ind_embedded[i]] > n_neighbors) *
                      (rank_orig[i, ind_embedded[i]] - n_neighbors))

    trust = 1 - 2 / (n_samples * n_neighbors * (2 * n_samples - 3 * n_neighbors - 1)) * np.sum(U)
    return float(trust)


def continuity(X, X_embedded, n_neighbors: int):
    """
    Compute Continuity of the embedding with respect to the original space.
    Mirrors the notebook implementation:
      - Builds NN in original and embedded spaces
      - Ranks neighbors and penalizes extrusions
    NOTE: This memory-inefficient implementation constructs n_samples x n_samples rank matrices,
    matching the original notebook semantics. For very large n, consider a batched/approx version.
    """
    n_samples = X.shape[0]

    # Nearest neighbors in original space
    nn_orig = NearestNeighbors(n_neighbors=n_neighbors + 1).fit(X)
    _, ind_orig = nn_orig.kneighbors(X)

    # Nearest neighbors in embedded space
    nn_embedded = NearestNeighbors(n_neighbors=n_neighbors + 1).fit(X_embedded)
    _, ind_embedded = nn_embedded.kneighbors(X_embedded)

    # Remove self neighbor
    ind_orig = ind_orig[:, 1:]
    ind_embedded = ind_embedded[:, 1:]

    # Rank matrices
    rank_orig = np.zeros((n_samples, n_samples))
    rank_embedded = np.zeros((n_samples, n_samples))

    for i in range(n_samples):
        rank_orig[i, ind_orig[i]] = np.arange(1, n_neighbors + 1)
        rank_embedded[i, ind_embedded[i]] = np.arange(1, n_neighbors + 1)

    # Continuity
    V = np.zeros(n_samples)
    for i in range(n_samples):
        V[i] = np.sum((rank_embedded[i, ind_orig[i]] > n_neighbors) *
                      (rank_embedded[i, ind_orig[i]] - n_neighbors))

    cont = 1 - 2 / (n_samples * n_neighbors * (2 * n_samples - 3 * n_neighbors - 1)) * np.sum(V)
    return float(cont)


# =============================
# Dunn Index implementation
# =============================
def dunn_index(features: np.ndarray, labels: np.ndarray) -> float:
    """
    Dunn Index:
      ratio of the smallest distance between observations in different clusters
      to the largest intra-cluster distance.
    Higher is better. Returns NaN if undefined (e.g., <2 clusters or zero intra-cluster spread).
    """
    labels = np.asarray(labels)
    unique = [c for c in np.unique(labels) if c != -1]  # ignore noise by convention
    if len(unique) < 2:
        return float("nan")

    # Pairwise distances
    D = euclidean_distances(features)

    min_inter = np.inf
    max_intra = 0.0

    for i, ci in enumerate(unique):
        idx_i = np.where(labels == ci)[0]
        # Intra-cluster (max)
        if idx_i.size > 1:
            intra_i = D[np.ix_(idx_i, idx_i)].max()
            if intra_i > max_intra:
                max_intra = intra_i

        # Inter-cluster (min)
        for cj in unique[i + 1:]:
            idx_j = np.where(labels == cj)[0]
            if idx_i.size > 0 and idx_j.size > 0:
                inter_ij = D[np.ix_(idx_i, idx_j)].min()
                if inter_ij < min_inter:
                    min_inter = inter_ij

    if max_intra <= 0 or not np.isfinite(min_inter):
        return float("nan")
    return float(min_inter / max_intra)

# =============================
# Entry
# =============================

def main():
    parser = build_arg_parser()
    args = parser.parse_args()
    paths = paths_from_args(args)

    # Ensure output directory exists and all parent directories for known outputs are created
    # (skip filesystem writes in --dry-run mode)
    if not bool(getattr(args, "dry_run", False)):
        os.makedirs(getattr(args, "outdir", "outputs"), exist_ok=True)
        for k, v in paths.items():
            if k in ("datainput", "idp_key"):
                continue
            if isinstance(v, str) and v:
                ensure_parent_dir(v)
        if getattr(args, "metrics_csv", None):
            ensure_parent_dir(args.metrics_csv)

    dry_run = bool(getattr(args, "dry_run", False))

    # In dry-run mode, avoid writing any outputs (including log files).
    if dry_run:
        logger = setup_console_logger(args.log_level)
    else:
        logger = setup_logger(paths["logfile"], args.log_level)

    dependency_banner(logger)

    if dry_run:
        logger.info("[DRY-RUN] DIMPLE-GWAS pipeline will not execute. Showing resolved configuration only.")
        logger.info("Resolved input:")
        logger.info("  datainput: %s", paths["datainput"])
        logger.info("Resolved outputs (under --outdir unless absolute):")
        for k, v in paths.items():
            if k == "datainput":
                continue
            logger.info("  %s: %s", k, v)

        logger.info("Key parameters:")
        logger.info("  drop_first_n_cols: %d", int(args.drop_first_n_cols))
        logger.info("  sep override: %s", str(args.sep))
        logger.info("  n_neighbors: %d", int(args.n_neighbors))
        logger.info("  min_dist: %s", str(args.min_dist))
        logger.info("  n_components: %d", int(args.n_components))
        logger.info("  densmap: %s", str(args.densmap))
        logger.info("  random_state: %d", int(args.random_state))
        logger.info("  n_random_states: %d", int(args.n_random_states))
        logger.info("  n_jobs: %d", int(args.n_jobs))
        logger.info("  no_plots: %s", str(bool(args.no_plots)))
        logger.info("  max_samples_trust: %d", int(args.max_samples_trust))
        logger.info("  trust_k: %d", int(args.trust_k))
        logger.info("  grid_max_evals: %d", int(args.grid_max_evals))
        logger.info("  grid_eps: %s", str(args.grid_eps))
        logger.info("  grid_min_samples: %s", str(args.grid_min_samples))
        logger.info("  grid_min_cluster_size: %s", str(args.grid_min_cluster_size))

        # Light validation without writing anything
        if not os.path.isfile(paths["datainput"]):
            logger.warning("[DRY-RUN] Input file does not exist: %s", paths["datainput"])
        else:
            logger.info("[DRY-RUN] Input file exists.")

        logger.info("Planned stages:")
        logger.info("  Stage 00: UMAP (viz) + preliminary HTML")
        logger.info("  Stage 01: Parallel UMAP ensemble -> HDBSCAN input CSV")
        logger.info("  Stage 02: HDBSCAN grid search -> scree CSV")
        logger.info("  Stage 04-06: Scree HTML plots")
        logger.info("  Stage 03: Optimization -> chosen config table")
        logger.info("  Stage 07: Silhouette analysis PNG")
        logger.info("  Stage 08: Metrics/logging")
        logger.info("  Stage 09: UMAP viz dataframe + labels CSV")
        logger.info("  Stage 10: Cluster solutions plot HTML")
        logger.info("  Stage 09b: Merge IDP key with UMAP table CSV (if IDP key provided)")
        return 0

    strict = bool(getattr(args, "strict", False))
    no_plots = bool(getattr(args, "no_plots", False))

    def _handle_stage_exception(stage: str, e: Exception):
        """Centralized exception handling; raises in strict mode."""
        logger.exception("[%s] failed: %s", stage, e)
        if strict:
            raise

    # Echo notebook Cell 1 effect:
    logger.info("Defining input and output objectives for pipeline")
    for k, v in paths.items():
        logger.info("  %s: %s", k, v)

    # =============================
    # Cell 2: Read in data
    # - Mirrors notebook cell to load input matrix, drop first 4 metadata columns, and transpose.
    # =============================
    logger.info("reading in input data")
    ensure_exists(paths["datainput"])
    sep = resolve_sep(paths["datainput"], args.sep)

    # Load the input dataframe using pyarrow when available, fall back to pandas engine if needed.
    try:
        df = pd.read_csv(paths["datainput"], engine="pyarrow", sep=sep)
    except Exception as e:
        logger.warning("Falling back to pandas CSV reader (pyarrow failed: %s)", e)
        df = pd.read_csv(paths["datainput"], sep=sep)

    # Drop the first N metadata columns (default 4) then transpose for analysis matrix X
    # Drop the first N metadata columns (default 4), coerce to numeric, then transpose for analysis matrix X
    df2 = df.iloc[:, args.drop_first_n_cols:].copy()
    df2 = df2.apply(pd.to_numeric, errors="coerce")
    if df2.isna().any().any():
        na_cells = int(df2.isna().sum().sum())
        raise ValueError(
            f"Non-numeric values or missingness detected after coercion (NA cells={na_cells}). "
            "Please ensure the analysis matrix is fully numeric and contains no missing values."
        )
    X = df2.T

    # Basic diagnostics to mirror notebook checks
    logger.info("Input df shape: %s", df.shape)
    logger.info("After dropping first %d cols: %s", args.drop_first_n_cols, df2.shape)
    logger.info("Analysis matrix X shape (transposed): %s", X.shape)

    # =============================
    # Cell 2b: Check dataframe (log to file)
    # Mirrors notebook: print("checking dataframe...\n", df)
    # For safety, log info + head instead of entire massive frames.
    # =============================
    logger.info("checking dataframe...")
    # Log df.info()
    info_buf = io.StringIO()
    df.info(buf=info_buf)
    logger.info("df.info():\n%s", info_buf.getvalue().rstrip())
    # Log df.head() preview
    try:
        logger.info("df.head(5):\n%s", df.head(5).to_string())
    except Exception as _e:
        logger.debug("Failed to render df.head() to string: %s", _e)
    # =============================
    # Cell 3: Generate UMAP for visualization + preliminary 3D Plotly scatter
    # Mirrors notebook: densmap=args.densmap, n_neighbors=30, min_dist=0.0, n_components=3, random_state=42
    # We keep these parameters sourced from CLI (defaults match the notebook), and force densmap=True for viz to match the cell.
    # =============================
    logger.info("generating UMAP dimensions for visualization...")
    try:
        clusterable_embedding_viz = umap.UMAP(
            densmap=args.densmap,  # densMAP toggle from CLI (default True)
            n_neighbors=args.n_neighbors,
            min_dist=args.min_dist,
            n_components=args.n_components,
            random_state=args.random_state,
        ).fit_transform(X.values if hasattr(X, "values") else X)

        # Build a DataFrame for plotting convenience
        umap_cols = [f"UMAP_{i+1}" for i in range(clusterable_embedding_viz.shape[1])]
        df_umap = pd.DataFrame(clusterable_embedding_viz, columns=umap_cols)

        if no_plots:
            logger.info("--no_plots set; skipping preliminary UMAP plot export.")
        else:
            # Produce a preliminary interactive plot
            if clusterable_embedding_viz.shape[1] >= 3:
                fig = go.Figure()
                fig.add_trace(go.Scatter3d(
                    x=df_umap[umap_cols[0]],
                    y=df_umap[umap_cols[1]],
                    z=df_umap[umap_cols[2]],
                    mode="markers",
                    marker=dict(size=5, color="blue", opacity=0.8),
                    name="UMAP Points"
                ))
                fig.update_layout(
                    title="3D UMAP Embedding",
                    scene=dict(
                        xaxis_title=umap_cols[0],
                        yaxis_title=umap_cols[1],
                        zaxis_title=umap_cols[2]
                    ),
                    legend_title="UMAP"
                )
            else:
                # Fallback to 2D scatter if fewer than 3 components are requested
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df_umap[umap_cols[0]],
                    y=df_umap[umap_cols[1]] if len(umap_cols) > 1 else pd.Series([0]*len(df_umap)),
                    mode="markers",
                    marker=dict(size=5, color="blue", opacity=0.8),
                    name="UMAP Points"
                ))
                fig.update_layout(
                    title="2D UMAP Embedding",
                    xaxis_title=umap_cols[0],
                    yaxis_title=umap_cols[1] if len(umap_cols) > 1 else "UMAP_placeholder"
                )

            ensure_parent_dir(paths["prelim_umap"])
            pio.write_html(fig, file=paths["prelim_umap"], auto_open=False)
            logger.info("write preliminary umap plot to %s", paths["prelim_umap"])
        logger.info("UMAP viz shape: %s", clusterable_embedding_viz.shape)

    except Exception as e:
        _handle_stage_exception("Cell 3 viz UMAP", e)

    # =============================
    # Cell 4: Parallelized UMAP implementation for HDBSCAN input
    # Runs UMAP over multiple random states in parallel, horizontally concatenates all embeddings,
    # and writes to the Stage_01 HDBSCAN input CSV.
    # Defaults: n_components=args.n_components, n_neighbors=args.n_neighbors, min_dist=args.min_dist,
    # densmap=True (as per notebook), random states 1..args.n_random_states, n_jobs=args.n_jobs
    # =============================
    try:
        logger.info("initiating parallelized UMAP with %d random states....", args.n_random_states)

        def _run_umap_state(random_state: int):
            # Small helper for joblib parallel mapping
            reducer = umap.UMAP(
                densmap=args.densmap,
                n_neighbors=args.n_neighbors,
                min_dist=args.min_dist,
                n_components=args.n_components,
                random_state=random_state
            )
            emb = reducer.fit_transform(X.values if hasattr(X, "values") else X)
            return emb.astype(np.float32, copy=False)

        if args.n_random_states < 1:
            raise ValueError("--n_random_states must be >= 1")

        # Execute in parallel
        results = Parallel(n_jobs=args.n_jobs)(
            delayed(_run_umap_state)(rs) for rs in range(1, args.n_random_states + 1)
        )

        # Pre-allocate and fill to avoid large intermediate copies from np.hstack
        n_samples = results[0].shape[0]
        n_comp = results[0].shape[1]
        consolidated_umap_array = np.empty((n_samples, n_comp * len(results)), dtype=np.float32)
        for i, emb in enumerate(results):
            consolidated_umap_array[:, i * n_comp:(i + 1) * n_comp] = emb.astype(np.float32, copy=False)

        # Encourage GC of the list of arrays before proceeding
        del results
        gc.collect()

        # Build column names UMAP_1..UMAP_k
        total_cols = consolidated_umap_array.shape[1]
        umap_cols_all = [f"UMAP_{i+1}" for i in range(total_cols)]

        umap_df = pd.DataFrame(consolidated_umap_array, columns=umap_cols_all)
        ensure_parent_dir(paths["hdbscan_input"])
        umap_df.to_csv(paths["hdbscan_input"], index=False)
        logger.info("UMAP embeddings saved to hdbscan input file: %s (shape=%s)", paths["hdbscan_input"], umap_df.shape)
    except Exception as e:
        _handle_stage_exception("Cell 4 parallel UMAP", e)

    # =============================
    # Cell 5: Parallelized grid search for best fitting cluster
    # Reads Stage_01 HDBSCAN input, explores epsilon/min_samples/min_cluster_size space,
    # and writes the full set of suitable configurations to Stage_02 scree CSV.
    # =============================
    try:
        logger.info("parallelized grid search for best fitting cluster....")
        # Load HDBSCAN input produced above
        try:
            clusterable_embedding_df = pd.read_csv(paths["hdbscan_input"], engine="pyarrow")
        except Exception as e_read:
            logger.warning("Falling back to pandas CSV reader for hdbscan_input (pyarrow failed: %s)", e_read)
            clusterable_embedding_df = pd.read_csv(paths["hdbscan_input"])
        clusterable_embedding = clusterable_embedding_df.values  # use numpy array for speed

        # Grid space (use new parsers; defaults are specified in argparse)
        eps_list = _parse_seq_floats(args.grid_eps)
        min_samples_list = _parse_seq_ints(args.grid_min_samples)
        min_cluster_size_list = _parse_seq_ints(args.grid_min_cluster_size)

        logger.info("Grid sizes — epsilon: %d, min_samples: %d, min_cluster_size: %d",
                    len(eps_list), len(min_samples_list), len(min_cluster_size_list))

        l_eps = len(eps_list)
        l_ms = len(min_samples_list)
        l_mcs = len(min_cluster_size_list)
        total_cfg = l_eps * l_ms * l_mcs
        logger.info("Total grid configurations: %d", total_cfg)

        rng = np.random.default_rng(int(args.random_state))
        max_evals = int(getattr(args, "grid_max_evals", 0))
        if max_evals is None:
            max_evals = 0

        if max_evals > 0 and total_cfg > max_evals:
            sel = rng.choice(total_cfg, size=max_evals, replace=False)
            sel = np.sort(sel)
            logger.warning(
                "Grid too large (%d). Evaluating a random subset of %d configurations (set --grid_max_evals to change).",
                total_cfg, max_evals
            )
        else:
            sel = None

        def _decode_linear(idx: int):
            # Map linear index into (eps, ms, mcs) triple without materializing full product list
            per_eps = l_ms * l_mcs
            ieps = idx // per_eps
            rem = idx % per_eps
            ims = rem // l_mcs
            imcs = rem % l_mcs
            return eps_list[ieps], min_samples_list[ims], min_cluster_size_list[imcs]

        # Define evaluation of a single configuration
        def evaluate_config(epsilon, min_samples, min_cluster_size, emb):
            clusterer = hdbscan.HDBSCAN(
                min_samples=min_samples,
                min_cluster_size=min_cluster_size,
                cluster_selection_epsilon=epsilon,
                cluster_selection_method='eom'
            ).fit(emb)

            labels = clusterer.labels_
            num_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            noise_count = int((labels == -1).sum())

            if num_clusters > 1:
                non_noise_indices = labels != -1
                filtered_labels = labels[non_noise_indices]
                filtered_embedding = emb[non_noise_indices]

                sil_values = silhouette_samples(filtered_embedding, filtered_labels)
                sil_avg = float(np.mean(sil_values))

                return {
                    "Silhouette_avg": sil_avg,
                    "Epsilon": float(epsilon),
                    "Min_samples": int(min_samples),
                    "Min_cluster_size": int(min_cluster_size),
                    "Clusters": int(num_clusters),
                    "Noise_points": int(noise_count),
                }
            return None

        if sel is None:
            iter_triples = ((eps, ms, mcs) for eps in eps_list for ms in min_samples_list for mcs in min_cluster_size_list)
        else:
            iter_triples = (_decode_linear(int(i)) for i in sel)

        configs = Parallel(n_jobs=args.n_jobs)(
            delayed(evaluate_config)(eps, ms, mcs, clusterable_embedding)
            for (eps, ms, mcs) in iter_triples
        )

        # Filter out None and save to scree CSV
        suitable = [c for c in configs if c is not None]
        df_scree = pd.DataFrame(suitable)
        if df_scree.empty:
            logger.warning("Grid search produced no valid cluster configurations (num_clusters <= 1 everywhere).")
        else:
            # Optional: sort by Clusters desc, Silhouette desc to mirror manual inspection
            df_scree = df_scree.sort_values(by=["Clusters", "Silhouette_avg"], ascending=[False, False])
            logger.info("Top of grid search results:\n%s", df_scree.head(10).to_string(index=False))

        ensure_parent_dir(paths["screeinput"])
        df_scree.to_csv(paths["screeinput"], index=False)
        logger.info("saving cluster properties to file.... -> %s", paths["screeinput"])
    except Exception as e:
        _handle_stage_exception("Cell 5 grid search", e)

    # =============================
    # Cell 6: Generate the three scree plots
    # Notebook behavior: show() the figures; CLI behavior: save HTML + log.
    # =============================
    try:
        logger.info("generating screeplots....")
        if no_plots:
            logger.info("--no_plots set; skipping scree plot exports.")
            # Stage skip
            raise RuntimeError("NO_PLOTS_STAGE_SKIP")
        try:
            dfsc = pd.read_csv(paths["screeinput"], engine="pyarrow")
        except Exception as e_read:
            logger.warning("Falling back to pandas CSV reader for screeinput (pyarrow failed: %s)", e_read)
            dfsc = pd.read_csv(paths["screeinput"])

        # Sort by Clusters desc then Silhouette_avg desc for inspection parity
        sorted_dfsc = dfsc.sort_values(by=["Clusters", "Silhouette_avg"], ascending=[False, False])
        logger.info("Scree input (sorted) head:\n%s", sorted_dfsc.head(10).to_string(index=False))

        # 1) Silhouette Average vs Clusters
        fig1 = px.scatter(
            sorted_dfsc, x="Silhouette_avg", y="Clusters",
            title="Silhouette Average vs. Clusters",
            labels={"Silhouette_avg": "Silhouette Average", "Clusters": "Number of Clusters"},
            hover_data=sorted_dfsc.columns
        )
        ensure_parent_dir(paths["screeplot1"])
        pio.write_html(fig1, file=paths["screeplot1"], auto_open=False)
        logger.info("Saved scree plot 1 to %s", paths["screeplot1"])

        # 2) Noise Points vs Clusters
        fig2 = px.scatter(
            sorted_dfsc, x="Noise_points", y="Clusters",
            title="Noise Points vs. Clusters",
            labels={"Noise_points": "Number of Noise Points", "Clusters": "Number of Clusters"},
            hover_data=sorted_dfsc.columns
        )
        ensure_parent_dir(paths["screeplot2"])
        pio.write_html(fig2, file=paths["screeplot2"], auto_open=False)
        logger.info("Saved scree plot 2 to %s", paths["screeplot2"])

        # 3) Silhouette Averages vs Noise Points
        fig3 = px.scatter(
            sorted_dfsc, x="Silhouette_avg", y="Noise_points",
            title="Silhouette Averages vs. Noise Points",
            labels={"Silhouette_avg": "Silhouette Average", "Noise_points": "Number of Noise Points"},
            hover_data=sorted_dfsc.columns
        )
        ensure_parent_dir(paths["screeplot3"])
        pio.write_html(fig3, file=paths["screeplot3"], auto_open=False)
        logger.info("Saved scree plot 3 to %s", paths["screeplot3"])
    except Exception as e:
        if str(e) == "NO_PLOTS_STAGE_SKIP":
            logger.info("Scree plots skipped.")
        else:
            _handle_stage_exception("Cell 6 scree plots", e)

    # =============================
    # Cell 7: Optimization code to select best cluster solution
    # - Normalizes Silhouette_avg, Clusters, Noise_points to [0,1]
    # - Computes weights by dynamic range
    # - Builds weighted Score = +wS*Sil - wN*Noise + wC*Clusters
    # - Picks top, median, and (optionally) a custom override rank from CLI
    # - Saves the sorted table to Stage_03 as per notebook
    # =============================
    try:
        logger.info("carrying out optimization for cluster selection....")
        try:
            df_opt = pd.read_csv(paths["screeinput"], engine="pyarrow")
        except Exception as e_read:
            logger.warning("Falling back to pandas CSV reader for screeinput (pyarrow failed: %s)", e_read)
            df_opt = pd.read_csv(paths["screeinput"])

        if df_opt.empty:
            logger.warning("Optimization skipped: screeinput is empty.")
        else:
            # Normalize to [0,1] with safe division
            def _safe_norm(series: pd.Series) -> pd.Series:
                m = series.max()
                if pd.isna(m) or m == 0:
                    return pd.Series(0.0, index=series.index)
                return series / m

            df_opt["Silhouette_avg_normalized"] = _safe_norm(df_opt["Silhouette_avg"])
            df_opt["Clusters_normalized"] = _safe_norm(df_opt["Clusters"])
            df_opt["Noise_points_normalized"] = _safe_norm(df_opt["Noise_points"])

            # Compute ranges
            range_silhouette = float(df_opt["Silhouette_avg"].max() - df_opt["Silhouette_avg"].min())
            range_clusters = float(df_opt["Clusters"].max() - df_opt["Clusters"].min())
            range_noise = float(df_opt["Noise_points"].max() - df_opt["Noise_points"].min())
            total_range = range_silhouette + range_clusters + range_noise

            if total_range <= 0 or pd.isna(total_range):
                # Fallback to equal weights
                weight_silhouette = weight_clusters = weight_noise = 1.0 / 3.0
            else:
                weight_silhouette = range_silhouette / total_range
                weight_clusters = range_clusters / total_range
                weight_noise = range_noise / total_range

            logger.info(
                "Assigned Weights: Silhouette = %.6f, Clusters = %.6f, Noise = %.6f",
                weight_silhouette, weight_clusters, weight_noise
            )

            # Weighted score (maximize Silhouette and Clusters, minimize Noise)
            df_opt["Score"] = (
                weight_silhouette * df_opt["Silhouette_avg_normalized"]
                + weight_clusters * df_opt["Clusters_normalized"]
                - weight_noise * df_opt["Noise_points_normalized"]
            )

            # Sort by score descending
            df_sorted = df_opt.sort_values(by="Score", ascending=False)

            # Top configuration
            top_config = df_sorted.iloc[0]
            logger.info("Top configuration based on weighted score:\n%s", top_config.to_string())

            # Median configuration
            median_index = len(df_sorted) // 2
            median_config = df_sorted.iloc[median_index]
            logger.info("Median configuration based on weighted score:\n%s", median_config.to_string())

            # Optional manual override by rank
            if args.override_rank is not None:
                if 0 <= args.override_rank < len(df_sorted):
                    top_config = df_sorted.iloc[int(args.override_rank)]
                    logger.info("Customized configuration based on override rank %d:\n%s",
                                args.override_rank, top_config.to_string())
                else:
                    logger.warning("override_rank %d is out of bounds [0, %d); using top config instead.",
                                   args.override_rank, len(df_sorted))

            # Extract best params for downstream steps
            best_epsilon = float(top_config["Epsilon"])
            best_min_samples = int(top_config["Min_samples"])
            best_min_cluster_size = int(top_config["Min_cluster_size"])
            best_avg_silhouette = float(top_config["Silhouette_avg"])

            logger.info("Best Epsilon: %s", best_epsilon)
            logger.info("Best Min Samples: %s", best_min_samples)
            logger.info("Best Min Cluster Size: %s", best_min_cluster_size)
            logger.info("Best Average Silhouette: %s", best_avg_silhouette)

            # Persist the sorted table
            ensure_parent_dir(paths["optimized_out"])
            df_sorted.to_csv(paths["optimized_out"], index=False)
            logger.info("saving optimized cluster outputs.... -> %s", paths["optimized_out"])

            # Stash into locals for later cells that may use these
            # (These variables remain in scope within main() for subsequent steps.)
        # end non-empty
    except Exception as e:
        _handle_stage_exception("Cell 7 optimization", e)

    # =============================
    # Cell 8: Sequential clustering using optimized HDBSCAN parameters
    # - Fits HDBSCAN with best_* from Cell 7
    # - Computes cluster counts and silhouette diagnostics
    # - Saves silhouette analysis plot to Stage_07 (silplot)
    # =============================
    try:
        logger.info("conducting HDBSCAN procedures based on optimized cluster solution...")

        # Ensure we have the embedding in memory; reload if needed
        if 'clusterable_embedding' not in locals():
            try:
                _df_emb = pd.read_csv(paths["hdbscan_input"], engine="pyarrow")
            except Exception as e_read:
                logger.warning("Falling back to pandas CSV reader for hdbscan_input reload (pyarrow failed: %s)", e_read)
                _df_emb = pd.read_csv(paths["hdbscan_input"])
            clusterable_embedding = _df_emb.values

        # Ensure we have chosen parameters; if not (e.g., optimization skipped), try loading optimized_out
        if 'best_epsilon' not in locals() or 'best_min_samples' not in locals() or 'best_min_cluster_size' not in locals():
            try:
                df_sorted_fallback = pd.read_csv(paths["optimized_out"])
                top_config_fb = df_sorted_fallback.iloc[0]
                best_epsilon = float(top_config_fb["Epsilon"])
                best_min_samples = int(top_config_fb["Min_samples"])
                best_min_cluster_size = int(top_config_fb["Min_cluster_size"])
                best_avg_silhouette = float(top_config_fb.get("Silhouette_avg", np.nan))
                logger.warning("Optimized params not found in memory; using top row from optimized_out.")
            except Exception as e_fb:
                logger.exception("No optimized parameters available and failed to reload from file: %s", e_fb)
                raise

        epsilon = float(best_epsilon)
        min_samples = int(best_min_samples)
        min_cluster_size = int(best_min_cluster_size)
        avgsil = float(best_avg_silhouette) if 'best_avg_silhouette' in locals() else np.nan

        # Fit HDBSCAN and obtain labels
        labels = hdbscan.HDBSCAN(
            min_samples=min_samples,
            min_cluster_size=min_cluster_size,
            cluster_selection_epsilon=epsilon,
            cluster_selection_method='eom'
        ).fit_predict(clusterable_embedding)

        # Count clusters excluding noise (-1)
        from collections import Counter
        hdb_counter = Counter(labels)
        hdb_n_clusters = len([lab for lab in hdb_counter.keys() if lab != -1])

        # Compute silhouette on non-noise points if at least 2 clusters exist
        unique_non_noise = [c for c in np.unique(labels) if c != -1]
        if len(unique_non_noise) > 1:
            mask_nn = labels != -1
            silhouette_avg = silhouette_score(clusterable_embedding[mask_nn], labels[mask_nn])
        else:
            silhouette_avg = -1.0

        logger.info("n_components (requested): %d", args.n_components)
        logger.info("silhouette_avg (non-noise): %.6f", silhouette_avg)
        logger.info("Clusters (excluding noise): %d", hdb_n_clusters)

        # Silhouette analysis plot (use non-noise labels for stability)
        try:
            if len(unique_non_noise) > 1:
                sil_vals = silhouette_samples(clusterable_embedding[mask_nn], labels[mask_nn])
                cl_labels = np.unique(labels[mask_nn])
                y_lower, y_upper = 0, 0
                yticks = []

                plt.figure(figsize=(8, 6))
                for i, c in enumerate(cl_labels):
                    c_sil_vals = sil_vals[labels[mask_nn] == c]
                    c_sil_vals.sort()
                    y_upper += len(c_sil_vals)
                    plt.barh(range(y_lower, y_upper), c_sil_vals, edgecolor='none', height=1)
                    yticks.append((y_lower + y_upper) / 2)
                    y_lower += len(c_sil_vals)

                # Red line = mean of current silhouette; Blue line = average from grid-search best (if available)
                plt.axvline(np.mean(sil_vals), color="red", linestyle="--", label="Mean silhouette (current)")
                if not np.isnan(avgsil):
                    plt.axvline(avgsil, color="blue", linestyle="--", label="Mean silhouette (optimized row)")
                plt.yticks(yticks, cl_labels + 1)
                plt.ylabel('Cluster')
                plt.xlabel('Silhouette coefficient')
                plt.title('Silhouette Analysis')
                plt.legend(loc="best")
                plt.tight_layout()
                if no_plots:
                    logger.info("--no_plots set; skipping silhouette plot export.")
                else:
                    ensure_parent_dir(paths["silplot"])
                    plt.savefig(paths["silplot"])
                plt.close()
                if not no_plots:
                    logger.info("Silhouette analysis plot saved to %s", paths["silplot"])
            else:
                logger.warning("Silhouette plot skipped: need at least 2 non-noise clusters.")
        except Exception as e_plot:
            logger.exception("Failed to generate silhouette analysis plot: %s", e_plot)

    except Exception as e:
        _handle_stage_exception("Cell 8 clustering", e)

    # =============================
    # Cell 9: Additional cluster indices (Trustworthiness, Continuity, CH, DB, Dunn)
    # - By default, compute on the SAME feature space used for clustering ('hdbscan') and EXCLUDE noise.
    # - You can override with --metrics_space viz and/or --metrics_include_noise.
    # NOTE: Trust/Continuity are neighborhood-preservation measures (X vs embedding) and do not use labels directly.
    # =============================
    try:
        logger.info("computing additional cluster fit statistics...")

        # Decide feature space
        if args.metrics_space == "viz":
            if 'clusterable_embedding_viz' in locals():
                feats = clusterable_embedding_viz
                logger.info("Using 'viz' feature space (3D UMAP) for metrics.")
            else:
                logger.warning("'viz' feature space requested but unavailable; falling back to 'hdbscan' space.")
                feats = clusterable_embedding if 'clusterable_embedding' in locals() else None
        else:
            feats = clusterable_embedding if 'clusterable_embedding' in locals() else None

        if feats is None:
            try:
                _df_emb2 = pd.read_csv(paths["hdbscan_input"], engine="pyarrow")
            except Exception as e_read2:
                logger.warning("Falling back to pandas CSV reader for hdbscan_input (pyarrow failed: %s)", e_read2)
                _df_emb2 = pd.read_csv(paths["hdbscan_input"])
            feats = _df_emb2.values
            logger.info("Reloaded HDBSCAN feature space from %s", paths["hdbscan_input"])

        # Ensure we have labels
        if 'labels' not in locals():
            logger.warning("Labels not found in memory; refitting HDBSCAN with best parameters for metrics.")
            labels = hdbscan.HDBSCAN(
                min_samples=int(best_min_samples),
                min_cluster_size=int(best_min_cluster_size),
                cluster_selection_epsilon=float(best_epsilon),
                cluster_selection_method='eom'
            ).fit_predict(feats)

        labels_arr = np.asarray(labels)
        if args.metrics_include_noise:
            mask = np.ones_like(labels_arr, dtype=bool)
        else:
            mask = labels_arr != -1

        # Sanity for metrics requiring >= 2 clusters
        unique_masked = np.unique(labels_arr[mask])
        unique_masked = unique_masked[unique_masked != -1] if not args.metrics_include_noise else unique_masked
        if mask.sum() < 2 or unique_masked.size < 2:
            logger.warning("Insufficient non-noise clusters for CH/DB/Dunn; metrics will be NaN.")
        
        # Trustworthiness & Continuity (on masked rows to align with cluster-space computation)
        try:
            Xm = (X.values if hasattr(X, "values") else X)[mask]
            Fm = feats[mask]

            # Optional subsampling to control O(n^2) memory in trust/continuity
            max_n = int(getattr(args, "max_samples_trust", 0))
            if max_n and max_n > 0 and Xm.shape[0] > max_n:
                rng_tc = np.random.default_rng(int(getattr(args, "trust_seed", 42)))
                sel_idx = rng_tc.choice(Xm.shape[0], size=max_n, replace=False)
                Xm = Xm[sel_idx]
                Fm = Fm[sel_idx]
                logger.warning("Subsampling trust/continuity to %d samples (from %d).", max_n, mask.sum())

            trust = trustworthiness(Xm, Fm, n_neighbors=int(args.trust_k))
            cont = continuity(Xm, Fm, n_neighbors=int(args.trust_k))
        except Exception as e_tc:
            logger.exception("Trust/Continuity computation failed: %s", e_tc)
            trust = float("nan")
            cont = float("nan")

        # CH / DB
        try:
            ch_score = calinski_harabasz_score(Fm, labels_arr[mask]) if unique_masked.size >= 2 else float("nan")
        except Exception as e_ch:
            logger.exception("CH score failed: %s", e_ch)
            ch_score = float("nan")

        try:
            db_score = davies_bouldin_score(Fm, labels_arr[mask]) if unique_masked.size >= 2 else float("nan")
        except Exception as e_db:
            logger.exception("DB score failed: %s", e_db)
            db_score = float("nan")

        # Dunn
        try:
            dunn = dunn_index(Fm, labels_arr[mask]) if unique_masked.size >= 2 else float("nan")
        except Exception as e_dn:
            logger.exception("Dunn index failed: %s", e_dn)
            dunn = float("nan")

        # Log summary
        logger.info("Trustworthiness (k=%d): %s", args.trust_k, f"{trust:.4f}" if np.isfinite(trust) else "NaN")
        logger.info("Continuity (k=%d): %s", args.trust_k, f"{cont:.4f}" if np.isfinite(cont) else "NaN")
        logger.info("HDBSCAN epsilon (cluster_selection_epsilon): %s", best_epsilon if 'best_epsilon' in locals() else "NA")
        logger.info("HDBSCAN min_samples: %s", best_min_samples if 'best_min_samples' in locals() else "NA")
        logger.info("HDBSCAN min_cluster_size: %s", best_min_cluster_size if 'best_min_cluster_size' in locals() else "NA")
        # Cluster counts (computed on the full label vector for clear interpretation)
        n_clusters_incl_noise = int(np.unique(labels_arr).size)
        n_clusters_excl_noise = int(len([c for c in np.unique(labels_arr) if c != -1]))
        logger.info("Clusters (including noise): %d", n_clusters_incl_noise)
        logger.info("Clusters (excluding noise): %d", n_clusters_excl_noise)
        logger.info("Silhouette_avg (non-noise): %s", f"{silhouette_avg:.4f}" if 'silhouette_avg' in locals() else "NA")
        logger.info("Calinski-Harabasz Index: %s", f"{ch_score:.4f}" if np.isfinite(ch_score) else "NaN")
        logger.info("Davies-Bouldin Index: %s", f"{db_score:.4f}" if np.isfinite(db_score) else "NaN")
        logger.info("Dunn Index: %s", f"{dunn:.4f}" if np.isfinite(dunn) else "NaN")

        # Optional CSV append
        if args.metrics_csv:
            import csv
            header = ["metrics_space", "include_noise", "trust_k", "trustworthiness", "continuity",
                      "epsilon", "min_samples", "min_cluster_size", "silhouette_avg",
                      "calinski_harabasz", "davies_bouldin", "dunn_index",
                      "n_clusters_masked", "n_points_masked"]
            row = [
                args.metrics_space,
                bool(args.metrics_include_noise),
                int(args.trust_k),
                float(trust) if np.isfinite(trust) else np.nan,
                float(cont) if np.isfinite(cont) else np.nan,
                float(best_epsilon) if 'best_epsilon' in locals() else np.nan,
                int(best_min_samples) if 'best_min_samples' in locals() else np.nan,
                int(best_min_cluster_size) if 'best_min_cluster_size' in locals() else np.nan,
                float(silhouette_avg) if 'silhouette_avg' in locals() and np.isfinite(silhouette_avg) else np.nan,
                float(ch_score) if np.isfinite(ch_score) else np.nan,
                float(db_score) if np.isfinite(db_score) else np.nan,
                float(dunn) if np.isfinite(dunn) else np.nan,
                int(unique_masked.size),
                int(mask.sum())
            ]
            try:
                write_header = not os.path.exists(args.metrics_csv)
                with open(args.metrics_csv, "a", newline="") as fcsv:
                    writer = csv.writer(fcsv)
                    if write_header:
                        writer.writerow(header)
                    writer.writerow(row)
                logger.info("Appended metrics row to %s", args.metrics_csv)
            except Exception as e_csv:
                logger.exception("Failed to append metrics CSV: %s", e_csv)

    except Exception as e:
        _handle_stage_exception("Cell 9 metrics", e)

    # =============================
    # Cell 10: Build UMAP dataframe with labels and save
    # - Creates df_umap from visualization embedding
    # - Appends HDBSCAN labels
    # - Attaches an 'index' column derived from X.index
    # - Saves to Stage_09 CSV (umapdataframe)
    # =============================
    try:
        logger.info("creating data frame for easy visualization....")

        # Ensure we have the visualization embedding
        if 'clusterable_embedding_viz' not in locals():
            logger.warning("Visualization embedding not found; recomputing a small viz UMAP for dataframe export.")
            clusterable_embedding_viz = umap.UMAP(
                densmap=args.densmap,
                n_neighbors=args.n_neighbors,
                min_dist=args.min_dist,
                n_components=args.n_components,
                random_state=args.random_state,
            ).fit_transform(X.values if hasattr(X, "values") else X)

        # Ensure we have labels (from Cell 8). If missing, refit using best params.
        if 'labels' not in locals():
            logger.warning("Labels not found in memory; refitting HDBSCAN with best parameters for dataframe export.")
            labels = hdbscan.HDBSCAN(
                min_samples=int(best_min_samples),
                min_cluster_size=int(best_min_cluster_size),
                cluster_selection_epsilon=float(best_epsilon),
                cluster_selection_method='eom'
            ).fit_predict(clusterable_embedding if 'clusterable_embedding' in locals() else clusterable_embedding_viz)

        # Build UMAP dataframe
        umap_cols = [f"UMAP_{i+1}" for i in range(clusterable_embedding_viz.shape[1])]
        df_umap = pd.DataFrame(clusterable_embedding_viz, columns=umap_cols)
        df_umap["label"] = labels

        # Log cluster sizes (counts only, to keep logs manageable)
        unique_lbls = sorted(np.unique(labels))
        for cl in unique_lbls:
            cnt = int(np.sum(labels == cl))
            logger.info("Cluster %s: %d samples", cl, cnt)

        # Attach an 'index' column derived from X.index (string)
        idp_label = pd.DataFrame({"index": (X.index.astype(str) if hasattr(X.index, "astype") else pd.Index(X.index).astype(str))})
        df_umap_with_label = pd.concat([idp_label.reset_index(drop=True), df_umap.reset_index(drop=True)], axis=1)

        # Save to CSV
        ensure_parent_dir(paths["umapdataframe"])
        df_umap_with_label.to_csv(paths["umapdataframe"], index=False)
        logger.info("UMAP viz with cluster solutions saved to %s (shape=%s)", paths["umapdataframe"], df_umap_with_label.shape)

        # Optional quick head for verification
        logger.info("checking umap viz with cluster solutions.....")
        try:
            logger.info("df_umap_with_label.head(5):\n%s", df_umap_with_label.head(5).to_string(index=False))
        except Exception as _eh:
            logger.debug("Failed to render df_umap_with_label.head() to string: %s", _eh)

    except Exception as e:
        _handle_stage_exception("Cell 10 dataframe export", e)

    # =============================
    # Cell 11: 3D Plotly cluster visualization (cluster solutions)
    # - Colors by HDBSCAN label; grey for noise (-1)
    # - Saves interactive HTML to Stage_10 (clusterplot1)
    # =============================
    try:
        logger.info("generating 3D plotly solutions....")

        # Ensure viz embedding available
        if 'clusterable_embedding_viz' not in locals():
            logger.warning("Visualization embedding not found; recomputing for 3D cluster plot.")
            clusterable_embedding_viz = umap.UMAP(
                densmap=args.densmap,
                n_neighbors=args.n_neighbors,
                min_dist=args.min_dist,
                n_components=args.n_components,
                random_state=args.random_state,
            ).fit_transform(X.values if hasattr(X, "values") else X)

        # Ensure labels available
        if 'labels' not in locals():
            logger.warning("Labels not found; refitting HDBSCAN for 3D cluster plot.")
            # Prefer using the consolidated embedding if available; fallback to viz embedding
            feats_for_labels = clusterable_embedding if 'clusterable_embedding' in locals() else clusterable_embedding_viz
            labels = hdbscan.HDBSCAN(
                min_samples=int(best_min_samples),
                min_cluster_size=int(best_min_cluster_size),
                cluster_selection_epsilon=float(best_epsilon),
                cluster_selection_method='eom'
            ).fit_predict(feats_for_labels)

        # Require at least 3D to plot 3D; fallback to 2D if n_components < 3
        if clusterable_embedding_viz.shape[1] < 3:
            logger.warning("Visualization embedding has <3 dimensions; falling back to 2D scatter.")
            import plotly.express as px
            df_tmp = pd.DataFrame(clusterable_embedding_viz, columns=[f"UMAP_{i+1}" for i in range(clusterable_embedding_viz.shape[1])])
            df_tmp["label"] = labels
            fig = px.scatter(
                df_tmp, x="UMAP_1", y=("UMAP_2" if "UMAP_2" in df_tmp.columns else "UMAP_1"),
                color=df_tmp["label"].astype(str),
                title="Neuroimaging IDP Cluster Solution (2D fallback)",
                opacity=0.85
            )
            if no_plots:
                logger.info("--no_plots set; skipping cluster plot export.")
            else:
                ensure_parent_dir(paths["clusterplot1"])
                pio.write_html(fig, file=paths["clusterplot1"], auto_open=False)
                logger.info("Saved 2D cluster solution plot to %s", paths["clusterplot1"])
        else:
            # Build 3D cluster plot
            import plotly.express as px
            clustered = (labels >= 0)
            unique_labels = np.unique(labels[clustered]) if np.any(clustered) else np.array([], dtype=int)

            # Combine palettes to expand number of distinct colors
            all_palettes = px.colors.qualitative.Plotly + px.colors.qualitative.Dark24
            if len(unique_labels) > len(all_palettes):
                logger.warning("More clusters (%d) than colors (%d); colors will cycle.", len(unique_labels), len(all_palettes))

            fig = go.Figure()

            # Add a trace per cluster label (excluding noise)
            for i, lab in enumerate(unique_labels):
                mask = (labels == lab)
                fig.add_trace(go.Scatter3d(
                    x=clusterable_embedding_viz[mask, 0],
                    y=clusterable_embedding_viz[mask, 1],
                    z=clusterable_embedding_viz[mask, 2],
                    mode="markers",
                    marker=dict(
                        size=5,
                        color=all_palettes[i % len(all_palettes)],
                        opacity=0.85
                    ),
                    name=f"hdbs k {lab}"
                ))

            # Optional: noise points
            if np.any(labels == -1):
                mask_noise = (labels == -1)
                fig.add_trace(go.Scatter3d(
                    x=clusterable_embedding_viz[mask_noise, 0],
                    y=clusterable_embedding_viz[mask_noise, 1],
                    z=clusterable_embedding_viz[mask_noise, 2],
                    mode="markers",
                    marker=dict(size=4, color="grey", opacity=0.6),
                    name="Noise"
                ))

            fig.update_layout(
                title="Neuroimaging IDP Cluster Solution",
                scene=dict(
                    xaxis_title="UMAP1",
                    yaxis_title="UMAP2",
                    zaxis_title="UMAP3"
                ),
                legend_title="IDP Clusters",
                legend=dict(
                    x=0.8,
                    y=0.5,
                    bgcolor="rgba(255,255,255,0.5)",
                    bordercolor="Black"
                )
            )

            if no_plots:
                logger.info("--no_plots set; skipping cluster plot export.")
            else:
                ensure_parent_dir(paths["clusterplot1"])
                pio.write_html(fig, file=paths["clusterplot1"], auto_open=False)
                logger.info("Saved 3D cluster solution plot to %s", paths["clusterplot1"])

    except Exception as e:
        _handle_stage_exception("Cell 11 cluster plots", e)

    # =============================
    # Cell 12: Merge IDP_KEY.csv with UMAP dataframe
    # - Reads the IDP key from --idp_key
    # - Ensures 'index' is string on both sides
    # - Merges on 'index' (left join from key to UMAP labels/coords)
    # - Keeps result in memory as `merged_df` for downstream plots (e.g., modalities)
    # =============================
    try:
        logger.info("merging IDP key with UMAP data....")
        if not os.path.isfile(paths["idp_key"]):
            logger.warning("IDP key file not found at %s; skipping merge.", paths["idp_key"])
        else:
            try:
                idp_key = pd.read_csv(paths["idp_key"], engine="pyarrow")
            except Exception as e_read:
                logger.warning("Falling back to pandas CSV reader for idp_key (pyarrow failed: %s)", e_read)
                idp_key = pd.read_csv(paths["idp_key"])

            # Ensure 'index' is string in key
            if "index" not in idp_key.columns:
                logger.warning("IDP key does not contain an 'index' column; columns are: %s. Skipping merge.", list(idp_key.columns))
            else:
                idp_key["index"] = idp_key["index"].astype(str)

                # Ensure df_umap_with_label is available; load from disk if needed
                if 'df_umap_with_label' not in locals():
                    try:
                        df_umap_with_label = pd.read_csv(paths["umapdataframe"], engine="pyarrow")
                    except Exception as e_read2:
                        logger.warning("Falling back to pandas CSV reader for umapdataframe (pyarrow failed: %s)", e_read2)
                        df_umap_with_label = pd.read_csv(paths["umapdataframe"])

                # Ensure 'index' exists and is string in df_umap_with_label
                if "index" not in df_umap_with_label.columns:
                    logger.warning("'index' column not found in df_umap_with_label; attempting to recover from DataFrame index.")
                    df_umap_with_label = df_umap_with_label.reset_index()
                    df_umap_with_label["index"] = df_umap_with_label["index"].astype(str)
                else:
                    df_umap_with_label["index"] = df_umap_with_label["index"].astype(str)

                # Merge
                merged_df = pd.merge(idp_key, df_umap_with_label, on="index", how="left")

                # Save merged table to disk
                try:
                    ensure_parent_dir(paths["merged_umap"])
                    merged_df.to_csv(paths["merged_umap"], index=False)
                    logger.info("Merged UMAP+IDP key saved to %s (shape=%s)", paths["merged_umap"], merged_df.shape)
                except Exception as e_save:
                    logger.exception("Failed to write merged UMAP table to %s: %s", paths["merged_umap"], e_save)

                logger.info("Merged DataFrame shape: %s", merged_df.shape)
                try:
                    logger.info("Merged head(5):\n%s", merged_df.head(5).to_string(index=False))
                except Exception as _ehm:
                    logger.debug("Failed to render merged_df.head() to string: %s", _ehm)
    except Exception as e:
        _handle_stage_exception("Cell 12 merge idp_key", e)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
