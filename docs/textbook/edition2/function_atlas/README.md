# Function atlas scope and Gate 1 report

The inventory denominator is **110 package-defined callable or callable-data symbols** across current `dimple_gwas/*.py` modules. It includes module functions, class definitions, class methods, and nested local functions; it excludes imported third-party callables and names merely referenced from dependencies.

| Classification | Count |
| --- | ---: |
| Tier A — user-facing/core analytical | 42 |
| Tier B — important supporting/public named | 36 |
| Tier C — private/local mechanical | 32 |
| Tier D — deprecated/unreachable | 0 |
| Module functions | 107 |
| Classes | 1 |
| Methods | 0 |
| Nested local functions | 2 |

Every symbol has a source location, visibility, tier, purpose, caller/dependency mapping, signature, explicit-raise summary, state/output behavior, direct test-name matches, example route, planned chapter, and evidence status. Every Tier A/B symbol has a planned coverage form and a 20-field dossier checklist. Zero direct name matches in a test do not automatically mean untested: integration tests frequently reach private helpers through a public caller, and that distinction will be resolved during the final coverage audit.

Gate 1 status: **pass for discovery, classification, and planned coverage**. Gate C remains pending until every Tier A/B dossier field is completed and integration coverage is adjudicated.
