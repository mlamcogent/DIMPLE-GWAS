# Edition 2 curriculum specification

The 24-chapter plan targets **90,700 substantive words** before appendices, bibliography, and generated reference tables. It merges Edition 1's short checklist chapters into connected conceptual and operational units.

| Ch. | Part | Title | Prerequisites | Target | Core implementation |
| ---: | :---: | --- | --- | ---: | --- |
| 1 | I | The scientific problem, scope, and evidence boundary | none | 3,200 | `cli.main; run_search` |
| 2 | I | GWAS-derived phenotype vectors and high-dimensional geometry | 1 | 3,800 | `prepare_analysis_matrix` |
| 3 | I | Similarity, distance, scaling, transformation, and uncertainty | 2 | 3,800 | `rank_inverse_normal_transform; compute_similarity` |
| 4 | I | Dimension reduction: linear and nonlinear perspectives | 2-3 | 3,200 | `_fit_one` |
| 5 | I | Density clustering, validation, and circular inference | 3-4 | 3,600 | `fit_hdbscan; evaluate_candidate` |
| 6 | II | Data contract, preprocessing, RINT, and orientation | 2-3 | 4,000 | `prepare_analysis_matrix; prepare_explanation_matrix` |
| 7 | II | UMAP and densMAP from graph construction to optimization | 3-4,6 | 5,000 | `_fit_one` |
| 8 | II | Repeated stochastic embeddings and concatenated geometry | 7 | 3,800 | `ensemble_seeds; run_repeated_umap` |
| 9 | II | HDBSCAN hierarchy, density, selection, and noise | 5,8 | 4,800 | `estimator_kwargs; fit_hdbscan` |
| 10 | II | Search-space enumeration and computational design | 8-9 | 3,300 | `enumerate_candidates; candidate_identity` |
| 11 | II | Candidate diagnostics, legacy_dimple, ranking, ties, and sensitivity | 5,9-10 | 5,200 | `evaluate_candidate; legacy_dimple_score; rank_models` |
| 12 | II | Selected-model reproduction, provenance, and comparison | 8-11 | 4,000 | `run_comparison; run_validation; capture_environment` |
| 13 | III | Installation, environment verification, and first run | 1,6 | 3,000 | `cli.main` |
| 14 | III | Configuration and search-space inspection | 6,10,13 | 3,200 | `resolve_config; enumerate_candidates` |
| 15 | III | Complete pipeline execution and monitoring | 7-14 | 3,600 | `run_search; write_model_outputs` |
| 16 | III | Model summaries, selection, reproduction, comparison, and validation | 11-15 | 3,800 | `rank_models; run_comparison; run_validation` |
| 17 | III | Original-space explanation, heatmaps, and responsible interpretation | 3,5,12,16 | 4,000 | `run_explanation; render_heatmap` |
| 18 | IV | A hand-calculable toy analysis from matrix to score | 6-11 | 3,600 | `core analytical functions` |
| 19 | IV | Fixed synthetic end-to-end analysis | 13-17 | 3,800 | `all CLI workflow functions` |
| 20 | IV | Custom bounded search, sensitivity, and selected-model replay | 10-16,19 | 3,400 | `custom_score; run_search` |
| 21 | IV | Explanation, comparison, validation, and report generation | 16-17,19 | 3,400 | `run_explanation; run_comparison; run_validation` |
| 22 | IV | MNIST benchmark and original 164-IDP reconstruction protocol | 12-21 | 3,800 | `pipeline and historical adapters` |
| 23 | V | Technical, statistical, biological, and cross-platform validation | 5,12,19-22 | 3,800 | `run_validation` |
| 24 | V | Reproducible reporting, limitations, migration, and reviewer-facing methods | 1-23 | 3,600 | `reporting and provenance modules` |

Every chapter must open with a real problem, introduce intuition before formalism, trace claims to source or literature, include a worked or executed example where applicable, and end with exercises mapped to its objectives. Lookup-heavy details remain in appendices, the function atlas, and the output atlas.
