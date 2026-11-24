# Deployment repair notice

Read DEPLOY_FIXES.md first: it supersedes the older launch, identity, capacity and evidence commands below.

# Freeze 5.3 deployment sheet

Run the local sections from an extracted, verified release. Sections marked **AWS** require your own authorization and can create costs. Keep the `.private` directory, run data, configuration, and logs out of GitHub and Docker Hub.

Commands are marked **Workstation** (your machine, with the AWS CLI) or **Controller (SSM)** (the bootstrap instance). Planning, CloudFormation, and the matrix upload run on the workstation. Staging the kit, rewriting the grid path, and launching Nextflow run on the controller, through:

```bash
# Workstation
aws ssm start-session --region "$region" --target "$controller_id"
```

Then work as `ec2-user` on the published AL2023 AMI (`sudo -iu ec2-user` if the session is `ssm-user` or root).

## 1. Local prerequisites and input

**Workstation.** Use Java 21 and Nextflow 26.10.3 with `nf-amazon@3.12.1` on a durable controller. Use Python 3.9+ for planning and an existing AWS CLI v2 for the later owner-operated AWS steps. Choose a commercial AWS region and a registry digest for a Linux x86_64 worker built from this source. See the worker checklist in [RELEASE.md](RELEASE.md).

```bash
kit="$(pwd -P)"
umask 077
mkdir -p "$kit/.private"
matrix="$kit/examples/synthetic-matrix.csv"
grid="$kit/.private/smoke-grid.json"
python3 "$kit/bin/matrix_intake.py" --matrix "$matrix" \
  --orientation objects_by_features --object-id-column object_id \
  --preprocessing none --output "$grid"
```

For a local Nextflow wiring check, keep all paths local and use a fresh output directory. The 182-task shape below uses one seed chunk per configuration, with all scientific commands replaced by stubs.

```bash
mkdir -p "$kit/.private/stub-controller"
cd "$kit/.private/stub-controller"
nextflow -C "$kit/nextflow.config" run "$kit/main.nf" -stub-run \
  -work-dir "$kit/.private/stub-work" --outdir "$kit/.private/stub-out" \
  --input "$matrix" --grid "$grid" --seed_chunk 1000
```

**Check before continuing:** intake wrote the grid file, and the optional stub run finished without touching AWS.

## 2. AWS network, IAM and cost review

Have the AWS owner confirm the account, region, quotas, and budget. You can either deploy `deploy/bootstrap.yaml` (Step 0) or supply an existing network and roles. Private subnets must be in one VPC, with public IP assignment off, and approved outbound HTTPS for S3, ECR or your chosen registry, ECS/Batch agent services, and CloudWatch Logs. Confirm DNS, image-pull reachability, and instance capacity. Docker Hub pulls need an approved registry egress route and may be subject to rate limits. If using private ECR, prepare separate repository-scoped pull permissions.

If you are not using Step 0, provide an existing Batch service-linked role, an EC2 ECS instance profile, a task job role with trust for `ecs-tasks.amazonaws.com`, and a separate execution role with that trust. Keep data permissions off the instance profile and execution role. Review existing SCPs, permissions boundaries, endpoint policies, and explicit denies with the AWS owner. Use temporary credentials or a role on the controller. Maintain a separate authorized input-ingest identity.

The batch stack creates a private versioned SSE-S3 bucket, HTTPS-only bucket policy, no-ingress worker security group, IMDSv2/encrypted-disk launch template, managed on-demand Batch compute environment, disabled queue, and retained CloudWatch log group. The template sets zero minimum vCPUs. Batch's allocation strategy can exceed the configured maximum by one instance. Review RAM headroom per instance, disk capacity, and monitoring for compute, NAT, data transfer, logs and retained S3 versions. [AWS Batch compute resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-batch-computeenvironment-computeresources.html)

The published `deploy/batch.yaml` default for MaxVcpus is 24. Do not change the published default; pass MaxVcpus explicitly to fit your quota, and consider setting it to 0 while the queue is idle.

A NAT gateway, its public IPv4 address, and the controller disk keep billing after the controller is stopped. Delete the bootstrap stack only after a reviewed teardown plan, and only after any needed controller snapshot.

## 3. Step 0: deploy bootstrap.yaml (network + controller)

