"""Transparent scoring profiles, independent of search enumeration."""

from __future__ import annotations

from typing import Any, Mapping


LEGACY_COLUMN_ALIASES = {
    "Silhouette_avg": "silhouette",
    "Clusters": "number_of_clusters",
    "Noise_points": "number_of_noise_points",
    "Min_samples": "hdbscan_min_samples",
    "Min_cluster_size": "hdbscan_min_cluster_size",
    "Epsilon": "hdbscan_cluster_selection_epsilon",
}


LEGACY_FORMULA = (
    "For eligible candidates, component_normalized = component / component.max(). "
    "Each component weight is its raw dynamic range divided by the sum of raw ranges. "
    "raw_score = w_silhouette*silhouette_normalized + "
    "w_clusters*number_of_clusters_normalized - w_noise*noise_points_normalized. "
    "When score_noise_penalty=false (legacy fit_include_noise=false), noise_points_for_score=0 and w_noise=0. "
    "score=(raw_score-min(raw_score))/(max(raw_score)-min(raw_score)); a zero score range maps to 1."
)


def normalize_model_table_schema(frame):
    """Adapt the historical notebook table schema without discarding source fields."""

    import pandas as pd

    result = frame.copy()
    migrated: dict[str, str] = {}
    for source, destination in LEGACY_COLUMN_ALIASES.items():
        if destination not in result.columns and source in result.columns:
            result[destination] = result[source]
            migrated[source] = destination
    required = {"silhouette", "number_of_clusters", "number_of_noise_points"}
    missing = sorted(required - set(result.columns))
    if missing:
        raise ValueError(f"Model table lacks required scoring columns: {missing}")
    if "status" not in result.columns:
        result["status"] = "success"
        migrated["<implicit>"] = "status=success"
    if "candidate_ordinal" not in result.columns:
        result["candidate_ordinal"] = range(1, len(result) + 1)
        migrated["<row order>"] = "candidate_ordinal"
    if "model_id" not in result.columns:
        result["model_id"] = [f"legacy_row_{index:06d}" for index in range(1, len(result) + 1)]
        migrated["<row order>"] = "model_id"
    for column in ("Score", "Score_raw", "score", "raw_score"):
        if column in result.columns:
            destination = f"source_{column}"
            if destination not in result.columns:
                result[destination] = result[column]
    return result, {"column_migrations": migrated, "source_rows": int(len(result))}


def _safe_divide_by_max(series):
    import pandas as pd

    maximum = series.max()
    if pd.isna(maximum) or maximum == 0:
        return pd.Series(0.0, index=series.index, dtype=float)
    return series.astype(float) / float(maximum)


def _scale_final(raw):
    import pandas as pd

    minimum = float(raw.min())
    maximum = float(raw.max())
    score_range = maximum - minimum
    if pd.isna(score_range) or score_range <= 0:
        return pd.Series(1.0, index=raw.index, dtype=float)
    return (raw - minimum) / score_range


def legacy_dimple_score(frame, fit_include_noise: bool = False):
    import numpy as np
    import pandas as pd

    result = frame.copy()
    result["raw_score"] = np.nan
    result["score"] = np.nan
    result["Score_raw"] = np.nan
    result["Score"] = np.nan
    result["scoring_profile"] = "legacy_dimple"
    result["fit_include_noise"] = bool(fit_include_noise)
    eligible = result['status'].eq('success')
    for column in ('silhouette', 'number_of_clusters', 'number_of_noise_points'):
        if not np.isfinite(pd.to_numeric(result.loc[eligible, column], errors='coerce')).all():
            raise ValueError('Nonfinite scoring values: ' + column)
    if not eligible.any():
        return result, {
            "profile": "legacy_dimple",
            "formula": LEGACY_FORMULA,
            "fit_include_noise": bool(fit_include_noise),
            "eligible_models": 0,
            "weights": {},
        }

    for column in ('silhouette', 'number_of_clusters', 'number_of_noise_points'):
        if not np.isfinite(result.loc[eligible, column].astype(float)).all():
            raise ValueError('Nonfinite scoring values: ' + column)
    work = result.loc[eligible, ["silhouette", "number_of_clusters", "number_of_noise_points"]].astype(float).copy()
    work["noise_points_for_score"] = work["number_of_noise_points"] if fit_include_noise else 0.0
    work["silhouette_normalized"] = _safe_divide_by_max(work["silhouette"])
    work["clusters_normalized"] = _safe_divide_by_max(work["number_of_clusters"])
    work["noise_normalized"] = _safe_divide_by_max(work["noise_points_for_score"])

    ranges = {
        "silhouette": float(work["silhouette"].max() - work["silhouette"].min()),
        "number_of_clusters": float(work["number_of_clusters"].max() - work["number_of_clusters"].min()),
        "number_of_noise_points": float(work["noise_points_for_score"].max() - work["noise_points_for_score"].min()),
    }
    total_range = sum(ranges.values())
    if not np.isfinite(total_range) or total_range <= 0:
        if fit_include_noise:
            weights = {"silhouette": 1 / 3, "number_of_clusters": 1 / 3, "number_of_noise_points": 1 / 3}
        else:
            weights = {"silhouette": 0.5, "number_of_clusters": 0.5, "number_of_noise_points": 0.0}
    else:
        weights = {key: value / total_range for key, value in ranges.items()}
    raw = (
        weights["silhouette"] * work["silhouette_normalized"]
        + weights["number_of_clusters"] * work["clusters_normalized"]
        - weights["number_of_noise_points"] * work["noise_normalized"]
    )
    score = _scale_final(raw)
    result.loc[eligible, "raw_score"] = raw
    result.loc[eligible, "score"] = score
    result.loc[eligible, "Score_raw"] = raw
    result.loc[eligible, "Score"] = score
    return result, {
        "profile": "legacy_dimple",
        "formula": LEGACY_FORMULA,
        "fit_include_noise": bool(fit_include_noise),
        "eligible_models": int(eligible.sum()),
        "raw_ranges": ranges,
        "weights": weights,
        "edge_cases": {
            "zero_component_max": "normalized component is 0",
            "zero_total_range": "equal weights across active components",
            "zero_final_range": "all eligible scores are 1",
            "ineligible": "status is not success or silhouette is unavailable; score is null",
        },
    }


