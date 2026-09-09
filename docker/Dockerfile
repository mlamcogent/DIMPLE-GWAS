ARG PYTHON_BASE=python:3.12.14-slim-bookworm@sha256:9c47360a2a0355e2da18516d0b1c2126ec22c195d2185e97347c9d98398c5bef
FROM ${PYTHON_BASE} AS freeze3-wheel
ARG SOURCE_DATE_EPOCH
ENV SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH} PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /build/source
COPY source/ /build/source/
COPY wheelhouse/ /build/wheelhouse/
COPY locks/build.lock /build/build.lock
RUN python -m pip install --no-index --find-links=/build/wheelhouse --require-hashes -r /build/build.lock \
 && python -m build --no-isolation --wheel --outdir /out .

FROM scratch AS wheel-export
COPY --from=freeze3-wheel /out/ /

FROM ${PYTHON_BASE} AS runtime-environment
ARG SOURCE_DATE_EPOCH
ARG WHEEL_SHA256
ENV SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH} \
    PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=0 NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 \
    MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
    LOKY_MAX_CPU_COUNT=1 TZ=UTC LC_ALL=C.UTF-8 LANG=C.UTF-8 \
    NUMBA_CACHE_DIR=/tmp/numba MPLCONFIGDIR=/tmp/matplotlib \
    XDG_CACHE_HOME=/tmp/cache HOME=/tmp
COPY wheelhouse/ /staging/wheelhouse/
COPY locks/ /staging/locks/
COPY wheel/ /staging/wheel/
RUN python -m venv /opt/venv \
 && /opt/venv/bin/python -m pip install --no-index --find-links=/staging/wheelhouse --require-hashes -r /staging/locks/pip.lock \
 && /opt/venv/bin/python -m pip install --no-index --find-links=/staging/wheelhouse --require-hashes --report /opt/runtime-install-report.json -r /staging/locks/runtime.lock \
 && printf '%s  %s\n' "${WHEEL_SHA256}" /staging/wheel/dimple_gwas-3.0.0rc1-py3-none-any.whl | sha256sum -c - \
 && /opt/venv/bin/python -m pip install --no-index --no-deps /staging/wheel/dimple_gwas-3.0.0rc1-py3-none-any.whl \
 && /opt/venv/bin/python -m pip check \
 && /opt/venv/bin/python -m pip list --format=json > /opt/runtime-packages-with-installer.json

FROM runtime-environment AS freeze3-test
RUN /opt/venv/bin/python -m pip install --no-index --find-links=/staging/wheelhouse --require-hashes -r /staging/locks/test.lock \
 && /opt/venv/bin/python -m pip check \
 && groupadd --gid 10001 dimple \
 && useradd --uid 10001 --gid 10001 --no-create-home --home-dir /tmp --shell /usr/sbin/nologin dimple
ENV PATH=/opt/venv/bin:$PATH
USER 10001:10001
WORKDIR /data/output
ENTRYPOINT ["/opt/venv/bin/python"]
CMD ["-m", "pytest", "--help"]

FROM runtime-environment AS runtime-clean
RUN /opt/venv/bin/python -m pip uninstall --yes pip \
 && find /opt/venv -type d -name __pycache__ -prune -exec rm -rf '{}' +

FROM ${PYTHON_BASE} AS freeze3-runtime
ARG SOURCE_DATE_EPOCH
ARG SOURCE_SHA256
ARG WHEEL_SHA256
ARG LOCK_SHA256
ARG VARIANT=current
ENV PATH=/opt/venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
    NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 LOKY_MAX_CPU_COUNT=1 \
    TZ=UTC LC_ALL=C.UTF-8 LANG=C.UTF-8 \
    NUMBA_CACHE_DIR=/tmp/numba MPLCONFIGDIR=/tmp/matplotlib \
    XDG_CACHE_HOME=/tmp/cache HOME=/tmp
RUN /usr/local/bin/python -m pip uninstall --yes pip \
 && groupadd --gid 10001 dimple \
 && useradd --uid 10001 --gid 10001 --no-create-home --home-dir /tmp --shell /usr/sbin/nologin dimple \
 && mkdir -p /data/input /data/output /opt/dimple \
 && chown 10001:10001 /data/output
COPY --from=runtime-clean /opt/venv /opt/venv
COPY --from=runtime-environment /opt/runtime-packages-with-installer.json /opt/dimple/build-package-manifest.json
COPY wheel/ /opt/dimple/wheel/
COPY locks/runtime.lock /opt/dimple/runtime.lock
COPY LICENSE source.json /opt/dimple/
LABEL org.opencontainers.image.title="DIMPLE-GWAS Freeze 3 RC1" \
      org.opencontainers.image.version="3.0.0rc1" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.revision="sha256:${SOURCE_SHA256}" \
      org.opencontainers.image.description="Locked CPU Linux AMD64 release-candidate runtime; qualification limits in accompanying report" \
      org.dimple.source.identity.kind="content-sha256-no-git" \
      org.dimple.wheel.sha256="${WHEEL_SHA256}" \
      org.dimple.lock.sha256="${LOCK_SHA256}" \
      org.dimple.variant="${VARIANT}" \
      org.dimple.source-date-epoch="${SOURCE_DATE_EPOCH}"
USER 10001:10001
WORKDIR /data/output
ENTRYPOINT ["dimple-gwas"]
CMD ["--help"]

FROM freeze3-test AS freeze3-current-test
FROM freeze3-runtime AS freeze3-current-runtime
