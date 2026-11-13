# Freeze 5.2: deploy and run on AWS

This is the primary deployment path and supersedes overlapping commands in DEPLOY_FIXES.md. Run the commands yourself only after approving the account, data transfer and cost. This source-only publish02 cleanup retains the deployed scientific code, workflow and worker image; it requires no image rebuild. Use the full approved `linux/amd64` image digest; an abbreviated digest is not usable.

The two supplied templates create the network, roles, controller, storage and workers. The existing `runner_stack.py` renders a small, run-specific IAM stack from the plan. No pre-existing VPC, instance profile or controller is assumed. A signed-in AWS administrator/operator, AWS CLI v2, Session Manager plugin and local Python 3.9+ are prerequisites. SCPs, permission boundaries, account activation and service quotas can still prevent creation; the templates do not override them.

## 1. Owner shell: identity, quota and bootstrap

Use Bash on the Mac, from a clean extracted package. Keep this shell for later steps. All regional resources are in Singapore. Only direct `aws iam` commands use `us-east-1`; do not set an IAM endpoint URL.

```bash
set -euo pipefail
umask 077
export PYTHONDONTWRITEBYTECODE=1
export AWS_DEFAULT_REGION=ap-southeast-1
REGION=ap-southeast-1
KIT="$(pwd -P)"
BOOT=dimple-f52-bootstrap
WORKERS=dimple-f52-workers
RUNNER=dimple-f52-runner
python3 "$KIT/bin/pack_release.py" --verify "$KIT" >/dev/null
mkdir -p "$KIT/.private"
aws sts get-caller-identity --region ap-southeast-1
aws service-quotas get-service-quota --service-code ec2 --quota-code L-1216C47A --region ap-southeast-1
aws ec2 describe-instances --region ap-southeast-1 \
  --filters Name=instance-state-name,Values=pending,running \
  --query 'Reservations[].Instances[].[InstanceId,InstanceType,State.Name]'
```

Use `MAX_VCPUS=16` for the first deployment if the account has the 32-vCPU Standard On-Demand quota and no other capacity consumes the headroom. Workers use `m6i.2xlarge` (8 vCPUs/32 GiB); Batch may exceed the maximum by one instance. Thus 16 + 8 + the 2-vCPU controller fits 32, but existing instances must be counted. At least 10 available Standard vCPUs are needed for one 8-vCPU worker plus the 2-vCPU controller; lowering maxVcpus does not shrink a worker. If insufficient, HOLD until an approved quota increase is granted. A pending request is not capacity. NAT Gateway, controller, EBS, public IPv4, logs and S3 incur costs even with no Batch jobs.

```bash
# Only after owner approval, if the granted quota is insufficient:
aws service-quotas request-service-quota-increase --service-code ec2 \
  --quota-code L-1216C47A --desired-value 32 --region ap-southeast-1
# Wait for approval; this read must show sufficient GRANTED capacity before launch:
aws service-quotas get-service-quota --service-code ec2 --quota-code L-1216C47A \
  --region ap-southeast-1 --query Quota.Value
```

When capacity is sufficient, continue:

