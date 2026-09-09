# Returning to the original summary-statistic space

An embedding is useful because it simplifies. Interpretation is dangerous for the same reason. Once a model is selected, the analyst should return to the original association-profile matrix and ask whether members assigned together actually show coherent patterns there.

Freeze 3's `explain` command performs this post hoc description without refitting or reranking. It loads either a native retained model or an adapted legacy label table, verifies identity and hashes where available, aligns vector identifiers with the original matrix, computes Pearson or Spearman similarity, orders observations within cluster blocks, writes summaries, and renders static and interactive heatmaps.

## Original-space similarity

For vectors $i$ and $j$, Pearson similarity is their centered correlation over the included variables. Spearman similarity is Pearson correlation of their ranks. Both are descriptive summaries of the supplied coordinates. They do not model LD, coordinate uncertainty, sample overlap, ancestry, or causal variants.

A cluster whose members have high within-block similarity in the original matrix has survived one useful sanity check: it is not only an artifact of the selected display coordinates. But the check is conditional on the same data used to construct and select the partition. It is not independent validation.

## Ordering is for reading, not refitting

A raw label order can scatter cluster members across a heatmap. Freeze 3 first keeps cluster blocks together, places noise according to the declared policy, and then uses hierarchical ordering within blocks. Cutpoints record the boundaries. This makes patterns visible without changing memberships.

For large analyses, the software can choose a block-preserving subset for display. The full similarity and analytical summaries remain distinct from the displayed subset. A sampled heatmap must never be described as though the excluded observations were absent from the analysis.

## What a heatmap can show

A heatmap can reveal internally coherent blocks, gradients within a cluster, heterogeneous clusters, relationships among noise observations, and discrepancies between embedding-based labels and original-space similarity. Annotations can help identify whether apparent structure follows modality, anatomical family, data source, or another known category.

These observations guide follow-up. They do not prove that a visual block has one mechanism. Color-scale limits, ordering, sampling, and annotation choices can create strong perceptual narratives. Captions should state the similarity metric, included observations, ordering, noise treatment, and evidence status.

## Coordinate associations

Freeze 3 can optionally compute descriptive associations between supplied coordinates and original variables. These may suggest which original dimensions vary with a displayed direction. They are especially easy to overread. A UMAP axis is not a stable latent loading, and the association is calculated after constructing and selecting the representation. Treat it as exploratory and verify any scientific conclusion independently.

The optional coordinate-association path was not freshly covered in Stage 1, and one related XLSX path was skipped because `openpyxl` was absent. Documentation should not imply broader execution than the retained evidence supports.

## Native artifacts and legacy adapters

A native explanation begins from a retained model summary and verifies the label hash and input identity. A legacy explanation adapts historical tables, detects or accepts orientation, aligns IDs, and writes exclusions only when incomplete matching is explicitly allowed. Exact matching is the default because silent dropping would change the result population.

The historical 164-IDP route achieved exact matching for all 164 IDs and preserved the five clusters and 102 noise assignments. That is an exact adaptation and descriptive explanation of retained labels. UMAP and HDBSCAN were not refitted, so “reproduced the historical clustering” is too broad.

## Reading noise in original space

Noise should be inspected rather than hidden. Some noise vectors may resemble a cluster weakly, form a gradient, or show a small dense group below the minimum cluster size. Others may be genuinely isolated under the selected geometry. Original-space similarity can distinguish these descriptive patterns, but biological interpretation still requires upstream and independent evidence.

Reporting only non-noise groups can bias the scientific story by treating coverage as invisible. At minimum report the count and fraction of noise, how it changes across plausible settings, and whether noise observations show recognizable original-space structure.

## An interpretation workflow

Begin with identity: exact IDs, input hash, label hash, and analysis level. Then inspect cluster and noise counts. Next read the full similarity summary and within-block ordering before viewing the heatmap. Compare original-space relationships with the selected partition and with alternative models. Record mismatches rather than explaining them away. Only then bring in annotations and domain hypotheses.

Finally, separate three sentences in the report:

1. **Observed:** which retained objects were assigned together and what descriptive original-space pattern they showed.
2. **Interpretation:** a plausible scientific explanation.
3. **Needed evidence:** the independent, perturbational, or selection-aware analysis required to support that explanation.

## Why the next chapter is about inference

Returning to original space makes selected groups easier to describe, which increases the temptation to test and name them as though they were prespecified. The next chapter explains the double-use problem and how a discovered topology can become a defensible biological claim.

**Evidence trail.** Claims INT-001 to INT-003, SCI-164, SLM-004, SLM-007, SLM-013 and SLM-016; coverage COV-016 to COV-018.

## Questions for the reader

1. Why is a high within-cluster Pearson similarity not independent validation?
2. List the caption details required for a sampled original-space heatmap.
3. Rewrite “Cluster 2 is the neurodevelopment pathway” into observation, hypothesis, and needed-evidence sentences.

\newpage
