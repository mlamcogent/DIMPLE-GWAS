# Edition 1 page and figure audit

All 122 Edition 1 pages were available as 110-dpi page renders and in 11 contact sheets. The contact sheets were reviewed for global pagination and every suspected figure page was reopened at full resolution. Seven defects are recorded in `edition1_visual_defect_ledger.tsv`; three are material figure/layout failures.

The macro's starting examples are confirmed. Page 25 contains overlapping sibling nodes in the input-orientation diagram. Page 44 separates the search-space figure from its generic section heading. Page 102 compresses five provenance-source boxes into an overlapping row with congested connectors. These defects were not detected by the Edition 1 automated QA because it verified image hashes, page counts, and contact-sheet coverage but did not measure SVG bounding boxes or require a full-resolution checklist per source figure.

Edition 2 therefore adopts a two-level visual gate: each diagram must pass source SVG geometry checks before composition, and every containing page must pass full-resolution inspection after typesetting. Contact sheets remain useful for sequence and density but are not sufficient evidence of label or node clearance.