```bash
MAX_VCPUS=16
EXISTING_BATCH_ROLE=''
if aws iam get-role --role-name AWSServiceRoleForBatch --region us-east-1 \
    > "$KIT/.private/batch-role.json" 2> "$KIT/.private/batch-role.err"; then
  EXISTING_BATCH_ROLE=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["Role"]["Arn"])' "$KIT/.private/batch-role.json")
elif ! grep -q NoSuchEntity "$KIT/.private/batch-role.err"; then
  cat "$KIT/.private/batch-role.err"; exit 1
fi
RUNNER_PROFILE=''
CONTROLLER_AMI=$(aws ssm get-parameter --name /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 \
  --region ap-southeast-1 --query Parameter.Value --output text)
printf '%s\n' "$CONTROLLER_AMI" > "$KIT/.private/controller-ami.txt"
deploy_bootstrap() {
  aws cloudformation deploy --region ap-southeast-1 --stack-name "$BOOT" \
    --template-file "$KIT/deploy/bootstrap.yaml" --capabilities CAPABILITY_IAM \
    --parameter-overrides WorkerStackName="$WORKERS" \
      ExistingBatchServiceRoleArn="$EXISTING_BATCH_ROLE" \
      RunnerProfileName="$RUNNER_PROFILE" ControllerType=t3.medium ControllerAmi="$CONTROLLER_AMI" \
    --no-fail-on-empty-changeset
}
deploy_bootstrap
output() {
  aws cloudformation describe-stacks --region ap-southeast-1 --stack-name "$1" \
    --query "Stacks[0].Outputs[?OutputKey=='$2'].OutputValue | [0]" --output text
}
CONTROLLER_ID=$(output "$BOOT" ControllerId)
aws cloudformation describe-stacks --region ap-southeast-1 --stack-name "$BOOT" \
  --query 'Stacks[0].[StackStatus,Outputs]'
aws ssm describe-instance-information --region ap-southeast-1 \
  --filters "Key=InstanceIds,Values=$CONTROLLER_ID" \
  --query 'InstanceInformationList[].[InstanceId,PingStatus]'
```

Success: stack `CREATE_COMPLETE`, controller reported `Online` by SSM. The successful installation marker is `$HOME/dimple/BOOTSTRAP_OK` for ec2-user. Bootstrap's creation signal confirms installation succeeded; if it fails, inspect the stack events and controller user-data log, do not proceed. The private controller is reached by SSM, with no SSH ingress. Workers use private subnets through a single NAT Gateway; it is a simple research layout, not a multi-AZ availability design. Internet HTTPS is needed for installation, Nextflow plugin retrieval, registry pulls and AWS APIs. Docker Hub rate limits can still affect pulls.

## 2. Owner shell: storage and workers

```bash
VPC_ID=$(output "$BOOT" VpcId)
SUBNETS=$(output "$BOOT" PrivateSubnets)
BATCH_ROLE=$(output "$BOOT" BatchServiceRoleArn)
WORKER_PROFILE=$(output "$BOOT" InstanceProfileArn)
JOB_ROLE=$(output "$BOOT" JobRoleArn)
JOB_ROLE_NAME=$(output "$BOOT" JobRoleName)
EXECUTION_ROLE=$(output "$BOOT" ExecutionRoleArn)
deploy_workers() {
  aws cloudformation deploy --region ap-southeast-1 --stack-name "$WORKERS" \
    --template-file "$KIT/deploy/batch.yaml" \
    --parameter-overrides VpcId="$VPC_ID" PrivateSubnets="$SUBNETS" \
      BatchServiceRoleArn="$BATCH_ROLE" InstanceProfileArn="$WORKER_PROFILE" \
      MaxVcpus="$MAX_VCPUS" InstanceTypes=m6i.2xlarge RootVolumeGiB=80 \
      QueueState="$QUEUE_STATE" --no-fail-on-empty-changeset
}
MAX_VCPUS=0
QUEUE_STATE=DISABLED
deploy_workers
BUCKET=$(output "$WORKERS" Bucket)
QUEUE=$(output "$WORKERS" QueueName)
QUEUE_ARN=$(output "$WORKERS" QueueArn)
CE=$(output "$WORKERS" WorkerComputeArn)
LOG_GROUP=$(output "$WORKERS" LogGroup)
aws batch describe-compute-environments --compute-environments "$CE" --region ap-southeast-1 \
  --query 'computeEnvironments[].[status,state,computeResources.minvCpus,computeResources.maxvCpus]'
aws batch describe-job-queues --job-queues "$QUEUE" --region ap-southeast-1 \
  --query 'jobQueues[].[status,state]'
```

Success: compute environment and queue `VALID`, queue `DISABLED`, minimum zero. Wait for `VALID` before continuing. The stack retains the versioned encrypted bucket and job log group on deletion. The bootstrap provides separate job and execution roles; the next step grants exact run-prefix data permissions to the job role. No dataset access is granted to the worker instance profile.

