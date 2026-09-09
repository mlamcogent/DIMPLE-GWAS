# Original 164-IDP reproduction

## Recovered contract

The local `test_data/test_dat.csv` is byte-identical to the preserved historical pipeline input (SHA-256 `0cc17db052e28e3c1cd7600f7140f9b929b9e2d2a5b4f9ded3ebf4df3e032f96`). It contains 86,885 variant rows, four metadata columns, and 164 exact IDP vector columns. `test_data/IDP_KEY.csv` has SHA-256 `b664e6139e18305168327c5420c1a1af8379312f3ce0645f5f42dbcc394febc4`.

The executed historical notebook used no additional preprocessing; it transposed columns after the first four. It concatenated 1,000 three-dimensional DensMAP embeddings for seeds 1–1,000 with 30 neighbours, zero minimum distance, Euclidean defaults, and no PCA. HDBSCAN used contrib `hdbscan`, EOM, Euclidean defaults, `min_samples=4`, `min_cluster_size=6`, and epsilon 0 for the published five-cluster solution.

The historical search was epsilon 0/1/2 × min samples 2–19 × minimum cluster size 5–49. Its score included noise. The published solution was explicitly selected from sorted row 16 instead of the top-scoring two-cluster candidate. That human choice is preserved only in `configs/original_idp_164_selected.yaml`; `configs/original_idp_164_historical_search.yaml` represents the full recovered population.

## Known historical output

The final membership contains 164 IDs: 102 noise, and five clusters of 9, 13, 15, 14, and 11. Workbook annotations name them:

1. Resting State Unimodal–heteromodal (9)
2. Resting State Visual + inter-hemispheric (13)
3. Resting State cortico-cerebellar (15)
4. Resting State DMN + intra-network (14)
5. Resting State motor (11)

## Validated commands

Inspect the full historical search without fitting:

```bash
dimple-gwas show-search-space --search-mode custom \
  --config configs/original_idp_164_historical_search.yaml --show-first 0
```

Pending fresh selected-model run:

```bash
dimple-gwas run --search-mode fixed \
  --config configs/original_idp_164_selected.yaml \
  --output-dir outputs/original_idp_164_selected_1000seed
```

Then explain and compare the retained result against the immutable historical table. Always use new output directories.

## Current evidence status

Freeze 3 independently reproduced the historical raw scores and score-tie groups for all 333 retained 164-IDP model rows to below `1e-15`; it applies stable model-ID ordering within ties. It also ingested the immutable labels with complete exact IDs and generated the original-space similarity/heatmap package. This is recovered-output concordance, not a fresh 1,000-seed clustering reproduction.

The final workbook lacks one third visualization-coordinate cell for `IDP_2143`; the current historical explanation therefore uses the two complete coordinates for projection diagnostics while using all 86,885 original dimensions for similarity.

A fresh 1,000-seed run is pending because one local one-seed fit took about 11 seconds end-to-end; serial scale is approximately three hours before full comparison, and aggressive parallelism risks memory pressure on a 16 GB host. Numerical library versions also differ from the historical Python 3.9 environment. Run it as a pre-specified controlled validation, not as an interactive parameter-selection exercise.
