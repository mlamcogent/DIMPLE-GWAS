#!/usr/bin/env python3
"""Build the complete package-defined callable atlas and traceability matrices."""

from __future__ import annotations

import ast
import csv
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


EDITION2 = Path(__file__).resolve().parents[2]
FREEZE3 = EDITION2.parents[2]
PACKAGE = FREEZE3 / "dimple_gwas"
TESTS = FREEZE3 / "tests"
ATLAS = EDITION2 / "function_atlas"
E1_EVIDENCE = FREEZE3 / "docs" / "manual" / "evidence"


@dataclass
class Symbol:
    source_path: str
    module: str
    symbol: str
    qualified_symbol: str
    kind: str
    parent: str
    line: int
    visibility: str
    signature: str
    return_annotation: str
    docstring: str
    node: ast.AST


def write_tsv(path: Path, header: list[str], rows: Iterable[Iterable[object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def visibility(name: str) -> str:
    if name.startswith("__") and name.endswith("__"):
        return "dunder"
    if name.startswith("_"):
        return "private"
    return "public_named"


def unparse(value: ast.AST | None) -> str:
    return ast.unparse(value) if value is not None else ""


def discover() -> list[Symbol]:
    symbols: list[Symbol] = []
    for path in sorted(PACKAGE.glob("*.py")):
        module = path.stem
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                symbols.append(Symbol(
                    path.relative_to(FREEZE3).as_posix(), module, node.name, f"{module}.{node.name}",
                    "class", "", node.lineno, visibility(node.name), "", "", ast.get_docstring(node) or "", node,
                ))
                for child in node.body:
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        symbols.append(Symbol(
                            path.relative_to(FREEZE3).as_posix(), module, child.name,
                            f"{module}.{node.name}.{child.name}", "method", node.name, child.lineno,
                            visibility(child.name), unparse(child.args), unparse(child.returns), ast.get_docstring(child) or "", child,
                        ))
                        collect_nested(symbols, path, module, child, f"{node.name}.{child.name}")
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                symbols.append(Symbol(
                    path.relative_to(FREEZE3).as_posix(), module, node.name, f"{module}.{node.name}",
                    "module_function", "", node.lineno, visibility(node.name), unparse(node.args),
                    unparse(node.returns), ast.get_docstring(node) or "", node,
                ))
                collect_nested(symbols, path, module, node, node.name)
    return symbols


def collect_nested(symbols: list[Symbol], path: Path, module: str, parent_node: ast.AST, parent_name: str) -> None:
    for child in getattr(parent_node, "body", []):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            symbols.append(Symbol(
                path.relative_to(FREEZE3).as_posix(), module, child.name,
                f"{module}.{parent_name}.<locals>.{child.name}", "nested_function", parent_name,
                child.lineno, "local", unparse(child.args), unparse(child.returns), ast.get_docstring(child) or "", child,
            ))
            collect_nested(symbols, path, module, child, f"{parent_name}.<locals>.{child.name}")
        elif isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try, ast.Match)):
            for nested_body_name in ("body", "orelse", "finalbody"):
                for nested in getattr(child, nested_body_name, []):
                    if isinstance(nested, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        symbols.append(Symbol(
                            path.relative_to(FREEZE3).as_posix(), module, nested.name,
                            f"{module}.{parent_name}.<locals>.{nested.name}", "nested_function", parent_name,
                            nested.lineno, "local", unparse(nested.args), unparse(nested.returns), ast.get_docstring(nested) or "", nested,
                        ))


TIER_A = {
    "cli.build_parser", "cli.main", "cli._inspect", "cli._show", "cli._score", "cli._summarize",
    "cli._reproduce", "cli._explain", "cli._compare", "cli._validate",
    "config.resolve_config", "config.validate_config", "config.normalized_parameter_space",
    "io.read_table", "io.validated_identifiers", "preprocessing.rank_inverse_normal_transform",
    "preprocessing.prepare_analysis_matrix", "preprocessing.prepare_explanation_matrix",
    "umap_runner.ensemble_seeds", "umap_runner.run_repeated_umap", "hdbscan_runner.fit_hdbscan",
    "metrics.embedding_quality_metrics", "metrics.evaluate_candidate", "search_space.count_candidates",
    "search_space.enumerate_candidates", "scoring.legacy_dimple_score", "scoring.custom_score",
    "scoring.apply_scoring", "ranking.rank_models", "ranking.pareto_front", "ranking.family_summaries",
    "pipeline.run_search", "reporting.write_model_outputs", "interpretation.compute_similarity",
    "interpretation.compute_order", "interpretation.coordinate_association_table",
    "interpretation.run_explanation", "comparison.run_comparison", "validation.run_validation",
    "visualization.render_heatmap", "provenance.base_manifest", "provenance.package_source_digest",
}


CHAPTER_BY_MODULE = {
    "cli": "13–17; Appendix A",
    "comparison": "12, 16, 21, 23",
    "config": "6, 10, 14; Appendix B",
    "hdbscan_runner": "9",
    "interpretation": "17, 21",
    "io": "6, 13–17",
    "metrics": "7, 9, 11",
    "pipeline": "8–12, 15",
    "preprocessing": "3, 6, 18",
    "provenance": "12, 15, 23, 24",
    "ranking": "11, 16, 20",
    "reporting": "12, 15; output atlas",
    "scoring": "11, 18, 20",
    "search_space": "10, 14, 20",
    "umap_runner": "7, 8",
    "validation": "12, 16, 21, 23",
    "visualization": "17, 21",
    "__main__": "13; Appendix A",
    "__init__": "13; front matter",
}


PURPOSES = {
    "cli.main": "Dispatch the command-line interface and return a process exit status.",
    "cli.build_parser": "Construct the complete user-facing command and flag grammar, including the interpret alias.",
    "pipeline.run_search": "Execute preprocessing, repeated embeddings, candidate evaluation, scoring, retention, reporting, and provenance for one run.",
    "preprocessing.rank_inverse_normal_transform": "Apply the implementation's rank-based inverse-normal transform to numeric analysis columns.",
    "preprocessing.prepare_analysis_matrix": "Validate the input contract, remove metadata, transform if requested, transpose, and return vector-by-variant analysis data.",
    "umap_runner.ensemble_seeds": "Generate the exact repeated-embedding seed sequence under current or legacy scheduling.",
    "umap_runner.run_repeated_umap": "Fit repeated UMAP/densMAP representations and concatenate their coordinates.",
    "hdbscan_runner.fit_hdbscan": "Fit contributed HDBSCAN with normalized Freeze 3 parameters.",
    "metrics.embedding_quality_metrics": "Calculate bounded trustworthiness and continuity diagnostics for an embedding.",
    "metrics.evaluate_candidate": "Compute cluster counts, persistence, silhouette, CH, DB, optional DBCV, and validity status for one candidate.",
    "search_space.enumerate_candidates": "Expand the declared UMAP-family and HDBSCAN Cartesian product into deterministically identified candidates.",
    "scoring.legacy_dimple_score": "Reproduce the compatibility score using observed dynamic-range weights and population-dependent normalization.",
    "scoring.custom_score": "Apply a user-declared multi-component scoring profile with orientations and weights.",
    "ranking.rank_models": "Apply deterministic eligibility, score, and tie ordering to candidate rows.",
    "reporting.write_model_outputs": "Write the complete candidate, ranking, selection, retained-model, compatibility, and manifest artifact family.",
    "interpretation.run_explanation": "Return to original input space, align IDs, calculate similarities/summaries, order a heatmap, and record a non-refitting explanation manifest.",
    "comparison.run_comparison": "Compare two label artifacts using exact IDs, permutation-invariant structure, noise sets, mapping, and optional coordinates.",
    "validation.run_validation": "Audit a run directory against required files, schemas, counts, identities, hashes, and manifest contracts.",
    "provenance.package_source_digest": "Compute a stable hash over package source files for non-Git source identity.",
    "visualization.render_heatmap": "Render static and interactive original-space similarity heatmaps with block-preserving sampling.",
}


OUTPUT_MAP = {
    "reporting.write_resolved_config": ["resolved_config.yaml"],
    "reporting.write_search_space": ["search_space_manifest.tsv", "search_space_manifest.json"],
    "reporting._top_artifact": ["labels.tsv", "summary.json", "reproduce.yaml"],
    "reporting.write_model_outputs": [
        "run_manifest.json", "models/all_models.tsv", "models/all_models.parquet", "models/ranked_models.tsv",
        "models/top_models.tsv", "models/best_model.json", "models/model_selection_manifest.json",
        "models/pareto_front.tsv", "models/family_summaries.tsv", "stage02_hdbscan_gridsearch_results.csv",
        "stage03_optimized_cluster_solutions.csv", "stage09_umap_vizdata_with_clusters.csv",
        "stage09b_umap_vizdata_with_annotations.csv",
    ],
    "pipeline.setup_logger": ["logs/run.log"],
    "interpretation.run_explanation": [
        "original_space_similarity.tsv.gz", "heatmap_order.tsv", "cluster_cutpoints.tsv", "cluster_summary.tsv",
        "projection_quality.tsv", "coordinate_associations.tsv", "exclusions.tsv", "original_space_heatmap.png",
        "original_space_heatmap.html", "interpretation_manifest.json", "README.md",
    ],
    "comparison.run_comparison": [
        "comparison_summary.json", "membership_comparison.tsv", "cluster_sizes.tsv", "label_confusion.tsv",
        "optimal_label_mapping.tsv", "comparison_manifest.json",
    ],
    "validation.run_validation": ["validation_checks.tsv", "validation_report.json", "validation_manifest.json"],
    "cli._score": ["rescored_table.tsv", "rescored_table.tsv.manifest.json"],
    "cli._summarize": ["family_summaries.tsv", "pareto_front.tsv", "top_models.tsv", "summary.json"],
    "visualization.render_heatmap": ["original_space_heatmap.png", "original_space_heatmap.html"],
}


EXAMPLES_BY_MODULE = {
    "config": "Lab 1 inspect-config/show-search-space",
    "search_space": "Labs 1–2 candidate enumeration",
    "preprocessing": "Lab 0 hand-worked matrix; Lab 1 executed fixture",
    "umap_runner": "Labs 1–2 repeated fixture representations",
    "hdbscan_runner": "Labs 1–2 candidate fitting",
    "metrics": "Lab 0 hand calculation; Lab 2 executed diagnostics",
    "scoring": "Lab 0 score table; Lab 2 executed ranking",
    "ranking": "Labs 0 and 2",
    "pipeline": "Labs 1–2",
    "reporting": "Labs 1–3 output walk-throughs",
    "interpretation": "Lab 3 explanation",
    "visualization": "Lab 3 heatmap",
    "comparison": "Labs 0 and 3",
    "validation": "Labs 1 and 3",
    "provenance": "All executed labs",
    "io": "Labs 0–3",
    "cli": "Labs 1–3",
}


def tier_for(symbol: Symbol) -> str:
    if symbol.qualified_symbol in TIER_A:
        return "A"
    if symbol.kind == "nested_function" or symbol.visibility in {"private", "local", "dunder"}:
        return "C"
    if symbol.kind in {"module_function", "class", "method"}:
        return "B"
    return "D"


def purpose(symbol: Symbol) -> str:
    if symbol.qualified_symbol in PURPOSES:
        return PURPOSES[symbol.qualified_symbol]
    if symbol.docstring:
        return re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", symbol.docstring.strip()))[0]
    words = symbol.symbol.strip("_").replace("_", " ")
    prefix = "Local helper for" if symbol.kind == "nested_function" else "Implementation callable for"
    return f"{prefix} {words}."


def calls_in(node: ast.AST) -> list[str]:
    values = []
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        if isinstance(child.func, ast.Name):
            values.append(child.func.id)
        elif isinstance(child.func, ast.Attribute):
            values.append(child.func.attr)
    return sorted(set(values))


def raises_in(node: ast.AST) -> str:
    values = []
    for child in ast.walk(node):
        if isinstance(child, ast.Raise) and child.exc is not None:
            exc = child.exc.func if isinstance(child.exc, ast.Call) else child.exc
            values.append(unparse(exc))
    return "; ".join(sorted(set(values))) or "No explicit raise in this symbol; delegated calls may raise."


def state_effects(symbol: Symbol, call_names: list[str]) -> str:
    source = ast.unparse(symbol.node)
    effects = []
    if any(token in source for token in ["write_text", "to_csv", "to_parquet", "mkdir", "atomic_json_dump", "savefig", "write_html"]):
        effects.append("writes files/directories")
    if any(token in call_names for token in ["logging", "getLogger", "info", "warning", "exception"]):
        effects.append("emits logs")
    if any(token in source for token in ["fit(", "fit_predict(", "UMAP(", "HDBSCAN("]):
        effects.append("fits numerical model")
    if not effects:
        effects.append("returns in-memory value; no direct file effect observed")
    return "; ".join(effects)


def test_mentions(symbol: Symbol) -> list[str]:
    pattern = re.compile(rf"\b{re.escape(symbol.symbol)}\b")
    matches = []
    for path in sorted(TESTS.glob("test_*.py")):
        text = path.read_text(encoding="utf-8")
        if pattern.search(text):
            for node in ast.parse(text).body:
                if isinstance(node, ast.FunctionDef) and node.name.startswith("test_") and pattern.search(ast.unparse(node)):
                    matches.append(f"{path.relative_to(FREEZE3).as_posix()}::{node.name}")
    return sorted(set(matches))


def main() -> None:
    ATLAS.mkdir(parents=True, exist_ok=True)
    symbols = discover()
    by_name: dict[str, list[str]] = defaultdict(list)
    for symbol in symbols:
        by_name[symbol.symbol].append(symbol.qualified_symbol)

    dependencies: dict[str, list[str]] = {}
    callers: dict[str, set[str]] = defaultdict(set)
    for symbol in symbols:
        resolved = []
        for called in calls_in(symbol.node):
            if len(by_name.get(called, [])) == 1:
                resolved.append(by_name[called][0])
            elif by_name.get(called):
                same_module = [value for value in by_name[called] if value.startswith(symbol.module + ".")]
                resolved.extend(same_module or by_name[called])
        resolved = sorted(set(value for value in resolved if value != symbol.qualified_symbol))
        dependencies[symbol.qualified_symbol] = resolved
        for value in resolved:
            callers[value].add(symbol.qualified_symbol)

    rows = []
    test_rows = []
    chapter_rows = []
    output_rows = []
    dossier_rows = []
    for symbol in symbols:
        tier = tier_for(symbol)
        tests = test_mentions(symbol)
        outputs = OUTPUT_MAP.get(symbol.qualified_symbol, [])
        chapter = CHAPTER_BY_MODULE.get(symbol.module, "Function atlas only")
        call_names = calls_in(symbol.node)
        rows.append([
            symbol.source_path, symbol.line, symbol.module, symbol.symbol, symbol.qualified_symbol, symbol.kind,
            symbol.parent, symbol.visibility, tier, purpose(symbol),
            "; ".join(sorted(callers.get(symbol.qualified_symbol, []))) or "CLI/import/direct caller or no package caller detected",
            "; ".join(dependencies[symbol.qualified_symbol]) or "No package-defined dependency detected",
            symbol.signature or "class construction/data container", symbol.return_annotation or "not annotated",
            raises_in(symbol.node), state_effects(symbol, call_names), "; ".join(tests) or "No direct symbol-name test reference; assess through caller/integration coverage",
            EXAMPLES_BY_MODULE.get(symbol.module, "Reference-only; caller examples"), chapter,
            "; ".join(outputs) or "No direct canonical artifact; in-memory/supporting result",
            "current implementation" if tier != "D" else "deprecated/unreachable",
        ])
        test_rows.append([symbol.qualified_symbol, tier, len(tests), "; ".join(tests), "direct name match plus integration mapping required where zero"])
        chapter_rows.append([symbol.qualified_symbol, tier, chapter, "full dossier" if tier == "A" else ("operational/statistical dossier" if tier == "B" else "atlas reference entry")])
        for output in outputs:
            output_rows.append([symbol.qualified_symbol, tier, output, "direct writer/producer", chapter])
        if tier in {"A", "B"}:
            for field_number, field in enumerate([
                "name_and_scientific_purpose", "workflow_position", "plain_language_intuition", "statistical_background",
                "mathematical_formulation", "assumptions_and_conditions", "implementation_traceability", "inputs_and_shapes",
                "parameters_and_defaults", "how_to_use", "hand_worked_example", "executed_example", "outputs",
                "result_interpretation", "diagnostics_and_validation", "failure_modes_and_recovery", "computational_behavior",
                "connections", "exercises_and_solutions", "evidence_and_further_reading",
            ], 1):
                dossier_rows.append([symbol.qualified_symbol, tier, field_number, field, chapter, "planned", "Must be completed before Gate C"])

    header = [
        "source_path", "source_line", "module", "symbol", "qualified_symbol", "kind", "parent", "visibility", "tier",
        "purpose", "callers", "package_dependencies", "input_signature", "return_annotation", "explicit_exceptions",
        "state_or_provenance_effects", "tests", "examples", "planned_chapter", "direct_outputs", "evidence_status",
    ]
    write_tsv(ATLAS / "function_inventory.tsv", header, rows)
    write_tsv(ATLAS / "function_to_test_matrix.tsv", ["qualified_symbol", "tier", "direct_test_count", "direct_tests", "coverage_note"], test_rows)
    write_tsv(ATLAS / "function_to_output_matrix.tsv", ["qualified_symbol", "tier", "artifact", "relationship", "planned_chapter"], output_rows)
    write_tsv(ATLAS / "function_to_chapter_matrix.tsv", ["qualified_symbol", "tier", "planned_chapter", "coverage_form"], chapter_rows)
    write_tsv(ATLAS / "function_dossier_coverage.tsv", ["qualified_symbol", "tier", "field_number", "required_field", "planned_chapter", "status", "note"], dossier_rows)

    counts = Counter(tier_for(symbol) for symbol in symbols)
    kinds = Counter(symbol.kind for symbol in symbols)
    command_graph = """# Command-to-function call graph

This graph is a teaching-level view derived from the current CLI dispatch and package call graph. The complete symbol-level inventory and dependencies are in `function_inventory.tsv`.

```mermaid
flowchart LR
  shell["dimple-gwas / python -m dimple_gwas"] --> main["cli.main"]
  main --> inspect["inspect-config → cli._inspect"]
  main --> show["show-search-space → cli._show"]
  main --> run["run → pipeline.run_search"]
  main --> score["score-existing → cli._score"]
  main --> summarize["summarize-models → cli._summarize"]
  main --> reproduce["reproduce-model → pipeline.run_search (fixed)"]
  main --> explain["explain / interpret → interpretation.run_explanation"]
  main --> compare["compare → comparison.run_comparison"]
  main --> validate["validate → validation.run_validation"]

  inspect --> config["resolve_config → validate_config"]
  show --> enumerate["enumerate_candidates → write_search_space"]
  run --> prep["prepare_analysis_matrix"]
  run --> enumerate
  run --> umap["run_repeated_umap"]
  run --> hdb["fit_hdbscan"]
  run --> metrics["evaluate_candidate"]
  run --> scoring["apply_scoring → rank_models"]
  run --> report["write_model_outputs"]
  explain --> similarity["compute_similarity / compute_order"]
  explain --> heatmap["render_heatmap"]
```

The `interpret` spelling is a compatibility alias for `explain`, not a separate analytical implementation. `reproduce-model` resolves a one-candidate fixed configuration and enters the same audited search pipeline; it is not an unrecorded shortcut.
"""
    (ATLAS / "command_to_function_call_graph.md").write_text(command_graph, encoding="utf-8")

    deprecated = """# Deprecated and unreachable callables

Static inspection of the current `dimple_gwas` package identified no package-defined Tier D callable. The user-facing `interpret` name is a supported compatibility alias for `explain`; it does not map to a second function. `legacy_dimple_score` is compatibility behavior but remains active and is not classified as deprecated. Historical Dev/Freeze 2 scripts outside the current package are migration evidence, not current package callables.

Nested local functions are retained in `function_inventory.tsv` as Tier C entries because they are executable callables inside current functions, but they are not public import targets and do not receive standalone textbook dossiers.
"""
    (ATLAS / "deprecated_and_unreachable_callables.md").write_text(deprecated, encoding="utf-8")

    report = f"""# Function atlas scope and Gate 1 report

The inventory denominator is **{len(symbols)} package-defined callable or callable-data symbols** across current `dimple_gwas/*.py` modules. It includes module functions, class definitions, class methods, and nested local functions; it excludes imported third-party callables and names merely referenced from dependencies.

| Classification | Count |
| --- | ---: |
| Tier A — user-facing/core analytical | {counts['A']} |
| Tier B — important supporting/public named | {counts['B']} |
| Tier C — private/local mechanical | {counts['C']} |
| Tier D — deprecated/unreachable | {counts['D']} |
| Module functions | {kinds['module_function']} |
| Classes | {kinds['class']} |
| Methods | {kinds['method']} |
| Nested local functions | {kinds['nested_function']} |

Every symbol has a source location, visibility, tier, purpose, caller/dependency mapping, signature, explicit-raise summary, state/output behavior, direct test-name matches, example route, planned chapter, and evidence status. Every Tier A/B symbol has a planned coverage form and a 20-field dossier checklist. Zero direct name matches in a test do not automatically mean untested: integration tests frequently reach private helpers through a public caller, and that distinction will be resolved during the final coverage audit.

Gate 1 status: **pass for discovery, classification, and planned coverage**. Gate C remains pending until every Tier A/B dossier field is completed and integration coverage is adjudicated.
"""
    (ATLAS / "README.md").write_text(report, encoding="utf-8")

    manifest_path = EDITION2 / "BOOK_BUILD_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["phase_status"]["phase_1_function_atlas"] = "complete_planning_gate"
    manifest["function_inventory"] = {
        "denominator": len(symbols),
        "tier_counts": dict(sorted(counts.items())),
        "kind_counts": dict(sorted(kinds.items())),
        "scope": "package-defined module functions, classes, methods, and nested local functions; imported third-party callables excluded",
        "gate_1": "pass",
        "gate_c_final_dossiers": "pending",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Function atlas: {len(symbols)} symbols; tiers {dict(counts)}")


if __name__ == "__main__":
    main()
