"""Owner-invoked private evidence capture. No changes to AWS; preserves existing attempts."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--attempt-dir',type=Path,required=True);p.add_argument('--job-ids',type=Path,required=True);p.add_argument('--region',required=True);p.add_argument('--log-group',required=True);p.add_argument('--results-dir',type=Path,required=True);a=p.parse_args()
has_results=a.results_dir.is_dir() and any(f.is_file() for f in a.results_dir.rglob('*'))
d=a.attempt_dir/'export';d.mkdir(exist_ok=False)
def aws(*args):return json.loads(subprocess.check_output(['aws','--region',a.region,*args,'--output','json']))
ids=json.loads(a.job_ids.read_text());jobs=[]
for i in range(0,len(ids),100):jobs+=aws('batch','describe-jobs','--jobs',*ids[i:i+100])['jobs']
if {j['jobId'] for j in jobs}!=set(ids):raise ValueError('Incomplete job readback; HOLD evidence export')
(d/'jobs.json').write_text(json.dumps(jobs,indent=2))
errors=[] if has_results else [{'error':'No downloaded outputs; capture is partial'}]
for j in jobs:
 streams={x.get('container',{}).get('logStreamName') for x in j.get('attempts',[])}|{j.get('container',{}).get('logStreamName')}
 for n,stream in enumerate(sorted(x for x in streams if x)):
  try:
   events=[];token=None
   while True:
    args=['logs','get-log-events','--log-group-name',a.log_group,'--log-stream-name',stream,'--start-from-head']
    if token:args+=['--next-token',token]
    page=aws(*args);events+=page['events'];next_token=page['nextForwardToken']
    if next_token==token:break
    token=next_token
   (d/(j['jobId']+'-'+str(n)+'.json')).write_text(json.dumps({'stream':stream,'events':events}))
  except Exception as e:errors.append({'job':j['jobId'],'error':str(e)})
(d/'capture-errors.json').write_text(json.dumps(errors,indent=2))
checks={str(f.relative_to(a.results_dir)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(a.results_dir.rglob('*')) if f.is_file() and not f.is_symlink()}
(d/'output-sha256.json').write_text(json.dumps(checks,indent=2))
(d/'cost-receipt.json').write_text(json.dumps({'status':'UNRECONCILED','note':'Batch duration/resource receipts are jobs.json. Obtain billing export separately; runtime estimates are not billed cost.'},indent=2))
(d/'status.json').write_text(json.dumps({'status':'PARTIAL' if errors else 'CAPTURED_BILLING_PENDING','errors':len(errors)}))
print(d)
sys.exit(2 if errors else 0)
