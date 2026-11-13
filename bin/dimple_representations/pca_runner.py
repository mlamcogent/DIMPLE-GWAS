"""Deterministic, centered PCA for traits × original SNP features.

No feature scaling, imputation or file I/O occurs here.  For centered ``X`` of
shape T × S, the exported transformation obeys ``scores = X @ components.T``
and ``X_hat = scores @ components``.  Eigenvalues use denominator T - 1;
ICA can whiten selected scores to empirical unit variance using sqrt(T) / s.

Wide inputs use a blockwise T × T Gram matrix, never an S × S covariance
matrix.  Its numerical-rank floor reflects the precision loss from squaring
the spectrum; it must not treat positive roundoff eigenvalues as real signal.
"""

from __future__ import annotations

import time
from numbers import Integral, Real
from typing import Any, Mapping


_FEATURE_BLOCK_SIZE = 4096


def retention_diagnostics(prepared, observations: int, features: int) -> dict[str, Any]:
    """Describe the existing selection without recomputing or changing it."""
    selected_k = int(prepared["selected_k"])
    cumulative = prepared["cumulative_variance_ratio"]
    at_k = float(cumulative[selected_k - 1])
    before_k = None if selected_k == 1 else float(cumulative[selected_k - 2])
    threshold_selection = prepared["selection_mode"] == "variance_threshold"
    target = float(prepared["variance_threshold"]) if threshold_selection else None
    return {
        "selected_k": selected_k,
        "numerical_rank": int(prepared["numerical_rank"]),
        "selection_mode": prepared["selection_mode"],
        "selection_rule": (
            "explicit_component_count" if not threshold_selection else
            ("all_numerically_resolvable_components" if target == 1.0 else
             "smallest_count_reaching_variance_threshold")
        ),
        "threshold_decision_applied": threshold_selection,
        "cumulative_variance_at_k": at_k,
        "cumulative_variance_at_k_minus_1": before_k,
        "target_variance": target,
        "configured_variance_threshold": prepared["variance_threshold"],
        "margin_above_target": None if target is None else at_k - target,
        "margin_below_target": None if target is None or before_k is None else target - before_k,
        "centering_rank_upper_bound": min(observations - 1, features),
        "centering_rank_explanation": "Feature centering across T trait observations enforces rank at most min(T-1, S). Rank T-1 alone does not establish an additional dependency in the uncentered input.",
        "variance_scope": "Selected centered PCA subspace before any ICA whitening or rotation.",
    }


def _validated_values(matrix):
    import numpy as np

    values = matrix.values if hasattr(matrix, "values") else matrix
    try:
        values = np.asarray(values, dtype=np.float64)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("PCA requires a numeric traits × features matrix") from exc
    if values.ndim != 2:
        raise ValueError("PCA requires a two-dimensional traits × features matrix")
    if values.shape[0] < 2:
        raise ValueError("PCA requires at least two trait observations")
    if values.shape[1] < 1:
        raise ValueError("PCA requires at least one SNP/feature")
    # Checking blocks avoids a second full-sized Boolean matrix on wide input.
    for first in range(0, values.shape[1], _FEATURE_BLOCK_SIZE):
        if not np.isfinite(values[:, first:first + _FEATURE_BLOCK_SIZE]).all():
            raise ValueError("PCA input contains nonfinite values (NaN or infinity)")
    return values


def _validate_selection(variance_threshold, retained_components):
    import numpy as np

    threshold_disabled = variance_threshold is None and retained_components is not None
    if not threshold_disabled and (
        isinstance(variance_threshold, (bool, np.bool_))
        or not isinstance(variance_threshold, Real)
        or not np.isfinite(variance_threshold)
        or not 0.0 < variance_threshold <= 1.0
    ):
        raise ValueError("variance_threshold must be finite and in (0, 1]")
    if retained_components is not None and (
        isinstance(retained_components, (bool, np.bool_))
        or not isinstance(retained_components, Integral)
        or retained_components < 1
    ):
        raise ValueError("retained_components must be a positive integer")


def _canonicalize_signs(scores, components):
    """Use the first largest-absolute original-feature coefficient as pivot."""
    import numpy as np

    # argmax returns the first position on a tie, preserving feature order.
    for index in range(components.shape[0]):
        pivot = int(np.argmax(np.abs(components[index])))
        if components[index, pivot] < 0.0:
            components[index] *= -1.0
            scores[:, index] *= -1.0


