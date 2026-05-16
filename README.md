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

# Validate paths and CLI options
python DIMPLEGWAS.py --dry-run --datainput test_data/test_dat.csv --annotation_file test_data/IDP_KEY.csv

# Small smoke test on bundled toy data
python DIMPLEGWAS.py \
  --datainput test_data/test_dat.csv \
  --annotation_file test_data/IDP_KEY.csv \
  --outdir output_smoke \
  --n_random_states 2 \
  --grid_eps 0:1 \
  --grid_min_samples 2:4 \
  --grid_min_cluster_size 2:6 \
  --grid_max_evals 50 \
  --no_plots
```

### Option B: conda (recommended for compiled/binary deps)

On some Linux/HPC images, wheels for compiled extensions can be unreliable. In that case, install **compiled dependencies** from **conda-forge** first, then install the remaining Python deps via pip.

```bash
conda create -n dimple python=3.11 -y
conda activate dimple

# Prefer conda-forge for compiled deps (avoid source builds)
conda install -c conda-forge -y \
  numpy pandas scipy scikit-learn joblib \
  hdbscan umap-learn numba llvmlite pyarrow \
  matplotlib plotly

# Install the remaining Python dependencies from requirements.txt
# (Use --no-deps so pip does not overwrite the conda-forge builds above.)
pip install --no-deps -r requirements.txt

python DIMPLEGWAS.py --dry-run --datainput test_data/test_dat.csv --annotation_file test_data/IDP_KEY.csv
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
│   └── IDP_KEY.csv               # Example feature annotation file for toy dataset
└── utility/
    ├── dimple-ref-run.py         # Reference (hard-coded) run used for regression checks
    ├── generate_idp_key.py       # Utility to generate a simple feature annotation file
    └── legacy_explicit.txt       # Conda @EXPLICIT spec for the manuscript environment
```

## Input Matrix Format

The input file can be CSV or TSV. By default, DIMPLE-GWAS treats the first four columns as variant-level metadata and drops them before analysis; adjust this with `--drop_first_n_cols` if your file has a different layout.

After metadata columns are dropped, the remaining columns should be numeric feature/trait Z-score vectors and the rows should represent variants. The pipeline transposes this matrix internally, so HDBSCAN clusters features/traits based on their genome-wide Z-score profiles. Missing or non-numeric values in the analysis matrix are rejected.

## Pipeline Overview

DIMPLE-GWAS runs the following stages:

1. Read the input matrix, drop metadata columns, optionally apply Z-score preprocessing, and transpose to feature-by-variant orientation.
2. Generate a preliminary UMAP embedding for visualization.
3. Generate an ensemble UMAP embedding across `--n_random_states` random seeds for HDBSCAN input.
4. Run an HDBSCAN grid search and save candidate cluster solutions.
5. Select a cluster solution with the model-selection fit score.
6. Fit the selected HDBSCAN model, compute post-hoc cluster quality metrics, and export plots/tables.
7. Merge optional feature annotations into the UMAP/cluster output.

## Feature Annotation Files

A feature annotation file allows DIMPLE-GWAS to re-identify clustered features later (e.g., for plots, tables, and cluster interpretation). For historical neuroimaging examples, the bundled annotation file is named `IDP_KEY.csv`, but new analyses can pass any CSV via `--annotation_file`.

The only required column is the feature identifier column that matches the analyzed feature columns in the input matrix. By default this column is named `index`; use `--annotation_index_col` if your annotation file uses another name such as `metabolite_id`, `protein_id`, or `trait_id`.

All other annotation columns are preserved in the merged output. Useful optional columns include human-readable feature names, assay/platform labels, modality, tissue, pathway, metabolite class, or protein target metadata.

If you omit `--annotation_file`, the pipeline can still cluster, but downstream interpretation outputs will be less informative. The historical `--idp_key` argument is still accepted as an alias for `--annotation_file`.

---

## Z-Score Preprocessing

By default, DIMPLE-GWAS analyzes the input Z-score matrix as provided. For multiomic use cases such as metabolomics or proteomics, some traits may have a spike-and-slab pattern where a small number of very strong associations dominate the feature vector. In those cases, users can optionally apply rank-based inverse normal transformation (RINT) before UMAP:

```bash
python DIMPLEGWAS.py \
  --datainput "test_data/test_dat.csv" \
  --annotation_file "test_data/IDP_KEY.csv" \
  --zscore_transform rint
