# Security and distribution status

The current image is retained for local evaluation. Publication is blocked by open
runtime defects and security dispositions. No registry upload, signing or cloud use
occurred. User preference for public repositories under `zymlam` is recorded.

On2026-09-05 the offline Trivy0.74.0 scan reported265 Debian package/advisory records:
5 Critical,55 High,96 Medium,102 Low,7 Unknown. None of the High/Critical records has a
fixed version in that database;6 Unknown records have an available PCRE2 update.
No exception was granted. Some Critical records have component/architecture triage,
but SQLite and disputed Perl applicability remain open. Zero Python-package findings
and zero detected project secrets do not prove complete vulnerability coverage.

Syft1.51.1 records128 components. All19 installed application source files match the
frozen source. No project research data or Dev/test source entered the runtime image.
Forty datasets and embedded public crypto-test keys are byte-verified upstream package
resources.156 licence/notice files were inventoried; public redistribution obligations
still require disposition. No historical Anaconda image was built or cleared.

All evidence, scanner/database/tool hashes, severities, unsuppressed raw results and
licence details are in `/Users/maxlam/Downloads/Cogent-analysis-audit/DIMPLE-GWAS/freeze3_workspace/docker_validation/runs/20260905T083643Z-774bbf2de95d-33a471/security/current-security-assessment.md` and its referenced
machine-readable records. SPDX/CycloneDX files are in `sbom/current-verified/`.

Minimal BuildKit provenance exists in the OCI archive but has an empty statement
subject and incomplete local materials. A separate local unsigned supplement maps the
actual runtime/config subjects to source, wheel, lock, base and context hashes. It is
not a signature, complete independent attestation or registry-attached evidence.

The missing HEALTHCHECK advisory is inapplicable to a terminating batch CLI. Bounded
non-root offline read-only execution was tested; it does not waive the CVE findings.
Do not expose the image as an Internet-facing service or infer publication clearance.
