# Chapter dependency map

An arrow means ‘read or understand before’. The quickstart route is deliberately short.

```mermaid
flowchart LR
  C1["1: scope"] --> C3["3: RC1 boundary"]
  C3 --> C4["4: workflow"]
  C4 --> C9["9: setup"]
  C9 --> C10["10: data"]
  C10 --> C11["11: config"]
  C11 --> C12["12: inspect"]
  C12 --> C13["13: run"]
  C13 --> C14["14: verify"]
  C14 --> C15["15: preprocessing"]
  C15 --> C16["16: UMAP"]
  C16 --> C17["17: repeats"]
  C17 --> C18["18: HDBSCAN"]
  C18 --> C19["19: metrics"]
  C19 --> C20["20: score"]
  C20 --> C21["21: select"]
  C21 --> C22["22: reproduce"]
  C22 --> C23["23: compare/validate"]
  C23 --> C25["25: original space"]
  C25 --> C29["29: circularity"]
  C29 --> C30["30: validation"]
```

## Per-chapter prerequisites

- Chapter 1: `none` → **What DIMPLE-GWAS is and is not**
- Chapter 2: `1` → **The scientific problem: structure among genetically informed phenotype vectors**
- Chapter 3: `1` → **Stage 1 scope and the Freeze 3 RC1 status boundary**
- Chapter 4: `1-3` → **From input matrix to candidate partitions**
- Chapter 5: `2` → **Essential GWAS, vector-space, distance, and clustering concepts**
- Chapter 6: `4-5` → **Why repeated nonlinear embeddings and density clustering are used**
- Chapter 7: `5-6` → **Choosing among complementary methods**
- Chapter 8: `1-7` → **Scientific interpretation, circularity, and validation boundaries**
- Chapter 9: `basic shell` → **System requirements and isolated environment setup**
- Chapter 10: `2, 9` → **Input data contract, orientation, metadata columns, and missingness**
- Chapter 11: `9-10` → **Configuration files and precedence**
- Chapter 12: `11` → **Inspecting a configuration and enumerating the search space**
- Chapter 13: `9-12` → **Fixed synthetic quickstart**
- Chapter 14: `13` → **Reading the run manifest**
- Chapter 15: `10-11` → **Preprocessing and optional RINT**
- Chapter 16: `5-6, 15` → **UMAP and densMAP fundamentals**
- Chapter 17: `16` → **Repeated seeds, concatenated embeddings, determinism, and compute cost**
- Chapter 18: `5, 17` → **HDBSCAN concepts and the Freeze 3 search grid**
- Chapter 19: `18` → **Candidate-model metrics**
- Chapter 20: `19` → **The legacy_dimple score and optional alternatives**
- Chapter 21: `18-20` → **Ranking, summarising, and choosing a model**
- Chapter 22: `13-14, 21` → **Reproducing a selected model**
- Chapter 23: `22` → **Comparing partitions and validating outputs**
- Chapter 24: `16-17` → **Why UMAP coordinates are not biological loadings**
- Chapter 25: `10, 23-24` → **Returning to the original input-vector space**
- Chapter 26: `25` → **Pearson and Spearman association summaries**
- Chapter 27: `25-26` → **Cluster heatmaps, ordering, annotations, and cutpoints**
- Chapter 28: `18, 25` → **Noise assignments and uncertainty**
- Chapter 29: `8, 25-28` → **Avoiding double dipping and post-selection overclaiming**
- Chapter 30: `8, 23, 29` → **Technical, statistical, and biological validation**
- Chapter 31: `1-30` → **Reporting a DIMPLE-GWAS analysis**
- Chapter 32: `13-14` → **Fixed synthetic dataset case study**
- Chapter 33: `18-21, 32` → **Custom bounded search-space case study**
- Chapter 34: `22-30` → **Explanation, comparison, and validation case study**
- Chapter 35: `4-8` → **MNIST as a software benchmark**
- Chapter 36: `1-31` → **Original 164-IDP analysis**
- Chapter 37: `9-14` → **Complete command reference**
- Chapter 38: `11` → **Complete configuration reference**
- Chapter 39: `12, 18` → **Search-space reference**
- Chapter 40: `19-21` → **Scoring and model-selection reference**
- Chapter 41: `14, 23, 25` → **Output atlas and data dictionary**
- Chapter 42: `14, 17, 23` → **Provenance and reproducibility checklist**
- Chapter 43: `9-23` → **Error messages, troubleshooting, and recovery**
- Chapter 44: `12, 17-18` → **Performance, memory, threading, and bounded-run guidance**
- Chapter 45: `14, 37-42` → **Migration from Dev and Freeze 2**
- Chapter 46: `all` → **Known issues and scientific limitations**
