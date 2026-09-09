# Appendix G — Release-status and validation matrix

| Layer | Current evidence | Status |
| --- | --- | --- |
| Software | 45 tests pass in the isolated macOS environment | pass |
| Fixed-fixture technical rerun | ARI, NMI, noise Jaccard, and mapped membership are 1; Procrustes is near zero | pass, bounded |
| Artifact validation | 24/24 checks pass for Tutorial 1 v2 | pass, bounded |
| Historical 164-IDP reconstruction | Exact recorded counts, manual row-16 selection, historical adaptation/rescoring | historical only |
| Fresh 164-IDP 1,000-seed search | Not executed in this build | pending Docker phase |
| Statistical/biological validation | Not established by internal metrics or tutorials | pending external work |
| Docker/Linux/GCP/AWS | Not built or tested | pending |

No lower layer substitutes for a higher layer.
