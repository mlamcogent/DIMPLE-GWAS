# Tutorial 5 — Original 164-IDP analysis

## Track A — Historical reconstruction

Status: **historical/adapted evidence, not a fresh fit**.

The authoritative record contains 164 IDPs: 102 historical HDBSCAN-noise assignments and five non-noise clusters of 9, 13, 15, 14, and 11. The historical published solution used epsilon 0, min-samples 4, and min-cluster-size 6 and was manually selected from sorted row 16. Preserve the historical workbook/table and label checksums, rescore/adapt without overwriting, and report exact/permutation-invariant concordance separately.

## Track B — Fresh 1,000-seed protocol

Status: **deferred until the Docker image is created, by coordinator direction**.

The later authorized workflow must:

```bash
dimple-gwas inspect-config \
  --search-mode custom \
  --config configs/original_idp_164_historical_search.yaml

dimple-gwas show-search-space \
  --search-mode custom \
  --config configs/original_idp_164_historical_search.yaml \
  --output-dir /new/output/mount/164_preflight

dimple-gwas run \
  --search-mode custom \
  --config configs/original_idp_164_historical_search.yaml \
  --input /read-only/input/mount/AUTHORITATIVE_164_MATRIX \
  --output-dir /new/output/mount/164_full_run
```

The placeholders must be replaced only after checking authoritative input checksum, permissions, storage, memory, threads, and candidate count. No fresh labels, runtime, or comparison metric is claimed in this edition. Do not tune a new configuration after viewing resemblance to the historical labels.
