# Technical reference: errors and recovery

| Failure surface | Typical cause | Evidence-preserving response |
|---|---|---|
| parser exit | missing command or invalid option | read live help; retain command and stderr |
| configuration error | unknown key, bad type/range, unsupported metric, invalid interaction | inspect resolved inputs; correct YAML/override into a new command record |
| input error | missing file, delimiter, metadata prefix, nonnumeric/missing values, duplicate IDs | repair upstream or issue a new validated input; never silently impute through the pipeline |
| occupied output root | path already contains artifacts | choose a new root; preserve existing evidence |
| candidate `failed` | backend/runtime exception | keep failure row/log; inspect family pattern and environment |
| candidate `invalid_topology` | fewer than two non-noise clusters or unusable diagnostic | retain as an evaluated structural outcome |
| optional Parquet/XLSX issue | absent optional dependency or unsupported source | use native required artifacts; install only in an approved isolated environment if coverage is required |
| explanation ID mismatch | wrong orientation/key/table or genuinely different populations | require exact match; use incomplete mode only with explicit exclusions |
| hash mismatch | stale, modified or substituted artifact | stop interpretation; recover immutable source or document the change |
| validation failure | missing/schema/count/hash inconsistency | repair by a new derivation; do not edit the manifest to match the defect |

An exception is not permission to change the scientific method. Preserve the failing evidence, isolate the cause, and rerun only into a fresh root.

\newpage
