# Provenance

Freeze 3 was assembled on 2026-08-20 in Asia/Singapore from a clean copy of the modular Freeze 2 implementation. No source directory contained Git metadata, so file-level SHA-256 identities and the external `freeze3_workspace` audit bundle are the authoritative lineage record.

| Role | Absolute source path | Policy |
|---|---|---|
| Authoritative implementation base | `/Users/maxlam/Downloads/Cogent-analysis-audit/DIMPLE-GWAS/DIMPLE-GWAS-freeze2` | Copied selectively into a clean source tree |
| Historical dev evidence | `/Users/maxlam/Downloads/Cogent-analysis-audit/DIMPLE-GWAS/DIMPLE-GWAS-dev` | Inspected; monolith not distributed |
| Cluster prototype evidence | `/Users/maxlam/Downloads/Cogent-analysis-audit/DIMPLE-GWAS/cluster-optimization` | Inspected; only allowlisted general interpretation concepts reimplemented |
| Original IDP evidence | `/Users/maxlam/Downloads/Cogent-analysis-audit/DIMPLE-GWAS/umap-hdbscan` | Read-only reconstruction evidence |
| Target | `/Users/maxlam/Downloads/Cogent-analysis-audit/DIMPLE-GWAS/DIMPLE-GWAS-freeze3` | Freeze 3 release-candidate source |
| Audit bundle | `/Users/maxlam/Downloads/Cogent-analysis-audit/DIMPLE-GWAS/freeze3_workspace` | Inventories, reports, logs, comparisons, manifests, and handoff |

## Selected identities

| Artifact | SHA-256 |
|---|---|
| Freeze 2 `pyproject.toml` | `b4f5a08337e97c0b6c030631232bc8e0316393478363b76c0be8a40ffded100b` |
| Freeze 2 `dimple_gwas/cli.py` | `b36293198a03100eaca86d26a5e5aa7f0c3ac8662e9f5c0b0573dd41235da51f` |
| Freeze 2 `dimple_gwas/pipeline.py` | `40718e8eda29b527d5f9292e2d90f749a1c5a41ac69aaa98675da4f7df2b62bf` |
| Exact 164-IDP input, `test_data/test_dat.csv` | `0cc17db052e28e3c1cd7600f7140f9b929b9e2d2a5b4f9ded3ebf4df3e032f96` |
| IDP annotation key, `test_data/IDP_KEY.csv` | `b664e6139e18305168327c5420c1a1af8379312f3ce0645f5f42dbcc394febc4` |

The complete source-release file manifest, with hashes and sizes, is generated at `freeze3_workspace/handoff/11_freeze3_file_manifest.tsv`. Broader upstream inventories and checksums are in `freeze3_workspace/inventories/` and `freeze3_workspace/source_maps/`.

## Derivation policy

- Generic input, preprocessing, repeated UMAP, contrib-HDBSCAN, candidate evaluation, and legacy-score behavior remain derived from Freeze 2.
- Freeze 3 adds a post-selection interpretation layer, exact-ID comparison and validation commands, spreadsheet input support, deterministic visualization outputs, and stronger provenance manifests.
- Interpretation never refits topology, changes membership, or contributes to model ranking.
- The sklearn soft-target experiment, dataset-specific target penalties, prototype source files, historical monolith, Dockerfile, prior outputs, virtual environments, and caches are excluded from the distributable source.
- No default cluster-count, noise, largest-cluster, pQTL, IDP, or visual target is present in ranking.

## Runtime provenance

Run manifests record the normalized input/config hashes, command, deterministic seeds, package source digest, Python/platform/package versions, timestamps, candidate/status counts, runtime, and selected model. Selected files are bound to hashes and byte sizes. `dimple-gwas validate` independently verifies the declared output schemas, counts, and hashes.

The source tree is versioned `3.0.0rc1`. The RC designation is deliberate: unit/integration/regression tests and historical adapter concordance are complete, while a fresh full 1,000-seed original-IDP rerun, Linux/container qualification, security scanning, registry publication, and cloud execution remain downstream gates.
