"""Render an owner-supplied Batch run plan locally. It never executes a command."""
import argparse
import csv
import json
import re
import shlex
from pathlib import Path

from matrix_intake import inspect_matrix, load_json, save_new, validate_contract
from matrix_intake import ROOT, GRID_FIELDS, canonical
from science_config import resolve_grid, resolved_science, hdb_candidates

LIMITS = {'seed_chunk': (1, 1000), 'queue_size': (1, 100), 'task_hours': (1, 24),
          **{stage + '_memory_gib': (1, 512) for stage in ('prepare', 'umap', 'concat', 'grid', 'rank')}}
ROLE = r'arn:aws:iam::([0-9]{12}):role/[A-Za-z0-9_+=,.@/-]{1,512}'
IMAGE = r'[A-Za-z0-9][A-Za-z0-9._:/-]+@sha256:[a-f0-9]{64}'


def checked(pattern, value, field):
    if not isinstance(value, str) or not re.fullmatch(pattern, value):
        raise ValueError(f'invalid {field}')
    return value


def plan(settings, matrix, grid_path, run_id, params_path):
    required = {'region', 'queue', 'image', 'job_role', 'execution_role', 'log_group', 'bucket', 'project_prefix'}
    if set(settings) - (required | LIMITS.keys()) or not required <= set(settings):
        raise ValueError('use the deployment settings schema and remove unknown fields')
    region = checked(r'[a-z]{2}(-[a-z]+)+-[1-9][0-9]*', settings['region'], 'commercial AWS region')
    if region.startswith(('cn-', 'us-gov-', 'us-iso')):
        raise ValueError('use a commercial AWS region')
    checked(r'[A-Za-z0-9][A-Za-z0-9_-]{0,127}', settings['queue'], 'Batch queue name')
    checked(IMAGE, settings['image'], 'immutable worker image reference')
    for field in ('job_role', 'execution_role'):
        checked(ROLE, settings[field], field)
    if settings['job_role'] == settings['execution_role'] or (
        re.fullmatch(ROLE, settings['job_role'])[1] != re.fullmatch(ROLE, settings['execution_role'])[1]
    ):
        raise ValueError('use separate job and execution roles in the same account')
    checked(r'/[A-Za-z0-9_./#-]{1,200}', settings['log_group'], 'CloudWatch log group')
    bucket = checked(r'[a-z0-9][a-z0-9-]{1,61}[a-z0-9]', settings['bucket'], 'dedicated S3 bucket name')
    prefix = checked(r'[a-z0-9][a-z0-9-]{0,62}', settings['project_prefix'], 'one project prefix segment')
    checked(r'[A-Za-z0-9][A-Za-z0-9-]{0,62}', run_id, 'fresh run identifier')
    for key, (minimum, maximum) in LIMITS.items():
        if key in settings and (type(settings[key]) is not int or not minimum <= settings[key] <= maximum):
            raise ValueError(f'{key} must be an integer from {minimum} to {maximum}')
    grid = load_json(grid_path)
    recipe = load_json(ROOT / 'conf/recipe.json')
    resolve_grid(grid, recipe)
    contract = grid['input_contract']
    validate_contract(contract)
    facts, _, _ = inspect_matrix(matrix, contract['orientation'], contract['object_id_column'], drop_columns=contract.get('drop_columns', []))
    if any(contract[key] != facts[key] for key in facts):
        raise ValueError('matrix checksum or shape changed since intake')
    for path in (matrix, grid_path, params_path, ROOT):
        if any(not char.isprintable() for char in str(Path(path).resolve())):
            raise ValueError('local paths cannot contain control characters')
    base = f's3://{bucket}/{prefix}/{run_id}'
    params = {key: settings[key] for key in settings.keys() - {'bucket', 'project_prefix'}}
    params.update(input=f'{base}/input/matrix.csv', grid=str(Path(grid_path).resolve()), outdir=base)
    run = ['python3', str(ROOT / 'bin/launch_attempt.py'), '--params', str(Path(params_path).resolve()),
           '--attempt-dir', str(Path(params_path).resolve().parent / 'evidence' / run_id / 'attempt01')]
    upload = ['aws', 's3', 'cp', str(Path(matrix).resolve()), params['input'], '--region', region,
              '--no-progress', '--only-show-errors']
    science = resolved_science(grid)
    candidates = sum(1 for _ in hdb_candidates(science)) * len(science['configs'])
    return params, {'status': 'LOCAL_PLAN_ONLY', 'backend': science['backend'], 'configurations': len(science['configs']), 'candidate_rows': candidates, 'input_sha256': facts['sha256'], 'run_root': base,
                    'upload_command': shlex.join(upload), 'run_command': shlex.join(run)}


