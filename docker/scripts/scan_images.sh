#!/usr/bin/env bash
# Uses a previously downloaded run-owned DB; it cannot download one or upload scans.
# Usage: scan_images.sh --run-root RUN --archive IMAGE.tar --output RUN/security/IMAGE [--context RUN/contexts/CONTEXT]
set -euo pipefail
exec python3 - "$@" <<'PY'
import argparse, datetime, hashlib, json, os, platform, subprocess, sys, tarfile, uuid
from collections import Counter
from pathlib import Path, PurePosixPath

TOOLS = {
    'arm64': 'aquasec/trivy@sha256:55ad20f8a239a3e95427e60b8aaea38788550c18a3f1772976bebf732e6ae166',
    'amd64': 'aquasec/trivy@sha256:ee940acbf1f58ebadb42d01434ce4609530bf1b52536afbd1eee66cd7123c5c9',
}
p = argparse.ArgumentParser(description='Offline local vulnerability, secret and licence scan with a pinned Trivy container and predownloaded DB.')
p.add_argument('--run-root', required=True)
p.add_argument('--archive', required=True)
p.add_argument('--output', required=True)
p.add_argument('--db-cache')
p.add_argument('--context')
a = p.parse_args()
os.umask(0o077)

def path(value):
    q = Path(value).absolute()
    if any(c in str(q) for c in ',\n\r') or any(x.is_symlink() for x in [q, *q.parents]):
        raise ValueError('Unsafe path: symlink or mount-delimiter/control character')
    return q.resolve()

def sha(q):
    h = hashlib.sha256()
    with q.open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''): h.update(block)
    return h.hexdigest()

root, archive, out = map(path, (a.run_root, a.archive, a.output))
if root.parent.name != 'runs' or not (root/'inventory/source_identity.json').is_file(): p.error('run-root must be an existing recorded validation run')
if root not in archive.parents or not archive.is_file(): p.error('archive must be a regular run-owned file')
if root/'security' not in out.parents: p.error('output must be a child directory of RUN_ROOT/security')
if out.exists() and (not out.is_dir() or any(out.iterdir())): p.error('output must be new or empty; existing evidence is never overwritten')
cache = path(a.db_cache or str(root/'security/tooling/trivy-cache'))
if root/'security' not in cache.parents: p.error('DB cache must be beneath RUN_ROOT/security')
context = path(a.context) if a.context else None
if context and (root/'contexts' not in context.parents or not context.is_dir()): p.error('context must be a child directory of RUN_ROOT/contexts')
out.mkdir(parents=True, exist_ok=True)
status = {'status':'RUNNING','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'archive':str(archive),'network':'none','docker_socket_mounted':False,'host_bind_mounts':False,'transport':'task-owned named volumes populated by docker cp','checks':{}}
(out/'status.json').write_text(json.dumps(status,indent=2)+'\n')
transport=[]; volumes=[]; containers=[]
def local(cmd, timeout=120):
    item={'command':cmd};transport.append(item)
    (out/'transport.json').write_text(json.dumps(transport,indent=2)+'\n')
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout)
    item.update(exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr)
    (out/'transport.json').write_text(json.dumps(transport,indent=2)+'\n')
    if r.returncode: raise RuntimeError('Docker transport operation failed; see transport.json')
    return r.stdout.strip()
