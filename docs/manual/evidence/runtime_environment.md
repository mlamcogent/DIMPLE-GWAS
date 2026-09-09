# Runtime environment

- Evidence recorded: `2026-08-25T13:37:18.969706+00:00`
- Operating system/platform: `macOS-26.5.1-arm64-arm-64bit`
- Architecture: `arm64`
- Isolated Python: `3.12.13`
- Package: DIMPLE-GWAS `3.0.0rc1`
- Package-source SHA-256: `df87825992ab51dc016c673cf420a978ba5c161bd6c755e00a5199ead310e65b`
- Input SHA-256 for executed synthetic tutorials: `77d1956fd074da9d82ce0d6a9c896446895a5e22b2fc6da85417169d13b9bb01`
- Reducer backend: `umap-learn`
- Clusterer backend: `hdbscan.contrib`
- Tutorial thread settings: `n_jobs=1`, `candidate_jobs=1`, `core_dist_n_jobs=1`
- Test thread caps: `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `NUMBA_NUM_THREADS=1`
- Dependency integrity: `pip check` exit `0`
- Fresh pytest: exit `0`, duration `54.30` seconds

## Installed scientific stack

| Package | Exact version |
| --- | --- |
| `Pillow` | `12.3.0` |
| `PyYAML` | `6.0.3` |
| `hdbscan` | `0.8.44` |
| `joblib` | `1.5.3` |
| `matplotlib` | `3.11.1` |
| `numpy` | `2.5.2` |
| `openpyxl` | `3.1.5` |
| `pandas` | `3.0.5` |
| `plotly` | `6.9.0` |
| `pyarrow` | `25.0.1` |
| `scikit-learn` | `1.9.0` |
| `scipy` | `1.18.1` |
| `umap-learn` | `0.5.12` |
| `xlrd` | `2.0.2` |


## Reproducibility boundary

These versions and checksums identify the executed macOS/Apple-Silicon environment. They do not guarantee bitwise equality on Linux, another architecture, another BLAS/OpenMP implementation, or a future Docker image. The Docker phase should reuse the exact source/checksum manifest and record any platform-dependent tolerance.
