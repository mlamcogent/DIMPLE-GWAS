# Native and cloud handoff — NOT RUN

No cloud resource was accessed or provisioned. Resolve local acceptance blockers first.
Use a native Linux AMD64 host for canonical qualification; ARM emulation is separate.
Runtime/config digest: `sha256:a5543cdaacaa3c9e8027df8e846a1352832ef2da3fe224df3be9cd465ea7ef03`.
Runtime OCI manifest: `sha256:b93e26512bba759d1f8162a69bded041ba8fe6cfe4452a64f4532f6fac7cb116`.
This is a local OCI digest, not an observed registry digest. No remote digest exists.

The portable Docker archive is782327296 bytes; independent compressed OCI archive is
248457728 bytes. Verify the run's archive manifests and after loading verify image ID.
Start the bounded fixture with2vCPU,6GiB RAM and2GiB tmpfs, using BUILD_AND_RUN.md's exact
helper command. Store input read-only and export every output and validation status.
Repeat native runs against the same sealed fixture hashes and criteria, retaining
CPU/BLAS/platform metadata; compare per-seed geometry and label/noise identities.

For a future full164 run,8vCPU/32GiB RAM and at least20GiB plus input/output storage are
initial planning allowances, not measured requirements or performance promises. First
benchmark a short separate seed run natively; full1000 timing/memory remain unknown.
No cost estimate is meaningful until provider, region, machine and runtime are selected.

The exact input SHA256 is0cc17db052e28e3c1cd7600f7140f9b929b9e2d2a5b4f9ded3ebf4df3e032f96;
annotation SHA256 b664e6139e18305168327c5420c1a1af8379312f3ce0645f5f42dbcc394febc4.
The selected config uses densMAP3D, neighbors30,1000 seeds1..1000 concatenated into3000
columns, no RINT/PCA, HDBSCANmin_cluster_size6/min_samples4/epsilon0/EOM.

After separate authorization and native pilot, the full application command is:

```sh
dimple-gwas run --input /data/input/original_idp_164.tsv \
  --config /data/input/original_idp_164_selected.yaml --search-mode fixed \
  --output-dir /data/output/fresh-164
dimple-gwas validate --run-dir /data/output/fresh-164
```

Input basename is an explicit destination convention, not an assertion about the
current research filename. Supply verified files through approved read-only mounts;
never embed them in an image. Run `docker/scripts/run_164_idp_protocol.sh --plan` for
all prerequisites. Preserve failures, order, per-seed blocks and separate native/GCP/AWS
results; do not force retained cluster counts or label alignment to pass thresholds.
