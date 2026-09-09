#!/usr/bin/env python3
"""Draft the 23 non-calibration TE2 chapters from audited, mapped evidence."""

from __future__ import annotations

import csv
import re
from pathlib import Path


EDITION2=Path(__file__).resolve().parents[2]
FREEZE3=EDITION2.parents[2]
OLD=FREEZE3/"docs/manual/chapters"
CHAPTERS=EDITION2/"chapters"


# number, title, prerequisites, question, central tension, evidence boundary,
# Edition 1 chapters, concepts, modules, worked-example prompt, transition
SPECS=[
(1,"The scientific problem, scope, and evidence boundary","none","What can Stage 1 learn from a collection of GWAS-derived phenotype vectors, and what remains outside its reach?","Exploratory structure is scientifically useful only when the unit of analysis and the validation layer remain explicit.","The present evidence establishes local software behavior and bounded fixtures; it does not establish causal pathways, biological truth, or cross-platform equivalence.",[1,2,3,46],["C01","C34","C35"],["cli","pipeline","provenance"],"Classify ten proposed conclusions as implemented behavior, statistical explanation, historical evidence, or unsupported biological inference.","Chapter 2 turns the unit-of-analysis boundary into matrix notation and geometry."),
(2,"GWAS-derived phenotype vectors and high-dimensional geometry","1","How does a table of association summaries become a geometry among phenotypes?","A vector can carry shared biological signal and shared technical or sampling structure at the same time.","DIMPLE-GWAS receives upstream summaries; it does not estimate LD, correct sample overlap, or rerun the contributing GWAS.",[2,4,5],["C01","C02","C03","C06"],["preprocessing","io"],"Use three five-variant vectors to calculate two distances, then identify how a shared scale factor and one outlying variant alter the ordering.","Chapter 3 makes the metric, scaling, and transformation choices explicit."),
(3,"Similarity, distance, scaling, transformation, and uncertainty","2","Which transformations and metrics make two phenotype vectors look close?","Geometry is chosen, not discovered in a parameter-free form; transformation can stabilize a marginal distribution while changing neighbors.","RINT and similarity are implemented precisely, but neither removes LD, measurement error, sample overlap, or post-selection dependence.",[5,15,26],["C03","C04","C05","C31","C32"],["preprocessing","interpretation","metrics"],"Rank a tied six-value column by hand, apply (rank−0.5)/n, and compare Euclidean and correlation-based conclusions.","Chapter 4 asks why and how a nonlinear representation is introduced."),
(4,"Dimension reduction: linear and nonlinear perspectives","2–3","What is gained and lost when a high-dimensional relationship is represented with fewer coordinates?","A low-dimensional display can clarify neighborhoods while obscuring global scale, uncertainty, and coordinate identity.","Freeze 3 has no user-visible PCA, SVD, or ICA pre-reducer; comparator methods answer different questions and are not implemented stages.",[6,7,24],["C06","C07","C08","C10"],["umap_runner","metrics"],"Project a centered three-variable toy matrix onto one stated linear direction, then contrast that operation with neighborhood preservation.","Chapter 5 introduces the density and validation problems that arise after representation."),
(5,"Density clustering, validation, and circular inference","3–4","When does a dense region justify a cluster, and what evidence can validate it?","Internal diagnostics are computed on the same representation used to construct candidates, so they guide selection without becoming independent confirmation.","HDBSCAN labels are algorithmic; post-selection summaries are descriptive unless a valid independent or selective-inference design is supplied.",[8,18,19,28,29,30],["C14","C15","C16","C17","C20","C23","C33","C34"],["hdbscan_runner","metrics","interpretation","validation"],"Draw a five-point mutual-reachability graph, identify an unassigned point, and separate internal, structural, and external validation claims.","Chapter 6 returns to the exact data contract before the method is derived."),
(6,"Data contract, preprocessing, RINT, and orientation","2–3","Which cells become the vectors that UMAP actually sees?","Row and column language changes after transposition; an apparently small orientation mistake changes the unit being clustered.","Production `run` rejects missing or nonnumeric analysis cells; explanation mode supports two explicit orientations with identifier-based inference safeguards.",[10,15],["C01","C02","C04","C05"],["preprocessing","io","config"],"Follow the Lab 0 six-by-eight table through metadata removal, average-rank RINT, transpose, and its final four-by-six analysis matrix.","Chapter 7 derives the UMAP/densMAP representation built from that matrix."),
(8,"Repeated stochastic embeddings and concatenated geometry","7","Why fit more than one seeded layout, and what geometry results from concatenating them?","Repeats expose and aggregate stochastic layouts, but raw concatenation does not align coordinate axes or prove consensus.","Freeze 3 records seed schedules and returns a raw horizontal concatenation; it does not persist per-seed or full concatenated arrays as files.",[6,17],["C10","C12","C13","C35"],["umap_runner","provenance"],"Prove the squared-distance sum identity for two two-dimensional runs, then rescale one run and recalculate its contribution.","Chapter 9 places density clustering on the concatenated representation."),
(9,"HDBSCAN hierarchy, density, selection, and noise","5,8","How does HDBSCAN turn local density into a hierarchy and a flat partition?","A stable density branch can be useful without making every point belong to a cluster.","Freeze 3 delegates fitting to the contributed `hdbscan` package and records outputs; label −1 remains parameter-conditional unassignment.",[18,28],["C14","C15","C16","C17"],["hdbscan_runner","metrics"],"Calculate core distances and mutual reachability for a six-point line, then predict how raising `min_samples` changes the density scale.","Chapter 10 converts UMAP and HDBSCAN parameter families into auditable candidates."),
(10,"Search-space enumeration and computational design","8–9","How many models will a configuration request, and which work is shared across them?","A Cartesian grid is transparent but can grow faster than intuition; deterministic enumeration does not make an oversized run wise.","The standard HDBSCAN grid is 2,430 candidates for one UMAP configuration; custom and extended modes have different, exactly enumerated counts.",[12,17,39,44],["C12","C18","C19"],["search_space","config","pipeline"],"Calculate the 32 candidates in Lab 2, separate four UMAP families from eight HDBSCAN settings, and estimate the number of UMAP fits.","Chapter 11 explains how each retained candidate is measured and ranked."),
(11,"Candidate diagnostics, legacy_dimple, ranking, ties, and sensitivity","5,9–10","How should heterogeneous diagnostics be combined without disguising their assumptions?","A deterministic score is reproducible yet remains population-relative and sensitive to component ranges and candidate composition.","`legacy_dimple` uses silhouette and cluster count plus an optional subtracted noise term; DBCV, CH, DB, persistence, and projection diagnostics are not default score components.",[19,20,21,40],["C20","C21","C22","C23","C24","C25","C26"],["metrics","scoring","ranking"],"Compute both Lab 0 score profiles from the three-row candidate table and explain why cluster count dominates when its raw range is larger.","Chapter 12 freezes one selected model into a replayable artifact and compares results structurally."),
(12,"Selected-model reproduction, provenance, and comparison","8–11","What must be retained to replay a model and decide whether two results agree?","Numeric labels and raw coordinates can differ while partitions agree, whereas identical labels without identifier checks can be meaningless.","Same-environment fixture concordance is technical evidence. It is not a guarantee across machines and not biological validation.",[22,23,42],["C19","C27","C28","C29","C30","C34","C35"],["comparison","provenance","validation","pipeline"],"Relabel a partition, calculate its noise Jaccard, and interpret why ARI=1 can coexist with nonidentical numeric labels.","Part III begins by turning these contracts into an installable, inspectable workflow."),
(13,"Installation, environment verification, and first run","1,6","How does a newcomer establish that the intended RC1 is the code actually running?","An installed command can succeed while pointing to the wrong environment or an uncontrolled dependency set.","The fresh Edition 2 environment is macOS arm64 and passed 45 tests; Docker/Linux/cloud evidence remains pending.",[9,13],["C34","C35"],["cli","provenance","pipeline"],"Create an isolated environment, verify `dimple-gwas --version`, capture help, run `pip check`, and distinguish installation from analytical validation.","Chapter 14 makes configuration precedence and candidate enumeration inspectable before compute begins."),
(14,"Configuration and search-space inspection","6,10,13","Which values will the software actually use after built-ins, YAML, and CLI overrides are combined?","Readable YAML is not necessarily the resolved configuration, and a plausible range can still request unintended compute.","`inspect-config` and `show-search-space` are preflight tools; successful inspection does not validate the scientific suitability of settings.",[11,12,38,39],["C18","C19"],["cli","config","search_space"],"Predict one override result and the Lab 2 candidate count before comparing both with fresh command output.","Chapter 15 executes the resolved plan and teaches the run manifest as the primary narrative."),
(15,"Complete pipeline execution and monitoring","7–14","What happens between pressing return and receiving a selected model?","The pipeline shares each UMAP representation across a family of HDBSCAN candidates while retaining invalid and failed models instead of silently dropping them.","A complete run reports software and artifact status; it does not imply that the selected model is scientifically preferred outside the declared score and candidate set.",[4,13,14,43,44],["C02","C12","C18","C19","C25","C35"],["pipeline","reporting","provenance","visualization"],"Trace one Lab 1 candidate through resolved configuration, prepared shape, UMAP family, candidate evaluation, scoring, refit, and manifest entries.","Chapter 16 starts from the retained tables and performs the post-run command sequence."),
(16,"Model summaries, selection, reproduction, comparison, and validation","11–15","How does an analyst move from a ranked table to a defensible retained model?","The highest score is a reproducible ordering under one objective, not an instruction to skip sensitivity, failure review, or scientific adjudication.","Commands operate on retained artifacts and exact IDs. Historical manual selection must remain disclosed when it differs from automatic rank.",[20,21,22,23],["C25","C26","C27","C28","C29","C30","C34"],["ranking","scoring","comparison","validation","cli"],"Use the tied Lab 2 top rows to explain deterministic tie ordering and write a selection note that distinguishes automatic rank from analyst choice.","Chapter 17 returns to original input space without refitting the selected partition."),
(17,"Original-space explanation, heatmaps, and responsible interpretation","3,5,12,16","What structure do retained labels describe in the original variant dimensions?","A heatmap can make a selected partition intelligible while also inviting circular biological claims.","Freeze 3 reports descriptive Pearson/Spearman summaries, order and cutpoint sidecars, exclusions, and optional coordinate associations; it emits no post-selection p-values.",[24,25,26,27,28,29],["C02","C17","C24","C31","C32","C33"],["interpretation","preprocessing","visualization"],"Follow Lab 3 from exact ID matching through similarity, ordering, cutpoints, cluster summaries, and the rendered heatmap; state three conclusions the image cannot support.","Part IV begins with a hand-calculable integration of the method."),
(18,"A hand-calculable toy analysis from matrix to score","6–11","Can the essential contracts be understood without hiding behind a large run?","A toy must simplify UMAP while remaining literal about implemented preprocessing, diagnostics, scoring, and comparison.","Lab 0 executes valid code paths but does not claim a hand reconstruction of stochastic UMAP or HDBSCAN hierarchy.",[4,5,15,19,20,23],["C02","C03","C04","C05","C20","C25","C27","C28","C29"],["preprocessing","metrics","scoring","ranking","comparison"],"Reproduce every retained Lab 0 number and reconcile exact numeric inequality with permutation-invariant agreement.","Chapter 19 increases realism by running the packaged fixed synthetic fixture end to end."),
(19,"Fixed synthetic end-to-end analysis","13–17","Can a fresh user complete the entire software path and account for every output?","A designed fixture can verify contracts quickly but cannot estimate production robustness or biological validity.","The fresh Edition 2 run uses one seed and one candidate, producing three designed groups of eight with no noise.",[13,14,32,41],["C12","C17","C19","C20","C24","C25","C34"],["pipeline","reporting","validation"],"Audit the 24-by-80 prepared shape, the selected model, its metric values, the output inventory, and all 24 validation checks.","Chapter 20 expands the candidate population to reveal ranking and sensitivity behavior."),
(20,"Custom bounded search, sensitivity, and selected-model replay","10–16,19","How can an analyst learn about parameter dependence without turning sensitivity analysis into target matching?","Changing the candidate population can alter normalized scores even when a candidate's raw diagnostics do not change.","Lab 2 is a designed 32-candidate example; identical fixture labels across settings do not imply universal insensitivity.",[12,21,33,44],["C12","C18","C19","C23","C24","C25","C26"],["search_space","pipeline","scoring","ranking"],"Group the 32 candidates by UMAP family, compare diagnostic shifts, identify top-score ties, and write a preregistered sensitivity conclusion.","Chapter 21 exercises every post-run explanation, comparison, and validation route."),
(21,"Explanation, comparison, validation, and report generation","16–17,19","Can retained outputs be interpreted and compared without rerunning discovery or losing identifier integrity?","Post-run tooling increases auditability but does not convert same-data summaries into confirmatory inference.","Lab 3 is exact same-environment fixture evidence; publishable reporting must use sanitized paths and preserve conditional language.",[23,25,26,27,34],["C02","C24","C27","C28","C29","C30","C31","C32","C33","C34"],["interpretation","comparison","validation","reporting"],"Reproduce, explain, compare, and validate Lab 1; then write one technical result paragraph and one separate scientific-limitations paragraph.","Chapter 22 contrasts a public benchmark with the historically important 164-IDP workflow."),
(22,"MNIST benchmark and original 164-IDP reconstruction protocol","12–21","How should public engineering evidence and protected historical scientific evidence coexist in one validation program?","MNIST can stress software without validating genetics; historical reconstruction can preserve provenance without becoming a fresh run.","MNIST remains protocol-only here. The fresh 164-IDP 1,000-seed run is explicitly deferred until Docker; only historical outputs and acceptance criteria are described.",[35,36],["C12","C27","C28","C29","C30","C34","C35"],["pipeline","comparison","validation","provenance"],"Build a two-column evidence table separating historical reconstruction from fresh computation, including the disclosed row-16 selection and pending Docker requirements.","Part V generalizes these examples into a layered validation strategy."),
(23,"Technical, statistical, biological, and cross-platform validation","5,12,19–22","What evidence would justify each kind of claim an analyst might want to make?","One impressive metric cannot stand in for software, structural, statistical, biological, external, and platform evidence simultaneously.","Current evidence supports local contracts and fixed fixtures; external biological and Docker/Linux/cloud layers remain incomplete.",[8,23,29,30,42,46],["C27","C28","C29","C30","C33","C34","C35"],["validation","comparison","provenance","metrics"],"Assign twelve checks to the validation ladder, choose exact or tolerance-based acceptance, and identify which layers remain unanswered.","Chapter 24 turns the full evidence chain into reporting, migration, and reviewer-facing documentation."),
(24,"Reproducible reporting, limitations, migration, and reviewer-facing methods","1–23","How can a methods section be exact about software while remaining modest about scientific inference?","A polished narrative can conceal unresolved evidence unless every claim is connected to manifests, code, literature, and named limitations.","This internal-review edition preserves unresolved Yang/Zhao attribution as a gap, keeps reviewer correspondence private, and leaves public release, Docker, and team adjudication pending.",[3,7,31,36,42,45,46],["C01","C02","C19","C33","C34","C35"],["reporting","provenance","validation","cli"],"Draft a methods paragraph from the Lab 2 manifest, a limitations paragraph from the claim register, and a Docker handoff acceptance block.","The appendices provide the exact CLI, configuration, function, output, migration, solution, and evidence references."),
]