def role_policies(params, run_root):
    """Separate policies for owner review and attachment by the AWS administrator."""
    bucket, prefix = run_root.removeprefix('s3://').split('/', 1)
    bucket_arn = f'arn:aws:s3:::{bucket}'
    run_arn = f'{bucket_arn}/{prefix}'
    input_arn = f'{run_arn}/input/matrix.csv'
    work_arn = f'{run_arn}/work/*'
    results_arn = f'{run_arn}/results/*'
    account = re.fullmatch(ROLE, params['job_role'])[1]
    region = params['region']
    batch = f'arn:aws:batch:{region}:{account}:'
    queue = batch + 'job-queue/' + params['queue']
    definition = batch + 'job-definition/nf-*'
    job = batch + 'job/*'
    log_stream = f"arn:aws:logs:{region}:{account}:log-group:{params['log_group']}:log-stream:*"

    def allow(actions, resources, condition=None):
        statement = {'Effect': 'Allow', 'Action': actions, 'Resource': resources}
        if condition:
            statement['Condition'] = condition
        return statement

    def policy(*statements):
        return {'Version': '2012-10-17', 'Statement': statements}

    def list_bucket(*folders):
        paths = [f'{prefix}/{folder}{suffix}' for folder in folders for suffix in ('', '/*')]
        return allow('s3:ListBucket', bucket_arn, {'StringLike': {'s3:prefix': paths}})

    def write_objects(resources):
        return allow(['s3:PutObject', 's3:AbortMultipartUpload', 's3:ListMultipartUploadParts'], resources)

    def read_objects(resources):
        return allow(['s3:GetObject', 's3:GetObjectVersion'], resources)

    location = allow('s3:GetBucketLocation', bucket_arn)
    logs = allow(['logs:CreateLogStream', 'logs:PutLogEvents'], log_stream)
    regional = {'StringEquals': {'aws:RequestedRegion': region}}
    return {
        'controller': policy(
            location, list_bucket('input', 'work', 'results', 'metadata', 'embeddings', 'evidence', 'configs'), read_objects([input_arn, work_arn, results_arn]),
            write_objects([work_arn, results_arn, *[f'{run_arn}/{d}/*' for d in ('metadata', 'embeddings', 'evidence', 'configs')]]),
            allow(['batch:DescribeJobDefinitions', 'batch:DescribeJobs', 'batch:DescribeJobQueues',
                   'batch:ListJobs', 'batch:DescribeComputeEnvironments'], '*', regional),
            allow(['ecs:DescribeTasks', 'ecs:DescribeContainerInstances', 'ec2:DescribeInstances',
                   'ec2:DescribeInstanceAttribute', 'ec2:DescribeInstanceStatus', 'ec2:DescribeInstanceTypes'], '*', regional),
            allow('batch:RegisterJobDefinition', definition,
                  {'StringEquals': {'batch:Image': params['image'], 'batch:User': '10001'},
                   'BoolIfExists': {'batch:Privileged': 'false'}}),
            allow('batch:TagResource', [definition, job], regional),
            allow('batch:SubmitJob', [queue, definition, job]),
            allow(['batch:CancelJob', 'batch:TerminateJob'], job),
            allow('iam:PassRole', [params['job_role'], params['execution_role']],
                  {'StringEquals': {'iam:PassedToService': 'ecs-tasks.amazonaws.com'}}),
        ),
        'worker_job': policy(location, list_bucket('input', 'work'), read_objects([input_arn, work_arn]),
                             write_objects(work_arn)),
        'worker_execution_logs': policy(logs),
        'input_ingest': policy(location, read_objects(input_arn), write_objects(input_arn)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('deployment', 'matrix', 'grid', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--policies', type=Path, help='optional fresh output for role policy fragments')
    args = parser.parse_args()
    try:
        params, commands = plan(load_json(args.deployment), args.matrix, args.grid, args.run_id, args.output)
        if args.policies and (args.policies.resolve() == args.output.resolve() or args.policies.exists()):
            raise ValueError('use a separate fresh policy output path')
        save_new(args.output, params)
        if args.policies:
            save_new(args.policies, role_policies(params, commands['run_root']))
    except (OSError, ValueError, TypeError, KeyError, EOFError, csv.Error) as error:
        parser.exit(2, f'Plan refused: {error}\n')
    print(json.dumps(commands, indent=2))


if __name__ == '__main__':
    main()
