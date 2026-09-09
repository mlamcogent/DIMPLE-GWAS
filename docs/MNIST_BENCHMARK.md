# MNIST Benchmark

The reproducible benchmark lives in `benchmarks/mnist/` and uses OpenML `mnist_784` version 1: 70,000 samples and 784 pixels. Pixel values are divided by 255. Digit labels are not passed to UMAP, HDBSCAN, search construction, scoring, or winner selection.

## Protocol

Two predeclared UMAP families are fit once each. Five named HDBSCAN configurations cover the historical pQTL-inspired restriction, dev baseline, EOM, leaf, and unrestricted maximum size. A 96-candidate search crosses both UMAP families with HDBSCAN size, density, epsilon, selection-method, and maximum-size controls. The expanded winner is selected with `legacy_dimple` before digit labels are converted for evaluation.

Full silhouette is quadratic in sample count, so the benchmark uses the same fixed-seed 2,000-point cap for every candidate and records sampling explicitly. DBCV is disabled for this large comparison. Required post-hoc metrics use all 70,000 labels: ARI, NMI, homogeneity, completeness, and V-measure treat noise as label `-1`; weighted purity uses only clustered samples.

## Verified results

| Configuration | Clusters | Noise fraction | Weighted purity | ARI | NMI | Largest cluster |
|---|---:|---:|---:|---:|---:|---:|
| Jibin historical report | 140 | 0.7382 | 0.9829 | NA | NA | NA |
| Representative pQTL-inspired rerun | 1,394 | 0.5437 | 0.9720 | 0.0019 | 0.3250 | 263 |
| Dev-compatible baseline | 3,281 | 0.3023 | 0.9687 | 0.2193 | 0.4291 | 7,971 |
| EOM, restrictive max | 440 | 0.6882 | 0.9709 | 0.0018 | 0.2877 | 257 |
| Leaf, unrestricted | 493 | 0.7206 | 0.9700 | 0.0008 | 0.2665 | 221 |
| EOM, unrestricted | 8 | 0.0032 | 0.6026 | 0.5436 | 0.7660 | 21,088 |
| Expanded legacy-score winner | 1,541 | 0.5776 | 0.9720 | 0.0016 | 0.3097 | 93 |

The expanded winner was primary UMAP + leaf, `min_cluster_size=10`, `min_samples=3`, epsilon 0, and `max_cluster_size=300`. Maximum size has no effect for leaf selection; the otherwise identical unlimited candidate tied and stable model ID broke the tie.

The realized legacy weights were 0.999716 for cluster count and 0.000284 for silhouette because the formula combines native-unit dynamic ranges; noise was excluded by the default profile. This result is backward-compatible but scientifically illustrates why scoring objectives must be declared and inspected.

## Interpretation

Weighted purity measures local homogeneity only among retained samples. The high-purity solutions are severely fragmented and reject 54–72% of samples, while their all-sample ARI is near zero. The unrestricted EOM solution recovers broader class structure (NMI 0.7660, completeness 0.9083) with little noise but only eight clusters, one of which contains 21,088 samples. Neither is automatically the correct topology; they express different trade-offs.

## Reproduction

```bash
python benchmarks/mnist/run_benchmark.py \
  --config benchmarks/mnist/benchmark_config.yaml \
  --output-dir benchmarks/mnist/outputs \
  --data-home benchmarks/mnist/data
```

Verified runtime was 273.47 seconds on macOS arm64 with Python 3.12.13, UMAP 0.5.12, contrib-HDBSCAN 0.8.44, and scikit-learn 1.9.0. The manifest, full expanded table, named results, and six retained label arrays are under `benchmarks/mnist/outputs/`.

