# Appendix A — Complete command-line reference

The following grammar was captured from the fresh Edition 2 environment. `interpret` is a compatibility alias for `explain`; both were executed in Lab 3. `python -m dimple_gwas` reaches the same dispatcher.

## Top-level dispatcher

```text
usage: dimple-gwas [-h] [--version]
                   {run,inspect-config,show-search-space,score-existing,summarize-models,reproduce-model,explain,interpret,compare,validate}
                   ...

DIMPLE-GWAS Freeze 3 topology search and original-space interpretation

positional arguments:
  {run,inspect-config,show-search-space,score-existing,summarize-models,reproduce-model,explain,interpret,compare,validate}
    run                 Run UMAP/HDBSCAN topology search
    inspect-config      Resolve and validate configuration
    show-search-space   Enumerate candidate models without fitting
    score-existing      Apply a declared score to an existing model table
    summarize-models    Create family and Pareto summaries
    reproduce-model     Re-run a retained model artifact
    explain (interpret)
                        Explain retained labels in the original input space
                        without refitting
    compare             Compare two retained clustering artifacts by exact IDs
    validate            Validate run schemas, artifacts, and recorded hashes

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
```

## `inspect-config`

```text
usage: dimple-gwas inspect-config [-h]
                                  [--search-mode {standard,extended,custom,fixed}]
                                  [--config CONFIG] [--input INPUT_PATH]
                                  [--drop-first-n-cols DROP_FIRST_N_COLS]
                                  [--sep SEP] [--zscore-transform {none,rint}]
                                  [--annotation-file ANNOTATION_FILE]
                                  [--annotation-index-col ANNOTATION_INDEX_COL]
                                  [--umap-n-neighbors UMAP_N_NEIGHBORS]
                                  [--umap-min-dist UMAP_MIN_DIST]
                                  [--umap-n-components UMAP_N_COMPONENTS]
                                  [--umap-metric UMAP_METRIC]
                                  [--umap-spread UMAP_SPREAD]
                                  [--umap-learning-rate UMAP_LEARNING_RATE]
                                  [--umap-repulsion-strength UMAP_REPULSION_STRENGTH]
                                  [--umap-negative-sample-rate UMAP_NEGATIVE_SAMPLE_RATE]
                                  [--umap-local-connectivity UMAP_LOCAL_CONNECTIVITY]
                                  [--umap-set-op-mix-ratio UMAP_SET_OP_MIX_RATIO]
                                  [--random-state UMAP_RANDOM_STATE]
                                  [--densmap] [--no-densmap]
                                  [--hdbscan-min-cluster-size HDBSCAN_MIN_CLUSTER_SIZE]
                                  [--hdbscan-min-samples HDBSCAN_MIN_SAMPLES]
                                  [--hdbscan-cluster-selection-epsilon HDBSCAN_CLUSTER_SELECTION_EPSILON]
                                  [--hdbscan-cluster-selection-persistence HDBSCAN_CLUSTER_SELECTION_PERSISTENCE]
                                  [--hdbscan-cluster-selection-method HDBSCAN_CLUSTER_SELECTION_METHOD]
                                  [--hdbscan-alpha HDBSCAN_ALPHA]
                                  [--hdbscan-allow-single-cluster HDBSCAN_ALLOW_SINGLE_CLUSTER]
                                  [--hdbscan-max-cluster-size HDBSCAN_MAX_CLUSTER_SIZE]
                                  [--hdbscan-metric HDBSCAN_METRIC]
                                  [--n-random-states N_RANDOM_STATES]
                                  [--n-jobs N_JOBS]
                                  [--candidate-jobs CANDIDATE_JOBS]
                                  [--top-n-models TOP_N_MODELS]
                                  [--warn-candidate-count WARN_CANDIDATE_COUNT]
                                  [--max-candidate-models MAX_CANDIDATE_MODELS]
                                  [--max-samples-trust MAX_SAMPLES_TRUST]
                                  [--max-samples-silhouette MAX_SAMPLES_SILHOUETTE]
                                  [--trust-k TRUST_K]
                                  [--trust-seed TRUST_SEED]
                                  [--silhouette-seed SILHOUETTE_SEED]
                                  [--legacy-ensemble-seeds]
                                  [--no-legacy-ensemble-seeds]
                                  [--compute-dbcv] [--no-compute-dbcv]
                                  [--write-parquet] [--no-write-parquet]
                                  [--strict]
                                  [--scoring-profile {legacy_dimple,custom}]
                                  [--fit-include-noise] [--fit-exclude-noise]
                                  [--output OUTPUT]

options:
  -h, --help            show this help message and exit
  --search-mode {standard,extended,custom,fixed}
  --config CONFIG       YAML configuration; explicit CLI values override it
  --input INPUT_PATH, --datainput INPUT_PATH
                        GWAS summary-statistics matrix (CSV/TSV)
  --drop-first-n-cols DROP_FIRST_N_COLS, --drop_first_n_cols DROP_FIRST_N_COLS
  --sep SEP
  --zscore-transform {none,rint}, --zscore_transform {none,rint}
  --annotation-file ANNOTATION_FILE, --annotation_file ANNOTATION_FILE, --idp_key ANNOTATION_FILE
  --annotation-index-col ANNOTATION_INDEX_COL, --annotation_index_col ANNOTATION_INDEX_COL
  --umap-n-neighbors UMAP_N_NEIGHBORS, --n-neighbors UMAP_N_NEIGHBORS, --n_neighbors UMAP_N_NEIGHBORS
  --umap-min-dist UMAP_MIN_DIST, --min-dist UMAP_MIN_DIST, --min_dist UMAP_MIN_DIST
  --umap-n-components UMAP_N_COMPONENTS, --n-components UMAP_N_COMPONENTS, --n_components UMAP_N_COMPONENTS
  --umap-metric UMAP_METRIC, --umap_metric UMAP_METRIC
  --umap-spread UMAP_SPREAD
  --umap-learning-rate UMAP_LEARNING_RATE
  --umap-repulsion-strength UMAP_REPULSION_STRENGTH
  --umap-negative-sample-rate UMAP_NEGATIVE_SAMPLE_RATE
  --umap-local-connectivity UMAP_LOCAL_CONNECTIVITY
  --umap-set-op-mix-ratio UMAP_SET_OP_MIX_RATIO
  --random-state UMAP_RANDOM_STATE, --random_state UMAP_RANDOM_STATE
  --densmap
  --no-densmap
  --hdbscan-min-cluster-size HDBSCAN_MIN_CLUSTER_SIZE, --grid-min-cluster-size HDBSCAN_MIN_CLUSTER_SIZE, --grid_min_cluster_size HDBSCAN_MIN_CLUSTER_SIZE
  --hdbscan-min-samples HDBSCAN_MIN_SAMPLES, --grid-min-samples HDBSCAN_MIN_SAMPLES, --grid_min_samples HDBSCAN_MIN_SAMPLES
  --hdbscan-cluster-selection-epsilon HDBSCAN_CLUSTER_SELECTION_EPSILON, --grid-eps HDBSCAN_CLUSTER_SELECTION_EPSILON, --grid_eps HDBSCAN_CLUSTER_SELECTION_EPSILON
  --hdbscan-cluster-selection-persistence HDBSCAN_CLUSTER_SELECTION_PERSISTENCE, --grid-cluster-selection-persistence HDBSCAN_CLUSTER_SELECTION_PERSISTENCE, --grid_cluster_selection_persistence HDBSCAN_CLUSTER_SELECTION_PERSISTENCE
  --hdbscan-cluster-selection-method HDBSCAN_CLUSTER_SELECTION_METHOD, --grid-cluster-selection-method HDBSCAN_CLUSTER_SELECTION_METHOD, --grid_cluster_selection_method HDBSCAN_CLUSTER_SELECTION_METHOD, --cluster_selection_method HDBSCAN_CLUSTER_SELECTION_METHOD
  --hdbscan-alpha HDBSCAN_ALPHA, --grid-alpha HDBSCAN_ALPHA, --grid_alpha HDBSCAN_ALPHA
  --hdbscan-allow-single-cluster HDBSCAN_ALLOW_SINGLE_CLUSTER, --grid-allow-single-cluster HDBSCAN_ALLOW_SINGLE_CLUSTER, --grid_allow_single_cluster HDBSCAN_ALLOW_SINGLE_CLUSTER
  --hdbscan-max-cluster-size HDBSCAN_MAX_CLUSTER_SIZE, --max-cluster-size HDBSCAN_MAX_CLUSTER_SIZE, --max_cluster_size HDBSCAN_MAX_CLUSTER_SIZE
  --hdbscan-metric HDBSCAN_METRIC, --hdbscan_metric HDBSCAN_METRIC
  --n-random-states N_RANDOM_STATES, --n_random_states N_RANDOM_STATES
  --n-jobs N_JOBS, --n_jobs N_JOBS
  --candidate-jobs CANDIDATE_JOBS
  --top-n-models TOP_N_MODELS
  --warn-candidate-count WARN_CANDIDATE_COUNT
  --max-candidate-models MAX_CANDIDATE_MODELS
  --max-samples-trust MAX_SAMPLES_TRUST, --max_samples_trust MAX_SAMPLES_TRUST
  --max-samples-silhouette MAX_SAMPLES_SILHOUETTE
  --trust-k TRUST_K, --trust_k TRUST_K
  --trust-seed TRUST_SEED, --trust_seed TRUST_SEED
  --silhouette-seed SILHOUETTE_SEED
  --legacy-ensemble-seeds
  --no-legacy-ensemble-seeds
  --compute-dbcv
  --no-compute-dbcv
  --write-parquet
  --no-write-parquet
  --strict
  --scoring-profile {legacy_dimple,custom}
  --fit-include-noise
  --fit-exclude-noise
  --output OUTPUT       Optional resolved YAML path
```

