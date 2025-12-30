# DIMPLE: Dimensionality Reduction and Integrated Multi-Phenotype Landscape Explorer

DIMPLE is a command-line pipeline for clustering high-dimensional neuroimaging phenotypes (e.g., imaging-derived phenotypes, IDPs). It generates UMAP embeddings (optionally as an ensemble across multiple random seeds), performs a parallelized HDBSCAN hyperparameter search, selects an operating point using quantitative diagnostics, and exports analysis-ready tables and figures.

## Instructions (quick start)

1. Create and activate a Python environment.
2. Install dependencies from `requirements.txt`.
3. Run a smoke test using `--dry-run`.
4. Re-run without `--dry-run` to execute the workflow.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python dimple.py --dry-run --datainput toy_data.tsv
python dimple.py --datainput toy_data.tsv
```

---

## 1) Overview and installation

### What DIMPLE does

At a high level, DIMPLE:

- Generates UMAP embeddings (optionally as an ensemble across multiple seeds).
- Concatenates embeddings (e.g., 3 dimensions × *N* seeds) to capture stable structure.
- Searches HDBSCAN hyperparameters (e.g., min cluster size, min samples, epsilon) in parallel.
- Scores candidate solutions using silhouette and additional diagnostics.
- Selects a final clustering configuration and produces cluster assignments.
- Exports standard outputs (tables, plots, logs) suitable for downstream analysis.

### Inputs

DIMPLE expects an input matrix (TSV/CSV).

- Rows correspond to the entities being embedded and clustered (e.g., IDPs).
- Columns correspond to high-dimensional measurements (e.g., SNP loadings, imaging-derived vectors).

If your first column is an identifier, ensure your script version is configured accordingly (or pre-process the file to standardize the format).

### Installation

Recommended: Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python dimple.py --help
```

Notes:

- `pyarrow` is optional but can accelerate CSV/TSV reads.
- Large ensemble runs can require substantial RAM; start with smaller settings for smoke tests.

### Folder structure

```text
.
├── dimple.py               # Main pipeline script
├── plot_utils.py           # Visualization utilities (if present)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 2) CLI options (argparse)

Run `python dimple.py --help` to see the definitive options for your version.

### Core I/O

- `--datainput`  Path to the input matrix (`.tsv`/`.csv`).
- `--idp_key`  Optional path to `IDP_KEY.csv` used to enrich visualization outputs.

### Output artifacts

Defaults are stage-based filenames; you may override any of these to redirect outputs.

- `--prelim_umap`  Preliminary UMAP QC plot (HTML).
- `--hdbscan_input`  Concatenated embeddings used as HDBSCAN input (CSV).
- `--screeinput`  Grid-search results table used for diagnostics (CSV).
- `--optimized_out`  Ranked/optimized grid-search table (CSV).
- `--screeplot1`, `--screeplot2`, `--screeplot3`  Interactive diagnostic plots (HTML).
- `--silplot`  Silhouette analysis plot (PNG).
- `--logfile`  Run log / metrics summary (TXT).
- `--umapdataframe`  UMAP visualization table with cluster labels (CSV).
- `--clusterplot1`  3D cluster solution plot (HTML).
- `--clusterplot2`  3D modality overlay plot (HTML), if modality mapping is enabled.
- `--merged_umap`  Merged UMAP + IDP key table (CSV).

### Execution controls

- `--dry-run`  Validates inputs and prints the inferred configuration, then exits without running expensive steps.

Common performance-related flags (if enabled in your version):

- `--n_random_states`  Number of UMAP runs to ensemble. For testing, 10–50 is typical; for robust runs, 50–200 is common.
- `--n_components`  UMAP dimensionality per run (commonly 2 or 3).
- `--n_jobs`  Parallelism control; `-1` typically means “use all cores”.

---

## 3) Cloud deployments (GCP and AWS)

The ensemble UMAP and grid-search steps can be compute- and memory-intensive.

### Practical sizing guidance

- Laptop smoke tests: reduce `--n_random_states`, reduce grid size, and run `--dry-run` first.
- Workstation: 16–64 vCPU and 64–256 GB RAM can be appropriate depending on dataset size and ensemble settings.
- Cloud: select compute-optimized or high-memory instances based on the expected runtime and memory profile.

### AWS (EC2)

Lightweight test:

1. Launch Ubuntu 22.04 (e.g., `t3.xlarge` or similar).
2. Attach sufficient EBS (≥100 GB is a reasonable starting point).
3. SSH in and install prerequisites.

```bash
sudo apt-get update
sudo apt-get install -y git python3-venv build-essential

