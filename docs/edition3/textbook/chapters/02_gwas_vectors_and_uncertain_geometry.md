# GWAS summary statistics as high-dimensional trait vectors

The attractive simplification behind DIMPLE-GWAS is that every phenotype can be represented by a point. The dangerous simplification is forgetting what had to be true for those points to be comparable.

Suppose the input table has $v$ variant rows, $m$ metadata columns, and $p$ analysis columns. Before preprocessing, write the numeric block as $X\in\mathbb{R}^{v\times p}$. Entry $x_{ji}$ is the association quantity for variant $j$ and phenotype $i$. After metadata removal and transposition, phenotype $i$ becomes row $\mathbf{y}_i=(x_{1i},\ldots,x_{vi})$ of $Y=X^{\mathsf T}$.

![DIMPLE-GWAS removes the declared metadata prefix, validates the numeric block, optionally transforms columns, and transposes it so phenotype-associated vectors become the rows being represented and clustered.](assets/figures/matrix_orientation.png){#fig-orientation width=92%}

The algebra is simple. The scientific contract is not.

## Aligned coordinates are a prerequisite

A coordinate-by-coordinate distance assumes that row $j$ refers to a comparable quantity in every analysis column. Variant identifiers, alleles, strand orientation, genome build, imputation and quality thresholds, and the sign convention must be aligned upstream. A sign reversal in one phenotype does not look like a small clerical error in Euclidean space; it can rotate the entire association profile away from otherwise similar vectors.

DIMPLE-GWAS does not perform allele harmonization, LD pruning, genomic control, study-overlap correction, ancestry adjustment, or imaging-confound correction. Those operations require information and estimands outside the clustering package. Summary-statistic QC guidance and LD-score methods demonstrate why inflation, overlap, and covariance cannot be inferred from a bare numeric matrix [@winkler2014qc; @buliksullivan2015ldsc; @buliksullivan2015rg].

The pipeline's input validation should therefore be viewed as a *software contract*, not a GWAS-validity certificate. It can establish that the analysis block is present, numeric, finite under the declared rules, and oriented as expected. It cannot establish that the numbers were scientifically commensurate before arrival.

## Scale defines what “near” means

If one phenotype column contains effect sizes and another contains $Z$-scores, equal numeric differences do not have equal meaning. Even when every column uses the same nominal statistic, unequal sample sizes and standard errors can change scale and noise. A large coordinate can reflect a strong association, a small standard error, population structure, LD, or another feature of the upstream study.

Consider three variants and two phenotype vectors:

$$
\mathbf{y}_A=(0.8,0.1,-0.6),\qquad
\mathbf{y}_B=(-0.2,0.4,-0.5).
$$

Their Euclidean distance is

$$
d_E(A,B)=\sqrt{(0.8+0.2)^2+(0.1-0.4)^2+(-0.6+0.5)^2}
=\sqrt{1.10}\approx1.049.
$$

The number is exact for the supplied coordinates. It is not automatically an exact measure of genetic dissimilarity. If the first coordinate is much less precise, in high LD with many nearby coordinates, or allele-misaligned for one phenotype, the scientific meaning changes while the arithmetic does not.

This motivates weighted or covariance-aware distances in some applications, but Freeze 3 does not silently implement such a model. The correct documentation stance is explicit: the package treats the prepared numeric coordinates as its geometry. Analysts who require uncertainty or covariance modelling must design and validate that upstream or extend the method transparently.

## Correlation is another geometry, not a causal shortcut

Two profiles can be similar because their signed patterns rise and fall together even if their magnitudes differ. Pearson correlation between centered vectors can capture this pattern similarity:

$$
r_{AB}=\frac{\sum_j(y_{Aj}-\bar y_A)(y_{Bj}-\bar y_B)}
{\sqrt{\sum_j(y_{Aj}-\bar y_A)^2}\sqrt{\sum_j(y_{Bj}-\bar y_B)^2}}.
$$

Spearman correlation applies the same idea to ranks. Freeze 3 uses Pearson or Spearman similarity in its *post hoc original-space explanation* route, not as proof of shared causal variants or formal genetic correlation. The distinction matters. LD-score regression estimates a different object under an explicit model [@buliksullivan2015rg]. A high profile correlation can be informative as a descriptive diagnostic while remaining compatible with LD, sample overlap, scale, confounding, or phenotype-construction explanations.

## High dimension changes intuition

When $v$ is very large, distances can become difficult to discriminate. For some distributions, the relative contrast between the nearest and farthest points decreases as dimension grows [@aggarwal2001distance]. Neighborhood lists can also develop *hubs*: observations that appear unusually often among other observations' nearest neighbors [@radovanovic2010hubness].

Neither phenomenon says that high-dimensional data are unusable or that a “true topology” will reveal itself if one chooses the right nonlinear plot. They say that the chosen metric, scaling, feature set, and neighborhood size become part of the scientific analysis. A responsible workflow asks whether neighbor relations survive plausible perturbations.

One useful diagnostic is to compare $k$-nearest-neighbor sets under alternative preprocessing or metrics. For object $i$, let $N_k^{(a)}(i)$ and $N_k^{(b)}(i)$ be the neighbor sets under two choices. Their Jaccard agreement is

$$
J_i=\frac{|N_k^{(a)}(i)\cap N_k^{(b)}(i)|}{|N_k^{(a)}(i)\cup N_k^{(b)}(i)|}.
$$

A low average $J_i$ is not a software error; it is evidence that the local geometry is choice-sensitive. Freeze 3 reports trustworthiness and continuity for original-to-embedded neighborhoods, but Stage 1 did not complete a real-data metric or feature-set stability study.

## The observational unit can carry correlated error

Each row of $Y$ is treated as an object, but the coordinate noise within and between rows may be correlated. Shared participants across GWAS, overlapping covariates, common preprocessing, related phenotypes, and LD across variants violate a naive view of independent coordinates. This does not invalidate exploratory geometry by definition. It limits the estimand: the observed profile space includes biological and technical covariance unless explicitly separated.

For imaging-derived phenotypes, upstream image processing and confound control also shape the association vectors. Large IDP GWAS demonstrate how phenotype definition, imaging quality, population structure, and genetic QC interact [@elliott2018idp]. Cross-ancestry transfer is not automatic [@martin2019portability]. A cluster may therefore be a useful map of the supplied statistical summaries while remaining agnostic about why the summaries cohere.

## What the software enforces

The current preprocessing path drops a configured metadata prefix, requires the remaining columns to be numeric under its coercion rules, optionally applies column-wise rank inverse normal transformation, rejects unresolved missing or non-numeric values, transposes to vectors by variables, and converts the working array for downstream computation. No linear reducer is inserted. Identifiers are carried forward so that retained labels can be joined and validated exactly.

This contract prevents several mechanical failures: treating metadata as features, clustering variant rows by accident, silently keeping strings, or losing phenotype identifiers. It cannot detect a plausible-looking but scientifically misaligned numeric matrix. That responsibility is shared between upstream provenance and analyst review.

## A preflight argument, not just a checklist

Before fitting, an analyst should be able to defend four sentences:

1. Every analysis column refers to a phenotype-associated vector measured over the same ordered coordinates.
2. The sign, scale, and missingness conventions are comparable or their differences are an intentional part of the geometry.
3. Upstream QC and overlap decisions are documented outside DIMPLE-GWAS.
4. The metadata prefix and identifiers make the post-transpose unit unambiguous.

If any sentence is false, a beautiful embedding will not repair it. The next chapter therefore treats preprocessing and metric choice as scientific modelling decisions rather than a routine prelude.

**Evidence trail.** Claims PRE-001 to PRE-003, UMA-001, BIO-001, SLM-004, SLM-013, SLM-014 and SLM-024; implementation coverage COV-002, COV-003 and COV-009.

## Questions for the reader

1. Give two upstream errors that the numeric input contract cannot detect.
2. Explain why a Euclidean distance can be computationally correct but scientifically misleading.
3. What extra design would be needed before calling original-space correlation evidence of a shared genetic mechanism?

\newpage
