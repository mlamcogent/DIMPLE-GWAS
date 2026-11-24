# Freeze 5.3 portable.2 validation and limits

Source version 5.3.0-research-multicloud.2, checked 11 November 2026 Singapore time; promoted to Freeze 5.3 stable after the 23 November 2026 AWS + GCP interoperability run below. Originally a source-only update from frozen 5.2.0-research-portable.3 archive SHA256 6d801729b033185e5f97df794d0e12e8b1aedf324fc283c6ea311aba8b6cdaa0.

- 35 offline tests passed in 21.781 seconds: 29 inherited 5.2 cases plus 6 GCP cases. After independent review found a PREPARE/full-run attempt-directory collision, the planner now emits distinct prepare01 and attempt01 directories; the 6-case GCP suite passed again with a regression assertion.
- Actual local synthetic PCA pipeline: PREPARE, representation, CONCAT, GRID and RANK all completed. Initial resume exposed Python bytecode changing staged module-directory identity. The package now disables runtime bytecode writes; a fresh five-task run completed and unchanged resume cached all five tasks with zero resubmissions. This is a five-task small-data software check, not the full default research search or cloud validation.
- Both actual provider profiles render with empty stderr using pinned nf-amazon 3.12.1 and officially hash-verified nf-google 1.29.1. Native GCS mount options explicitly map UID/GID 10001; actual Batch VM acceptance and read/write permissions still require a live PREPARE.
- Against frozen 5.2 portable.3: research AST identical excluding version/docstring; intake, science configuration, representation modules, scoring, default recipe and numeric lock byte-identical. Both clouds invoke these same modules.
- Explicit --config scientific overrides and --drop-columns intake exclusions are supported. Missing values/scaling/orientation are not silently inferred. Minimum 51 objects remains enforced, including standalone PCA/ICA. Dropping columns from fitting does not redact the source file uploaded to cloud storage.
- Current gcpfix02 image: 38 local container tests passed on Python 3.12.14; non-root default WORKDIR and tiny synthetic PREPARE-through-ranking checks passed. The image is public at the digest in DEPLOY_GCP.md. The old multicloud.1 image/17-test receipt and 182-task stub checks remain historical.

## Freeze 5.3 stable: AWS + GCP interoperability (23 November 2026)

- Image: `docker.io/zymlam/dimple-gwas-f5:5.3.0@sha256:4398934e14aded2b5ec2c891f39a2d0f559522cf276799997a49f4a45c24a383` (also tagged `5.3.0-research-multicloud.2-gcpfix02`). AWS pulled it from Docker Hub; GCP used a regional Artifact Registry mirror of the identical digest.
- Source: this package, with the Google Batch profile staging task inputs by copy (`process.stageInMode = 'copy'`). Science modules, recipe and scoring are unchanged and byte-identical to the files in the image.
- Run: the default digits benchmark on AWS Batch and on Google Batch with identical input, grid, pixels and object-ID hashes and identical post-hoc commands. Both runs produced a COMPLETE_POOL of 2,430 candidates.
- Result: ARI 1.0 (object-ID aligned, noise as its own label) for the primary K, K_eom, K_leaf and legacy global winners; all 2,430 matched candidates ARI 1.0. Embeddings were bit-identical (3/3) and label arrays identical (9/9); only timings and run hashes differed.
- Scope: this establishes cross-cloud reproducibility on the digits benchmark. Representative full runs on intended research data, and their scientific acceptance, are evaluated separately. No real participant matrix or 2,315-trait data was used in this qualification.
