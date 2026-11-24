# Deployment repair notice

Read DEPLOY_FIXES.md first: it supersedes the older launch, identity, capacity and evidence commands below.

# Freeze 5.3 deployment sheet

Run the local sections from an extracted, verified release. Sections marked **AWS** require your own authorization and can create costs. Keep the `.private` directory, run data, configuration, and logs out of GitHub and Docker Hub.

## 1. Local prerequisites and input

Use Java 21 and Nextflow 26.10.3 with `nf-amazon@3.12.1` on a durable controller. Use Python 3.9+ for planning and an existing AWS CLI v2 for the later owner-operated AWS steps. Choose a commercial AWS region and a registry digest for a Linux x86_64 worker built from this source. See the worker checklist in [RELEASE.md](RELEASE.md).

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

## 2. AWS network, IAM and cost review

Have the AWS owner confirm the account, region, quotas, and budget. You can either deploy `deploy/bootstrap.yaml` (Step 0) or supply an existing network and roles. Private subnets must be in one VPC, with public IP assignment off, and approved outbound HTTPS for S3, ECR or your chosen registry, ECS/Batch agent services, and CloudWatch Logs. Confirm DNS, image-pull reachability, and instance capacity. Docker Hub pulls need an approved registry egress route and may be subject to rate limits. If using private ECR, prepare separate repository-scoped pull permissions.

If you are not using Step 0, provide an existing Batch service-linked role, an EC2 ECS instance profile, a task job role with trust for `ecs-tasks.amazonaws.com`, and a separate execution role with that trust. Keep data permissions off the instance profile and execution role. Review existing SCPs, permissions boundaries, endpoint policies, and explicit denies with the AWS owner. Use temporary credentials or a role on the controller. Maintain a separate authorized input-ingest identity.

The batch stack creates a private versioned SSE-S3 bucket, HTTPS-only bucket policy, no-ingress worker security group, IMDSv2/encrypted-disk launch template, managed on-demand Batch compute environment, disabled queue, and retained CloudWatch log group. The template sets zero minimum vCPUs. Batch's allocation strategy can exceed the configured maximum by one instance. Review RAM headroom per instance, disk capacity, and monitoring for compute, NAT, data transfer, logs and retained S3 versions. [AWS Batch compute resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-batch-computeenvironment-computeresources.html)

The published `deploy/batch.yaml` default for MaxVcpus is 24. Do not change the published default; pass MaxVcpus explicitly to fit your quota, and consider setting it to 0 while the queue is idle.

A NAT gateway, its public IPv4 address, and the controller disk keep billing after the controller is stopped. Delete the bootstrap stack only after a reviewed teardown plan, and only after any needed controller snapshot.

## 3. Step 0: deploy bootstrap.yaml (network + controller)

This stack creates a VPC, NAT gateway, S3 gateway endpoint, SSM-only controller, Batch service-linked role if missing, worker instance profile, job role, and execution role. Resource names follow the CloudFormation stack name. Choose a unique stack name and an unused /16 for VpcCidr (default 10.72.0.0/16) that does not overlap any VPC in the account or any network you peer or connect with. A parallel test stack should use a different prefix and CIDR, for example `dimple-f53-ghtest-bootstrap` with `10.73.0.0/16`.

Set `WorkerStackName` to the exact name you will use for the batch stack in the next step. Leave `RunnerProfileName` empty until a run-scoped runner stack exists. Leave `ControllerAmi` empty to resolve the current public AL2023 x86_64 AMI from SSM; to avoid later instance replacement, resolve once and pass that AMI ID as `ControllerAmi` on this deploy and on updates.

```bash
region=ap-southeast-1
account="$(aws sts get-caller-identity --query Account --output text)"
bootstrap_stack=dimple-network
workers_stack=dimple-workers
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

Read the outputs you will pass to `batch.yaml` (`VpcId`, `PrivateSubnets`, `BatchServiceRoleArn`, `InstanceProfileArn`) and keep `JobRoleName`, `JobRoleArn`, `ExecutionRoleArn`, and `ControllerId` for the runner and launch steps:

```bash
aws cloudformation describe-stacks --region "$region" --stack-name "$bootstrap_stack" \
  --query 'Stacks[0].Outputs'
```

## 4. AWS create the reviewed batch stack

In an authenticated owner shell, fill these variables from the Step 0 outputs or from approved existing AWS resources. Use a dedicated stack name short enough for the Batch queue and log group, and set it to the same value as `WorkerStackName` above.

```bash
aws cloudformation deploy --region "$region" --stack-name "$workers_stack" \
  --template-file "$kit/deploy/batch.yaml" --no-execute-changeset \
  --parameter-overrides VpcId="$vpc_id" PrivateSubnets="$subnet_ids_csv" \
    BatchServiceRoleArn="$batch_service_role_arn" InstanceProfileArn="$instance_profile_arn" \
    MaxVcpus=24 RootVolumeGiB=80 InstanceTypes=m6i.2xlarge QueueState=DISABLED
