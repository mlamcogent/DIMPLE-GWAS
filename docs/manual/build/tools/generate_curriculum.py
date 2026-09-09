#!/usr/bin/env python3
"""Generate the curriculum design evidence used by the modular manual."""

from __future__ import annotations

import csv
from pathlib import Path


FREEZE3 = Path(__file__).resolve().parents[4]
EVIDENCE = FREEZE3 / "docs" / "manual" / "evidence"


CHAPTERS = [
    (1, "What DIMPLE-GWAS is and is not", "Orientation", "none", "Distinguish phenotype-vector clustering from association testing; state the RC1 scope accurately.", "README, version, claim register"),
    (2, "The scientific problem: structure among genetically informed phenotype vectors", "Foundation", "1", "Describe the matrix-level scientific question; distinguish a phenotype vector from a variant.", "data contract, manuscript context"),
    (3, "Stage 1 scope and the Freeze 3 RC1 status boundary", "Orientation", "1", "Classify verified, historical, pending, and out-of-scope claims.", "release assessment, missing-evidence register"),
    (4, "From input matrix to candidate partitions", "Foundation", "1-3", "Trace data through preprocessing, embedding, clustering, scoring, and retained artifacts.", "pipeline.py, workflow diagram"),
    (5, "Essential GWAS, vector-space, distance, and clustering concepts", "Foundation", "2", "Define summary statistics, vectors, distances, partitions, and internal metrics.", "primary methods literature"),
    (6, "Why repeated nonlinear embeddings and density clustering are used", "Foundation", "4-5", "Explain the design rationale while rejecting topology or determinism guarantees.", "umap_runner.py, UMAP/HDBSCAN papers"),
    (7, "Choosing among complementary methods", "Methods", "5-6", "Compare PCA, ICA, clustering, and multivariate association tools by input, output, and goal.", "comparator matrix, primary papers"),
    (8, "Scientific interpretation, circularity, and validation boundaries", "Methods", "1-7", "Recognize post-selection circularity and select appropriate validation layers.", "claim register, selective-inference paper"),
    (9, "System requirements and isolated environment setup", "Beginner", "basic shell", "Create an isolated environment; verify the installed version and dependencies.", "pyproject, executed runtime evidence"),
    (10, "Input data contract, orientation, metadata columns, and missingness", "Beginner", "2, 9", "Validate column roles, orientation, identifiers, numeric values, and missingness before a run.", "io.py, preprocessing.py, DATA_CONTRACT"),
    (11, "Configuration files and precedence", "Beginner", "9-10", "Resolve built-in, YAML, and CLI precedence; identify default versus tutorial values.", "config.py, cli.py"),
    (12, "Inspecting a configuration and enumerating the search space", "Beginner", "11", "Use inspect-config and show-search-space; calculate and audit candidate count.", "executed CLI logs, search manifests"),
    (13, "Fixed synthetic quickstart", "Beginner", "9-12", "Execute the canonical bounded run without overwriting prior outputs.", "Tutorial 1 v2"),
    (14, "Reading the run manifest", "Beginner", "13", "Confirm completion, provenance, backends, seeds, threads, and hashes.", "Tutorial 1 run_manifest.json"),
    (15, "Preprocessing and optional RINT", "Operational", "10-11", "Explain the implemented transformation order and decide when RINT is configured.", "preprocessing.py, tests"),
    (16, "UMAP and densMAP fundamentals", "Methods", "5-6, 15", "Relate configured UMAP parameters to the implementation without interpreting axes as loadings.", "umap_runner.py, UMAP/densMAP papers"),
    (17, "Repeated seeds, concatenated embeddings, determinism, and compute cost", "Methods", "16", "Trace seed generation and concatenation; bound determinism and resource claims.", "umap_runner.py, manifests"),
    (18, "HDBSCAN concepts and the Freeze 3 search grid", "Methods", "5, 17", "Interpret density parameters and enumerate standard/custom grids.", "hdbscan_runner.py, search_space.py"),
    (19, "Candidate-model metrics", "Methods", "18", "Separate topology, silhouette, DBCV, cluster-size, and projection diagnostics.", "metrics.py, primary metric papers"),
    (20, "The legacy_dimple score and optional alternatives", "Methods", "19", "Reconstruct the score, define dynamic-range weights, and distinguish computed metrics from score terms.", "scoring.py, scoring tests"),
    (21, "Ranking, summarising, and choosing a model", "Operational", "18-20", "Audit eligibility, ranking, ties, Pareto summaries, and selection leakage.", "ranking.py, Tutorial 2"),
    (22, "Reproducing a selected model", "Operational", "13-14, 21", "Build and run a fixed one-model reproduction from a retained JSON contract.", "reproduce-model, Tutorial 3"),
    (23, "Comparing partitions and validating outputs", "Operational", "22", "Use exact IDs, permutation-invariant metrics, and artifact validation correctly.", "comparison.py, validation.py, Tutorial 3"),
    (24, "Why UMAP coordinates are not biological loadings", "Interpretation", "16-17", "Reject axis-loading and causal interpretations of latent coordinates.", "UMAP paper, explainability docs"),
    (25, "Returning to the original input-vector space", "Interpretation", "10, 23-24", "Explain a retained partition without refitting and audit ID matching.", "interpretation.py, Tutorial 3"),
    (26, "Pearson and Spearman association summaries", "Interpretation", "25", "Interpret descriptive correlation summaries and their assumptions.", "interpretation.py, claim INT-003"),
    (27, "Cluster heatmaps, ordering, annotations, and cutpoints", "Interpretation", "25-26", "Reconstruct heatmap order and read cutpoints and annotations safely.", "Tutorial 3 heatmap artifacts"),
    (28, "Noise assignments and uncertainty", "Interpretation", "18, 25", "Explain label -1 algorithmically and examine its parameter dependence.", "HDBSCAN source/paper"),
    (29, "Avoiding double dipping and post-selection overclaiming", "Interpretation", "8, 25-28", "Identify circular analyses and replace naive inference with bounded description or external validation.", "selective-inference paper"),
    (30, "Technical, statistical, and biological validation", "Interpretation", "8, 23, 29", "Place evidence on the correct validation layer and define pending release gates.", "validation ladder, comparison evidence"),
    (31, "Reporting a DIMPLE-GWAS analysis", "Methods", "1-30", "Report inputs, settings, selection, outputs, limitations, and validation without overclaim.", "claim register, reviewer crosswalk"),
    (32, "Fixed synthetic dataset case study", "Worked example", "13-14", "Reproduce and interpret the verified one-candidate tutorial.", "Tutorial 1 v2"),
    (33, "Custom bounded search-space case study", "Worked example", "18-21, 32", "Explain why 32 candidates are enumerated and compare families without target tuning.", "Tutorial 2"),
    (34, "Explanation, comparison, and validation case study", "Worked example", "22-30", "Execute and interpret all downstream Freeze 3 utilities.", "Tutorial 3"),
    (35, "MNIST as a software benchmark", "Worked example", "4-8", "Interpret the historical known-label benchmark as engineering evidence only.", "MNIST benchmark report"),
    (36, "Original 164-IDP analysis", "Worked example", "1-31", "Separate historical reconstruction from a future fresh 1,000-seed run protocol.", "historical reports/configs, missing-evidence register"),
    (37, "Complete command reference", "Reference", "9-14", "Select the correct command and required inputs for each task.", "command_and_flag_matrix.tsv, --help"),
    (38, "Complete configuration reference", "Reference", "11", "Look up every configuration key, default, constraint, and exposure.", "configuration_key_reference.tsv"),
    (39, "Search-space reference", "Reference", "12, 18", "Calculate standard, extended, custom, and fixed candidate counts.", "search_space.py, executed manifests"),
    (40, "Scoring and model-selection reference", "Reference", "19-21", "Audit formulas, eligible rows, realized weights, and selection manifests.", "scoring.py, ranking.py"),
    (41, "Output atlas and data dictionary", "Reference", "14, 23, 25", "Locate, classify, inspect, and match every produced artifact.", "output_atlas.tsv, executed tutorials"),
    (42, "Provenance and reproducibility checklist", "Reference", "14, 17, 23", "Capture source, input, configuration, environment, seeds, commands, artifacts, and tolerances.", "provenance.py, checksums"),
    (43, "Error messages, troubleshooting, and recovery", "Reference", "9-23", "Diagnose input, configuration, candidate, output-directory, and validation failures without deleting evidence.", "tests, logs, KNOWN_ISSUES"),
    (44, "Performance, memory, threading, and bounded-run guidance", "Reference", "12, 17-18", "Estimate candidate/repeat scale and choose safe thread and smoke-test settings.", "run manifests, resource reports"),
    (45, "Migration from Dev and Freeze 2", "Reference", "14, 37-42", "Map legacy flags/artifacts and distinguish compatibility aliases from new contracts.", "migration docs, historical adapter tests"),
    (46, "Known issues and scientific limitations", "Reference", "all", "Identify all open release gates and communicate limitations precisely.", "missing-evidence and issue registers"),
]


