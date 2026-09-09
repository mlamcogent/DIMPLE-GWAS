# Built current image: local evaluation only

Run evidence: `/Users/maxlam/Downloads/Cogent-analysis-audit/DIMPLE-GWAS/freeze3_workspace/docker_validation/runs/20260905T083643Z-774bbf2de95d-33a471`. Read `reports/10_release_readiness_report.md` before use.
Current image: `dimple-gwas:3.0.0rc1-774bbf2de95d-98637ae3352c-current-amd64`. Image/config ID: `sha256:a5543cdaacaa3c9e8027df8e846a1352832ef2da3fe224df3be9cd465ea7ef03`.
Platform Linux AMD64; this Mac executed it under emulation. One runtime image exists;
the separate test-overlay image is not the requested second historical runtime.

## Load and identify

The archive is portable and may be loaded on a separately authorized native AMD64 host.
Verify its hash before loading; the manifest records the exact image ID after loading.

```sh
export DIMPLE_RUN_ROOT='/Users/maxlam/Downloads/Cogent-analysis-audit/DIMPLE-GWAS/freeze3_workspace/docker_validation/runs/20260905T083643Z-774bbf2de95d-33a471'
shasum -a 256 "$DIMPLE_RUN_ROOT/oci/current.docker.tar"
docker load --input "$DIMPLE_RUN_ROOT/oci/current.docker.tar"
docker image inspect 'dimple-gwas:3.0.0rc1-774bbf2de95d-98637ae3352c-current-amd64' --format '{{.Id}}'
```

Expected archive SHA256: `208fe7569ad4af268a4749289b550cc78efb9967b7f0789c59ec24b2b19f72a5`.
Loading does not attach the separate OCI provenance or SBOM to Docker's classic image store.

## Offline run contract

```sh
docker run --rm --platform linux/amd64 --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges=true \
  --cpus 2 --memory 6g --pids-limit 256 \
  --tmpfs /tmp:rw,noexec,nosuid,size=2147483648,mode=1777 \
  'dimple-gwas:3.0.0rc1-774bbf2de95d-98637ae3352c-current-amd64' --help
```

Run as UID/GID10001. Inputs go read-only at `/data/input`; outputs use a new writable
volume at `/data/output`. The runtime root is read-only. Temporary caches use `/tmp`.
OMP/OpenBLAS/MKL/Numba threads and PYTHONHASHSEED are fixed to1/0 in the runtime profile.

On this Mac, workspace host bind mounts stall before container creation. Do not change
Desktop sharing settings implicitly. The tested fixture helper uses isolated named
volumes and `docker cp`; it preserves container inspections and output evidence.

```sh
DIMPLE_VOLUME_TRANSPORT=1 '/Users/maxlam/Downloads/Cogent-analysis-audit/DIMPLE-GWAS/DIMPLE-GWAS-freeze3/docker/scripts/run_three_lane_validation.sh' \
  'dimple-gwas:3.0.0rc1-774bbf2de95d-98637ae3352c-current-amd64' "$DIMPLE_RUN_ROOT/source/bootstrap" \
  "$DIMPLE_RUN_ROOT/comparisons/operator-rerun-$(date -u +%Y%m%dT%H%M%SZ)"
```

This takes about five minutes here for the original bounded matrix. It deliberately
returns nonzero because five malformed-input probes expose frozen-source defects.
Never interpret process exit0 alone as a successful scientific model: also inspect
candidate statuses, selection, validation output and identifier uniqueness.

## Rebuild

The recorded independent build is `logs/rebuild-current.json` and `.log`. It uses
builder `dimple-33a471-b`, `--no-cache`, the frozen generated current context, exact
source/wheel/lock arguments and `SOURCE_DATE_EPOCH=1787195002`. The resulting OCI archive
has the same config and all11 decompressed layers as the original image. Inspect the
recorded command for a fully concrete invocation. Do not overwrite its output or logs.
A new build needs a fresh run/output and builder identity. `docker/README.md` describes
frozen-input preparation and helper sequencing. Never build against the research workspace.

The build check on this ARM host reports an AMD64-versus-ARM64 warning despite explicit
AMD64 target arguments; both raw failed check outputs remain recorded. Loaded image and
OCI config, base child digest, runtime x86_64 probe and successful execution establish
the built architecture. No warning was suppressed or silently called passed.