## 3. Owner shell: smoke plan and scoped roles

Use the small included matrix for the first real worker smoke, not private data. The published image is pinned below; this step does not build or publish an image.

```bash
IMAGE='docker.io/zymlam/dimple-gwas-f5:5.2.0-research-portable.3-docsfix01-workdirfix01@sha256:278f7c36f475a82ad3b2444c911b6d90dcc8d2a59e936d48dcf3590b192c09cb'
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)-smoke"
MATRIX="$KIT/examples/synthetic-matrix.csv"
PREPARE_ONLY=true
PLAN="$KIT/.private/$RUN_ID"
mkdir "$PLAN"
export KIT PLAN REGION QUEUE IMAGE JOB_ROLE EXECUTION_ROLE LOG_GROUP BUCKET
python3 - <<'PY'
import json,os,pathlib
p=pathlib.Path(os.environ['PLAN'])
d=json.loads((pathlib.Path(os.environ['KIT'])/'examples/deployment.example.json').read_text())
for k,e in [('region','REGION'),('queue','QUEUE'),('image','IMAGE'),('job_role','JOB_ROLE'),('execution_role','EXECUTION_ROLE'),('log_group','LOG_GROUP'),('bucket','BUCKET')]: d[k]=os.environ[e]
(p/'deployment.json').write_text(json.dumps(d,indent=2))
PY
python3 "$KIT/bin/matrix_intake.py" --matrix "$MATRIX" \
  --orientation objects_by_features --object-id-column object_id \
  --preprocessing none --output "$PLAN/grid.json"
python3 "$KIT/bin/plan_batch.py" --deployment "$PLAN/deployment.json" \
  --matrix "$MATRIX" --grid "$PLAN/grid.json" --run-id "$RUN_ID" \
  --output "$PLAN/params.json" --policies "$PLAN/policies.json" > "$PLAN/plan.json"
cat "$PLAN/plan.json"
python3 "$KIT/bin/runner_stack.py" --policies "$PLAN/policies.json" --output "$PLAN/runner-stack.json"
aws cloudformation deploy --region ap-southeast-1 --stack-name "$RUNNER" \
  --template-file "$PLAN/runner-stack.json" --capabilities CAPABILITY_IAM \
  --parameter-overrides JobRoleName="$JOB_ROLE_NAME" --no-fail-on-empty-changeset
RUNNER_PROFILE_ARN=$(output "$RUNNER" RunnerProfileArn)
RUNNER_PROFILE="${RUNNER_PROFILE_ARN##*/}"
deploy_bootstrap
aws ec2 describe-instances --instance-ids "$CONTROLLER_ID" --region ap-southeast-1 \
  --query 'Reservations[0].Instances[0].IamInstanceProfile.Arn'
```

Success: runner stack complete and controller profile ARN equals `RUNNER_PROFILE_ARN`. Allow IAM propagation; verify the effective identity inside the controller before launch. Updating the runner stack replaces its run-prefix permissions: do this only when the preceding run has finished or been stopped. Keep the same saved CONTROLLER_AMI for every update; do not resolve a newer AMI during profile changes. Bootstrap updates keep the profile selection under CloudFormation rather than creating manual drift. Do not alter any old frozen controller or its explicit-deny policy.

## 4. Owner shell: upload input and copy the plan to the controller

Review `plan.json`, the exact input, digest and destination before executing the emitted upload command. Dropping columns affects analysis only: **remove private identifiers and labels locally before intake, because the original CSV is uploaded**. The synthetic smoke contains no private data. The owner identity needs scoped upload permissions; the plan's `input_ingest` policy is the reference for a restricted uploader.

