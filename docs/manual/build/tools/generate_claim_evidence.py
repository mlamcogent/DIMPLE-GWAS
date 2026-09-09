#!/usr/bin/env python3
"""Generate first-draft claim, citation, correction, and comparator registers."""

from __future__ import annotations

import csv
from pathlib import Path


FREEZE3 = Path(__file__).resolve().parents[4]
MANUAL = FREEZE3 / "docs" / "manual"
EVIDENCE = MANUAL / "evidence"
REFERENCES = MANUAL / "references"


def write_tsv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


SOURCES = {
    "umap2018": ("McInnes et al. (2018), UMAP", "10.21105/joss.00861", "https://joss.theoj.org/papers/10.21105/joss.00861"),
    "densmap2021": ("Narayan, Berger & Cho (2021), densMAP", "10.1038/s41587-020-00801-7", "https://www.nature.com/articles/s41587-020-00801-7"),
    "hdbscan2015": ("Campello et al. (2015), HDBSCAN*", "10.1145/2733381", "https://doi.org/10.1145/2733381"),
    "hdbscan2017": ("McInnes, Healy & Astels (2017), hdbscan library", "10.21105/joss.00205", "https://joss.theoj.org/papers/10.21105/joss.00205"),
    "dbcv2014": ("Moulavi et al. (2014), DBCV", "10.1137/1.9781611973440.96", "https://epubs.siam.org/doi/10.1137/1.9781611973440.96"),
    "silhouette1987": ("Rousseeuw (1987), silhouettes", "10.1016/0377-0427(87)90125-7", "https://doi.org/10.1016/0377-0427(87)90125-7"),
    "selective2024": ("Gao, Bien & Witten (2024), selective inference for hierarchical clustering", "10.1080/01621459.2022.2116331", "https://pubmed.ncbi.nlm.nih.gov/38660582/"),
    "oblong2024": ("Oblong et al. (2024), genomic PCA/ICA", "10.1111/gbb.12876", "https://onlinelibrary.wiley.com/doi/10.1111/gbb.12876"),
    "genomicsem2019": ("Grotzinger et al. (2019), Genomic SEM", "10.1038/s41562-019-0566-x", "https://www.nature.com/articles/s41562-019-0566-x"),
    "mtag2018": ("Turley et al. (2018), MTAG", "10.1038/s41588-017-0009-4", "https://www.nature.com/articles/s41588-017-0009-4"),
    "mostest2020": ("van der Meer et al. (2020), MOSTest", "10.1038/s41467-020-17368-1", "https://www.nature.com/articles/s41467-020-17368-1"),
    "pleio2021": ("Lee et al. (2021), PLEIO", "10.1016/j.ajhg.2020.11.017", "https://pmc.ncbi.nlm.nih.gov/articles/PMC7820744/"),
    "zhang2023": ("Zhang et al. (2023), scalable pleiotropy characterization", "10.1016/j.ajhg.2023.09.015", "https://pubmed.ncbi.nlm.nih.gov/37879338/"),
    "hofer2020": ("Hofer et al. (2020), cortical structure genetics", "10.1038/s41467-020-18367-y", "https://www.nature.com/articles/s41467-020-18367-y"),
    "elliott2018": ("Elliott et al. (2018), UK Biobank imaging GWAS", "10.1038/s41586-018-0571-7", "https://www.nature.com/articles/s41586-018-0571-7"),
    "umapdocs": ("UMAP official parameter and API documentation", "official documentation", "https://umap-learn.readthedocs.io/en/latest/parameters.html"),
    "hdbscandocs": ("hdbscan official parameter/API documentation", "official documentation", "https://hdbscan.readthedocs.io/en/latest/api.html"),
    "sklearnsilhouette": ("scikit-learn silhouette_score documentation", "official documentation", "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html"),
}


