# Attribution and third-party components

The original DIMPLE source is copyright 2025 COGENT Lab Github and is supplied under the [MIT License](../LICENSE). Freeze 5.2 derives the workflow, research stages, fixed recipe and scoring from the exact Freeze 5.1 research snapshot listed in [provenance](../conf/source-origin.json). The scoring module retains its original source text. The two example matrices are synthetic values generated for this release. They contain no participant, clinical, genotype or benchmark source data.

This source archive includes Python code, Nextflow code, infrastructure templates, and wheel hashes. Java, Nextflow, nf-amazon, AWS CLI, the Python base image, wheels, and all other runtime binaries are resolved separately. Each has its own license and notices. Keep those notices intact when building, and review the resulting image's package and OS inventory and its redistribution terms before pushing it.

- [Nextflow source and license](https://github.com/nextflow-io/nextflow)
- [AWS CLI source and license](https://github.com/aws/aws-cli)
- [Docker Official Image for Python](https://github.com/docker-library/python)
- [Scientific Python dependency versions and hashes](../deploy/requirements-linux-amd64.lock)

Portable.3 bundles the existing DIMPLE-GWAS canonical config.py, pca_runner.py and ica_runner.py implementations under bin/dimple_representations. Their source-byte hashes are pinned in self-contained tests and source_manifest.json. They are reused rather than replaced with new approximations; see repository LICENSE.