def custom_score(frame, rules: Mapping[str, Mapping[str, Any]]):
    import numpy as np
    import pandas as pd

    missing = set(rules) - set(frame.columns)
    if missing:
        raise ValueError(f"Custom scoring metrics are absent from model table: {sorted(missing)}")
    result = frame.copy()
    result["raw_score"] = np.nan
    result["score"] = np.nan
    result["Score_raw"] = np.nan
    result["Score"] = np.nan
    result["scoring_profile"] = "custom"
    for metric, rule in rules.items():
        weight = float(rule.get("weight", 0))
        if not np.isfinite(weight) or weight < 0 or rule.get('direction') not in {'maximize', 'minimize'}:
            raise ValueError('Invalid custom scoring rule: ' + metric)
    active = {metric: rule for metric, rule in rules.items() if float(rule.get("weight", 0)) > 0}
    if not active:
        raise ValueError('At least one custom score weight must be > 0')
    eligible = result["status"].eq("success")
    for metric in active:
        if not np.isfinite(pd.to_numeric(result.loc[eligible, metric], errors='coerce')).all():
            raise ValueError('Nonfinite custom scoring values: ' + metric)
    if not eligible.any():
        raise ValueError("No successful model has every metric required by custom scoring")
    total_weight = sum(float(rule["weight"]) for rule in active.values())
    if not np.isfinite(total_weight):
        raise ValueError('Total custom score weight must be finite')
    raw = pd.Series(0.0, index=result.index[eligible], dtype=float)
    normalized_rules = {}
    for metric, rule in active.items():
        values = result.loc[eligible, metric].astype(float)
        if not np.isfinite(values).all():
            raise ValueError("Nonfinite custom scoring values: " + metric)
        minimum = float(values.min())
        maximum = float(values.max())
        if maximum == minimum:
            normalized = pd.Series(0.0, index=values.index)
        else:
            normalized = (values - minimum) / (maximum - minimum)
        if rule["direction"] == "minimize":
            normalized = 1.0 - normalized
        weight = float(rule["weight"]) / total_weight
        raw += weight * normalized
        normalized_rules[metric] = {"weight": weight, "direction": rule["direction"], "minimum": minimum, "maximum": maximum}
    score = _scale_final(raw)
    result.loc[eligible, "raw_score"] = raw
    result.loc[eligible, "score"] = score
    result.loc[eligible, "Score_raw"] = raw
    result.loc[eligible, "Score"] = score
    return result, {
        "profile": "custom",
        "formula": "Weighted sum of per-metric min-max normalized values after applying declared direction; final raw scores rescaled to [0,1].",
        "eligible_models": int(eligible.sum()),
        "metrics": normalized_rules,
        "edge_cases": {"zero_metric_range": "normalized component is 0", "zero_final_range": "all eligible scores are 1"},
    }


def apply_scoring(frame, scoring_config: Mapping[str, Any]):
    profile = scoring_config.get("profile", "legacy_dimple")
    scope, penalty = noise_policies(scoring_config)
    if profile == "legacy_dimple":
        scored, manifest = legacy_dimple_score(frame, penalty)
        scored['score_noise_penalty'] = penalty
        manifest.update({'silhouette_noise_policy_for_new_fits': scope, 'score_noise_penalty': penalty,
                         'stored_silhouette_recomputed': False,
                         'score_scope': 'within supplied eligible population; not manuscript reported fit'})
        return scored, manifest
    if profile == "custom":
        return custom_score(frame, scoring_config.get("custom", {}))
    raise ValueError(f"Unknown scoring profile: {profile}")


def noise_policies(scoring):
    """Legacy-only preserves both coupled decisions. Explicit pair is independent."""
    keys = {'silhouette_noise_policy', 'score_noise_penalty'}
    if keys & scoring.keys():
        if not keys <= scoring.keys():
            raise ValueError('Both explicit noise controls are required')
        scope, penalty = scoring['silhouette_noise_policy'], scoring['score_noise_penalty']
        if scope not in {'non_noise', 'including_noise'} or not isinstance(penalty, bool):
            raise ValueError('Invalid explicit noise controls')
        if 'fit_include_noise' in scoring:
            legacy = scoring['fit_include_noise']
            if not isinstance(legacy, bool) or penalty != legacy or (scope == 'including_noise') != legacy:
                raise ValueError('Legacy and explicit noise controls conflict; remove legacy flag to migrate')
        return scope, penalty
    legacy = scoring.get('fit_include_noise', False)
    if not isinstance(legacy, bool):
        raise ValueError('fit_include_noise must be boolean')
    return ('including_noise' if legacy else 'non_noise'), legacy