## `show-search-space`

```text
usage: dimple-gwas show-search-space [-h]
                                     [--search-mode {standard,extended,custom,fixed}]
                                     [--config CONFIG] [--input INPUT_PATH]
                                     [--drop-first-n-cols DROP_FIRST_N_COLS]
                                     [--sep SEP]
                                     [--zscore-transform {none,rint}]
                                     [--annotation-file ANNOTATION_FILE]
                                     [--annotation-index-col ANNOTATION_INDEX_COL]
                                     [--umap-n-neighbors UMAP_N_NEIGHBORS]
                                     [--umap-min-dist UMAP_MIN_DIST]
                                     [--umap-n-components UMAP_N_COMPONENTS]
                                     [--umap-metric UMAP_METRIC]
                                     [--umap-spread UMAP_SPREAD]
                                     [--umap-learning-rate UMAP_LEARNING_RATE]
                                     [--umap-repulsion-strength UMAP_REPULSION_STRENGTH]
                                     [--umap-negative-sample-rate UMAP_NEGATIVE_SAMPLE_RATE]
                                     [--umap-local-connectivity UMAP_LOCAL_CONNECTIVITY]
                                     [--umap-set-op-mix-ratio UMAP_SET_OP_MIX_RATIO]
                                     [--random-state UMAP_RANDOM_STATE]
                                     [--densmap] [--no-densmap]
                                     [--hdbscan-min-cluster-size HDBSCAN_MIN_CLUSTER_SIZE]
                                     [--hdbscan-min-samples HDBSCAN_MIN_SAMPLES]
                                     [--hdbscan-cluster-selection-epsilon HDBSCAN_CLUSTER_SELECTION_EPSILON]
                                     [--hdbscan-cluster-selection-persistence HDBSCAN_CLUSTER_SELECTION_PERSISTENCE]
                                     [--hdbscan-cluster-selection-method HDBSCAN_CLUSTER_SELECTION_METHOD]
                                     [--hdbscan-alpha HDBSCAN_ALPHA]
                                     [--hdbscan-allow-single-cluster HDBSCAN_ALLOW_SINGLE_CLUSTER]
                                     [--hdbscan-max-cluster-size HDBSCAN_MAX_CLUSTER_SIZE]
                                     [--hdbscan-metric HDBSCAN_METRIC]
                                     [--n-random-states N_RANDOM_STATES]
                                     [--n-jobs N_JOBS]
                                     [--candidate-jobs CANDIDATE_JOBS]
                                     [--top-n-models TOP_N_MODELS]
                                     [--warn-candidate-count WARN_CANDIDATE_COUNT]
                                     [--max-candidate-models MAX_CANDIDATE_MODELS]
                                     [--max-samples-trust MAX_SAMPLES_TRUST]
                                     [--max-samples-silhouette MAX_SAMPLES_SILHOUETTE]
                                     [--trust-k TRUST_K]
                                     [--trust-seed TRUST_SEED]
                                     [--silhouette-seed SILHOUETTE_SEED]
                                     [--legacy-ensemble-seeds]
                                     [--no-legacy-ensemble-seeds]
                                     [--compute-dbcv] [--no-compute-dbcv]
                                     [--write-parquet] [--no-write-parquet]
                                     [--strict]
                                     [--scoring-profile {legacy_dimple,custom}]
                                     [--fit-include-noise]
                                     [--fit-exclude-noise]
                                     [--output-dir OUTPUT_DIR]
                                     [--show-first SHOW_FIRST]

options:
  -h, --help            show this help message and exit
  --search-mode {standard,extended,custom,fixed}
  --config CONFIG       YAML configuration; explicit CLI values override it
  --input INPUT_PATH, --datainput INPUT_PATH
                        GWAS summary-statistics matrix (CSV/TSV)
  --drop-first-n-cols DROP_FIRST_N_COLS, --drop_first_n_cols DROP_FIRST_N_COLS
  --sep SEP
  --zscore-transform {none,rint}, --zscore_transform {none,rint}
  --annotation-file ANNOTATION_FILE, --annotation_file ANNOTATION_FILE, --idp_key ANNOTATION_FILE
  --annotation-index-col ANNOTATION_INDEX_COL, --annotation_index_col ANNOTATION_INDEX_COL
  --umap-n-neighbors UMAP_N_NEIGHBORS, --n-neighbors UMAP_N_NEIGHBORS, --n_neighbors UMAP_N_NEIGHBORS
  --umap-min-dist UMAP_MIN_DIST, --min-dist UMAP_MIN_DIST, --min_dist UMAP_MIN_DIST
  --umap-n-components UMAP_N_COMPONENTS, --n-components UMAP_N_COMPONENTS, --n_components UMAP_N_COMPONENTS
  --umap-metric UMAP_METRIC, --umap_metric UMAP_METRIC
  --umap-spread UMAP_SPREAD
  --umap-learning-rate UMAP_LEARNING_RATE
  --umap-repulsion-strength UMAP_REPULSION_STRENGTH
  --umap-negative-sample-rate UMAP_NEGATIVE_SAMPLE_RATE
  --umap-local-connectivity UMAP_LOCAL_CONNECTIVITY
  --umap-set-op-mix-ratio UMAP_SET_OP_MIX_RATIO
  --random-state UMAP_RANDOM_STATE, --random_state UMAP_RANDOM_STATE
  --densmap
  --no-densmap
  --hdbscan-min-cluster-size HDBSCAN_MIN_CLUSTER_SIZE, --grid-min-cluster-size HDBSCAN_MIN_CLUSTER_SIZE, --grid_min_cluster_size HDBSCAN_MIN_CLUSTER_SIZE
  --hdbscan-min-samples HDBSCAN_MIN_SAMPLES, --grid-min-samples HDBSCAN_MIN_SAMPLES, --grid_min_samples HDBSCAN_MIN_SAMPLES
  --hdbscan-cluster-selection-epsilon HDBSCAN_CLUSTER_SELECTION_EPSILON, --grid-eps HDBSCAN_CLUSTER_SELECTION_EPSILON, --grid_eps HDBSCAN_CLUSTER_SELECTION_EPSILON
  --hdbscan-cluster-selection-persistence HDBSCAN_CLUSTER_SELECTION_PERSISTENCE, --grid-cluster-selection-persistence HDBSCAN_CLUSTER_SELECTION_PERSISTENCE, --grid_cluster_selection_persistence HDBSCAN_CLUSTER_SELECTION_PERSISTENCE
  --hdbscan-cluster-selection-method HDBSCAN_CLUSTER_SELECTION_METHOD, --grid-cluster-selection-method HDBSCAN_CLUSTER_SELECTION_METHOD, --grid_cluster_selection_method HDBSCAN_CLUSTER_SELECTION_METHOD, --cluster_selection_method HDBSCAN_CLUSTER_SELECTION_METHOD
  --hdbscan-alpha HDBSCAN_ALPHA, --grid-alpha HDBSCAN_ALPHA, --grid_alpha HDBSCAN_ALPHA
  --hdbscan-allow-single-cluster HDBSCAN_ALLOW_SINGLE_CLUSTER, --grid-allow-single-cluster HDBSCAN_ALLOW_SINGLE_CLUSTER, --grid_allow_single_cluster HDBSCAN_ALLOW_SINGLE_CLUSTER
  --hdbscan-max-cluster-size HDBSCAN_MAX_CLUSTER_SIZE, --max-cluster-size HDBSCAN_MAX_CLUSTER_SIZE, --max_cluster_size HDBSCAN_MAX_CLUSTER_SIZE
  --hdbscan-metric HDBSCAN_METRIC, --hdbscan_metric HDBSCAN_METRIC
  --n-random-states N_RANDOM_STATES, --n_random_states N_RANDOM_STATES
  --n-jobs N_JOBS, --n_jobs N_JOBS
  --candidate-jobs CANDIDATE_JOBS
  --top-n-models TOP_N_MODELS
  --warn-candidate-count WARN_CANDIDATE_COUNT
  --max-candidate-models MAX_CANDIDATE_MODELS
  --max-samples-trust MAX_SAMPLES_TRUST, --max_samples_trust MAX_SAMPLES_TRUST
  --max-samples-silhouette MAX_SAMPLES_SILHOUETTE
  --trust-k TRUST_K, --trust_k TRUST_K
  --trust-seed TRUST_SEED, --trust_seed TRUST_SEED
  --silhouette-seed SILHOUETTE_SEED
  --legacy-ensemble-seeds
  --no-legacy-ensemble-seeds
  --compute-dbcv
  --no-compute-dbcv
  --write-parquet
  --no-write-parquet
  --strict
  --scoring-profile {legacy_dimple,custom}
  --fit-include-noise
  --fit-exclude-noise
  --output-dir OUTPUT_DIR
                        Write complete TSV/JSON manifests here
  --show-first SHOW_FIRST
```