def read_tsv(path):
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle,delimiter="\t"))


def clean_old(number):
    matches=list(OLD.glob(f"{number:02d}_*.md"))
    if not matches: return ""
    text=matches[0].read_text(encoding="utf-8")
    text=re.sub(r"^# .*?\n","",text,count=1)
    text=re.sub(r"> \*\*Release status\.\*\*.*?\n\n","",text)
    # Remove repeated orientation/objective/completion/xref scaffolds while retaining substantive sections.
    text=re.sub(r"## Orientation\n.*?(?=\n## )","",text,flags=re.S)
    text=re.sub(r"## Learning objectives\n.*?(?=\n## )","",text,flags=re.S)
    text=re.sub(r"## Completion check\n.*?(?=\n## |\Z)","",text,flags=re.S)
    text=re.sub(r"<p class=\"xref\".*?</p>","",text,flags=re.S)
    # Edition 1 figures are superseded by the Edition 2 figure inventory.  Strip the
    # archived embeds/captions and update their prose references to the fresh labs.
    text=re.sub(r"^!\[Figure [^\n]+\]\([^\n]+\)\n?","",text,flags=re.M)
    text=re.sub(r"^\*Figure [^\n]+\*\n?","",text,flags=re.M)
    text=text.replace("Figure 1 shows three separated synthetic groups.","The fresh Lab 1 display in Chapter 19 shows three separated synthetic groups.")
    text=text.replace("Figure 2 makes the four family-level score bands visible.","The fresh Lab 2 rank plot in Chapter 20 makes the four family-level score bands visible.")
    text=text.replace("Figure 3 labels these as post-selection descriptive summaries.","The fresh Lab 3 treatment in Chapters 17 and 21 labels these as post-selection descriptive summaries.")
    text=text.replace("Figure 5 separates the historical count panel from a prominent ‘fresh run pending’ panel.","The Edition 2 evidence-status graphic in Chapter 22 separates historical evidence from a prominent fresh-run-pending status.")
    text=re.sub(r"Figure 6 is copied byte-for-byte from Tutorial 3's `original_space_heatmap\.png`; its source checksum and script/manifest are in `figure_source_manifest\.tsv`\.","The Edition 2 Lab 3 heatmap is regenerated at publication resolution from the freshly retained similarity matrix; its source and generation record are in `qa/figure_inventory.tsv`.",text)
    text=text.replace("Tutorial 1","Edition 2 Lab 1").replace("Tutorial 2","Edition 2 Lab 2").replace("Tutorial 3","Edition 2 Lab 3").replace("Tutorial 4","Edition 2 Lab 4")
    text=text.replace("docs/manual/tutorials/","docs/textbook/edition2/labs/")
    text=text.replace("docs/manual/build/runtime_env","docs/textbook/edition2/build/runtime_env")
    text=text.replace("run_20260825_v2","run_20260826")
    text=text.replace("`tutorial_execution_manifest.tsv`","`docs/textbook/edition2/labs/execution_manifest.json`")
    text=text.replace("`figure_source_manifest.tsv`","`qa/figure_inventory.tsv`")
    text=text.replace("`evidence/figure_source_manifest.tsv`","`qa/figure_inventory.tsv`")
    text=text.replace("Chapter 41 maps every named output to its producer and consumer.","Appendix D maps every named output to its producer and consumer.")
    text=text.replace("Verify the generated file set against Chapter 41.","Verify the generated file set against Appendix D.")
    text=text.replace("Follow Chapters 11–14 using the actual YAML. Then use Chapter 22 to reproduce the selected summary, Chapter 23 to compare it, and Chapter 25 to explain it.","Use Chapters 14–15 with the actual YAML, Chapter 16 to reproduce the selected summary, Chapter 21 to compare it, and Chapter 17 to explain it.")
    text=text.replace("## Explanation and implementation","### Operational foundation")
    text=text.replace("## Evidence-backed example","### Retained evidence")
    text=text.replace("## Outputs to inspect","### Output-reading checkpoint")
    text=text.replace("## Common mistakes","### Misinterpretations to avoid")
    text=text.replace("## Scientific and operational limits","### Boundary inherited from Edition 1")
    return text.strip()


