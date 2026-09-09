# 31. Reporting a DIMPLE-GWAS analysis

> **Release status.** DIMPLE-GWAS Freeze 3 RC1 (`3.0.0rc1`) is software-complete under local and fixed-fixture evidence. It is not yet scientifically frozen or cross-platform validated.

## Orientation

This chapter belongs to **Part IV — Explainability and responsible interpretation**. It separates observed Freeze 3 behavior from scientific interpretation, historical evidence, and pending release work.

## Learning objectives

After this chapter, you can:

- Report inputs, settings, selection, outputs, limitations, and validation without overclaim.
- identify the evidence artifact that supports the behavior or boundary;
- describe one common misuse in language appropriate for a methods report.

Prerequisites: 1-30.

## Explanation and implementation

A complete report states: software/version/source identity; input cohort and upstream GWAS construction; matrix shape/orientation/metadata prefix; preprocessing; UMAP/densMAP parameters, repeat/seed sequence, and metric; HDBSCAN search space and backend; candidate counts/failures; all calculated metrics; scoring formula/profile/noise term; selection/ties/manual decisions; retained cluster/noise counts; original-space descriptive summaries; sensitivity/comparison evidence; validation layer; and limitations.

Use conditional language: ‘under the specified representation and HDBSCAN parameters, the selected model assigned…’. Separate implementation results from interpretation and hypotheses. Disclose the historical manual row-16 choice. Name unassigned observations neutrally. If results come from adapted historical labels, say so. Include exact artifact identifiers/checksums in supplements or repositories permitted by data policy.

Methods should be reproducible without claiming bitwise platform independence; results should be readable without turning internal scores into biological proof.

## Evidence-backed example

A safe synthetic sentence is: ‘In the 24-vector fixed fixture, the one-candidate RC1 run assigned three clusters of eight and no noise; a same-environment fixed rerun had ARI and NMI 1. These engineering checks do not establish biological validity.’

## Outputs to inspect

Report from resolved config, run/selection manifests, all/ranked models, retained summary/labels, explanation/comparison/validation manifests, source/input hashes, and issue register.

## Common mistakes

Do not omit failed candidates, ties, noise, manual selection, or pending gates. Do not present display axes as biological components. Do not claim causal mechanisms from correlations.

## Scientific and operational limits

Journal word limits may require a concise main text; place complete contracts and machine-readable evidence in a suitable supplement without exposing restricted data.

## Completion check

Draft a methods paragraph and results paragraph for Tutorial 2, then highlight every phrase supported only by internal rather than external evidence.

<p class="xref"><strong>Operational cross-reference:</strong> Chapter 37 covers commands, Chapter 38 configuration, Chapter 41 artifact schemas, Chapter 42 provenance, and Chapter 46 current limitations.</p>
