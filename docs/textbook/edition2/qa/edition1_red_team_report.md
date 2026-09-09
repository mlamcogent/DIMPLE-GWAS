# Edition 1 pedagogical red-team report

## Verdict

Edition 1 succeeds as a cautious analyst-manual skeleton: it names the implemented stages, gives portable command patterns, records fresh fixture evidence, and preserves important interpretation boundaries. It does not yet teach the method at graduate-textbook depth. The weakness is systemic, not confined to a handful of chapters.

## Principal failures

1. **Architecture fragments concepts.** Forty-six short chapters interrupt the conceptual arc. UMAP, repetition, HDBSCAN, diagnostics, scoring, selection, reproduction, comparison, and interpretation are introduced as adjacent checklists rather than developed as a connected inferential workflow.
2. **Mathematics is largely deferred.** The mathematical appendix contains several formulas, but main chapters rarely derive objectives, define edge cases, or connect equations to implementation behavior.
3. **Examples assert rather than teach.** Executed fixture results are real, but most chapters state one result instead of walking through a calculation, file excerpt, decision, and alternative interpretation.
4. **Function coverage is indirect.** Commands and configuration keys are mapped, but the reader cannot trace every core function through inputs, parameters, exceptions, outputs, tests, and computational behavior.
5. **Exercises do not assess objectives.** A one-sentence completion check appears in every chapter; there are no developed problem sets, calculation exercises, applied tasks, or separated solutions.
6. **Citations are too remote.** Bibliographic entries and occasional chapter references exist, but many statistical claims lack nearby citations and a reader cannot always see which statement a paper supports.
7. **Output education is centralized.** The atlas is useful, yet stage chapters rarely annotate representative rows/fields before sending the reader to a distant reference.
8. **Visual QA was too coarse.** Contact sheets established page presence but did not catch node overlap and figure-heading separation at full resolution.

## Edition 2 editorial disposition

- Merge the 46 notes into 24 substantial chapters organized by conceptual dependency.
- Rewrite core statistical and method chapters from zero.
- Retain verified commands, outputs, cautious language, and evidence identifiers as source material rather than prose templates.
- Move exhaustive command/configuration/function/output lookup content to structured appendices and atlases.
- Add a hand-calculable lab, executed labs, multi-step exercises, and a solutions appendix.
- Use a function dossier as a content-completeness contract, but integrate its fields into natural prose rather than repeating 20 visible headings.
- Audit every source figure independently and again on the composed page.

The machine-readable rubric is `edition1_chapter_gap_matrix.tsv`. Scores describe the supplied Edition 1 baseline only; they are diagnostic planning evidence, not a publication-quality rating.