PARTS = {
    range(1, 9): "Part I — Orientation and conceptual foundations",
    range(9, 15): "Part II — Installation, data preparation, and the first successful run",
    range(15, 24): "Part III — The complete DIMPLE-GWAS workflow",
    range(24, 32): "Part IV — Explainability and responsible interpretation",
    range(32, 37): "Part V — Worked case studies",
    range(37, 47): "Part VI — Operational reference",
}


def part_for(number: int) -> str:
    return next(name for numbers, name in PARTS.items() if number in numbers)


def write_tsv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Curriculum specification", "",
        "The curriculum is progressive but layered: beginners can follow Chapters 1, 3–4, and 9–14 before returning to the methods chapters; operators can use Parts III and VI; reviewers can trace claims through Parts I, IV, the bibliography, and the evidence registers.", "",
        "Every chapter uses the same teaching contract: orientation, observable objectives, prerequisites, plain-language model, implementation truth, evidence-backed example, outputs, mistakes, boundaries, and a completion check. Defaults, tutorial values, historical values, and recommendations are explicitly labelled.", "",
    ]
    current = None
    objective_rows = []
    dependency_lines = ["# Chapter dependency map", "", "An arrow means ‘read or understand before’. The quickstart route is deliberately short.", "", "```mermaid", "flowchart LR", "  C1[\"1: scope\"] --> C3[\"3: RC1 boundary\"]", "  C3 --> C4[\"4: workflow\"]", "  C4 --> C9[\"9: setup\"]", "  C9 --> C10[\"10: data\"]", "  C10 --> C11[\"11: config\"]", "  C11 --> C12[\"12: inspect\"]", "  C12 --> C13[\"13: run\"]", "  C13 --> C14[\"14: verify\"]", "  C14 --> C15[\"15: preprocessing\"]", "  C15 --> C16[\"16: UMAP\"]", "  C16 --> C17[\"17: repeats\"]", "  C17 --> C18[\"18: HDBSCAN\"]", "  C18 --> C19[\"19: metrics\"]", "  C19 --> C20[\"20: score\"]", "  C20 --> C21[\"21: select\"]", "  C21 --> C22[\"22: reproduce\"]", "  C22 --> C23[\"23: compare/validate\"]", "  C23 --> C25[\"25: original space\"]", "  C25 --> C29[\"29: circularity\"]", "  C29 --> C30[\"30: validation\"]", "```", "", "## Per-chapter prerequisites", ""]
    for number, title, level, prerequisites, objective, evidence in CHAPTERS:
        part = part_for(number)
        if part != current:
            lines.extend([f"## {part}", ""])
            current = part
        executable = "Tutorial evidence or CLI demonstration" if number in {9, 10, 11, 12, 13, 14, 22, 23, 25, 27, 32, 33, 34, 37, 38, 39, 40, 41, 42, 43, 44, 45} else "Evidence-backed walkthrough or reflection"
        outputs = "Relevant manifest/table/figure and its checksum" if number >= 9 else "Claim/evidence and cited source"
        lines.extend([
            f"### {number}. {title}", "",
            f"- Audience: {level}; prerequisites: {prerequisites}.",
            f"- Observable objective: {objective}",
            f"- Example: {executable}.",
            f"- Outputs to inspect: {outputs}.",
            f"- Misconception check: distinguish implementation evidence from scientific or biological proof.",
            f"- Caveat: retain RC1, historical-versus-fresh, and descriptive-versus-inferential boundaries where relevant.",
            f"- Evidence: {evidence}.", "",
        ])
        objective_rows.append([number, title, level, prerequisites, objective, executable, outputs, evidence])
        dependency_lines.append(f"- Chapter {number}: `{prerequisites}` → **{title}**")
    (EVIDENCE / "curriculum_specification.md").write_text("\n".join(lines), encoding="utf-8")
    (EVIDENCE / "chapter_dependency_map.md").write_text("\n".join(dependency_lines) + "\n", encoding="utf-8")
    write_tsv(EVIDENCE / "learning_objectives.tsv", ["chapter", "title", "audience", "prerequisites", "observable_learning_objective", "example_type", "outputs_to_inspect", "evidence"], objective_rows)

    glossary = [
        ["GWAS", "genome-wide association study", "A study that tests associations between genetic variants and a phenotype.", "5", "Do not confuse a GWAS association with causation."],
        ["summary statistic", "statistical result for one variant–phenotype test", "In the input matrix, an analysis value indexed by a variant row and vector column.", "2,5,10", "The exact measure and harmonization must be documented upstream."],
        ["vector / IDP", "one phenotype-associated column across variants", "The unit clustered after the input matrix is prepared and transposed.", "2,10", "IDP is a domain-specific vector label, not a generic feature."],
        ["feature_id", "stable retained vector identifier", "Identifier written with labels and used for exact matching.", "10,23,25,41", "Whitespace and duplicates are validation concerns."],
        ["RINT", "rank inverse normal transformation", "Optional rank-based normalization applied before transpose as implemented.", "15", "Off by default; it changes the analysis values."],
        ["UMAP", "Uniform Manifold Approximation and Projection", "Nonlinear neighborhood-based embedding used by the pipeline.", "6,16", "Axes are not biological loadings."],
        ["densMAP", "density-augmented UMAP", "UMAP mode adding a density-correlation objective.", "16", "Density preservation is not biological validation."],
        ["seed", "pseudorandom initializer", "Base or derived integer controlling a repeated embedding.", "17", "A fixed seed does not ensure cross-platform bitwise equality."],
        ["concatenated embedding", "horizontal concatenation of repeated embeddings", "The high-dimensional representation supplied to HDBSCAN.", "17", "An empirical stability strategy, not a true-topology estimator."],
        ["HDBSCAN", "hierarchical density-based spatial clustering of applications with noise", "Density-clustering backend used to label vectors.", "18", "Freeze 3 uses the contributed hdbscan package."],
        ["candidate model", "one UMAP-family and HDBSCAN-parameter combination", "A complete enumerated configuration that produces a retained success, invalid topology, or failure row.", "18-21", "A candidate is not necessarily eligible for ranking."],
        ["selected model", "rank-one retained eligible candidate", "The candidate named in best_model.json and the selection manifest.", "21-22", "Selection is heuristic and conditional on the searched population."],
        ["noise label -1", "HDBSCAN noise/unassigned status", "Algorithmic non-membership under one representation and parameterization.", "18,28", "Not biological irrelevance or absence of pleiotropy."],
        ["silhouette", "within-versus-nearest-cluster separation diagnostic", "Metric-aware internal partition score used by legacy_dimple.", "19-20", "Geometry dependent; not biological validation."],
        ["DBCV", "density-based clustering validation", "Optional density-aware diagnostic recorded by Freeze 3.", "19-20", "Not a legacy_dimple score component."],
        ["ARI", "adjusted Rand index", "Permutation-invariant pairwise partition concordance metric.", "23", "Does not test biological validity."],
        ["NMI", "normalized mutual information", "Permutation-invariant information overlap between partitions.", "23", "Numeric label values need not match."],
        ["Procrustes disparity", "shape discrepancy after alignment", "Coordinate-only comparison diagnostic when both artifacts supply coordinates.", "23", "Separate from membership concordance."],
        ["structural concordance", "agreement in partition structure", "Comparison of labels/noise sets invariant to label renaming.", "23,30", "Not exact computational reproduction."],
        ["biological validation", "external evidence that a grouping reflects meaningful biology", "A later evidence layer beyond software and internal metrics.", "30", "Not established by passing tests or MNIST."],
        ["provenance", "record of source, inputs, settings, environment, commands, and artifacts", "Evidence required to interpret and reproduce a run.", "14,42", "A dependency list alone is insufficient."],
    ]
    write_tsv(EVIDENCE / "glossary_source.tsv", ["term", "expanded_form_or_type", "definition", "first_chapters", "boundary_note"], glossary)


if __name__ == "__main__":
    main()
