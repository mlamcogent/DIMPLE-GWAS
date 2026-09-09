# From discovered topology to defensible biological claims

Unsupervised analysis creates hypotheses precisely because it can reveal structure that was not prespecified. The same flexibility creates an inferential problem: after choosing clusters from the data, it is easy to test those clusters on the same data and treat a small $p$-value as confirmation.

## The double-use problem

Suppose a pipeline selects a partition because it maximizes internal separation. The analyst then tests whether the selected groups differ on a variable that contributed to the representation or selection. The groups were constructed to differ under related information, so the ordinary null distribution no longer describes a prespecified comparison. This is a form of circular analysis or “double dipping” [@kriegeskorte2009double].

The problem is broader than reusing an identical column. Trying many preprocessing choices, clusterings, annotations, and narrative labels before reporting the strongest contrast also creates selection. A conventional test that ignores this search can be anti-conservative.

## Descriptive characterization is still valuable

The appropriate response is not to forbid post hoc analysis. A selected cluster can be described: its members, original-space similarity, annotation composition, noise boundary, and sensitivity. Descriptive summaries help formulate hypotheses and design follow-up.

The language should match the design. “The selected cluster contained…” and “members showed a higher descriptive similarity…” are supported by the retained artifacts. “The cluster represents a causal pathway” requires evidence that the discovery pipeline does not supply.

## Paths to stronger inference

**Independent validation.** Apply a prespecified representation and assignment or comparison strategy to an independent cohort or data release. Independence is strongest when upstream GWAS estimation is also independent.

**Sample splitting.** Use one partition of the data for discovery and another for confirmation. In summary-statistic settings, creating genuinely independent splits may be difficult and can reduce precision, but the principle makes the information boundary explicit.

**Nested resampling.** Repeat all tuning inside resamples and evaluate held-out structure outside the selection loop. This addresses some selection optimism but requires a defined target and a way to map clusters across folds.

**Selective inference.** Use methods whose null distribution accounts for the selection event. Selective inference for hierarchical clustering exists in specialized settings but is not implemented by DIMPLE-GWAS [@gao2024selective]. One cannot obtain its guarantees by adding a caution sentence to an ordinary test.

**External biological evidence.** Functional annotations, QTLs, fine mapping, colocalization, experimental results, or clinical associations can support interpretation when their design is appropriate. DIMPLE-GWAS does not execute these analyses, and their presence does not erase the need to account for cluster selection.

## Discrete groups versus continuous structure

Density clustering produces labels, but the scientific system may contain gradients, overlapping processes, or hierarchical continua. A label is a useful summary if it is stable and predictive for the intended use. It need not imply that nature contains a sharp boundary.

Evidence for continuity can appear as unstable border assignments, gradual original-space similarity, sensitivity to minimum cluster size, or persistent coarse groups with fragile leaves. Rather than forcing a binary verdict, report both discrete and continuous summaries where they illuminate different aspects of the data.

## Naming clusters

A biological name compresses an interpretation into a label and can become more memorable than the evidence. Names should begin descriptively—membership, modality enrichment, or an observed pattern—and advance to mechanistic language only with independent support.

“Cluster enriched for diffusion measures” states composition. “White-matter genetic mechanism” states an explanation. The second may be a hypothesis, but the label should not silently convert it into a fact.

## Noise as a scientific question

The reviewer record correctly treats noise observations as worthy of follow-up. The safe framing is that they were not assigned to a sufficiently persistent dense component under the fitted pipeline. Their meaning could include transitions, unique profiles, small groups, unstable associations, or technical effects. Whether they are biologically independent or non-pleiotropic is unresolved.

A useful analysis compares noise frequency and identity across seeds, parameter families, metrics, and independent data; examines original-space similarity; and avoids selecting a post hoc explanation solely because it fits a favored narrative.

## A claim ladder

The following ladder helps calibrate prose:

1. **Artifact claim:** the retained file assigns these identifiers to these labels.
2. **Structural claim:** the partition shows this internal or cross-run agreement under named metrics.
3. **Descriptive scientific claim:** these selected members show this pattern in the supplied data.
4. **Replicative claim:** a prespecified pattern appears in independent data.
5. **Mechanistic or causal claim:** an appropriate design supports a pathway or causal interpretation.

Evidence does not skip levels because a plot is compelling. A methods paper should make the highest supported rung clear and name the next required analysis.

## Reviewer-facing practice

When responding to a request for “validation,” identify the requested layer. If the request concerns software integrity, a manifest-backed rerun and comparison may suffice. If it concerns cluster stability, a perturbation analysis is needed. If it concerns biological relevance, independent or carefully designed downstream evidence is needed. If it concerns an alternative method, specify the matched estimand and benchmark.

Stage 1 found several reviewer-facing analyses still unperformed, including the quantitative external ABCD package and a fair comparator benchmark. The action register records requirements, not completed evidence.

## The decision created by this chapter

Treat discovered clusters as data-dependent summaries that can generate and organize hypotheses. Advance to confirmation through independent, split-sample, nested, or genuinely selection-aware designs. The next chapter applies this discipline to every DIMPLE-GWAS case currently in the evidence archive.

**Evidence trail.** Claims BIO-001, BIO-002, SLM-007, SLM-008, SLM-015 and SLM-020; gaps G-009 to G-012; sources [@kriegeskorte2009double; @gao2024selective].

## Questions for the reader

1. Give an example of a descriptive post-selection statement and its invalid confirmatory upgrade.
2. Why can an independent annotation still fail to provide independent confirmation if the analysis was chosen after inspecting it?
3. Place “exact label hash,” “replicated annotation pattern,” and “causal pathway” on the claim ladder.

\newpage
