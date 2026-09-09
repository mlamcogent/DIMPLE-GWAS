# Textbook Edition 2 build report

Date: 2026-08-26  
Software: DIMPLE-GWAS 3.0.0rc1  
Distribution status: internal review, near-public-facing draft

## Source identity

No usable Git metadata is present in the supplied Freeze 3 tree, so SHA-256 identities are authoritative. The source inventory, authority/conflict map, missing-evidence register, and source checksum register are retained under `evidence/`. The author line follows `Cogent manuscript/Manuscript-draft5_05.25.2026.docx` (SHA-256 `eb4cce0f23f1c3d385e8ff0fa378e59d43caf2c2c6974aa96f642db26fc4fcdd`) in manuscript order.

## Baseline and diagnosis

Edition 1 contained 46 chapters across 122 pages. Its audit identified sparse/fragmented pedagogy and three material visual defects: input-orientation, search-space, and provenance diagrams. Edition 2 consolidates the curriculum, replaces those diagrams, and adds executable and reference layers.

## Edition 2 metrics

| Metric | Value |
|---|---:|
| Parts / chapters / appendices | 5 / 24 / 15 |
| Main-chapter regex words | 87,534 |
| Assembled regex words | 109,808 |
| PDF pages / extracted words | 370 / 110,000 |
| Figures / tables / numbered display equations | 21 / 35 / 9 |
| Verified references / used citation keys | 25 / 23 |
| Claim/evidence entries | 30 |
| Statistical concept entries | 35 |
| Labs defined / executed | 6 / 4 |
| Fresh command records | 14 |
| Command interfaces checked | 13 |
| Callables inventoried | 110 |
| Tier A/B dossiers complete | 78/78 (100%) |
| Output patterns documented | 35/35 (100%) |
| Output patterns freshly verified | 34/35 (97.1%) |
| Exercises / solutions | every chapter / Appendix J |
| Tests | 45 passed; 5 retained warnings |

## Execution environment and laboratories

The fresh environment used Python 3.12.13 on macOS arm64. Dependency checking passed. Labs 0–3 executed from retained configurations into new output roots; execution commands, timestamps, exit codes, logs, sanitized examples, and checksums are retained. The fixed lab produced one 3×8, zero-noise candidate. The bounded custom search completed 32 candidates and selected a deterministic tie-broken model. Reproduction matched the fixed result exactly on ARI, NMI, noise Jaccard, and mapped membership; VI was 0 and Procrustes disparity was approximately 2.7088×10⁻³¹. Validation passed 24/24 checks.

Lab 4 is an exact MNIST protocol rather than a claimed completed benchmark. Lab 5 distinguishes retained historical material from the not-yet-run Freeze 3 reconstruction protocol. In accordance with the coordinator decision, the fresh 164-IDP/1,000-seed run is deferred until Docker is built.

## Coverage and evidence integrity

All 110 inventoried callables map to source, tests or integration coverage, outputs or a stated non-artifact contract, chapters, and evidence status. Every Tier A/B callable has all 20 required dossier fields. All 10 CLI subcommands, the `interpret` alias, top-level version/help behavior, and the Python module entry point are documented and checked. The output atlas documents all 35 patterns; only the opt-in coordinate-association artifact lacks fresh execution.

Twenty-five bibliography entries have verified metadata; 23 keys are cited and resolved in the assembled book. The Yang- and Zhao-attributed reviewer papers remain unidentified, are explicitly recorded as unresolved, and are not used to support claims. Reviewer correspondence is represented only by a sanitized method crosswalk.

## Visual QA

The tagged, selectable-text PDF is 370 US-Letter pages (6,293,648 bytes). All pages were rendered to PNG and inspected through 19 contact sheets; all 21 figure assets and containing pages were inspected. Figure 16 was corrected during QA after an initial key mismatch produced zero bars. After rebuilding, there are zero known overlap, clipping, accidental-split, unreadable-label, or unresolved-reference defects. The self-contained HTML provides navigation; PDF outline bookmarks are renderer-dependent (root outline items detected: 0).

## Acceptance result

No gate failed. Gates A, C, D, and J pass. Gates B, E, F, G, H, I, and K pass with the limitations recorded in `qa/acceptance_gate_matrix.tsv`. These limitations prevent describing the artifact as a completed public software/documentation release.

## Exact next steps

1. Build the Freeze 3 Docker image using the constraints in Appendix O.
2. Re-run the isolated test suite and Labs 0–3 inside the image.
3. Execute the retained Lab 5 164-IDP/1,000-seed protocol inside Docker, preserve logs/checksums, and update only evidence-supported results.
4. Complete Linux/container and required cross-platform comparison and validation.
5. Ask the review team to identify the Yang/Zhao papers or formally remove those attributions.
6. Conduct team statistical, biological, privacy, and editorial adjudication; decide whether to compress the logged traceability repetition.
7. Rebuild and rerun all QA gates before changing the label from internal review to public-facing release.

## Deliverable checksums

The checksum manifest contains 16 authoritative SHA-256 records at `checksums/edition2_build_checksums.sha256`. Because the build manifest itself changes when reports are finalized, its checksum should be regenerated for any subsequent release candidate.
