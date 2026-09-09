# Preface: three ways through one method

DIMPLE-GWAS sits at an awkward but productive boundary. It is a scientific method whose output can be tempting to overinterpret, a computational pipeline whose behavior depends on exact contracts, and a teaching problem that spans summary-statistic geometry, nonlinear representation, density clustering, model selection, and post-selection reasoning. Earlier documentation placed all of those responsibilities in the same stream. The result was comprehensive but difficult to learn from.

Documentation Edition 3 separates the reading tasks while preserving one evidence base.

The **academic textbook** develops the method in dependency order. It begins with the scientific unit, then builds the geometry, nonlinear representation, density hierarchy, model search, selection, validation, and interpretation. Equations are used to expose assumptions rather than to decorate prose. Implementation details appear where they illuminate a statistical decision; exhaustive contracts are deferred to the reference.

The **analyst workbook** begins with predictions and checkpoints. A learner inspects configuration before computing, uses a fresh output root, reads manifests before plots, compares partitions without relying on numeric label names, and labels every case as fresh, retained, reconstructed, illustrative, or protocol-only.

The **technical reference** is deliberately lookup-oriented. It records commands, defaults, function and output contracts, errors, provenance, and the analysis hierarchy. This is where exact implementation traceability belongs.

## Suggested paths

**New analyst.** Read Chapters 1-3, then complete Workbook Labs 0-4. Return to Chapters 8-11 before expanding a search. Use the reference when an option, field, or failure needs exact interpretation.

**Statistics or data-science learner.** Read the textbook in order and work the numerical interludes. Chapters 5-8 form the UMAP/densMAP/HDBSCAN spine; Chapters 9-11 show why model search and validation cannot be treated as afterthoughts.

**Domain scientist.** Begin with Chapters 1, 2, 12, 13, and 14. These chapters distinguish algorithmic grouping from genetic or biological explanation and show how retained historical results differ from fresh reruns.

**Methods reviewer.** Read Chapters 10-15, then use the technical reference, claim register, reviewer-literature crosswalk, analysis hierarchy, and known-limitations file.

## Evidence vocabulary

This edition uses five status words consistently:

- **Freshly executed** means run during the recorded Stage 1 local verification.
- **Retained historical** means preserved from an earlier analysis with immutable artifact identity.
- **Reconstructed** means derived exactly from retained artifacts, for example reapplying a score or adapting a schema, without refitting the original model.
- **Illustrative** means chosen to teach a calculation or decision and not presented as empirical evidence.
- **Protocol-only** means the commands and acceptance criteria are specified but the consequential run has not been performed.

The distinction is part of the scientific result. A hash check, an exact fixed-fixture replay, a table rescore, a retained-label adapter, a fresh manuscript-scale fit, and an external biological replication answer different questions.

## Notation and conventions

We write an input table as $X \in \mathbb{R}^{v \times p}$, with $v$ aligned variant rows and $p$ phenotype-associated vectors or IDPs in analysis columns. After metadata removal, validation, optional column-wise transformation, and transposition, the working matrix is $Y=X^{\mathsf T}\in\mathbb{R}^{p\times v}$: one row per object being clustered.

The term *noise* is reserved for HDBSCAN label `-1`. It means unassigned under a fitted representation and parameterization. It is never shorthand for failed biology, a non-heritable phenotype, or a phenotype without pleiotropic relationships.

Citations support general methodological context. They do not validate DIMPLE-GWAS outputs. Software-specific facts are tied to the Stage 1 claim and implementation registers.

\newpage