## `run`

```text
usage: dimple-gwas run [-h] [--search-mode {standard,extended,custom,fixed}]
                       [--config CONFIG] [--input INPUT_PATH]
                       [--output-dir OUTPUT_DIR]
                       [--drop-first-n-cols DROP_FIRST_N_COLS] [--sep SEP]
                       [--zscore-transform {none,rint}]
                       [--annotation-file ANNOTATION_FILE]
                       [--annotation-index-col ANNOTATION_INDEX_COL]
                       [--umap-n-neighbors UMAP_N_NEIGHBORS]
                       [--umap-min-dist UMAP_MIN_DIST]
                       [--umap-n-components UMAP_N_COMPONENTS]
                       [--umap-metric UMAP_METRIC] [--umap-spread UMAP_SPREAD]
                       [--umap-learning-rate UMAP_LEARNING_RATE]
                       [--umap-repulsion-strength UMAP_REPULSION_STRENGTH]
                       [--umap-negative-sample-rate UMAP_NEGATIVE_SAMPLE_RATE]
                       [--umap-local-connectivity UMAP_LOCAL_CONNECTIVITY]
                       [--umap-set-op-mix-ratio UMAP_SET_OP_MIX_RATIO]
                       [--random-state UMAP_RANDOM_STATE] [--densmap]
                       [--no-densmap]
                       [--hdbscan-min-cluster-size HDBSCAN_MIN_CLUSTER_SIZE]
                       [--hdbscan-min-samples HDBSCAN_MIN_SAMPLES]
                       [--hdbscan-cluster-selection-epsilon HDBSCAN_CLUSTER_SELECTION_EPSILON]
                       [--hdbscan-cluster-selection-persistence HDBSCAN_CLUSTER_SELECTION_PERSISTENCE]
                       [--hdbscan-cluster-selection-method HDBSCAN_CLUSTER_SELECTION_METHOD]
                       [--hdbscan-alpha HDBSCAN_ALPHA]
                       [--hdbscan-allow-single-cluster HDBSCAN_ALLOW_SINGLE_CLUSTER]
                       [--hdbscan-max-cluster-size HDBSCAN_MAX_CLUSTER_SIZE]
                       [--hdbscan-metric HDBSCAN_METRIC]
                       [--n-random-states N_RANDOM_STATES] [--n-jobs N_JOBS]
                       [--candidate-jobs CANDIDATE_JOBS]
                       [--top-n-models TOP_N_MODELS]
                       [--warn-candidate-count WARN_CANDIDATE_COUNT]
                       [--max-candidate-models MAX_CANDIDATE_MODELS]
                       [--max-samples-trust MAX_SAMPLES_TRUST]
                       [--max-samples-silhouette MAX_SAMPLES_SILHOUETTE]
                       [--trust-k TRUST_K] [--trust-seed TRUST_SEED]
                       [--silhouette-seed SILHOUETTE_SEED]
                       [--legacy-ensemble-seeds] [--no-legacy-ensemble-seeds]
                       [--compute-dbcv] [--no-compute-dbcv] [--write-parquet]
                       [--no-write-parquet] [--strict]
                       [--scoring-profile {legacy_dimple,custom}]
                       [--fit-include-noise] [--fit-exclude-noise]

options:
  -h, --help            show this help message and exit
  --search-mode {standard,extended,custom,fixed}
  --config CONFIG       YAML configuration; explicit CLI values override it
  --input INPUT_PATH, --datainput INPUT_PATH
                        GWAS summary-statistics matrix (CSV/TSV)
  --output-dir OUTPUT_DIR, --outdir OUTPUT_DIR
  --drop-first-n-cols DROP_FIRST_N_COLS, --drop_first_n_cols DROP_FIRST_N_COLS
  --sep SEP
  --zscore-transform {none,rint}, --zscore_transform {none,rint}
  --annotation-file ANNOTATION_FILE, --annotation_file ANNOTATION_FILE, --idp_key ANNOTATION_FILE
  --annotation-index-col ANNOTATION_INDEX_COL, --annotation_index_col ANNOTATION_INDEX_COL
  --umap-n-neighbors UMAP_N_NEIGHBORS, --n-neighbors UMAP_N_NEIGHBORS, --n_neighbors UMAP_N_NEIGHBORS
  --umap-min-dist UMAP_MIN_DIST, --min-dist UMAP_MIN_DIST, --min_dist UMAP_MIN_DIST
  --umap-n-components UMAP_N_COMPONENTS, --n-components UMAP_N_COMPONENTS, --n_components UMAP_N_COMPONENTS
  --umap-metric UMAP_METRIC, --umap_metric UMAP_METRIC
  --umap-spread UMAP_SPREAD
  --umap-learning-rate UMAP_LEARNING_RATE
  --umap-repulsion-strength UMAP_REPULSION_STRENGTH
  --umap-negative-sample-rate UMAP_NEGATIVE_SAMPLE_RATE
  --umap-local-connectivity UMAP_LOCAL_CONNECTIVITY
  --umap-set-op-mix-ratio UMAP_SET_OP_MIX_RATIO
  --random-state UMAP_RANDOM_STATE, --random_state UMAP_RANDOM_STATE
  --densmap
  --no-densmap
  --hdbscan-min-cluster-size HDBSCAN_MIN_CLUSTER_SIZE, --grid-min-cluster-size HDBSCAN_MIN_CLUSTER_SIZE, --grid_min_cluster_size HDBSCAN_MIN_CLUSTER_SIZE
  --hdbscan-min-samples HDBSCAN_MIN_SAMPLES, --grid-min-samples HDBSCAN_MIN_SAMPLES, --grid_min_samples HDBSCAN_MIN_SAMPLES
  --hdbscan-cluster-selection-epsilon HDBSCAN_CLUSTER_SELECTION_EPSILON, --grid-eps HDBSCAN_CLUSTER_SELECTION_EPSILON, --grid_eps HDBSCAN_CLUSTER_SELECTION_EPSILON
  --hdbscan-cluster-selection-persistence HDBSCAN_CLUSTER_SELECTION_PERSISTENCE, --grid-cluster-selection-persistence HDBSCAN_CLUSTER_SELECTION_PERSISTENCE, --grid_cluster_selection_persistence HDBSCAN_CLUSTER_SELECTION_PERSISTENCE
  --hdbscan-cluster-selection-method HDBSCAN_CLUSTER_SELECTION_METHOD, --grid-cluster-selection-method HDBSCAN_CLUSTER_SELECTION_METHOD, --grid_cluster_selection_method HDBSCAN_CLUSTER_SELECTION_METHOD, --cluster_selection_method HDBSCAN_CLUSTER_SELECTION_METHOD
  --hdbscan-alpha HDBSCAN_ALPHA, --grid-alpha HDBSCAN_ALPHA, --grid_alpha HDBSCAN_ALPHA
  --hdbscan-allow-single-cluster HDBSCAN_ALLOW_SINGLE_CLUSTER, --grid-allow-single-cluster HDBSCAN_ALLOW_SINGLE_CLUSTER, --grid_allow_single_cluster HDBSCAN_ALLOW_SINGLE_CLUSTER
  --hdbscan-max-cluster-size HDBSCAN_MAX_CLUSTER_SIZE, --max-cluster-size HDBSCAN_MAX_CLUSTER_SIZE, --max_cluster_size HDBSCAN_MAX_CLUSTER_SIZE
  --hdbscan-metric HDBSCAN_METRIC, --hdbscan_metric HDBSCAN_METRIC
  --n-random-states N_RANDOM_STATES, --n_random_states N_RANDOM_STATES
  --n-jobs N_JOBS, --n_jobs N_JOBS
  --candidate-jobs CANDIDATE_JOBS
  --top-n-models TOP_N_MODELS
  --warn-candidate-count WARN_CANDIDATE_COUNT
  --max-candidate-models MAX_CANDIDATE_MODELS
  --max-samples-trust MAX_SAMPLES_TRUST, --max_samples_trust MAX_SAMPLES_TRUST
  --max-samples-silhouette MAX_SAMPLES_SILHOUETTE
  --trust-k TRUST_K, --trust_k TRUST_K
  --trust-seed TRUST_SEED, --trust_seed TRUST_SEED
  --silhouette-seed SILHOUETTE_SEED
  --legacy-ensemble-seeds
  --no-legacy-ensemble-seeds
  --compute-dbcv
  --no-compute-dbcv
  --write-parquet
  --no-write-parquet
  --strict
  --scoring-profile {legacy_dimple,custom}
  --fit-include-noise
  --fit-exclude-noise
```