```bash
python3 - "$PLAN/plan.json" <<'PY'
import json,shlex,subprocess,sys
subprocess.run(shlex.split(json.load(open(sys.argv[1]))['upload_command']),check=True)
PY
RUN_ROOT=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["run_root"])' "$PLAN/plan.json")
INPUT_KEY="${RUN_ROOT#s3://$BUCKET/}/input/matrix.csv"
aws s3api head-object --bucket "$BUCKET" --key "$INPUT_KEY" --region ap-southeast-1 \
  > "$PLAN/input-object.json"
```

Success: `head-object` succeeds; retain its version ID and the intake SHA-256. Next transfer the source package plus grid/parameter files. This transfer bundle excludes the matrix, labels, private local logs and credentials. It rewrites only the plan's local grid path and smoke flag for the controller; scientific settings are not changed.

```bash
CONTROLLER_HOME=/home/ec2-user
export RUN_ID PREPARE_ONLY CONTROLLER_HOME
python3 - <<'PY'
import importlib.util,json,os,pathlib,tarfile
kit=pathlib.Path(os.environ['KIT']); p=pathlib.Path(os.environ['PLAN'])
spec=importlib.util.spec_from_file_location('packer',kit/'bin/pack_release.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
# Verify allowlisted source bytes without including the newly created .private directory.
assert json.loads((kit/m.MANIFEST).read_text()) == m.manifest({n:(kit/n).read_bytes() for n in m.NAMES}), 'Source package changed'
params=json.loads((p/'params.json').read_text())
params['grid']=os.environ['CONTROLLER_HOME']+'/dimple-runs/'+os.environ['RUN_ID']+'/grid.json'
params['prepare_only']=os.environ['PREPARE_ONLY']=='true'
(p/'controller-params.json').write_text(json.dumps(params,indent=2))
with tarfile.open(p/'controller-payload.tar.gz','w:gz') as t:
 for name in (*m.NAMES,m.MANIFEST): t.add(kit/name,arcname='kit/'+name,recursive=False)
 t.add(p/'grid.json',arcname='grid.json',recursive=False)
 t.add(p/'controller-params.json',arcname='params.json',recursive=False)
PY
PAYLOAD_SHA=$(shasum -a 256 "$PLAN/controller-payload.tar.gz" | awk '{print $1}')
aws s3 cp "$PLAN/controller-payload.tar.gz" "$RUN_ROOT/evidence/controller-payload.tar.gz" --region ap-southeast-1
PAYLOAD_URL=$(aws s3 presign "$RUN_ROOT/evidence/controller-payload.tar.gz" --expires-in 900 --region ap-southeast-1)
export PAYLOAD_URL PAYLOAD_SHA
python3 - <<'PY'
import base64,json,os,pathlib,shlex
q=shlex.quote
script='''set -euo pipefail
cd "$HOME"
mkdir -p dimple-runs
mkdir dimple-runs/{run}
cd dimple-runs/{run}
curl --fail --silent --show-error --location {url} -o payload.tar.gz
printf '%s  payload.tar.gz\\n' {sha} | sha256sum -c -
tar -xzf payload.tar.gz
/usr/local/bin/python3 kit/bin/pack_release.py --verify kit >/dev/null
aws sts get-caller-identity --region ap-southeast-1
/usr/local/bin/python3 --version
nextflow -version
'''.format(run=q(os.environ['RUN_ID']),url=q(os.environ['PAYLOAD_URL']),sha=q(os.environ['PAYLOAD_SHA']))
encoded=base64.b64encode(script.encode()).decode()
cmd="echo "+q(encoded)+" | base64 -d | runuser -u ec2-user -- bash -l"
(pathlib.Path(os.environ['PLAN'])/'ssm-copy.json').write_text(json.dumps({'commands':[cmd]}))
PY
COPY_COMMAND=$(aws ssm send-command --region ap-southeast-1 --instance-ids "$CONTROLLER_ID" \
  --document-name AWS-RunShellScript --parameters "file://$PLAN/ssm-copy.json" \
  --query 'Command.CommandId' --output text)
aws ssm wait command-executed --region ap-southeast-1 --command-id "$COPY_COMMAND" --instance-id "$CONTROLLER_ID"
aws ssm get-command-invocation --region ap-southeast-1 --command-id "$COPY_COMMAND" --instance-id "$CONTROLLER_ID" \
  --query '[Status,StandardOutputContent,StandardErrorContent]'
unset PAYLOAD_URL
```

