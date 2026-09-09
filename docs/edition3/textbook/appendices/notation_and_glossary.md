# Appendix A - Notation and glossary

## Notation

- $v$: number of aligned original variables, usually variant rows.
- $p$: number of phenotype-associated vectors or IDPs; the objects clustered.
- $X\in\mathbb{R}^{v\times p}$: numeric input block before transpose.
- $Y=X^{\mathsf T}\in\mathbb{R}^{p\times v}$: prepared working matrix.
- $d$: dimensions in one UMAP/densMAP view.
- $r$: number of seeded views.
- $Z\in\mathbb{R}^{p\times rd}$: horizontally concatenated representation.
- $d(i,j)$: declared pairwise distance.
- $c_k(i)$: HDBSCAN core distance to the $k$th neighbor.
- $d_{\mathrm{mreach},k}(i,j)$: mutual-reachability distance.
- `-1`: HDBSCAN noise/unassigned label.

## Glossary

**Analysis level.** A distinct data population, method execution and evidence role whose counts must not be mixed with another level.

**Candidate.** One complete declared combination of representation and clustering parameters.

**Concatenated embedding.** Horizontal join of repeated seeded coordinate blocks; not alignment, averaging or consensus.

**DBCV.** Density-based clustering validation diagnostic; optional and not part of the legacy score.

**densMAP.** UMAP extension that adds a relative local-density preservation objective.

**EOM.** Excess-of-mass cluster extraction from the HDBSCAN condensed hierarchy.

**IDP.** Imaging-derived phenotype. In the pipeline it is represented by an aligned association-profile vector.

**Legacy DIMPLE score.** Table-relative compatibility score combining normalized silhouette and cluster count, optionally penalizing noise, with weights derived from raw component ranges.

**Noise.** HDBSCAN label `-1`: unassigned under the fitted representation and parameters.

**RINT.** Rank-based inverse normal transformation applied column-wise before transpose when enabled.

**Structural equivalence.** Agreement of partitions, noise sets, neighborhoods or coordinates under declared metrics, which need not imply byte equality or biological validity.

**UMAP family.** Candidate group sharing the same UMAP/densMAP representation settings and therefore able to reuse one concatenated embedding.

\newpage
