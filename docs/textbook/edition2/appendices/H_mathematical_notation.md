# Appendix H — Mathematical notation

The main chapters derive the core expressions; this appendix provides a compact index.

| Concept | Notation or equation | Interpretation boundary |
| --- | --- | --- |
| GWAS-derived vector | `X in R^(p x v)` | A vector is a statistical summary, not a person or causal mechanism. |
| identifier alignment | `I_A = I_B` | Order is not identity; normalize and validate keys before joining. |
| distance and similarity | `d_2(x,y)=sqrt(sum_j (x_j-y_j)^2)` | The metric defines which differences count as close. |
| scaling and transformation | `z=(x-mu)/sigma; z_i=Phi^-1((r_i-0.5)/n)` | Transformation changes geometry; it does not create independent evidence. |
| RINT ties and missingness | `r_i=average tied rank` | Freeze 3 rejects missing analysis cells before the pipeline and applies RINT column-wise before transpose. |
| high-dimensional concentration | `contrast=(d_max-d_min)/d_min` | The phenomenon depends on distribution and norm; it is not a universal collapse theorem. |
| linear dimension reduction | `Z=XW` | PCA/ICA are comparators, not hidden Freeze 3 preprocessing. |
| nearest-neighbor graph | `N_k(i)` | Neighbor identity depends on metric, scale, k, and ties. |
| UMAP fuzzy membership | `w_ij=exp(-(d_ij-rho_i)/sigma_i)` | This is an educational form of delegated UMAP behavior, not reimplemented code. |
| UMAP cross-entropy | `C=sum_ij [w_ij log(w_ij/v_ij)+(1-w_ij)log((1-w_ij)/(1-v_ij))]` | Optimization is stochastic and coordinates are non-identifiable up to layout symmetries. |
| densMAP regularization | `L=L_UMAP+lambda L_density` | Density preservation trades against the base layout objective and does not make density biologically true. |
| seed schedule | `legacy: 1,...,S; current: r,...,r+S-1` | Recorded seeds permit replay but do not guarantee cross-platform bitwise identity. |
| concatenated geometry | `Y*=[Y^(1)|...|Y^(S)] in R^(p x Sq)` | Squared Euclidean distances add across runs, so unaligned rotations/scales influence the aggregate. |
| core distance | `core_k(x)` | Larger min_samples changes the density scale and may increase unassigned points. |
| mutual reachability | `d_mr(a,b)=max(core_k(a),core_k(b),d(a,b))` | It smooths single-linkage effects without removing parameter dependence. |
| HDBSCAN stability | `Stability(C)=sum_(x in C)(lambda_x-lambda_birth)` | The library computes the hierarchy; Freeze 3 records persistence summaries. |
| noise label | `label_i=-1` | Noise is algorithmic and parameter-conditional, never a biological-null statement. |
| Cartesian search | `N_candidates=product_j |Theta_j|` | The standard grid is 45 x 18 x 3 = 2,430 for one UMAP family. |
| candidate identity | `model_id=H(canonical parameters)` | Identity supports replay; it is not a quality score. |
| silhouette | `s(i)=(b(i)-a(i))/max(a(i),b(i))` | Freeze 3 can exclude noise and supplies the configured HDBSCAN metric. |
| Calinski-Harabasz | `CH=[tr(B)/(k-1)]/[tr(W)/(n-k)]` | The implementation uses non-noise embedded points and Euclidean centroid geometry. |
| Davies-Bouldin | `DB=(1/k)sum_i max_(j!=i)(S_i+S_j)/M_ij` | Lower is better; Euclidean centroid assumptions can mismatch density geometry. |
| DBCV | `weighted cluster validity in [-1,1]` | It is optional and supplementary under legacy_dimple, not the default score component. |
| trustworthiness and continuity | `T(k)=1-c sum_i sum_(j in U_k(i))(r(i,j)-k)` | Freeze 3 computes both through directed calls to sklearn trustworthiness under Euclidean geometry. |
| legacy_dimple score | `raw=w_s s/max(s)+w_k k/max(k)-w_n n/max(n)` | Weights are raw dynamic ranges divided by their sum; final scores are min-max scaled. |
| eligibility and ties | `eligible=(status=success) and finite silhouette` | Ties resolve deterministically through configured sort keys and candidate identity. |
| adjusted Rand index | `ARI=(RI-E[RI])/(max(RI)-E[RI])` | Permutation invariant; a value of 1 does not imply coordinate identity. |
| normalized mutual information | `NMI=2I(U;V)/(H(U)+H(V))` | Normalization conventions matter; Freeze 3 uses the sklearn convention recorded in code. |
| noise Jaccard | `J(A,B)=|A intersect B|/|A union B|` | It isolates agreement about unassigned membership, not all clusters. |
| Procrustes disparity | `min_R ||X_c R-Y_c||_F^2` | Low disparity supports aligned coordinate similarity under the chosen transformation, not biological replication. |
| Pearson association | `r=sum(x-xbar)(y-ybar)/sqrt(sum(x-xbar)^2 sum(y-ybar)^2)` | Post-selection descriptive only; undefined constant vectors follow configured policy. |
| Spearman association | `rho=cor(rank(x),rank(y))` | Ties receive average ranks; monotonic association is not mechanism. |
| circular analysis | `selection(Y) then test(Y) without adjustment` | Same-data heatmaps and correlations are descriptive; independent or selective-inference designs are needed for confirmatory claims. |
| validation ladder | `E_software != E_biological` | Passing tests or exact fixture replay cannot substitute for external biological validation. |
| floating-point reproducibility | `fl((a+b)+c) may differ from fl(a+(b+c))` | Pinned dependencies improve control but do not guarantee universal bitwise equality. |