Success: command `Success`, bundle hash and package manifest verified, Python 3.11.11 and Nextflow 26.10.3 shown, and STS identity is the new runner role. If the waiter times out, read command status; do not resubmit blindly into the already-created directory. The temporary signed URL and `ssm-copy.json` permit private bundle retrieval until expiry: keep them private and do not paste into public logs. SSM command history is operator-visible. No permanent staging-bucket read grant is added to the controller.

## 5. Enable workers, launch smoke, verify

Back in the owner shell:

```bash
MAX_VCPUS=16  # approved positive capacity; recalculate quota/headroom first
QUEUE_STATE=ENABLED
deploy_workers
aws batch describe-job-queues --job-queues "$QUEUE" --region ap-southeast-1 --query 'jobQueues[].[status,state]'
aws ssm start-session --target "$CONTROLLER_ID" --region ap-southeast-1
```

Success: queue `VALID`/`ENABLED`, SSM session opens. In that controller session, substitute the exact RUN_ID printed in the owner shell, then run:

```bash
sudo -iu ec2-user
export AWS_DEFAULT_REGION=ap-southeast-1
export NXF_OPTS='-Xms256m -Xmx1024m'
cd "$HOME/dimple-runs/REPLACE_WITH_RUN_ID"
nextflow plugin install nf-amazon@3.12.1
nohup /usr/local/bin/python3 kit/bin/launch_attempt.py --params params.json \
  --attempt-dir evidence/attempt01 > attempt01-supervisor.log 2>&1 &
LAUNCHER_PID=$!
while [ ! -f evidence/attempt01/launcher.log ]; do
  kill -0 "$LAUNCHER_PID" 2>/dev/null || { cat attempt01-supervisor.log; exit 1; }
  sleep 1
done
tail -f evidence/attempt01/launcher.log
```

Ctrl-C stops only `tail`, not the background launcher. After completion:

```bash
cat evidence/attempt01/exit.json
cat evidence/attempt01/trace.tsv
```

Success: exit zero, one `PREPARE` task `COMPLETED`, no other scientific tasks. In the owner shell, inspect the metadata and its digest/shape:

```bash
mkdir "$PLAN/smoke-metadata"
aws s3 cp "$RUN_ROOT/metadata/" "$PLAN/smoke-metadata/" --recursive --region ap-southeast-1
ls -l "$PLAN/smoke-metadata"
cat "$PLAN/smoke-metadata/manifest.json"
```

Verify the manifest records the original intake SHA-256, 60 objects and three features. This is a real cloud staging smoke, not scientific acceptance or full-run qualification. Failed smoke: keep its evidence and fix the cause before a full run.

## 6. Approved run, monitoring and resume

Once smoke succeeds, in the same owner shell set a **new** dated RUN_ID, MATRIX to the approved locally cleaned file, and `PREPARE_ONLY=false`; set PLAN to the new `.private/$RUN_ID` directory. Repeat steps 3–5, starting at `mkdir "$PLAN"` in step 3. Keep `IMAGE` unchanged. Adjust the intake orientation/ID column/preprocessing explicitly for that file; never guess orientation. The published recipe stays the default. For supported PCA/ICA/custom settings follow MANUAL.md before planning. Review the printed plan and data/cost approval before upload. For an initial full qualification, keep MATRIX at the included synthetic matrix. Use real data only after separate data-transfer and scientific approval.

Wait for exit zero and verify task counts, final trace/report/timeline and published outputs. Do not reuse an old plan or a smoke run root for a new scientific run. Resource-only changes can resume the same scientific run as a **new attempt**, keeping the same controller working directory, session UUID, source, image, input/grid and S3 work root:

