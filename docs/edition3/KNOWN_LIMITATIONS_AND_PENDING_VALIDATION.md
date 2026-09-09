# Known limitations and pending validation

This file is the reader-facing translation of the Stage 1 unresolved-evidence register. Open items do not imply that the software path is broken. They define claims that the present evidence cannot support.

## Scientific analyses not freshly reproduced

- The 2,315-IDP primary matrix is absent. Its reported 15-cluster, 153-noise result and retained 2,430-row model table can be discussed, and its legacy score can be reconstructed, but the embedding and labels cannot be freshly refitted.
- The 459-IDP secondary matrix and complete model table are absent, and retained parameter records conflict. Edition 3 does not issue a reproduction YAML or choose one parameter record by editorial judgment.
- The exact 164-IDP input and retained selected artifacts exist, but the fresh 1,000-seed Freeze 3 refit remains pending. Exact schema adaptation, retained-label comparison, and the 333-row score reconstruction are not described as refitting.

## Statistical and biological validation still open

- No real-data stability study has yet varied seed, metric, RINT, feature set, or hyperparameters under a prespecified analysis plan.
- Same-data biological characterization after clustering remains descriptive unless independent data, sample splitting, or valid selection-aware inference is supplied.
- No matched benchmark supports superiority or equivalence claims against genomic PCA/ICA, Genomic SEM, MTAG, PLEIO, MOSTest, or vertex-wise alternatives.
- The requested external ABCD validation package was not located.

## Release and environment limits

- The live source tree has no Git commit or signed tag. Per-file and package-source SHA-256 identities are used.
- Stage 1 ran on macOS arm64 using the retained Freeze 2 environment with Freeze 3 source. A project-scoped clean Freeze 3 environment was not created.
- Docker, Linux, x86-64, GCP, AWS, and cross-library concordance remain untested.
- `openpyxl` and `xlrd` were absent. Forty-four tests passed; one optional XLSX test skipped; five warnings were preserved.

## Publication hygiene

Private runtime manifests and logs can contain absolute machine paths. Publishable copies must be sanitized while the original evidence remains immutable. The verified bibliography records DOI or authoritative URL identity, but publisher snapshots are not archived locally.

## Evidence needed to change these statements

A limitation closes only through a retained artifact tied to its exact input, configuration, environment, command, output, and acceptance rule. Rewording a claim, rerendering the book, or pinning a container does not itself close a scientific or cross-platform gate.
