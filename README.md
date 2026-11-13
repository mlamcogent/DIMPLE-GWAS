# DIMPLE 5.3.0-research-multicloud.2

One package retains AWS Batch and adds Google Batch/GCS, using the same flexible science and explicit matrix intake from frozen 5.2 portable.3. Default published recipe/scoring remain preserved; custom UMAP/seed/HDBSCAN settings and standalone PCA/ICA are deliberate alternatives, not silently substituted defaults.

- AWS: [quickstart](docs/QUICKSTART.md), [deployment](docs/DEPLOY.md), [deployment fixes](docs/DEPLOY_FIXES.md).
- GCP: [deployment sheet](docs/DEPLOY_GCP.md).
- Shared [manual](docs/MANUAL.md), [interoperability](docs/INTEROPERABILITY.md), [current validation](docs/VALIDATION_5_3.md).

**Worker image public:** `docker.io/zymlam/dimple-gwas-f5:5.3.0-research-multicloud.2-gcpfix02@sha256:4398934e14aded2b5ec2c891f39a2d0f559522cf276799997a49f4a45c24a383`. GCP live qualification is pending. This is research software; local tests and image availability are not scientific acceptance.

The inherited 5.2 baseline documentation follows for provenance; the multi-cloud guidance above takes precedence.

# DIMPLE Freeze 5.2

Freeze 5.2 is a portable research workflow for clustering objects described by a dense numeric feature matrix. Nextflow runs the approved nine-configuration DensMAP and HDBSCAN study on native AWS Batch. Each deployment uses the operator's private storage, queue, roles, and digest-pinned worker image.

- [Deployment sheet](docs/DEPLOY.md) walks through local input checks, owner-reviewed AWS setup, a one-job staging check, a full run, and cleanup.
- [User manual](docs/MANUAL.md) covers matrix formats, options, results, and troubleshooting.
- [Science and provenance](docs/SCIENCE.md) defines the fixed recipe, scoring, and traceability.
- [Publisher handoff](docs/RELEASE.md) describes the GitHub source release and Docker Hub worker build.
- [License](LICENSE) and [attribution](docs/ATTRIBUTION.md) identify the source and separate third-party terms.

Start locally with the bundled synthetic matrix. Python 3.9+ is enough for this step.

```bash
mkdir -p .private
python3 bin/matrix_intake.py \
  --matrix examples/synthetic-matrix.csv \
  --orientation objects_by_features --object-id-column object_id \
  --preprocessing none --output .private/run-grid.json
```

The examples exercise software behavior. Scientific suitability for an external dataset requires separate review. The release status and the qualified runtime are tracked independently from the source archive.

Deployment repair01: see docs/DEPLOY_FIXES.md for exact operator steps and qualification limits.
