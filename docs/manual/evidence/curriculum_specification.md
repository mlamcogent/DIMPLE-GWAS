# Curriculum specification

The curriculum is progressive but layered: beginners can follow Chapters 1, 3–4, and 9–14 before returning to the methods chapters; operators can use Parts III and VI; reviewers can trace claims through Parts I, IV, the bibliography, and the evidence registers.

Every chapter uses the same teaching contract: orientation, observable objectives, prerequisites, plain-language model, implementation truth, evidence-backed example, outputs, mistakes, boundaries, and a completion check. Defaults, tutorial values, historical values, and recommendations are explicitly labelled.

## Part I — Orientation and conceptual foundations

### 1. What DIMPLE-GWAS is and is not

- Audience: Orientation; prerequisites: none.
- Observable objective: Distinguish phenotype-vector clustering from association testing; state the RC1 scope accurately.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Claim/evidence and cited source.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: README, version, claim register.

### 2. The scientific problem: structure among genetically informed phenotype vectors

- Audience: Foundation; prerequisites: 1.
- Observable objective: Describe the matrix-level scientific question; distinguish a phenotype vector from a variant.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Claim/evidence and cited source.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: data contract, manuscript context.

### 3. Stage 1 scope and the Freeze 3 RC1 status boundary

- Audience: Orientation; prerequisites: 1.
- Observable objective: Classify verified, historical, pending, and out-of-scope claims.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Claim/evidence and cited source.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: release assessment, missing-evidence register.

### 4. From input matrix to candidate partitions

- Audience: Foundation; prerequisites: 1-3.
- Observable objective: Trace data through preprocessing, embedding, clustering, scoring, and retained artifacts.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Claim/evidence and cited source.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: pipeline.py, workflow diagram.

### 5. Essential GWAS, vector-space, distance, and clustering concepts

- Audience: Foundation; prerequisites: 2.
- Observable objective: Define summary statistics, vectors, distances, partitions, and internal metrics.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Claim/evidence and cited source.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: primary methods literature.

### 6. Why repeated nonlinear embeddings and density clustering are used

- Audience: Foundation; prerequisites: 4-5.
- Observable objective: Explain the design rationale while rejecting topology or determinism guarantees.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Claim/evidence and cited source.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: umap_runner.py, UMAP/HDBSCAN papers.

### 7. Choosing among complementary methods

- Audience: Methods; prerequisites: 5-6.
- Observable objective: Compare PCA, ICA, clustering, and multivariate association tools by input, output, and goal.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Claim/evidence and cited source.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: comparator matrix, primary papers.

### 8. Scientific interpretation, circularity, and validation boundaries

- Audience: Methods; prerequisites: 1-7.
- Observable objective: Recognize post-selection circularity and select appropriate validation layers.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Claim/evidence and cited source.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: claim register, selective-inference paper.

## Part II — Installation, data preparation, and the first successful run

### 9. System requirements and isolated environment setup

- Audience: Beginner; prerequisites: basic shell.
- Observable objective: Create an isolated environment; verify the installed version and dependencies.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: pyproject, executed runtime evidence.

### 10. Input data contract, orientation, metadata columns, and missingness

- Audience: Beginner; prerequisites: 2, 9.
- Observable objective: Validate column roles, orientation, identifiers, numeric values, and missingness before a run.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: io.py, preprocessing.py, DATA_CONTRACT.

### 11. Configuration files and precedence

- Audience: Beginner; prerequisites: 9-10.
- Observable objective: Resolve built-in, YAML, and CLI precedence; identify default versus tutorial values.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: config.py, cli.py.

### 12. Inspecting a configuration and enumerating the search space

- Audience: Beginner; prerequisites: 11.
- Observable objective: Use inspect-config and show-search-space; calculate and audit candidate count.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: executed CLI logs, search manifests.

### 13. Fixed synthetic quickstart

- Audience: Beginner; prerequisites: 9-12.
- Observable objective: Execute the canonical bounded run without overwriting prior outputs.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: Tutorial 1 v2.

