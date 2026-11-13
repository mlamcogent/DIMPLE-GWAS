# Freeze 5.2 user manual

## Prepare a matrix

Supply a UTF-8 comma-separated table, optionally gzip-compressed. The digest covers the actual supplied file bytes, including compression if present. Both supported layouts produce the same ordered objects-by-features float64 matrix.

| Orientation | IDs | Numeric payload |
| --- | --- | --- |
| `objects_by_features` | Values in exactly one named ID column | Every other column, one object per row |
| `features_by_objects` | Header fields, one per object | Every row, one feature per row |

All headers and IDs must be unique, nonempty, printable, and free of leading or trailing whitespace. IDs are case-sensitive text. Leading zeroes, NA-like literals and Unicode are preserved. Use --drop-columns to remove explicitly named feature-name/metadata/label columns, or keep them in separate files. The declared object ID column must not be dropped. If an integer metadata column remains, the software has no semantic way to distinguish it from a feature.

There must be at least 51 objects and one feature. Rows must be rectangular and feature cells must be finite decimal numbers. Scientific notation and signs are accepted. Missing values, ragged rows, duplicate columns or IDs, NaN and infinities are refused. Decide any imputation, feature scaling or preprocessing outside DIMPLE and record it. The software performs no scaling, imputation or orientation guessing. Optional declared PCA/ICA uses the existing DIMPLE backend transforms. A constant, highly sparse, duplicate-heavy or inappropriate feature representation can still be scientifically unsuitable.

`bin/matrix_intake.py` accepts `--matrix`, `--orientation`, and a fresh `--output`. With row orientation supply `--object-id-column`. With column orientation omit it. Supply `--preprocessing none` or `--preprocessing external --preprocessing-record PATH`. Retain the external record privately. Its digest, the matrix digest, declared orientation, ID column, expected shape, scaling and missing-value policy enter the grid. Repeat intake after changing bytes or compression.

The synthetic example is available in both orientations. For the transposed file, run:

```bash
python3 bin/matrix_intake.py --matrix examples/synthetic-transposed.csv \
  --orientation features_by_objects --preprocessing none \
  --output .private/transposed-grid.json
```

## Plan the run

Use `bin/plan_batch.py --deployment PATH --matrix PATH --grid PATH --run-id NAME --output PATH`. Add `--policies PATH` for reviewed role policy fragments. Output filenames must be fresh. The planner validates the exact matrix and recipe again, writes local JSON, and prints shell-quoted commands. It does not contact AWS. Keep deployment and policy files private.

Required deployment keys come from `examples/deployment.example.json`. Use a commercial `region`, Batch `queue` name, immutable `image` repository plus SHA256 digest, distinct `job_role` and `execution_role` ARNs from the same account, `log_group` name, dedicated S3 `bucket` name without dots, and one lowercase `project_prefix` segment. `--run-id` is a fresh alphanumeric/hyphen segment; dated IDs such as `20261111T001700Z-digits` are accepted. The generated run root contains `input/matrix.csv`, `work/`, and `results/`. The stored object name is fixed even for gzip bytes, which the worker detects by content. Preserve a unique run root and the exact original S3 version and digest.

| Optional key | Default | Accepted integer range and purpose |
| --- | --- | --- |
| `seed_chunk` | 25 | 1–1000 seeds per task, with the same seeds and recipe |
| `queue_size` | 16 | 1–100 tasks managed at once by the executor |
| `task_hours` | 4 | 1–24 requested hours per task |
| `prepare_memory_gib`, `umap_memory_gib` | 4 each | 1–512 GiB per task |
| `concat_memory_gib`, `grid_memory_gib`, `rank_memory_gib` | 8 each | 1–512 GiB per task |

Every task requests one vCPU with numerical libraries limited to one thread. Default RAM is a starting configuration. Check available per-instance memory after ECS and OS reservations and leave room for dense arrays and work files. Each configuration stores a float32 ensemble of about `4 × N × 3000` bytes and a float64 distance matrix of about `8 × N²` bytes, plus temporary copies, per-candidate labels, repeated staging, and other overhead. The run has `173 + 9 × ceil(1000 / seed_chunk)` tasks, before failures. The input shape alone does not determine runtime or price. Calibrate from measured run timings and the approved deployment's current prices. The 5.1 digits timing evidence can guide this calibration when available.

The generated command supplies `--input`, `--grid`, `--outdir`, the owner AWS settings and `-work-dir`. For a staging-only invocation use `--prepare_only true` on a dedicated run root. The standard profile can run a local wiring check with `-stub-run`. The AWS profile expects the real worker and uses the CLI on the image's PATH for transport. Keep the image immutable between trials. [Nextflow AWS Batch executor](https://docs.seqera.io/nextflow/reference/executor/aws-batch/)

## Permissions and trust

