# Current Linux AMD64 dependency artifacts

The selected environment is dated 2026-09-05: Python 3.12.14 with the numerical
versions exercised by the prior Freeze 3 macOS validation. The Linux build and
scientific gates must still qualify this candidate. Optional Plotly/Matplotlib
extras are excluded; the package's core visualization uses Pillow.

`wheel_plan.json` records the approved exact versions, filenames, hashes, groups,
source identity and immutable AMD64 base. `runtime.lock`, `test.lock` and
`build.lock` pin the full runtime closure, current test overlay and wheel-building
tools respectively. The first two groups share no distributions; packaging is
shared by the test and build groups. There are 31 distinct wheels overall.

Fetch without installing anything on the host:

```sh
python3 docker/current/fetch_locked_wheels.py --run-root /absolute/path/to/run --phase build
python3 docker/current/fetch_locked_wheels.py --run-root /absolute/path/to/run --phase all
```

Run those commands from the Freeze 3 package root. The script uses only Python's
standard library, fetches exact-version metadata from `pypi.org` and wheel bytes
from `files.pythonhosted.org`, and verifies filenames, published hashes, local
hashes, lengths and the distribution's top-level wheel metadata. Existing files
are verified and are never replaced. No source distribution, host installation
or floating resolver is used. `--phase build` makes the six build tools available
first; `--phase all` finishes runtime and test dependencies.

Run artifacts live beneath `builds/lane_c/`: `wheelhouse/`, `metadata/`, copied
`locks/`, `wheel_plan.json`, `build-artifacts.json` and `artifact-manifest.json`.
The manifests contain the exact source URLs, downloaded SHA256 values, metadata
hashes, sizes and group membership. Invocation records and detailed event logs
live beneath `logs/lane_c/`. Verification failures remain in those logs.

## Shared Dockerfile integration recommendation

Use this exact current base and explicit `--platform=linux/amd64`:

```text
python:3.12.14-slim-bookworm@sha256:9c47360a2a0355e2da18516d0b1c2126ec22c195d2185e97347c9d98398c5bef
```

The coordinator owns the shared Dockerfile. Create a `freeze3-wheel` stage with
an isolated build environment and install `build.lock` offline. Build the pure
Python application wheel once using `python -m build --wheel --no-isolation`.
Export its physical bytes and checksum before either runtime installs it.

For `current-environment`, create a venv with `--without-pip` and install only
`runtime.lock`, then the one frozen application wheel with `--no-deps`.
The already verified pip wheel can run from a temporary ZIP import path, avoiding
an unpinned bootstrap upgrade and avoiding pip inside the runtime venv:

```sh
PYTHONPATH=/wheelhouse/pip-26.2.1-py3-none-any.whl /opt/runtime/bin/python -m pip install \
  --no-index --find-links=/wheelhouse --only-binary=:all: --require-hashes \
  -r /locks/runtime.lock
```

Use BuildKit read-only wheelhouse mounts or intermediate stages so downloaded
wheels and metadata never enter the final image layers. Verify the application
wheel checksum explicitly before installing it. Retain the hash inside runtime
provenance and independently verify the installed package identity.

Derive `freeze3-current-test` from the completed application environment and add
only `test.lock` plus safe test sources. The final `freeze3-current-runtime`
must instead use the runtime environment before the test overlay. Keep build,
test and package-installation tooling out of that final image, including the
bootstrap pip already present in the official base if the coordinator can remove
it without disturbing the Python runtime. Keep installed wheel and OS licenses.

No apt installation is planned. Verify imports and shared-library resolution
before adding any OS library; missing libraries require exact package versions,
download hashes and a recorded snapshot source. Record actual BLAS/LAPACK,
OpenMP, libc and OS package manifests from the image. Use the macro's non-root,
offline, read-only root and writable temporary/cache profile and validate it
with real execution.

The wheel availability audit and download verification do not pass pip resolution,
Linux import, unit/scientific, security, native AMD64 or two-image release gates.
