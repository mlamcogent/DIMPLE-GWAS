#!/usr/bin/env python3
"""Owner-invoked only. Dry-run default. Never discover/terminate a whole queue."""
import argparse,json,subprocess,re
from pathlib import Path
UUID=re.compile(r'^[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}$')
def validate(job,queue,work_prefix):
 if job.get('jobQueue')!=queue: raise ValueError('Queue does not match pinned ARN')
 if not work_prefix.startswith('s3://') or len(work_prefix.rstrip('/').split('/'))<5: raise ValueError('Specific dated run work prefix required')
 # Nextflow Batch wrapper carries its S3 task work directory in the command.
 command=' '.join(job.get('container',{}).get('command',[]))
 if work_prefix.rstrip('/')+'/' not in command: raise ValueError('Job command lacks exact run work-prefix binding: '+job.get('jobId','?'))
 return job.get('status') not in ('SUCCEEDED','FAILED')
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--job-ids',required=True,help='JSON array of ALL IDs from this Nextflow session, including retries');p.add_argument('--queue-arn',required=True);p.add_argument('--work-prefix',required=True);p.add_argument('--region',required=True);p.add_argument('--submissions-closed',action='store_true',help='Owner has stopped and verified this launcher cannot submit more work');p.add_argument('--execute',action='store_true');a=p.parse_args()
 ids=json.loads(Path(a.job_ids).read_text());assert isinstance(ids,list) and ids and all(isinstance(x,str) and UUID.fullmatch(x) for x in ids),'Invalid IDs';ids=sorted(set(ids))
 def aws(*args): return json.loads(subprocess.check_output(['aws','--region',a.region,*args,'--output','json']))
 jobs=[]
 for i in range(0,len(ids),100): jobs+=aws('batch','describe-jobs','--jobs',*ids[i:i+100])['jobs']
 if {j['jobId'] for j in jobs}!=set(ids): raise ValueError('Missing job readbacks; HOLD')
 active=[j for j in jobs if validate(j,a.queue_arn,a.work_prefix)]
 print(json.dumps({'verified_jobs':jobs,'active_ids':[j['jobId'] for j in active],'execute':a.execute},indent=2))
 if a.execute:
  if not a.submissions_closed: raise ValueError('HOLD: stop and verify the session launcher first')
  for j in active:
   fresh=aws('batch','describe-jobs','--jobs',j['jobId'])['jobs'][0]
   if validate(fresh,a.queue_arn,a.work_prefix): aws('batch','terminate-job','--job-id',j['jobId'],'--reason','Owner requested scoped run stop')
if __name__=='__main__': main()
