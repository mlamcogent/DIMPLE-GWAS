# Freeze 3 Docker packaging

Publication update (2026-09-05): the current RC1 image is now public at
[zymlam/dimple-gwas](https://hub.docker.com/r/zymlam/dimple-gwas), following explicit
user authorization. Registry digest `sha256:e539d0efff63d3b6493ad6358eeb775218ee5616dc870acda23bfcf8c7f509d2`.
The publication receipt is in the recorded run’s `publication-current/` directory.
The qualification findings below are unchanged.

Current result: one runtime image built locally; requested two-image completion and
release qualification are blocked. Five malformed-input probes expose frozen-source
defects, and Critical/High security dispositions remain open. See the run's report
10 and the operator documents in `../docs/docker/` before using or distributing it.

This packages the unmodified, content-addressed Freeze 3 RC1 source as an offline,
non-root Linux AMD64 runtime. The current environment is dated 2026-09-05 and is
fully locked to verified wheel bytes. Core plotting uses Pillow; optional
Matplotlib and Plotly extras are not installed.

The requested exact historical Freeze 3 image is blocked: Python 3.9.13 does not
satisfy Freeze 3 metadata, and historical HDBSCAN 0.8.37 lacks the
`cluster_selection_persistence` option the application always uses. Even the
declared HDBSCAN floor 0.8.40 lacks it; 0.8.41 is the first suitable later release.
No installer override or scientific-source patch is applied. A compatibility
replacement is a separate scope decision. Do not call the current image a
completed two-image release, or infer historical scientific parity.

## Existing build evidence

See the explicit run directory supplied by the coordinator beneath
`../freeze3_workspace/docker_validation/runs/` relative to the package root.
Each run contains immutable source, package download hashes,
wheel, generated contexts, build logs, image manifests, tests, archive checksums,
security reports and release status. Never select an arbitrary run by name alone;
verify its `inventory/source_identity.json` and `wheel/wheel-manifest.json`.

## Rebuild an existing frozen context

For a newly prepared frozen run whose builder `b` and independent archive do not
already exist, use the following from the Freeze 3 package root:

```sh
export DIMPLE_RUN_ROOT=/absolute/path/to/docker_validation/runs/RUN_ID
python3 docker/scripts/pipeline.py create-builder --run-root "$DIMPLE_RUN_ROOT" --builder-suffix b
python3 docker/scripts/pipeline.py rebuild-current --run-root "$DIMPLE_RUN_ROOT" --builder-suffix b
```

The independent rebuild reuses the frozen wheel and locks, uses an isolated
builder without shared task cache, and writes a new OCI archive with provenance.
It refuses existing output files. It never overwrites the locally loaded image.
The digest-pinned base and builder may need to be downloaded; package installation
inside build steps has no network access. The scripts never publish.
Both builders and archives already exist in the completed current run. Do not
replay these commands against that run. Its `logs/rebuild-current.json` records
the tested concrete build command; another reconstruction needs a fresh output
and task-owned builder identity. Existing evidence is deliberately not overwritten.

For a fresh run, first create its source identity manifest and immutable source
snapshot according to the main run macro. Then fetch approved wheels using
`current/fetch_locked_wheels.py`; generate `wheel` context using
`scripts/prepare_contexts.sh wheel`; create builder `a`; build and checksum the
single wheel; generate `current` context; build runtime/test targets. Every
wrapper accepts `--run-root`. Existing source snapshots, contexts, tags and logs
are preserved. The shared Dockerfile must be copied into a generated context,
never invoked against the multi-gigabyte research workspace.

## Run

```sh
docker run --rm --platform linux/amd64 --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges=true \
  --tmpfs /tmp:rw,noexec,nosuid,size=2147483648,mode=1777 \
  dimple-gwas:VERSION-SOURCE-LOCK-current-amd64 --help
```

Use the actual tag in the run's image manifest. For data execution, mount input
read-only at `/data/input` and a new writable destination at `/data/output`.
The configured user is UID/GID 10001. If host folder sharing works, a host UID/GID
override may be used to write host-owned outputs while remaining non-root.
On this Mac, workspace bind mounts stalled before container creation; use the
validated task-volume transfer mode below instead of changing Docker settings.

## Bounded scientific validation

Create a bootstrap folder containing `validation/harness.py`, the run's sealed
`comparisons/preregistered_acceptance_criteria.json`, and all seven shipped YAMLs
in `configs/`. Then:

```sh
DIMPLE_VOLUME_TRANSPORT=1 docker/scripts/run_three_lane_validation.sh \
  ACTUAL_CURRENT_IMAGE /absolute/bootstrap /absolute/new-validation-output
```

This uses task-specific Docker volumes and `docker cp` instead of host bind
mounts, retaining transport evidence. It runs scientific commands offline as
UID/GID 10001 with a read-only root. Input and output volumes are separate.
Only non-sensitive generated fixtures belong in this bundled validation. The
native 45-case suite uses the separate test image and an external, read-only
test-source tree; the original Dev monolith appears there solely for a hash
guard. It is absent from runtime images and exports.

Read per-command statuses and the final gate report. A harness failure is not
silently waived by passing unit tests. This is emulated AMD64 engineering
evidence; native qualification, the historical 1,000-seed fit, GCP/AWS and
biological validation remain separate.

## Archives, scans and publication

`export_oci_images.sh` currently writes the available current runtime as a
Docker-save archive, an equivalent portable image artifact, verifies its tag
manifest and records SHA-256 after the file closes. Independent rebuilding
additionally produces a true OCI archive. Neither exports the Dev reference or
test image. Scanner scripts accept an explicit closed archive and fresh
run-owned output destination; tools are digest-pinned and inspect artifacts
offline after a separate public database download.

`publication_dry_run.sh` prints proposed immutable tags under `zymlam` and
commands only. Public visibility is the user's stated preference. Do not publish
an image whose scientific/security/licence gates remain unreviewed or blocked.
No `latest` tag is used. Runtime image identity, archive format and registry
manifest digest are distinct and must not be conflated.
