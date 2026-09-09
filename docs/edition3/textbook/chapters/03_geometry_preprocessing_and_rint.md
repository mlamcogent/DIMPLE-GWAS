# Geometry before algorithms: preprocessing, distance, and RINT

Analysts often ask which UMAP or HDBSCAN parameters they should use. That question arrives too late. Before either algorithm runs, preprocessing has already decided which differences are large, which orderings matter, and which observations can become neighbors.

## Preprocessing is a model of relevance

Let $\mathbf{y}_i\in\mathbb{R}^v$ and $\mathbf{y}_j\in\mathbb{R}^v$ be two phenotype vectors. Euclidean distance gives every coordinate the same squared-error role:

$$
d_E(i,j)=\left(\sum_{q=1}^{v}(y_{iq}-y_{jq})^2\right)^{1/2}.
$$

Manhattan distance uses absolute differences,

$$
d_1(i,j)=\sum_{q=1}^{v}|y_{iq}-y_{jq}|,
$$

and cosine distance focuses on direction,

$$
d_{\cos}(i,j)=1-\frac{\mathbf{y}_i^{\mathsf T}\mathbf{y}_j}{\|\mathbf{y}_i\|_2\|\mathbf{y}_j\|_2}.
$$

None is universally correct. Euclidean distance reacts strongly to large coordinate differences. Manhattan distance changes that influence pattern but remains scale-sensitive. Cosine distance discounts overall magnitude but can become unstable near zero. Correlation distance additionally removes location and scale within each vector. Each asks a different scientific question.

Freeze 3 exposes metrics through its UMAP and HDBSCAN configuration, but the metric contracts are not perfectly interchangeable. Silhouette follows the configured clustering metric and declared noise scope. Calinski-Harabasz and Davies-Bouldin are Euclidean, non-noise diagnostics in the current implementation. DBCV uses the configured clustering metric when enabled. Comparing metric values without disclosing geometry and scope is therefore invalid even when every number was computed correctly.

## A small scaling example

Consider three objects over two coordinates:

$$
A=(0,0),\qquad B=(1,1),\qquad C=(2,100).
$$

Without scaling, $d_E(A,B)=\sqrt{2}$ while $d_E(B,C)\approx99.005$. The second coordinate dominates. Standardizing the coordinates over this three-point sample would reduce that domination, but it would also define “one unit” using this particular sample. If the large second-coordinate range carries genuine scientific meaning, standardization can erase it. If it is a unit artifact, failing to standardize can create spurious neighborhoods.

DIMPLE-GWAS does not insert a generic z-score standardization stage before UMAP. The analyst should not assume that every conventional preprocessing step occurs simply because it is common elsewhere. The resolved configuration and implementation path are the authority.

## Rank inverse normal transformation

Freeze 3 optionally applies a rank-based inverse normal transformation column by column in the original variants-by-vector table. For a column with $n$ non-missing values, tied observations receive average ranks $r_j$, which are mapped to

$$
z_j=\Phi^{-1}\left(\frac{r_j-0.5}{n}\right),
$$

where $\Phi^{-1}$ is the standard normal quantile function. The transform preserves rank order but changes spacings and marginal interpretation.

Take the values $(2,2,5,9)$. Their average ranks are $(1.5,1.5,3,4)$. With $n=4$, the plotting positions are $(0.25,0.25,0.625,0.875)$, giving approximate transformed values $(-0.674,-0.674,0.319,1.150)$. The two tied values remain tied. The original gaps $(0,3,4)$ become new normal-quantile gaps determined by order rather than magnitude.

This can reduce the influence of heavy marginal tails and place columns on a common rank-normal scale. It can also remove meaningful magnitude information and alter distances substantially. RINT is therefore a sensitivity choice, not a correction that automatically improves every dataset [@beasley2009rint]. It does not impute missing data, fix allele orientation, model LD, correct overlap, or remove ancestry and imaging confounds.

The implementation rejects all-missing columns and remaining missing or non-numeric values. This is scientifically preferable to silently inventing coordinates, but it means the analyst must decide whether a missingness problem should be solved upstream, by feature exclusion, or through a separately justified model.

## Metric choice and neighbor graphs

UMAP begins with nearest-neighbor relations. A small change in distance can change the $k$th neighbor, which changes the local graph, which changes the embedding, which changes the density landscape seen by HDBSCAN. This cascading dependence is why metric sensitivity is not a cosmetic robustness plot.

Suppose point $A$ has candidate neighbors $B$ and $C$. Under Euclidean distance, $B$ may be closer because their magnitudes match. Under cosine distance, $C$ may be closer because the vectors point in a similar direction. There is no algorithmic contradiction. The methods are preserving different relationships.

In high dimensions, one should ask at least three questions. Is the nearest-neighbor graph stable under plausible transformations? Are a small number of hubs dominating many neighbor lists? Do resulting partitions change structurally, including noise status, under the alternative? The appropriate response to disagreement is to report dependence, not to select the graph that looks most biologically appealing after seeing the labels.

## Separate preprocessing sensitivity from selection

A common design error is to include many preprocessing choices in one giant candidate search and then select the best internal score as if all candidates estimated the same object. They do not. A metric or transformation can redefine the geometry itself, whereas an HDBSCAN parameter changes a density interpretation within a geometry.

A clearer analysis has nested questions:

1. Define a small set of scientifically defensible preprocessing/metric families.
2. Inspect neighborhood properties within each family.
3. Search clustering parameters without mixing incompatible score meanings.
4. Compare the selected partitions structurally across families.
5. Treat family disagreement as part of uncertainty.

Freeze 3 can enumerate candidate parameters and compare retained partitions, but Stage 1 did not execute a complete real-data design of this kind. Edition 3 therefore teaches it as a validation strategy rather than a completed result.

## What to inspect in a run

The resolved configuration is the only reliable record of whether RINT, densMAP, a metric, or a particular parameter value was active after built-in defaults, YAML settings, and explicit command-line overrides were merged. The input contract in the run manifest records the prepared orientation and shape. Candidate tables record metric names and diagnostic scopes. A report should carry those fields into any comparison of scores or plots.

In the fixed Stage 1 run, the prepared shape was 24 by 80, RINT was not invoked by the retained tutorial configuration, UMAP and HDBSCAN used Euclidean distance, and one candidate was fitted. Those facts belong to the fixture. They should not be silently upgraded to recommendations for manuscript-scale IDP analysis.

## Why the next chapter compares representations

After the geometry is declared, we still need a representation strategy. Linear decompositions, metric-preserving maps, neighborhood embeddings, and multivariate genetic models retain different aspects of the data. Understanding those differences prevents a false contest in which “nonlinear” is treated as synonymous with “better.”

**Evidence trail.** Claims PRE-001 to PRE-003, MET-001 to MET-004, SLM-009, SLM-014 and SLM-024; coverage COV-002, COV-003, COV-009 and COV-010.

## Questions for the reader

1. Recompute the RINT example and explain what information is preserved and lost.
2. Why can Calinski-Harabasz and a non-Euclidean silhouette be inappropriate to compare as if they used the same geometry?
3. Sketch a sensitivity design that keeps preprocessing-family uncertainty separate from within-family HDBSCAN tuning.

\newpage
