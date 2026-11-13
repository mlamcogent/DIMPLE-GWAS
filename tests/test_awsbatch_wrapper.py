"""Offline Batch-style PREPARE wrapper test. No image pull, build, network or AWS.

Set DIMPLE_WRAPPER_IMAGE to an immutable locally cached image ID/digest to run.
DIMPLE_WRAPPER_RECEIPT optionally selects a new JSON receipt path.
DIMPLE_WRAPPER_OLD_IMAGE optionally adds the prior-image negative/override controls.
S3 staging is deliberately replaced by local read-only fixture copies; this is
not a live Batch/IAM/S3 test or a full Nextflow execution.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'bin'))
from matrix_intake import create_grid

# AWS Batch starts bash in the image's configured cwd. Stage the task wrapper
# relative to that cwd BEFORE its contents can change directory.
BATCH_WRAPPER = r'''set -euo pipefail
printf 'WRAPPER_START uid=%s cwd=%s\n' "$(id -u)" "$PWD"
cp /fixtures/.command.run .command.run
/bin/bash .command.run
'''
COMMAND_RUN = r'''#!/bin/bash
set -euo pipefail
umask 077
trap 'rc=$?; printf "%s\n" "$rc" > .exitcode' EXIT
cp -R /fixtures/task/. .
/bin/bash -ue .command.sh > .command.out 2> .command.err
cat .command.out
'''
COMMAND_SH = r'''set -euo pipefail
python research.py prepare --input matrix.csv --grid run-grid.json --recipe recipe.json --source-manifest source_manifest.json --image "$DIMPLE_TEST_IMAGE"
python - <<'PY_RESULT'
import hashlib,json,os
from pathlib import Path
import numpy as np
m=json.loads(Path('manifest.json').read_text())
p=np.load('pixels.npy',allow_pickle=False)
assert os.getuid()==10001
assert Path.cwd()==Path('/tmp')
assert os.statvfs('/').f_flag & os.ST_RDONLY, 'Root filesystem is not read-only'
assert p.shape==(60,3) and m['matrix_shape']==[60,3]
assert len(Path('object_ids.csv').read_text().splitlines())==61
assert m['input_sha256']==hashlib.sha256(Path('matrix.csv').read_bytes()).hexdigest()
print('DIMPLE_WRAPPER_RESULT '+json.dumps({'uid':os.getuid(),'cwd':str(Path.cwd()),'root_readonly':True,'matrix_shape':m['matrix_shape'],'source_checksums_verified_by_prepare':True,'input_sha256':m['input_sha256'],'outputs':['pixels.npy','object_ids.csv','manifest.json']}))
PY_RESULT
'''

class AwsBatchWrapper(unittest.TestCase):
    def test_dockerfile_workdir(self):
        text = (ROOT / 'deploy/Dockerfile').read_text()
        self.assertIn('\nWORKDIR /tmp\n', text)
        self.assertIn('\nUSER 10001\n', text)
        self.assertLess(text.index('\nWORKDIR /tmp\n'), text.index('\nUSER 10001\n'))

    @unittest.skipUnless(os.environ.get('DIMPLE_WRAPPER_IMAGE'),
                         'Set DIMPLE_WRAPPER_IMAGE to a cached immutable image for the actual container test')
    def test_real_prepare_through_batch_style_wrapper(self):
        image = os.environ['DIMPLE_WRAPPER_IMAGE']
        self.assertTrue(image.startswith('sha256:') or '@sha256:' in image,
                        'Pin an image ID or repository digest, not a mutable tag')
        inspected = json.loads(subprocess.check_output(['docker','image','inspect',image],text=True))[0]
        self.assertEqual(inspected['Architecture'], 'amd64')
        self.assertEqual(inspected['Config']['WorkingDir'], '/tmp')
        self.assertEqual(inspected['Config']['User'], '10001')
        observations = []
        with tempfile.TemporaryDirectory(prefix='dimple-wrapper-') as tmp:
            fixtures = Path(tmp).resolve()
            task = fixtures/'task'; task.mkdir()
            for name in ('research.py','freeze5_scoring.py','matrix_intake.py','science_config.py'):
                shutil.copyfile(ROOT/'bin'/name,task/name)
            shutil.copytree(ROOT/'bin/dimple_representations',task/'dimple_representations',
                            ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
            for src,dest in [('examples/synthetic-matrix.csv','matrix.csv'),
                             ('conf/recipe.json','recipe.json'),('source_manifest.json','source_manifest.json')]:
                shutil.copyfile(ROOT/src,task/dest)
            grid = create_grid(ROOT/'examples/synthetic-matrix.csv','objects_by_features','object_id','none',None)
            (task/'run-grid.json').write_text(json.dumps(grid))
            (fixtures/'.command.run').write_text(COMMAND_RUN)
            (task/'.command.sh').write_text(COMMAND_SH)
            # Bind fixtures are readable by the unprivileged container user.
            fixtures.chmod(0o755)
            for p in fixtures.rglob('*'): p.chmod(0o755 if p.is_dir() else 0o644)

            def run(label, target, workdir=None):
                cmd=['docker','run','--rm','--pull=never','--platform','linux/amd64',
                     '--network','none','--read-only','--user','10001:10001',
                     '--cap-drop','ALL','--security-opt','no-new-privileges',
                     '--tmpfs','/tmp:rw,nosuid,nodev,size=256m,mode=1777',
                     '--mount','type=bind,src='+str(fixtures)+',dst=/fixtures,readonly',
                     '--env','HOME=/tmp','--env','PYTHONDONTWRITEBYTECODE=1',
                     '--env','DIMPLE_TEST_IMAGE='+target]
                if workdir is not None: cmd += ['--workdir',workdir]
                cmd += ['--entrypoint','/bin/bash',target,'-o','pipefail','-c',BATCH_WRAPPER]
                r=subprocess.run(cmd,text=True,capture_output=True,timeout=180)
                observations.append({'case':label,'image':target,'explicit_workdir':workdir,
                                     'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,
                                     'command':cmd})
                return r

            result=run('fixed-image-default-workdir',image)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            markers=[x for x in result.stdout.splitlines() if x.startswith('DIMPLE_WRAPPER_RESULT ')]
            self.assertEqual(len(markers),1,result.stdout)
            facts=json.loads(markers[0].split(' ',1)[1])
            self.assertEqual(facts['matrix_shape'],[60,3])
            negative=run('fixed-image-forced-root-negative',image,'/')
            self.assertNotEqual(negative.returncode,0)
            self.assertNotIn('DIMPLE_WRAPPER_RESULT ',negative.stdout)
            self.assertIn('cwd=/',negative.stdout)
            self.assertIn('.command.run',negative.stderr)
            old=os.environ.get('DIMPLE_WRAPPER_OLD_IMAGE')
            if old:
                self.assertTrue(old.startswith('sha256:') or '@sha256:' in old)
                old_result=run('prior-image-default-negative',old)
                self.assertNotEqual(old_result.returncode,0)
                self.assertIn('.command.run',old_result.stderr)
                override=run('prior-image-explicit-tmp-positive',old,'/tmp')
                self.assertEqual(override.returncode,0,override.stdout+override.stderr)
        receipt={'result':'PASS','image_id':inspected['Id'], 'repo_digests':inspected['RepoDigests'],
                 'image_workdir':inspected['Config']['WorkingDir'],'image_user':inspected['Config']['User'],
                 'task':'real synthetic PREPARE (60 objects x 3 features)',
                 'wrapper_scope':'Batch-style relative .command.run staging and .command.sh execution; local copies replace S3',
                 'network':'none','root_filesystem':'read-only','tmp':'writable tmpfs',
                 'facts':facts,'cases':observations,
                 'not_tested':['live AWS Batch','IAM/S3 transport','complete Nextflow workflow','full scientific run']}
        if os.environ.get('DIMPLE_WRAPPER_RECEIPT'):
            p=Path(os.environ['DIMPLE_WRAPPER_RECEIPT'])
            with p.open('x') as f: json.dump(receipt,f,indent=2); f.write('\n')
        print(json.dumps({'wrapper_result':'PASS','cases':len(observations),'image_id':inspected['Id'],'matrix_shape':facts['matrix_shape']}))

if __name__=='__main__':
    unittest.main(verbosity=2)