def prepare_pca(
    matrix,
    variance_threshold: float | None = 0.99,
    retained_components: int | None = None,
) -> dict[str, Any]:
    """Fit one centered, unwhitened PCA representation in float64.

    ``matrix`` is T traits × S original features.  ``retained_components``
    replaces threshold selection when supplied (and permits threshold=None);
    upstream configuration rejects
    contradictory explicit selections within the same configuration layer.
    ``singular_values`` contains selected values, while ``eigenvalues``,
    ``explained_variance_ratio`` and ``cumulative_variance_ratio`` contain the
    full min(T, S) numerical spectrum, including numerical zeros.

    SVD rank tolerance is eps64 * max(T, S) * largest singular value.  For the
    trait-Gram route, eigenvalue roundoff tolerance is eps64 * max(T, S) *
    largest Gram eigenvalue, and rank tolerance is its square root.  This
    conservative Gram tolerance deliberately discards unresolved directions.
    ``rank_tolerance`` is always expressed in singular-value units; the Gram
    roundoff tolerance is expressed in unnormalized Gram-eigenvalue units.
    """
    import numpy as np

    _validate_selection(variance_threshold, retained_components)
    values = _validated_values(matrix)
    observations, features = values.shape
    eps = np.finfo(np.float64).eps
    with np.errstate(over="ignore", invalid="ignore"):
        feature_means = values.mean(axis=0, dtype=np.float64)
    if not np.isfinite(feature_means).all():
        raise ValueError("PCA feature means overflowed float64 precision")

    # SVD is preferable on small/narrow problems.  The dual formulation keeps
    # memory bounded when original SNP features vastly outnumber traits.
    if features <= 2 * observations:
        centered = values - feature_means
        if not np.isfinite(centered).all():
            raise ValueError("PCA centering overflowed float64 precision")
        try:
            left, full_singular_values, all_components = np.linalg.svd(
                centered, full_matrices=False
            )
        except np.linalg.LinAlgError as exc:
            raise ValueError("PCA economy SVD did not converge") from exc
        maximum = float(full_singular_values[0])
        rank_tolerance = eps * max(values.shape) * maximum
        numerical_rank = int(np.count_nonzero(full_singular_values > rank_tolerance))
        with np.errstate(over="ignore", invalid="ignore"):
            squared_spectrum = np.square(full_singular_values)
        squared_spectrum[numerical_rank:] = 0.0
        eigenvalue_roundoff_tolerance = rank_tolerance ** 2
        solver = "economy_svd"
    else:
        gram = np.zeros((observations, observations), dtype=np.float64)
        with np.errstate(over="ignore", invalid="ignore"):
            for first in range(0, features, _FEATURE_BLOCK_SIZE):
                block = values[:, first:first + _FEATURE_BLOCK_SIZE] - feature_means[
                    first:first + _FEATURE_BLOCK_SIZE
                ]
                gram += block @ block.T
        if not np.isfinite(gram).all():
            raise ValueError("PCA trait-Gram matrix overflowed float64 precision")
        # Guarantee symmetry to the eigensolver despite accumulation roundoff.
        gram = (gram + gram.T) * 0.5
        try:
            eigenvalues, left = np.linalg.eigh(gram)
        except np.linalg.LinAlgError as exc:
            raise ValueError("PCA trait-Gram eigendecomposition did not converge") from exc
        squared_spectrum = eigenvalues[::-1].copy()
        left = left[:, ::-1]
        maximum_squared = max(0.0, float(squared_spectrum[0]))
        eigenvalue_roundoff_tolerance = eps * max(values.shape) * maximum_squared
        if np.any(squared_spectrum < -eigenvalue_roundoff_tolerance):
            raise ValueError(
                "PCA trait-Gram matrix has a materially negative eigenvalue "
                f"({float(squared_spectrum.min()):.6g}; roundoff tolerance "
                f"{eigenvalue_roundoff_tolerance:.6g})"
            )
        squared_spectrum[squared_spectrum <= eigenvalue_roundoff_tolerance] = 0.0
        full_singular_values = np.sqrt(squared_spectrum)
        rank_tolerance = float(np.sqrt(eigenvalue_roundoff_tolerance))
        numerical_rank = int(np.count_nonzero(full_singular_values > rank_tolerance))
        solver = "trait_gram_eigh"
        all_components = None

    if numerical_rank == 0:
        raise ValueError("PCA input has zero total centered variance at numerical precision")
    total_squared = float(squared_spectrum.sum())
    if not np.isfinite(total_squared) or total_squared <= 0.0:
        raise ValueError("PCA total centered variance overflowed float64 precision")
    eigenvalues = squared_spectrum / (observations - 1)
    explained_variance_ratio = squared_spectrum / total_squared
    cumulative_variance_ratio = np.cumsum(explained_variance_ratio)
    # Rank and numerical zeros define the full retained numerical variance.
    # Pin its endpoint so threshold=1 cannot request a null direction solely
    # because of floating-point accumulation.
    cumulative_variance_ratio[numerical_rank - 1:] = 1.0
    if retained_components is not None:
        selected_k = int(retained_components)
        if selected_k > numerical_rank:
            raise ValueError(
                f"retained_components={selected_k} exceeds numerical rank {numerical_rank}"
            )
        selection_mode = "retained_components"
    else:
        # Explicit full retention means every numerically resolvable direction,
        # including an SVD tail too small to change a float64 cumulative sum.
        selected_k = numerical_rank if variance_threshold == 1.0 else int(np.searchsorted(
            cumulative_variance_ratio[:numerical_rank], float(variance_threshold), side="left"
        ) + 1)
        selection_mode = "variance_threshold"
    singular_values = full_singular_values[:selected_k].copy()
    scores = (left[:, :selected_k] * singular_values).copy()
    if all_components is not None:
        components = all_components[:selected_k].copy()
    else:
        components = np.empty((selected_k, features), dtype=np.float64)
        # No division by a numerical zero: selection is bounded by rank above.
        for first in range(0, features, _FEATURE_BLOCK_SIZE):
            block = values[:, first:first + _FEATURE_BLOCK_SIZE] - feature_means[
                first:first + _FEATURE_BLOCK_SIZE
            ]
            components[:, first:first + _FEATURE_BLOCK_SIZE] = (
                left[:, :selected_k].T @ block
            ) / singular_values[:, None]
    _canonicalize_signs(scores, components)
    if not np.isfinite(scores).all() or not np.isfinite(components).all():
        raise ValueError("PCA transformation contains nonfinite values")
    return {
        "scores": scores,
        "components": components,
        "feature_means": feature_means,
        "singular_values": singular_values,
        "eigenvalues": eigenvalues,
        "explained_variance_ratio": explained_variance_ratio,
        "cumulative_variance_ratio": cumulative_variance_ratio,
        "numerical_rank": numerical_rank,
        "selected_k": selected_k,
        "achieved_variance": float(cumulative_variance_ratio[selected_k - 1]),
        "solver": solver,
        "rank_tolerance": float(rank_tolerance),
        "eigenvalue_roundoff_tolerance": float(eigenvalue_roundoff_tolerance),
        "selection_mode": selection_mode,
        "variance_threshold": None if variance_threshold is None else float(variance_threshold),
    }


