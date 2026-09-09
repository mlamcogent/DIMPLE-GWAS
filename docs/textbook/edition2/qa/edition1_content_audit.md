# Edition 1 content audit

Edition 1 is a useful verified operational baseline but not a graduate-level textbook. The compiled Markdown contains **21,215 words** across **46 chapters** and **8 appendices**; the PDF contains **122 A4 pages** and approximately **20,701 extractable words**. The median chapter has **416 words** (range 355–504).

## Density and structure

- 23 pages (18.85%) contain fewer than 100 extracted words.
- 49 pages (40.16%) contain fewer than 150 extracted words.
- 72 pages (59.02%) contain fewer than 200 extracted words.
- The same eight-section teaching scaffold appears in all 46 chapters.
- A large release-status box appears 46 times and the same operational cross-reference appears 46 times.
- The edition contains 16 image references, 8 fenced code blocks, 1 display-math blocks, and 2 Markdown tables.

## Source-of-sparsity diagnosis

The generation system treated every topic as an identically shaped two-page unit. Short parameter descriptions, scientific cautions, command fragments, and completion prompts were spread across 46 forced chapter openings. Repeated banners, boilerplate prerequisites, generic evidence language, and part-divider pages consumed pagination without developing the underlying mathematics or examples. The chapter generator optimized structural coverage—every topic received the same headings—but did not budget depth by conceptual difficulty. Reference-like content was mixed into the main narrative, while function contracts, formula derivations, hand-worked calculations, exercises, and output schemas remained too compressed.

The remedy is architectural rather than cosmetic: merge the 46 notes into 24 substantial chapters, move lookup material to function/output atlases, draft by conceptual dependency, require method-specific dossiers and worked calculations, and permit chapter structures to vary. Edition 2 must measure substantive words after removing front matter, code-only listings, bibliography, and generated schema tables so visual length cannot substitute for explanatory depth.

## Evidence files

- `edition1_chapter_metrics.tsv`: chapter-level density and scaffold counts.
- `edition1_page_density.tsv`: page-level extracted-word counts.
- `edition1_duplicate_passages.tsv`: exact and high-similarity boilerplate evidence.
- `edition1_content_metrics.json`: machine-readable baseline.
