import json
import os
import subprocess
from pathlib import Path
import shlex
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'bin'))
import matrix_intake as intake
import plan_gcp


class Multicloud(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        self.matrix = ROOT / 'examples/synthetic-matrix.csv'
        self.grid = self.path / 'grid with spaces.json'
        self.grid.write_text(json.dumps(intake.create_grid(self.matrix, 'objects_by_features', 'object_id', 'none', None)))
        self.settings = {'project': 'example-project', 'location': 'asia-southeast1',
                         'service_account': 'dimple-worker@example-project.iam.gserviceaccount.com',
                         'bucket': 'example-dimple-bucket', 'project_prefix': 'dimple',
                         'image': 'asia-southeast1-docker.pkg.dev/example-project/workers/dimple@sha256:' + 'a'*64}

    def run_plan(self, **changes):
        return plan_gcp.plan(dict(self.settings, **changes), self.matrix, self.grid, 'run-001', self.path / 'params with spaces.json')

    def test_plan_gcs_and_prepare(self):
        params, commands = self.run_plan()
        self.assertEqual(params['input'], 'gs://example-dimple-bucket/work/run-001/input/matrix.csv')
        self.assertEqual(params['work_dir'], 'gs://example-dimple-bucket/work/run-001/')
        self.assertEqual(params['outdir'], 'gs://example-dimple-bucket/results/run-001')
        argv = shlex.split(commands['run_command'])
        self.assertEqual(argv[argv.index('--profile')+1], 'gcp')
        self.assertEqual(argv[argv.index('--params')+1], str((self.path/'params with spaces.json').resolve()))
        self.assertEqual(shlex.split(commands['prepare_command'])[-1], '--prepare-only')
        prep=shlex.split(commands['prepare_command'])
        self.assertNotEqual(prep[prep.index('--attempt-dir')+1],argv[argv.index('--attempt-dir')+1])
        self.assertIn('--no-clobber', shlex.split(commands['upload_command']))
        self.assertEqual(commands['status'], 'LOCAL_PLAN_ONLY')

    def test_gcp_launcher_receipt_without_cloud(self):
        params, _ = self.run_plan()
        pp = self.path/'params.json'; pp.write_text(json.dumps(params))
        shim = self.path/'nextflow'; shim.write_text('#!/bin/sh\nexit 0\n'); shim.chmod(0o755)
        dest = self.path/'attempt'
        env = dict(os.environ, PATH=str(self.path)+':'+os.environ['PATH'])
        result = subprocess.run([sys.executable, str(ROOT/'bin/launch_attempt.py'),
            '--profile','gcp','--prepare-only','--params',str(pp),'--attempt-dir',str(dest)],env=env)
        self.assertEqual(result.returncode,0)
        record=json.loads((dest/'launch.json').read_text())
        self.assertEqual(record['command'][record['command'].index('-work-dir')+1],params['work_dir'])
        self.assertEqual(record['profile'],'gcp')
        self.assertEqual(record['region'],'asia-southeast1')
        self.assertEqual(record['command'][-2:],['--prepare_only','true'])
        self.assertEqual(json.loads((dest/'exit.json').read_text())['exit'],0)

    def test_custom_science_and_dropped_metadata(self):
        matrix=self.path/'metadata.csv'
        original=self.matrix.read_text().splitlines()
        matrix.write_text(original[0]+',notes\n'+'\n'.join(row+',drop-me' for row in original[1:])+'\n')
        config=ROOT/'examples/science-pca.example.json'
        grid=intake.create_grid(matrix,'objects_by_features','object_id','none',None,drop_columns=['notes'],config=config)
        self.grid.write_text(json.dumps(grid))
        params,commands=plan_gcp.plan(self.settings,matrix,self.grid,'20261111T010000Z-pca',self.path/'custom-params.json')
        self.assertEqual(params['grid'],str(self.grid.resolve()))
        self.assertEqual(grid['input_contract']['drop_columns'],['notes'])
        self.assertEqual(grid['science']['backend'],'pca')
        self.assertIn('launch_attempt.py',commands['run_command'])
        from science_config import resolved_science
        self.assertEqual(resolved_science(grid)['backend'],'pca')

    def test_bad_settings(self):
        for changes in ({'image': 'image:latest'}, {'project': 'bad;rm'}, {'queue_size': True},
                        {'boot_disk_gib': 1}, {'unknown': 5}, {'subnetwork': 'subnet'},
                        {'service_account': 'user@example.org'}, {'location': 'asia-southeast1-a'}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.run_plan(**changes)

    def test_grid_and_matrix_binding(self):
        g = json.loads(self.grid.read_text()); g['confirmed'] = False
        self.grid.write_text(json.dumps(g))
        with self.assertRaises(ValueError): self.run_plan()

    def test_profiles_and_shared_science(self):
        config = (ROOT/'nextflow.config').read_text()
        self.assertIn("process.executor = 'awsbatch'", config)
        self.assertIn("process.executor = 'google-batch'", config)
        self.assertIn('google.batch.serviceAccountEmail', config)
        self.assertIn('google.batch.spot = false', config)
        self.assertIn("PYTHONDONTWRITEBYTECODE = '1'",config)
        main = (ROOT/'main.nf').read_text()
        self.assertNotIn("executor = 'google-batch'", main)
        self.assertNotIn("executor = 'awsbatch'", main)
        self.assertIn('Choose exactly one cloud execution profile', main)
        self.assertNotIn('broker', config)


if __name__ == '__main__': unittest.main()
