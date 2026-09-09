# External container validation

`harness.py` imports the installed wheel and rejects a source-checkout import.
It is mounted externally; it and native tests must not enter the release image.
The sealed criteria hash is checked before every invocation. Original scientific
code and research artifacts are never edited by this harness.

Import checks read the image's declared runtime lock. Missing Matplotlib/Plotly
extras excluded from that lock are recorded `NOT_INSTALLED_OPTIONAL`; every core
dependency, including Pillow and Excel engines, remains required. An installed
but broken optional extra is still a failure.

Create a bootstrap directory containing `harness.py`, the sealed
`preregistered_acceptance_criteria.json`, and `configs/` containing all seven
shipped YAML files. Then use:

```text
docker/scripts/run_three_lane_validation.sh IMAGE /absolute/bootstrap /absolute/new-validation-root
```

The name reflects the reporting contract. The script executes current Lane C;
it explicitly records exact historical Lanes A and B as incomplete. Native tests
remain separately coordinator-owned: mount the staged validation tree read-only
at `/validation`, use cwd `/validation/DIMPLE-GWAS-freeze3`, and invoke the locked
test overlay against the installed package. The sibling Dev monolith exists only
in that test mount for the authoritative-hash test. Expect all 45 collected cases
and report every failure/skip/deselection rather than selecting a safe subset.

For individual modes:

```text
docker/scripts/run_smoke_tests.sh IMAGE /absolute/shared /absolute/empty-output MODE [OPTIONS]
```

On Docker Desktop hosts where bind-mounted starts stall, set
`DIMPLE_VOLUME_TRANSPORT=1`. This uses unique labeled named input/output volumes,
a stopped transfer container and `docker cp`, with no host bind mounts. Scientific
commands run as UID/GID 10001 with the same hardening. A nonroot ownership probe
uses root with only CHOWN only if the new empty output root requires ownership
initialization. `volume_transport/transport_manifest.json` records the exact
container exit, volume/container identities, copying and retained diagnostics.
Volumes and stopped containers are retained by default; optional
`DIMPLE_CLEAN_TRANSPORT_AFTER_EXPORT=1` permits cleanup after output retrieval.
The default portable bind mode runs with the invoking host's nonroot UID/GID.

Container API:

```text
python /data/input/harness.py MODE --input /data/input --output /data/output
```

`prepare` generates and hashes non-sensitive synthetic and analytic fixtures.
Copy its fixture files plus the harness/configs/criteria to a shared read-only
input directory before running other modes. `checks` covers imports, all CLI
help/config/enumeration checks, and independent analytic oracles. `fit` runs and
validates one fixed fixture, preserving preprocessed matrix and complete native
artifacts. Invoke it twice in separate fresh containers. `compare --left PATH
--right PATH` compares these retained run directories under sealed same-image
criteria. `postprocess --left PATH` exercises rescoring, summaries, model
reproduction, native comparison, Pearson/Spearman explanation, and isolated/tied
stressors. Stress outcomes reconcile the candidate table, manifest and failure
ledger and inspect the validator result. Failed candidates fail the probe;
native invalid-topology outcomes are `INCOMPLETE` even when the command exits
zero. No preferred cluster/noise count is asserted. `failures --left PATH` exercises malformed inputs, configurations and
tampered checksum behavior while preserving originals.

Every mode refuses nonempty output, records command/UTC/exit/stdout/stderr and
resource-use evidence, and writes `harness_report.json`. A failed expected-error
probe is a failure finding even if other modes pass. `PASS_WITH_LIMITATIONS`
preserves missing evidence. Current public artifacts do not retain membership
probabilities, outlier scores, per-cluster persistence or condensed trees; those
are marked `NOT_EMITTED`. The complete embedding is recoverable from the fixed
one-seed fixture's visualization only because it has exactly one seed. This
harness refuses to infer full multi-seed geometry from visualization columns.

Canonical platform is linux/amd64; report emulation on Apple Silicon and preserve
the separate native AMD64 gate. Fresh 164-IDP fitting and registry publication are
outside these scripts. `run_164_idp_protocol.sh --plan` prints the separate pending
scientific protocol.
