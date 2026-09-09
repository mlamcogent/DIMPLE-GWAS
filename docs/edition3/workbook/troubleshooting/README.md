# Troubleshooting and recovery

## Start with the evidence layer

- **Parser or configuration failure:** inspect current `--help`, resolved precedence, types, choices, and validation errors.
- **Input failure:** verify orientation, metadata prefix, numeric conversion, missingness, delimiter/sheet, and identifiers before changing analysis parameters.
- **Occupied output directory:** choose a new path; do not delete evidence to satisfy the command.
- **Candidate failure:** retain the failure row and log; distinguish backend exception from invalid topology.
- **Unexpected label change:** compare source, config, seed, dependency, architecture, threads, IDs, and hashes before interpreting science.
- **Explanation mismatch:** use exact identifier sets by default; investigate orientation and join keys rather than allowing silent exclusions.
- **Missing Parquet or XLSX support:** confirm optional dependencies and whether the run treats failure as warning or strict error.
- **Slow or oversubscribed run:** inspect candidate and UMAP-family counts, repeated seeds, job settings, BLAS/OpenMP threads, JIT warm-up, and memory.

## Recovery rule

Preserve the failed root. Correct one identified cause, document the change, and write a new root. A clean rerun that hides its predecessor is less reproducible than a failed attempt with an intelligible lineage.

\newpage