## `score-existing`

```text
usage: dimple-gwas score-existing [-h] --models MODELS [--config CONFIG]
                                  [--scoring-profile {legacy_dimple,custom}]
                                  [--fit-include-noise] --output OUTPUT

options:
  -h, --help            show this help message and exit
  --models MODELS
  --config CONFIG
  --scoring-profile {legacy_dimple,custom}
  --fit-include-noise
  --output OUTPUT
```

## `summarize-models`

```text
usage: dimple-gwas summarize-models [-h] --models MODELS --output-dir
                                    OUTPUT_DIR [--top-n-models TOP_N_MODELS]

options:
  -h, --help            show this help message and exit
  --models MODELS
  --output-dir OUTPUT_DIR
  --top-n-models TOP_N_MODELS
```

## `reproduce-model`

```text
usage: dimple-gwas reproduce-model [-h] --model-json MODEL_JSON
                                   [--input INPUT_PATH] --output-dir
                                   OUTPUT_DIR [--n-jobs N_JOBS]

options:
  -h, --help            show this help message and exit
  --model-json MODEL_JSON
                        best_model.json or top-model summary.json
  --input INPUT_PATH
  --output-dir OUTPUT_DIR
  --n-jobs N_JOBS
```

## `explain`

```text
usage: dimple-gwas explain [-h]
                           (--model-json MODEL_JSON | --legacy-table LEGACY_TABLE)
                           [--input INPUT_PATH] [--outdir OUTPUT_DIR]
                           [--config CONFIG] [--input-sep INPUT_SEP]
                           [--input-sheet INPUT_SHEET]
                           [--legacy-sheet LEGACY_SHEET]
                           [--matrix-orientation {auto,variants_by_vectors,vectors_by_variants}]
                           [--vector-id-source VECTOR_ID_SOURCE]
                           [--drop-first-n-cols DROP_FIRST_N_COLS]
                           [--zscore-transform {none,rint}]
                           [--id-column ID_COLUMN]
                           [--label-column LABEL_COLUMN]
                           [--coordinate-columns COORDINATE_COLUMNS]
                           [--similarity-metric {pearson,spearman}]
                           [--order {cluster_then_hclust,cluster,hclust,input}]
                           [--noise-policy {separate_last,include,exclude}]
                           [--undefined-correlation {error,zero}]
                           [--require-complete-match]
                           [--allow-incomplete-match]
                           [--max-full-heatmap MAX_FULL_HEATMAP]
                           [--write-similarity] [--no-write-similarity]
                           [--force-large-matrix] [--coordinate-associations]
                           [--coordinate-methods COORDINATE_METHODS]
                           [--top-n-associations TOP_N_ASSOCIATIONS]

options:
  -h, --help            show this help message and exit
  --model-json MODEL_JSON
                        Native top-model summary.json
  --legacy-table LEGACY_TABLE
                        Legacy label/UMAP table (CSV/TSV/XLSX)
  --input INPUT_PATH    Original matrix; optional native path override
  --outdir OUTPUT_DIR, --output-dir OUTPUT_DIR
  --config CONFIG       Optional Freeze 3 YAML providing interpretation
                        defaults
  --input-sep INPUT_SEP
  --input-sheet INPUT_SHEET
  --legacy-sheet LEGACY_SHEET
  --matrix-orientation {auto,variants_by_vectors,vectors_by_variants}
  --vector-id-source VECTOR_ID_SOURCE
  --drop-first-n-cols DROP_FIRST_N_COLS
  --zscore-transform {none,rint}
  --id-column ID_COLUMN
  --label-column LABEL_COLUMN
  --coordinate-columns COORDINATE_COLUMNS
                        Comma-separated supplied UMAP columns
  --similarity-metric {pearson,spearman}
  --order {cluster_then_hclust,cluster,hclust,input}
  --noise-policy {separate_last,include,exclude}
  --undefined-correlation {error,zero}
  --require-complete-match
  --allow-incomplete-match
  --max-full-heatmap MAX_FULL_HEATMAP
  --write-similarity
  --no-write-similarity
  --force-large-matrix
  --coordinate-associations
  --coordinate-methods COORDINATE_METHODS
  --top-n-associations TOP_N_ASSOCIATIONS
```

