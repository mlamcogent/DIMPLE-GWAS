import json
from pathlib import Path
import subprocess
import unittest
ROOT=Path(__file__).resolve().parents[1]
class GcpAlignment(unittest.TestCase):
    def test_private_quota_profile(self):
        s=(ROOT/'nextflow.config').read_text().split('    gcp {',1)[1].split('    awsbatch {',1)[0]
        for v in ["process.machineType = 'n2-standard-4'",'google.batch.usePrivateAddress = true','google.batch.spot = false','google.batch.preemptible = false','google.batch.maxSpotAttempts = 0','Math.min(6, params.queue_size as int)']:
            self.assertIn(v,s)
        self.assertNotIn('noExternalIpAddress',s)
        d=json.loads((ROOT/'examples/deployment.gcp.example.json').read_text())
        self.assertEqual(d['project'],'YOUR_PROJECT_ID')
        self.assertEqual(d['queue_size']*4,24)
        import sys
        sys.path.insert(0,str(ROOT/'bin'))
        import plan_gcp
        with self.assertRaises(ValueError):
            plan_gcp.plan(d, ROOT/'examples/synthetic-matrix.csv', ROOT/'unused-grid.json', 'smoke-001', ROOT/'unused-params.json')
        self.assertIn('asia-southeast1',d['subnetwork'])
        self.assertEqual(d['image'],'asia-southeast1-docker.pkg.dev/YOUR_PROJECT_ID/dimple/dimple-gwas-f5@sha256:4398934e14aded2b5ec2c891f39a2d0f559522cf276799997a49f4a45c24a383')
        self.assertEqual(d['bucket'],'YOUR_BUCKET_NAME')
        self.assertEqual(d['service_account'],'dimple-batch-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com')
    def test_setup_is_guarded_and_scoped(self):
        p=ROOT/'deploy/gcp-prerequisites.sh'
        self.assertEqual(subprocess.run(['bash','-n',str(p)]).returncode,0)
        result=subprocess.run(['bash',str(p)],capture_output=True,text=True)
        self.assertEqual(result.returncode,2)
        self.assertIn('--apply',result.stderr)
        s=p.read_text()
        for v in ['batch.googleapis.com','artifactregistry.googleapis.com','iam.googleapis.com','roles/batch.agentReporter','roles/logging.logWriter','roles/artifactregistry.reader','roles/storage.objectAdmin','--enable-private-ip-google-access']:
            self.assertIn(v,s)
        self.assertNotIn('--role=roles/storage.admin',s)
        self.assertNotIn('keys create',s)
        self.assertFalse((ROOT/'deploy/gcp-lifecycle.json').exists())
        for forbidden in ['--lifecycle-file','buckets update','buckets create','service-accounts create','cloudresourcemanager.googleapis.com','roles/batch.jobsEditor','roles/iam.serviceAccountUser','CONTROLLER_MEMBER']:
            self.assertNotIn(forbidden,s)
    def test_nonroot_workdir_and_retention_warning(self):
        s=(ROOT/'deploy/Dockerfile').read_text()
        self.assertIn('ENV HOME=/tmp\nWORKDIR /tmp\nUSER 10001',s)
        d=(ROOT/'docs/DEPLOY_GCP.md').read_text()
        for v in ['IAP-only', 'RUN_CONTROLLER_DIR', 'docker.io/zymlam/dimple-gwas-f5:', 'GCP live qualification remains pending','not spending caps','not Docker Hub','a project-wide hard vCPU cap','No GCP changes']:
            self.assertIn(v,d)
if __name__=='__main__': unittest.main()
