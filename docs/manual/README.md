# DIMPLE-GWAS Freeze 3 RC1 Analyst Manual sources

This directory contains the complete first-draft textbook, executable tutorial evidence, source-derived reference maps, figures/diagrams, and the later Docker/cloud handoff.

Primary navigation:

- [Quickstart](QUICKSTART.md)
- [Compiled Markdown manual](DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.md)
- `DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.html` — generated navigable edition
- `DIMPLE_GWAS_FREEZE3_RC1_ANALYST_MANUAL.pdf` — rendered edition after PDF QA
- [Build report](MANUAL_BUILD_REPORT.md)
- [QA report](MANUAL_QA_REPORT.md)
- [Docker/cloud handoff](DOCKER_CLOUD_SUPPLEMENT_HANDOFF.md)

## Modular chapters

- [1. What DIMPLE-GWAS is and is not](chapters/01_what_dimple_gwas_is_and_is_not.md)
- [2. The scientific problem: structure among genetically informed phenotype vectors](chapters/02_the_scientific_problem_structure_among_genetically_informed_phenotype_vectors.md)
- [3. Stage 1 scope and the Freeze 3 RC1 status boundary](chapters/03_stage_1_scope_and_the_freeze_3_rc1_status_boundary.md)
- [4. From input matrix to candidate partitions](chapters/04_from_input_matrix_to_candidate_partitions.md)
- [5. Essential GWAS, vector-space, distance, and clustering concepts](chapters/05_essential_gwas_vector_space_distance_and_clustering_concepts.md)
- [6. Why repeated nonlinear embeddings and density clustering are used](chapters/06_why_repeated_nonlinear_embeddings_and_density_clustering_are_used.md)
- [7. Choosing among complementary methods](chapters/07_choosing_among_complementary_methods.md)
- [8. Scientific interpretation, circularity, and validation boundaries](chapters/08_scientific_interpretation_circularity_and_validation_boundaries.md)
- [9. System requirements and isolated environment setup](chapters/09_system_requirements_and_isolated_environment_setup.md)
- [10. Input data contract, orientation, metadata columns, and missingness](chapters/10_input_data_contract_orientation_metadata_columns_and_missingness.md)
- [11. Configuration files and precedence](chapters/11_configuration_files_and_precedence.md)
- [12. Inspecting a configuration and enumerating the search space](chapters/12_inspecting_a_configuration_and_enumerating_the_search_space.md)
- [13. Fixed synthetic quickstart](chapters/13_fixed_synthetic_quickstart.md)
- [14. Reading the run manifest](chapters/14_reading_the_run_manifest.md)
- [15. Preprocessing and optional RINT](chapters/15_preprocessing_and_optional_rint.md)
- [16. UMAP and densMAP fundamentals](chapters/16_umap_and_densmap_fundamentals.md)
- [17. Repeated seeds, concatenated embeddings, determinism, and compute cost](chapters/17_repeated_seeds_concatenated_embeddings_determinism_and_compute_cost.md)
- [18. HDBSCAN concepts and the Freeze 3 search grid](chapters/18_hdbscan_concepts_and_the_freeze_3_search_grid.md)
- [19. Candidate-model metrics](chapters/19_candidate_model_metrics.md)
- [20. The legacy_dimple score and optional alternatives](chapters/20_the_legacy_dimple_score_and_optional_alternatives.md)
- [21. Ranking, summarising, and choosing a model](chapters/21_ranking_summarising_and_choosing_a_model.md)
- [22. Reproducing a selected model](chapters/22_reproducing_a_selected_model.md)
- [23. Comparing partitions and validating outputs](chapters/23_comparing_partitions_and_validating_outputs.md)
- [24. Why UMAP coordinates are not biological loadings](chapters/24_why_umap_coordinates_are_not_biological_loadings.md)
- [25. Returning to the original input-vector space](chapters/25_returning_to_the_original_input_vector_space.md)
- [26. Pearson and Spearman association summaries](chapters/26_pearson_and_spearman_association_summaries.md)
- [27. Cluster heatmaps, ordering, annotations, and cutpoints](chapters/27_cluster_heatmaps_ordering_annotations_and_cutpoints.md)
- [28. Noise assignments and uncertainty](chapters/28_noise_assignments_and_uncertainty.md)
- [29. Avoiding double dipping and post-selection overclaiming](chapters/29_avoiding_double_dipping_and_post_selection_overclaiming.md)
- [30. Technical, statistical, and biological validation](chapters/30_technical_statistical_and_biological_validation.md)
- [31. Reporting a DIMPLE-GWAS analysis](chapters/31_reporting_a_dimple_gwas_analysis.md)
- [32. Fixed synthetic dataset case study](chapters/32_fixed_synthetic_dataset_case_study.md)
- [33. Custom bounded search-space case study](chapters/33_custom_bounded_search_space_case_study.md)
- [34. Explanation, comparison, and validation case study](chapters/34_explanation_comparison_and_validation_case_study.md)
- [35. MNIST as a software benchmark](chapters/35_mnist_as_a_software_benchmark.md)
- [36. Original 164-IDP analysis](chapters/36_original_164_idp_analysis.md)
- [37. Complete command reference](chapters/37_complete_command_reference.md)
- [38. Complete configuration reference](chapters/38_complete_configuration_reference.md)
- [39. Search-space reference](chapters/39_search_space_reference.md)
- [40. Scoring and model-selection reference](chapters/40_scoring_and_model_selection_reference.md)
- [41. Output atlas and data dictionary](chapters/41_output_atlas_and_data_dictionary.md)
- [42. Provenance and reproducibility checklist](chapters/42_provenance_and_reproducibility_checklist.md)
- [43. Error messages, troubleshooting, and recovery](chapters/43_error_messages_troubleshooting_and_recovery.md)
- [44. Performance, memory, threading, and bounded-run guidance](chapters/44_performance_memory_threading_and_bounded_run_guidance.md)
- [45. Migration from Dev and Freeze 2](chapters/45_migration_from_dev_and_freeze_2.md)
- [46. Known issues and scientific limitations](chapters/46_known_issues_and_scientific_limitations.md)

## Maintenance workflow

1. Treat executable source and fresh artifacts as authority.
2. Update claim/software/output/citation evidence before changing authoritative prose.
3. Regenerate source maps, runtime evidence, figures, curriculum, chapters, and the compiled edition with the scripts under `build/tools/`.
4. Never overwrite a prior tutorial output; use a new root and regenerate manifests/checksums.
5. Rerun tests, command/output QA, privacy scans, link checks, and PDF page inspection.
6. Preserve the RC1 status banner until every corresponding release gate has direct evidence.

The isolated build environment under `build/runtime_env/` is ignored and is not a deliverable. Markdown is the maintainable authority; HTML/PDF are rendered products.
