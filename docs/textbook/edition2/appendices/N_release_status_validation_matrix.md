# Appendix N — Release-status and validation matrix

| Layer | Edition 2 evidence | Status |
| --- | --- | --- |
| Source identity | Package version and source/checksum inventory; Git metadata absent | pass with checksum fallback |
| Unit/integration tests | Fresh isolated run: 45 passed, five retained warnings | pass |
| Hand-worked implementation paths | Lab 0 preprocessing, RINT, silhouette, score, label comparison | pass |
| Fixed-fixture execution | One candidate, 24 vectors, three groups of eight, no candidate failure | pass, bounded |
| Bounded sensitivity | 32 candidates across four UMAP and eight HDBSCAN settings; all retained | pass, bounded |
| Reproduction/comparison | ARI/NMI/noise Jaccard/mapped membership 1; VI 0; Procrustes ~2.7e-31 | pass, same environment |
| Artifact validation | 24/24 checks | pass, bounded |
| Output atlas | 34/35 patterns freshly verified; opt-in coordinate associations not executed | pass with limitation |
| MNIST | Public engineering protocol only | bounded |
| Historical 164 IDPs | Counts and manual row-16 selection reconstructed | historical only |
| Fresh 164-IDP 1,000-seed run | Deferred until Docker by coordinator | pending |
| Docker/Linux/GCP/AWS | Not built or executed in this documentation task | pending |
| Statistical/biological/external validation | Not established by internal metrics/tutorials | pending external work |

No lower layer substitutes for a higher layer.