```

Review the reported change set, IAM context, subnet route settings, launch template, and cost estimate. Execute that exact change set with the AWS owner using the console or `aws cloudformation execute-change-set --region "$region" --change-set-name "$reviewed_change_set_arn"`. Wait for completion and inspect outputs. Use **Region**, **Bucket**, **QueueName**, and **LogGroup** from this stack to fill a private copy of `examples/deployment.example.json`. Use a reviewed digest URI for `image` and the exact distinct job/execution role ARNs from Step 0. Verify that the queue, both roles, and the bucket belong to the intended deployment.

## 5. Local render, runner stack, then AWS one-job staging check

```bash
python3 "$kit/bin/plan_batch.py" --deployment "$kit/.private/deployment.json" \
  --matrix "$matrix" --grid "$grid" --run-id staging-check-01 \
  --output "$kit/.private/smoke-params.json" --policies "$kit/.private/smoke-policies.json"
```

The planner prints an upload command and a launch_attempt.py command and writes the private parameter file. Check the exact source digest, run ID and S3 prefixes. The policies file contains separate policy objects for this run only. **Generate a fresh runner stack from those fragments. Do not reuse a hand-edited ResearchRun or job-role policy from an earlier run.**

```bash
python3 "$kit/bin/runner_stack.py" --policies "$kit/.private/smoke-policies.json" \
  --output "$kit/.private/runner-stack.json"
aws cloudformation deploy --region "$region" --stack-name "$runner_stack" \
  --template-file "$kit/.private/runner-stack.json" --capabilities CAPABILITY_IAM \
  --no-execute-changeset --parameter-overrides JobRoleName="$job_role_name"
```

Review and execute that change set. Then point the controller at the new instance profile with a reviewed bootstrap update (`RunnerProfileName` set to the runner profile name) or by replacing the instance-profile association as in [DEPLOY_FIXES.md](DEPLOY_FIXES.md). See [permissions and trust](MANUAL.md#permissions-and-trust) for instance registration, optional ECR pull, logs, and Batch role passing.

After owner review, enable the dedicated queue through a reviewed CloudFormation update with the same parameters and `QueueState=ENABLED`. Check that the queue and compute environment are valid. In the intended ingest identity, execute the generated upload command against the unused input key. Retain the observed object version and locally recorded SHA256. For this staging-only check, add `"prepare_only": true` to the generated smoke-params.json, then run the generated launch_attempt.py command from a fresh durable controller directory under the controller role.

This submits one real **PREPARE** task to check worker startup, scoped S3 staging, pinned input validation, and result publication. Confirm one successful Batch job and the three files under `metadata/`, including the exact input digest and expected 60 × 3 shape. The ordinary production graph runs only when `prepare_only` is false. Keep AWS executions separate from local `-stub-run`.

## 6. AWS approved research run and monitoring

Prepare the actual matrix and a fresh grid. Render another plan using a unique run ID and distinct parameter and policy filenames, and deploy a new runner stack from those policies. Obtain approval for this exact data, image digest, role scope and spending plan. Review the new run policy. Upload the exact matrix once to its new input key, record the version, and run the emitted command from a dedicated durable controller directory. Keep the controller attached or use your organization's supervised session manager.

Watch the controller log and the selected Batch queue. Keep the local controller cache and the exact S3 work prefix. Inspect the final trace, report, timeline and result manifest after successful completion. Use the same local controller directory, session, input/params/image and work prefix with `launch_attempt.py --resume SESSION_UUID` and a new attempt directory for an unchanged scientific run. Changed input, source or recipe calls for a fresh run ID and reviewed plan.

## 7. AWS cancel and clean up

To cancel, stop the exact controller process gracefully. Verify the jobs it submitted from its log, trace and Batch console. Cancel queued jobs and terminate running jobs only by recorded job ID, then confirm terminal states. Preserve logs, versions, and outputs needed for analysis. Disable the dedicated queue when finished and use the stack lifecycle to retire its Batch and launch resources after jobs drain. Delete stacks in this order: runner, then workers, then bootstrap. The batch template retains the S3 bucket, its transport policy, and log group; a test stack's retained bucket and log group must be emptied and deleted separately if they are not being kept. The bootstrap stack terminates the controller and deletes its disk (`DeleteOnTermination` is true) and the NAT gateway. Review and remove obsolete versions, delete markers, work, logs, and job definition revisions only under your retention policy. Check continuing storage and network charges.
