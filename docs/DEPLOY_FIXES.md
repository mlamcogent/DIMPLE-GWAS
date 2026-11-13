# Freeze 5.2 deployment repair 01

DEPLOY.md is now the primary blank-account path and supersedes overlapping commands below. This file retains operational background and evidence-export guidance. Published default recipe and scoring are unchanged. Portable.3 adds explicit existing scientific parameter/backend passthrough; see MANUAL.md. The bootstrap repair leaves the approved published image unchanged; do not rebuild it for this repair. No AWS operation has been performed by this repair. Owner runs all cloud commands below. Never change the old frozen controller role's explicit denies. Never upload private evidence in the public package.

## 1. Quota and capacity
Set REGION to the deployment region; IAM examples explicitly use us-east-1 (IAM is global). Check quota before deployment:
```sh
aws service-quotas get-service-quota --service-code ec2 --quota-code L-1216C47A --region "$REGION"
aws ec2 describe-instances --region "$REGION" --filters Name=instance-state-name,Values=pending,running --output json > running-instances.json
# Only if needed, owner approves and requests; pending request is NOT granted capacity:
aws service-quotas request-service-quota-increase --service-code ec2 --quota-code L-1216C47A --desired-value 64 --region "$REGION"
```
Default workers m6i.2xlarge (32 GiB) and maxvCpus=16, min=0. Reserve quota for controller and other Standard-family On-Demand instances. BEST_FIT_PROGRESSIVE may exceed maxvCpus by one instance, so 24 + 8 plus controller does not fit a quota of 32: quota enforces the ceiling; the default maxvCpus=16 reserves headroom for this case. queue_size=16 is submitted-task concurrency, not worker vCPU. Task RAM8GiB needs worker overhead above8GiB; do not use m6i.large. Review changed CE through CloudFormation before applying; emergency owner command (reconcile stack afterwards):
```sh
aws batch update-compute-environment --compute-environment "$CE" --compute-resources 'minvCpus=0,maxvCpus=16,instanceTypes=m6i.2xlarge' --region "$REGION"
```

## 2. Separate runner and stack-managed work access

Follow DEPLOY.md steps 1–4. The new bootstrap supplies the roles and profiles instead of assuming they exist. `plan_batch.py --policies` emits the run-scoped controller/worker policy fragments; the existing `runner_stack.py` manages their attachment through CloudFormation. Bootstrap's `RunnerProfileName` update selects that new profile on its own dedicated controller without manual drift or modifying frozen controllers. The controller policy includes Batch tagging, nf-amazon's ECS/EC2 reads, and PassRole only for the exact task and execution roles. The initial bootstrap profile is SSM-only. The execution role supplies scoped job-log access. Review SCPs/permission boundaries and wait for propagation; none of these roles bypass explicit denies.

## 3. Controller and network
Recommend t3.medium, Java21, pinned Nextflow26.10.3 and nf-amazon3.12.1. Launcher defaults NXF_OPTS=-Xms256m -Xmx1024m; adjust only after checking free RAM. Controller requires outbound HTTPS to public.cr.seqera.io for plugin retrieval plus the configured image registry and AWS endpoints. Run `nextflow plugin install nf-amazon@3.12.1` before the launch window and verify cache; do not assume existing cache on a fresh host. Standard private subnet NAT/endpoint charges may persist when Batch idle.

## 4. Dated run root and attempts
Planner uses s3://bucket/project/YYYYMMDDTHHMMSSZ-name with input/,work/,metadata/,configs/<config>/embeddings and grid/,results/. No doubled results/results. Use a fresh root for a new scientific run. Resume uses the SAME root/cache and explicit session UUID, but a NEW local attempt directory. Keep the Nextflow launch working directory stable for .nextflow/cache.
```sh
nohup python3 bin/launch_attempt.py --params params.json --attempt-dir evidence/attempt01 > attempt01-supervisor.log 2>&1 &
nohup python3 bin/launch_attempt.py --params params.json --attempt-dir evidence/attempt02 --resume "$SESSION_UUID" > attempt02-supervisor.log 2>&1 &
```
The launcher creates a distinct process session and records PID, PGID and ps start identity; nohup keeps its supervisor alive after SSH disconnect. Each attempt retains launch command/hash/PID/time, console+controller Nextflow log, trace,report,timeline,exit. Explicit trace fields include native_id, timing and peak memory. Never copy owner overlays, local matrix or evidence into the source archive.

## 5. Stop only this run
No hard spend cap is claimed. Owner must monitor billing; task_hours bounds individual tasks, not whole-run cost. Stop new submissions by interrupting the verified Nextflow session (check PID command+start time against launch.json, not stale PID alone), then verify it exited. Build a complete JSON array of all submitted Batch job UUIDs from that session's controller submission logs, including retries and pending jobs; trace alone is insufficient. Never use queue-wide enumeration as a fallback. The supplied stop helper verifies every job's queue and exact run work prefix, failing closed on missing proof:
```sh
python3 bin/stop_run.py --job-ids run-job-ids.json --queue-arn "$QUEUE_ARN" --work-prefix "$RUN_ROOT/work" --region "$REGION"
# Only after reviewing readback and confirming launcher is stopped:
python3 bin/stop_run.py --job-ids run-job-ids.json --queue-arn "$QUEUE_ARN" --work-prefix "$RUN_ROOT/work" --region "$REGION" --submissions-closed --execute
```
Existing5.1 jobs have no tags. Do not assume tags or generic names establish ownership. If log manifest is incomplete or a job lacks exact command-prefix proof, HOLD and reconcile owner receipts, do not broaden cancellation.

## 6. Evidence and costs
After completion/stop, download this run's published outputs only into a new private directory, then capture job receipts/all attempt CloudWatch streams/checksums:
```sh
for prefix in metadata configs results; do
  aws s3 cp "$RUN_ROOT/$prefix/" "evidence/results/$prefix/" --recursive --region "$REGION"
done
python3 bin/export_evidence.py --attempt-dir evidence/attempt01 --job-ids run-job-ids.json --region "$REGION" --log-group "$LOG_GROUP" --results-dir evidence/results
aws s3 cp evidence/ "$RUN_ROOT/evidence/" --recursive --region "$REGION"
```
Use owner operator permissions for export, review diagnostics for private data, keep S3 private. Save actual billing/CUR allocation receipt as cost-billing.json next to cost-receipt.json when available; latter explicitly says UNRECONCILED until then. Batch resource/duration receipts permit calibration but are not exact cost. Include controller/EC2 uptime, EBS, NAT, transfers and log/storage charges. Export errors are listed, not silently treated as successful capture.

## 7. Qualification and handoff
Run self-contained tests from the extracted archive and cfn-lint on the templates. Use the full existing owner-approved linux/amd64 image digest unchanged in deployment.json. Perform owner-controlled prepare-only and full-run qualification only after separate approval; this bootstrap repair does not rebuild or publish an image. This package does not certify an AWS run merely from local tests. Archive filename is dimple-freeze5.2-5.2.0-research-portable.3.tar.gz in the separate parameter-fix qualification kit, not deliverables/. GrokBot owns publication. Never use the2,315-trait matrix for this qualification.
