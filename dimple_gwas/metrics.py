"""Candidate and embedding metrics with explicit geometry and failure reporting."""

from __future__ import annotations

import math
from typing import Any


def effective_neighbor_count(n_samples: int, requested: int) -> int:
    if n_samples < 3:
        return 0
    return min(int(requested), max(1, (n_samples - 1) // 2))


def embedding_quality_metrics(
    original,
    embedding,
    requested_k: int,
    max_samples: int,
    seed: int,
) -> dict[str, Any]:
    import numpy as np
    from sklearn.manifold import trustworthiness as sklearn_trustworthiness

    source = np.asarray(original)
    projected = np.asarray(embedding)
    sampled = False
    original_count = int(source.shape[0])
    if max_samples > 0 and source.shape[0] > max_samples:
        rng = np.random.default_rng(int(seed))
        selected = rng.choice(source.shape[0], size=int(max_samples), replace=False)
        source = source[selected]
        projected = projected[selected]
        sampled = True
    used_k = effective_neighbor_count(source.shape[0], requested_k)
    if used_k < 1:
        trust = continuity = float("nan")
    else:
        trust = float(sklearn_trustworthiness(source, projected, n_neighbors=used_k, metric="euclidean"))
        continuity = float(sklearn_trustworthiness(projected, source, n_neighbors=used_k, metric="euclidean"))
    return {
        "trustworthiness": trust,
        "continuity": continuity,
        "trust_k_requested": int(requested_k),
        "trust_k_used": int(used_k),
        "trust_sampled": bool(sampled),
        "trust_sample_size": int(source.shape[0]),
        "trust_original_sample_size": original_count,
        "embedding_quality_metric": "euclidean",
    }


def _cluster_sizes(labels):
    import numpy as np

    labels = np.asarray(labels)
    return np.asarray([int((labels == label).sum()) for label in np.unique(labels) if label != -1], dtype=float)


def evaluate_candidate(
    embedding,
    labels,
    clusterer,
    silhouette_metric: str,
    fit_include_noise: bool,
    compute_dbcv: bool,
    max_samples_silhouette: int = 0,
    silhouette_seed: int = 42,
) -> dict[str, Any]:
    import numpy as np
    from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_score

    labels = np.asarray(labels)
    sizes = _cluster_sizes(labels)
    sample_count = int(labels.size)
    noise_count = int((labels == -1).sum())
    cluster_count = int(sizes.size)
    non_noise = labels != -1
    warnings: list[str] = []

    metrics: dict[str, Any] = {
        "number_of_clusters": cluster_count,
        "number_of_noise_points": noise_count,
        "noise_fraction": noise_count / sample_count if sample_count else float("nan"),
        "largest_cluster_size": int(sizes.max()) if sizes.size else 0,
        "largest_cluster_fraction": (float(sizes.max()) / sample_count) if sizes.size and sample_count else 0.0,
        "smallest_cluster_size": int(sizes.min()) if sizes.size else 0,
        "median_cluster_size": float(np.median(sizes)) if sizes.size else float("nan"),
        "mean_cluster_size": float(np.mean(sizes)) if sizes.size else float("nan"),
        "cluster_size_dispersion": (
            float(np.std(sizes, ddof=0) / np.mean(sizes)) if sizes.size and np.mean(sizes) else float("nan")
        ),
        "silhouette": float("nan"),
        "silhouette_scope": "including_noise" if fit_include_noise else "non_noise",
        "silhouette_metric": silhouette_metric,
        "silhouette_sampled": False,
        "silhouette_sample_size": 0,
        "calinski_harabasz": float("nan"),
        "calinski_harabasz_metric": "euclidean",
        "davies_bouldin": float("nan"),
        "davies_bouldin_metric": "euclidean",
        "dbcv": float("nan"),
        "dbcv_metric": silhouette_metric,
        "hdbscan_persistence_mean": float("nan"),
        "hdbscan_persistence_median": float("nan"),
        "hdbscan_persistence_min": float("nan"),
        "hdbscan_persistence_max": float("nan"),
    }

    persistence = np.asarray(getattr(clusterer, "cluster_persistence_", []), dtype=float)
    if persistence.size:
        metrics.update({
            "hdbscan_persistence_mean": float(np.mean(persistence)),
            "hdbscan_persistence_median": float(np.median(persistence)),
            "hdbscan_persistence_min": float(np.min(persistence)),
            "hdbscan_persistence_max": float(np.max(persistence)),
        })

    if cluster_count < 2:
        metrics["metric_warnings"] = "fewer than two non-noise clusters"
        return metrics

    silhouette_mask = np.ones(sample_count, dtype=bool) if fit_include_noise else non_noise
    silhouette_indices = np.flatnonzero(silhouette_mask)
    if max_samples_silhouette > 0 and silhouette_indices.size > max_samples_silhouette:
        rng = np.random.default_rng(int(silhouette_seed))
        silhouette_indices = np.sort(rng.choice(
            silhouette_indices, size=int(max_samples_silhouette), replace=False
        ))
        metrics["silhouette_sampled"] = True
    metrics["silhouette_sample_size"] = int(silhouette_indices.size)
    silhouette_labels = labels[silhouette_indices]
    if np.unique(silhouette_labels).size >= 2 and silhouette_labels.size > np.unique(silhouette_labels).size:
        try:
            metrics["silhouette"] = float(
                silhouette_score(embedding[silhouette_indices], silhouette_labels, metric=silhouette_metric)
            )
        except Exception as exc:
            warnings.append(f"silhouette failed: {type(exc).__name__}: {exc}")

    if non_noise.sum() > cluster_count:
        try:
            metrics["calinski_harabasz"] = float(calinski_harabasz_score(embedding[non_noise], labels[non_noise]))
        except Exception as exc:
            warnings.append(f"Calinski-Harabasz failed: {type(exc).__name__}: {exc}")
        try:
            metrics["davies_bouldin"] = float(davies_bouldin_score(embedding[non_noise], labels[non_noise]))
        except Exception as exc:
            warnings.append(f"Davies-Bouldin failed: {type(exc).__name__}: {exc}")

    if compute_dbcv:
        try:
            from hdbscan.validity import validity_index

            metrics["dbcv"] = float(validity_index(
                np.asarray(embedding, dtype=np.float64), labels, metric=silhouette_metric
            ))
        except Exception as exc:
            warnings.append(f"DBCV unavailable: {type(exc).__name__}: {exc}")

    metrics["metric_warnings"] = " | ".join(warnings)
    return metrics


def is_finite_number(value: Any) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False
