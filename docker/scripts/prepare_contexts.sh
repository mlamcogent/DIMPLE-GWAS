#!/usr/bin/env bash
set -euo pipefail
DIMPLE_SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
DIMPLE_KIND="${1:?First argument must be wheel or current}"
shift
case "$DIMPLE_KIND" in wheel|current) ;; *) exit 2 ;; esac
exec python3 "$DIMPLE_SCRIPT_DIR/pipeline.py" "prepare-$DIMPLE_KIND" "$@"