**Workstation.** This stack creates a VPC, NAT gateway, S3 gateway endpoint, SSM-only controller, Batch service-linked role if missing, worker instance profile, job role, and execution role. Resource names follow the CloudFormation stack name. Choose a unique stack name and an unused /16 for VpcCidr (default 10.72.0.0/16) that does not overlap any VPC in the account or any network you peer or connect with. A parallel test stack should use a different prefix and CIDR, for example `dimple-network-test` with `10.73.0.0/16`.

Set `WorkerStackName` to the exact name you will use for the batch stack in the next step. Leave `RunnerProfileName` empty until a run-scoped runner stack exists. Leave `ControllerAmi` empty to resolve the current public AL2023 x86_64 AMI from SSM; to avoid later instance replacement, record that AMI after create and pass it as `ControllerAmi` on every update.

```bash
# Workstation
region=ap-southeast-1
account="$(aws sts get-caller-identity --query Account --output text)"
bootstrap_stack=dimple-network
workers_stack=dimple-workers
runner_stack=dimple-runner
vpc_cidr=10.72.0.0/16

aws cloudformation deploy --region "$region" --stack-name "$bootstrap_stack" \
  --template-file "$kit/deploy/bootstrap.yaml" --capabilities CAPABILITY_IAM \
  --no-execute-changeset \
  --parameter-overrides \
    WorkerStackName="$workers_stack" \
    VpcCidr="$vpc_cidr" \
    ControllerType=t3.medium \
    ExpectedRegion="$region" \
    ExistingBatchServiceRoleArn="arn:aws:iam::${account}:role/aws-service-role/batch.amazonaws.com/AWSServiceRoleForBatch"
```

If the account does not already have the Batch service-linked role, omit `ExistingBatchServiceRoleArn` and let the stack create it. Review the change set, then execute that exact change set with the AWS owner (`aws cloudformation execute-change-set --region "$region" --change-set-name "$reviewed_change_set_arn"`). Creation can take up to 30 minutes while the controller compiles Python 3.11.11 and installs Nextflow 26.10.3. Wait for `CREATE_COMPLETE` and `BOOTSTRAP_OK` on the controller.

Read the outputs you will pass to `batch.yaml` (`VpcId`, `PrivateSubnets`, `BatchServiceRoleArn`, `InstanceProfileArn`) and keep `JobRoleName`, `JobRoleArn`, `ExecutionRoleArn`, and `ControllerId` for the runner and launch steps. Also record the controller AMI so later updates can pin it:

```bash
# Workstation
aws cloudformation describe-stacks --region "$region" --stack-name "$bootstrap_stack" \
  --query 'Stacks[0].Outputs'
controller_id="$(aws cloudformation describe-stacks --region "$region" --stack-name "$bootstrap_stack" \
  --query 'Stacks[0].Outputs[?OutputKey==`ControllerId`].OutputValue' --output text)"
controller_ami="$(aws ec2 describe-instances --region "$region" --instance-ids "$controller_id" \
  --query 'Reservations[0].Instances[0].ImageId' --output text)"
```

**Check before continuing:** the stack is `CREATE_COMPLETE`, the controller reports `BOOTSTRAP_OK` and is reachable over SSM, and you have recorded the outputs plus `$controller_id` and `$controller_ami`.

## 4. AWS create the reviewed batch stack

**Workstation.** In an authenticated owner shell, fill these variables from the Step 0 outputs or from approved existing AWS resources. Use a dedicated stack name short enough for the Batch queue and log group, and set it to the same value as `WorkerStackName` above. Pass `MaxVcpus` explicitly and leave the queue `DISABLED` until you are ready to launch. (`$kit` is the extracted release path from section 1.)

