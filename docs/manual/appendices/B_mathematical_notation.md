# Appendix B — Mathematical notation and equations

Let the prepared analysis matrix be \(X \in \mathbb{R}^{p \times v}\), with \(p\) vectors/IDPs and \(v\) input variables/variants after the declared metadata prefix is removed and the table is transposed. For repeated embeddings \(U_s \in \mathbb{R}^{p \times d}\), the HDBSCAN input is the horizontal concatenation \(Z=[U_1|\cdots|U_R] \in \mathbb{R}^{p \times dR}\). This is an implementation identity, not a theorem about true topology.

For an observation \(i\), silhouette is \(s(i)=(b(i)-a(i))/\max\{a(i),b(i)\}\), where \(a(i)\) is its mean within-cluster distance and \(b(i)\) is the smallest mean distance to another cluster under the configured metric. Freeze 3 summarizes eligible non-noise observations.

For each legacy-score component \(x\), Freeze 3 computes \(x'=x/\max(x)\) over the eligible candidate population. Component weights are their observed raw dynamic ranges divided by the sum of included ranges. The raw score is

\[S_{raw}=w_s s' + w_c c' - w_n n'.\]

Here \(s\) is silhouette, \(c\) is non-noise cluster count, and \(n\) is noise count. When `fit_include_noise=false`, \(w_n=0\). The final score rescales \(S_{raw}\) to [0,1] over the same candidate population; a zero range maps to 1. DBCV is not a term in this formula.

ARI and NMI compare partitions invariant to numeric label permutation. Noise-set Jaccard is \(|N_A \cap N_B|/|N_A \cup N_B|\), with the implementation-defined convention for two empty noise sets. These are concordance diagnostics, not tests of biological validity.
