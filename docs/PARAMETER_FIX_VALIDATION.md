# Portable.3 local validation scope

29 self-contained test cases cover7 original portable checks,7 scientific configuration/backend cases,8 named-column intake cases and7 planner/launcher checks. Run from a clean extraction with `python -B -m unittest discover -s tests -v` in the pinned scientific environment. Exact terminal receipt accompanies the source kit.

Actual synthetic fits: standalone PCA and ICA use the exact existing canonical implementations; custom UMAP uses2 seeds and altered dimensions/metric/settings, followed by complete32-candidate HDBSCAN grids including cosine/manhattan and eom/leaf. Candidate corruption is rejected. Paired original/new default UMAP constructors produce identical float32 bytes on the same small matrix/seed, and default HDBSCAN labels and scoring agree exactly. Published recipe/scoring bytes are pinned unchanged. These checks do NOT rerun the full9×1,000-seed research search or establish scientific validity on another dataset.

Actual local Nextflow26.10.3 failure→resume: synthetic60×3 PCA route; first GRID attempt deliberately exits77, then resume succeeds with PREPARE, representation and CONCAT cached and GRID/RANK completed. Earlier attempt logs/traces remain separate. Launcher-specific failure/resume is additionally exercised with a shim, not confused with the real workflow test.

No image rebuild, AWS/GCP execution, publication, real participant input or2,315-trait matrix was used. Existing images do not contain these source changes. Live cloud qualification remains separate. Current intake retains minimum51 objects even for custom/PCA/ICA settings; smaller inputs are rejected explicitly. Numerical outputs/provenance vary for intentionally changed parameters; no claim of all metadata bytes remaining identical is made.
