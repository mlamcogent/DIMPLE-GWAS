# Technical reference: provenance and release status

## Identity

The live Freeze 3 tree is not a Git checkout. The Stage 1 authoritative package-source SHA-256 is `df87825992ab51dc016c673cf420a978ba5c161bd6c755e00a5199ead310e65b`; per-file hashes appear in the source inventory. A hash identifies content but is not a substitute for signed source history.

## Minimum run provenance

Retain software/version, package source digest, input size/hash/path, resolved configuration and digest, command, start/finish timestamps, Python and package versions, OS and architecture, seeds, threads/jobs, backend names, candidate/family counts, warnings/failures/exclusions, selected model ID, artifact hashes and validation status.

## Privacy

Native manifests can contain absolute paths, commands, platform details, filenames and study identifiers. Keep immutable private evidence; create a sanitized publication copy that removes workstation paths and restricted identifiers without changing scientific values. Record the sanitization method and source hash.

## Release matrix

| Layer | Current status |
|---|---|
| Source and local software path | verified by hashes, 44 passing tests and bounded execution |
| Optional XLSX path | one test skipped; dependency absent |
| Fixed synthetic regression | fresh exact local reproduction and structural comparison |
| Historical 164 labels and score table | retained/adapted; score reconstruction exact; fresh refit pending |
| 2,315 and 459 manuscript analyses | reported/retained evidence only; raw matrices absent; 459 parameters conflict |
| Real-data stability | pending |
| Biological/external validation | pending or incomplete |
| Docker/Linux/cloud/cross-platform | pending |

Use the full release-boundary sentence in the front matter. Elsewhere name only the relevant layer.

\newpage
