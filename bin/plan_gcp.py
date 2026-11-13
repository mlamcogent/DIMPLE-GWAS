"""Render a Google Batch run plan locally; never contact GCP or execute commands."""
import argparse
import csv
import json
from pathlib import Path
import shlex

from matrix_intake import ROOT, GRID_FIELDS, canonical, inspect_matrix, load_json, save_new, validate_contract
from plan_batch import IMAGE, LIMITS, checked
from science_config import resolve_grid


def plan(settings, matrix, grid_path, run_id, params_path):
    required = {'project', 'location', 'service_account', 'bucket', 'project_prefix', 'image'}
    optional = {'network', 'subnetwork', 'boot_disk_gib'} | LIMITS.keys()
    if set(settings) - (required | optional) or not required <= set(settings):
        raise ValueError('use the GCP deployment schema and remove unknown fields')
    project = checked(r'[a-z][a-z0-9-]{4,28}[a-z0-9]', settings['project'], 'GCP project ID')
    location = checked(r'[a-z]+-[a-z]+[0-9]+', settings['location'], 'GCP region')
    account = checked(r'[a-z][a-z0-9-]{4,28}[a-z0-9]@[a-z][a-z0-9-]{4,28}[a-z0-9]\.iam\.gserviceaccount\.com', settings['service_account'], 'worker service account email')
    bucket = checked(r'[a-z0-9][a-z0-9-]{1,61}[a-z0-9]', settings['bucket'], 'dedicated GCS bucket name')
    prefix = checked(r'[a-z0-9][a-z0-9-]{0,62}', settings['project_prefix'], 'one project prefix segment')
    checked(r'[A-Za-z0-9][A-Za-z0-9-]{0,62}', run_id, 'fresh run identifier')
    checked(IMAGE, settings['image'], 'immutable worker image reference')
    for key, (minimum, maximum) in {**LIMITS, 'boot_disk_gib': (30, 2048)}.items():
        if key in settings and (type(settings[key]) is not int or not minimum <= settings[key] <= maximum):
            raise ValueError(f'{key} must be an integer from {minimum} to {maximum}')
    for field in ('network', 'subnetwork'):
        if field in settings:
            checked(r'[A-Za-z0-9][A-Za-z0-9_./-]{0,255}', settings[field], field)
    if 'subnetwork' in settings and 'network' not in settings:
        raise ValueError('provide network with subnetwork')
    grid = load_json(grid_path)
    recipe = load_json(ROOT / 'conf/recipe.json')
    resolve_grid(grid, recipe)
    if grid.get("confirmed") is not True:
        raise ValueError("use a confirmed matrix-intake grid")
    contract = grid['input_contract']
    validate_contract(contract)
    facts, _, _ = inspect_matrix(matrix, contract['orientation'], contract['object_id_column'], drop_columns=contract.get('drop_columns', []))
    if any(contract[key] != facts[key] for key in facts):
        raise ValueError('matrix checksum or shape changed since intake')
    for path in (matrix, grid_path, params_path, ROOT):
        if any(not char.isprintable() for char in str(Path(path).resolve())):
            raise ValueError('local paths cannot contain control characters')
    base = f'gs://{bucket}/results/{run_id}'
    work = f'gs://{bucket}/work/{run_id}/'
    params = {key: settings[key] for key in settings.keys() & LIMITS.keys()}
    params.update(image=settings['image'], google_project=project, google_location=location,
                  google_service_account=account, google_boot_disk_gib=settings.get('boot_disk_gib', 50),
                  input=f'{work}input/matrix.csv', grid=str(Path(grid_path).resolve()), outdir=base, work_dir=work)
    for field in ('network', 'subnetwork'):
        if field in settings:
            params['google_' + field] = settings[field]
    run = ['python3', str(ROOT / 'bin/launch_attempt.py'), '--profile', 'gcp',
           '--params', str(Path(params_path).resolve()), '--attempt-dir',
           str(Path(params_path).resolve().parent / 'evidence' / run_id / 'attempt01')]
    prepare = list(run)
    prepare[prepare.index('--attempt-dir') + 1] = str(Path(params_path).resolve().parent / 'evidence' / run_id / 'prepare01')
    prepare.append('--prepare-only')
    upload = ['gcloud', 'storage', 'cp', '--no-clobber', str(Path(matrix).resolve()), params['input'], '--project', project]
    return params, {'status': 'LOCAL_PLAN_ONLY', 'input_sha256': facts['sha256'], 'run_root': base,
                    'upload_command': shlex.join(upload), 'run_command': shlex.join(run),
                    'prepare_command': shlex.join(prepare),
                    'warning': 'No permissions, image pull, quotas, billing, network or live staging verified. Review before execution.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('deployment', 'matrix', 'grid', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--run-id', required=True)
    args = parser.parse_args()
    try:
        params, commands = plan(load_json(args.deployment), args.matrix, args.grid, args.run_id, args.output)
        save_new(args.output, params)
    except (OSError, ValueError, TypeError, KeyError, EOFError, csv.Error) as error:
        parser.exit(2, f'Plan refused: {error}\n')
    print(json.dumps(commands, indent=2))


if __name__ == '__main__':
    main()
