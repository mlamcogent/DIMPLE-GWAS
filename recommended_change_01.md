## Summary

- **Add `matplotlib>=3.7` to `requirements.txt`** — `matplotlib` is imported in `DIMPLEGWAS.py` (used for the silhouette analysis plot) but was missing from `requirements.txt`, causing `ImportError` for pip-only installs.
- **Add a minimal `Dockerfile`** — based on `python:3.11-slim`, installs all deps from `requirements.txt` and sets `DIMPLEGWAS.py` as the entrypoint. Useful for HPC/container environments where native UMAP/HDBSCAN deps are difficult to install.

## Test plan

- [ ] `pip install -r requirements.txt` in a fresh venv succeeds (matplotlib now included)
- [ ] `docker build -t dimple-gwas .` builds successfully
- [ ] `docker run dimple-gwas --dry-run --datainput test_data/test_dat.csv --idp_key test_data/IDP_KEY.csv` runs the dry-run smoke test
- [ ] Existing `python DIMPLEGWAS.py` workflows are unaffected

See also: issue with broader recommendations for pre-release cleanup (linked separately).