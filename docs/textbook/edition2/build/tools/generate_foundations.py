#!/usr/bin/env python3
"""Generate TE2 concept, claim, literature, and curriculum planning artifacts."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


EDITION2 = Path(__file__).resolve().parents[2]
FREEZE3 = EDITION2.parents[2]
EVIDENCE = EDITION2 / "evidence"
REFERENCES = EDITION2 / "references"
QA = EDITION2 / "qa"


def write_tsv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


concepts = [
    ("C01", "GWAS-derived vector", "effect estimates or association statistics for one phenotype across matched variants", "X in R^(p x v)", "A vector is a statistical summary, not a person or causal mechanism.", "prepare_analysis_matrix", "input matrix", "2,6", "elliott2018; buliksullivan2015"),
    ("C02", "identifier alignment", "a one-to-one correspondence between vector or feature identifiers across artifacts", "I_A = I_B", "Order is not identity; normalize and validate keys before joining.", "validated_identifiers; align_rows", "labels.tsv; coordinates.tsv", "3,6,16,17", "internal-code"),
    ("C03", "distance and similarity", "geometry chosen to compare vectors or embedded points", "d_2(x,y)=sqrt(sum_j (x_j-y_j)^2)", "The metric defines which differences count as close.", "evaluate_candidate; compute_similarity", "model_table.csv; similarity_matrix.csv", "3,5,11,17", "aggarwal2001"),
    ("C04", "scaling and transformation", "changes to marginal scale before geometric analysis", "z=(x-mu)/sigma; z_i=Phi^-1((r_i-0.5)/n)", "Transformation changes geometry; it does not create independent evidence.", "rank_inverse_normal_transform; prepare_analysis_matrix", "resolved_config.yaml", "3,6", "beasley2009"),
    ("C05", "RINT ties and missingness", "average ranks with missing values retained during ranking", "r_i=average tied rank", "Freeze 3 rejects missing analysis cells before the pipeline and applies RINT column-wise before transpose.", "rank_inverse_normal_transform", "prepared matrix", "6,18", "beasley2009; internal-code"),
    ("C06", "high-dimensional concentration", "relative contrast among common distances can weaken as dimension grows", "contrast=(d_max-d_min)/d_min", "The phenomenon depends on distribution and norm; it is not a universal collapse theorem.", "run_repeated_umap", "embedding.npy", "2,3,4", "aggarwal2001"),
    ("C07", "linear dimension reduction", "projection onto directions satisfying a linear objective", "Z=XW", "PCA/ICA are comparators, not hidden Freeze 3 preprocessing.", "not implemented", "none", "4,24", "oblong2024"),
    ("C08", "nearest-neighbor graph", "local graph connecting points under an input-space metric", "N_k(i)", "Neighbor identity depends on metric, scale, k, and ties.", "_fit_one (umap-learn delegate)", "embedding_manifest.json", "7", "mcinnes2018umap"),
    ("C09", "UMAP fuzzy membership", "locally calibrated edge strength in a fuzzy graph", "w_ij=exp(-(d_ij-rho_i)/sigma_i)", "This is an educational form of delegated UMAP behavior, not reimplemented code.", "_fit_one", "embedding.npy", "7", "mcinnes2018umap; umapdocs"),
    ("C10", "UMAP cross-entropy", "low-dimensional layout objective balancing represented and absent fuzzy edges", "C=sum_ij [w_ij log(w_ij/v_ij)+(1-w_ij)log((1-w_ij)/(1-v_ij))]", "Optimization is stochastic and coordinates are non-identifiable up to layout symmetries.", "_fit_one", "visualization_embedding.tsv", "7,8", "mcinnes2018umap"),
    ("C11", "densMAP regularization", "additional objective encouraging agreement of local density radii", "L=L_UMAP+lambda L_density", "Density preservation trades against the base layout objective and does not make density biologically true.", "_fit_one", "embedding_manifest.json", "7", "narayan2021densmap"),
    ("C12", "seed schedule", "deterministic list controlling repeated stochastic fits", "legacy: 1,...,S; current: r,...,r+S-1", "Recorded seeds permit replay but do not guarantee cross-platform bitwise identity.", "ensemble_seeds", "embedding_manifest.json", "8,12,23", "internal-code; reproduciblesum2015"),
    ("C13", "concatenated geometry", "horizontal concatenation of S embeddings with q components", "Y*=[Y^(1)|...|Y^(S)] in R^(p x Sq)", "Squared Euclidean distances add across runs, so unaligned rotations/scales influence the aggregate.", "run_repeated_umap", "embedding.npy", "8", "internal-code"),
    ("C14", "core distance", "distance from a point to its min_samples-th neighbor", "core_k(x)", "Larger min_samples changes the density scale and may increase unassigned points.", "fit_hdbscan (hdbscan delegate)", "candidate labels", "9", "campello2015hdbscan"),
    ("C15", "mutual reachability", "density-aware dissimilarity used by HDBSCAN", "d_mr(a,b)=max(core_k(a),core_k(b),d(a,b))", "It smooths single-linkage effects without removing parameter dependence.", "fit_hdbscan", "condensed tree state", "9", "campello2015hdbscan"),
    ("C16", "HDBSCAN stability", "persistence of a cluster through the density hierarchy", "Stability(C)=sum_(x in C)(lambda_x-lambda_birth)", "The library computes the hierarchy; Freeze 3 records persistence summaries.", "fit_hdbscan; evaluate_candidate", "model_table.csv", "9,11", "campello2015hdbscan; mcinnes2017hdbscan"),
    ("C17", "noise label", "label -1 for points unassigned under a fitted density model", "label_i=-1", "Noise is algorithmic and parameter-conditional, never a biological-null statement.", "fit_hdbscan", "labels.tsv", "9,17", "campello2015hdbscan"),
    ("C18", "Cartesian search", "product of enumerated parameter families", "N_candidates=product_j |Theta_j|", "The standard grid is 45 x 18 x 3 = 2,430 for one UMAP family.", "enumerate_candidates", "search_space.tsv", "10,14,20", "internal-code"),
    ("C19", "candidate identity", "deterministic hash and ordinal for a resolved parameter combination", "model_id=H(canonical parameters)", "Identity supports replay; it is not a quality score.", "candidate_identity", "search_space.tsv; model_table.csv", "10,12", "internal-code"),
    ("C20", "silhouette", "within-versus-nearest-other-cluster separation under a configured metric", "s(i)=(b(i)-a(i))/max(a(i),b(i))", "Freeze 3 can exclude noise and supplies the configured HDBSCAN metric.", "evaluate_candidate", "model_table.csv", "5,11,18", "rousseeuw1987"),
    ("C21", "Calinski-Harabasz", "between-cluster to within-cluster dispersion ratio", "CH=[tr(B)/(k-1)]/[tr(W)/(n-k)]", "The implementation uses non-noise embedded points and Euclidean centroid geometry.", "evaluate_candidate", "model_table.csv", "11", "calinski1974"),
    ("C22", "Davies-Bouldin", "average worst within/between centroid scatter ratio", "DB=(1/k)sum_i max_(j!=i)(S_i+S_j)/M_ij", "Lower is better; Euclidean centroid assumptions can mismatch density geometry.", "evaluate_candidate", "model_table.csv", "11", "davies1979"),
    ("C23", "DBCV", "density-based validity index", "weighted cluster validity in [-1,1]", "It is optional and supplementary under legacy_dimple, not the default score component.", "evaluate_candidate", "model_table.csv", "11", "moulavi2014dbcv"),
    ("C24", "trustworthiness and continuity", "directed neighborhood-retention diagnostics", "T(k)=1-c sum_i sum_(j in U_k(i))(r(i,j)-k)", "Freeze 3 computes both through directed calls to sklearn trustworthiness under Euclidean geometry.", "embedding_quality_metrics", "run_summary.json", "7,11,17", "venna2010"),
    ("C25", "legacy_dimple score", "population-relative weighted combination of normalized silhouette, clusters, and optionally noise", "raw=w_s s/max(s)+w_k k/max(k)-w_n n/max(n)", "Weights are raw dynamic ranges divided by their sum; final scores are min-max scaled.", "legacy_dimple_score", "scoring_manifest.json; model_table.csv", "11,18", "internal-code"),
    ("C26", "eligibility and ties", "rules deciding which candidates receive scores and stable rank order", "eligible=(status=success) and finite silhouette", "Ties resolve deterministically through configured sort keys and candidate identity.", "rank_models", "ranked_models.csv", "11,16", "internal-code"),
    ("C27", "adjusted Rand index", "chance-adjusted pairwise partition agreement", "ARI=(RI-E[RI])/(max(RI)-E[RI])", "Permutation invariant; a value of 1 does not imply coordinate identity.", "compare_partitions", "comparison_summary.json", "12,16,18", "hubert1985"),
    ("C28", "normalized mutual information", "normalized information shared by two labelings", "NMI=2I(U;V)/(H(U)+H(V))", "Normalization conventions matter; Freeze 3 uses the sklearn convention recorded in code.", "compare_partitions", "comparison_summary.json", "12,16", "vinh2010"),
    ("C29", "noise Jaccard", "overlap of the two sets labeled -1", "J(A,B)=|A intersect B|/|A union B|", "It isolates agreement about unassigned membership, not all clusters.", "noise_jaccard", "comparison_summary.json", "12,16", "internal-code"),
    ("C30", "Procrustes disparity", "residual after centering, scaling, and orthogonal alignment", "min_R ||X_c R-Y_c||_F^2", "Low disparity supports aligned coordinate similarity under the chosen transformation, not biological replication.", "compare_coordinates", "comparison_summary.json", "12,16", "gower1975"),
    ("C31", "Pearson association", "linear association in original input dimensions", "r=sum(x-xbar)(y-ybar)/sqrt(sum(x-xbar)^2 sum(y-ybar)^2)", "Post-selection descriptive only; undefined constant vectors follow configured policy.", "compute_similarity", "similarity_matrix.csv", "17,21", "kriegeskorte2009"),
    ("C32", "Spearman association", "Pearson correlation of marginal ranks", "rho=cor(rank(x),rank(y))", "Ties receive average ranks; monotonic association is not mechanism.", "compute_similarity", "similarity_matrix.csv", "17,21", "internal-code"),
    ("C33", "circular analysis", "reuse of discovery data for apparently confirmatory inference", "selection(Y) then test(Y) without adjustment", "Same-data heatmaps and correlations are descriptive; independent or selective-inference designs are needed for confirmatory claims.", "run_explanation", "explanation outputs", "5,17,23", "kriegeskorte2009; gao2024"),
    ("C34", "validation ladder", "separate software, technical, structural, statistical, biological, external, and cross-platform evidence", "E_software != E_biological", "Passing tests or exact fixture replay cannot substitute for external biological validation.", "run_validation", "validation_report.json", "1,12,23,24", "internal-evidence"),
    ("C35", "floating-point reproducibility", "dependence of finite-precision results on operation order and platform", "fl((a+b)+c) may differ from fl(a+(b+c))", "Pinned dependencies improve control but do not guarantee universal bitwise equality.", "capture_environment", "environment.json", "12,23,24", "reproduciblesum2015"),
]


chapters = [
    (1,"The scientific problem, scope, and evidence boundary","I",3200,"none","Define Stage 1 units; separate discovery from validation; locate evidence status","cli.main; run_search","run_manifest.json"),
    (2,"GWAS-derived phenotype vectors and high-dimensional geometry","I",3800,"1","Construct vector notation; explain LD/sample-overlap cautions; interpret distances","prepare_analysis_matrix","input matrix"),
    (3,"Similarity, distance, scaling, transformation, and uncertainty","I",3800,"2","Compare metrics; reason about scaling; distinguish sensitivity from proof","rank_inverse_normal_transform; compute_similarity","prepared matrix; similarity_matrix.csv"),
    (4,"Dimension reduction: linear and nonlinear perspectives","I",3200,"2-3","Contrast objectives; explain neighborhood preservation; locate non-identifiability","_fit_one","embedding.npy"),
    (5,"Density clustering, validation, and circular inference","I",3600,"3-4","Explain density partitions; classify validation; identify double dipping","fit_hdbscan; evaluate_candidate","labels.tsv; model_table.csv"),
    (6,"Data contract, preprocessing, RINT, and orientation","II",4000,"2-3","Validate input; calculate RINT; trace transpose and identifier handling","prepare_analysis_matrix; prepare_explanation_matrix","resolved_config.yaml"),
    (7,"UMAP and densMAP from graph construction to optimization","II",5000,"3-4,6","Derive graph weights; interpret cross-entropy; explain densMAP trade-offs","_fit_one","embedding.npy; visualization_embedding.tsv"),
    (8,"Repeated stochastic embeddings and concatenated geometry","II",3800,"7","Derive seed schedule; prove distance identity; diagnose unaligned-run effects","ensemble_seeds; run_repeated_umap","embedding_manifest.json"),
    (9,"HDBSCAN hierarchy, density, selection, and noise","II",4800,"5,8","Calculate mutual reachability; read hierarchy; interpret -1 responsibly","estimator_kwargs; fit_hdbscan","labels.tsv; model_table.csv"),
    (10,"Search-space enumeration and computational design","II",3300,"8-9","Enumerate products; estimate compute; trace candidate failure retention","enumerate_candidates; candidate_identity","search_space.tsv"),
    (11,"Candidate diagnostics, legacy_dimple, ranking, ties, and sensitivity","II",5200,"5,9-10","Derive metrics; hand-score candidates; analyze population dependence","evaluate_candidate; legacy_dimple_score; rank_models","model_table.csv; scoring_manifest.json"),
    (12,"Selected-model reproduction, provenance, and comparison","II",4000,"8-11","Replay fixed parameters; compare partitions; distinguish reconstruction layers","run_comparison; run_validation; capture_environment","selected_model.json; comparison_summary.json"),
    (13,"Installation, environment verification, and first run","III",3000,"1,6","Create clean environment; verify version/help; run a bounded smoke path","cli.main","environment.json"),
    (14,"Configuration and search-space inspection","III",3200,"6,10,13","Apply precedence; validate keys; predict exact candidate count","resolve_config; enumerate_candidates","resolved_config.yaml; search_space.tsv"),
    (15,"Complete pipeline execution and monitoring","III",3600,"7-14","Launch safely; read progress; recover from retained failures","run_search; write_model_outputs","run_manifest.json; logs"),
    (16,"Model summaries, selection, reproduction, comparison, and validation","III",3800,"11-15","Summarize rankings; select without leakage; replay and validate","rank_models; run_comparison; run_validation","ranked_models.csv; validation_report.json"),
    (17,"Original-space explanation, heatmaps, and responsible interpretation","III",4000,"3,5,12,16","Align IDs; compute correlations; read heatmaps without causal overclaim","run_explanation; render_heatmap","similarity_matrix.csv; heatmaps"),
    (18,"A hand-calculable toy analysis from matrix to score","IV",3600,"6-11","Perform manual transform; compute metrics; distinguish label equivalence","core analytical functions","lab 00 outputs"),
    (19,"Fixed synthetic end-to-end analysis","IV",3800,"13-17","Execute fixed fixture; audit every output; reproduce selected model","all CLI workflow functions","lab 01 outputs"),
    (20,"Custom bounded search, sensitivity, and selected-model replay","IV",3400,"10-16,19","Design bounded grid; compare candidate populations; replay selection","custom_score; run_search","lab 02 outputs"),
    (21,"Explanation, comparison, validation, and report generation","IV",3400,"16-17,19","Execute post-run commands; inspect joins; phrase bounded findings","run_explanation; run_comparison; run_validation","lab 03 outputs"),
    (22,"MNIST benchmark and original 164-IDP reconstruction protocol","IV",3800,"12-21","Separate public engineering benchmark from genetics; distinguish historical/fresh tracks; apply acceptance criteria","pipeline and historical adapters","lab 04/05 protocols"),
    (23,"Technical, statistical, biological, and cross-platform validation","V",3800,"5,12,19-22","Design layered validation; choose tolerances; identify pending cross-platform work","run_validation","validation matrix"),
    (24,"Reproducible reporting, limitations, migration, and reviewer-facing methods","V",3600,"1-23","Write methods from manifests; disclose limitations; migrate historical workflows","reporting and provenance modules","report; handoff"),
]


refs = [
    ("mcinnes2018umap","McInnes, L.; Healy, J.; Saul, N.; Grossberger, L.","UMAP: Uniform Manifold Approximation and Projection","Journal of Open Source Software","2018","10.21105/joss.00861","https://joss.theoj.org/papers/10.21105/joss.00861","primary","UMAP algorithm and software"),
    ("narayan2021densmap","Narayan, A.; Berger, B.; Cho, H.","Assessing single-cell transcriptomic variability through density-preserving data visualization","Nature Biotechnology","2021","10.1038/s41587-020-00801-7","https://pmc.ncbi.nlm.nih.gov/articles/PMC8195812/","primary","densMAP density objective"),
    ("campello2015hdbscan","Campello, R. J. G. B.; Moulavi, D.; Zimek, A.; Sander, J.","Hierarchical Density Estimates for Data Clustering, Visualization, and Outlier Detection","ACM Transactions on Knowledge Discovery from Data","2015","10.1145/2733381","https://doi.org/10.1145/2733381","primary","HDBSCAN hierarchy and stability"),
    ("mcinnes2017hdbscan","McInnes, L.; Healy, J.; Astels, S.","hdbscan: Hierarchical density based clustering","Journal of Open Source Software","2017","10.21105/joss.00205","https://joss.theoj.org/papers/10.21105/joss.00205","primary-software","contributed Python implementation"),
    ("rousseeuw1987","Rousseeuw, P. J.","Silhouettes: A graphical aid to the interpretation and validation of cluster analysis","Journal of Computational and Applied Mathematics","1987","10.1016/0377-0427(87)90125-7","https://doi.org/10.1016/0377-0427(87)90125-7","primary","silhouette definition"),
    ("calinski1974","Calinski, T.; Harabasz, J.","A dendrite method for cluster analysis","Communications in Statistics","1974","10.1080/03610927408827101","https://www.tandfonline.com/doi/abs/10.1080/03610927408827101","primary","variance-ratio criterion"),
    ("davies1979","Davies, D. L.; Bouldin, D. W.","A Cluster Separation Measure","IEEE Transactions on Pattern Analysis and Machine Intelligence","1979","10.1109/TPAMI.1979.4766909","https://doi.org/10.1109/TPAMI.1979.4766909","primary","Davies-Bouldin index"),
    ("moulavi2014dbcv","Moulavi, D.; Jaskowiak, P. A.; Campello, R. J. G. B.; Zimek, A.; Sander, J.","Density-Based Clustering Validation","SIAM International Conference on Data Mining","2014","10.1137/1.9781611973440.96","https://doi.org/10.1137/1.9781611973440.96","primary","DBCV"),
    ("beasley2009","Beasley, T. M.; Erickson, S.; Allison, D. B.","Rank-Based Inverse Normal Transformations Are Increasingly Used, But Are They Merited?","Behavior Genetics","2009","10.1007/s10519-009-9281-0","https://pmc.ncbi.nlm.nih.gov/articles/PMC2921808/","primary","RINT benefits and limitations"),
    ("hubert1985","Hubert, L.; Arabie, P.","Comparing partitions","Journal of Classification","1985","10.1007/BF01908075","https://doi.org/10.1007/BF01908075","primary","adjusted Rand index"),
    ("vinh2010","Vinh, N. X.; Epps, J.; Bailey, J.","Information Theoretic Measures for Clusterings Comparison: Variants, Properties, Normalization and Correction for Chance","Journal of Machine Learning Research","2010","JMLR 11:2837-2854","https://jmlr.org/papers/v11/vinh10a.html","primary","NMI and information-theoretic comparison"),
    ("gower1975","Gower, J. C.","Generalized Procrustes Analysis","Psychometrika","1975","10.1007/BF02291478","https://doi.org/10.1007/BF02291478","primary","configuration alignment"),
    ("venna2010","Venna, J.; Peltonen, J.; Nybo, K.; Aidos, H.; Kaski, S.","Information Retrieval Perspective to Nonlinear Dimensionality Reduction for Data Visualization","Journal of Machine Learning Research","2010","JMLR 11:451-490","https://jmlr.org/papers/v11/venna10a.html","primary","neighborhood preservation, trustworthiness/continuity context"),
    ("aggarwal2001","Aggarwal, C. C.; Hinneburg, A.; Keim, D. A.","On the Surprising Behavior of Distance Metrics in High Dimensional Spaces","ICDT 2001","2001","10.1007/3-540-44503-X_27","https://doi.org/10.1007/3-540-44503-X_27","primary","high-dimensional distance behavior"),
    ("kriegeskorte2009","Kriegeskorte, N.; Simmons, W. K.; Bellgowan, P. S. F.; Baker, C. I.","Circular analysis in systems neuroscience: the dangers of double dipping","Nature Neuroscience","2009","10.1038/nn.2303","https://www.nature.com/articles/nn.2303","primary-perspective","circular selection and analysis"),
    ("gao2024","Gao, L. L.; Bien, J.; Witten, D.","Selective Inference for Hierarchical Clustering","Journal of the American Statistical Association","2024","10.1080/01621459.2022.2116331","https://doi.org/10.1080/01621459.2022.2116331","primary","bounded selective-inference context"),
    ("reproduciblesum2015","Collange, S.; Defour, D.; Graillat, S.; Iakymchuk, R.","Numerical reproducibility for the parallel reduction on multi- and many-core architectures","Parallel Computing","2015","10.1016/j.parco.2015.09.001","https://doi.org/10.1016/j.parco.2015.09.001","primary","floating-point parallel reproducibility"),
    ("buliksullivan2015","Bulik-Sullivan, B. K. et al.","LD Score regression distinguishes confounding from polygenicity in genome-wide association studies","Nature Genetics","2015","10.1038/ng.3211","https://www.nature.com/articles/ng.3211","primary","LD and confounding context"),
    ("elliott2018","Elliott, L. T. et al.","Genome-wide association studies of brain imaging phenotypes in UK Biobank","Nature","2018","10.1038/s41586-018-0571-7","https://doi.org/10.1038/s41586-018-0571-7","primary","imaging-derived phenotype GWAS context"),
    ("oblong2024","Oblong, L. M. et al.","Principal and independent genomic components of brain structure and function","Genes, Brain and Behavior","2024","10.1111/gbb.12876","https://doi.org/10.1111/gbb.12876","primary","genomic PCA/ICA comparator; corrected attribution"),
    ("grotzinger2019","Grotzinger, A. D. et al.","Genomic structural equation modelling provides insights into the multivariate genetic architecture of complex traits","Nature Human Behaviour","2019","10.1038/s41562-019-0566-x","https://doi.org/10.1038/s41562-019-0566-x","primary","Genomic SEM comparator"),
    ("turley2018","Turley, P. et al.","Multi-trait analysis of genome-wide association summary statistics using MTAG","Nature Genetics","2018","10.1038/s41588-017-0009-4","https://doi.org/10.1038/s41588-017-0009-4","primary","MTAG comparator"),
    ("vandermeer2020","van der Meer, D. et al.","Understanding the genetic determinants of the brain with MOSTest","Nature Communications","2020","10.1038/s41467-020-17368-1","https://doi.org/10.1038/s41467-020-17368-1","primary","MOSTest comparator"),
    ("lee2021","Lee, C. H. et al.","PLEIO: a method to map and interpret pleiotropic loci with GWAS summary statistics","American Journal of Human Genetics","2021","10.1016/j.ajhg.2020.11.017","https://pmc.ncbi.nlm.nih.gov/articles/PMC7820744/","primary","PLEIO comparator"),
    ("zhang2023","Zhang, Z. et al.","A scalable approach to characterize pleiotropy across thousands of human diseases and complex traits using GWAS summary statistics","American Journal of Human Genetics","2023","10.1016/j.ajhg.2023.09.015","https://doi.org/10.1016/j.ajhg.2023.09.015","primary","distinct Zhang pleiotropy paper, not reviewer attribution"),
]


claims = [
    ("REL-001","Edition 1; release dossier","Freeze 3 RC1 is software complete.","Freeze 3 RC1 is a software-complete release candidate under current local and fixed-fixture evidence; it is not scientifically frozen or cross-platform validated.","release","pyproject.toml; source; tests","45-test prior run; new TE2 run pending","","verified_with_qualification","Fresh 164-IDP and Docker/cloud gates remain pending.","1,23,24","reproducibility","verified"),
    ("DATA-001","source and data contract","The input is a generic matrix.","Production input has variants in rows, four declared metadata columns by default, and vector/IDP columns; preprocessing drops the prefix and transposes to vectors by variants.","implementation","preprocessing.py; io.py","fixed synthetic fixture","","implementation_specific","Explanation mode also permits an explicit vectors-by-variants orientation.","2,6","input audit","verified"),
    ("DATA-002","source and provisional prose","RINT is standard and row-wise.","RINT is optional, off by default, and applied column-wise to analysis columns before transpose using average ranks and (rank-0.5)/n.","implementation","preprocessing.rank_inverse_normal_transform","unit tests planned/current","beasley2009","implementation_specific","The post-transpose viewpoint reverses row/column language; always state the orientation.","3,6,18","method clarity","verified"),
    ("PIPE-001","Gemini/provisional descriptions","PCA is applied before UMAP.","The current production path passes the prepared matrix directly to UMAP and has no user-visible PCA/SVD/ICA pre-reducer.","implementation","pipeline.py; umap_runner.py","source audit","oblong2024","verified","UMAP internals do not constitute a documented preprocessing reducer.","4,7","comparator","verified"),
    ("PIPE-002","Gemini dossier","Repeated UMAP bypasses randomness and reveals true topology.","Repeated seeded embeddings are concatenated as an empirical representation strategy; the implementation supplies no theorem that it eliminates stochasticity or recovers true topology.","methodological","umap_runner.py","bounded rerun evidence pending TE2","mcinnes2018umap","reject","Parameters, layout symmetries, libraries, and hardware still matter.","7,8,23","reviewer coordinate concern","resolved"),
    ("PIPE-003","source/default config","The standard grid contains 2,430 candidates.","The standard grid enumerates 45 min_cluster_size values, 18 min_samples values, and 3 epsilon values: 2,430 HDBSCAN candidates for one UMAP configuration.","software","config.py; search_space.py","show-search-space prior and TE2 run","","verified","Custom and extended modes differ.","10,14","parameter audit","verified"),
    ("PIPE-004","source","Freeze 3 uses sklearn HDBSCAN.","Freeze 3 calls the contributed hdbscan package, not sklearn.cluster.HDBSCAN.","implementation","hdbscan_runner.py","run manifests","campello2015hdbscan; mcinnes2017hdbscan","implementation_specific","Backends with similar names can differ in semantics.","9,13","implementation identity","verified"),
    ("SCORE-001","Gemini/Edition 1 correction","DBCV is the default score.","DBCV is an optional diagnostic; legacy_dimple ranks with normalized silhouette and cluster count and optionally subtracts a noise component.","implementation","metrics.py; scoring.py","tests; hand example","moulavi2014dbcv","reject","Computing a diagnostic does not make it part of the ranking objective.","11,18","model selection","resolved"),
    ("SCORE-002","provisional prose","Silhouette is inherently Euclidean.","Silhouette is defined relative to a distance; Freeze 3 passes the configured HDBSCAN metric to scikit-learn.","statistical","metrics.evaluate_candidate","unit tests","rousseeuw1987","reject","Metric choice remains geometry-dependent; CH and DB use Euclidean centroid geometry.","5,11","metric audit","resolved"),
    ("SCORE-003","source","legacy_dimple has biological target bands.","The default score has no biological label, pQTL target, preferred cluster band, or noise ceiling.","implementation","scoring.py; config.py","score reproduction","","verified","The population-relative heuristic still embeds trade-offs via ranges.","11,24","model-selection integrity","verified"),
    ("INT-001","provisional interpretation","UMAP coordinates are biological loadings.","UMAP coordinates are descriptive latent coordinates, not biological loadings, effects, mechanisms, or causal axes.","interpretation","interpretation.py; EXPLAINABILITY.md","explanation outputs","mcinnes2018umap","reject","Optional coordinate correlations remain descriptive.","7,17","interpretation","resolved"),
    ("INT-002","provisional interpretation","Noise means non-pleiotropic.","Label -1 means unassigned under the fitted representation, metric, density assumptions, and parameters.","interpretation","hdbscan_runner.py","labels outputs","campello2015hdbscan","reject","Noise status can change across candidate settings.","9,17","unassigned IDPs","resolved"),
    ("INT-003","review response context","Original-space correlations prove mechanism.","Pearson/Spearman summaries are post-selection descriptive diagnostics conditional on the retained partition.","interpretation","interpretation.py","lab 03 planned","kriegeskorte2009; gao2024","verified_with_qualification","They do not provide causal, replication, or unbiased significance evidence.","5,17,21","biological validity","resolved"),
    ("INT-004","suggested analysis","ANOVA on discovered clusters validates them.","Classical tests on the same data used for group discovery are vulnerable to circularity; Freeze 3 omits cluster ANOVA and post-selection p-values.","statistical","interpretation.py; limitations docs","source audit","kriegeskorte2009; gao2024","verified_with_qualification","The cited selective method is not a turnkey HDBSCAN procedure.","5,17,23","validity","resolved"),
    ("CMP-001","Gemini dossier","K-means is completely ineffective.","K-means targets centroid-based partitions and may mismatch irregular density structure; it is not universally ineffective.","comparator","not implemented","not applicable","","reject","Performance depends on representation and objective.","4,5,24","positioning","resolved"),
    ("CMP-002","reviewer/Gemini synthesis","PCA/ICA components are proven mechanisms.","Genomic PCA/ICA provide linear components; reproducible components do not by themselves establish mechanisms or a gold standard.","comparator","not implemented","not applicable","oblong2024","reject","These tools answer different questions from DIMPLE-GWAS Stage 1.","4,24","comparator","resolved"),
    ("CMP-003","review context","MOSTest, MTAG, PLEIO, and DIMPLE-GWAS are direct competitors.","These multivariate association tools and DIMPLE-GWAS have different inputs, objectives, and outputs; compare questions rather than a single rank.","comparator","scope docs","not applicable","turley2018; vandermeer2020; lee2021","verified_with_qualification","Workflows can be complementary.","1,24","positioning","resolved"),
    ("VAL-001","release evidence","45 tests prove biological validity.","The local suite's passing tests support bounded software contracts, not biological validity.","validation","tests","prior 45-test run; fresh run pending","","verified_with_qualification","One environment cannot establish cross-platform behavior.","1,23","reproducibility","verified"),
    ("VAL-002","bounded fixture","A fixed rerun proves general determinism.","Within the prior same-environment fixture comparison, ARI, NMI, noise Jaccard, and mapped membership were 1 with near-zero Procrustes disparity.","validation","comparison.py","Edition 1 lab output; TE2 rerun pending","hubert1985; vinh2010; gower1975","verified_with_qualification","Does not generalize across platforms or all configurations.","12,19,23","technical validation","verified"),
    ("HIST-001","historical workbook/notebook","The historical 164-IDP solution was top-ranked.","The historical five-cluster solution was manually selected from sorted row 16, not the top automatic score.","historical","historical adapter/docs","historical artifacts","","historical_only","The historical retained table contains 333 successful rows from a theoretical 2,430-candidate grid.","11,22,24","selection disclosure","verified"),
    ("HIST-002","historical/fresh conflation","Freeze 3 freshly regenerated the 164-IDP result.","Freeze 3 adapted and rescored immutable historical outputs, but a fresh 1,000-seed 164-IDP fit remains deferred until Docker.","historical","original-IDP configs","historical only","","reject","The book supplies a protocol and acceptance criteria, not fabricated results.","22,23","reproducibility","deferred"),
    ("HIST-003","historical artifacts","The historical labels contain five clusters.","The historical record contains 164 IDPs: 102 noise and five non-noise clusters of 9, 13, 15, 14, and 11.","historical","historical labels","checksummed historical outputs","","historical_only","Original material may change after current-development adjudication.","22","historical reconstruction","verified"),
    ("REP-001","container rhetoric","A pinned container guarantees identical output everywhere.","Pinning improves traceability but cannot alone guarantee bitwise identity across architecture, hardware, numerical libraries, or thread schedules.","reproducibility","provenance.py","same-platform evidence","reproduciblesum2015","reject","Docker/Linux/cloud validation remains pending.","12,23,24","cross-platform","resolved"),
    ("REV-001","Gemini/reviewer attribution","The genomic-components paper was authored by Zhang, Yang, or Zhao.","Principal and independent genomic components of brain structure and function is by Oblong et al. (2024), DOI 10.1111/gbb.12876.","citation","manuscript bibliography","reviewer action register","oblong2024","reject","No exact Yang/Zhao reviewer paper is identifiable; do not guess.","24","reviewer literature","resolved_with_gap"),
    ("METH-001","source audit","RINT makes transformed data normally distributed in an inferential sense.","Freeze 3 maps observed marginal ranks to normal scores; that deterministic sample transformation does not validate downstream parametric assumptions or causal interpretation.","statistical","preprocessing.py","hand lab planned","beasley2009","verified_with_qualification","Dependence, ties, and selection remain.","3,6,18","method clarity","verified"),
    ("METH-002","source audit","densMAP preserves all densities exactly.","densMAP adds a density-preservation term to the UMAP objective; it balances objectives and does not guarantee exact preservation.","statistical","umap_runner.py delegates densmap=True","lab 01 planned","narayan2021densmap","verified_with_qualification","Domain evidence comes from another application area.","7","method clarity","verified"),
    ("METH-003","source audit","Repeated concatenation aligns equivalent UMAP axes.","Freeze 3 concatenates raw run coordinates without Procrustes alignment; squared Euclidean distances therefore sum run-specific distances but remain sensitive to run scale and layout.","implementation","umap_runner.py","hand identity and lab planned","mcinnes2018umap; gower1975","implementation_specific","Rotation preserves within-run Euclidean distance; scale does not.","8","coordinate concern","verified"),
    ("METH-004","source audit","CH and DB validate HDBSCAN density structure directly.","Freeze 3 calculates CH and DB on non-noise embedded points using Euclidean centroid geometry; they are supplementary views that may disagree with density-based criteria.","implementation","metrics.py","lab 02 planned","calinski1974; davies1979","implementation_specific","Do not treat agreement as independent evidence after selection.","11","metric audit","verified"),
    ("METH-005","source audit","Trustworthiness and continuity are symmetric names for the same statistic.","Freeze 3 obtains two directed neighborhood diagnostics by swapping original and projected spaces in sklearn's trustworthiness function.","implementation","metrics.embedding_quality_metrics","lab 01 planned","venna2010","implementation_specific","Both are computed with Euclidean geometry and possible sampling.","7,11","projection diagnostics","verified"),
    ("GWAS-001","scientific context","Similarity among GWAS vectors is pure shared biology.","Vector geometry can reflect shared biology, LD structure, sample overlap, scale, confounding, and preprocessing; DIMPLE-GWAS does not separate these causes.","scientific","scope and input only","not tested","buliksullivan2015","verified_with_qualification","Interpretation requires upstream harmonization and independent evidence.","2,3,23","biological calibration","verified"),
]


def build_concepts() -> None:
    write_tsv(EVIDENCE / "statistical_concept_coverage.tsv",
              ["concept_id","concept","definition","equation_or_notation","interpretation_and_caution","functions","outputs","chapters","evidence_sources","status"],
              [list(row)+["planned_complete"] for row in concepts])
    lines = ["# Statistical concept dependency map", "", "This map fixes the prerequisite order used by Edition 2. Arrows mean “must be understood before,” not causal influence.", "", "```mermaid", "flowchart TD", "  vectors[GWAS-derived vectors and identifiers] --> geometry[distance, similarity, scaling]", "  geometry --> transform[RINT and orientation]", "  geometry --> graph[nearest-neighbor graph]", "  graph --> umap[UMAP fuzzy graph and objective]", "  umap --> dens[densMAP regularization]", "  umap --> repeats[seeded repeats and concatenation]", "  repeats --> density[core distance and mutual reachability]", "  density --> hierarchy[HDBSCAN hierarchy, stability, and noise]", "  hierarchy --> diagnostics[candidate diagnostics]", "  diagnostics --> score[legacy_dimple and ranking]", "  score --> replay[selected-model replay]", "  replay --> compare[ARI, NMI, noise Jaccard, Procrustes]", "  replay --> explain[original-space Pearson/Spearman explanation]", "  compare --> ladder[validation ladder]", "  explain --> circular[circularity safeguards]", "  circular --> ladder", "```", "", "The complete equation, implementation, output, evidence, and chapter mapping is in `statistical_concept_coverage.tsv`. All Tier A analytical routes have prerequisite concepts. Concepts delegated to third-party libraries are labeled as delegated behavior rather than DIMPLE-GWAS reimplementations."]
    (EVIDENCE / "statistical_concept_dependency_map.md").write_text("\n".join(lines)+"\n", encoding="utf-8")


def build_curriculum() -> None:
    write_tsv(EVIDENCE / "chapter_content_budget.tsv", ["chapter","part","title","substantive_word_target","minimum_words","editorial_reason_if_below_1500"], [[n,p,t,b,1500,""] for n,t,p,b,*_ in chapters])
    objective_rows=[]
    for n,title,part,budget,prereq,objectives,functions,outputs in chapters:
        for idx,objective in enumerate(objectives.split("; "),1):
            objective_rows.append([n,f"LO-{n:02d}.{idx}",objective,"chapter exercise and evidence walk-through"])
    write_tsv(EVIDENCE / "learning_objectives.tsv", ["chapter","objective_id","learning_objective","assessment"], objective_rows)
    lines=["# Edition 2 curriculum specification","",f"The 24-chapter plan targets **{sum(row[3] for row in chapters):,} substantive words** before appendices, bibliography, and generated reference tables. It merges Edition 1's short checklist chapters into connected conceptual and operational units.","","| Ch. | Part | Title | Prerequisites | Target | Core implementation |", "| ---: | :---: | --- | --- | ---: | --- |"]
    for n,title,part,budget,prereq,objectives,functions,outputs in chapters:
        lines.append(f"| {n} | {part} | {title} | {prereq} | {budget:,} | `{functions}` |")
    lines += ["", "Every chapter must open with a real problem, introduce intuition before formalism, trace claims to source or literature, include a worked or executed example where applicable, and end with exercises mapped to its objectives. Lookup-heavy details remain in appendices, the function atlas, and the output atlas."]
    (EVIDENCE / "edition2_curriculum_specification.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    dep=["# Chapter dependency map","","```mermaid","flowchart LR","  C1 --> C2 --> C3 --> C4 --> C5","  C3 --> C6 --> C7 --> C8 --> C9 --> C10 --> C11 --> C12","  C6 --> C13 --> C14 --> C15 --> C16 --> C17","  C11 --> C18 --> C19 --> C20 --> C21 --> C22","  C12 --> C23","  C17 --> C23 --> C24","```","","The linear reading path is supported, while experienced analysts may enter at Chapter 13 and follow the operational chain with cross-references to Chapters 6–12."]
    (EVIDENCE / "chapter_dependency_map.md").write_text("\n".join(dep)+"\n",encoding="utf-8")

    old_gap=QA / "edition1_chapter_gap_matrix.tsv"
    cross=[]
    if old_gap.exists():
        with old_gap.open(encoding="utf-8") as h:
            rows=list(csv.DictReader(h,delimiter="\t"))
        for row in rows:
            title=row.get("title","")
            text=title.lower()
            if any(k in text for k in ["umap","densmap"]): target="7-8"
            elif "hdbscan" in text or "noise" in text: target="9"
            elif any(k in text for k in ["score","rank","selection"]): target="11,16"
            elif any(k in text for k in ["explain","heatmap","correlation"]): target="17,21"
            elif any(k in text for k in ["compare","validat","reproduc"]): target="12,16,23"
            elif any(k in text for k in ["install","environment"]): target="13"
            elif any(k in text for k in ["config","search"]): target="10,14"
            elif any(k in text for k in ["input","preprocess","rint","orientation"]): target="3,6"
            elif any(k in text for k in ["original","164","mnist","synthetic","tutorial"]): target="18-22"
            elif any(k in text for k in ["limit","scope","release","review"]): target="1,23,24"
            else: target="1-24 or appendix; adjudicated during drafting"
            cross.append([row.get("chapter",row.get("chapter_number","")),title,target,"rewrite/merge","Edition 1 evidence retained; prose not copied wholesale"])
    write_tsv(EVIDENCE / "edition1_to_edition2_crosswalk.tsv", ["edition1_chapter","edition1_title","edition2_destination","action","note"], cross)


def build_references() -> None:
    REFERENCES.mkdir(parents=True,exist_ok=True)
    write_tsv(EVIDENCE / "citation_verification_log.tsv", ["citation_key","authors","title","venue","year","doi_or_identifier","primary_url","source_type","nearby_claim","metadata_status"], [list(r)+["verified"] for r in refs])
    md=["# Verified bibliography for Textbook Edition 2","","Metadata and relevance were checked against primary publisher, PubMed/PMC, JMLR/JOSS, or DOI records. Citation does not imply validation of DIMPLE-GWAS beyond the nearby claim.",""]
    for key,authors,title,venue,year,doi,url,kind,claim in refs:
        md.append(f"- **{key}.** {authors} ({year}). *{title}*. {venue}. [{doi}]({url}). Supports: {claim}.")
    md += ["", "## Attribution and unresolved records", "", "The genomic-components paper is Oblong et al. (2024), DOI `10.1111/gbb.12876`. Zhang et al. (2023), DOI `10.1016/j.ajhg.2023.09.015`, is a separate paper. The supplied reviewer record does not identify an exact Yang- or Zhao-attributed paper; those proposed attributions remain unresolved and are not cited as facts."]
    (REFERENCES/"VERIFIED_BIBLIOGRAPHY.md").write_text("\n".join(md)+"\n",encoding="utf-8")
    bib=[]
    for key,authors,title,venue,year,doi,url,kind,claim in refs:
        author_field=" and ".join(part.strip() for part in authors.replace(" et al.","").split(";"))
        bib.append(f"@article{{{key},\n  author = {{{author_field}}},\n  title = {{{title}}},\n  journal = {{{venue}}},\n  year = {{{year}}},\n  doi = {{{doi}}},\n  url = {{{url}}}\n}}")
    (REFERENCES/"dimple_gwas_textbook_edition2.bib").write_text("\n\n".join(bib)+"\n",encoding="utf-8")


def build_claims() -> None:
    header=["claim_id","original_source","original_wording","proposed_safe_wording","category","implementation_evidence","executed_evidence","primary_citation","classification","limitation_or_counterpoint","book_location","reviewer_relevance","status","resolution"]
    write_tsv(EVIDENCE/"claim_evidence_register.tsv",header,[list(r)+["accepted_for_internal_draft" if r[12] not in {"deferred"} else "deferred_by_coordinator"] for r in claims])
    correction_ids={"PIPE-002","SCORE-001","SCORE-002","INT-001","INT-002","INT-003","INT-004","CMP-001","CMP-002","REP-001","REV-001","METH-001","METH-002","METH-003","METH-004","METH-005"}
    correction_rows=[]
    for r in claims:
        if r[0] in correction_ids:
            correction_rows.append([r[0],r[1],r[2],r[3],r[9],r[5],r[7],r[12]])
    write_tsv(EVIDENCE/"edition1_and_gemini_correction_ledger.tsv",["claim_id","source","unsafe_or_incomplete_wording","edition2_wording","reason_or_limitation","implementation_evidence","external_evidence","status"],correction_rows)


def update_manifest() -> None:
    manifest_path=EDITION2/"BOOK_BUILD_MANIFEST.json"
    data=json.loads(manifest_path.read_text(encoding="utf-8"))
    data["statistical_concepts"]={"count":len(concepts),"gate_2":"pass_planning","coverage":"equations, cautions, functions, outputs, chapters, and evidence mapped"}
    data["literature"]={"verified_entries":len(refs),"claim_register_entries":len(claims),"unresolved_reviewer_attributions":["Yang-attributed paper","Zhao-attributed paper"]}
    data["curriculum"]={"chapters":len(chapters),"parts":6,"planned_substantive_words":sum(row[3] for row in chapters),"gate_4":"pass_planning"}
    data["phase_status"]["phase_2_statistical_foundations"]="complete_planning_gate"
    data["phase_status"]["phase_3_claims_and_literature"]="complete_with_named_attribution_gap"
    data["phase_status"]["phase_4_curriculum"]="complete_planning_gate"
    manifest_path.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf-8")


def main() -> None:
    EVIDENCE.mkdir(parents=True,exist_ok=True)
    build_concepts()
    build_curriculum()
    build_references()
    build_claims()
    update_manifest()
    print(f"Concepts: {len(concepts)}; references: {len(refs)}; claims: {len(claims)}; planned words: {sum(r[3] for r in chapters):,}")


if __name__ == "__main__":
    main()
