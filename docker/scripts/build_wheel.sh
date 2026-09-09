#!/usr/bin/env bash
set -euo pipefail
DIMPLE_SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
exec python3 "$DIMPLE_SCRIPT_DIR/pipeline.py" build-wheel "$@"
