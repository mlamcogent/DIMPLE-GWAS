"""Launch Nextflow with immutable per-attempt local evidence. Owner invoked, never automatic."""
import argparse,datetime,hashlib,json,os,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--params',type=Path,required=True);p.add_argument('--attempt-dir',type=Path,required=True);p.add_argument('--resume',help='explicit Nextflow session UUID');a=p.parse_args()
params=json.loads(a.params.read_text());root=Path(__file__).resolve().parents[1]
a.attempt_dir.mkdir(parents=True,exist_ok=False);d=a.attempt_dir.resolve()
cmd=['nextflow','-log',str(d/'nextflow.log'),'-C',str(root/'nextflow.config'),'run',str(root/'main.nf'),'-profile','awsbatch','-params-file',str(a.params.resolve()),'-work-dir',params['outdir']+'/work','-with-trace',str(d/'trace.tsv'),'-with-report',str(d/'report.html'),'-with-timeline',str(d/'timeline.html')]
if a.resume:cmd+=['-resume',a.resume]
env=os.environ.copy();env.setdefault('NXF_OPTS','-Xms256m -Xmx1024m')
record={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'params_sha256':hashlib.sha256(a.params.read_bytes()).hexdigest(),'run_root':params['outdir'],'region':params['region'],'queue':params['queue'],'NXF_OPTS':env['NXF_OPTS']}
(d/'launch.json').write_text(json.dumps(record,indent=2))
with (d/'launcher.log').open('xb') as log:
 try:
  child=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,env=env,start_new_session=True)
 except Exception as error:
  (d/'exit.json').write_text(json.dumps({'exit':127,'error':str(error)}));raise
 try:
  identity={'pid':child.pid,'pgid':child.pid,'command':cmd,'started_utc':record['started_utc']}
  try:identity['process_start']=subprocess.check_output(['ps','-p',str(child.pid),'-o','lstart='],text=True).strip()
  except (OSError,subprocess.CalledProcessError) as error:identity['identity_unavailable']=str(error)
  (d/'launcher-pid.json').write_text(json.dumps(identity))
 finally:
  status=child.wait()
  (d/'exit.json').write_text(json.dumps({'exit':status,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
sys.exit(status)
