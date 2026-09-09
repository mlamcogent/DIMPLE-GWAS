# Lab 0 - Environment and CLI inspection

**Evidence status:** freshly executed in Stage 1; safe to repeat locally.

**Purpose:** establish software identity and map analyst tasks to current commands before touching data.

**Working directory:** `DIMPLE-GWAS-freeze3/`.

Run:

```bash
python -m dimple_gwas --version
python -m dimple_gwas --help
python -m dimple_gwas run --help
python -m dimple_gwas inspect-config --help
python -m dimple_gwas show-search-space --help
python -m dimple_gwas score-existing --help
python -m dimple_gwas summarize-models --help
python -m dimple_gwas reproduce-model --help
python -m dimple_gwas explain --help
python -m dimple_gwas compare --help
python -m dimple_gwas validate --help
```

Stage 1 observed version `3.0.0rc1`; all help surfaces exited zero. Record Python, operating system, architecture, and package versions. Confirm that the package source digest matches the Stage 1 identity if the source is expected to be unchanged.

**Decision checkpoint:** if the version or source digest differs, do not apply Stage 1 numeric expectations until the affected checks are rerun.

**Reflection:** classify `validate`, `compare`, and `explain` as artifact integrity, structural comparison, or retained-result description. None is a biological-validation command.

\newpage
