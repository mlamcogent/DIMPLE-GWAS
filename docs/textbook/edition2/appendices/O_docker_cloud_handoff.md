# Appendix O — Docker and cloud handoff

Status: protocol for the next authorised stage. This manual build did **not** create a Dockerfile, image, registry, cloud resource, bucket, credential, or deployment workflow.

## Package identity

- Software: DIMPLE-GWAS Freeze 3 RC1 `3.0.0rc1`.
- Package-source SHA-256 observed in the executed manifests: `df87825992ab51dc016c673cf420a978ba5c161bd6c755e00a5199ead310e65b`.
- Git commit/tag: unavailable in the supplied snapshot. Establish a versioned source identity before packaging and reconcile it byte-for-byte with `evidence/04_source_checksums.tsv`.
- Dependency inputs: `pyproject.toml`, `requirements.txt`, and the executed `evidence/resolved_dependencies.txt`. The latter is an environment record, not by itself a portable lockfile.
- Entry point: `dimple-gwas`; module equivalent: `python -m dimple_gwas`.

## Image design constraints

- Use a minimal supported Python base and a non-root runtime user.
- Install from the versioned source identity; do not embed research inputs, historical workbooks, tutorial outputs, credentials, or secrets.
- Use read-only source/input/config mounts and a separate writable output mount.
- Set a predictable working directory and preserve CLI exit status.
- Record OS/base digest, architecture, Python, resolved packages, numerical libraries, BLAS/OpenMP/Numba settings, CPU/memory limits, and package-source hash.
- Produce an SBOM, vulnerability-scan result, image digest, and later signature/attestation under the organisation's approved process. A clean scan is a separate gate from scientific validation.

## Smoke-test fixture

Use the repository-owned synthetic fixture:

- input: `benchmarks/synthetic/synthetic_matrix.tsv`;
- annotations: `benchmarks/synthetic/synthetic_annotations.csv`;
- config: `docs/textbook/edition2/labs/01_fixed_synthetic/tutorial_config.yaml`;
- expected enumeration: one candidate;
- expected structural result: 24 unique IDs, three non-noise clusters of eight, zero failed candidates, complete manifest, present annotation join;
- expected validation: all run-contract checks pass.

Use a new container output mount. Run `inspect-config`, `show-search-space`, `run`, `validate`, `reproduce-model`, `compare`, and `explain`. Compare exact schemas/IDs/parameters/counts and permutation-invariant labels; use tolerances/alignment for floating-point values and coordinates.

## Full 164-IDP contract

- Search protocol: `configs/original_idp_164_historical_search.yaml`.
- Selected historical parameters: `configs/original_idp_164_selected.yaml`.
- Repeats: verified configuration value of 1,000, with three components per repeat and the historical seed-sequence setting.
- The authoritative raw matrix must be selected and SHA-256-verified before launch; mount it read-only and do not copy it into the image or logs.
- Preflight must record matrix dimensions/metadata prefix/ID set, candidate count (theoretical standard HDBSCAN grid 2,430), free storage, memory limit, CPUs, threads, and output permissions.
- Use a new output directory. No parameter may be tuned after viewing resemblance to the historical labels.
- Preserve every candidate row, failure/invalid row, resolved configuration, run/model-selection manifests, retained labels/summaries, logs, environment, and hashes.

Track A historical expectations are comparison targets, not fresh-run promises: 164 IDs, 102 historical noise assignments, five clusters of 9/13/15/14/11, and the disclosed manual sorted-row-16 selection (epsilon 0, min-samples 4, min-cluster-size 6). Report exact label equality separately from ARI, NMI, noise-set Jaccard, mapped membership, and coordinate comparison. One historical `UMAP_3` value is missing; labels are complete.

## Resource and threading evidence

- Current fresh tutorials: macOS arm64, Python 3.12.13; Tutorial 2 used four UMAP families, two repeats, 32 candidates, one UMAP/candidate job, and approximately 10.713 manifest seconds.
- Historical MNIST full runtime: 273.47 seconds in its recorded environment/configuration.
- Prior Freeze 3 note: a 16-GB host warrants caution against unrestricted parallel UMAP fitting.
- No fresh 164-IDP 1,000-seed runtime/memory benchmark exists. Do not derive cloud sizing by naive linear extrapolation from the small fixture.
- Profile the container with bounded fixtures/pilots first. Avoid nested oversubscription; record `n_jobs`, `candidate_jobs`, HDBSCAN core-distance jobs, and `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`, and `NUMBA_NUM_THREADS`.

## Platform matrix

Execute the same versioned image digest and mounted checksums on:

1. local Docker on the reference Mac;
2. Linux Docker on a controlled x86_64 host;
3. the chosen GCP CPU/memory/storage class;
4. the chosen AWS CPU/memory/storage class.

For every platform retain command, image digest, host metadata, start/end/runtime, limits, exit status, warnings/failures, manifests, output checksums, and comparison/validation reports. Cloud objects must use least privilege, encryption, restricted network/access logging, lifecycle rules, and no public ACLs.

## Comparison rules

| Artifact/property | Rule |
| --- | --- |
| Source, image, input, config | Exact SHA-256 identity |
| Schemas, required files, IDs, candidate counts/ordinals, parameters, statuses | Exact equality |
| Cluster labels | Exact equality reported; also ARI/NMI/mapped membership and noise-set Jaccard |
| Floating-point metrics | Predeclared absolute/relative tolerances; investigate rank changes near ties |
| Embedding/display coordinates | Procrustes/alignment plus predeclared tolerance; never require raw axis/sign identity alone |
| Score/rank | Exact formula/profile/population; compare realized weights and tie order; investigate numeric boundary changes |
| PNG/HTML | Compare source data, dimensions, label/legend presence, and visual rendering; byte identity is supplementary |
| Logs | Required events/status/counts present; timestamps and paths are expected to differ |
| Runtime/memory | Descriptive platform evidence, not equality targets |

Dependency pinning does not guarantee bitwise equality across operating systems, architectures, CPUs, BLAS/OpenMP, thread schedules, or numerical libraries.

## Cross-platform pass/fail criteria

Call Freeze 3 cross-platform validated only after:

- the image identity/security/SBOM gates pass;
- every synthetic smoke test and artifact validation passes on every target platform;
- exact schemas, IDs, enumeration, parameters, statuses, and required artifacts agree;
- label and numeric comparisons meet predeclared criteria, with all differences explained;
- the fresh full 164-IDP run completes on the approved platform and is compared transparently with the historical record;
- failures/warnings and platform-specific deviations are resolved or accepted in a signed release record;
- no protected input or secret is embedded or disclosed.

Recommended next action: establish the versioned source identity, author the minimal non-root Docker package from the checksum-verified tree, execute the fixed synthetic smoke/validation matrix, profile a bounded scientific pilot, and only then authorize the fresh 164-IDP 1,000-seed run.