### 14. Reading the run manifest

- Audience: Beginner; prerequisites: 13.
- Observable objective: Confirm completion, provenance, backends, seeds, threads, and hashes.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: Tutorial 1 run_manifest.json.

## Part III — The complete DIMPLE-GWAS workflow

### 15. Preprocessing and optional RINT

- Audience: Operational; prerequisites: 10-11.
- Observable objective: Explain the implemented transformation order and decide when RINT is configured.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: preprocessing.py, tests.

### 16. UMAP and densMAP fundamentals

- Audience: Methods; prerequisites: 5-6, 15.
- Observable objective: Relate configured UMAP parameters to the implementation without interpreting axes as loadings.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: umap_runner.py, UMAP/densMAP papers.

### 17. Repeated seeds, concatenated embeddings, determinism, and compute cost

- Audience: Methods; prerequisites: 16.
- Observable objective: Trace seed generation and concatenation; bound determinism and resource claims.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: umap_runner.py, manifests.

### 18. HDBSCAN concepts and the Freeze 3 search grid

- Audience: Methods; prerequisites: 5, 17.
- Observable objective: Interpret density parameters and enumerate standard/custom grids.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: hdbscan_runner.py, search_space.py.

### 19. Candidate-model metrics

- Audience: Methods; prerequisites: 18.
- Observable objective: Separate topology, silhouette, DBCV, cluster-size, and projection diagnostics.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: metrics.py, primary metric papers.

### 20. The legacy_dimple score and optional alternatives

- Audience: Methods; prerequisites: 19.
- Observable objective: Reconstruct the score, define dynamic-range weights, and distinguish computed metrics from score terms.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: scoring.py, scoring tests.

### 21. Ranking, summarising, and choosing a model

- Audience: Operational; prerequisites: 18-20.
- Observable objective: Audit eligibility, ranking, ties, Pareto summaries, and selection leakage.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: ranking.py, Tutorial 2.

### 22. Reproducing a selected model

- Audience: Operational; prerequisites: 13-14, 21.
- Observable objective: Build and run a fixed one-model reproduction from a retained JSON contract.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: reproduce-model, Tutorial 3.

### 23. Comparing partitions and validating outputs

- Audience: Operational; prerequisites: 22.
- Observable objective: Use exact IDs, permutation-invariant metrics, and artifact validation correctly.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: comparison.py, validation.py, Tutorial 3.

## Part IV — Explainability and responsible interpretation

### 24. Why UMAP coordinates are not biological loadings

- Audience: Interpretation; prerequisites: 16-17.
- Observable objective: Reject axis-loading and causal interpretations of latent coordinates.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: UMAP paper, explainability docs.

### 25. Returning to the original input-vector space

- Audience: Interpretation; prerequisites: 10, 23-24.
- Observable objective: Explain a retained partition without refitting and audit ID matching.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: interpretation.py, Tutorial 3.

### 26. Pearson and Spearman association summaries

- Audience: Interpretation; prerequisites: 25.
- Observable objective: Interpret descriptive correlation summaries and their assumptions.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: interpretation.py, claim INT-003.

### 27. Cluster heatmaps, ordering, annotations, and cutpoints

- Audience: Interpretation; prerequisites: 25-26.
- Observable objective: Reconstruct heatmap order and read cutpoints and annotations safely.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: Tutorial 3 heatmap artifacts.

### 28. Noise assignments and uncertainty

- Audience: Interpretation; prerequisites: 18, 25.
- Observable objective: Explain label -1 algorithmically and examine its parameter dependence.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: HDBSCAN source/paper.

### 29. Avoiding double dipping and post-selection overclaiming

- Audience: Interpretation; prerequisites: 8, 25-28.
- Observable objective: Identify circular analyses and replace naive inference with bounded description or external validation.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: selective-inference paper.

### 30. Technical, statistical, and biological validation

