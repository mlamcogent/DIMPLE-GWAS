"""Build or verify the deterministic, allowlisted Freeze 5.3 source archive."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import stat
import tarfile

ROOT = Path(__file__).resolve().parents[1]
NAMES = (
    'deploy/gcp-prerequisites.sh', 'tests/test_gcp_alignment.py',
    'bin/plan_gcp.py', 'docs/DEPLOY_GCP.md', 'docs/INTEROPERABILITY.md', 'docs/VALIDATION_5_3.md', 'examples/deployment.gcp.example.json', 'tests/test_multicloud.py',
    'bin/runner_stack.py', 'bin/launch_attempt.py', 'bin/export_evidence.py', 'bin/stop_run.py', 'docs/DEPLOY_FIXES.md', 'bin/science_config.py', 'bin/dimple_representations/__init__.py', 'bin/dimple_representations/config.py', 'bin/dimple_representations/pca_runner.py', 'bin/dimple_representations/ica_runner.py', 'bin/dimple_representations/hdbscan_runner.py', 'CITATION.cff', 'examples/science-custom.example.json', 'examples/science-pca.example.json', 'examples/science-ica.example.json', 'docs/QUICKSTART.md', 'docs/PARAMETER_FIX_VALIDATION.md', 'tests/test_intake_drops.py', 'tests/test_custom_science.py', '.dockerignore', '.gitignore', 'LICENSE', 'README.md', 'VERSION', 'main.nf', 'nextflow.config',
    'source_manifest.json', 'bin/freeze5_scoring.py', 'bin/matrix_intake.py', 'bin/pack_release.py',
    'bin/plan_batch.py', 'bin/research.py', 'conf/recipe.json', 'conf/source-origin.json',
    'deploy/Dockerfile', 'deploy/batch.yaml', 'deploy/requirements-linux-amd64.lock',
    'docs/ATTRIBUTION.md', 'docs/DEPLOY.md', 'docs/LOCAL_VALIDATION.md', 'docs/MANUAL.md',
    'docs/RELEASE.md', 'docs/SCIENCE.md', 'examples/deployment.example.json',
    'examples/synthetic-matrix.csv', 'examples/synthetic-transposed.csv', 'tests/test_portable.py', 'tests/test_deploy_fixes.py',
)
MANIFEST = 'EXPORT_MANIFEST.json'
PRIVATE = re.compile(
    rb'/(?:Users|home)/[^/\r\n]+/|'
    rb'arn:aws:[^ \r\n]*:[0-9]{12}:|\b(?:AKIA|ASIA)[A-Z0-9]{16}\b|'
    rb'BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|gh[pousr]_[A-Za-z0-9]{30,}'
)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def source(root, exported=False):
    entries = {}
    for path in root.rglob('*'):
        if path.is_symlink():
            raise ValueError('linked export path')
        if not path.is_dir():
            entries[path.relative_to(root).as_posix()] = path
    expected = set(NAMES) | ({MANIFEST} if exported else set())
    if set(entries) != expected:
        raise ValueError(f'export paths differ from allowlist: {sorted(set(entries) ^ expected)}')
    data = {}
    for name in NAMES:
        path = entries[name]
        metadata = path.lstat()
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1 or metadata.st_size > 256 * 1024:
            raise ValueError(f'unexpected export member: {name}')
        raw = path.read_bytes()
        raw.decode('utf-8')
        if PRIVATE.search(raw):
            raise ValueError(f'private identifier or secret pattern in {name}')
        data[name] = raw
    runtime = json.loads(data['source_manifest.json'])
    if not runtime or any(name not in data or sha(data[name]) != digest for name, digest in runtime.items()):
        raise ValueError('staged runtime source manifest differs from export')
    return data


def manifest(data):
    return {'schema': 'dimple.freeze5.3.export/v1', 'version': data['VERSION'].decode().strip(),
            'files': {name: {'bytes': len(raw), 'mode': '0644', 'sha256': sha(raw)}
                      for name, raw in sorted(data.items())}}


def verify(root):
    data = source(root, exported=True)
    expected = manifest(data)
    if json.loads((root / MANIFEST).read_text(encoding='utf-8')) != expected:
        raise ValueError('export manifest differs from exact extracted bytes')
    if any(stat.S_IMODE((root / name).stat().st_mode) != 0o644 for name in (*NAMES, MANIFEST)):
        raise ValueError('export file mode differs from 0644')
    return expected


def pack(root, output):
    data = source(root)
    identity = manifest(data)
    manifest_bytes = (json.dumps(identity, indent=2, sort_keys=True) + '\n').encode()
    data[MANIFEST] = manifest_bytes
    with output.open('xb') as stream, gzip.GzipFile(filename='', mode='wb', fileobj=stream, mtime=0) as zipped:
        with tarfile.open(fileobj=zipped, mode='w', format=tarfile.USTAR_FORMAT) as archive:
            for name, raw in sorted(data.items()):
                info = tarfile.TarInfo(name)
                info.size = len(raw)
                info.mode = 0o644
                archive.addfile(info, io.BytesIO(raw))
    return {'files': len(data), 'bytes': output.stat().st_size, 'sha256': sha(output.read_bytes()),
            'export_manifest_sha256': sha(manifest_bytes)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--output', type=Path)
    mode.add_argument('--verify', type=Path)
    args = parser.parse_args()
    try:
        result = verify(args.verify) if args.verify else pack(ROOT, args.output)
    except (OSError, ValueError) as error:
        parser.exit(2, f'Export refused: {error}\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