```bash
# Controller, from the SAME dimple-runs/RUN_ID directory; set the recorded session UUID.
SESSION_UUID=REPLACE_WITH_RECORDED_NEXTFLOW_SESSION_UUID
nohup /usr/local/bin/python3 kit/bin/launch_attempt.py --params params.json \
  --attempt-dir evidence/attempt02 --resume "$SESSION_UUID" > attempt02-supervisor.log 2>&1 &
```

See DEPLOY_FIXES.md for evidence export. `task_hours` limits individual tasks, not total spend. Monitor the whole run and continuing controller/NAT/storage costs.

## 7. Stop only this run, then remove worker capacity

First stop the verified launcher, not unrelated processes. In the controller run directory, select the current attempt and inspect its recorded PID/PGID/start time:

```bash
ATTEMPT=evidence/attempt01
/usr/local/bin/python3 - "$ATTEMPT/launcher-pid.json" <<'PY_STOP'
import json,os,signal,subprocess,sys
r=json.load(open(sys.argv[1])); pid=int(r['pid']); pgid=int(r['pgid'])
probe=subprocess.run(['ps','-p',str(pid),'-o','lstart='],text=True,capture_output=True)
if probe.returncode:
 print('Recorded process is absent; no signal sent. Verify the exit receipt.')
else:
 assert pid>1 and pgid==pid and r.get('process_start'), 'Missing identity proof: HOLD'
 assert probe.stdout.strip()==r['process_start'], 'PID start time changed: HOLD'
 assert os.getpgid(pid)==pgid, 'Process group changed: HOLD'
 args=subprocess.check_output(['ps','-p',str(pid),'-o','args='],text=True)
 assert 'nextflow' in args.lower(), 'Not the recorded Nextflow process: HOLD'
 print('Sending SIGINT to verified Nextflow group',pgid)
 os.killpg(pgid,signal.SIGINT)
PY_STOP
# Allow graceful exit; verify the recorded process is absent and inspect exit.json.
cat "$ATTEMPT/exit.json"
```

Do not kill a reused PID or send another signal if identity cannot be confirmed. If no process exists, verify the saved exit record instead. Confirm launcher exit before proceeding. In the original owner shell, supply a complete, reconciled JSON array of this run's submitted Batch job UUIDs (including all attempts/retries) at "$PLAN/run-job-ids.json" from the run's existing submission receipts. Trace alone may omit pending jobs. If receipts are incomplete, HOLD; never substitute a queue-wide sweep. The existing stop helper verifies queue and run-prefix ownership before acting.

```bash
cd "$PLAN"
python3 "$KIT/bin/stop_run.py" --job-ids run-job-ids.json --queue-arn "$QUEUE_ARN" \
  --work-prefix "$RUN_ROOT/work" --region ap-southeast-1
# Review readback; only after submissions are closed:
python3 "$KIT/bin/stop_run.py" --job-ids run-job-ids.json --queue-arn "$QUEUE_ARN" \
  --work-prefix "$RUN_ROOT/work" --region ap-southeast-1 --submissions-closed --execute
# Repeat the read-only command and verify there are no active IDs.
```

Missing ownership proof or incomplete job IDs means HOLD and reconcile the receipts; never broaden termination. With this dedicated queue's runs drained or terminated, in the original owner shell:

```bash
QUEUE_STATE=DISABLED
MAX_VCPUS=0
deploy_workers
aws batch describe-job-queues --job-queues "$QUEUE" --region ap-southeast-1 --query 'jobQueues[].[status,state]'
aws batch describe-compute-environments --compute-environments "$CE" --region ap-southeast-1 \
  --query 'computeEnvironments[].[status,computeResources.minvCpus,computeResources.maxvCpus,computeResources.desiredvCpus]'
```

