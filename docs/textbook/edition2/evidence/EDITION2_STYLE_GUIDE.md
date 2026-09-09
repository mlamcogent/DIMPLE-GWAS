# Textbook Edition 2 style and evidence guide

## Editorial position

Textbook Edition 2 is an internal-review draft designed to be publication-ready in substance. It names the software as **DIMPLE-GWAS Freeze 3 RC1** and the document as **DIMPLE-GWAS Freeze 3 RC1 Academic Textbook and Analyst Reference, Edition 2**. It never implies that documentation work creates a new software freeze. The standing release sentence is:

> DIMPLE-GWAS Freeze 3 RC1 is a software-complete release candidate under current local and fixed-fixture evidence. It is not yet a scientifically frozen or cross-platform validated release.

Use that sentence in front matter and where the evidence boundary is genuinely material. Do not repeat it as a chapter-opening banner.

## Voice and progression

Write connected academic prose. Begin with the scientific or analytical problem, develop plain-language intuition, introduce notation, and only then state equations. Interpret every displayed equation immediately in words. Transitions must explain why the next idea is needed; headings are not substitutes for transitions.

Separate four kinds of statement explicitly:

1. a general statistical principle, supported by a primary source;
2. current DIMPLE-GWAS behavior, supported by source, tests, help text, or a fresh output;
3. a historical result, supported by preserved historical evidence;
4. an interpretation or recommendation, bounded by assumptions and counterexamples.

Avoid promotional adjectives, biological shorthand that turns an algorithmic label into a mechanism, and claims that one method is universally superior. The reader should always know whether a number is a default, an example setting, a historical value, or a fresh measurement.

## Mathematical conventions

Define symbols before use and maintain the notation appendix. Use vectors in lowercase bold where rendering permits, matrices in uppercase, and sets in calligraphic or plainly named notation. State dimensions. For a matrix containing variants by phenotype-associated vectors, use (X\in\mathbb{R}^{v\times p}) before preprocessing and (X^\top\in\mathbb{R}^{p\times v}) after the production transpose.

Give the exact implemented formula when describing DIMPLE-GWAS. If a library performs the operation, say that DIMPLE-GWAS delegates it and distinguish the pedagogical equation from reimplemented code. Discuss edge cases—ties, missing values, degenerate ranges, too few clusters, noise denominators, sampling, and undefined correlations—beside the formula, not in a remote disclaimer.

## Implementation traceability

Function names use code styling and resolve to the function atlas. A full Tier A/B dossier records: purpose; scientific role; source; callers; signature; argument semantics; defaults; accepted types; input shape; output type and shape; side effects; generated files; exceptions; warnings; deterministic controls; complexity; tests; executed evidence; chapter/example; and limitations. Main chapters may present the fields that aid learning and link to the complete atlas row, but no required field may remain blank in the final dossier table.

Commands must be copied from fresh `--help`, shown with a fresh output directory, and labeled as executed, syntax-checked, historical, or protocol-only. A command transcript must preserve exit status, environment, timestamps, checksums, logs, seeds, and deviations.

## Evidence and citations

Use citation keys in the form `[@key]` immediately after the supported claim. Every cited key must occur in the verified bibliography and citation-verification log. Prefer primary papers and official API documentation. Never treat a citation as proof of a DIMPLE-GWAS result. Private reviewer correspondence may inform a sanitized method crosswalk but must not be quoted or exposed.

Claims inherit their status from `claim_evidence_register.tsv`: verified, verified with qualification, implementation-specific, historical-only, hypothesis, educational simplification, unresolved, or rejected. Rejected wording may appear only as a misconception that is explicitly corrected. Unresolved attribution is not publishable fact.

## Pedagogical components

Each substantive chapter includes learning objectives and prerequisites, but chapter structures should vary. Use definition, caution, implementation, historical, and pending-validation callouts sparingly. Each core method needs both a hand-worked example and a traceable software example. Exercises mix conceptual reasoning, calculation, source/output inspection, and communication; every exercise has a solution in the solutions appendix.

A worked example states which simplifications are educational. An executed example names its retained lab, configuration, command, software version, and evidence status. Output excerpts preserve column names and representative values but omit protected identifiers and absolute personal paths.

## Interpretation guardrails

- DIMPLE-GWAS clusters phenotype-associated vectors or IDPs, not people or variants.
- UMAP coordinates are descriptive latent coordinates, not biological loadings.
- Repeated embeddings and concatenation are empirical representation choices, not a proof of consensus or true topology.
- HDBSCAN `-1` is a parameter-conditional unassigned label, not a biological-null class.
- Silhouette is metric-configurable; Calinski–Harabasz and Davies–Bouldin use Euclidean centroid geometry in the current implementation.
- DBCV is supplementary under `legacy_dimple`.
- Original-space correlation and heatmaps are conditional descriptive diagnostics after selection.
- Exact fixture agreement is not biological or cross-platform validation.
- A pinned container controls an environment but does not guarantee bitwise identity everywhere.

## Visual and layout rules

Use figures only when they explain geometry, flow, hierarchy, or quantitative evidence better than prose. Keep editable source and deterministic render scripts. Figure text must be at least 8 pt in the composed PDF, code at least 8.5 pt, and body text approximately 10.5–11.5 pt. Use a colorblind-safe palette with redundant labels or shapes. Captions state the evidence source, what to notice, and what not to infer.

No diagram may rely on unrendered Mermaid in the final PDF. Source and page-level QA must confirm no overlap, clipping, crossing labels, accidental splitting, or detached captions. Wide diagrams use landscape or panels rather than illegible compression.

## Editing and scoring

Run duplication checks after each chapter. Avoid stock opening sentences, repeated checklists, and large status boxes. Core method chapters must score at least 90/100 and all other chapters at least 85/100 under the calibration rubric. A chapter fails regardless of total score if any rubric category is zero, a material claim is unresolved, a command is falsely labeled executed, or an output interpretation exceeds its evidence.