git clone <your_repo>
cd dimple_cluster_pipeline
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python dimple.py --dry-run --datainput toy_data.tsv
```

High-powered runs:

- Consider `m6i`/`r6i`/`c6i` families depending on CPU vs RAM needs.
- Use `tmux`/`screen` for long jobs.
- Treat Plotly HTML outputs as optional at very large `n` (files can be large).

### GCP (Compute Engine)

Lightweight test:

- Ubuntu 22.04 on `e2-standard-*` or `n2-standard-*`.

High-powered runs:

- Use high-memory machines (e.g., `n2-highmem-*`) when ensemble size or input dimensionality is large.
- Ensure persistent disk is sized appropriately; consider SSD-backed disks if I/O becomes limiting.

Operational notes (both clouds):

- Stage inputs locally on the VM to avoid repeated remote reads.
- Prefer checkpointing intermediate outputs by keeping the default stage artifacts, so reruns can resume.

---

## 4) Step-by-step feature walkthrough

### Stage A — Input validation and QC

- Parses the input matrix, validates dimensions and missingness assumptions, and checks that downstream parameters are coherent.
- `--dry-run` executes only this stage and prints the resolved configuration.

### Stage B — Preliminary UMAP (quick diagnostic)

- Produces an early embedding for sanity checking.
- Output: `--prelim_umap` (HTML).

### Stage C — Ensemble UMAP (optional but recommended)

- Runs UMAP across multiple seeds and concatenates embeddings to form the representation used for clustering.
- Output: `--hdbscan_input` (CSV).

### Stage D — Parallel HDBSCAN grid search

- Evaluates a parameter grid to identify stable clustering regimes.
- Output: `--screeinput` (CSV) containing silhouette, number of clusters, and noise points per configuration.

### Stage E — Diagnostic scree plots

- Visualizes trade-offs across solutions.
- Outputs: `--screeplot1/2/3` (HTML).

### Stage F — Optimization and selection

- Computes a composite ranking of solutions and selects the final configuration.
- Output: `--optimized_out` (CSV).

### Stage G — Final clustering and metrics

- Executes HDBSCAN using the selected configuration and computes clustering diagnostics.
- Outputs: `--silplot` (PNG) and `--logfile` (TXT).

### Stage H — Export results

- Exports visualization-ready tables mapping entities to UMAP coordinates and cluster labels.
- Outputs: `--umapdataframe` (CSV) and optionally `--merged_umap` (CSV).

### Stage I — Interactive 3D visualization

- Produces 3D plots colored by cluster (and optionally modality).
- Outputs: `--clusterplot1` and `--clusterplot2` (HTML).

---

## Reproducibility and performance notes

- Prefer fixed seeds for reproducible runs.
- Start with small `--n_random_states` and a coarse grid for smoke tests, then scale up.
- Trustworthiness/continuity computations can be memory-intensive on larger datasets; use subsampling or approximations if supported by your script version.

## Outputs (summary)

Typical outputs include:

- UMAP embeddings for clustering (`--hdbscan_input`)
- Grid search table (`--screeinput`)
- Optimization table (`--optimized_out`)
- Cluster assignment tables (`--umapdataframe`, `--merged_umap`)
- Diagnostic plots (HTML/PNG)

## Citation / attribution

If you use DIMPLE in a publication, please cite the accompanying manuscript and upstream methods (UMAP, HDBSCAN, and any additional statistical frameworks used in your analysis).