def claim_rows() -> list[list[object]]:
    return [
        ["REL-001", "Freeze 3 RC1 is software complete.", "Freeze 3 RC1 is a software-complete release candidate under local macOS and fixed-fixture evidence; it is not scientifically frozen or cross-platform validated.", "release", "1,3,42,46", "pyproject.toml; README.md", "freeze3_workspace/reports/09_freeze3_release_assessment.md", "", "strong local", "Fresh 164-IDP and Docker/cloud gates remain.", "Reviewer reproducibility", "verified_with_qualification", "manual", "Use status banner throughout."],
        ["REL-002", "Version is 3.0.0rc1.", "The installed package and pyproject metadata report 3.0.0rc1.", "software", "1,9,37", "pyproject.toml; CLI --version", "pytest/pip environment", "", "strong", "No Git commit is available.", "", "verified", "manual", "Checksum identity substitutes for commit."],
        ["DATA-001", "Production data are variants by vectors.", "The run input is variants in rows with four declared metadata columns followed by vector/IDP columns; preprocessing drops the prefix and transposes to vectors by variants.", "implementation", "4,10,15", "preprocessing.py; io.py", "executed synthetic and 164 fixtures", "", "strong", "Legacy explanation also supports explicit vectors-by-variants orientation.", "", "implementation_specific", "manual", "Document exact ID matching."],
        ["DATA-002", "RINT is part of the standard method.", "Row/column terminology must follow implementation: optional rank inverse normal transformation is applied column-wise to analysis columns before transpose when explicitly configured; it is off by default.", "implementation", "10,15", "preprocessing.py; config.py", "tests/test_preprocessing_metrics.py", "", "strong", "Gemini/coordinator wording may say row-wise depending on post-transpose viewpoint.", "", "verified_with_qualification", "manual", "Use code orientation to prevent ambiguity."],
        ["PIPE-001", "PCA is applied before UMAP.", "The default production path passes the full prepared matrix to UMAP and has no PCA/SVD/ICA pre-reducer.", "implementation", "4,15,17", "pipeline.py; umap_runner.py", "freeze3_workspace/runtime_probes/freeze2_no_reducer", "", "strong", "UMAP's internal initialization is not a user-visible pre-reduction stage.", "", "verified", "manual", "Explicitly reject hidden-reducer claim."],
        ["PIPE-002", "Repeated UMAP bypasses randomness and reveals true topology.", "Repeated seeded embeddings are concatenated as an empirical stability strategy. This implementation offers no theorem that it eliminates stochasticity, estimates expected distance, recovers true topology, or performs formal consensus clustering.", "methodological", "6,17,30", "umap_runner.py", "tests and tutorial rerun", "umap2018; umapdocs", "qualified", "Base parameters and software/hardware still matter.", "Reviewer coordinate-independence concern", "reject", "manual", "Gemini statement corrected."],
        ["PIPE-003", "Standard search contains 2,430 candidates.", "The standard grid enumerates 45 min_cluster_size values x 18 min_samples values x 3 epsilon values = 2,430 HDBSCAN candidates for one UMAP configuration.", "software", "12,18,39", "config.py; search_space.py", "executed show-search-space", "", "strong", "Custom/extended counts differ; extended shipped example is 1,728.", "Reviewer parameter audit", "verified", "manual", "Show calculation."],
        ["PIPE-004", "Freeze 3 uses contributed hdbscan.", "Freeze 3 fits the contrib hdbscan package, not sklearn.cluster.HDBSCAN.", "implementation", "18,37", "hdbscan_runner.py", "run manifests", "hdbscan2017; hdbscan2015", "strong", "Estimator semantics differ across implementations.", "", "implementation_specific", "manual", "Name backend in manifests."],
        ["SCORE-001", "DBCV is the default DIMPLE score.", "DBCV can be computed as an optional diagnostic, but legacy_dimple ranks using normalized silhouette and cluster count and, only when enabled, a subtracted noise term. DBCV is not a legacy score component.", "implementation", "19,20,40", "scoring.py; metrics.py", "tests/test_scoring_ranking.py", "dbcv2014", "strong", "Base config may compute DBCV without using it for ranking.", "Reviewer score audit", "reject", "manual", "Separate calculation from ranking."],
        ["SCORE-002", "Silhouette is inherently Euclidean.", "Silhouette is defined relative to a distance metric; Freeze 3 supplies the configured HDBSCAN metric to scikit-learn. Its suitability remains geometry dependent.", "statistical", "19,20", "metrics.py", "tests/test_preprocessing_metrics.py", "silhouette1987; sklearnsilhouette", "strong", "Other internal indices also have assumptions.", "", "reject", "manual", "Do not universalize failure."],
        ["SCORE-003", "legacy_dimple has universal biological targets.", "The default score contains no preferred cluster-count band, noise ceiling, largest-cluster target, pQTL target, or biological label.", "implementation", "20,21,40", "scoring.py; config.py", "legacy-score reproduction", "", "strong", "The score remains a population-relative heuristic with dynamic-range weighting.", "Reviewer model-selection integrity", "verified", "manual", "Explain full formula and trade-offs."],
        ["INT-001", "UMAP coordinates are biological loadings.", "UMAP coordinates are descriptive latent coordinates and are not biological loadings, effects, mechanisms, or causal axes.", "interpretation", "24,25,31", "interpretation.py; docs/EXPLAINABILITY.md", "reviewer action register", "umap2018", "strong", "Coordinates can be correlated descriptively if explicitly requested.", "Reviewer interpretation", "reject", "manual", "Visible warning in explainability chapters."],
        ["INT-002", "Noise means non-pleiotropic or irrelevant.", "Label -1 means unassigned under the fitted representation, metric, density assumptions, and parameters. It does not establish biological irrelevance or lack of pleiotropy.", "interpretation", "18,28,31", "hdbscan_runner.py; interpretation.py", "historical adapter", "hdbscan2015", "strong", "Noise status can change across parameterizations.", "Reviewer asks characterisation of unassigned IDPs", "reject", "manual", "Use algorithmic language only."],
        ["INT-003", "Original-space correlations prove mechanism.", "Pearson/Spearman original-space summaries are post-selection descriptive diagnostics conditional on the retained partition; they do not prove causation, mechanism, replication, or unbiased significance.", "interpretation", "25,26,29", "interpretation.py", "tutorial 3 output", "selective2024", "strong", "Correlation also reflects shared technical and LD structure.", "Reviewer biological validity", "verified_with_qualification", "manual", "No p-values emitted."],
        ["INT-004", "Naive ANOVA validates discovered clusters.", "Classical tests applied to the same data used to discover groups are vulnerable to selection bias and circularity; Freeze 3 intentionally omits cluster ANOVA and post-selection p-values.", "statistical", "29,30", "interpretation.py", "docs/SCIENTIFIC_LIMITATIONS.md", "selective2024", "strong conceptual", "The cited selective method is for hierarchical clustering, not a turnkey HDBSCAN procedure.", "Reviewer validity", "verified_with_qualification", "manual", "Recommend independent/held-out validation."],
        ["CMP-001", "K-means is completely ineffective.", "K-means is optimized for centroid-based partitions and can be poorly matched to irregular density structure, but it is not universally ineffective.", "comparator", "7,18", "not implemented", "Gemini correction", "", "moderate", "Performance depends on representation and objective.", "Reviewer positioning", "reject", "manual", "Comparator matrix only."],
        ["CMP-002", "PCA/ICA components are proven biological mechanisms.", "Genomic PCA/ICA provide linear components that may improve representation and interpretation; component reproducibility or loadings do not by themselves establish biological mechanisms or a gold standard.", "comparator", "7,24", "not implemented", "manuscript and reviewer register", "oblong2024", "strong", "Oblong et al. support reproducibility and interpretability, not automatic causality.", "Reviewer comparator", "reject", "manual", "Correct attribution to Oblong et al."],
        ["CMP-003", "MOSTest, MTAG, PLEIO, and DIMPLE-GWAS are direct competitors.", "MOSTest, MTAG, and PLEIO are multivariate association tools with different outputs; DIMPLE-GWAS clusters phenotype vectors. Compare scientific questions and outputs, not a single performance ranking.", "comparator", "7", "Freeze 3 scope", "reviewer register", "mostest2020; mtag2018; pleio2021", "strong", "Some workflows may be complementary.", "Reviewer positioning", "verified_with_qualification", "manual", "Not implemented in Freeze 3."],
        ["VAL-001", "45 tests prove biological validity.", "The fresh local suite passed 45 tests; this supports software behavior and fixed-fixture contracts, not biological validity.", "validation", "3,30,42", "tests", "docs/manual/build/logs/pytest_full.log", "", "strong local", "Warnings documented; one OS/architecture only.", "Reviewer reproducibility", "verified_with_qualification", "manual", "Separate validation ladder."],
        ["VAL-002", "Fixed rerun is deterministic.", "The bounded synthetic fixture and its reproduction had ARI/NMI/noise Jaccard/mapped membership of 1 and near-zero Procrustes disparity in the same environment.", "validation", "23,34", "comparison.py", "tutorial 3 comparison_summary.json", "", "strong bounded", "Does not generalize to platforms or all configurations.", "", "verified_with_qualification", "manual", "Use exact tutorial values."],
        ["HIST-001", "The historical 164-IDP solution was top-ranked.", "The published historical five-cluster solution was manually selected from sorted row 16 (epsilon 0, min_samples 4, min_cluster_size 6), not the top automatic score.", "historical", "21,36", "historical notebook evidence", "freeze3 reports 07/08", "", "strong historical", "Historical table retains 333 successful rows from a 2,430 candidate theoretical grid.", "Reviewer model-selection", "historical_only", "manual", "Disclose prominently."],
        ["HIST-002", "Fresh Freeze 3 regenerated the 164 solution.", "Freeze 3 rescored and adapted immutable historical labels exactly, but the full 1,000-seed 164-IDP fit has not been freshly executed.", "historical", "36,46", "configs/original_idp_164_*.yaml", "freeze3 reports 07/08", "", "strong boundary", "Fresh reproduction is deferred to Docker phase.", "Reviewer reproducibility", "reject", "manual", "Two-track tutorial."],
        ["HIST-003", "164 historical counts.", "The historical record contains 164 IDPs: 102 noise and five non-noise clusters of 9, 13, 15, 14, and 11.", "historical", "36,41", "historical workbook and labels", "freeze3 reports 07/08", "", "strong historical", "One historical UMAP_3 value is missing; labels are complete.", "", "verified", "manual", "Mark original material provisional for later development."],
        ["REP-001", "Pinned dependencies guarantee identical outputs.", "Dependency pinning improves traceability but does not guarantee bitwise identity across OS, architecture, hardware, BLAS/OpenMP, thread counts, or numerical libraries.", "reproducibility", "17,42,44", "provenance.py", "same-platform tutorial", "", "strong engineering", "Docker/Linux/cloud validation is pending.", "Reviewer reproducibility", "reject", "manual", "Use exact versus tolerance rules."],
        ["REV-001", "Principal and independent genomic components was authored by Zhang/Yang/Zhao.", "The paper is by Oblong et al. (2024), DOI 10.1111/gbb.12876. The Gemini collective Zhang/Yang/Zhao attribution is unsupported by the current reviewer record.", "citation", "7,47", "manuscript reference 25", "reviewer action register", "oblong2024", "strong", "Zhang et al. 2023 is a different pleiotropy paper.", "Reviewer literature", "reject", "manual", "Retain exact individual papers only."],
    ]


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    REFERENCES.mkdir(parents=True, exist_ok=True)
    claims = claim_rows()
    write_tsv(
        EVIDENCE / "claim_evidence_register.tsv",
        ["claim_id", "original_wording", "proposed_safe_wording", "category", "manual_chapters", "software_evidence", "internal_evidence", "external_primary_citation", "evidence_strength", "limitation_or_counterpoint", "reviewer_relevance", "verification_status", "owner_action", "resolution_note"],
        claims,
    )

    correction_ids = {"PIPE-002", "SCORE-001", "SCORE-002", "INT-001", "INT-002", "INT-003", "CMP-001", "CMP-002", "REP-001", "REV-001"}
    correction_rows = [[row[0], row[1], row[2], row[9], row[6], row[7], row[11]] for row in claims if row[0] in correction_ids]
    write_tsv(
        EVIDENCE / "gemini_claim_correction_ledger.tsv",
        ["claim_id", "original_wording", "revised_wording", "reason_or_limitation", "internal_evidence", "external_evidence", "status"],
        correction_rows,
    )

    citation_rows = []
    for key, (citation, identifier, url) in SOURCES.items():
        citation_rows.append([key, citation, identifier, url, "primary paper" if identifier.startswith("10.") else "official documentation", "verified", "Supports bounded method description; does not establish DIMPLE-GWAS biological validity."])
    write_tsv(
        EVIDENCE / "citation_verification_log.tsv",
        ["citation_key", "verified_citation", "doi_or_identifier", "primary_url", "source_type", "status", "scope_note"],
        citation_rows,
    )

    chapter_map = [
        ["5-8", "conceptual foundations and boundaries", "umap2018; densmap2021; hdbscan2015; selective2024; oblong2024"],
        ["16-18", "UMAP/densMAP/repeated embeddings/HDBSCAN", "umap2018; densmap2021; hdbscan2015; hdbscan2017; umapdocs; hdbscandocs"],
        ["19-21", "metrics, score, and selection", "silhouette1987; dbcv2014; sklearnsilhouette"],
        ["24-31", "explainability and validation", "selective2024; umap2018; hdbscan2015"],
        ["7", "comparator matrix", "oblong2024; genomicsem2019; mtag2018; mostest2020; pleio2021; zhang2023"],
        ["35", "MNIST benchmark", "software/internal benchmark evidence only"],
        ["36", "historical 164-IDP case", "internal historical records; elliott2018 for UKB context"],
    ]
    write_tsv(EVIDENCE / "chapter_citation_map.tsv", ["chapters", "claim_scope", "citation_keys"], chapter_map)

    gaps = [
        ["CIT-GAP-001", "Exact Yang and Zhao works allegedly cited by reviewers", "No such named citations appear in the currently supplied Reviewer #2 action register.", "Do not attribute papers to the reviewer; retain as unresolved until exact correspondence is supplied.", "open"],
        ["CIT-GAP-002", "Formal theory for concatenating repeated UMAP embeddings", "No supplied or identified source proves that concatenated Euclidean distances equal an expected-distance estimator or recover true topology.", "Describe as empirical stability strategy only.", "bounded"],
        ["CIT-GAP-003", "Direct selective-inference procedure for the exact DIMPLE UMAP+HDBSCAN pipeline", "Gao et al. addresses hierarchical clustering, not this full selection pipeline.", "Use it to establish the general circularity problem; recommend held-out/independent validation.", "bounded"],
        ["CIT-GAP-004", "Biological validity of original-space correlations", "No method paper converts post-selection correlation summaries into causal evidence.", "Label summaries descriptive and conditional.", "bounded"],
    ]
    write_tsv(EVIDENCE / "evidence_gap_register.tsv", ["gap_id", "unresolved_item", "evidence_status", "manual_handling", "status"], gaps)

    reviewer = [
        ["Reviewer #2 major 1", "Position DIMPLE-GWAS as hypothesis-free phenotype grouping and complement to multivariate association/decomposition.", "mostest2020; genomicsem2019; oblong2024", "accepted and bounded", "Chapters 1, 7, 31"],
        ["Reviewer #2 major 2", "Do not equate modality alignment or noise status with biological distinctiveness.", "hofer2020; hdbscan2015", "accepted", "Chapters 28-30, 36"],
        ["Reviewer #2 major 3", "Use effect sizes/uncertainty rather than p-values alone for external validation.", "reviewer action register", "outside executable Stage 1 manual; principle included", "Chapters 29-31"],
        ["Reviewer #2 major 4", "Parameter guidance and complete tutorial.", "umapdocs; hdbscandocs", "implemented in draft", "Chapters 11-23, 32-44"],
        ["Reviewer #2 major 6", "Readable 2D figures and self-defining captions.", "reviewer action register", "applied to manual figures", "Chapters 27, 32-36"],
        ["Gemini reviewer crosswalk", "Attribution to Zhang/Yang/Zhao", "oblong2024; zhang2023", "partly rejected/unresolved", "Reviewer-method appendix"],
    ]
    write_tsv(EVIDENCE / "reviewer_reference_crosswalk.tsv", ["reviewer_point", "method_issue", "verified_sources", "resolution", "manual_location"], reviewer)

    comparator = [
        ["PCA", "linear variance decomposition", "matrix", "orthogonal continuous components and loadings", "linear", "none", "none intrinsic", "no", "high mathematical but not automatically biological", "compact global representation", "linear/global; component choice matters", "conceptual complement", "no"],
        ["ICA", "linear source separation", "matrix", "statistically independent components/mixing weights", "linear", "non-Gaussian independent-source model", "none intrinsic", "no", "potentially interpretable; not causal proof", "finds independent directions", "identifiability/stability and scaling choices", "conceptual complement", "no"],
        ["k-means", "centroid-based partition", "points x features", "K exhaustive clusters and centroids", "usually Euclidean", "centroid/within-sum-of-squares", "assigns all points", "yes", "centroids", "simple, fast", "K chosen a priori; poor match to some irregular density structures", "conceptual comparator", "no"],
        ["hierarchical clustering", "nested grouping", "features or distances", "dendrogram/flat cut", "depends", "linkage-dependent", "usually assigns all", "yes", "dendrogram/linkages", "multi-resolution view", "linkage and cut choice materially affect result", "conceptual comparator", "no"],
        ["Gaussian mixture", "probabilistic mixture modeling", "points x features", "component probabilities/parameters", "parametric", "mixture distribution, commonly Gaussian", "soft assignment; optional outlier model", "yes", "component parameters", "uncertainty-aware soft assignments", "distributional assumptions; component count/model selection", "conceptual comparator", "no"],
        ["UMAP", "nonlinear manifold embedding", "points x features", "latent coordinates", "nonlinear", "nearest-neighbor fuzzy topology", "no clustering/noise label", "no", "axes not inherently interpretable", "local neighborhood representation", "stochastic; parameter and metric dependent", "implemented embedding stage", "yes"],
        ["densMAP", "density-augmented UMAP", "points x features", "latent coordinates with density-correlation objective", "nonlinear", "UMAP plus density regularization", "no clustering/noise label", "no", "axes not inherently interpretable", "encourages local-density correspondence", "trade-off with base UMAP objective; no biological guarantee", "implemented when densmap=true", "yes"],
        ["HDBSCAN", "hierarchical density clustering", "points/embedding", "clusters, noise, persistence/probabilities", "nonlinear/nonparametric", "density and metric choices", "explicit -1 noise", "yes", "membership/persistence diagnostics", "arbitrary-shape density clusters and noise", "parameter/representation dependent", "implemented clustering stage", "yes"],
        ["DBCV", "internal density-based validation", "points + labels", "score in [-1,1]", "not a reducer", "density connectedness", "accounts for density/noise structure", "no", "diagnostic score", "aligned with density geometry", "not biological validation or universal best", "optional metric, not legacy score component", "yes"],
        ["MTAG", "trait-specific multi-trait GWAS", "GWAS summary statistics", "updated trait-specific associations", "linear statistical model", "shared effects/covariance assumptions", "not applicable", "no", "trait-specific effects", "power borrowing across traits", "assumptions and trait heterogeneity; different goal", "related downstream/alternative association method", "no"],
        ["PLEIO", "joint pleiotropic-locus test", "GWAS summary statistics", "one joint p-value per locus plus interpretation", "statistical test", "variance-component genetic covariance model", "not applicable", "no", "locus-pattern visualization", "models correlations, heritability, units", "not phenotype clustering; pleiotropy types not distinguished", "related multivariate association method", "no"],
        ["MOSTest", "multivariate omnibus association testing", "individual-level/permuted multivariate data", "omnibus SNP p-values", "statistical test", "distributed multivariate effects", "not applicable", "no", "limited directionality", "locus-discovery power", "different input/goal; not a cluster method", "complementary association method", "no"],
    ]
    write_tsv(EVIDENCE / "comparator_matrix.tsv", ["method", "purpose", "input", "output", "linear_or_nonlinear", "assumptions", "handling_of_noise", "discovers_clusters", "interpretability", "strengths", "limitations", "relationship_to_dimple", "implemented_in_freeze3"], comparator)

    bib = r'''@article{mcinnes2018umap,
  author = {McInnes, Leland and Healy, John and Saul, Nathaniel and Grossberger, Lukas},
  title = {UMAP: Uniform Manifold Approximation and Projection},
  journal = {Journal of Open Source Software}, year = {2018}, volume = {3}, number = {29}, pages = {861},
  doi = {10.21105/joss.00861}
}
@article{narayan2021densmap,
  author = {Narayan, Ashwin and Berger, Bonnie and Cho, Hyunghoon},
  title = {Assessing single-cell transcriptomic variability through density-preserving data visualization},
  journal = {Nature Biotechnology}, year = {2021}, volume = {39}, pages = {765--774}, doi = {10.1038/s41587-020-00801-7}
}
@article{campello2015hdbscan,
  author = {Campello, Ricardo J. G. B. and Moulavi, Davoud and Zimek, Arthur and Sander, Joerg},
  title = {Hierarchical Density Estimates for Data Clustering, Visualization, and Outlier Detection},
  journal = {ACM Transactions on Knowledge Discovery from Data}, year = {2015}, volume = {10}, number = {1}, pages = {5:1--5:51}, doi = {10.1145/2733381}
}
@article{mcinnes2017hdbscan,
  author = {McInnes, Leland and Healy, John and Astels, Steve}, title = {hdbscan: Hierarchical density based clustering},
  journal = {Journal of Open Source Software}, year = {2017}, volume = {2}, number = {11}, pages = {205}, doi = {10.21105/joss.00205}
}
@inproceedings{moulavi2014dbcv,
  author = {Moulavi, Davoud and Jaskowiak, Pablo A. and Campello, Ricardo J. G. B. and Zimek, Arthur and Sander, Joerg},
  title = {Density-Based Clustering Validation}, booktitle = {Proceedings of the 2014 SIAM International Conference on Data Mining},
  year = {2014}, pages = {839--847}, doi = {10.1137/1.9781611973440.96}
}
@article{rousseeuw1987silhouettes,
  author = {Rousseeuw, Peter J.}, title = {Silhouettes: A graphical aid to the interpretation and validation of cluster analysis},
  journal = {Journal of Computational and Applied Mathematics}, year = {1987}, volume = {20}, pages = {53--65}, doi = {10.1016/0377-0427(87)90125-7}
}
@article{gao2024selective,
  author = {Gao, Lucy L. and Bien, Jacob and Witten, Daniela}, title = {Selective Inference for Hierarchical Clustering},
  journal = {Journal of the American Statistical Association}, year = {2024}, volume = {119}, number = {545}, pages = {332--342}, doi = {10.1080/01621459.2022.2116331}
}
@article{oblong2024genomic,
  author = {Oblong, Lennart M. and Soheili-Nezhad, Sourena and Trevisan, Nicolo and Shi, Yingjie and Beckmann, Christian F. and Sprooten, Emma},
  title = {Principal and independent genomic components of brain structure and function}, journal = {Genes, Brain and Behavior}, year = {2024}, volume = {23}, number = {1}, pages = {e12876}, doi = {10.1111/gbb.12876}
}
@article{grotzinger2019genomicsem,
  author = {Grotzinger, Andrew D. and Rhemtulla, Mijke and de Vlaming, Ronald and others}, title = {Genomic structural equation modelling provides insights into the multivariate genetic architecture of complex traits},
  journal = {Nature Human Behaviour}, year = {2019}, volume = {3}, pages = {513--525}, doi = {10.1038/s41562-019-0566-x}
}
@article{turley2018mtag,
  author = {Turley, Patrick and Walters, Raymond K. and Maghzian, Omeed and others}, title = {Multi-trait analysis of genome-wide association summary statistics using MTAG},
  journal = {Nature Genetics}, year = {2018}, volume = {50}, pages = {229--237}, doi = {10.1038/s41588-017-0009-4}
}
@article{vandermeer2020mostest,
  author = {van der Meer, Dennis and Frei, Oleksandr and Kaufmann, Tobias and others}, title = {Understanding the genetic determinants of the brain with MOSTest},
  journal = {Nature Communications}, year = {2020}, volume = {11}, pages = {3512}, doi = {10.1038/s41467-020-17368-1}
}
@article{lee2021pleio,
  author = {Lee, Cue Hyunkyu and Shi, Huwenbo and Pasaniuc, Bogdan and Eskin, Eleazar and Han, Buhm}, title = {PLEIO: a method to map and interpret pleiotropic loci with GWAS summary statistics},
  journal = {The American Journal of Human Genetics}, year = {2021}, volume = {108}, pages = {36--48}, doi = {10.1016/j.ajhg.2020.11.017}
}
@article{zhang2023scalable,
  author = {Zhang, Zixuan and Jung, Junghyun and Kim, Artem and Suboc, Noah and Gazal, Steven and Mancuso, Nicholas}, title = {A scalable approach to characterize pleiotropy across thousands of human diseases and complex traits using GWAS summary statistics},
  journal = {The American Journal of Human Genetics}, year = {2023}, volume = {110}, pages = {1863--1874}, doi = {10.1016/j.ajhg.2023.09.015}
}
@article{hofer2020cortical,
  author = {Hofer, Edith and others}, title = {Genetic correlations and genome-wide associations of cortical structure in general population samples of 22,824 adults},
  journal = {Nature Communications}, year = {2020}, volume = {11}, doi = {10.1038/s41467-020-18367-y}
}
@article{elliott2018ukb,
  author = {Elliott, Lloyd T. and Sharp, Kevin and Alfaro-Almagro, Fidel and others}, title = {Genome-wide association studies of brain imaging phenotypes in UK Biobank},
  journal = {Nature}, year = {2018}, volume = {562}, pages = {210--216}, doi = {10.1038/s41586-018-0571-7}
}
'''
    (REFERENCES / "dimple_gwas_manual.bib").write_text(bib, encoding="utf-8")
    lines = ["# Verified bibliography", "", "This first-draft bibliography uses primary papers and official documentation. Each entry is bounded to the claim actually supported; none is treated as proof of DIMPLE-GWAS biological validity.", ""]
    for key, (citation, identifier, url) in SOURCES.items():
        lines.append(f"- **{key}:** [{citation}]({url}). Identifier: `{identifier}`.")
    lines.extend(["", "## Attribution correction", "", "*Principal and independent genomic components of brain structure and function* is by Oblong et al. (2024), DOI `10.1111/gbb.12876`. Zhang et al. (2023), DOI `10.1016/j.ajhg.2023.09.015`, is a separate pleiotropy-characterization paper. No exact Yang/Zhao reviewer-cited paper is identifiable in the supplied Reviewer #2 action register; those attributions remain unresolved rather than guessed.", ""])
    (REFERENCES / "VERIFIED_BIBLIOGRAPHY.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
