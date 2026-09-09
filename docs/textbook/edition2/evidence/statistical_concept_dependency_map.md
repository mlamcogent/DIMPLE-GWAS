# Statistical concept dependency map

This map fixes the prerequisite order used by Edition 2. Arrows mean “must be understood before,” not causal influence.

```mermaid
flowchart TD
  vectors[GWAS-derived vectors and identifiers] --> geometry[distance, similarity, scaling]
  geometry --> transform[RINT and orientation]
  geometry --> graph[nearest-neighbor graph]
  graph --> umap[UMAP fuzzy graph and objective]
  umap --> dens[densMAP regularization]
  umap --> repeats[seeded repeats and concatenation]
  repeats --> density[core distance and mutual reachability]
  density --> hierarchy[HDBSCAN hierarchy, stability, and noise]
  hierarchy --> diagnostics[candidate diagnostics]
  diagnostics --> score[legacy_dimple and ranking]
  score --> replay[selected-model replay]
  replay --> compare[ARI, NMI, noise Jaccard, Procrustes]
  replay --> explain[original-space Pearson/Spearman explanation]
  compare --> ladder[validation ladder]
  explain --> circular[circularity safeguards]
  circular --> ladder
```

The complete equation, implementation, output, evidence, and chapter mapping is in `statistical_concept_coverage.tsv`. All Tier A analytical routes have prerequisite concepts. Concepts delegated to third-party libraries are labeled as delegated behavior rather than DIMPLE-GWAS reimplementations.
