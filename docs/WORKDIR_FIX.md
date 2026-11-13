# Freeze 5.2 worker working-directory repair

This source patch adds `WORKDIR /tmp` to `deploy/Dockerfile`. It accompanies the blank-account bootstrap repair and does not change science, intake, scoring, recipe, workflow or dependencies. No image build, push or AWS deployment is part of this patch. Use the owner's separately approved fixed image digest when deploying.

The AWS Batch-style shell starts in the image's working directory and stages `.command.run` there before that script can change directory. `HOME=/tmp` alone does not change the current directory. With uid 10001 and a read-only root filesystem, the former default `/` cannot receive that wrapper. The new default `/tmp` works when writable temporary storage is supplied by the runtime.

## Local, offline regression

Run from a clean extract with the existing scientific test environment and Docker. The selected immutable image must already be cached; this test uses `--pull=never`, `--network none`, uid 10001, a read-only root, a writable `/tmp` tmpfs and read-only synthetic fixtures. It does not mount credentials, data or the Docker socket into the container.

```bash
export PYTHONDONTWRITEBYTECODE=1
export DIMPLE_WRAPPER_IMAGE='REPLACE_WITH_CACHED_REPOSITORY_AT_SHA256_OR_IMAGE_SHA256'
export DIMPLE_WRAPPER_RECEIPT="$PWD/../wrapper-receipt.json"
python -m unittest discover -s tests -p test_awsbatch_wrapper.py -v
```

The test runs one real PREPARE task on the included 60-by-3 synthetic matrix via relative `.command.run` and `.command.sh` staging. It verifies output shape, source/input hashes, uid, cwd and the read-only root. A negative control forces cwd `/` and must fail during wrapper staging. Optionally set `DIMPLE_WRAPPER_OLD_IMAGE` to the cached immutable prior image to demonstrate its default fails and `--workdir /tmp` passes.

This is a Batch-style wrapper contract test, not a full Nextflow-generated-wrapper or AWS transport qualification: local read-only fixture copies replace S3 transfers. The test will explicitly skip the actual container case if DIMPLE_WRAPPER_IMAGE is unset. A source-only test pass must not be described as a container pass. The adjacent delivery receipt records the exact tested local image and all cases.
