# 1. What DIMPLE-GWAS is and is not

> **Release status.** DIMPLE-GWAS Freeze 3 RC1 (`3.0.0rc1`) is software-complete under local and fixed-fixture evidence. It is not yet scientifically frozen or cross-platform validated.

## Orientation

This chapter belongs to **Part I — Orientation and conceptual foundations**. It separates observed Freeze 3 behavior from scientific interpretation, historical evidence, and pending release work.

## Learning objectives

After this chapter, you can:

- Distinguish phenotype-vector clustering from association testing; state the RC1 scope accurately.
- identify the evidence artifact that supports the behavior or boundary;
- describe one common misuse in language appropriate for a methods report.

Prerequisites: none.

## Explanation and implementation

DIMPLE-GWAS Stage 1 groups phenotype-associated vectors according to structure in their genetic association profiles. It accepts a variant-by-vector matrix, creates a nonlinear representation, fits density-based partitions, ranks declared candidates, and preserves selected labels and provenance. It does not run a GWAS, identify causal variants, perform enrichment, fine mapping, PRS, QTL analysis, Genomic SEM, genomic PCA/ICA, MTAG, PLEIO, or MOSTest. Those may be upstream, downstream, or comparator methods, but they are not hidden Freeze 3 features.

The unit clustered is a vector/IDP, not a person and not a variant. A cluster is an algorithmic grouping conditional on input construction, preprocessing, metric, embedding parameters, seeds, HDBSCAN settings, candidate population, and selection rule. Treat it as a testable descriptive structure rather than a biological truth label.

## Evidence-backed example

Read `pyproject.toml`, run `dimple-gwas --version`, and inspect `evidence/software_truth_report.md`. All identify package `3.0.0rc1`; the evidence report also names pending scientific and cross-platform gates.

## Outputs to inspect

Start with `run_manifest.json`, `models/model_selection_manifest.json`, retained `labels.tsv`, and the claim/evidence register. Together they answer what was run, what was selected, and how strongly it may be interpreted.

## Common mistakes

Do not describe the software as a multivariate association test or an automatic biological-discovery engine. Do not collapse Stage 1 clustering and later scientific validation into one claim.

## Scientific and operational limits

The current build proves local software behavior and bounded fixture reproduction. It does not prove that any real-data cluster is stable, causal, clinically useful, or externally replicated.

## Completion check

In one sentence, name the clustered unit, the implemented output, and one task the software does not perform. Then label the release correctly as RC1.

<p class="xref"><strong>Operational cross-reference:</strong> Chapter 37 covers commands, Chapter 38 configuration, Chapter 41 artifact schemas, Chapter 42 provenance, and Chapter 46 current limitations.</p>
