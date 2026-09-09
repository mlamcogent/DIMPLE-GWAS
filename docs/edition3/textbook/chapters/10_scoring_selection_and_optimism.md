# Scoring and selecting models

A scalar score compresses several desirable properties into one ordering. That can make a large search usable. It can also conceal value judgments, unit dependence, edge cases, and selection-induced optimism. Freeze 3 preserves the historical `legacy_dimple` score for compatibility and exposes its components so that readers can see exactly what the number means.

## Eligible candidates

A candidate is eligible for the legacy score when its fit status is `success` and silhouette is available. The pipeline separately records failed fits and invalid topologies. An eligible candidate $i$ has silhouette $s_i$, number of clusters $c_i$, and number of noise points $n_i$.

For each active component, the implementation divides by the maximum among eligible candidates:

$$
\tilde s_i=\frac{s_i}{\max_j s_j},\qquad
\tilde c_i=\frac{c_i}{\max_j c_j},\qquad
\tilde n_i=\frac{n_i}{\max_j n_j}.
$$

If a component maximum is zero, its normalized values are set to zero. These are maximum normalizations, not min-max normalizations.

Next calculate raw ranges,

$$
r_s=\max s-\min s,\quad r_c=\max c-\min c,\quad r_n=\max n-\min n.
$$

When the total range is positive, component weights are

$$
w_s=\frac{r_s}{r_s+r_c+r_n},\qquad
w_c=\frac{r_c}{r_s+r_c+r_n},\qquad
w_n=\frac{r_n}{r_s+r_c+r_n}.
$$

The raw score is

$$
R_i=w_s\tilde s_i+w_c\tilde c_i-w_n\tilde n_i.
$$

Finally, raw scores are min-max rescaled:

$$
S_i=\frac{R_i-\min_j R_j}{\max_j R_j-\min_j R_j}.
$$

If the final range is zero, every eligible candidate receives score 1.

## The default noise rule

With `fit_include_noise=false`, which is the default, the score substitutes zero for the noise component and sets its weight to zero. Observed noise remains reported in the model table; it simply does not influence the legacy ranking. With `fit_include_noise=true`, the noise penalty becomes active and silhouette uses the declared noise-inclusive scope.

This is a substantive choice. Excluding noise avoids rewarding or punishing coverage through that component, while including it expresses a preference for fewer unassigned observations. Neither rule turns `-1` into biology.

## A hand-worked score

Consider three eligible candidates:

| Model | Silhouette $s$ | Clusters $c$ | Noise $n$ |
|---|---:|---:|---:|
| A | 0.50 | 4 | 20 |
| B | 0.60 | 6 | 40 |
| C | 0.55 | 5 | 10 |

If noise is excluded, $r_s=0.10$, $r_c=2$, and $r_n=0$. The realized weights are approximately $w_s=0.0476$ and $w_c=0.9524$. Cluster-count variation dominates because the historical formula compares raw ranges in native units. Candidate B is strongly favored even though its silhouette advantage is modest.

This is not a calculation error. It is a property of the compatibility formula. It shows why the manifest records realized ranges and weights and why a score should not be described as a universal measure of cluster quality.

## Table-relative meaning

Both normalizations and weights depend on the eligible candidate table. Add a candidate with an extreme cluster count and the maximum, range, weights, raw scores, and final scores can all change—even for previously unchanged models. Legacy scores from two different candidate populations are therefore not absolute quantities that can be compared without reconstructing both tables.

The fixed tutorial makes the edge case visible. With one eligible candidate, all ranges and the final score range are zero; active components receive fallback weights and the final score is 1. The correct interpretation is “only eligible candidate under this table-relative rule,” not “perfect clustering.”

## Custom scoring

Freeze 3 also supports a declared custom profile. Each named metric has a non-negative weight and a direction to maximize or minimize. Eligible values are min-max normalized; minimized metrics are inverted; weights are normalized to sum to one; the weighted result is finally rescaled to $[0,1]$. A constant metric contributes zero.

Custom scoring is more explicit, not automatically more valid. Weights still encode preferences, metrics still share selection data, and the candidate population still influences normalization. A biologically targeted weight set requires a prespecified rationale and independent evaluation.

## Ranking and ties

Freeze 3 ranks eligible rows by score descending, then raw score descending, then stable model ID ascending, using stable sorting. Sequential ranks are assigned even when numerical scores tie. A rank-one row is therefore the deterministic winner under these rules, not necessarily a uniquely better statistical model.

The selected historical 164-IDP solution makes this distinction concrete. The retained row was manually chosen at sorted position 16 rather than automatically selected as score rank one. Documentation that says “the score selected the five-cluster model” is false. The accurate statement is that the historical workflow manually selected that retained row; the decision rationale is not fully preserved.

## Pareto summaries and family views

A scalar score hides trade-offs. Freeze 3 therefore writes family summaries and a supplementary Pareto front. The current Pareto calculation maximizes silhouette and cluster count while minimizing noise fraction and largest-cluster fraction. A candidate is retained when no other successful candidate is at least as good on all four objectives and strictly better on one.

Pareto membership does not mean truth. The set changes when objectives or directions change, and “more clusters” is not universally desirable. Its value is to expose unresolved trade-offs that a scalar score collapses.

## Selection optimism

Selecting the best of many candidates using a noisy internal criterion makes that winner's observed performance optimistic [@cawley2010selection; @varma2006bias]. The problem grows when the search, score, and interpretation are revised after inspecting outcomes. Internal cross-validation or resampling can reduce some bias, but the final scientific claim still needs independent or selection-aware evaluation.

A responsible report therefore includes the candidate population, failure counts, score formula, realized weights, tie rule, sensitivity of near-top models, and any manual decision. It distinguishes “best under this search” from “stable across reasonable searches” and from “externally validated.”

## The decision created by this chapter

Use the legacy score as an auditable compatibility ranking, not an absolute validity scale. Use custom scoring only with declared objectives. Inspect families and trade-offs. Preserve manual choices. The next chapter asks what evidence can establish that a selected partition or representation is actually reproducible.

**Evidence trail.** Claims SCO-001 to SCO-004, SCI-164R, SLM-010 to SLM-012; coverage COV-011 to COV-013 and COV-024.

## Questions for the reader

1. In the three-candidate example, compute the realized weights when noise is included.
2. Why can an unchanged candidate receive a different legacy score after other candidates are added?
3. Write one sentence that reports a tied rank-one result without calling it uniquely correct.

\newpage
