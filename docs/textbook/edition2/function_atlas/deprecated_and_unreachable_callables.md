# Deprecated and unreachable callables

Static inspection of the current `dimple_gwas` package identified no package-defined Tier D callable. The user-facing `interpret` name is a supported compatibility alias for `explain`; it does not map to a second function. `legacy_dimple_score` is compatibility behavior but remains active and is not classified as deprecated. Historical Dev/Freeze 2 scripts outside the current package are migration evidence, not current package callables.

Nested local functions are retained in `function_inventory.tsv` as Tier C entries because they are executable callables inside current functions, but they are not public import targets and do not receive standalone textbook dossiers.
