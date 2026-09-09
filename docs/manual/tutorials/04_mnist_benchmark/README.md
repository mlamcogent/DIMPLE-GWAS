# Tutorial 4 — MNIST benchmark (historical evidence track)

Status: **documented historical benchmark; not freshly rerun in this manual build**.

Use `benchmarks/mnist/MNIST_BENCHMARK_REPORT.md`, `docs/MNIST_BENCHMARK.md`, `benchmarks/mnist/benchmark_config.yaml`, and `benchmarks/mnist/run_benchmark.py` as the source set. Verified prior outputs exist in the broader Freeze 3 evidence workspace. Do not download a new dataset or overwrite those outputs during a documentation verification.

Before a future Docker rerun:

1. verify the dataset source, licence, checksum, split, and preprocessing;
2. inspect the benchmark configuration and candidate count;
3. set bounded threads and a new output mount;
4. record environment, command, timestamps, seeds, labels, known-label metrics, runtime, and hashes;
5. compare outputs using structural metrics and numerical tolerances;
6. state that MNIST is engineering evidence, not biological validation.

The prior full benchmark runtime was 273.47 seconds in its recorded environment. It is not a universal resource estimate.