def chapter_match(planned,number):
    normalized=planned.replace("–","-")
    for a,b in re.findall(r"(\d+)\s*-\s*(\d+)",normalized):
        if int(a)<=number<=int(b): return True
    return bool(re.search(rf"(?<!\d){number}(?!\d)",normalized))


def cite(raw):
    keys=[key.strip() for key in raw.split(";") if key.strip() and not key.strip().startswith("internal") and key.strip() not in {"not applicable"}]
    return f" [@{'; @'.join(keys)}]" if keys else ""


def main():
    CHAPTERS.mkdir(parents=True,exist_ok=True)
    concepts={r["concept_id"]:r for r in read_tsv(EDITION2/"evidence/statistical_concept_coverage.tsv")}
    functions=read_tsv(EDITION2/"function_atlas/function_inventory.tsv")
    claims=read_tsv(EDITION2/"evidence/claim_evidence_register.tsv")
    outputs=read_tsv(EDITION2/"output_atlas/output_atlas.tsv")
    for number,title,prereq,question,tension,boundary,old_numbers,concept_ids,modules,worked,transition in SPECS:
        lines=[f"# {number}. {title}","",f"*Guiding question:* **{question}**","",f"Prerequisites: {prereq}.","","## Why the question matters","",tension,"",boundary,"",f"This chapter develops the question in the order needed for a reader to move from statistical principle to current implementation, retained evidence, and a defensible statement. Its central worked task is: {worked}","","## Learning objectives","",f"After completing Chapter {number}, the reader can:",""]
        selected_concepts=[concepts[c] for c in concept_ids if c in concepts]
        for idx,c in enumerate(selected_concepts[:5],1):
            lines.append(f"{idx}. define {c['concept']} and explain its role without exceeding the stated caution;")
        lines += [f"{min(6,len(selected_concepts)+1)}. trace the relevant package functions and generated artifacts;",f"{min(7,len(selected_concepts)+2)}. complete the worked task and distinguish observation from interpretation.","","## Conceptual and mathematical development",""]
        for c in selected_concepts:
            lines += [f"### {c['concept']}","",f"{c['definition'].capitalize()}. A compact notation is `{c['equation_or_notation']}`. In practical terms, {c['interpretation_and_caution'][0].lower()+c['interpretation_and_caution'][1:]}{cite(c['evidence_sources'])}","",f"Within Freeze 3 RC1 the concept is connected to `{c['functions']}` and is visible through `{c['outputs']}`. This connection is narrower than the general statistical idea: software evidence establishes the implemented route, while the mapped primary or internal evidence supplies background authority. The distinction prevents a mathematical definition from being mistaken for proof that a particular scientific interpretation is correct.",""]
        old_parts=[clean_old(n) for n in old_numbers]
        old_parts=[p for p in old_parts if p]
        if old_parts:
            lines += ["## Reconstructed operational foundation","", "Edition 1 contained the following verified operational material in separate short notes. Edition 2 consolidates it here and subjects it to the concept and evidence boundaries above.",""]
            for n,part in zip(old_numbers,old_parts):
                lines += [f"### Evidence retained from former Chapter {n}","",part,""]

        selected_functions=[r for r in functions if r["tier"] in {"A","B"} and (r["module"] in modules or chapter_match(r["planned_chapter"],number))][:12]
        lines += ["## Implementation trace",""]
        if selected_functions:
            for r in selected_functions:
                lines += [f"**`{r['qualified_symbol']}`** is defined at `{r['source_path']}:{r['source_line']}` with signature `{r['input_signature']}`. {r['purpose']} It is reached from {r['callers']} and connects to {r['package_dependencies']}. Its direct artifact contract is {r['direct_outputs']}; its explicit error surface is {r['explicit_exceptions']}. Test evidence is recorded as {r['tests']}. This is a {r['tier']}-tier contract, so the complete 20-field dossier is retained in the function atlas.",""]
        else:
            lines.append("The relevant functions are cross-cutting and are treated in the adjacent chapters; the function atlas remains authoritative for source locations and tests.\n")

        mapped_claims=[]
        for r in claims:
            locs={int(x) for x in re.findall(r"\d+",r["book_location"])}
            if number in locs: mapped_claims.append(r)
        if mapped_claims:
            lines += ["## Claim adjudication notebook","", "The following statements are admitted to the draft only in their safe form:",""]
            for r in mapped_claims:
                lines += [f"- **{r['claim_id']} ({r['classification']}):** {r['proposed_safe_wording']}{cite(r['primary_citation'])} Limitation: {r['limitation_or_counterpoint']} Implementation evidence: `{r['implementation_evidence']}`.",""]

        command_map={10:["run/show-search-space"],11:["run"],12:["compare","validate"],13:["run"],14:["run/show-search-space"],15:["run"],16:["run","score-existing","summarize-models","compare","validate"],17:["explain"],18:["run","compare"],19:["run","validate"],20:["run","run/show-search-space"],21:["explain","compare","validate"],22:["compare","validate"],23:["validate","compare"],24:["run","validate"]}
        selected_outputs=[r for r in outputs if r["producing_command"] in command_map.get(number,[]) and r["artifact_id"].startswith("ART-")][:14]
        if selected_outputs:
            lines += ["## Reading the generated evidence","", f"For Chapter {number}, the `{title}` files are read as a provenance chain rather than as isolated results:","", "| Artifact | Producer | What to verify before interpretation |", "| --- | --- | --- |"]
            for r in selected_outputs:
                lines.append(f"| `{r['name_or_pattern']}` | `{r['producer']}` | {r['healthy_properties']} |")
            lines += ["", f"The output atlas supplies the complete schemas, checksums, conditions, consumers, and privacy notes for this Chapter {number} route. Native manifests can contain machine paths; the assembled textbook uses sanitized excerpts while restricted evidence retains the original provenance chain.",""]

        answer_rule=(f"A complete Chapter {number} answer must expose its intermediate reasoning, name the source or output used for `{title}`, "
                     f"and finish with separate support and non-support statements. Applying that discipline to the question “{question}” prevents a calculation, "
                     "a software observation, and a scientific interpretation from collapsing into one claim.")
        recovery=(f"If the Chapter {number} route fails, retain its log and candidate status before deciding whether the cause is input, configuration, dependency, "
                  f"compute, identifier alignment, or output-root state. Correct an operational failure by writing a new result directory. Treat instability in `{title}` "
                  "as sensitivity evidence: report it and identify the independent evidence needed instead of relabeling ambiguity as a software exception.")
        central_concept=selected_concepts[0]['concept'] if selected_concepts else 'the workflow contract'
        lines += ["## Worked reasoning and evidence exercise","",worked,"", answer_rule,"", "## Assumptions, diagnostics, and recovery","",f"The Chapter {number} analysis assumes the stated unit and inputs, the recorded configuration and software identity, and a diagnostic that addresses the claimed property rather than a convenient surrogate. Its decisive boundary is: {boundary}","", recovery,"", "## Chapter synthesis","",f"{tension} The implementation trace makes the current behavior auditable, but the evidence boundary remains part of the result. {transition}","", "## Exercises","",f"1. For `{title}`, name the unit of analysis and one plausible but invalid substitute.",f"2. Reconstruct the notation for {central_concept}; define its dimensions or denominator and interpret every term.",f"3. Choose a Tier A function mapped to Chapter {number}; identify its caller and direct output, then propose a topic-specific edge case.",f"4. Select one Chapter {number} artifact from the output atlas and state three integrity checks that must precede scientific reading.",f"5. Convert a tempting `{title}` overclaim into one observed statement followed by its limitation.",f"6. {worked}","", f"Appendix J gives the Chapter {number} adjudication guide. Its further-reading keys supply statistical context; no external paper is treated as automatic validation of the current software or dataset.",""]
        path=CHAPTERS/f"{number:02d}_{re.sub(r'[^a-z0-9]+','_',title.lower()).strip('_')}.md"
        path.write_text("\n".join(lines),encoding="utf-8")
    print(f"Drafted {len(SPECS)} chapters; preserved calibration Chapter 7")


if __name__=="__main__":
    main()
