from __future__ import annotations

import numpy as np

import dimple_gwas.pipeline as pipeline
from dimple_gwas.provenance import sha256_file
from dimple_gwas.search_space import enumerate_candidates


def test_failed_candidate_is_retained(monkeypatch, small_run_config):
    candidate = enumerate_candidates(small_run_config)[0]
    monkeypatch.setattr(pipeline, "fit_hdbscan", lambda *args, **kwargs: (_ for _ in ()).throw(ValueError("intentional")))
    row = pipeline._evaluate_one(
        candidate,
        np.zeros((10, 2)),
        {},
        0.1,
        [42],
        False,
        False,
        1,
        0,
        42,
    )
    assert row["status"] == "failed"
    assert "intentional" in row["error_message"]
    assert row["model_id"] == candidate["model_id"]


def test_authoritative_source_hash_unchanged():
    assert sha256_file("../DIMPLE-GWAS-dev/DIMPLEGWAS.py") == "c07bb1796066b1e97295945badc78568651255c0721f3f0b337221ad8a671123"