try:
    arch = {'aarch64':'arm64','arm64':'arm64','x86_64':'amd64','amd64':'amd64'}.get(platform.machine())
    if arch not in TOOLS: raise RuntimeError('No pinned scanner for host architecture')
    tool = TOOLS[arch]
    for name in ['trivy.db','metadata.json']:
        f = cache/'db'/name
        if not f.is_file() or f.is_symlink(): raise ValueError('Missing regular database file: '+name)
    metadata = json.loads((cache/'db/metadata.json').read_text())
    before = sha(archive)
    db_hash = sha(cache/'db/trivy.db')
    status.update(tool=tool,scanner_version='0.74.0',scanner_platform='linux/'+arch,archive_sha256=before,database_metadata=metadata,database_sha256=db_hash)
    with tarfile.open(archive,'r:*') as tf:
        names=[]
        for member in tf:
            parts=PurePosixPath(member.name)
            if parts.is_absolute() or '..' in parts.parts or member.issym() or member.islnk(): raise ValueError('Unsafe outer image archive member')
            names.append(member.name.lstrip('./'))
    if 'manifest.json' not in names and 'oci-layout' not in names: raise ValueError('Unrecognized image archive')
    name='dimple-f3-scan-'+uuid.uuid4().hex[:12]; label='io.dimple.validation-run='+root.name
    for suffix in ['input','db']:
        volume=name+'-'+suffix
        local(['docker','volume','create','--label',label,volume]);volumes.append(volume)
    helper=name+'-transfer'
    local(['docker','create','--name',helper,'--label',label,'--pull=never','--platform','linux/'+arch,'--network','none','--read-only','--cap-drop=ALL','--security-opt=no-new-privileges','--mount',f'type=volume,src={name}-input,dst=/input','--mount',f'type=volume,src={name}-db,dst=/database',tool,'version']);containers.append(helper)
    local(['docker','cp','-a',str(archive),helper+':/input/image.tar'])
    for filename in ['trivy.db','metadata.json']:
        local(['docker','cp','-a',str(cache/'db'/filename),helper+':/database/'+filename])
    base = ['docker','run','--rm','--pull=never','--platform','linux/'+arch,'--network','none','--read-only','--cap-drop=ALL','--security-opt=no-new-privileges','--user',f'{os.getuid()}:{os.getgid()}','--cpus','2','--memory','3g','--pids-limit','128','--tmpfs','/tmp:rw,noexec,nosuid,mode=1777,size=1536m','--tmpfs','/cache:rw,noexec,nosuid,mode=1777,size=256m','--env','HOME=/tmp','--label',label,'--mount',f'type=volume,src={name}-input,dst=/input,readonly','--mount',f'type=volume,src={name}-db,dst=/cache/db,readonly']
    common = ['--offline-scan','--skip-db-update','--skip-java-db-update','--skip-check-update','--skip-vex-repo-update','--disable-telemetry','--skip-version-check','--cache-dir','/cache','--timeout','10m','--format','json','--exit-code','0']
    commands={}
    def run_scan(label, command):
        scanner_name=name+'-'+label;containers.append(scanner_name)
        command=command[:2]+['--name',scanner_name]+command[2:]
        commands[label]=command
        (out/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
        with (out/(label+'.json')).open('w') as stdout,(out/(label+'.stderr.log')).open('w') as stderr:
            r=subprocess.run(command,stdout=stdout,stderr=stderr,timeout=660)
        status['checks'][label]={'exit_code':r.returncode,'status':'PASS' if r.returncode==0 else 'FAIL'}
        if r.returncode: raise RuntimeError(f'{label} scanner failed: exit {r.returncode}')
        j=json.loads((out/(label+'.json')).read_text())
        if 'SchemaVersion' not in j: raise ValueError('Invalid Trivy JSON')
        return j
    report=run_scan('image',base+[tool,'image',*common,'--scanners','vuln,secret,license','--image-config-scanners','secret','--license-full','--input','/input/image.tar'])
    vulnerabilities=[];secrets=[];licences=[]
    for result in report.get('Results',[]):
        for finding in result.get('Vulnerabilities',[]): vulnerabilities.append({'target':result.get('Target'),**finding})
        for finding in result.get('Secrets',[]): secrets.append({'target':result.get('Target'),'rule_id':finding.get('RuleID'),'severity':finding.get('Severity'),'title':finding.get('Title')})
        for finding in result.get('Licenses',[]): licences.append({'target':result.get('Target'),**finding})
    severity=Counter(v.get('Severity','UNKNOWN') for v in vulnerabilities)
    fixable_critical=[v for v in vulnerabilities if v.get('Severity')=='CRITICAL' and v.get('FixedVersion')]
    high=[v for v in vulnerabilities if v.get('Severity')=='HIGH']
    status['vulnerability_summary']={'severity_counts':dict(severity),'fixable_critical_count':len(fixable_critical),'high_count':len(high),'secret_finding_count':len(secrets),'licence_findings_count':len(licences)}
    status['current_release_security_gate']='FAIL' if fixable_critical or secrets else 'REVIEW_REQUIRED' if high else 'PASS_SCANNED_SCOPE'
    (out/'licence-inventory.json').write_text(json.dumps({'status':'INVENTORY_ONLY_REVIEW_REQUIRED','findings':licences},indent=2)+'\n')
    (out/'secrets-redacted-summary.json').write_text(json.dumps(secrets,indent=2)+'\n')
    if context:
        context_files=[]
        for f in sorted(context.rglob('*')):
            if f.is_symlink(): raise ValueError('Context symlinks are forbidden')
            if f.is_file(): context_files.append({'path':str(f.relative_to(context)),'size':f.stat().st_size,'sha256':sha(f)})
        (out/'context-manifest.json').write_text(json.dumps(context_files,indent=2)+'\n')
        local(['docker','cp','-a',str(context),helper+':/input/context'])
        context_report=run_scan('context',base+[tool,'filesystem',*common,'--scanners','secret,misconfig,license','--license-full','/input/context'])
        context_secrets=sum(len(x.get('Secrets',[])) for x in context_report.get('Results',[]))
        context_misconfig=sum(sum(y.get('Status')=='FAIL' for y in x.get('Misconfigurations',[])) for x in context_report.get('Results',[]))
        status['checks']['context'].update(secret_finding_count=context_secrets,misconfiguration_failure_count=context_misconfig)
        if context_secrets:status['current_release_security_gate']='FAIL'
        elif context_misconfig and status['current_release_security_gate']!='FAIL':status['current_release_security_gate']='REVIEW_REQUIRED'
    else:
        status['checks']['context']={'status':'NOT_RUN','reason':'No context path supplied; separate context evidence required'}
    if sha(archive)!=before or sha(cache/'db/trivy.db')!=db_hash: raise RuntimeError('Archive or database changed during scan')
    status.update(status='PASS',limitations=['Scanner success is distinct from current_release_security_gate. High findings require owned time-bounded exceptions; fixable Critical findings block current release.', 'Licence findings are an inventory, not completed redistribution review.', 'Image scan covers final filesystem/configuration; inspect all layers for deleted protected content separately.', 'No Java DB downloaded; unexpected Java package detection requires separate coverage review.'])
except BaseException as exc:
    status.update(status='FAIL',error=f'{type(exc).__name__}: {exc}')
finally:
    cleanup=[]
    for resource in reversed(containers):
        r=subprocess.run(['docker','rm','-f',resource],capture_output=True,text=True,timeout=30)
        if r.returncode and 'No such container' not in r.stderr:cleanup.append({'container':resource,'error':r.stderr})
    for resource in reversed(volumes):
        r=subprocess.run(['docker','volume','rm',resource],capture_output=True,text=True,timeout=30)
        if r.returncode:cleanup.append({'volume':resource,'error':r.stderr})
    status['cleanup_errors']=cleanup
    if cleanup:status['status']='FAIL'
    status['ended_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    status['artifacts']=[{'name':x.name,'size':x.stat().st_size,'sha256':sha(x)} for x in out.iterdir() if x.is_file() and x.name!='status.json']
    (out/'status.json').write_text(json.dumps(status,indent=2)+'\n')
print(json.dumps(status,indent=2))
sys.exit(0 if status['status']=='PASS' else 1)
PY
