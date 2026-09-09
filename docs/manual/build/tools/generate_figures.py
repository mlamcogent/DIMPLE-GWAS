#!/usr/bin/env python3
"""Generate evidence-backed manual figures and editable Mermaid diagrams."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np
import pandas as pd


FREEZE3 = Path(__file__).resolve().parents[4]
MANUAL = FREEZE3 / "docs" / "manual"
TUTORIALS = MANUAL / "tutorials"
FIGURES = MANUAL / "assets" / "figures"
DIAGRAMS = MANUAL / "assets" / "diagrams"
EVIDENCE = MANUAL / "evidence"


BLUE = "#0072B2"
ORANGE = "#E69F00"
GREEN = "#009E73"
PINK = "#CC79A7"
GREY = "#6B7280"
RED = "#D55E00"
PALETTE = [BLUE, ORANGE, GREEN, PINK, RED, "#56B4E9"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def finish(fig, path: Path) -> None:
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def embedding_plot() -> tuple[Path, str]:
    source = TUTORIALS / "02_custom_search_space" / "run_20260825" / "stage09b_umap_vizdata_with_annotations.csv"
    frame = pd.read_csv(source)
    fig, ax = plt.subplots(figsize=(7.4, 5.2))
    for index, (label, group) in enumerate(frame.groupby("label", sort=True)):
        ax.scatter(group["UMAP_1"], group["UMAP_2"], s=55, color=PALETTE[index], edgecolor="black", linewidth=0.45, label=f"cluster {label}")
    ax.set(xlabel="UMAP display coordinate 1", ylabel="UMAP display coordinate 2", title="Selected synthetic partition (32-candidate tutorial)")
    ax.legend(frameon=False, ncol=3)
    ax.grid(alpha=0.18)
    ax.text(0.01, -0.18, "Display coordinates are descriptive; they are not biological loadings.", transform=ax.transAxes, fontsize=9)
    path = FIGURES / "figure_01_synthetic_embedding.png"
    finish(fig, path)
    return path, source.relative_to(FREEZE3).as_posix()


def score_plot() -> tuple[Path, str]:
    source = TUTORIALS / "02_custom_search_space" / "run_20260825" / "models" / "ranked_models.tsv"
    frame = pd.read_csv(source, sep="\t").sort_values("rank")
    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    colors = [PALETTE[int(v) % len(PALETTE)] for v in pd.Categorical(frame["umap_id"]).codes]
    ax.scatter(frame["rank"], frame["score"], c=colors, s=46, edgecolor="black", linewidth=0.35)
    ax.plot(frame["rank"], frame["score"], color=GREY, alpha=0.35, linewidth=1)
    ax.set(xlabel="Rank", ylabel="Normalized legacy_dimple score", title="Candidate ranks reflect four UMAP families")
    ax.set_ylim(-0.06, 1.06)
    ax.grid(alpha=0.18)
    ax.text(0.01, -0.20, "Ties are resolved by raw score, then model_id; score is conditional on this candidate population.", transform=ax.transAxes, fontsize=9)
    path = FIGURES / "figure_02_candidate_score_rank.png"
    finish(fig, path)
    return path, source.relative_to(FREEZE3).as_posix()


def similarity_plot() -> tuple[Path, str]:
    source = TUTORIALS / "03_explain_compare_validate" / "explanation_20260825" / "cluster_summary.tsv"
    frame = pd.read_csv(source, sep="\t")
    x = np.arange(len(frame))
    width = 0.36
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.bar(x - width / 2, frame["within_similarity_mean"], width, color=BLUE, label="within-cluster mean")
    ax.bar(x + width / 2, frame["between_similarity_mean"], width, color=ORANGE, label="between-cluster mean")
    ax.set_xticks(x, [f"cluster {v}" for v in frame["cluster_label"]])
    ax.set(ylabel="Pearson similarity", title="Original-space descriptive similarity")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.18)
    ax.text(0.01, -0.18, "Post-selection summary for a synthetic fixture; it is not an inferential test.", transform=ax.transAxes, fontsize=9)
    path = FIGURES / "figure_03_original_space_summary.png"
    finish(fig, path)
    return path, source.relative_to(FREEZE3).as_posix()


def comparison_plot() -> tuple[Path, str]:
    source = TUTORIALS / "03_explain_compare_validate" / "comparison_20260825" / "comparison_summary.json"
    payload = json.loads(source.read_text(encoding="utf-8"))
    labels = ["ARI", "NMI", "Noise\nJaccard", "Mapped\nmembership"]
    values = [payload["adjusted_rand_index"], payload["normalized_mutual_information"], payload["noise_set_jaccard"], payload["mapped_membership_match_fraction"]]
    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    bars = ax.bar(labels, values, color=[BLUE, GREEN, ORANGE, PINK], edgecolor="black", linewidth=0.45)
    ax.bar_label(bars, fmt="%.2f", padding=3)
    ax.set(ylim=(0, 1.12), ylabel="Concordance", title="Fixed-model reproduction agrees structurally")
    ax.grid(axis="y", alpha=0.18)
    ax.text(0.01, -0.19, f"24 IDs; Procrustes disparity = {payload['procrustes_disparity']:.3e}. Same environment and fixture.", transform=ax.transAxes, fontsize=9)
    path = FIGURES / "figure_04_partition_comparison.png"
    finish(fig, path)
    return path, source.relative_to(FREEZE3).as_posix()


def historical_status_plot() -> tuple[Path, str]:
    source = "freeze3_workspace reports 07/08 and authoritative historical label table"
    categories = ["Noise\n(-1)", "Cluster 0", "Cluster 1", "Cluster 2", "Cluster 3", "Cluster 4"]
    counts = [102, 9, 13, 15, 14, 11]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.3, 4.6), gridspec_kw={"width_ratios": [1.65, 1]})
    bars = ax1.bar(categories, counts, color=[GREY, *PALETTE[:5]], edgecolor="black", linewidth=0.4)
    ax1.bar_label(bars, padding=2)
    ax1.set(ylabel="Historical IDP count", title="Track A: historical assignments")
    ax1.tick_params(axis="x", rotation=25)
    ax1.grid(axis="y", alpha=0.18)
    ax2.axis("off")
    ax2.text(0.5, 0.66, "Track B", fontsize=16, weight="bold", ha="center")
    ax2.text(0.5, 0.48, "Fresh 1,000-seed run", fontsize=12, ha="center")
    ax2.text(0.5, 0.33, "PENDING DOCKER PHASE", fontsize=12, weight="bold", color=RED, ha="center")
    ax2.text(0.5, 0.12, "No fresh labels or metrics are claimed.", fontsize=9.5, ha="center")
    path = FIGURES / "figure_05_historical_idp_status.png"
    finish(fig, path)
    return path, source


DIAGRAM_TEXT = {
    "diagram_01_stage1_workflow.mmd": '''flowchart LR
  A["Variants × vectors input"] --> B["Drop declared metadata columns"]
  B --> C["Optional RINT"]
  C --> D["Transpose: vectors × variants"]
  D --> E["Repeated seeded UMAP / densMAP"]
  E --> F["Concatenated embedding"]
  F --> G["Enumerated HDBSCAN candidates"]
  G --> H["Metrics and declared score"]
  H --> I["Ranked and retained models"]
  I --> J["Explain / compare / validate"]
''',
    "diagram_02_input_orientation.mmd": '''flowchart TB
  A["Input rows: variants"] --> B["First N columns: metadata"]
  A --> C["Remaining columns: phenotype vectors / IDPs"]
  C --> D["Optional transform across analysis columns"]
  D --> E["Transpose"]
  E --> F["Analysis rows: vector IDs"]
  E --> G["Analysis columns: input variants"]
''',
    "diagram_03_config_precedence.mmd": '''flowchart LR
  A["Built-in search mode"] --> D["Deep merge"]
  B["YAML overlay"] --> D
  D --> E["Explicit CLI overrides"]
  E --> F["Validation"]
  F --> G["resolved_config.yaml"]
''',
    "diagram_04_repeated_embeddings.mmd": '''flowchart LR
  A["Prepared matrix"] --> U1["Seed s: UMAP d dims"]
  A --> U2["Seed s+1: UMAP d dims"]
  A --> UN["Seed s+n-1: UMAP d dims"]
  U1 --> C["Horizontal concatenation: d × n dims"]
  U2 --> C
  UN --> C
  C --> H["HDBSCAN metric space"]
''',
    "diagram_05_search_space.mmd": '''flowchart LR
  U["UMAP parameter Cartesian product"] --> X["×"]
  H["HDBSCAN parameter Cartesian product"] --> X
  X --> C["Complete deterministic candidates"]
  C --> S["Success"]
  C --> I["Invalid topology"]
  C --> F["Failure retained with error"]
''',
    "diagram_06_selection_reproduction.mmd": '''flowchart LR
  A["All candidate rows"] --> B["Eligibility + metrics"]
  B --> C["Declared score"]
  C --> D["Rank + tie order"]
  D --> E["best_model.json"]
  E --> F["reproduce-model fixed rerun"]
  F --> G["compare membership and coordinates"]
''',
    "diagram_07_original_space_explanation.mmd": '''flowchart LR
  L["Retained labels + exact feature_id"] --> M["Identifier match"]
  O["Original input matrix"] --> M
  M --> S["Original-space Pearson / Spearman"]
  S --> H["Order, cutpoints, heatmap, summaries"]
  H --> W["Descriptive only; no refit or causal inference"]
''',
    "diagram_08_compare_validate.mmd": '''flowchart LR
  A["Artifact A"] --> I["Exact ID set check"]
  B["Artifact B"] --> I
  I --> C["ARI / NMI / VI / noise Jaccard"]
  I --> P["Optional coordinate Procrustes"]
  R["Run directory"] --> V["Schema / count / hash validation"]
''',
    "diagram_09_provenance_lineage.mmd": '''flowchart TB
  S["Source SHA-256"] --> R["Run manifest"]
  I["Input SHA-256"] --> R
  C["Resolved config SHA-256"] --> R
  E["Environment + package versions"] --> R
  X["Command, seeds, threads, timestamps"] --> R
  R --> A["Artifact hashes"]
  A --> Q["Compare / validate / manual evidence"]
''',
    "diagram_10_validation_ladder.mmd": '''flowchart TB
  A["Software: tests, schemas, hashes"] --> B["Technical: rerun and artifact concordance"]
  B --> C["Statistical: stability, uncertainty, held-out analysis"]
  C --> D["Biological: independent data and domain evidence"]
  D --> E["Cross-platform: Docker, Linux, GCP, AWS"]
''',
}


def render_mermaid_flow(source: str, destination: Path) -> None:
    """Render the small manual flowcharts while retaining Mermaid as editable source."""
    lines = [line.strip() for line in source.splitlines() if line.strip()]
    orientation = "LR" if lines[0].endswith("LR") else "TB"
    labels: dict[str, str] = {}
    edges: list[tuple[str, str]] = []
    node_pattern = re.compile(r'([A-Za-z][A-Za-z0-9_]*)\["([^"]+)"\]')
    for line in lines[1:]:
        for node, label in node_pattern.findall(line):
            labels[node] = label
        if "-->" in line:
            left, right = line.split("-->", 1)
            left_id = re.match(r"([A-Za-z][A-Za-z0-9_]*)", left.strip()).group(1)
            right_id = re.match(r"([A-Za-z][A-Za-z0-9_]*)", right.strip()).group(1)
            edges.append((left_id, right_id))
    nodes = list(labels)
    incoming = {node: [] for node in nodes}
    outgoing = {node: [] for node in nodes}
    for left, right in edges:
        outgoing.setdefault(left, []).append(right)
        incoming.setdefault(right, []).append(left)
    layer = {node: 0 for node in nodes}
    for _ in range(len(nodes)):
        changed = False
        for left, right in edges:
            if layer[right] < layer[left] + 1:
                layer[right] = layer[left] + 1
                changed = True
        if not changed:
            break
    levels: dict[int, list[str]] = {}
    for node in nodes:
        levels.setdefault(layer[node], []).append(node)
    max_level = max(levels)
    max_across = max(len(value) for value in levels.values())
    if orientation == "LR":
        wrap = max_level >= 6 and all(len(members) == 1 for members in levels.values())
        fig, ax = plt.subplots(figsize=((11.5 if wrap else max(8.0, 2.35 * (max_level + 1))), (4.1 if wrap else max(3.0, 1.55 * max_across))))
        positions = {}
        for level, members in levels.items():
            for index, node in enumerate(members):
                if wrap:
                    row, column = divmod(level, 5)
                    snake_column = column if row % 2 == 0 else 4 - column
                    positions[node] = (snake_column * 2.2, -row * 1.35)
                else:
                    positions[node] = (level * 2.2, (len(members) - 1) / 2 - index)
        box_w, box_h = 1.62, 0.66
    else:
        fig, ax = plt.subplots(figsize=(max(7.0, 2.2 * max_across), max(4.4, 1.35 * (max_level + 1))))
        positions = {}
        for level, members in levels.items():
            for index, node in enumerate(members):
                positions[node] = (index - (len(members) - 1) / 2, -level * 1.25)
        box_w, box_h = 1.95, 0.7
    for left, right in edges:
        x1, y1 = positions[left]
        x2, y2 = positions[right]
        if orientation == "LR":
            if abs(x2 - x1) < 0.2:
                start, end = (x1, y1 - box_h / 2), (x2, y2 + box_h / 2)
            elif x2 > x1:
                start, end = (x1 + box_w / 2, y1), (x2 - box_w / 2, y2)
            else:
                start, end = (x1 - box_w / 2, y1), (x2 + box_w / 2, y2)
        else:
            start, end = (x1, y1 - box_h / 2), (x2, y2 + box_h / 2)
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=12, linewidth=1.3, color=GREY, connectionstyle="arc3,rad=0.0", zorder=1))
    for index, node in enumerate(nodes):
        x, y = positions[node]
        fill = "#E8F1F8" if index % 2 == 0 else "#FDF3DD"
        patch = FancyBboxPatch((x - box_w / 2, y - box_h / 2), box_w, box_h, boxstyle="round,pad=0.06,rounding_size=0.08", facecolor=fill, edgecolor="#25364A", linewidth=1.15, zorder=2)
        ax.add_patch(patch)
        ax.text(x, y, textwrap.fill(labels[node], width=22), ha="center", va="center", fontsize=8.7, color="#182635", zorder=3)
    xs = [value[0] for value in positions.values()]
    ys = [value[1] for value in positions.values()]
    ax.set_xlim(min(xs) - box_w, max(xs) + box_w)
    ax.set_ylim(min(ys) - box_h, max(ys) + box_h)
    ax.axis("off")
    fig.tight_layout(pad=0.2)
    fig.savefig(destination, bbox_inches="tight", facecolor="white")
    fig.savefig(destination.with_suffix(".png"), dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    DIAGRAMS.mkdir(parents=True, exist_ok=True)
    rows = []
    for number, generator in enumerate((embedding_plot, score_plot, similarity_plot, comparison_plot, historical_status_plot), start=1):
        path, source = generator()
        rows.append([f"FIG-{number:02d}", path.relative_to(MANUAL).as_posix(), source, sha256(path), "generated by docs/manual/build/tools/generate_figures.py", "3.0.0rc1", "synthetic/public or aggregate historical status", "verified quantitative figure"])
    source_heatmap = TUTORIALS / "03_explain_compare_validate" / "explanation_20260825" / "original_space_heatmap.png"
    copied_heatmap = FIGURES / "figure_06_original_space_heatmap.png"
    shutil.copy2(source_heatmap, copied_heatmap)
    rows.append(["FIG-06", copied_heatmap.relative_to(MANUAL).as_posix(), source_heatmap.relative_to(FREEZE3).as_posix(), sha256(copied_heatmap), "copied byte-for-byte from executed explain output", "3.0.0rc1", "synthetic fixture", "verified tutorial figure"])
    for name, text in DIAGRAM_TEXT.items():
        path = DIAGRAMS / name
        path.write_text(text, encoding="utf-8")
        rows.append([name.replace("diagram_", "DIA-").replace(".mmd", ""), path.relative_to(MANUAL).as_posix(), "implementation and evidence maps", sha256(path), "editable Mermaid source", "3.0.0rc1", "no data", "conceptual diagram grounded in source"])
        svg_path = path.with_suffix(".svg")
        render_mermaid_flow(text, svg_path)
        rows.append([name.replace("diagram_", "DIA-").replace(".mmd", "-render"), svg_path.relative_to(MANUAL).as_posix(), path.relative_to(FREEZE3).as_posix(), sha256(svg_path), "rendered by docs/manual/build/tools/generate_figures.py", "3.0.0rc1", "no data", "rendered conceptual diagram"])
    with (EVIDENCE / "figure_source_manifest.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(["figure_id", "manual_path", "source_artifact", "sha256", "generator", "software_version", "data_status", "evidence_status"])
        writer.writerows(rows)


if __name__ == "__main__":
    main()
