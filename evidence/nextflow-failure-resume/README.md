# Retained real Nextflow failure/resume evidence

This is the existing local synthetic 60×3 standalone-PCA test from 11 November 2026, 01:23 SGT, not a new run and not AWS/GCP qualification. The workflow process retains the historical name UMAP_CHUNK although the selected backend is PCA.

COMMANDS.txt and history.txt retain both actual launch commands and session identity. failure-wrapper.sh is the original injection wrapper with only the local workspace prefix normalized: on the first research.py grid invocation, it creates fail_once, emits INTENTIONAL_ONCE_GRID_FAILURE and exits 77; subsequent invocations use the scientific Python environment. It was selected through the test PATH. The two concurrent GRID tasks can race; the retained first trace records one FAILED/77 and one ABORTED.

On resume of the same session and work directory, PREPARE, UMAP_CHUNK (PCA) and CONCAT are CACHED (3); both GRID tasks and RANK are COMPLETED (3). The final Nextflow log independently records succeededCount=3, failedCount=0, cachedCount=3. Both earlier attempt traces/logs are bundled separately and were not overwritten. The underlying test used direct Nextflow; launcher-specific resume was separately tested with a shim, as the original validation document states.

Only the absolute local workspace prefix is replaced with WORKSPACE in public copies. PROVENANCE.json records original and bundled SHA-256s and exact source-relative paths. Task hashes, status, exit codes, timestamps, session UUID and counts are unchanged. These evidence files are historical records, not a portable rerun script. The original local evidence remains untouched.