- Audience: Interpretation; prerequisites: 8, 23, 29.
- Observable objective: Place evidence on the correct validation layer and define pending release gates.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: validation ladder, comparison evidence.

### 31. Reporting a DIMPLE-GWAS analysis

- Audience: Methods; prerequisites: 1-30.
- Observable objective: Report inputs, settings, selection, outputs, limitations, and validation without overclaim.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: claim register, reviewer crosswalk.

## Part V — Worked case studies

### 32. Fixed synthetic dataset case study

- Audience: Worked example; prerequisites: 13-14.
- Observable objective: Reproduce and interpret the verified one-candidate tutorial.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: Tutorial 1 v2.

### 33. Custom bounded search-space case study

- Audience: Worked example; prerequisites: 18-21, 32.
- Observable objective: Explain why 32 candidates are enumerated and compare families without target tuning.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: Tutorial 2.

### 34. Explanation, comparison, and validation case study

- Audience: Worked example; prerequisites: 22-30.
- Observable objective: Execute and interpret all downstream Freeze 3 utilities.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: Tutorial 3.

### 35. MNIST as a software benchmark

- Audience: Worked example; prerequisites: 4-8.
- Observable objective: Interpret the historical known-label benchmark as engineering evidence only.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: MNIST benchmark report.

### 36. Original 164-IDP analysis

- Audience: Worked example; prerequisites: 1-31.
- Observable objective: Separate historical reconstruction from a future fresh 1,000-seed run protocol.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: historical reports/configs, missing-evidence register.

## Part VI — Operational reference

### 37. Complete command reference

- Audience: Reference; prerequisites: 9-14.
- Observable objective: Select the correct command and required inputs for each task.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: command_and_flag_matrix.tsv, --help.

### 38. Complete configuration reference

- Audience: Reference; prerequisites: 11.
- Observable objective: Look up every configuration key, default, constraint, and exposure.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: configuration_key_reference.tsv.

### 39. Search-space reference

- Audience: Reference; prerequisites: 12, 18.
- Observable objective: Calculate standard, extended, custom, and fixed candidate counts.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: search_space.py, executed manifests.

### 40. Scoring and model-selection reference

- Audience: Reference; prerequisites: 19-21.
- Observable objective: Audit formulas, eligible rows, realized weights, and selection manifests.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: scoring.py, ranking.py.

### 41. Output atlas and data dictionary

- Audience: Reference; prerequisites: 14, 23, 25.
- Observable objective: Locate, classify, inspect, and match every produced artifact.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: output_atlas.tsv, executed tutorials.

### 42. Provenance and reproducibility checklist

- Audience: Reference; prerequisites: 14, 17, 23.
- Observable objective: Capture source, input, configuration, environment, seeds, commands, artifacts, and tolerances.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: provenance.py, checksums.

### 43. Error messages, troubleshooting, and recovery

- Audience: Reference; prerequisites: 9-23.
- Observable objective: Diagnose input, configuration, candidate, output-directory, and validation failures without deleting evidence.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: tests, logs, KNOWN_ISSUES.

### 44. Performance, memory, threading, and bounded-run guidance

- Audience: Reference; prerequisites: 12, 17-18.
- Observable objective: Estimate candidate/repeat scale and choose safe thread and smoke-test settings.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: run manifests, resource reports.

### 45. Migration from Dev and Freeze 2

- Audience: Reference; prerequisites: 14, 37-42.
- Observable objective: Map legacy flags/artifacts and distinguish compatibility aliases from new contracts.
- Example: Tutorial evidence or CLI demonstration.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: migration docs, historical adapter tests.

### 46. Known issues and scientific limitations

- Audience: Reference; prerequisites: all.
- Observable objective: Identify all open release gates and communicate limitations precisely.
- Example: Evidence-backed walkthrough or reflection.
- Outputs to inspect: Relevant manifest/table/figure and its checksum.
- Misconception check: distinguish implementation evidence from scientific or biological proof.
- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.
- Evidence: missing-evidence and issue registers.
