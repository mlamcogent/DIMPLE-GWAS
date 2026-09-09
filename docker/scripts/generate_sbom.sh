#!/usr/bin/env bash
# Offline, immutable-tool SBOM generation. Output must be a new/empty run-owned directory.
# Usage: generate_sbom.sh --run-root RUN --archive IMAGE.tar --output RUN/sbom/IMAGE
set -euo pipefail
exec python3 - "$@" <<'PY'
import argparse, datetime, hashlib, json, os, platform, subprocess, sys, tarfile, uuid
from pathlib import Path, PurePosixPath

TOOLS = {
    'arm64': 'anchore/syft@sha256:0d7d157c1fc16d924c6b2c9667f9f8bfde3e2aa3c0e61c9223125e4c02e756ca',
    'amd64': 'anchore/syft@sha256:600896ff278677fb13b16dc35999452f4e79636fc098c9fee6ce3cffef9858e2',
}
p = argparse.ArgumentParser(description='Generate local SPDX, CycloneDX and Syft JSON from one closed image archive; no network or Docker socket in scanner.')
p.add_argument('--run-root', required=True)
p.add_argument('--archive', required=True)
p.add_argument('--output', required=True)
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
        for block in iter(lambda: f.read(1024 * 1024), b''): h.update(block)
    return h.hexdigest()

root, archive, out = map(path, (a.run_root, a.archive, a.output))
if root.parent.name != 'runs' or not (root/'inventory/source_identity.json').is_file():
    p.error('run-root must be an existing recorded validation run')
if root not in archive.parents or not archive.is_file(): p.error('archive must be a regular run-owned file')
if root/'sbom' not in out.parents: p.error('output must be a child directory of RUN_ROOT/sbom')
if out.exists() and (not out.is_dir() or any(out.iterdir())): p.error('output must be new or empty; existing evidence is never overwritten')
out.mkdir(parents=True, exist_ok=True)
status = {'status': 'RUNNING', 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'archive': str(archive), 'network': 'none', 'docker_socket_mounted': False, 'host_bind_mounts': False, 'transport':'task-owned named volume populated by docker cp'}
(out/'status.json').write_text(json.dumps(status, indent=2)+'\n')
transport=[]; volumes=[]; containers=[]
def local(cmd, timeout=90):
    item={'command':cmd}; transport.append(item)
    (out/'transport.json').write_text(json.dumps(transport,indent=2)+'\n')
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout)
    item.update(exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr)
    (out/'transport.json').write_text(json.dumps(transport,indent=2)+'\n')
    if r.returncode: raise RuntimeError('Docker transport operation failed; see transport.json')
    return r.stdout.strip()
