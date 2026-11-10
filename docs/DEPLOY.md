# Deployment repair notice

Read DEPLOY_FIXES.md first: it supersedes the older launch, identity, capacity and evidence commands below.

# Freeze 5.2 deployment sheet

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

Have the AWS owner confirm the account, region, quotas, and budget. Select private subnets in one VPC with public IP assignment off. Provide approved outbound HTTPS, either private endpoints or controlled egress, for S3, ECR or your chosen registry, ECS/Batch agent services, and CloudWatch Logs. Confirm DNS, image-pull reachability, and instance capacity. Docker Hub pulls need an approved registry egress route and may be subject to rate limits. If using private ECR, prepare separate repository-scoped pull permissions.

Provide an existing Batch service-linked role, an EC2 ECS instance profile, a task job role with trust for `ecs-tasks.amazonaws.com`, and a separate execution role with that trust. Keep data permissions off the instance profile and execution role. Review existing SCPs, permissions boundaries, endpoint policies, and explicit denies with the AWS owner. Use temporary credentials or a role on the controller. Maintain a separate authorized input-ingest identity.

The stack creates a private versioned SSE-S3 bucket, HTTPS-only bucket policy, no-ingress worker security group, IMDSv2/encrypted-disk launch template, managed on-demand Batch compute environment, disabled queue, and retained CloudWatch log group. You supply the network, roles, worker image, and controller. The template sets zero minimum vCPUs. Batch's allocation strategy can exceed the configured maximum by one instance. Review RAM headroom per instance, disk capacity, and monitoring for compute, NAT, data transfer, logs and retained S3 versions. [AWS Batch compute resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-batch-computeenvironment-computeresources.html)

## 3. AWS create the reviewed stack

In an authenticated owner shell, fill these variables from approved AWS resources. Use a dedicated stack name short enough for the Batch queue and log group.

```bash
aws cloudformation deploy --region "$region" --stack-name "$stack" \
  --template-file "$kit/deploy/batch.yaml" --no-execute-changeset \
  --parameter-overrides VpcId="$vpc_id" PrivateSubnets="$subnet_ids_csv" \
    BatchServiceRoleArn="$batch_service_role_arn" InstanceProfileArn="$instance_profile_arn" \
    MaxVcpus=24 RootVolumeGiB=80 InstanceTypes=m6i.2xlarge QueueState=DISABLED
```

Review the reported change set, IAM context, subnet route settings, launch template, and cost estimate. Execute that exact change set with the AWS owner using the console or `aws cloudformation execute-change-set --region "$region" --change-set-name "$reviewed_change_set_arn"`. Wait for completion and inspect outputs. Use **Region**, **Bucket**, **QueueName**, and **LogGroup** from this stack to fill a private copy of `examples/deployment.example.json`. Use a reviewed digest URI for `image` and the exact distinct job/execution role ARNs. Verify that the queue, both roles, and the bucket belong to the intended deployment.

## 4. Local render, then AWS one-job staging check

```bash
python3 "$kit/bin/plan_batch.py" --deployment "$kit/.private/deployment.json" \
  --matrix "$matrix" --grid "$grid" --run-id staging-check-01 \
  --output "$kit/.private/smoke-params.json" --policies "$kit/.private/smoke-policies.json"
```

The planner prints an upload command and a launch_attempt.py command and writes the private parameter file. Check the exact source digest, run ID and S3 prefixes. The policies file contains separate policy objects. Give each to the administrator for attachment to the matching identity. See [permissions and trust](MANUAL.md#permissions-and-trust) for instance registration, optional ECR pull, logs, and Batch role passing.

After owner review, enable the dedicated queue through a reviewed CloudFormation update with the same parameters and `QueueState=ENABLED`. Check that the queue and compute environment are valid. In the intended ingest identity, execute the generated upload command against the unused input key. Retain the observed object version and locally recorded SHA256. For this staging-only check, add `"prepare_only": true` to the generated smoke-params.json, then run the generated launch_attempt.py command from a fresh durable controller directory under the controller role.

This submits one real **PREPARE** task to check worker startup, scoped S3 staging, pinned input validation, and result publication. Confirm one successful Batch job and the three files under `metadata/`, including the exact input digest and expected 60 × 3 shape. The ordinary production graph runs only when `prepare_only` is false. Keep AWS executions separate from local `-stub-run`.

## 5. AWS approved research run and monitoring

Prepare the actual matrix and a fresh grid. Render another plan using a unique run ID and distinct parameter and policy filenames. Obtain approval for this exact data, image digest, role scope and spending plan. Review the new run policy. Upload the exact matrix once to its new input key, record the version, and run the emitted command from a dedicated durable controller directory. Keep the controller attached or use your organization's supervised session manager.

Watch the controller log and the selected Batch queue. Keep the local controller cache and the exact S3 work prefix. Inspect the final trace, report, timeline and result manifest after successful completion. Use the same local controller directory, session, input/params/image and work prefix with `launch_attempt.py --resume SESSION_UUID` and a new attempt directory for an unchanged scientific run. Changed input, source or recipe calls for a fresh run ID and reviewed plan.

## 6. AWS cancel and clean up

To cancel, stop the exact controller process gracefully. Verify the jobs it submitted from its log, trace and Batch console. Cancel queued jobs and terminate running jobs only by recorded job ID, then confirm terminal states. Preserve logs, versions, and outputs needed for analysis. Disable the dedicated queue when finished and use the stack lifecycle to retire its Batch and launch resources after jobs drain. The template retains the S3 bucket, its transport policy, and log group. Review and remove obsolete versions, delete markers, work, logs, and job definition revisions only under your retention policy. Check continuing storage and network charges.
