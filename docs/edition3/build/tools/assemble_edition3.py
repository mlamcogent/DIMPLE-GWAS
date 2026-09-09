from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "DIMPLE_GWAS_FREEZE3_RC1_DOCUMENTATION_EDITION3.md"
STATS = ROOT / "build" / "assembly_stats.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def part(title: str, intro: str) -> str:
    return f"# {title} {{.unnumbered}}\n\n{intro}\n\n\\newpage\n"


ordered: list[Path | tuple[str, str]] = [
    ROOT / "textbook/front_matter/00_title_and_status.md",
    ROOT / "textbook/front_matter/01_preface_and_reader_paths.md",
    ("Part I - Scientific problem and representation", "The first four chapters define the unit, geometry and representation questions before any density model is selected."),
    ROOT / "textbook/chapters/01_scientific_problem_and_pipeline.md",
    ROOT / "textbook/chapters/02_gwas_vectors_and_uncertain_geometry.md",
    ROOT / "textbook/chapters/03_geometry_preprocessing_and_rint.md",
    ROOT / "textbook/chapters/04_linear_and_nonlinear_views.md",
    ("Part II - Building the nonlinear representation", "These chapters open the UMAP/densMAP construction and the repeated-view strategy used by Freeze 3."),
    ROOT / "textbook/chapters/05_umap_from_graph_to_coordinates.md",
    ROOT / "textbook/chapters/06_densmap_and_relative_density.md",
    ROOT / "textbook/chapters/07_repeated_stochastic_embeddings.md",
    ("Part III - Discovering and selecting density structure", "The next three chapters move from the HDBSCAN hierarchy through complete search-space design to transparent model selection."),
    ROOT / "textbook/chapters/08_hdbscan_hierarchy_and_noise.md",
    ROOT / "textbook/chapters/09_searching_the_model_landscape.md",
    ROOT / "textbook/chapters/10_scoring_selection_and_optimism.md",
    ("Part IV - Interpretation and scientific practice", "The final textbook chapters separate artifact, structural, statistical and biological evidence, then position DIMPLE-GWAS among complementary multivariate genetic methods."),
    ROOT / "textbook/chapters/11_validation_stability_and_reproducibility.md",
    ROOT / "textbook/chapters/12_returning_to_original_space.md",
    ROOT / "textbook/chapters/13_from_topology_to_biological_claims.md",
    ROOT / "textbook/chapters/14_worked_cases_and_evidence_boundaries.md",
    ROOT / "textbook/chapters/15_dimple_in_multivariate_genetics.md",
    ("Part V - Analyst workbook", "The workbook converts the conceptual sequence into an evidence-labelled path from environment inspection to a pending manuscript-scale protocol."),
    ROOT / "workbook/learning_paths/README.md",
    ROOT / "workbook/labs/00_environment_and_cli.md",
    ROOT / "workbook/labs/01_input_orientation_and_contract.md",
    ROOT / "workbook/labs/02_hand_calculations.md",
    ROOT / "workbook/labs/03_fixed_synthetic_model.md",
    ROOT / "workbook/labs/04_small_search_and_ranking.md",
    ROOT / "workbook/labs/05_reproduce_and_compare.md",
    ROOT / "workbook/labs/06_original_space_explanation.md",
    ROOT / "workbook/labs/07_historical_164_reconstruction.md",
    ROOT / "workbook/labs/08_full_run_protocol.md",
    ROOT / "workbook/troubleshooting/README.md",
    ROOT / "workbook/exercises/SOLUTIONS.md",
    ("Part VI - Technical reference", "This lookup section records the current command, configuration, function, output, error and provenance contracts without interrupting the textbook narrative."),
    ROOT / "reference/cli/CLI_REFERENCE.md",
    ROOT / "reference/configuration/CONFIGURATION_REFERENCE.md",
    ROOT / "reference/function_atlas/FUNCTION_ATLAS.md",
    ROOT / "reference/output_atlas/OUTPUT_ATLAS.md",
    ROOT / "reference/errors/ERRORS_AND_RECOVERY.md",
    ROOT / "reference/provenance/PROVENANCE_AND_RELEASE.md",
    ROOT / "textbook/appendices/notation_and_glossary.md",
    ROOT / "textbook/appendices/evidence_and_claim_index.md",
]

chunks: list[str] = []
inputs: list[dict[str, object]] = []
for item in ordered:
    if isinstance(item, tuple):
        chunks.append(part(*item))
        continue
    if not item.is_file():
        raise FileNotFoundError(item)
    text = item.read_text(encoding="utf-8").strip() + "\n"
    chunks.append(text)
    inputs.append({"path": item.relative_to(ROOT).as_posix(), "bytes": item.stat().st_size, "sha256": sha256(item)})

OUT.write_text("\n\n".join(chunks).rstrip() + "\n", encoding="utf-8")
plain = OUT.read_text(encoding="utf-8")
word_count = len(plain.replace("`", " ").split())
heading_count = sum(1 for line in plain.splitlines() if line.startswith("#"))
figure_count = plain.count("![")
table_separator_count = sum(1 for line in plain.splitlines() if line.startswith("|---"))
stats = {
    "schema": "dimple-gwas.edition3-assembly.v1",
    "created_at_utc": datetime.now(timezone.utc).isoformat(),
    "master": OUT.name,
    "master_sha256": sha256(OUT),
    "source_file_count": len(inputs),
    "source_files": inputs,
    "approximate_whitespace_word_count": word_count,
    "markdown_heading_count": heading_count,
    "figure_reference_count": figure_count,
    "markdown_table_count": table_separator_count,
}
STATS.parent.mkdir(parents=True, exist_ok=True)
STATS.write_text(json.dumps(stats, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(stats, indent=2, sort_keys=True))