## `interpret`

```text
usage: dimple-gwas explain [-h]
                           (--model-json MODEL_JSON | --legacy-table LEGACY_TABLE)
                           [--input INPUT_PATH] [--outdir OUTPUT_DIR]
                           [--config CONFIG] [--input-sep INPUT_SEP]
                           [--input-sheet INPUT_SHEET]
                           [--legacy-sheet LEGACY_SHEET]
                           [--matrix-orientation {auto,variants_by_vectors,vectors_by_variants}]
                           [--vector-id-source VECTOR_ID_SOURCE]
                           [--drop-first-n-cols DROP_FIRST_N_COLS]
                           [--zscore-transform {none,rint}]
                           [--id-column ID_COLUMN]
                           [--label-column LABEL_COLUMN]
                           [--coordinate-columns COORDINATE_COLUMNS]
                           [--similarity-metric {pearson,spearman}]
                           [--order {cluster_then_hclust,cluster,hclust,input}]
                           [--noise-policy {separate_last,include,exclude}]
                           [--undefined-correlation {error,zero}]
                           [--require-complete-match]
                           [--allow-incomplete-match]
                           [--max-full-heatmap MAX_FULL_HEATMAP]
                           [--write-similarity] [--no-write-similarity]
                           [--force-large-matrix] [--coordinate-associations]
                           [--coordinate-methods COORDINATE_METHODS]
                           [--top-n-associations TOP_N_ASSOCIATIONS]

options:
  -h, --help            show this help message and exit
  --model-json MODEL_JSON
                        Native top-model summary.json
  --legacy-table LEGACY_TABLE
                        Legacy label/UMAP table (CSV/TSV/XLSX)
  --input INPUT_PATH    Original matrix; optional native path override
  --outdir OUTPUT_DIR, --output-dir OUTPUT_DIR
  --config CONFIG       Optional Freeze 3 YAML providing interpretation
                        defaults
  --input-sep INPUT_SEP
  --input-sheet INPUT_SHEET
  --legacy-sheet LEGACY_SHEET
  --matrix-orientation {auto,variants_by_vectors,vectors_by_variants}
  --vector-id-source VECTOR_ID_SOURCE
  --drop-first-n-cols DROP_FIRST_N_COLS
  --zscore-transform {none,rint}
  --id-column ID_COLUMN
  --label-column LABEL_COLUMN
  --coordinate-columns COORDINATE_COLUMNS
                        Comma-separated supplied UMAP columns
  --similarity-metric {pearson,spearman}
  --order {cluster_then_hclust,cluster,hclust,input}
  --noise-policy {separate_last,include,exclude}
  --undefined-correlation {error,zero}
  --require-complete-match
  --allow-incomplete-match
  --max-full-heatmap MAX_FULL_HEATMAP
  --write-similarity
  --no-write-similarity
  --force-large-matrix
  --coordinate-associations
  --coordinate-methods COORDINATE_METHODS
  --top-n-associations TOP_N_ASSOCIATIONS
```

## `compare`

```text
usage: dimple-gwas compare [-h] --left LEFT --right RIGHT --output-dir
                           OUTPUT_DIR [--id-column ID_COLUMN]
                           [--label-column LABEL_COLUMN]
                           [--require-same-order]

options:
  -h, --help            show this help message and exit
  --left LEFT           Left summary JSON or label table
  --right RIGHT         Right summary JSON or label table
  --output-dir OUTPUT_DIR
  --id-column ID_COLUMN
  --label-column LABEL_COLUMN
  --require-same-order
```

## `validate`

```text
usage: dimple-gwas validate [-h] --run-dir RUN_DIR [--output-dir OUTPUT_DIR]

options:
  -h, --help            show this help message and exit
  --run-dir RUN_DIR
  --output-dir OUTPUT_DIR
```