| Identity | Purpose and scope |
| --- | --- |
| Stack administrator | Review and apply the specific CloudFormation changes. Keep this access separate from pipeline roles. |
| Batch service-linked role | Allow the AWS Batch service to manage its approved compute environment. |
| ECS EC2 instance profile | Allow ECS agent registration and instance service calls. No project data access. Follow the approved ECS instance role policy. |
| Task execution role | Trust ECS tasks. Allow stream creation and writes in the specific log group. For private ECR, allow `ecr:GetAuthorizationToken` as required by ECR, plus `BatchCheckLayerAvailability`, `GetDownloadUrlForLayer`, and `BatchGetImage` for the single approved repository. Review whether the ECS agent uses the execution role or needs the same scoped logging permission on the instance role. |
| Worker job role | Trust ECS tasks. Read the exact staged input and use the run's work prefix for task inputs and outputs. This is the only worker role with application S3 permissions. |
| Nextflow controller | Read staged input, manage the exact work and results prefixes, and submit to the named queue with Nextflow `nf-*` definitions. Restrict definition registration to the approved image digest and UID 10001, with privileged mode refused. Describe operations that require service scope are restricted to the selected region. PassRole is restricted to the two specified task roles. Job identifiers are dynamic, so cancel and terminate permissions use the regional account's job ARN pattern. Use a dedicated controller role and cancel only recorded IDs. |
| Input-ingest identity | Write the one run input object. Remove write access after ingest if required by your policy. |

