#!/usr/bin/env python3
"""Generate deterministic conceptual and quantitative figures for Textbook Edition 2."""

from __future__ import annotations

import csv
import html
import json
import os
import shutil
import textwrap
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/dimple_te2_matplotlib")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


EDITION2 = Path(__file__).resolve().parents[2]
ASSETS = EDITION2 / "assets" / "figures"
QA = EDITION2 / "qa"
LABS = EDITION2 / "labs"

NAVY = "#17324d"
BLUE = "#2f6f9f"
TEAL = "#2a9d8f"
GOLD = "#e9c46a"
CORAL = "#e76f51"
INK = "#1e2933"
MUTED = "#617181"
PALE = "#f3f7fa"
WHITE = "#ffffff"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def wrap(value: str, width: int = 20) -> list[str]:
    return textwrap.wrap(value, width=width, break_long_words=False) or [""]


def svg_document(title: str, subtitle: str, body: str, width: int = 1600, height: int = 900) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{esc(title)}</title><desc id="desc">{esc(subtitle)}</desc>
<defs><marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="{BLUE}"/></marker>
<filter id="shadow"><feDropShadow dx="0" dy="4" stdDeviation="5" flood-opacity="0.12"/></filter></defs>
<rect width="100%" height="100%" fill="{WHITE}"/>
<text x="80" y="82" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="700" fill="{NAVY}">{esc(title)}</text>
<text x="80" y="124" font-family="Arial, Helvetica, sans-serif" font-size="22" fill="{MUTED}">{esc(subtitle)}</text>
{body}
<text x="80" y="858" font-family="Arial, Helvetica, sans-serif" font-size="17" fill="{MUTED}">DIMPLE-GWAS Freeze 3 RC1 · Textbook Edition 2 · internal review</text>
</svg>'''


def box(x: int, y: int, w: int, h: int, title: str, detail: str = "", fill: str = PALE, stroke: str = BLUE) -> str:
    title_lines = wrap(title, max(12, int(w / 20)))
    detail_lines = wrap(detail, max(16, int(w / 15))) if detail else []
    chunks = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}" stroke="{stroke}" stroke-width="3" filter="url(#shadow)"/>']
    ty = y + 42
    for line in title_lines:
        chunks.append(f'<text x="{x+w/2}" y="{ty}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="25" font-weight="700" fill="{NAVY}">{esc(line)}</text>')
        ty += 30
    ty += 8
    for line in detail_lines:
        chunks.append(f'<text x="{x+w/2}" y="{ty}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="19" fill="{INK}">{esc(line)}</text>')
        ty += 25
    return "\n".join(chunks)


def arrow(x1: int, y1: int, x2: int, y2: int, label: str = "") -> str:
    out = [f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{BLUE}" stroke-width="4" marker-end="url(#arrow)"/>']
    if label:
        out.append(f'<text x="{(x1+x2)/2}" y="{(y1+y2)/2-12}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="18" fill="{MUTED}">{esc(label)}</text>')
    return "\n".join(out)


def pill(x: int, y: int, w: int, text: str, fill: str = TEAL) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="42" rx="21" fill="{fill}"/><text x="{x+w/2}" y="{y+28}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="700" fill="white">{esc(text)}</text>'


def conceptual_figures() -> list[dict[str, str]]:
    records: list[dict[str, str]] = []

    def save(fid: str, chapter: int, name: str, title: str, subtitle: str, body: str, caption: str, caution: str) -> None:
        path = ASSETS / f"{fid}_{name}.svg"
        path.write_text(svg_document(title, subtitle, body), encoding="utf-8")
        records.append({"figure_id": fid, "file": str(path.relative_to(EDITION2)), "kind": "conceptual diagram", "chapter": str(chapter), "source": "deterministic SVG from audited software and evidence maps", "caption": caption, "caution": caution})

    body = "".join([
        box(65, 250, 230, 180, "GWAS-derived matrix", "phenotype vectors × retained variants"),
        arrow(295, 340, 365, 340), box(365, 250, 230, 180, "Prepare", "validate · orient · optional RINT", fill="#eaf5f3", stroke=TEAL),
        arrow(595, 340, 665, 340), box(665, 250, 230, 180, "Represent", "seeded UMAP / densMAP families", fill="#fff7df", stroke="#c79a2b"),
        arrow(895, 340, 965, 340), box(965, 250, 230, 180, "Cluster & score", "HDBSCAN grid · diagnostics · rank", fill="#fff0ec", stroke=CORAL),
        arrow(1195, 340, 1265, 340), box(1265, 250, 270, 180, "Retain & explain", "artifacts · replay · compare · validate"),
        pill(530, 555, 540, "Every arrow is a checksummed provenance transition", NAVY),
    ])
    save("F01", 1, "pipeline_overview", "From scientific question to retained evidence", "The software pipeline is an evidence chain, not a single clustering call.", body, "The end-to-end route shares prepared inputs and representations before retaining candidates, selected-model artifacts, explanations, comparisons, and validation records.", "The chain establishes implemented behavior; it does not by itself establish biological validity.")

    body = "".join([
        box(110, 220, 520, 220, "Input table", "rows = variants · columns = phenotype identifiers", fill="#eaf5f3", stroke=TEAL),
        arrow(630, 330, 820, 330, "remove metadata · validate · transform · transpose"),
        box(820, 220, 650, 220, "Prepared analysis matrix", "rows = phenotype vectors · columns = retained variant dimensions", fill="#fff7df", stroke="#c79a2b"),
        pill(290, 540, 1020, "Cluster membership belongs to phenotype vectors, never to arbitrary row numbers", NAVY),
        box(430, 645, 740, 105, "Orientation test", "Identifier axis + numeric analysis axis + expected output identifiers must agree", fill="#fff0ec", stroke=CORAL),
    ])
    save("F02", 6, "input_orientation", "Input orientation changes the unit of analysis", "A safe workflow names both the source table and the post-transposition matrix.", body, "DIMPLE-GWAS validates a variant-by-phenotype table and constructs a phenotype-vector-by-variant analysis matrix for fitting.", "A transposition or identifier error changes what is clustered even when the numeric array remains rectangular.")

    body = "".join([
        box(100, 230, 350, 170, "Built-in mode", "standard · extended · fixed · custom"),
        arrow(450, 315, 620, 315), box(620, 230, 350, 170, "Merged YAML", "recursive overlay on mode defaults", fill="#eaf5f3", stroke=TEAL),
        arrow(970, 315, 1140, 315), box(1140, 230, 350, 170, "Explicit CLI", "highest-precedence values", fill="#fff7df", stroke="#c79a2b"),
        arrow(795, 400, 795, 550), box(515, 550, 560, 150, "Resolved configuration", "inspect-config records the method that will execute", fill="#fff0ec", stroke=CORAL),
        pill(500, 755, 590, "show-search-space fixes the candidate denominator", NAVY),
    ])
    save("F03", 14, "configuration_precedence", "Configuration is resolved in three layers", "The overlay file is not the executed method until precedence has been resolved.", body, "Built-in mode values are recursively merged with YAML and finally overridden by explicit command-line values.", "A valid configuration can still be scientifically unsuitable or computationally oversized.")

    body = "".join([
        box(80, 250, 300, 180, "Prepared vectors", "metric determines neighbor ordering"), arrow(380, 340, 500, 340),
        box(500, 250, 300, 180, "Local fuzzy graph", "ρ and σ calibrate directed memberships", fill="#eaf5f3", stroke=TEAL), arrow(800, 340, 920, 340),
        box(920, 250, 300, 180, "Stochastic layout", "cross-entropy balances attraction and repulsion", fill="#fff7df", stroke="#c79a2b"), arrow(1220, 340, 1340, 340),
        box(1340, 250, 190, 180, "Coordinates", "descriptive axes", fill="#fff0ec", stroke=CORAL),
        pill(450, 550, 700, "densMAP adds a density-regularization objective", TEAL),
        pill(335, 640, 930, "Neighborhood preservation ≠ preservation of all distances or biological pathways", NAVY),
    ])
    save("F04", 7, "umap_densmap_flow", "UMAP turns local relations into a stochastic representation", "The current package delegates graph construction and optimization to umap-learn.", body, "A metric and neighborhood scale create a locally calibrated fuzzy graph; stochastic optimization constructs coordinates, with densMAP optionally regularizing relative local density.", "Coordinate axes, gaps, and apparent density are not calibrated biological effects.")

    body = "".join([
        box(90, 205, 300, 130, "Seed 42", "p × q coordinates", fill="#eaf5f3", stroke=TEAL),
        box(90, 385, 300, 130, "Seed 43", "p × q coordinates", fill="#fff7df", stroke="#c79a2b"),
        box(90, 565, 300, 130, "Seed 44", "p × q coordinates", fill="#fff0ec", stroke=CORAL),
        arrow(390, 270, 700, 375), arrow(390, 450, 700, 420), arrow(390, 630, 700, 465),
        box(700, 300, 440, 240, "Raw horizontal concatenation", "p × (qS) analytical representation", fill="#edf2f8", stroke=BLUE),
        arrow(1140, 420, 1270, 420), box(1270, 320, 250, 200, "HDBSCAN", "distance sums contributions from every seeded layout"),
        pill(570, 660, 670, "No Procrustes alignment is performed before concatenation", NAVY),
    ])
    save("F05", 8, "repeated_embeddings", "Repeated seeded layouts create a concatenated geometry", "Each run contributes q coordinates; raw axis scale influences its distance contribution.", body, "DIMPLE-GWAS derives a seed schedule, fits one representation per seed, and concatenates the coordinate blocks horizontally for clustering.", "Repeats expose stochastic dependence but do not create an aligned consensus or independent replication.")

    body = "".join([
        box(90, 250, 310, 180, "Core distances", "local density scale from min_samples"), arrow(400, 340, 520, 340),
        box(520, 250, 310, 180, "Mutual reachability", "max(core_i, core_j, distance)", fill="#eaf5f3", stroke=TEAL), arrow(830, 340, 950, 340),
        box(950, 250, 310, 180, "Hierarchy", "minimum spanning tree · condensed tree", fill="#fff7df", stroke="#c79a2b"), arrow(1260, 340, 1380, 340),
        box(1380, 250, 150, 180, "Flat labels", "clusters + −1", fill="#fff0ec", stroke=CORAL),
        pill(430, 550, 740, "Stability selects branches; −1 means parameter-conditional unassignment", NAVY),
    ])
    save("F06", 9, "hdbscan_hierarchy", "HDBSCAN converts density into a hierarchy and a flat partition", "Noise is a retained analytical outcome, not a missing value.", body, "Core distances and mutual reachability define a density-sensitive hierarchy from which stable branches are selected as clusters.", "A label of −1 is not proof that a phenotype is scientifically anomalous.")

    body = "".join([
        box(85, 210, 310, 160, "UMAP family A", "neighbors 10 · min_dist 0.0"), box(85, 420, 310, 160, "UMAP family B", "neighbors 10 · min_dist 0.1", fill="#eaf5f3", stroke=TEAL),
        box(85, 630, 310, 120, "…", "other representation families", fill="#fff7df", stroke="#c79a2b"),
        arrow(395, 290, 690, 390), arrow(395, 500, 690, 430), arrow(395, 690, 690, 470),
        box(690, 285, 400, 250, "Shared representation cache", "one UMAP fit per family × seed schedule", fill="#edf2f8", stroke=BLUE),
        arrow(1090, 410, 1225, 295), arrow(1090, 410, 1225, 455), arrow(1090, 410, 1225, 615),
        box(1225, 225, 285, 130, "HDBSCAN setting 1", "candidate row"), box(1225, 390, 285, 130, "HDBSCAN setting 2", "candidate row", fill="#eaf5f3", stroke=TEAL), box(1225, 555, 285, 130, "HDBSCAN setting k", "candidate row", fill="#fff0ec", stroke=CORAL),
    ])
    save("F07", 10, "search_space_lifecycle", "A Cartesian grid creates auditable candidates", "Representation work is shared within a UMAP family; every HDBSCAN setting remains a distinct candidate.", body, "Search-space expansion defines UMAP families, reuses each family representation, and evaluates the Cartesian HDBSCAN settings into retained candidate rows.", "A deterministic denominator does not make an oversized or post hoc search scientifically appropriate.")

    body = "".join([
        box(70, 250, 260, 180, "Raw diagnostics", "silhouette · clusters · noise · DBCV · persistence"), arrow(330, 340, 450, 340),
        box(450, 250, 260, 180, "Score profile", "declared components and directions", fill="#eaf5f3", stroke=TEAL), arrow(710, 340, 830, 340),
        box(830, 250, 260, 180, "Population scaling", "score depends on candidate set", fill="#fff7df", stroke="#c79a2b"), arrow(1090, 340, 1210, 340),
        box(1210, 250, 320, 180, "Deterministic ranking", "tie-break rules · selected ID · replay", fill="#fff0ec", stroke=CORAL),
        pill(415, 555, 770, "legacy_dimple is a reproducible objective, not independent confirmation", NAVY),
    ])
    save("F08", 11, "scoring_ranking_replay", "Diagnostics become a ranking only through a declared objective", "Raw metrics, normalization population, tie rules, and analyst selection all belong in the report.", body, "Candidate diagnostics feed a named score profile; normalized values are population-relative before deterministic ranking and exact model replay.", "Rank 1 is conditional on the candidate population and objective, not a universal scientific optimum.")

    body = "".join([
        box(80, 240, 280, 190, "Checksummed input", "matrix · identifiers · annotations"), arrow(360, 335, 465, 335),
        box(465, 240, 280, 190, "Resolved method", "software · dependencies · config · seeds", fill="#eaf5f3", stroke=TEAL), arrow(745, 335, 850, 335),
        box(850, 240, 280, 190, "Candidate record", "model ID · metrics · status · failure", fill="#fff7df", stroke="#c79a2b"), arrow(1130, 335, 1235, 335),
        box(1235, 240, 285, 190, "Selected artifacts", "labels · summary · reproduce YAML · checksum", fill="#fff0ec", stroke=CORAL),
        arrow(1375, 430, 1375, 610), box(1000, 610, 520, 120, "Reproduction and comparison", "identifier alignment + partition + geometry checks", fill="#edf2f8", stroke=BLUE),
        pill(235, 610, 650, "Sanitized publication copy preserves identity without machine paths", NAVY),
    ])
    save("F09", 12, "provenance_lineage", "Reproduction begins with lineage, not with a plot", "Selected-model artifacts join input identity, resolved method, candidate identity, and replay instructions.", body, "A selected model is replayable only when checksummed inputs, resolved configuration, seeds, software identity, candidate ID, and retained artifacts form one lineage.", "Same-environment replay is technical evidence and does not guarantee cross-platform or biological equivalence.")

    body = "".join([
        box(80, 250, 300, 180, "Selected labels", "exact feature identifiers"), arrow(380, 340, 500, 340),
        box(500, 250, 300, 180, "Original-space matrix", "declared orientation · transformations", fill="#eaf5f3", stroke=TEAL), arrow(800, 340, 920, 340),
        box(920, 250, 300, 180, "Descriptive summaries", "Pearson · Spearman · ordering · cutpoints", fill="#fff7df", stroke="#c79a2b"), arrow(1220, 340, 1340, 340),
        box(1340, 250, 190, 180, "Heatmap", "read with sidecars", fill="#fff0ec", stroke=CORAL),
        pill(365, 555, 870, "Explanation conditions on labels selected from related data", NAVY),
    ])
    save("F10", 17, "original_space_explanation", "Explanation returns labels to the original variables", "Identifier integrity and selection awareness precede descriptive interpretation.", body, "The explanation route aligns selected labels with the original-space matrix before computing summaries, ordering, cutpoints, and a heatmap.", "The heatmap contains no post-selection p-values and cannot establish independent biological enrichment.")

    body = "".join([
        box(90, 230, 310, 190, "Left result", "identifiers · labels · optional coordinates"), box(90, 520, 310, 190, "Right result", "identifiers · labels · optional coordinates", fill="#eaf5f3", stroke=TEAL),
        arrow(400, 325, 700, 405), arrow(400, 615, 700, 465),
        box(700, 310, 430, 250, "Alignment and concordance", "ARI · NMI · VI · noise Jaccard · mapped membership · Procrustes", fill="#fff7df", stroke="#c79a2b"),
        arrow(1130, 435, 1260, 435), box(1260, 335, 260, 200, "Validation report", "schema · files · counts · checksums · contracts", fill="#fff0ec", stroke=CORAL),
        pill(510, 670, 730, "Numeric label equality is neither necessary nor sufficient", NAVY),
    ])
    save("F11", 21, "comparison_validation", "Comparison tests structure after identifier alignment", "Partition, noise, geometry, and artifact validity are separate questions.", body, "Two results are aligned by identifiers and compared with permutation-invariant partition metrics, noise overlap, mapped membership, and optional aligned geometry before artifact validation.", "Perfect same-environment fixture concordance is not evidence of external or biological validity.")

    levels = [
        ("1", "Software", "tests · schema · deterministic contracts", "#dbeaf5"),
        ("2", "Artifact", "completeness · checksums · identifiers", "#d9f0eb"),
        ("3", "Structural", "replay · partitions · sensitivity", "#fff1c9"),
        ("4", "Statistical", "uncertainty · selection · independent design", "#fbe0d8"),
        ("5", "Biological", "mechanism · enrichment · external coherence", "#eadff2"),
        ("6", "Cross-platform & external", "Docker/Linux/cloud · new cohorts", "#dfe5eb"),
    ]
    body_parts = []
    for idx, (num, title, detail, color) in enumerate(levels):
        x = 155 + idx * 220
        y = 650 - idx * 78
        body_parts.append(box(x, y, 205, 150, f"{num}. {title}", detail, fill=color, stroke=NAVY))
        if idx:
            body_parts.append(arrow(x - 15, y + 75, x, y + 75))
    body_parts.append(pill(410, 755, 780, "Evidence does not automatically rise from one layer to the next", NAVY))
    save("F12", 23, "validation_ladder", "Validation is layered and claim-specific", "Each rung requires evidence appropriate to that claim; lower layers remain necessary but insufficient.", "".join(body_parts), "The validation ladder separates software, artifact, structural, statistical, biological, and cross-platform/external evidence.", "A successful lower layer never substitutes for an untested higher layer.")
    return records


def quantitative_figures() -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    plt.rcParams.update({"figure.dpi": 160, "font.size": 11, "axes.titlesize": 16, "axes.labelsize": 12, "axes.edgecolor": NAVY, "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})

    def savefig(fid: str, chapter: int, name: str, caption: str, caution: str, source: str) -> None:
        path = ASSETS / f"{fid}_{name}.png"
        plt.tight_layout()
        plt.savefig(path, bbox_inches="tight", facecolor="white")
        plt.close()
        records.append({"figure_id": fid, "file": str(path.relative_to(EDITION2)), "kind": "quantitative figure", "chapter": str(chapter), "source": source, "caption": caption, "caution": caution})

    fixed = pd.read_csv(LABS / "01_fixed_synthetic/run_20260826/stage09_umap_vizdata_with_clusters.csv")
    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    colors = {0: TEAL, 1: BLUE, 2: CORAL, -1: MUTED}
    for label, group in fixed.groupby("label"):
        ax.scatter(group["UMAP_1"], group["UMAP_2"], s=95, color=colors.get(int(label), GOLD), edgecolor="white", linewidth=0.8, label=f"label {label}")
        for _, row in group.iterrows():
            ax.annotate(str(row["feature_id"]).replace("trait_", ""), (row["UMAP_1"], row["UMAP_2"]), xytext=(4, 4), textcoords="offset points", fontsize=7, color=MUTED)
    ax.set_title("Fresh fixed-fixture display embedding")
    ax.set_xlabel("UMAP display coordinate 1")
    ax.set_ylabel("UMAP display coordinate 2")
    ax.grid(alpha=0.18)
    ax.legend(frameon=False, title="HDBSCAN")
    savefig("F13", 19, "fixed_fixture_embedding", "The fresh fixed fixture produced three designed groups of eight with no noise assignment in the first-run display coordinates.", "Coordinate axes and visual separation are fixture-specific and carry no pathway or significance interpretation.", "Fresh Lab 1 stage09_umap_vizdata_with_clusters.csv")

    ranked = pd.read_csv(LABS / "02_custom_search_space/run_20260826/models/ranked_models.tsv", sep="\t")
    ranked = ranked.sort_values("rank")
    fig, ax = plt.subplots(figsize=(11.5, 6.2))
    ax.scatter(ranked["rank"], ranked["score"], c=ranked["umap_n_neighbors"], cmap="viridis", s=70, edgecolor="white", linewidth=0.5)
    ax.axvline(8.5, color=CORAL, linestyle="--", linewidth=1.5, label="eight tied top scores")
    ax.set_title("Lab 2 candidate rank and population-relative score")
    ax.set_xlabel("Deterministic rank")
    ax.set_ylabel("legacy_dimple score")
    ax.set_xlim(0, len(ranked) + 1)
    ax.grid(alpha=0.18)
    ax.legend(frameon=False)
    savefig("F14", 20, "custom_search_ranking", "All 32 bounded-search candidates completed; the leading score was shared by eight rows and deterministic tie rules selected one model ID.", "The score changes with its candidate population and is not an independent validation statistic.", "Fresh Lab 2 ranked_models.tsv")

    metrics = ["trustworthiness", "continuity", "silhouette", "dbcv", "hdbscan_persistence_mean"]
    vals = [float(ranked.iloc[0][m]) for m in metrics]
    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    labels = ["Trustworthiness", "Continuity", "Silhouette", "DBCV", "Mean persistence"]
    bars = ax.barh(labels, vals, color=[BLUE, TEAL, GOLD, CORAL, NAVY])
    ax.set_xlim(0, 1.05)
    ax.set_title("Selected Lab 2 candidate diagnostics")
    ax.set_xlabel("Recorded value")
    ax.bar_label(bars, fmt="%.3f", padding=4)
    ax.grid(axis="x", alpha=0.18)
    savefig("F15", 20, "selected_candidate_diagnostics", "The selected bounded-search candidate has five separately interpreted diagnostics; no single bar certifies a correct cluster solution.", "Values are calculated on a designed fixture and are partly dependent on the same representation used for fitting.", "Fresh Lab 2 ranked_models.tsv, rank 1")

    comparison = json.loads((LABS / "03_explain_compare_validate/safe_artifacts/comparison_summary.json").read_text(encoding="utf-8"))
    metric_keys = ["adjusted_rand_index", "normalized_mutual_information", "noise_set_jaccard", "mapped_membership_match_fraction"]
    def find_value(obj, key):
        if isinstance(obj, dict):
            if key in obj: return obj[key]
            for value in obj.values():
                found = find_value(value, key)
                if found is not None: return found
        return None
    comp_vals = [float(find_value(comparison, key) or 0) for key in metric_keys]
    fig, ax = plt.subplots(figsize=(10.5, 5.5))
    bars = ax.bar(["ARI", "NMI", "Noise Jaccard", "Mapped membership"], comp_vals, color=[BLUE, TEAL, GOLD, CORAL])
    ax.set_ylim(0, 1.20)
    ax.set_title("Fresh same-environment reproduction concordance")
    ax.set_ylabel("Agreement")
    ax.bar_label(bars, fmt="%.3f", padding=2)
    ax.grid(axis="y", alpha=0.18)
    savefig("F16", 21, "reproduction_concordance", "The fixed fixture and its fresh reproduction agree exactly on four partition and noise metrics; variation of information was 0 and Procrustes disparity was approximately 2.7×10⁻³¹.", "This is same-environment technical concordance, not a cross-platform or biological result.", "Fresh Lab 3 sanitized comparison summary")

    similarity = pd.read_csv(LABS / "03_explain_compare_validate/explanation_20260826/original_space_similarity.tsv.gz", sep="\t", index_col=0)
    short_labels = [value.replace("trait_", "") for value in similarity.index]
    fig, ax = plt.subplots(figsize=(10.5, 9.2))
    image = ax.imshow(similarity.to_numpy(), cmap="coolwarm", vmin=-1, vmax=1, interpolation="nearest")
    ax.set_xticks(np.arange(len(short_labels)), labels=short_labels, rotation=90, fontsize=7)
    ax.set_yticks(np.arange(len(short_labels)), labels=short_labels, fontsize=7)
    for cut in (7.5, 15.5):
        ax.axhline(cut, color=INK, linewidth=1.8)
        ax.axvline(cut, color=INK, linewidth=1.8)
    ax.set_title("Fresh Lab 3 original-space Pearson similarity")
    ax.set_xlabel("Ordered phenotype vector")
    ax.set_ylabel("Ordered phenotype vector")
    cbar = fig.colorbar(image, ax=ax, fraction=0.045, pad=0.03)
    cbar.set_label("Pearson similarity")
    heatmap_target = ASSETS / "F17_original_space_heatmap.png"
    plt.tight_layout()
    plt.savefig(heatmap_target, bbox_inches="tight", facecolor="white")
    plt.close()
    records.append({"figure_id": "F17", "file": str(heatmap_target.relative_to(EDITION2)), "kind": "quantitative figure", "chapter": "17", "source": "Fresh Lab 3 original_space_heatmap.png", "caption": "The fresh explanation route orders the original-space similarity matrix by retained labels and writes sidecars for the order and cluster cutpoints.", "caution": "The display is descriptive and conditional on the selected labels; it supplies no independent post-selection p-values."})

    statuses = ["Fresh tests", "Labs 0–3", "Output atlas", "MNIST protocol", "Historical 164 IDPs", "Fresh 164-IDP run", "Docker/cloud"]
    values = [1.0, 1.0, 34 / 35, 0.5, 0.5, 0.0, 0.0]
    colors = [TEAL, TEAL, TEAL, GOLD, GOLD, CORAL, CORAL]
    fig, ax = plt.subplots(figsize=(11.5, 6.2))
    bars = ax.barh(statuses[::-1], values[::-1], color=colors[::-1])
    ax.set_xlim(0, 1.05)
    ax.set_title("Edition 2 evidence status at assembly")
    ax.set_xlabel("Completion within the declared documentation scope")
    ax.grid(axis="x", alpha=0.18)
    for bar, value in zip(bars, values[::-1]):
        label = "complete" if value == 1 else ("pending" if value == 0 else "bounded / historical")
        ax.text(min(value + 0.02, 0.88), bar.get_y() + bar.get_height()/2, label, va="center", fontsize=10)
    savefig("F18", 22, "evidence_status", "Fresh bounded software evidence is complete for tests and Labs 0–3; the original 164-IDP run and Docker/cloud validation remain explicitly pending.", "Bars show documentation-scope status, not a scientific-quality score.", "Edition 2 execution manifest and release-status matrix")

    raw_toy = pd.read_csv(LABS / "00_hand_worked_toy/toy_variants_by_vectors.tsv", sep="\t")
    rint_toy = pd.read_csv(LABS / "00_hand_worked_toy/executed_output/rint_vectors_by_variants.tsv", sep="\t", index_col=0)
    vector_names = ["V_A", "V_B", "V_C", "V_D"]
    palette = [BLUE, TEAL, CORAL, GOLD]
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.5), sharex=True)
    variant_index = np.arange(1, 7)
    for name, color in zip(vector_names, palette):
        axes[0].plot(variant_index, raw_toy[name], marker="o", linewidth=2, color=color, label=name)
        axes[1].plot(variant_index, rint_toy.loc[name].to_numpy(dtype=float), marker="o", linewidth=2, color=color, label=name)
    axes[0].set_title("Raw teaching values")
    axes[1].set_title("Implemented column-wise RINT")
    for ax in axes:
        ax.set_xlabel("Variant row")
        ax.grid(alpha=0.2)
    axes[0].set_ylabel("Value")
    axes[1].set_ylabel("Normal score")
    axes[1].legend(frameon=False, ncol=2)
    fig.suptitle("Lab 0 transformation changes marginal scale and vector geometry", fontsize=16, color=INK)
    savefig("F19", 3, "rint_transformation", "The hand-worked fixture shows the same four vectors before and after the implemented average-rank inverse-normal transformation; ties share scores and ordering remains column-specific.", "RINT changes geometry but does not remove dependence, uncertainty, confounding, or selection.", "Fresh Lab 0 toy input and rint_vectors_by_variants.tsv")

    matrix = rint_toy.to_numpy(dtype=float)
    distances = np.linalg.norm(matrix[:, None, :] - matrix[None, :, :], axis=2)
    fig, ax = plt.subplots(figsize=(7.5, 6.6))
    image = ax.imshow(distances, cmap="Blues", vmin=0)
    ax.set_xticks(np.arange(4), labels=vector_names)
    ax.set_yticks(np.arange(4), labels=vector_names)
    ax.set_title("Lab 0 Euclidean distances after RINT")
    for i in range(4):
        for j in range(4):
            ax.text(j, i, f"{distances[i,j]:.3f}", ha="center", va="center", color="white" if distances[i,j] > distances.max()/2 else INK, fontweight="bold")
    cbar = fig.colorbar(image, ax=ax, fraction=0.05, pad=0.04)
    cbar.set_label("Euclidean distance")
    savefig("F20", 3, "toy_distance_matrix", "The post-RINT distance matrix makes the nearest-pair relation explicit: V_A and V_B are separated by 0.329, whereas V_A and V_C are separated by 4.334.", "Distances are conditional on orientation, transformation, metric, and the six designed variant rows.", "Fresh Lab 0 rint_vectors_by_variants.tsv")

    labels_fixed = pd.read_csv(LABS / "01_fixed_synthetic/run_20260826/models/top_model_artifacts/model_060fac0208bb58e2/labels.tsv", sep="\t")
    labels_custom = pd.read_csv(LABS / "02_custom_search_space/run_20260826/models/top_model_artifacts/model_241ad5e99af55074/labels.tsv", sep="\t")
    categories = ["cluster 0", "cluster 1", "cluster 2", "noise −1"]
    counts = []
    for frame in (labels_fixed, labels_custom):
        value_counts = frame["label"].value_counts()
        counts.append([int(value_counts.get(label, 0)) for label in (0, 1, 2, -1)])
    x = np.arange(len(categories)); width = 0.35
    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    bars1 = ax.bar(x - width/2, counts[0], width, label="Lab 1 fixed", color=BLUE)
    bars2 = ax.bar(x + width/2, counts[1], width, label="Lab 2 selected", color=TEAL)
    ax.set_xticks(x, categories)
    ax.set_ylim(0, 10)
    ax.set_ylabel("Phenotype-vector count")
    ax.set_title("Selected fixture cluster sizes and noise counts")
    ax.bar_label(bars1, padding=3)
    ax.bar_label(bars2, padding=3)
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.2)
    savefig("F21", 19, "cluster_size_noise_summary", "The fresh fixed run and the selected bounded-search model each retained three clusters of eight phenotype vectors and zero noise assignments.", "The equality reflects a designed fixture and does not predict production cluster balance or absence of unassigned IDPs.", "Fresh Lab 1 and Lab 2 selected labels.tsv files")
    return records


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    records = conceptual_figures() + quantitative_figures()
    fields = ["figure_id", "file", "kind", "chapter", "source", "caption", "caution"]
    with (QA / "figure_inventory.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader(); writer.writerows(records)
    with (QA / "figure_visual_qa.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["figure_id", "file", "opened", "legible", "no_overlap", "caption_bounded", "review_note"], delimiter="\t")
        writer.writeheader()
        for row in records:
            writer.writerow({"figure_id": row["figure_id"], "file": row["file"], "opened": "pending", "legible": "pending", "no_overlap": "pending", "caption_bounded": "yes", "review_note": "source generated; visual inspection pending"})
    print(f"Generated {len(records)} figures in {ASSETS}")


if __name__ == "__main__":
    main()