try:
    arch = {'aarch64':'arm64', 'arm64':'arm64', 'x86_64':'amd64', 'amd64':'amd64'}.get(platform.machine())
    if arch not in TOOLS: raise RuntimeError('No pinned scanner available for host architecture')
    tool = TOOLS[arch]
    with tarfile.open(archive, 'r:*') as tf:
        names = []
        for member in tf:
            parts = PurePosixPath(member.name)
            if parts.is_absolute() or '..' in parts.parts or member.issym() or member.islnk():
                raise ValueError('Unsafe outer image archive member')
            names.append(member.name.lstrip('./'))
    kind = 'oci-archive' if 'oci-layout' in names else 'docker-archive' if 'manifest.json' in names else None
    if not kind: raise ValueError('Input is not an identifiable OCI or Docker-save image archive')
    digest_before = sha(archive)
    name='dimple-f3-sbom-'+uuid.uuid4().hex[:12]
    label='io.dimple.validation-run='+root.name
    local(['docker','volume','create','--label',label,name]); volumes.append(name)
    helper=name+'-transfer'
    local(['docker','create','--name',helper,'--label',label,'--pull=never','--platform','linux/'+arch,'--network','none','--read-only','--cap-drop=ALL','--security-opt=no-new-privileges','--mount',f'type=volume,src={name},dst=/input',tool,'version']); containers.append(helper)
    local(['docker','cp','-a',str(archive),helper+':/input/image.tar'])
    base=['docker','run','--rm','--pull=never','--platform','linux/'+arch,'--network','none','--read-only','--cap-drop=ALL','--security-opt=no-new-privileges','--user',f'{os.getuid()}:{os.getgid()}','--cpus','2','--memory','2g','--pids-limit','128','--tmpfs','/tmp:rw,noexec,nosuid,mode=1777,size=1536m','--env','SYFT_CHECK_FOR_APP_UPDATE=false','--env','HOME=/tmp','--label',label,'--mount',f'type=volume,src={name},dst=/input,readonly']
    scan_name=name+'-scan'; containers.append(scan_name)
    cmd=base+['--name',scan_name,tool,'scan',kind+':/input/image.tar','--scope','squashed','--parallelism','2','-o','syft-json']
    commands=[cmd]
    (out/'commands.json').write_text(json.dumps(commands, indent=2)+'\n')
    with (out/'sbom.syft.json').open('w') as stdout, (out/'stderr.log').open('w') as stderr:
        result = subprocess.run(cmd, stdout=stdout, stderr=stderr, timeout=900)
    status.update(tool=tool, scanner_platform='linux/'+arch, scanner_version='1.51.1', exit_code=result.returncode, archive_sha256=digest_before, source_type=kind)
    if result.returncode: raise RuntimeError(f'Syft exited {result.returncode}; see stderr.log')
    local(['docker','cp','-a',str(out/'sbom.syft.json'),helper+':/input/source.syft.json'])
    for format_name,filename in [('spdx-json','sbom.spdx.json'),('cyclonedx-json','sbom.cyclonedx.json')]:
        convert_name=name+'-'+format_name; containers.append(convert_name)
        cmd=base+['--name',convert_name,tool,'convert','/input/source.syft.json','-o',format_name]
        commands.append(cmd);(out/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
        with (out/filename).open('w') as stdout,(out/(filename+'.stderr.log')).open('w') as stderr:
            result=subprocess.run(cmd,stdout=stdout,stderr=stderr,timeout=180)
        if result.returncode: raise RuntimeError('SBOM format conversion failed: '+format_name)
    syft = json.loads((out/'sbom.syft.json').read_text())
    spdx = json.loads((out/'sbom.spdx.json').read_text())
    cdx = json.loads((out/'sbom.cyclonedx.json').read_text())
    if not syft.get('artifacts') or not spdx.get('spdxVersion') or cdx.get('bomFormat') != 'CycloneDX':
        raise RuntimeError('Missing packages or invalid SBOM format markers')
    packages = syft['artifacts']
    licence_rows = [{'name':x.get('name'), 'version':x.get('version'), 'type':x.get('type'), 'purl':x.get('purl'), 'licenses':x.get('licenses', []), 'locations':x.get('locations', [])} for x in packages]
    (out/'licence-inventory.json').write_text(json.dumps({'status':'INVENTORY_ONLY_REVIEW_REQUIRED','packages':licence_rows,'unknown_licence_count':sum(not x['licenses'] for x in licence_rows)}, indent=2)+'\n')
    if sha(archive) != digest_before: raise RuntimeError('Archive changed during scan')
    status.update(status='PASS', package_count=len(packages), application_packages=[{'name':x['name'],'version':x.get('version'),'type':x.get('type')} for x in packages if x.get('name','').lower().replace('_','-')=='dimple-gwas'], limitations=['SBOM inventory does not establish licence compliance or vulnerability absence.', 'Scope is the final squashed filesystem; deleted content needs separate layer inspection.'])
except BaseException as exc:
    status.update(status='FAIL', error=f'{type(exc).__name__}: {exc}')
finally:
    cleanup=[]
    for resource in reversed(containers):
        r=subprocess.run(['docker','rm','-f',resource],capture_output=True,text=True,timeout=30)
        if r.returncode and 'No such container' not in r.stderr: cleanup.append({'container':resource,'error':r.stderr})
    for resource in reversed(volumes):
        r=subprocess.run(['docker','volume','rm',resource],capture_output=True,text=True,timeout=30)
        if r.returncode: cleanup.append({'volume':resource,'error':r.stderr})
    status['cleanup_errors']=cleanup
    if cleanup: status['status']='FAIL'
    status['ended_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    status['artifacts'] = [{'name':x.name,'sha256':sha(x),'size':x.stat().st_size} for x in out.iterdir() if x.is_file() and x.name!='status.json']
    (out/'status.json').write_text(json.dumps(status, indent=2)+'\n')
print(json.dumps(status, indent=2))
sys.exit(0 if status['status']=='PASS' else 1)
PY
