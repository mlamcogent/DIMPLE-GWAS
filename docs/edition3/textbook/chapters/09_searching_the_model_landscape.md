# Searching the model landscape

A model cannot win against candidates that were never considered. The DIMPLE-GWAS search space is therefore part of the estimand. It declares which UMAP/densMAP families, HDBSCAN settings, metrics, and other options are eligible to compete.

## Cartesian enumeration

If a configuration provides parameter lists $A_1,\ldots,A_m$, the candidate set is their Cartesian product,

$$
\mathcal{C}=A_1\times A_2\times\cdots\times A_m,
\qquad |\mathcal{C}|=\prod_{\ell=1}^{m}|A_\ell|.
$$

Three neighbor values, two `min_dist` values, two seed counts, four minimum cluster sizes, three minimum-samples values, and two selection methods already create $3\times2\times2\times4\times3\times2=288$ candidates before adding metrics or epsilon values.

Freeze 3 enumerates the declared product deterministically. It does not silently sample a large grid. Stable content-derived identifiers name candidates and UMAP families. Standard mode currently enumerates 2,430 candidates; extended mode 1,728; the fixed tutorial one. A hard limit and warning thresholds protect against accidental explosion.

## Preflight before compute

The `show-search-space` command resolves configuration and writes or displays the candidate population without fitting. This is one of the most important commands in the software because it converts a vague configuration into a countable computational and scientific commitment.

A preflight should answer:

- Which parameters vary, and why are their values plausible?
- Which settings define reusable UMAP families and which require new embeddings?
- How many candidates will be fitted?
- Which metrics and noise rules apply?
- What failure and retention policy is active?
- How many top models and label artifacts will be retained?
- Is the output root new and empty?

The Stage 1 enumeration of standard and extended spaces exited zero without fitting either large grid. Enumeration evidence is not execution evidence.

## Search design encodes scientific beliefs

A narrow grid can miss relevant structure. A very broad grid can create selection optimism: with enough noisy candidates, one may look excellent by chance or by exploiting an internal criterion [@cawley2010selection; @varma2006bias]. Search breadth is therefore neither inherently conservative nor inherently rigorous.

The candidate set should be large enough to test plausible structural choices and small enough that every family has a scientific rationale. Parameters chosen to force a desired cluster count or noise fraction convert exploration into target-driven selection. The Modded lineage contained a soft score favoring particular cluster and noise targets; Freeze 3 rejected that as biologically pre-committed.

## Separate representation families from cluster candidates

Many HDBSCAN candidates can reuse one concatenated embedding when their UMAP-family settings are identical. Freeze 3 groups and caches by stable family identity. This saves compute and makes the hierarchy visible: representation choices sit above density-partition choices.

This structure also improves analysis. One can summarize the best and typical behavior within each representation family, ask whether a family has many invalid topologies, and compare selected partitions across families. A single global winner can hide that an entire family is unstable or that several families yield structurally equivalent partitions.

## Failures are data about the search

Backend exceptions, invalid topologies, and eligible candidates are different outcomes. Freeze 3 retains failed and invalid rows, writes a failure log, and can operate in strict mode when an error should stop the run. Hiding failures would overstate the effective search and bias later summaries.

Suppose 200 candidates are declared, 150 fail due to a metric/backend interaction, 45 produce one cluster, and five are eligible. Calling the selected model “best of 200” is misleading. It is the deterministic winner among five eligible candidates inside a search with substantial failure and collapse. The failure pattern should influence whether the search design is trusted.

## Compute, memory, and reproducibility

Repeated embeddings, candidate parallelism, BLAS/OpenMP threads, just-in-time compilation, and retained top artifacts all affect resource use. Exact runtime depends on $p$, $v$, seed count, neighbor search, representation families, candidates, dependencies, architecture, and cache state. Edition 3 uses runtime classes rather than inventing universal minute estimates.

Parallelism can also alter numerical order and reproducibility. A responsible production run records requested jobs and relevant thread variables, uses a fresh output root, monitors failures, and preserves the environment manifest. More workers are not always faster when nested libraries oversubscribe cores.

## A bounded custom-search example

Edition 2 retained a 32-candidate custom tutorial, and Stage 1 verified current search enumeration and the one-candidate fixed path. A small custom search is pedagogically useful when it varies one representation decision and one or two HDBSCAN decisions, then asks the reader to interpret failures, ties, family summaries, and partition comparisons. It is not a substitute for a prespecified real-data sensitivity design.

For example, one might compare two neighbor sizes, two seeds, two minimum cluster sizes, two minimum-samples values, and EOM versus leaf: $2^5=32$ candidates if all combinations are admissible. Before running, the learner predicts which parameter changes may increase noise and which belong to the same UMAP family. After running, the learner checks those predictions against artifacts rather than selecting by the nicest plot.

## Search-space provenance

The resolved configuration records the inputs after precedence resolution. Search manifests record candidates and identifiers. Model tables record status and metrics. The run manifest reconciles declared, successful, invalid, and failed counts. These artifacts define the population to which the score and rank refer.

The next chapter examines that score. Because the legacy formula depends on the observed ranges of the candidate table, changing the search changes not only the candidates but also the numerical scale on which they are selected.

**Evidence trail.** Claims SEA-001 to SEA-003, OUT-001 and SLM-011; coverage COV-008, COV-014 and COV-023.

## Questions for the reader

1. Calculate the size of a grid with 3 neighbor values, 2 dimensions, 5 cluster sizes, 4 minimum-samples values, and 2 selection methods.
2. Why is a candidate failure log part of statistical reporting rather than only debugging?
3. Describe one risk of a search that is too narrow and one risk of a search that is too broad.

\newpage
