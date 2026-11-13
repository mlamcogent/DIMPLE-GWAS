# DIMPLE Freeze 5.2

Freeze 5.2 is a portable research workflow for clustering objects described by a dense numeric feature matrix. Nextflow runs the approved nine-configuration DensMAP and HDBSCAN study on native AWS Batch. Each deployment uses the operator's private storage, queue, roles, and digest-pinned worker image.

- [Deployment sheet](docs/DEPLOY_AWS.md) walks through local input checks, owner-reviewed AWS setup, a one-job staging check, a full run, and cleanup.
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
