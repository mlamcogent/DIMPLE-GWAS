import contextlib
import csv
import gzip
import json
import os
from pathlib import Path
import shutil
import shlex
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'bin'))
import matrix_intake as intake
import plan_batch
import research

MATRIX = ROOT / 'examples/synthetic-matrix.csv'
RECIPE = ROOT / 'conf/recipe.json'


@contextlib.contextmanager
def directory(path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


class Portable(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def grid(self, matrix=MATRIX, orientation='objects_by_features', column='object_id'):
        return intake.create_grid(matrix, orientation, column, 'none', None)

    def test_prepare_preserves_text_orientation_and_compressed_identity(self):
        ids = ['001', 'NA', '東京']
        observed = []
        for index, (name, orient, column, compress) in enumerate([
            ('synthetic-matrix.csv', 'objects_by_features', 'object_id', False),
            ('synthetic-matrix.csv', 'objects_by_features', 'object_id', True),
            ('synthetic-transposed.csv', 'features_by_objects', None, False),
            ('synthetic-transposed.csv', 'features_by_objects', None, True),
        ]):
            task = self.root / str(index)
            task.mkdir()
            for script in ('research.py', 'freeze5_scoring.py', 'matrix_intake.py', 'science_config.py'):
                shutil.copyfile(ROOT / 'bin' / script, task / script)
            shutil.copytree(ROOT / 'bin/dimple_representations', task / 'dimple_representations')
            raw = (ROOT / 'examples' / name).read_bytes()
            matrix = task / "matrix bytes 'safe'.csv"
            matrix.write_bytes(gzip.compress(raw, mtime=0) if compress else raw)
            grid = self.grid(matrix, orient, column)
            intake.save_new(task / 'grid.json', grid)
            result = subprocess.run([sys.executable, '-B', 'research.py', 'prepare', '--input', str(matrix),
                '--grid', 'grid.json', '--recipe', str(RECIPE), '--source-manifest', str(ROOT / 'source_manifest.json')],
                cwd=task, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            manifest = intake.load_json(task / 'manifest.json')
            self.assertEqual(manifest['input_sha256'], research.sha(matrix))
            self.assertEqual(manifest['object_ids_sha256'], research.sha(task / 'object_ids.csv'))
            self.assertEqual(manifest['pixels_sha256'], research.sha(task / 'pixels.npy'))
            self.assertEqual(manifest['input_contract']['orientation'], orient)
            with (task / 'object_ids.csv').open() as handle:
                self.assertEqual([row['object_id'] for row in csv.DictReader(handle)][:3], ids)
            observed.append(np.load(task / 'pixels.npy', allow_pickle=False))
        for actual in observed[1:]:
            np.testing.assert_array_equal(observed[0], actual)
        self.assertEqual(observed[0].shape, (60, 3))

    def test_intake_invalid_inputs_and_wrong_pinned_bytes(self):
        raw = MATRIX.read_bytes()
        bad_examples = [
            raw.replace(b'feature_2', b'feature_1'), raw.replace(b'feature_2', b''),
            raw.replace(b'001,0.0', b'NA,0.0'), raw.replace(b'001,0.0', b' ,0.0'),
            raw.replace(b'001,0.0', b'001,NaN'), raw.replace(b'001,0.0', b'001,1e999'),
            raw.replace(b'001,0.0', b'001,not-a-number'), raw.replace(b'001,0.0', b'001,'),
            raw.replace(b'001,0.0', b'001'), b'PK\x03\x04not-csv', b'id,f\na,1\n',
        ]
        target = self.root / 'matrix.csv'
        for value in bad_examples:
            with self.subTest(value=value[:40]):
                target.write_bytes(value)
                with self.assertRaises(ValueError):
                    self.grid(target)
        target.write_bytes(raw + b'synthetic_extra,1,2,3\n')
        with self.assertRaisesRegex(ValueError, 'bytes or oriented shape'):
            intake.verify_input(target, self.grid()['input_contract'])
        with self.assertRaisesRegex(ValueError, 'declared object ID'):
            self.grid(target, column='no-such-column')
        with self.assertRaisesRegex(ValueError, 'supply a record'):
            intake.create_grid(MATRIX, 'objects_by_features', 'object_id', 'external', None)

    def test_grid_recipe_and_plan_reject_mutations(self):
        grid = self.grid()
        path = self.root / "run's grid.json"
        output = self.root / 'run params.json'
        intake.save_new(path, grid)
        # These synthetic identities are local policy fixtures only.
        account = '0' * 12
        settings = dict(region='us-west-2', queue='synthetic-queue',
                        image='example.invalid/dimple@sha256:' + 'f' * 64,
                        job_role=f'arn:aws:iam::{account}:role/synthetic-job',
                        execution_role=f'arn:aws:iam::{account}:role/synthetic-execution',
                        log_group='/dimple/synthetic/jobs', bucket='synthetic-dimple-bucket',
                        project_prefix='research', queue_size=2)
        params, preview = plan_batch.plan(settings, MATRIX, path, 'smoke-01', output)
        self.assertTrue(params['input'].endswith('/smoke-01/input/matrix.csv'))
        self.assertTrue(params['outdir'].endswith('/smoke-01'))
        self.assertIn('launch_attempt.py', preview['run_command'])
        self.assertEqual(params['grid'], str(path.resolve()))
        self.assertIn(str(output.resolve()), shlex.split(preview['run_command']))
        policies = plan_batch.role_policies(params, preview['run_root'])
        self.assertNotIn('/results/', json.dumps(policies['worker_job']))
        self.assertIn(settings['execution_role'], json.dumps(policies['controller']))
        tags = [row for row in policies['controller']['Statement'] if row['Action'] == 'batch:TagResource']
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0]['Resource'], [
            f'arn:aws:batch:us-west-2:{account}:job-definition/nf-*',
            f'arn:aws:batch:us-west-2:{account}:job/*',
        ])
        self.assertEqual(tags[0]['Condition'], {
            'StringEquals': {'aws:RequestedRegion': 'us-west-2'},
        })
        for bad in (dict(settings, image='mutable:tag'), dict(settings, queue_size=True),
                    dict(settings, job_role=settings['execution_role']),
                    dict(settings, project_prefix='../shared'), dict(settings, access_key='injected')):
            with self.assertRaises(ValueError):
                plan_batch.plan(bad, MATRIX, path, 'smoke-01', output)
        grid['configs'][0]['min_dist'] = False
        path.write_text(json.dumps(grid))
        with self.assertRaisesRegex(ValueError, 'fixed nine-config'):
            research.grid_load(path, RECIPE)
        with self.assertRaisesRegex(ValueError, 'unmodified matrix-intake|fixed nine-config'):
            plan_batch.plan(settings, MATRIX, path, 'smoke-01', output)

    def test_seed_order_and_rejection_of_foreign_fractional_or_missing(self):
        with directory(self.root):
            Path('manifest.json').write_text('{"matrix_shape":[3,1]}')
            args = SimpleNamespace(config='n15_d0', manifest='manifest.json')
            lineage = research.sha(args.manifest)

            def chunk(first, last, ids=None, sha=lineage):
                seeds = np.arange(first, last + 1)
                values = np.broadcast_to(seeds[:, None, None], (len(seeds), 3, 3)).astype(np.float32)
                np.savez_compressed(f'n15_d0.seeds-{first:04d}-{last:04d}.npz',
                                    seeds=seeds if ids is None else ids, embedding=values,
                                    config_id=args.config, run_sha256=sha)

            chunk(501, 1000)
            chunk(1, 500)
            research.concat(args)
            result = np.load('n15_d0.embedding.npy', allow_pickle=False)
            np.testing.assert_array_equal(result[0, ::3], np.arange(1, 1001))
            self.assertEqual(result.shape, (3, 3000))
            chunk(501, 1000, sha='0' * 64)
            with self.assertRaisesRegex(ValueError, 'different run'):
                research.concat(args)
            chunk(501, 1000, ids=np.arange(501, 1001) + 0.1)
            with self.assertRaisesRegex(ValueError, 'matching shapes'):
                research.concat(args)
            Path('n15_d0.seeds-0501-1000.npz').unlink()
            with self.assertRaisesRegex(ValueError, 'Missing seeds'):
                research.concat(args)

    def test_complete_pool_labels_no_eligible_config_and_foreign_rejection(self):
        with directory(self.root):
            grid = self.grid()
            intake.save_new('grid.json', grid)
            ids = ['001', 'NA', '東京', '04', '05', '06']
            pd.DataFrame({'object_id': ids}).to_csv('ids.csv', index=False)
            intake.save_new('manifest.json', {'matrix_shape': [len(ids), 3],
                'run_grid_sha256': research.sha('grid.json'), 'object_ids_sha256': research.sha('ids.csv')})
            lineage = research.sha('manifest.json')
            configs = [row['config_id'] for row in grid['configs']]
            absent = configs[0]
            for ci, cid in enumerate(configs):
                for ms in range(2, 20):
                    stem = f'{cid}.ms{ms:02d}'
                    base_labels = [-1] * len(ids) if cid == absent else [0, 0, 0, 1, 1, -1]
                    labels = np.tile(np.array(base_labels, dtype=np.int32), (135, 1))
                    np.savez_compressed(stem + '.labels.npz', labels=labels, config_id=cid,
                                        min_samples=ms, run_sha256=lineage)
                    rows = []
                    for eps in range(3):
                        for mcs in range(5, 50):
                            rows.append(dict(config_id=cid, candidate_ordinal=eps * 810 + (ms - 2) * 45 + mcs - 4,
                                epsilon=eps, cluster_selection_epsilon=float(eps), metric='euclidean', alpha=1.0,
                                cluster_selection_method='eom', cluster_selection_persistence=0.0, allow_single_cluster=False, max_cluster_size=0,
                                min_samples=ms, min_cluster_size=mcs, labels_file=stem + '.labels.npz',
                                label_row=len(rows), number_of_clusters=0 if cid == absent else 2,
                                number_of_noise_points=len(ids) if cid == absent else 1,
                                silhouette=None if cid == absent else (ci + mcs / 50) / 10,
                                status='ineligible' if cid == absent else 'success', seconds=0))
                    pd.DataFrame(rows).to_csv(stem + '.metrics.csv', index=False)
            args = SimpleNamespace(grid='grid.json', recipe=RECIPE, ids='ids.csv', manifest='manifest.json')
            shard = Path(f'{configs[-1]}.ms19.metrics.csv')
            original = shard.read_bytes()
            changed = pd.read_csv(shard)
            changed.loc[0, 'label_row'] = 1
            changed.to_csv(shard, index=False)
            with self.assertRaisesRegex(ValueError, 'candidate tuples|candidate parameters'):
                research.rank(args)
            self.assertFalse(Path('pooled_global_ranked.csv').exists())
            shard.write_bytes(original)
            identity = Path('ids.csv').read_bytes()
            pd.DataFrame({'object_id': ids[::-1]}).to_csv('ids.csv', index=False)
            with self.assertRaisesRegex(ValueError, 'object IDs or grid'):
                research.rank(args)
            Path('ids.csv').write_bytes(identity)
            research.rank(args)
            manifest = intake.load_json('run_manifest.json')
            self.assertEqual(manifest['candidate_rows'], 21870)
            self.assertEqual(manifest['per_config_outcomes'][absent], 'NO_ELIGIBLE_CANDIDATE')
            self.assertEqual(len(pd.read_csv('winners.csv')), 18)
            result = pd.read_csv('global_winner.labels.csv', dtype={'object_id':str}, keep_default_na=False)
            self.assertEqual(result.object_id.tolist(), ids)
            self.assertEqual(result.cluster.tolist(), [0, 0, 0, 1, 1, -1])
            self.assertFalse(Path(f'{absent}_within_best.labels.csv').exists())

    def test_raw_scoring_with_noise_and_ties(self):
        table = pd.DataFrame(dict(config_id=['a','b','c','d'], candidate_ordinal=[1,1,1,1],
            status=['success','success','success','ineligible'], silhouette=[.2,.7,.9,np.nan],
            number_of_clusters=[2,6,10,0], number_of_noise_points=[10,20,40,60]))
        ranked, metadata = research.score_table(table)
        weights = np.array([.7,8,30]) / 38.7
        expected = np.array([.2,.7,.9]) / .9 * weights[0] + np.array([2,6,10]) / 10 * weights[1] - np.array([10,20,40]) / 40 * weights[2]
        np.testing.assert_allclose(ranked.set_index('config_id').loc[['a','b','c'],'score'], expected)
        self.assertTrue(metadata['fit_include_noise'])
        self.assertTrue(np.isnan(ranked.set_index('config_id').loc['d','score']))
        tied = table.iloc[[0,0]].copy().assign(config_id=['b','a'])
        self.assertEqual(research.score_table(tied)[0].config_id.tolist(), ['a','b'])
        no_eligible = table.iloc[[3]]
        self.assertEqual(research.score_table(no_eligible)[1]['eligible_models'], 0)

    def test_optional_evaluation_joins_exact_text_and_keeps_output_exclusive(self):
        truth = self.root / 'truth.csv'
        truth.write_text('object_id,target\n001,first\n1,second\nNA,first\n東京,second\n', encoding='utf-8')
        (self.root / 'winners.csv').write_text('name,config_id,selection_scope,labels_file\nglobal,n30_d0,pooled_global,global.labels.csv\n')
        (self.root / 'global.labels.csv').write_text('object_id,cluster\n東京,1\n001,0\nNA,0\n1,1\n', encoding='utf-8')
        args = SimpleNamespace(truth=truth, results=self.root, output=self.root / 'evaluation.csv')
        with contextlib.redirect_stdout(__import__('io').StringIO()):
            research.evaluate(args)
        self.assertEqual(pd.read_csv(args.output).iloc[0].ari_all, 1.0)
        with self.assertRaises(FileExistsError):
            research.evaluate(args)
        truth.write_text('object_id,object_id\n001,first\n')
        with self.assertRaisesRegex(ValueError, 'exactly one target'):
            research.evaluate(args)


if __name__ == '__main__':
    unittest.main()
