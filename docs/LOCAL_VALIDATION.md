# Historical predecessor validation

The detailed evidence below was obtained for portable.1, not rerun for portable.3. See PARAMETER_FIX_VALIDATION.md for actual portable.3 checks. Version labels below identify the current package, not a claim of repeated182-task qualification.

# Local validation and release limits

Version `5.2.0-research-portable.3`, checked 11 November 2026 Singapore time.

| Check | Local result |
| --- | --- |
| Portable Python tests | Seven tests passed. They cover both CSV orientations with and without gzip, byte and shape mismatch, exact string IDs, recipe changes, path quoting, seed ordering and foreign/missing chunks, 21,870-row aggregation, a configuration with no eligible candidates, saved labels, raw scoring with noise, and optional truth-ID alignment. |
| Nextflow wiring | Nextflow 26.10.3 and Java 21 ran 182 local stub tasks. All 182 were cached on unchanged resume. Stub outputs carry a wiring-only marker. |
| Input preparation | One real local PREPARE task processed the synthetic gzip CSV with spaces and quotes in the paths. Mutating the bytes while retaining the original grid forced a new task on resume, which refused the stale hash. |
| AWS profile and stack | Offline nf-amazon 3.12.1 configuration rendered. The Batch CloudFormation template passed existing local cfn-lint. Static policy tests pin the plugin's required tag keys to scoped Batch resource ARNs. |

The local numerical tests used an existing Python environment with NumPy 2.5.4, pandas 3.0.6, scikit-learn 1.9.1, umap-learn 0.5.12 and hdbscan 0.8.44. The worker build has its own exact wheel hashes. Local synthetic checks verify software behavior. The worker container build and native Linux verification, AWS execution, and scientific acceptance on the intended data each require separate evidence.

The current 5.3 worker image is public; see [DEPLOY_GCP.md](DEPLOY_GCP.md) for its pinned reference and regional mirror steps. GCP live qualification and scientific acceptance remain pending. The predecessor evidence above is historical; current source/image checks are recorded in [VALIDATION_5_3.md](VALIDATION_5_3.md).
