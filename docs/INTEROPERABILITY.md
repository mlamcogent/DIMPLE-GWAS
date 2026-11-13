# Freeze 5.3 AWS + GCP interoperability

## One package, two execution profiles

Freeze 5.3 adds GCP to the portable 5.2 architecture; it does not replace AWS. Both `awsbatch` and `gcp` select the same `main.nf`, research/scoring/intake/configuration and representation modules, default recipe, dependency lock and output schema. `gcp` uses native Nextflow `google-batch` with `nf-google@1.29.1`; AWS uses native `awsbatch` with `nf-amazon@3.12.1`. There is no new custom broker, execution ledger or provider-specific scientific fork.

Use [DEPLOY.md](DEPLOY.md) for AWS and [DEPLOY_GCP.md](DEPLOY_GCP.md) for GCP. The shared [MANUAL.md](MANUAL.md) describes numeric CSV input, matrix orientation, labels, scoring and result interpretation. Provider-specific credentials, permissions, network resources, registries and object storage remain owner supplied.

| Shared contract | AWS adapter | GCP adapter |
| --- | --- | --- |
| Validated matrix + SHA256 and resolved scientific grid | S3 input object | GCS input object |
| Same workflow and scientific source | AWS Batch executor | Google Batch executor |
| Immutable Linux amd64 scientific worker | Approved registry digest | Same approved digest where accessible, or verified mirror |
| Separate per-run work and results | S3 prefixes | GCS prefixes |
| Durable Nextflow controller + session | AWS identity and role passing | ADC and worker service-account use |
| Same resource intent and numerical thread limits | AWS instance capacity/queue | GCP regional capacity/Batch placement |
| Native logs and accounting | CloudWatch/AWS billing | Cloud Logging/GCP billing |

An image digest shared across providers is preferred, but does not by itself establish working staging or identical hardware behavior. Verify both provider transports in the final image/runtime. The inspected Nextflow 26.10.3 native Google Batch route uses Batch GCS mounts/gcsfuse with local scratch, rather than gsutil inside the worker; no additional Google CLI in the shared scientific image is required by that route. Confirm the pinned nf-google@1.29.1 matches the inspected release, and test UID 10001 mount/scratch permissions and GCS access live. Cloud capacity, machine type, billing granularity, storage and network costs differ.

## Scientific invariants

With no `--config`, the nine UMAP configurations remain the approved expanded parameter grid, not a replacement for repeated seeds. Each configuration uses 1000 seeds with 3 dimensions per seed, producing its own 3000-dimensional ensemble and HDBSCAN search. The nine ensembles do not become one 27,000-dimensional clustering input. The 21,870 raw candidate rows are pooled for global scoring/ranking, with separately identifiable within-configuration ranking outputs. Seed chunking changes scheduling, not the scientific seed count.

The shared configurable route uses `matrix_intake.py --config science.json`. UMAP parameters, seed counts and HDBSCAN grids may be explicitly changed; `backend: pca` or `backend: ica` selects an existing standalone representation backend, not a chained preprocessing step. Both clouds resolve and execute these settings through the same modules. Candidate counts and representation dimensions follow the resolved config for custom runs. The published default recipe and pooled-scoring implementation remain unchanged. Silhouette retains its existing Euclidean-on-representation convention even if another HDBSCAN fit metric is selected; cross-setting comparisons require scientific judgment.

Explicit named-column intake is shared too. Use `--orientation`, the applicable `--object-id-column`, and `--drop-columns NAME [NAME ...]` (repeatable) rather than guessing column roles. The object ID column cannot be dropped. All retained features must be numeric. Excluding a column from fitting is not redaction: the original CSV is uploaded. Remove sensitive or truth columns from the actual cloud-bound file before intake when those data must stay local. Truth must never influence fitting or model selection; use retained local truth only for post-selection evaluation. Record external preprocessing and preserve ordered object identity. No implicit scaling, imputation, orientation inference or provider-specific search reduction is allowed.

This candidate incorporates frozen 5.2 `5.2.0-research-portable.3`, source archive SHA256 `6d801729b033185e5f97df794d0e12e8b1aedf324fc283c6ea311aba8b6cdaa0`. Earlier images are stale for these source changes. No replacement image build or cloud qualification is implied or authorized by this source update; a newly approved matching build and qualification are required before either deployment route is accepted.

## What interoperability does not promise

- It is not transparent cross-cloud job migration or Nextflow cache/resume. Start a new run ID/work prefix when changing providers.
- It is not identical wall-clock performance, costs, VM availability or automatic failover.
- It does not promise bitwise-identical floating-point outputs across CPU/platform changes. Compare agreed tolerances, object alignment, seed/config coverage, raw metrics, eligibility, selected parameters and labels; investigate differences.
- It does not turn passed software checks into scientific validation or release approval.

## Required evidence before team acceptance

1. **Offline package checks:** both profiles render; both planners reject invalid input/settings and create shell-quoted upload and durable-attempt commands; named-column exclusion, default compatibility, custom UMAP and standalone PCA/ICA contracts are checked; shared science hashes match the adopted 5.2 baseline or documented fixes; local stub and resume cover workflow wiring.
2. **Image/runtime checks:** pinned Linux amd64 build, scientific imports/dependencies, non-root staging/write permissions, AWS and Google transport support, provenance and immutable digest. Record each result, not merely the Dockerfile's intent.
3. **One real PREPARE per provider:** image pull, exact matrix hash, expected object/feature shape, metadata publication and job completion.
4. **Matched real pilot:** identical dataset/grid/scientific source and comparable numerical runtime on AWS and GCP, task/candidate accounting against that run's resolved configuration (including a complete default-recipe qualification where claimed), no label leakage, global score output and post-selection truth evaluation if available.
5. **Measured operational comparison:** actual timings, peak resources, failure/retry history and billed costs, with provider/account/region/date and known accounting delays.
6. **Team sign-off:** separate software operational acceptance, scientific assessment and public-release approval. No public repository or registry publication is implied by local package assembly.

The imported Cursor GCP 0.7.0 material was an offline custom-bridge candidate, not a validated live deployment. Its transport/resource lessons may inform this native route; its historic test counts do not validate this package. See current package validation notes for evidence actually obtained.

## Durable attempts and provider-specific operations

Both providers use `bin/launch_attempt.py` with explicit `--profile awsbatch` or `--profile gcp`, a private parameter file and a fresh `--attempt-dir`. Run it under the guide's `nohup` pattern on a durable controller. Keep the controller working directory/cache stable; resume with an explicit session UUID but a new attempt directory. Resource-only changes must be recorded; changed science or input requires a new scientific run. Trace, report, timeline and logs are unique local attempt artifacts and are not overwritten.

Both planners set the output directory to the run root. The published layout uses `metadata/`, `configs/<config>/embeddings/`, `configs/<config>/grid/`, and a single `results/` suffix, alongside `input/` and `work/`. Evidence is exported separately under `evidence/` after review.

The deployment repairs in [DEPLOY_FIXES.md](DEPLOY_FIXES.md) include AWS-only `runner_stack.py`, `export_evidence.py` and `stop_run.py`; those helpers must not be used for GCP. GCP operators collect native job/log evidence, upload it with `gcloud storage cp`, and cancel only identified run jobs with `gcloud batch jobs delete` after stopping submissions. These differing operations do not change the shared scientific contract.
