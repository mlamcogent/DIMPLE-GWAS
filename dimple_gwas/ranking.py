"""Deterministic ranking, top-N selection, family summaries, and Pareto reporting."""

from __future__ import annotations

from typing import Iterable


def rank_models(frame):
    import pandas as pd

    result = frame.copy()
    result["rank"] = pd.Series(pd.NA, index=result.index, dtype="Int64")
    eligible = result["score"].notna()
    ordered_index = result.loc[eligible].sort_values(
        ["score", "raw_score", "model_id"], ascending=[False, False, True], kind="mergesort"
    ).index
    result.loc[ordered_index, "rank"] = range(1, len(ordered_index) + 1)
    return result.sort_values(
        ["rank", "candidate_ordinal"], ascending=[True, True], na_position="last", kind="mergesort"
    ).reset_index(drop=True)


def top_models(frame, n: int):
    return frame.loc[frame["rank"].notna()].sort_values("rank").head(int(n)).copy()


def pareto_front(frame):
    import numpy as np

    eligible = frame.loc[
        frame["status"].eq("success")
        & frame[["silhouette", "noise_fraction", "largest_cluster_fraction", "number_of_clusters"]].notna().all(axis=1)
    ].copy()
    if eligible.empty:
        eligible["pareto_member"] = []
        return eligible
    objectives = np.column_stack((
        eligible["silhouette"].to_numpy(float),
        -eligible["noise_fraction"].to_numpy(float),
        -eligible["largest_cluster_fraction"].to_numpy(float),
        eligible["number_of_clusters"].to_numpy(float),
    ))
    members = np.ones(len(eligible), dtype=bool)
    for index, candidate in enumerate(objectives):
        if not members[index]:
            continue
        dominates = np.all(objectives >= candidate, axis=1) & np.any(objectives > candidate, axis=1)
        dominates[index] = False
        if dominates.any():
            members[index] = False
    eligible["pareto_member"] = members
    eligible["pareto_objectives"] = "maximize silhouette and clusters; minimize noise_fraction and largest_cluster_fraction"
    return eligible.loc[eligible["pareto_member"]].sort_values(
        ["score", "model_id"], ascending=[False, True], na_position="last"
    )


DEFAULT_FAMILY_COLUMNS = (
    "hdbscan_cluster_selection_method",
    "umap_metric",
    "hdbscan_metric",
    "hdbscan_max_cluster_size",
    "umap_n_neighbors",
    "umap_min_dist",
    "hdbscan_min_cluster_size",
    "hdbscan_min_samples",
    "hdbscan_cluster_selection_epsilon",
)


def family_summaries(frame, columns: Iterable[str] = DEFAULT_FAMILY_COLUMNS):
    import pandas as pd

    rows = []
    for column in columns:
        if column not in frame.columns:
            continue
        for value, group in frame.groupby(column, dropna=False):
            successful = group[group["status"].eq("success")]
            scored = group[group["score"].notna()]
            rows.append({
                "family_dimension": column,
                "family_value": value,
                "candidate_models": int(len(group)),
                "successful_models": int(len(successful)),
                "failed_models": int(group["status"].eq("failed").sum()),
                "invalid_topology_models": int(group["status"].eq("invalid_topology").sum()),
                "best_score": float(scored["score"].max()) if not scored.empty else float("nan"),
                "median_score": float(scored["score"].median()) if not scored.empty else float("nan"),
                "median_silhouette": float(successful["silhouette"].median()) if not successful.empty else float("nan"),
                "median_noise_fraction": float(successful["noise_fraction"].median()) if not successful.empty else float("nan"),
                "median_number_of_clusters": float(successful["number_of_clusters"].median()) if not successful.empty else float("nan"),
            })
    return pd.DataFrame(rows)