Review the policy fragments against actual Nextflow, AWS account restrictions, repository and network rules before attachment. Existing explicit denies govern. CloudFormation enables IMDSv2 and uses an encrypted root disk with no inbound security group rules. Use trusted same-owner jobs on the dedicated EC2 environment. ECS containers share the host kernel. Confirm effective IMDS isolation, image trust, agent behavior and role identity during the authorized smoke test. Keep access keys and session tokens in the approved credential mechanism, outside all project files. [ECS task IAM roles](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html) · [Batch job definition permissions](https://docs.aws.amazon.com/batch/latest/userguide/iam-example-job-def.html)

The pinned Batch plugin adds `nextflow.io/createdAt` and `nextflow.io/version` when it registers a job definition. The controller policy allows those keys on the regional account's Nextflow job definitions and Batch job ARNs. Keep other tagging privileges separate. [AWS Batch tag-on-create](https://docs.aws.amazon.com/batch/latest/userguide/tag-resources.html)

## Read the results

| Path under run root | Contents |
| --- | --- |
| `metadata/pixels.npy` | Float64 objects-by-features array. The filename is retained for compatibility with the research stages. |
| `metadata/object_ids.csv`, `metadata/manifest.json` | Exact ordered IDs and source, grid, image, input and intermediate identities. |
| `configs/<config>/embeddings/<config>.embedding.npy` | Nine separate float32 matrices, each 3000 columns in ascending seed order. |
| `results/pooled_global_ranked.csv` | All 21,870 candidate rows, globally scored in one pool. |
| `results/<config>.grid_results.csv`, `results/<config>.within_config_ranked.csv` | Raw metrics and separately scored within-configuration rows. |
| `results/winners.csv`, `results/*.labels.csv` | Global winner, best eligible models by configuration under each score scope, and the original 30/0 baseline selection when eligible. Includes matching saved labels and model parameters. |
| `results/scoring.json`, `results/run_manifest.json` | Scoring weights, per-config eligibility outcomes, software versions, input and exact source identities, and completion status. |
| Local `evidence/<run>/attemptNN/` | Per-attempt trace, report, timeline and launcher logs; export privately after capture. |

The planner sets outdir to the run root; ranked files are under `<run-root>/results/`, metadata under `metadata/`, and per-config raw artifacts under `configs/`. Keep the sibling work prefix for chunked seeds, pairwise distances, candidate label shards, job logs and resume. These work files can be much larger than the summary. The rank task starts only after all 162 metric and label shards arrive. A configuration with no eligible candidate still has its full raw and ranked rows, with an explicit status and no winner for that scope. A fully evaluated pool with no eligible model produces `COMPLETE_POOL_NO_ELIGIBLE_CANDIDATE` and a header-only winners table. Missing, corrupt or inconsistent shards fail validation before ranking. Require controller success and verify the expected file set before interpreting published files.

## Optional label-based evaluation

After selecting winners, put a separate CSV with exact `object_id` text and one nonempty target column alongside the result files. Use `python bin/research.py evaluate --truth TRUTH.csv --results PATH --output FRESH.csv` with the same scientific dependencies. It checks exact ID membership and one-to-one alignment and reports adjusted Rand, adjusted mutual information, and coverage, both overall and among assigned objects as applicable. Truth labels do not enter the main workflow. Use a new output path for each evaluation.

## Troubleshoot

- **Input refused**. Verify orientation, header uniqueness, data type and hashes, and recreate a grid after intentional changes. For gzip, keep the exact compressed bytes between preflight and upload.
- **No job starts**. Check the queue state, available x86_64 capacity, RAM and vCPU match, and registry or endpoint access. CloudWatch and Batch status reasons help distinguish permissions, provisioning and image failures.
- **Staging fails**. Check the image's CLI on PATH, worker job role and exact S3 prefixes, TLS routes, bucket policy, and logs. Run the one-job staging check with a new run ID after changes.
- **A task exceeds time, disk or memory**. Preserve work and evidence. Review trace and AWS job details. For resource-only RAM/time/concurrency changes, retain the same scientific grid, run root, work directory, input and image; resume the same session as a fresh attempt directory. Record changed resource settings. Scientific/input changes require a new run.
- **Resume schedules work again**. Check controller launch directory, cache/session, exact work prefix, params, staged input and image. Deep caching and artifact identity checks protect the result lineage.
- **No eligible model**. Review silhouette, noise, feature quality and the fixed parameter search. A valid calculation can yield no defensible clustering.

## Missing values and scaling

Before intake, choose and document an analysis-appropriate missing-data policy: remove affected rows/features or impute using a justified method. Check that all remaining feature values are finite. If scaling is required, perform it upstream on the declared feature axis and retain its method/fit provenance; DIMPLE never guesses or silently imputes/scales. Do not use truth labels to choose preprocessing. Pass `--preprocessing external --preprocessing-record record.json` to retain a digest of the upstream record, otherwise `--preprocessing none`.

## Named columns and explicit orientation

For SNP×IDP CSV containing `snp_id,IDP1,IDP2,...`, cluster IDPs with `--drop-columns snp_id --orientation features_by_objects`; to cluster SNPs, use `--object-id-column snp_id --orientation objects_by_features` without dropping that identifier. Drop probe/PRS label columns by exact name. No orientation or label guessing occurs. All remaining cells must be numeric.

Dropping a column during intake **does not redact the uploaded source CSV**: all original file bytes are uploaded and hashed. If labels, identifiers or metadata must stay local, remove them from the cloud-bound file before intake and retain the mapping/truth locally.

## Pseudonymising participant IDs

Replace participant identifiers locally with unique stable pseudonyms before upload; use a securely generated random identifier or keyed mapping, not a plain hash of predictable IDs. Preserve a one-to-one map in a separate access-controlled local location. Never include the map, names or original IDs in the source package, cloud inputs, logs or published artifacts. Check duplicate/missing IDs before and after replacement. Results preserve ordered object_id text, so rejoin pseudonyms to the original IDs locally only after analysis, using a validated one-to-one join. Pseudonymisation is not anonymisation: feature values and linked metadata can still identify people. Follow the dataset's consent, governance and approved cloud handling requirements.

## Scientific settings in one config

Pass a science-only JSON file with `matrix_intake.py --config science.json`. Omitting it selects the unchanged published nine-UMAP ×1,000-seed recipe and original HDBSCAN grid. Unknown top-level/nested keys are errors; settings are expanded and recorded as resolved_science in the run manifest. Source recipe and scoring implementation remain unchanged.

Existing DIMPLE names are used:
- `backend`: `umap` (default), `pca`, or `ica`. PCA/ICA are existing standalone representation backends, not an implicit PCA→ICA→UMAP chain. They use the existing validated implementations and cluster that representation.
- `umap`: n_neighbors, min_dist, n_components, metric, spread, learning_rate, repulsion_strength, negative_sample_rate, local_connectivity, set_op_mix_ratio, random_state, densmap. Values/ranges expand the requested UMAP configuration grid.
- `execution`: n_random_states and legacy_ensemble_seeds. Seed chunk size remains a deployment/resource setting, not a scientific seed count.
- `hdbscan`: min_samples, min_cluster_size and cluster_selection_epsilon grid values; existing estimator controls (also scalar/list/range grids) cluster_selection_method, cluster_selection_persistence, alpha, allow_single_cluster, max_cluster_size and metric. Historical grid_eps, grid_min_samples and grid_min_cluster_size aliases are also accepted without duplicate definitions.
- `pca`: variance_threshold or retained_components.
- `ica`: variance_threshold or retained_components, seed, tol, max_iter, plot_components, pairplot_components (existing controls). Do not send controls for inactive backends.

Small explicit custom UMAP example (software test only, not the default scientific search):
```json
{"umap":{"n_neighbors":5,"min_dist":0.1,"n_components":2,"densmap":false},"execution":{"n_random_states":2},"hdbscan":{"min_samples":[2],"min_cluster_size":[5,10],"cluster_selection_epsilon":[0,0.25]}}
```
PCA: `{"backend":"pca","pca":{"retained_components":2},"hdbscan":{"min_samples":[2],"min_cluster_size":[5],"cluster_selection_epsilon":[0]}}`. ICA uses backend `ica` and section `ica` with retained_components2, seed42, tol0.0001 and max_iter1000. No automatic retries or fallback on nonconvergence.

Changing scientific settings creates a new scientific run. Candidate cardinality, expected shards and representation dimensions follow the resolved settings rather than fixed3,000D checks. Pooled scoring code is unchanged. Silhouette scoring retains the existing Euclidean-on-representation convention even if a different HDBSCAN fitting metric is requested; interpret cross-setting comparisons accordingly.
