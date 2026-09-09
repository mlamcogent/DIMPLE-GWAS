# Documentation Edition 3 changelog

Date: 2 September 2026  
Status: reader draft under the Stage 1 `PASS_WITH_LIMITATIONS` gate

## Reader-facing reconstruction

- Rebuilt the documentation as one continuous reader draft with three coordinated modes: a 15-chapter academic textbook, a nine-lab analyst workbook, and a lookup-oriented technical reference.
- Added a preface with role-specific reading paths, a consistent evidence vocabulary, an analyst learning path, troubleshooting, exercise solutions, notation/glossary, and an evidence/claim index.
- Replaced the Edition 2 manual-like progression with a dependency-ordered narrative: scientific unit, geometry, nonlinear representation, density hierarchy, search, scoring, stability, original-space interpretation, biological claims, and comparative method positioning.
- Preserved modular Markdown sources so individual chapters, labs, and reference sections remain maintainable.

## Scientific and implementation corrections

- Made the clustered unit explicit: phenotype-associated vectors/IDPs after validated preprocessing and transpose, not participants, variants, or voxels.
- Distinguished repeated-coordinate concatenation from alignment, averaging, partition ensembles, and consensus clustering.
- Treated HDBSCAN label `-1` as algorithmic non-assignment, not failed biology.
- Explained the table-relative legacy score, zero-range fallback, dynamic-range weights, tie handling, and the distinction between scoring and validation.
- Recast the fixed 24-by-80 fixture as a bounded software regression, not real-data evidence.
- Kept the 2,315-, 459-, 164- and 356-object analyses separate and labelled their evidence status. No reproduction configuration was invented for the conflicting 459-object record.
- Recorded that the retained 164-object selection was manual at sorted position 16; exact adaptation and 333-row re-scoring are not described as a fresh fit.
- Separated artifact, software, structural, statistical, biological, and cross-platform validation claims.

## New visual and reference material

- Added five original diagrams: pipeline/evidence boundary, validation ladder, matrix orientation, repeated embeddings, and analysis hierarchy.
- Added command, configuration, function, output, error/recovery, and provenance reference sections.
- Added a function-concept-output coverage register, command execution register, and figure/table register.

## Build and format changes

- Produced self-contained Markdown and HTML editions plus privacy-scrubbed DOCX and tagged PDF reader builds.
- Preserved ten semantic tables in Markdown/HTML. In DOCX/PDF, their cells are rendered as compact labelled rows because the available LibreOffice renderer produced severe empty-grid pagination when consuming Pandoc tables. The workaround preserves the table content and eliminates blank spill pages.
- Applied a narrative-proposal document style: Letter pages, consistent margins, restrained blue hierarchy, running header, page-number footer, accessible heading styles, inline figures, and readable code formatting.

## Reader correction pass

- Replaced the empty Word-generated contents placeholder with a two-page static contents section containing 43 verified entries, dot leaders, and physical page numbers.
- Converted 159 inline expressions and 31 display equations into declared mathematical notation. The Word edition now contains native equation objects, and the HTML edition uses MathML rather than exposing LaTeX source.
- Styled software commands, parameter names, option values, paths, identifiers, and code spans in blue in the HTML, DOCX, and PDF editions while retaining the monospace distinction.
- Removed converter-only bookmark and hyperlink markers that LibreOffice exposed as stray `X` glyphs in the PDF; bibliography URLs remain visible, while the HTML edition retains live links.

## Open gates

This draft does not close the fresh historical 164-IDP 1,000-seed rerun, real-data stability analysis, independent biological validation, optional XLSX dependency, Git/tag identity, or Docker/Linux/cloud/cross-platform qualification. See `KNOWN_LIMITATIONS_AND_PENDING_VALIDATION.md`.
