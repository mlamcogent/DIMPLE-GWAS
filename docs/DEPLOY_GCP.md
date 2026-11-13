# Freeze 5.3 GCP deployment: owner terminal sheet

This is the GCP route in the same AWS + GCP package. Science, intake, scoring, recipe and workflow are unchanged. These are instructions, not evidence that resources have been created or a live GCP task has passed. No GCP changes, image build or publication were performed to prepare this package.

## Quick GCP test
1. On a durable controller install Java 21, Nextflow 26.10.3/nf-google 1.29.1, Python and Google CLI; arrange ADC.
2. Set your PROJECT, BUCKET and REGION, verify billing/quotas, and create missing SA/bucket with the two commands below.
3. Review and run the prerequisites script; confirm worker roles, regional repository and Private Google Access.
4. Copy the published image to your regional mirror using section 2; inspect UID/WORKDIR and record its digest.
5. Copy the GCP deployment example, replace every placeholder and set the verified mirror digest.
6. Run synthetic matrix intake and plan locally using section 3.
7. Execute the emitted upload command, then launch PREPARE-only from the durable controller as in section 4.
8. Require task success, 60×3 metadata, private VM and GCS read/write checks; this is not scientific acceptance.

## 1. Confirm the target and approve prerequisites

Choose your own billing-enabled project, regional default VPC/subnet and suitable quotas. Budget alerts are not spending caps and do not stop jobs. Check regional and project-wide CPU limits before launch.

Use the project **ID**, not the display name, in commands. Run from the extracted package on an approved durable Linux controller with Java 21, Nextflow 26.10.3, nf-google 1.29.1, Python 3.9+, Google CLI and valid Application Default Credentials. Preserve its launch directory and cache. CLI login alone does not establish Nextflow ADC. Use an attached identity or approved `gcloud auth application-default login`; do not create service-account keys. The controller needs internet access for Nextflow/plugin downloads; the private workers use Google endpoints only.

```bash
set -euo pipefail
kit="$(pwd -P)"
export PROJECT=YOUR_PROJECT_ID REGION=asia-southeast1
export BUCKET=YOUR_BUCKET_NAME REPOSITORY=dimple
# Run prerequisites as an administrator; no launcher grants are installed.
gcloud projects describe "$PROJECT" --format='yaml(projectId,name,projectNumber)'
gcloud billing projects describe "$PROJECT" --format='yaml(projectId,billingEnabled)'
gcloud services list --enabled --project="$PROJECT" --format='value(config.name)'
gcloud compute regions describe "$REGION" --project="$PROJECT" --format='yaml(quotas)'
gcloud compute project-info describe --project="$PROJECT" --format='yaml(quotas)'
gcloud compute networks subnets describe default --region="$REGION" --project="$PROJECT"
```

Success: project ID/name, billingEnabled=true and quotas and the regional default subnet match the reviewed target. Allow for other running workloads and the controller within your project-wide CPU limit. Stop if the target or quotas differ.

Prerequisite: enable Batch, Artifact Registry and IAM APIs with `gcloud services enable batch.googleapis.com artifactregistry.googleapis.com iam.googleapis.com --project="$PROJECT"` before the fresh-resource commands.

For a fresh setup only, after approval create the named service account and bucket with these two commands. Skip each command if that resource already exists. No lifecycle is installed:

```bash
gcloud iam service-accounts create dimple-batch-sa --display-name='DIMPLE Batch worker' --project="$PROJECT"
gcloud storage buckets create "gs://$BUCKET" --project="$PROJECT" --location="$REGION" --uniform-bucket-level-access --public-access-prevention
```

Review `deploy/gcp-prerequisites.sh`. It reuses the existing `dimple-batch-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com` and `gs://YOUR_BUCKET_NAME`; absent resources are a stop, not a reason to invent replacements. After explicit owner approval:

```bash
bash "$kit/deploy/gcp-prerequisites.sh" --apply
```

Only Batch, Artifact Registry and IAM APIs are enabled by this script. It does not enable Cloud Resource Manager or add launcher roles; the operator must already have the required administrator permissions. Worker grants are batch.agentReporter and logging.logWriter on the project, artifactregistry.reader on the regional repository, and storage.objectAdmin on this bucket only. It creates the regional `dimple` repository only if absent and enables Private Google Access. No service-account keys are created. The existing bucket lifecycle is never changed: inspect your actual policy before launch. Verify that policy before launch; durable `results/` must not be targeted. Batch service-agent roles belong only to the Google-managed service agent.

Success checks (inspect role memberships, repository location and retention, not just command exit):

