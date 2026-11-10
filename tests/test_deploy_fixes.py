import json,sys,subprocess,tempfile,unittest,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'bin'))
import stop_run
class DeployFixes(unittest.TestCase):
 def test_scoped_stop_rejects_cross_run(self):
  j={'jobQueue':'queue','status':'RUNNING','container':{'command':['aws s3 cp s3://bucket/20261111-run/work/abc/input .']}}
  self.assertTrue(stop_run.validate(j,'queue','s3://bucket/20261111-run/work'))
  with self.assertRaises(ValueError):stop_run.validate(j,'other','s3://bucket/20261111-run/work')
  with self.assertRaises(ValueError):stop_run.validate(j,'queue','s3://bucket/other/work')
 def test_runner_stack_and_job_policy(self):
  with tempfile.TemporaryDirectory() as tmp:
   d=Path(tmp);policy={'Version':'2012-10-17','Statement':[]}
   (d/'policy.json').write_text(json.dumps({'controller':policy,'worker_job':policy}))
   subprocess.run([sys.executable,str(ROOT/'bin/runner_stack.py'),'--policies',str(d/'policy.json'),'--output',str(d/'stack.json')],check=True)
   t=json.loads((d/'stack.json').read_text());self.assertIn('RunnerProfile',t['Resources']);self.assertIn('JobWorkPolicy',t['Resources'])
   self.assertNotIn('DedicatedDimple',json.dumps(t))
 def test_immediate_exit_receipts(self):
  with tempfile.TemporaryDirectory() as tmp:
   d=Path(tmp);(d/'params.json').write_text(json.dumps({'outdir':'s3://synthetic-bucket/run','region':'us-west-2','queue':'synthetic'}))
   for code in (0,1):
    shim=d/'nextflow';shim.write_text('#!/bin/sh\nexit '+str(code)+'\n');shim.chmod(0o755)
    dest=d/('attempt'+str(code));env=dict(os.environ,PATH=str(d)+':'+os.environ['PATH'])
    result=subprocess.run([sys.executable,str(ROOT/'bin/launch_attempt.py'),'--params',str(d/'params.json'),'--attempt-dir',str(dest)],env=env)
    self.assertEqual(result.returncode,code);self.assertEqual(json.loads((dest/'exit.json').read_text())['exit'],code)
 def test_published_dated_id_and_launcher_plan(self):
  import matrix_intake,plan_batch
  with tempfile.TemporaryDirectory() as tmp:
   d=Path(tmp);matrix=ROOT/'examples/synthetic-matrix.csv'
   grid=matrix_intake.create_grid(matrix,'objects_by_features','object_id','none',None)
   (d/'grid.json').write_text(json.dumps(grid));account='0'*12
   settings={'region':'ap-southeast-1','queue':'synthetic','image':'example.invalid/dimple@sha256:'+'f'*64,'job_role':'arn:aws:iam::'+account+':role/job','execution_role':'arn:aws:iam::'+account+':role/execution','log_group':'/synthetic','bucket':'synthetic-bucket','project_prefix':'research'}
   params,commands=plan_batch.plan(settings,matrix,d/'grid.json','20261111T001700Z-digits',d/'params.json')
   self.assertIn('20261111T001700Z-digits',params['outdir']);self.assertIn('launch_attempt.py',commands['run_command'])
   self.assertIn('batch:DescribeComputeEnvironments',json.dumps(plan_batch.role_policies(params,commands['run_root'])))
 def test_failure_then_resume_preserves_prior_logs(self):
  with tempfile.TemporaryDirectory() as tmp:
   d=Path(tmp);(d/'params.json').write_text(json.dumps({'outdir':'s3://synthetic-bucket/same-run','region':'us-west-2','queue':'synthetic'}))
   shim=d/'nextflow';shim.write_text('#!/bin/sh\necho failed-first-attempt\nexit 1\n');shim.chmod(0o755)
   env=dict(os.environ,PATH=str(d)+':'+os.environ['PATH']);cmd=[sys.executable,str(ROOT/'bin/launch_attempt.py'),'--params',str(d/'params.json')]
   first=d/'attempt01';second=d/'attempt02'
   self.assertEqual(subprocess.run(cmd+['--attempt-dir',str(first)],env=env).returncode,1)
   before=(first/'launcher.log').read_bytes()
   shim.write_text('#!/bin/sh\necho resumed-second-attempt\nexit 0\n')
   self.assertEqual(subprocess.run(cmd+['--attempt-dir',str(second),'--resume','synthetic-session'],env=env).returncode,0)
   self.assertEqual((first/'launcher.log').read_bytes(),before)
   self.assertIn('-resume',json.loads((second/'launch.json').read_text())['command'])
   self.assertNotEqual((second/'launcher.log').read_bytes(),before)
 def test_all_scripts_compile(self):
  for f in (ROOT/'bin').glob('*.py'):compile(f.read_text(),str(f),'exec')
 def test_attempt_evidence_and_capacity(self):
  s=(ROOT/'bin/launch_attempt.py').read_text()
  for x in ('exist_ok=False','launcher.log','launch.json','nextflow.log','-Xmx1024m'):self.assertIn(x,s)
  self.assertIn('Default: m6i.2xlarge',(ROOT/'deploy/batch.yaml').read_text())
  self.assertIn('trace.fields',(ROOT/'nextflow.config').read_text())
if __name__=='__main__':unittest.main()
