# GitHub and Docker Hub publisher handoff

Version `5.3.0-research-multicloud.2`. The source archive is the GitHub release input. The release directory contains its archive SHA256 and per-file export manifest. The Docker Hub input is the worker build specification and its pinned inputs, followed by the actual built image and observed registry digest.

## Prepare GitHub source

1. Verify the archive checksum supplied with the release. Extract it into a fresh directory with `tar -xzpf` and run `python3 bin/pack_release.py --verify .` from that extracted directory. Use the exact allowlisted tree as the source commit. Keep repository history, owner overlays, run inputs and deployment state outside the commit.
2. Use the owner's approved DIMPLE-GWAS repository and a dedicated Freeze 5.3 release branch/tag. Confirm the destination and its public visibility with the owner. Preserve Freeze 5 and 5.1. Attach the verified archive and checksum to the release.
3. Record commit, tag and archive digest. Link that exact commit to the Docker build and the resulting image digest. Include the deployment sheet, user manual, standalone Nextflow/configuration and local qualification limits in the release.

## Build and verify the Docker Hub worker

In the clean extracted package, choose a digest-pinned, Linux x86_64 CPython 3.12.14 Debian Bookworm base image with bash, coreutils and Info-ZIP `unzip`. If your standard Python image lacks unzip, prepare and review a derivative base first, then use its immutable digest. Fetch an exact approved AWS CLI v2 Linux x86_64 ZIP and its matching detached signature from AWS. Verify the signature using the AWS CLI team's documented key and verify the key fingerprint. Rename the exact ZIP `awscliv2.zip` in a separate build-context directory. Record the base digest, CLI version and verified ZIP SHA256. The build checks that hash and the exact Linux wheel hashes. The CLI executable is `/usr/local/bin/aws` inside the worker. The source archive includes no CLI installer or dependency binaries. [AWS CLI signature instructions](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

```bash
worker_tag="docker.io/REPLACE_NAMESPACE/REPLACE_WORKER:5.3.0-research-multicloud.2"
docker buildx build --platform linux/amd64 --load \
  --file deploy/Dockerfile --build-context verified_cli="$verified_cli_dir" \
  --build-arg PYTHON_BASE="$verified_python_base_digest_ref" \
  --build-arg AWS_CLI_ZIP_SHA256="$verified_cli_zip_sha256" \
  --tag "$worker_tag" .
docker run --rm --network none --platform linux/amd64 "$worker_tag" \
  bash -euc 'command -v aws; aws --version; python -m pip check; python -c "import hdbscan, numpy, pandas, sklearn, umap"; python /opt/dimple/bin/research.py --help'
```

Before promotion, verify linux/amd64, native Linux start/import behavior, wheel versions, source digests under `/opt/dimple`, absence of private files, and the effective runtime user and security profile. Generate an SBOM and retain required notices and dependency/source obligations. Scan the final image and review findings under the owner's publication policy. Image construction uses pinned inputs. Record the actual image digest after the approved build and push rather than assuming a registry digest from the local source hash.

After explicit release approval, the designated publisher pushes the reviewed tag to the approved Docker Hub repository, verifies the platform manifest and digest, and records the public pull reference `docker.io/<namespace>/<worker>@sha256:<digest>`. Use the immutable reference in deployment settings. The controller runs separately with Java 21, Nextflow 26.10.3 and nf-amazon 3.12.1. A registry mirror needs its own checked digest and access scope.

## Release checks

| Area | Evidence required |
| --- | --- |
| Source | Exact clean archive, file allowlist and hashes, independent software acceptance |
| Image | Recorded base/CLI/wheel identities, verified build, license/notice and security review, image platform and registry digest |
| AWS | One approved staging job followed by a separately approved research run when needed |
| Science | Interpretation on the intended data with separately reviewed provenance and results |
| Publication | Owner-approved GitHub destination/tag and Docker Hub namespace/tag, then confirmed public availability by the designated publisher |