```bash
SA="dimple-batch-sa@${PROJECT}.iam.gserviceaccount.com"
PN="$(gcloud projects describe "$PROJECT" --format='value(projectNumber)')"
AGENT="service-${PN}@gcp-sa-cloudbatch.iam.gserviceaccount.com"
gcloud iam service-accounts describe "$AGENT" --project="$PROJECT"
gcloud projects get-iam-policy "$PROJECT" --flatten='bindings[].members' \
  --filter="bindings.members:serviceAccount:$AGENT" --format='table(bindings.role)'
# Require roles/batch.serviceAgent on this Google-managed identity; stop if absent.
gcloud projects get-iam-policy "$PROJECT" --flatten='bindings[].members' \
  --filter="bindings.members:serviceAccount:$SA" --format='table(bindings.role)'
gcloud iam service-accounts get-iam-policy "$SA" --project="$PROJECT"
gcloud storage buckets describe "gs://$BUCKET" --project="$PROJECT" --format=json
gcloud storage buckets get-iam-policy "gs://$BUCKET" --project="$PROJECT"
gcloud artifacts repositories describe "$REPOSITORY" --location="$REGION" --project="$PROJECT"
gcloud artifacts repositories get-iam-policy "$REPOSITORY" --location="$REGION" --project="$PROJECT"
gcloud compute networks subnets describe default --region="$REGION" --project="$PROJECT" --format='value(privateIpGoogleAccess)'
```

PGA must be True. It reaches Google APIs, Cloud Storage and Artifact Registry, **not Docker Hub**. The profile sets `google.batch.usePrivateAddress=true`, no external worker IPs and no Spot/preemptible VMs. Leave the default route/DNS and required egress to Google services available; custom firewall/DNS policies need review. Review your firewall: use IAP-only SSH if needed and disable RDP unless explicitly required. This package makes no firewall changes; it does not re-verify those live rules. No SSH/RDP ingress is required for Batch.

## 2. Make the approved image reachable privately

The published worker image is `docker.io/zymlam/dimple-gwas-f5:5.3.0-research-multicloud.2-gcpfix02@sha256:4398934e14aded2b5ec2c891f39a2d0f559522cf276799997a49f4a45c24a383`. It is linux/amd64, UID10001, WORKDIR `/tmp`. GCP live qualification remains pending. Copy the public image from an internet-connected Docker host to your own regional Artifact Registry; private workers have no internet and cannot pull Docker Hub directly.

```bash
SOURCE_IMAGE='docker.io/zymlam/dimple-gwas-f5:5.3.0-research-multicloud.2-gcpfix02@sha256:4398934e14aded2b5ec2c891f39a2d0f559522cf276799997a49f4a45c24a383'
DEST="$REGION-docker.pkg.dev/$PROJECT/$REPOSITORY/dimple-gwas-f5:5.3.0-research-multicloud.2-gcpfix02"
gcloud auth configure-docker "$REGION-docker.pkg.dev"
docker pull --platform linux/amd64 "$SOURCE_IMAGE"
docker image inspect "$SOURCE_IMAGE" --format '{{.Architecture}} {{.Config.User}} {{.Config.WorkingDir}}'
# Require amd64, 10001 and /tmp before continuing.
docker tag "$SOURCE_IMAGE" "$DEST"
docker push "$DEST"
gcloud artifacts docker images describe "$DEST" --project="$PROJECT" --format='value(image_summary.digest)'
```

Use the returned full regional `.../dimple/dimple-gwas-f5@sha256:...` reference in your deployment JSON. Verify the mirror digest; do not assume a tag or a cross-registry digest proves image identity. Private Google Access reaches Google APIs, GCS and Artifact Registry, not the public internet.

## 3. Prepare locally and plan

Use synthetic data for the first billable PREPARE check. For real input, the user states orientation and removes private columns locally. Dropping a column during intake **does not redact the uploaded source CSV**: all original file bytes are uploaded and hashed. If labels, identifiers or metadata must stay local, remove them from the cloud-bound file before intake and retain the mapping/truth locally. Missing values/scaling are handled before intake as documented in MANUAL.md; no guessing.

```bash
umask 077
mkdir -p "$kit/.private"
matrix="$kit/examples/synthetic-matrix.csv"
grid="$kit/.private/gcp-grid.json"
python3 "$kit/bin/matrix_intake.py" --matrix "$matrix" \
  --orientation objects_by_features --object-id-column object_id \
  --preprocessing none --output "$grid"
cp "$kit/examples/deployment.gcp.example.json" "$kit/.private/gcp-deployment.json"
# Replace YOUR_PROJECT_ID and YOUR_BUCKET_NAME throughout the example; set your verified mirror digest.
# Unedited placeholders are deliberately rejected by the planner.
python3 "$kit/bin/plan_gcp.py" --deployment "$kit/.private/gcp-deployment.json" \
  --matrix "$matrix" --grid "$grid" --run-id gcp-staging-20261111-01 \
  --output "$kit/.private/gcp-params.json"
```

Success: LOCAL_PLAN_ONLY, expected SHA256/shape, correct project/region/service account, regional AR digest and scratch/input under `gs://bucket/work/run-id/` and durable output under `gs://bucket/results/run-id/`. Planner prints exact upload, run and prepare commands; it does not execute them. If planning on the Mac, copy the package and private grid/deployment/input to the durable controller by your approved transfer route, then regenerate parameters there so local absolute paths are correct. Do not upload evaluation labels.