```bash
# Workstation
vpc_id="$(aws cloudformation describe-stacks --region "$region" --stack-name "$bootstrap_stack" \
  --query 'Stacks[0].Outputs[?OutputKey==`VpcId`].OutputValue' --output text)"
subnet_ids_csv="$(aws cloudformation describe-stacks --region "$region" --stack-name "$bootstrap_stack" \
  --query 'Stacks[0].Outputs[?OutputKey==`PrivateSubnets`].OutputValue' --output text)"
batch_service_role_arn="$(aws cloudformation describe-stacks --region "$region" --stack-name "$bootstrap_stack" \
  --query 'Stacks[0].Outputs[?OutputKey==`BatchServiceRoleArn`].OutputValue' --output text)"
instance_profile_arn="$(aws cloudformation describe-stacks --region "$region" --stack-name "$bootstrap_stack" \
  --query 'Stacks[0].Outputs[?OutputKey==`InstanceProfileArn`].OutputValue' --output text)"
job_role_name="$(aws cloudformation describe-stacks --region "$region" --stack-name "$bootstrap_stack" \
  --query 'Stacks[0].Outputs[?OutputKey==`JobRoleName`].OutputValue' --output text)"

aws cloudformation deploy --region "$region" --stack-name "$workers_stack" \
  --template-file "$kit/deploy/batch.yaml" --no-execute-changeset \
  --parameter-overrides VpcId="$vpc_id" PrivateSubnets="$subnet_ids_csv" \
    BatchServiceRoleArn="$batch_service_role_arn" InstanceProfileArn="$instance_profile_arn" \
    MaxVcpus=24 RootVolumeGiB=80 InstanceTypes=m6i.2xlarge QueueState=DISABLED
```

Review the reported change set, IAM context, subnet route settings, launch template, and cost estimate. Execute that exact change set with the AWS owner using the console or `aws cloudformation execute-change-set --region "$region" --change-set-name "$reviewed_change_set_arn"`. Wait for completion and inspect outputs.

Copy `examples/deployment.example.json` to `$kit/.private/deployment.json` and fill it from the stack outputs. `queue`, `bucket`, `log_group`, and `region` come from the workers stack (`QueueName`, `Bucket`, `LogGroup`, `Region`). `job_role` and `execution_role` are the bootstrap outputs `JobRoleArn` and `ExecutionRoleArn`. `image` is a reviewed digest URI for a worker built from this source; see [RELEASE.md](RELEASE.md). A filled file looks like this, with your values in place of the placeholders:

```json
{
  "region": "$region",
  "queue": "dimple-workers-jobs",
  "image": "registry.example/dimple@sha256:DIGEST",
  "job_role": "arn:aws:iam::$account:role/dimple-network-JobRole-XXXXXXXX",
  "execution_role": "arn:aws:iam::$account:role/dimple-network-ExecutionRole-XXXXXXXX",
  "log_group": "/dimple/dimple-workers/jobs",
  "bucket": "dimple-workers-runbucket-xxxxxxxxxxxx",
  "project_prefix": "research",
  "seed_chunk": 25,
  "queue_size": 16,
  "task_hours": 4,
  "prepare_memory_gib": 4,
  "umap_memory_gib": 4,
  "concat_memory_gib": 8,
  "grid_memory_gib": 8,
  "rank_memory_gib": 8
}
```

Verify that the queue, both roles, and the bucket belong to the intended deployment. Record the workers outputs you will need later:

```bash
# Workstation
bucket="$(aws cloudformation describe-stacks --region "$region" --stack-name "$workers_stack" \
  --query 'Stacks[0].Outputs[?OutputKey==`Bucket`].OutputValue' --output text)"
log_group="$(aws cloudformation describe-stacks --region "$region" --stack-name "$workers_stack" \
  --query 'Stacks[0].Outputs[?OutputKey==`LogGroup`].OutputValue' --output text)"
# QueueName and Region also fill deployment.json (queue, region).
```

**Check before continuing:** the workers stack is `CREATE_COMPLETE`, the queue is `VALID` and `DISABLED`, and `.private/deployment.json` is filled and private.

## 5. Plan, runner stack, attach, enable, upload, stage, and one-job check

Do these substeps in order. 5.1 is local only. 5.2–5.5 are AWS commands on the workstation, each reviewed before execute. 5.6–5.7 run on the controller. An enabled queue still costs nothing until jobs are submitted, because the compute floor is 0 vCPUs.

### 5.1 Plan the run and render the runner stack

**Workstation.** The planner does not contact AWS. It writes a parameter file whose `grid` path is an absolute path on this machine, and it prints an upload command and a launch command. Use the upload command in 5.5. Do not paste the printed launch command on the workstation; launch runs on the controller after 5.6 rewrites the grid path.

```bash
# Workstation
python3 "$kit/bin/plan_batch.py" --deployment "$kit/.private/deployment.json" \
  --matrix "$matrix" --grid "$grid" --run-id staging-check-01 \
  --output "$kit/.private/smoke-params.json" --policies "$kit/.private/smoke-policies.json"
```

Check the exact source digest, run ID and S3 prefixes. The policies file contains separate policy objects for this run only. **Generate a fresh runner stack from those fragments. Do not reuse a hand-edited ResearchRun or job-role policy from an earlier run.**