Success: queue disabled, min/max zero; check worker instances actually terminate. **Setting maxvCpus to zero does not terminate already-running jobs.** It is a capacity control, not an immediate spend stop. Before a later launch restore the approved positive capacity and enable the queue. Bootstrap/controller/NAT/EBS and retained logs/S3 still cost money. Preserve all required evidence, then explicitly approve infrastructure teardown; deleting the worker stack retains its bucket/logs, and removing bootstrap networking requires worker resources to be gone first. Do not delete the runner stack while the controller still uses its profile; first restore `RUNNER_PROFILE=''` with `deploy_bootstrap` or remove the controller through the approved bootstrap teardown.


## 8. Return results and logs to the owner

After completion or a verified stop, export only attempt logs/reports from the controller's run directory. This does not copy the work cache, inputs or source payload:

```bash
RUN_ROOT=$(/usr/local/bin/python3 -c 'import json; print(json.load(open("params.json"))["outdir"])')
aws s3 cp evidence/ "$RUN_ROOT/evidence/logs/" --recursive --region ap-southeast-1 \
  --exclude '*' --include '*.log' --include '*.log.*' --include '*.tsv' \
  --include '*.html' --include '*/exit.json'
aws s3 cp . "$RUN_ROOT/evidence/logs/" --recursive --region ap-southeast-1 \
  --exclude '*' --include 'attempt*-supervisor.log'
```

In the original owner shell, download into a new directory. Only the published results prefix and run-scoped evidence/logs prefix are returned; no work/ directory is downloaded:

```bash
RETURN_DIR="$PLAN/returned-results-and-logs"
mkdir "$RETURN_DIR"
aws s3 cp "$RUN_ROOT/results/" "$RETURN_DIR/results/" --recursive --region ap-southeast-1
aws s3 cp "$RUN_ROOT/evidence/logs/" "$RETURN_DIR/logs/" --recursive --region ap-southeast-1 \
  --exclude '*' --include '*.log' --include '*.log.*' --include '*.tsv' \
  --include '*.html' --include '*/exit.json'
find "$RETURN_DIR" -type f -print
```

Success: expected result CSVs and each completed attempt's trace/report/timeline/exit receipt are present. A prepare-only smoke has no final result CSVs. Keep earlier attempts; do not overwrite them on resume.

## 9. Un-park for a later approved run

In the original owner shell, re-check the granted quota and existing instance usage from step 1. Wait for the previous run to finish before replacing runner permissions. Keep the saved controller AMI and pinned image.

```bash
MAX_VCPUS=16  # choose only an approved value that fits available headroom
QUEUE_STATE=ENABLED
deploy_workers
aws batch describe-job-queues --job-queues "$QUEUE" --region ap-southeast-1 --query 'jobQueues[].[status,state]'
aws batch describe-compute-environments --compute-environments "$CE" --region ap-southeast-1 \
  --query 'computeEnvironments[].[status,computeResources.minvCpus,computeResources.maxvCpus]'
```

Success: queue VALID/ENABLED, compute environment VALID with minimum zero and the approved positive maximum. For a new run use a fresh run ID and repeat planning, scoped runner deployment and transfer; do not reuse a smoke directory. Park again after results and logs have been checked.

## Qualification record and practical checks

The deployment run log records a successful PREPARE-only synthetic smoke on 13 November 2026, followed by a full default synthetic run: 182/182 tasks completed with exit zero (1 PREPARE, 9 UMAP_CHUNK, 9 CONCAT, 162 GRID, 1 RANK), 21,870 candidate rows and 7,776 eligible rows. This is operational synthetic qualification, not scientific acceptance or evidence about a real dataset. The live stack was then parked, not torn down.

Retain input hashes, ordered object IDs, trace/exit receipts and output counts when checking a run. Keep temporary signed transfer URLs private. Wait for launcher.log before tailing it; use the exact saved AMI on stack updates. Upload logs under evidence/logs, which is covered by the existing run-scoped controller policy; a separate top-level logs prefix is not. Controller, NAT, IPv4, EBS, logs and storage still incur costs while workers are parked.
