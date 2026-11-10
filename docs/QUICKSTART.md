# Ready-infrastructure quickstart

Prerequisites: approved ready AWS infrastructure, immutable qualified worker image matching this source, Java21/Nextflow26.10.3/nf-amazon3.12.1 and reviewed runner/work permissions. This source update does not authorize or perform an image build/cloud run. Keep the launch directory stable.

Dropping a column during intake **does not redact the uploaded source CSV**: all original file bytes are uploaded and hashed. If labels, identifiers or metadata must stay local, remove them from the cloud-bound file before intake and retain the mapping/truth locally.

1. Put deployment settings in deployment.json (see examples/deployment.example.json); optionally put scientific overrides in science.json (three small example files are under examples/science-*.example.json). Intake explicitly declares orientation and dropped columns:
```sh
python3 bin/matrix_intake.py --matrix input.csv --orientation objects_by_features --object-id-column object_id --preprocessing none --config science.json --output run-grid.json
python3 bin/plan_batch.py --deployment deployment.json --matrix input.csv --grid run-grid.json --run-id 20261111T001700Z-digits --output params.json --policies policies.json
```
Omit --config for byte-identical published science preset. Planner prints the exact input upload and attempt-launch commands. Owner uploads once using the printed command and verifies input checksum/version; do not alter the file afterwards.

2. One command to run the prepared config:
```sh
nohup python3 bin/launch_attempt.py --params params.json --attempt-dir evidence/attempt01 > attempt01-supervisor.log 2>&1 &
```
3. One command to resume after reviewing a failure, with same scientific identity/work/cache and a new attempt (RAM/time/concurrency can change in params.json):
```sh
nohup python3 bin/launch_attempt.py --params params.json --attempt-dir evidence/attempt02 --resume "$SESSION_UUID" > attempt02-supervisor.log 2>&1 &
```
4. Stop: first interrupt and verify the specific launcher has stopped submitting. Collect ALL submitted job IDs from its session logs (including pending/retries), then one scoped command:
```sh
python3 bin/stop_run.py --job-ids run-job-ids.json --queue-arn "$QUEUE_ARN" --work-prefix "$RUN_ROOT/work" --region "$REGION" --submissions-closed --execute
```
Omit --execute for read-only review. Missing ownership proof fails closed; never stop an entire shared queue. See DEPLOY_FIXES.md for evidence export, exact IAM/stack steps and cost limits. No hard whole-run spending cap is claimed.
