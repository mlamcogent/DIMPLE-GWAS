# DIMPLE-GWAS: Dimensionality Reduction and Integrated Multi-Phenotype Landscape Explorer

DIMPLE-GWAS is a command-line pipeline for clustering high-dimensional phenotypes (e.g., neuroimaging imaging-derived phenotypes/IDPs, or multi-omics feature vectors). It generates UMAP embeddings (optionally as an ensemble across multiple random seeds), performs a parallelized HDBSCAN hyperparameter search, selects an operating point using quantitative diagnostics, and exports analysis-ready tables and figures.

## Quick start

### Option A: venv (pip)

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\\Scripts\\activate       # Windows PowerShell

python -m pip install --upgrade pip
pip install -r requirements.txt

# Smoke test on bundled toy data
python DIMPLEGWAS.py --dry-run --datainput test_data/test_dat.csv --idp_key test_data/IDP_KEY.csv
python DIMPLEGWAS.py --datainput test_data/test_dat.csv --idp_key test_data/IDP_KEY.csv
```

### Option B: conda (recommended for compiled/binary deps)

On some Linux/HPC images, wheels for compiled extensions can be unreliable. In that case, install **compiled dependencies** from **conda-forge** first, then install the remaining Python deps via pip.

```bash
conda create -n dimple python=3.11 -y
conda activate dimple

# Prefer conda-forge for compiled deps (avoid source builds)
conda install -c conda-forge -y \
  hdbscan umap-learn numba llvmlite pyarrow \
  matplotlib plotly

# Install the remaining Python dependencies from requirements.txt
# (Use --no-deps so pip does not overwrite the conda-forge builds above.)
pip install --no-deps -r requirements.txt

python DIMPLEGWAS.py --dry-run --datainput test_data/test_dat.csv --idp_key test_data/IDP_KEY.csv
python DIMPLEGWAS.py --datainput test_data/test_dat.csv --idp_key test_data/IDP_KEY.csv
```

---

## Repository layout

```text
.
├── DIMPLEGWAS.py                 # Main pipeline script
├── requirements.txt              # Python dependencies (default install target)
├── README.md                     # Project documentation
├── LICENSE
├── test_data/
│   ├── test_dat.csv              # Bundled toy dataset (input matrix)
│   └── IDP_KEY.csv               # Feature key for toy dataset (required for feature re-identification)
└── utility/
    ├── dimple-ref-run.py         # Reference (hard-coded) run used for regression checks
    ├── generate_idp_key.py       # Utility to generate IDP_KEY.csv for a new dataset
    └── legacy_explicit.txt       # Conda @EXPLICIT spec for the manuscript environment
```

## What is `IDP_KEY.csv` and why it matters?

`IDP_KEY.csv` is the feature dictionary that allows DIMPLE-GWAS to re-identify features later (e.g., for plots, tables, and cluster interpretation). For generality across datasets, the pipeline only requires **three columns**:

- `index` — stable feature identifier (often an integer index)
- `feature_name` — human-readable feature name (e.g., “Left-Hippocampus volume”)
- `feature_category_name` — a broad category/modality label (e.g., “subcortical”, “DTI”, “proteomics”, “metabolomics”)

If you omit `--idp_key`, the pipeline can still cluster, but downstream interpretation outputs will be less informative.

---

## Running the pipeline

Run `python DIMPLEGWAS.py --help` to see the definitive CLI options for your version.

### Example run (publication-style parameters)

From the repo root, you can run the bundled toy dataset with a fully specified parameter set (this is also a good template for real data):

```bash
python3 DIMPLEGWAS.py \
  --datainput "test_data/test_dat.csv" \
  --outdir output \
  --idp_key "test_data/IDP_KEY.csv" \
  --n_neighbors 30 \
  --min_dist 0.0 \
  --n_components 3 \
  --densmap \
  --random_state 42 \
  --n_random_states 1000 \
  --n_jobs -1 \
  --grid_eps 0:3 \
  --grid_min_samples 2:20 \
  --grid_min_cluster_size 5:50 \
  --silhouette_include_noise \
  --dry-run
```

Remove `--dry-run` to execute the full pipeline.

---

## Utility scripts

### 1) Generate `IDP_KEY.csv` for a new dataset

The script `utility/generate_idp_key.py` generates an `IDP_KEY.csv` containing the three required columns:

- `index`
- `feature_name`
- `feature_category_name`

Because datasets encode feature and category metadata differently, this utility is intentionally lightweight and may require you to provide the appropriate inputs/column mappings.

Run:

```bash
python utility/generate_idp_key.py --help
```

Then sanity-check the output:

```bash
python - <<'PY'
import pandas as pd
p = "IDP_KEY.csv"  # replace with your output path
k = pd.read_csv(p)
req = {"index", "feature_name", "feature_category_name"}
missing = req - set(k.columns)
assert not missing, f"Missing required columns: {missing}"
print(k.head())
PY
```

### 2) Reference run (regression check)

`utility/dimple-ref-run.py` is a “reference” implementation with fixed assumptions/hard-coded choices. It is useful as a regression check to ensure `DIMPLEGWAS.py` produces comparable outputs on the same input.

```bash
# Run the reference script as-is
# (It is intentionally hard-coded and does not expose a CLI parser.)
python utility/dimple-ref-run.py
```

See the header comments at the top of `utility/dimple-ref-run.py` for its assumptions (input paths, parameters, and output locations).

---

## Reproducing the manuscript environment (exact)

For publication-grade *exact* reproduction, this repo includes a pinned conda **@EXPLICIT** environment spec.

```bash
conda create -n dimple_legacy_exact --file utility/legacy_explicit.txt
conda activate dimple_legacy_exact
```

Notes:

- The explicit spec captures the exact conda artifacts used for the manuscript run.
- If you must add packages not present in the spec (e.g., `hdbscan`), do so minimally and record the exact versions installed (e.g., `pip freeze` and `conda list --explicit`).

---

## Reproducibility checklist (recommended for publications)

When you generate results for a manuscript, record:

- Input dataset checksum (e.g., `sha256sum`)
- Full CLI invocation
- Environment manifest (`conda list --explicit` and `pip freeze`)

## Citation / attribution

If you use DIMPLE-GWAS in a publication, please cite the accompanying manuscript and upstream methods (UMAP, HDBSCAN, and any additional statistical frameworks used in your analysis).