Profile defaults: fixed `n2-standard-4` (4 vCPU/16 GB) and at most **six active jobs per Nextflow controller**, default six, so nominal worker allocation is at most 24 vCPU per controller. Tasks still use their unchanged 1-CPU scientific settings. Eight-GB tasks have headroom on a 16-GB VM. Requested queue_size above six is clamped. This is **not** a project-wide hard vCPU cap: concurrent controllers, other jobs or brief teardown overlap can exceed the nominal allocation. Run only one controller at a time and leave quota headroom. Your project-wide quota may be the tighter limit; budgets do not enforce the bound. No GPU or Spot quota is required. Resource requests larger than the fixed machine can fit must not be launched without a reviewed profile change.

## 4. Approved PREPARE smoke, then run

After approval, execute the exact emitted `upload_command` and record its GCS object generation:

```bash
input_uri="gs://$BUCKET/work/gcp-staging-20261111-01/input/matrix.csv"
gcloud storage objects describe "$input_uri" --project="$PROJECT" --format=json
mkdir "$kit/.private/gcp-controller"
cd "$kit/.private/gcp-controller"
set -C
nohup python3 "$kit/bin/launch_attempt.py" --profile gcp \
  --params "$kit/.private/gcp-params.json" --attempt-dir "$kit/.private/gcp-controller/evidence/prepare01" \
  --prepare-only > prepare01.nohup.log 2>&1 < /dev/null &
```

Success: launcher exit receipt 0; Batch task terminal SUCCEEDED; metadata/pixels.npy, object_ids.csv and manifest.json exist with synthetic **60×3** shape and expected input hash. Confirm actual VM has no external IP, n2-standard-4/on-demand, worker identity, image pull, UID10001 GCS read/write and local scratch. GCS mounts map UID/GID10001 using the existing profile flags; these remain subject to live transport qualification.

```bash
gcloud batch jobs list --project="$PROJECT" --location="$REGION"
# Use only a job ID recorded by this run's controller.
gcloud batch jobs describe "$recorded_job_id" --project="$PROJECT" --location="$REGION"
gcloud compute instances list --project="$PROJECT" --format='table(name,machineType,networkInterfaces[].accessConfigs[].natIP)'
gcloud storage ls "gs://$BUCKET/results/gcp-staging-20261111-01/metadata/"
```

Then prepare a fresh approved digits/scientific run with a new run ID/input/grid/plan/controller directory, and use the emitted `run_command` without `--prepare-only`, with a new attempt log. Do not silently reduce the published nine-config×1000-seed recipe. PCA and ICA remain explicit standalone alternative science configs; see MANUAL.md. A successful PREPARE is not full workflow/scientific acceptance. Require all expected tasks, pooled output and run manifest, then evaluate held-out labels separately. No claim about the 2,315-trait matrix follows from this smoke.

## 5. Resume, stop and retain evidence

For resource-only adjustments retain input, science, source identity, profile, work prefix and the **actual scientific run's original** launch directory/cache, not the smoke controller. Set the following paths and UUID from that run's original launch receipt. The attempt directory must be new:

```bash
: "${RUN_CONTROLLER_DIR:?Set the scientific run original launch directory}"
: "${RUN_PARAMS:?Set that same scientific run original params JSON}"
: "${SESSION_UUID:?Set that scientific run verified Nextflow session UUID}"
cd "$RUN_CONTROLLER_DIR"
set -C
nohup python3 "$kit/bin/launch_attempt.py" --profile gcp \
  --params "$RUN_PARAMS" --attempt-dir "$RUN_CONTROLLER_DIR/evidence/attempt02" \
  --resume "$SESSION_UUID" > attempt02.nohup.log 2>&1 < /dev/null &
```

Any existing `work/` cleanup policy limits resume: do not assume cached tasks survive expiry. Durable outputs, including metadata and the workflow's results subfolder, remain below `results/<run>/`; no results lifecycle is installed here. Re-plan only new runs using this corrected path layout; never silently relocate an already-started run's scratch.

Retain `--prepare-only` for a smoke-only resume. Cross-cloud cache migration is not supported. For an approved stop, verify Nextflow PID, command and start time in the attempt receipt, stop that controller, confirm it is no longer submitting, then identify **all exact owned Batch jobs**, including retries/pending jobs. After inspecting each job, cancel only those:

```bash
gcloud batch jobs delete "$recorded_job_id" --project="$PROJECT" --location="$REGION"
```

Success: owned jobs terminal/deleted and worker VMs/disks drained. Do not bulk-delete project jobs. Preserve unique attempt traces/reports/timelines, controller logs, job descriptions, output checksums and source/image/input identities. Export only reviewed evidence with owner approval, under the durable results prefix without changing the existing bucket policy. Estimate costs separately from billed costs; VMs, disks, logs, images and storage may continue charging after a controller stops. AWS-only runner_stack.py/export_evidence.py/stop_run.py must not be used for GCP.

References: [Nextflow Google Batch](https://www.nextflow.io/docs/latest/google.html), [Batch private networking](https://cloud.google.com/batch/docs/create-run-job-no-external-access), [Batch permissions](https://cloud.google.com/batch/docs/permissions). Pinned nf-google 1.29.1 maps usePrivateAddress to the Batch API noExternalIpAddress field; it is not named noExternalIpAddress in Nextflow config.
