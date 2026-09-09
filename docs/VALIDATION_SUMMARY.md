# Validation summary

Date: 2026-08-20. Platform: macOS arm64, Python 3.12.13.

## Clean package gates

- Editable install from `pyproject.toml`: pass.
- `pip check`: no broken requirements.
- Full tests: 45 passed, 0 failed, 0 skipped, 0 expected failures.
- Existing Freeze 2 tests retained: 20/20 passed.
- All command help screens and seven shipped YAML configurations parse.
- Fixed synthetic/fixture run: complete, one successful model, no failed candidates.
- Run validation: 24 checks passed, no warnings/failures.

Expected runtime warnings are UMAP's deterministic-seed `n_jobs=1` notice, a macOS physical-core detection fallback, and the intentional constant-vector correlation warning test.

## Scientific regression

- Runtime trap: no pre-UMAP reducer call; UMAP received the complete prepared matrix.
- Independent legacy score reproduction: maximum absolute difference zero in the synthetic audit.
- Fresh Freeze 2 versus Freeze 3 fixed run: same model ID; byte-identical labels; exact IDs/order; ARI 1; NMI 1; noise Jaccard 1; Procrustes disparity approximately `5.8e-32`.
- Historical 2,315-IDP score population: 2,430/2,430 rows rescored; max raw-score difference below `1e-15`; score-tie group ranks identical.
- Historical 164-IDP score population: 333/333 retained rows rescored; max raw-score difference below `1e-15`; score-tie group ranks identical.

The historical notebooks assigned the same minimum rank to tied scores. Freeze 3 preserves those tie groups while assigning a reproducible unique order within each tie by stable model identifier.
- Historical 164-IDP adapter: 164/164 exact IDs, zero exclusions, five clusters/102 noise retained exactly, ARI/NMI/noise Jaccard 1 against the emitted order table.

## Boundary

No fresh 1,000-seed original-IDP reclustering, Docker build, Linux test, security scan, registry publish, or cloud run was performed. See `KNOWN_ISSUES.md` and `ORIGINAL_IDP_REPRODUCTION.md`.
