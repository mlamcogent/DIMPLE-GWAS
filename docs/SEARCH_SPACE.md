# Search Space

## Precedence

Resolution order is:

1. built-in search-mode defaults;
2. YAML values;
3. explicit CLI values.

The resolved configuration is validated and written before fitting. Scalars and one-element lists are equivalent. Numeric fields also accept exclusive-stop ranges such as `2:20:2` or YAML `{start: 2, stop: 20, step: 2}`.

## Modes

| Mode | Purpose | Built-in candidate count |
|---|---|---:|
| `standard` | Dev-compatible UMAP defaults and HDBSCAN grid | 2,430 |
| `extended` | Broader UMAP/HDBSCAN geometry, leaf/EOM, bounded/unbounded size | 1,728 |
| `custom` | YAML-defined scalar/list product | configuration-dependent |
| `fixed` | One complete model | 1 |

Candidate count is the product of all UMAP-list lengths and all HDBSCAN-list lengths. Freeze 3 warns above `execution.warn_candidate_count`. It never silently samples or truncates the Cartesian product. A positive `execution.max_candidate_models` rejects an oversized grid and asks the user to narrow it or raise the explicit cap.

## Validation

Validation rejects:

- empty/malformed/zero-step ranges;
- non-finite numeric values;
- unsupported metric names;
- UMAP `n_neighbors < 2`, invalid dimensions, rates, or mixture bounds;
- `min_dist > spread` in any searched pairing;
- HDBSCAN `min_cluster_size < 2`, `min_samples < 1`, negative epsilon/persistence, or non-positive alpha;
- selection methods other than `eom` and `leaf`;
- negative maximum sizes or any nonzero `max_cluster_size < min_cluster_size` pairing;
- list-valued parameters in fixed mode;
- invalid execution bounds and undeclared custom-score directions.

Runtime errors that depend on the actual data remain candidate failures and do not crash a non-strict search.

## Identity and manifests

UMAP, HDBSCAN, and full-model identifiers are SHA-256 prefixes of canonical, sorted JSON parameters. They do not depend on enumeration order or score. The complete pre-fit grid is written to:

```text
search_space_manifest.tsv
search_space_manifest.json
```

Each record contains ordinal, stable IDs, model family, and every searched parameter. The JSON manifest explicitly states that enumeration is complete and deterministic.

## Search design cautions

`leaf` usually yields finer topology than EOM. A restrictive maximum size can force EOM toward smaller clusters but has no effect under leaf selection. Distance metrics change the estimand of similarity. These controls belong in the search space; they do not belong as hidden winner-selection targets.
