# Owner supplies an immutable linux/amd64 CPython 3.12.14 Bookworm image with unzip.
ARG PYTHON_BASE
FROM ${PYTHON_BASE} AS cli

ARG AWS_CLI_ZIP_SHA256
COPY --from=verified_cli awscliv2.zip /tmp/awscliv2.zip
RUN case "${AWS_CLI_ZIP_SHA256}" in (*[!a-f0-9]*|'') exit 2;; esac \
 && test "${#AWS_CLI_ZIP_SHA256}" -eq 64 \
 && echo "${AWS_CLI_ZIP_SHA256}  /tmp/awscliv2.zip" | sha256sum -c - \
 && unzip -q /tmp/awscliv2.zip -d /tmp/awscli \
 && /tmp/awscli/aws/install --install-dir /opt/aws-cli --bin-dir /usr/local/bin

FROM ${PYTHON_BASE}
COPY --from=cli /opt/aws-cli /opt/aws-cli
COPY deploy/requirements-linux-amd64.lock /tmp/requirements.lock
RUN ln -s /opt/aws-cli/v2/current/bin/aws /usr/local/bin/aws \
 && python -m pip install --only-binary=:all: --require-hashes --no-cache-dir -r /tmp/requirements.lock \
 && python -m pip check \
 && python -c 'import hdbscan, numpy, pandas, sklearn, umap' \
 && aws --version \
 && rm /tmp/requirements.lock

COPY bin/research.py bin/freeze5_scoring.py bin/matrix_intake.py bin/science_config.py /opt/dimple/bin/
COPY conf/recipe.json /opt/dimple/conf/
COPY VERSION LICENSE main.nf nextflow.config source_manifest.json /opt/dimple/
COPY docs/ATTRIBUTION.md /opt/dimple/docs/
LABEL org.opencontainers.image.title="DIMPLE Freeze 5.2 research worker" \
      org.opencontainers.image.version="5.2.0-research-portable.3"
ENV HOME=/tmp
USER 10001
ENTRYPOINT []

COPY bin/dimple_representations /opt/dimple/bin/dimple_representations/