```

RINT is applied independently to each analyzed Z-score vector after metadata columns are dropped and numeric checks are complete, but before the matrix is transposed for DIMPLE-GWAS. Ties receive average ranks and the transformed vectors are mapped to standard normal quantiles. This attenuates extreme sentinel-style associations while preserving each vector's rank ordering.

The default is `--zscore_transform none`, which preserves the manuscript-style behavior.

---

## UMAP Ensemble

The ensemble UMAP stage repeats UMAP across multiple random seeds and horizontally concatenates the resulting embeddings. The default is `--n_random_states 1000`, matching the manuscript-style workflow. Users can increase this value, for example to `--n_random_states 10000`, if they have sufficient compute and memory.

Each repetition contributes `--n_components` columns to the HDBSCAN input. With the default `--n_components 3`, 1000 repetitions produce 3000 embedding columns, while 10000 repetitions produce 30000 columns. For quick tests, use a small value such as `--n_random_states 2`.

---

## Noise Handling

By default, DIMPLE-GWAS excludes HDBSCAN noise points (`label = -1`) from model-selection fit scoring and post-hoc cluster quality metrics. This keeps the default behavior aligned with HDBSCAN's strength: separating uncertain points from stable clusters.

Use `--fit_include_noise` to include noise points in the model-selection fit calculation. In that mode, the grid-search silhouette is computed with the noise label included, and the composite fit score includes the `Noise_points` penalty.

Use `--metrics_include_noise` to include noise points in the post-hoc metrics suite after the selected HDBSCAN solution is fit. The older `--silhouette_include_noise` option is still accepted as an alias for backward compatibility, but `--metrics_include_noise` is preferred.

---

## Fit Score and Cluster Quality Metrics

DIMPLE-GWAS keeps model selection and post-hoc diagnostics separate.

The model-selection fit score is used to rank HDBSCAN grid-search candidates. It combines silhouette average and number of clusters by default, rescales the final score so `0` is worst and `1` is best, and records the sorted candidate table in `stage03_optimized_cluster_solutions.csv`. If `--fit_include_noise` is set, the score also includes the `Noise_points` penalty.

The post-hoc metrics are computed after the selected HDBSCAN solution is fit. They include trustworthiness, continuity, silhouette, Calinski-Harabasz, Davies-Bouldin, and Dunn index. By default, these diagnostics exclude noise points; use `--metrics_include_noise` to include them. Use `--metrics_csv path/to/metrics.csv` to append a compact one-row metrics summary.

---

## HDBSCAN Grid Search

The default HDBSCAN grid search preserves the manuscript-style behavior by varying:

- `--grid_eps`
- `--grid_min_samples`
- `--grid_min_cluster_size`

Advanced users can also expand the grid over HDBSCAN cluster-extraction parameters:

- `--grid_cluster_selection_method eom,leaf`
- `--grid_cluster_selection_persistence 0.0,0.1`
- `--grid_alpha 1.0,1.2`
- `--grid_allow_single_cluster false,true`

The full grid is the product of all requested values. If the grid exceeds `--grid_max_evals`, DIMPLE-GWAS evaluates a reproducible random subset using `--random_state`. Configurations with fewer than two non-noise clusters are still skipped by the current fit score.

HDBSCAN distance geometry is intentionally fixed to Euclidean distance in this version so that clustering, silhouette scoring, and Euclidean post-hoc diagnostics remain aligned.

---

## Running the pipeline

Run `python DIMPLEGWAS.py --help` to see the definitive CLI options for your version.

### Example run (publication-style parameters)

From the repo root, you can run the bundled toy dataset with a fully specified parameter set (this is also a good template for real data):

```bash
python3 DIMPLEGWAS.py \
  --datainput "test_data/test_dat.csv" \
  --outdir output \
  --annotation_file "test_data/IDP_KEY.csv" \
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
  --dry-run
```

Remove `--dry-run` to execute the full pipeline.

---

## Main Outputs

By default, outputs are written under `--outdir`:

- `stage00_umap_preliminary.html`: preliminary UMAP visualization.
- `stage01_hdbscan_input.csv`: concatenated ensemble UMAP matrix used for HDBSCAN.
- `stage02_hdbscan_gridsearch_results.csv`: HDBSCAN grid-search candidates and diagnostics.
- `stage03_optimized_cluster_solutions.csv`: model-selection scores and selected parameter candidates.
- `stage03b_score_vs_clusters.html`: score-vs-cluster plot.
- `stage04_silhouette_vs_clusters.html`, `stage05_noise_vs_clusters.html`, `stage06_silhouette_vs_noise.html`: grid-search diagnostic plots.
- `stage07_silhouette_analysis.png`: silhouette analysis plot for the selected solution.
- `stage08_cluster_metrics.log`: run log and cluster quality metrics.
- `stage09_umap_vizdata_with_clusters.csv`: feature IDs, visualization UMAP coordinates, and HDBSCAN labels.
- `stage09b_umap_vizdata_with_annotations.csv`: optional annotation-enriched UMAP/cluster output.
- `stage10_cluster_solutions_3d.html`: interactive cluster solution plot when plots are enabled.

`stage11_modalities_3d.html` remains a legacy/reserved output path option from the neuroimaging workflow, but the current generalized pipeline does not write a separate modality-specific plot.

---

## Utility scripts

### 1) Generate a feature annotation file for a new dataset

The script `utility/generate_idp_key.py` can generate a simple feature annotation CSV containing:

- `index`
- `feature_name`
- `feature_category_name`

These columns are convenient but not mandatory for the main pipeline; the pipeline only requires the join column specified by `--annotation_index_col`.

Run:

```bash
python utility/generate_idp_key.py --help
```

Then sanity-check the output:

```bash
python - <<'PY'
import pandas as pd
p = "feature_annotations.csv"  # replace with your output path
k = pd.read_csv(p)
req = {"index"}
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
