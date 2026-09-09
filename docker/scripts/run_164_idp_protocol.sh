#!/usr/bin/env bash
# This protocol prints a reviewable plan only; no implicit expensive fit or data upload.
set -euo pipefail
if [[ $# -ne 0 && ${1:-} != --plan ]]; then
  echo 'Only --plan is implemented. Fresh 164-IDP execution is a separate scientific gate.' >&2
  exit 64
fi
cat <<'PLAN'
Fresh 164-IDP 1,000-seed protocol: NOT RUN by Docker smoke validation.

Prerequisites:
1. Verify exact read-only input SHA256 0cc17db052e28e3c1cd7600f7140f9b929b9e2d2a5b4f9ded3ebf4df3e032f96.
2. Verify annotation SHA256 b664e6139e18305168327c5420c1a1af8379312f3ce0645f5f42dbcc394febc4.
3. Record immutable image/wheel/source/environment identity and canonical native AMD64 resources.
4. Resolve the historical -0.154 versus 0.846 score semantic discrepancy and exact legacy provenance.
5. Use original_idp_164_selected.yaml: no RINT/PCA, densMAP3D, 30 neighbors,
   seeds1..1000 in order, 3000 concatenated dimensions, HDBSCAN epsilon0,
   min_samples4/min_cluster_size6, EOM, noise included in historical score.
6. Retain per-seed block mapping and capture resource measurements before full launch.
7. Execute in a fresh separate output directory with reviewed memory/CPU/time budget.
8. Validate and compare IDs, permutation-invariant labels, noise mask, cluster sizes,
   geometry per independently aligned seed block, original-space summaries, scores,
   and the historical manually selected row16. Do not force a five-cluster outcome.

Retained-artifact identity and a one-seed smoke test cannot pass this gate.
The historical 2,315-IDP primary analysis is outside this protocol.
PLAN