def fit_pca(matrix, parameters: Mapping[str, Any]) -> dict[str, Any]:
    """Return one PCA fit under the backend-neutral representation contract."""
    started = time.perf_counter()
    prepared = prepare_pca(
        matrix,
        variance_threshold=parameters.get("variance_threshold", 0.99),
        retained_components=parameters.get("retained_components"),
    )
    selected_k = prepared["selected_k"]
    axes = [
        {
            "component": index + 1,
            "name": f"PC{index + 1}",
            "label": f"PC{index + 1} ({100.0 * prepared['explained_variance_ratio'][index]:.2f}%)",
            "kind": "pca",
            "explained_variance_ratio": float(prepared["explained_variance_ratio"][index]),
        }
        for index in range(min(2, selected_k))
    ]
    warnings = []
    if selected_k == 1:
        warnings.append("Only one component retained; a two-dimensional PCA display is unavailable.")
    arrays = {
        key: prepared[key]
        for key in (
            "components", "feature_means", "singular_values", "eigenvalues",
            "explained_variance_ratio", "cumulative_variance_ratio",
        )
    }
    diagnostics = {
        key: prepared[key]
        for key in (
            "numerical_rank", "selected_k", "achieved_variance", "solver",
            "rank_tolerance", "eigenvalue_roundoff_tolerance", "selection_mode",
        )
    }
    diagnostics.update({
        "retention": retention_diagnostics(
            prepared, prepared["scores"].shape[0], prepared["components"].shape[1]),
        "centering": "SNP/feature means across trait observations",
        "variance_denominator": int(prepared["scores"].shape[0] - 1),
        "whitened": False,
        "sign_convention": "largest_absolute_feature_coefficient_positive; ties_first_feature_position",
        "transform_equation": "scores = (X - feature_means) @ components.T",
        "reconstruction_equation": "X_hat = scores @ components + feature_means",
        "warnings": warnings,
    })
    return {
        "backend": "pca",
        "embedding": prepared["scores"],
        "visualization_embedding": prepared["scores"][:, :min(2, selected_k)].copy(),
        "axis_metadata": axes,
        "arrays": arrays,
        "diagnostics": diagnostics,
        "parameters": {
            "variance_threshold": prepared["variance_threshold"],
            "retained_components": parameters.get("retained_components"),
            "selection_mode": prepared["selection_mode"],
        },
        "runtime_seconds": time.perf_counter() - started,
    }