```bash
# Workstation
python3 "$kit/bin/runner_stack.py" --policies "$kit/.private/smoke-policies.json" \
  --output "$kit/.private/runner-stack.json"
```

**Check before continuing:** the planner printed `LOCAL_PLAN_ONLY`, and `runner-stack.json` was just generated from this run's policies.

### 5.2 Create the runner stack

**Workstation.**

```bash
# Workstation
aws cloudformation deploy --region "$region" --stack-name "$runner_stack" \
  --template-file "$kit/.private/runner-stack.json" --capabilities CAPABILITY_IAM \
  --no-execute-changeset --parameter-overrides JobRoleName="$job_role_name"
```

Review and execute that change set. The stack adds a runner role, a runner instance profile, and a work-prefix policy on the job role. These are IAM-only. See [permissions and trust](MANUAL.md#permissions-and-trust) for instance registration, optional ECR pull, logs, and Batch role passing.

**Check before continuing:** the runner stack is `CREATE_COMPLETE`.

### 5.3 Attach the runner profile to the controller

**Workstation.** Point the controller at the new instance profile with a bootstrap stack update that restates every parameter from the original bootstrap deploy (including whether you set or omitted `ExistingBatchServiceRoleArn`), pins the running controller AMI, and sets `RunnerProfileName` to the profile **name**, not the ARN. (The association-swap alternative is in [DEPLOY_FIXES.md](DEPLOY_FIXES.md).) If you omit `ControllerAmi`, CloudFormation may resolve a newer AL2023 AMI and replace the controller.

```bash
# Workstation
runner_profile_name="$(aws cloudformation describe-stack-resources --region "$region" \
  --stack-name "$runner_stack" --logical-resource-id RunnerProfile \
  --query 'StackResources[0].PhysicalResourceId' --output text)"
controller_ami="$(aws ec2 describe-instances --region "$region" --instance-ids "$controller_id" \
  --query 'Reservations[0].Instances[0].ImageId' --output text)"

aws cloudformation deploy --region "$region" --stack-name "$bootstrap_stack" \
  --template-file "$kit/deploy/bootstrap.yaml" --capabilities CAPABILITY_IAM \
  --no-execute-changeset \
  --parameter-overrides \
    WorkerStackName="$workers_stack" \
    VpcCidr="$vpc_cidr" \
    ControllerType=t3.medium \
    ExpectedRegion="$region" \
    ExistingBatchServiceRoleArn="arn:aws:iam::${account}:role/aws-service-role/batch.amazonaws.com/AWSServiceRoleForBatch" \
    ControllerAmi="$controller_ami" \
    RunnerProfileName="$runner_profile_name"
```

Inspect the change set before executing it:

```bash
# Workstation
aws cloudformation describe-change-set --region "$region" --change-set-name "$reviewed_change_set_arn" \
  --query 'Changes[].ResourceChange.{LogicalResourceId:LogicalResourceId,Action:Action,Replacement:Replacement}'
```

The `Controller` resource must be `Modify` with `Replacement` = `False`. If `Replacement` is `True`, stop and do not execute. After a clean execute, confirm the instance ID is unchanged, SSM comes back online, and the instance profile is the runner profile.

**Check before continuing:** the bootstrap stack is `UPDATE_COMPLETE`, the controller instance ID is unchanged, and it is reachable over SSM on the runner profile.

### 5.4 Enable the queue

**Workstation.** Update the workers stack with the same parameters as 4, changing only `QueueState=ENABLED`.

```bash
# Workstation
aws cloudformation deploy --region "$region" --stack-name "$workers_stack" \
  --template-file "$kit/deploy/batch.yaml" --no-execute-changeset \
  --parameter-overrides VpcId="$vpc_id" PrivateSubnets="$subnet_ids_csv" \
    BatchServiceRoleArn="$batch_service_role_arn" InstanceProfileArn="$instance_profile_arn" \
    MaxVcpus=24 RootVolumeGiB=80 InstanceTypes=m6i.2xlarge QueueState=ENABLED
```

The change set should show a `Modify` on the job queue with no replacement. Review and execute it. Check that the queue and compute environment are valid.

**Check before continuing:** the workers stack is `UPDATE_COMPLETE`, and the queue is `ENABLED` and `VALID`.

### 5.5 Upload the matrix

**Workstation.** In the intended ingest identity, execute the upload command printed by `plan_batch.py` against the unused input key, or the equivalent:

```bash
# Workstation
aws s3 cp "$matrix" "s3://${bucket}/${project_prefix}/${run_id}/input/matrix.csv" \
  --region "$region" --no-progress --only-show-errors
aws s3api head-object --region "$region" --bucket "$bucket" \
  --key "${project_prefix}/${run_id}/input/matrix.csv"
```

Retain the observed object `VersionId`, `ETag`, size, and the locally recorded SHA256.

**Check before continuing:** the object size and checksum match the local matrix, and you have recorded `VersionId`.

### 5.6 Stage the kit on the controller

**Controller (SSM).** Launch is from a durable run directory on the controller, not from the workstation path printed by the planner. Use the same verified kit you planned with.

```bash
# Controller (SSM), as ec2-user
run_id=staging-check-01
run="$HOME/dimple-runs/$run_id"
mkdir -p "$run/kit" "$run/evidence"
```

Copy the verified release tarball onto the controller and unpack it into `$run/kit`, or download the same pinned commit you planned against and check the tarball hash:

```bash
# Controller (SSM), as ec2-user
curl -fL --retry 3 -o /tmp/kit.tar.gz \
  "https://codeload.github.com/mlamcogent/DIMPLE-GWAS/tar.gz/${commit}"
echo "$tar_sha256  /tmp/kit.tar.gz" | sha256sum -c -
tar -xzf /tmp/kit.tar.gz -C "$run/kit" --strip-components=1
```

Confirm `plan_batch.py`, `runner_stack.py`, and `launch_attempt.py` match the hashes from your workstation copy of the kit:

```bash
# Workstation, record these first:
sha256sum "$kit/bin/plan_batch.py" "$kit/bin/runner_stack.py" "$kit/bin/launch_attempt.py"
# Controller (SSM):
sha256sum "$run/kit/bin/plan_batch.py" "$run/kit/bin/runner_stack.py" "$run/kit/bin/launch_attempt.py"
```

Copy `smoke-params.json` and the grid file from the workstation into `$run/params.json` and `$run/grid.json` (Session Manager or `scp`). The planner wrote an absolute workstation path in `params.json`; rewrite it to the controller path:

```bash
# Controller (SSM), as ec2-user
python3 - "$run" <<'PY'
import json, sys
from pathlib import Path
run = Path(sys.argv[1])
params_path = run / "params.json"
params = json.loads(params_path.read_text())
params["grid"] = str((run / "grid.json").resolve())
params_path.write_text(json.dumps(params, indent=2) + "\n")
print("grid", params["grid"])
PY
```

If the SSM session is root or `ssm-user`, make the run directory owned by `ec2-user` before launch.

**Check before continuing:** script hashes match, `params.json` has `grid` equal to `$run/grid.json`, and no workstation paths remain in `params.json`. Stop if a hash or path check fails.

### 5.7 Launch the one-job staging check

**Controller (SSM).** For this staging-only check, pass `--prepare-only` so only the PREPARE task runs. Launch as `ec2-user`, detached, so the process survives the SSM session ending. `launch_attempt.py` starts Nextflow in a new session and writes the Nextflow console to `evidence/attempt01/launcher.log`. Redirecting supervisor stdout to `evidence/launch.out` can leave that file empty; follow `launcher.log`.

```bash
# Controller (SSM), as ec2-user
cd "$run"
setsid -f nohup python3 kit/bin/launch_attempt.py --params params.json \
  --attempt-dir evidence/attempt01 --prepare-only \
  > evidence/launch.out 2>&1 < /dev/null
```

Confirm the process started, then record:

- `evidence/attempt01/launcher-pid.json` — PID, process group, and start time
- `evidence/attempt01/nextflow.log` — contains `Session UUID:`
- `evidence/attempt01/launcher.log` — Nextflow console; this is the file to follow

Watch `launcher.log` and the Batch queue until the PREPARE job finishes. Confirm one successful Batch job and the three files under `metadata/`, including the exact input digest and expected shape (60 × 3 for the synthetic example). The ordinary production graph runs only when `prepare_only` is false. Keep AWS executions separate from local `-stub-run`.

**Check before continuing:** `exit.json` reports exit 0, the PREPARE job succeeded, and the metadata files match the planned input digest and shape.

## 6. AWS approved research run and monitoring

**Workstation, then Controller (SSM).** Prepare the actual matrix and a fresh grid. Repeat section 5 with a unique run ID and distinct parameter and policy filenames, and deploy a **new** runner stack from those policies. Attach the new profile the same way as 5.3 (restate every bootstrap parameter and pin `ControllerAmi`). Once the controller uses the new profile, you can delete the previous runner stack. Obtain approval for this exact data, image digest, role scope and spending plan. Review the new run policy. Upload the exact matrix once to its new input key, record the version, stage the kit and rewrite the grid path, then launch from the dedicated controller directory **without** `--prepare-only`.

```bash
# Controller (SSM), as ec2-user
cd "$run"
setsid -f nohup python3 kit/bin/launch_attempt.py --params params.json \
  --attempt-dir evidence/attempt01 \
  > evidence/launch.out 2>&1 < /dev/null
```

Watch `evidence/attempt01/launcher.log` and the selected Batch queue. Keep the local controller cache and the exact S3 work prefix. Inspect the final trace, report, timeline and result manifest after successful completion. Use the same local controller directory, session, input/params/image and work prefix with `launch_attempt.py --resume SESSION_UUID` and a new attempt directory for an unchanged scientific run. Changed input, source or recipe calls for a fresh run ID and reviewed plan.

**Check before continuing:** the controller `exit.json` reports exit 0, expected jobs succeeded, and the published result files are present under the run root. Copy evidence off the controller before any teardown; the controller disk is deleted with the bootstrap stack.

## 7. AWS cancel and clean up

To cancel, stop the exact controller process gracefully. Verify the jobs it submitted from its log, trace and Batch console. Cancel queued jobs and terminate running jobs only by recorded job ID, then confirm terminal states. See [DEPLOY_FIXES.md](DEPLOY_FIXES.md) for `stop_run.py` and evidence export. Preserve logs, versions, and outputs needed for analysis, including a copy of `$run/evidence` from the controller.

Disable the dedicated queue when finished (`QueueState=DISABLED` with the same workers-stack parameters as 5.4) and use the stack lifecycle to retire its Batch and launch resources after jobs drain. Delete stacks in this order: runner, then workers, then bootstrap.

Before deleting the runner stack, detach its profile from the controller. Use the same bootstrap update as 5.3, still pinning `ControllerAmi`, but pass `RunnerProfileName=` (empty). Omitting the parameter would keep the previous name. The change set must again show `Controller` as `Modify`, `Replacement` = `False`. If you delete the runner stack while the controller still uses that profile, CloudFormation may refuse to remove the instance profile.

The batch template retains the S3 bucket, its transport policy, and log group. A test stack's retained bucket and log group must be emptied and deleted separately if they are not being kept. **The bucket is versioned:** `aws s3 rm` leaves prior versions and delete markers, so list and delete every version, repeating if `IsTruncated` is true, then delete the bucket. If `delete-bucket` is denied, delete the retained bucket policy first.

```bash
# Workstation. Review versions.json, then delete only after you have copied results and evidence.
aws s3api list-object-versions --bucket "$bucket" --region "$region" > versions.json
python3 - "$bucket" "$region" <<'PY'
import json, subprocess, sys
data = json.load(open("versions.json"))
objs = [{"Key": o["Key"], "VersionId": o["VersionId"]}
        for key in ("Versions", "DeleteMarkers") for o in data.get(key) or []]
if not objs:
    raise SystemExit("no versions to delete")
# If IsTruncated is true in versions.json, rerun list-object-versions / delete-objects until empty.
bucket, region = sys.argv[1], sys.argv[2]
for i in range(0, len(objs), 1000):
    body = json.dumps({"Objects": objs[i:i+1000], "Quiet": True})
    subprocess.check_call([
        "aws", "s3api", "delete-objects",
        "--bucket", bucket, "--region", region,
        "--delete", body,
    ])
print("deleted", len(objs), "versions")
PY
aws s3api delete-bucket --bucket "$bucket" --region "$region"
aws logs delete-log-group --log-group-name "$log_group" --region "$region"
```

The bootstrap stack terminates the controller and deletes its disk (`DeleteOnTermination` is true) and the NAT gateway. Review and remove obsolete versions, delete markers, work, logs, and job definition revisions only under your retention policy. Check continuing storage and network charges.

**Check before continuing (end of teardown):** the three stacks are gone, the retained bucket and log group are deleted if you are not keeping them, and no NAT or controller charges remain.
