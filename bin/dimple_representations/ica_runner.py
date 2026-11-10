"""Standalone ICA on a selected, explicitly whitened PCA subspace.

For input ``X`` with traits as rows and SNPs as columns, let ``P`` be the
selected PCA axes, ``d`` their singular values and ``T`` the trait count.
FastICA receives a deterministic orthogonal rotation of the selected,
unwhitened PCA scores and performs one SVD whitening with
``whiten="unit-variance"``. The rotation avoids axis-aligned exact zeros in
sklearn's first-row SVD sign convention that can erase a PCA direction. Full
integrity checks reject any remaining loss in an arbitrary numerical basis. It
preserves the selected subspace and Euclidean geometry and is fully composed
back into every exported transformation. For geometry checks, reference
whitened PCA is ``Z = (X - means) @ P.T @ diag(sqrt(T) / d)``. This reference
matrix is never whitened again or supplied to the estimator.
The exported scores, original-SNP unmixing and mixing obey
``scores = (X - means) @ unmixing.T`` and
``reconstruction = scores @ mixing.T``. Reconstruction is the selected PCA
projection; it need not equal the full input after dimensional reduction.

ICA order is the fitted FastICA order, never an importance ranking. Signs
make each component's largest absolute original-SNP reconstruction coefficient
positive, breaking ties at the first feature position. All affected matrices
and scores receive the same sign changes.
"""

from __future__ import annotations

import math
import numbers
import time
import warnings
from typing import Any, Mapping

import numpy as np

from .pca_runner import prepare_pca, retention_diagnostics


class ICAFitError(RuntimeError):
    """An ICA fitting failure with the available numerical diagnostics."""

    def __init__(self, message: str, diagnostics: Mapping[str, Any]):
        super().__init__(message)
        self.diagnostics = dict(diagnostics)


class ICAConvergenceError(ICAFitError):
    """A single ICA fit failed to converge; diagnostics remain inspectable."""


def _fitted_rotation_diagnostics(estimator: Any,
                                 whitening_scale: np.ndarray | None = None,
                                 reflector: np.ndarray | None = None) -> dict[str, Any]:
    """Inspect partial fitted state without another fit or matrix inverse.

    sklearn sets ``n_iter_`` and ``components_`` before constructing ``mixing_``.
    A failure during that construction must not erase the iteration evidence.
    With unit-variance whitening, compose the public operator with the inverse
    reference PCA whitening scale before inspecting orthogonality. Row norms
    cover every fitted component; off-diagonal orthogonality uses a
    deterministic sample of at most 64 rows against all fitted component rows.
    """
    components = getattr(estimator, "components_", None)
    result: dict[str, Any] = {
        "components_available": components is not None,
        "mixing_available": hasattr(estimator, "mixing_"),
    }
    if components is None:
        return result
    components = np.asarray(components)
    finite = np.isfinite(components)
    result.update({
        "components_shape": list(components.shape),
        "components_finite": bool(finite.all()),
        "components_nonfinite_count": int(components.size - np.count_nonzero(finite)),
    })
    if components.ndim != 2 or not finite.all():
        return result
    if reflector is not None:
        components = _reflect_right(components, reflector)
    if estimator.whiten is not False:
        if whitening_scale is None:
            result["orthogonality_available"] = False
            result["operator_basis"] = "selected unwhitened PCA scores"
            return result
        components = components / whitening_scale
    result["orthogonality_available"] = True
    result["operator_basis"] = "reference unit-variance whitened PCA scores"
    row_norms_squared = np.einsum("ij,ij->i", components, components)
    sampled_rows = np.linspace(0, components.shape[0] - 1,
                               min(components.shape[0], 64), dtype=int)
    sampled_gram = components[sampled_rows] @ components.T
    sampled_gram[np.arange(len(sampled_rows)), sampled_rows] -= 1.0
    result.update({
        "row_norm_squared_min": float(row_norms_squared.min()),
        "row_norm_squared_max": float(row_norms_squared.max()),
        "row_norm_squared_max_abs_error": float(np.max(np.abs(row_norms_squared - 1.0))),
        "orthogonality_sampled_rows": len(sampled_rows),
        "orthogonality_compared_rows": components.shape[0],
        "orthogonality_sample_max_abs_error": float(np.max(np.abs(sampled_gram))),
    })
    return result


def _householder_reflector(components: int) -> np.ndarray:
    """A compact orthogonal change of basis whose first row is dense.

    H = I - 2 v v.T maps the first basis vector to normalized [1, 2, ..., k].
    The dense, nonuniform direction avoids symmetric cancellation patterns in
    repeated-spectrum bases. H is symmetric and H^-1 = H; one dimension uses
    identity (v=0). Integrity checks still guard arbitrary eigensolver bases.
    """
    if components == 1:
        return np.zeros(1, dtype=np.float64)
    direction = np.arange(1, components + 1, dtype=np.float64)
    direction /= np.linalg.norm(direction)
    vector = -direction
    vector[0] += 1.0
    vector /= np.linalg.norm(vector)
    return vector


def _reflect_right(matrix: np.ndarray, reflector: np.ndarray) -> np.ndarray:
    """Compute matrix @ H without forming a dense H or changing dimensions."""
    return matrix - 2.0 * np.outer(matrix @ reflector, reflector)


def _fit_integrity(pca_scores: np.ndarray, scores: np.ndarray,
                   components: np.ndarray, mixing: np.ndarray,
                   score_means: np.ndarray, whitening_scale: np.ndarray) -> dict[str, Any]:
    """Check every retained direction before exporting or clustering it."""
    count = pca_scores.shape[1]
    rotation = components / whitening_scale
    gram = rotation @ rotation.T
    gram.flat[::count + 1] -= 1.0
    orthogonality_error = float(np.max(np.abs(gram)))
    del gram
    inverse = components @ mixing
    inverse.flat[::count + 1] -= 1.0
    inverse_error = float(np.max(np.abs(inverse)))
    del inverse
    reconstructed = scores @ mixing.T + score_means
    reconstruction_error = float(np.max(np.abs(reconstructed - pca_scores)))
    reconstruction_relative_error = reconstruction_error / max(1.0, float(np.max(np.abs(pca_scores))))
    del reconstructed
    predicted = (pca_scores - score_means) @ components.T
    transform_error = float(np.max(np.abs(predicted - scores)))
    transform_relative_error = transform_error / max(1.0, float(np.max(np.abs(scores))))
    tolerance = 1e-7
    errors = (orthogonality_error, inverse_error, reconstruction_relative_error,
              transform_relative_error)
    return {
        "retained_directions_checked": count,
        "orthogonality_max_abs_error": orthogonality_error,
        "inverse_identity_max_abs_error": inverse_error,
        "selected_space_reconstruction_max_abs_error": reconstruction_error,
        "selected_space_reconstruction_relative_error": reconstruction_relative_error,
        "selected_space_transform_max_abs_error": transform_error,
        "selected_space_transform_relative_error": transform_relative_error,
        "tolerance": tolerance,
        "passed": all(math.isfinite(error) and error <= tolerance for error in errors),
    }


def _positive_integer(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, numbers.Integral) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return int(value)


def _component_indices(value: Any, name: str, selected_k: int,
                       minimum: int, maximum: int) -> list[int]:
    if isinstance(value, str):
        try:
            value = [int(token.strip()) for token in value.split(",")]
        except ValueError as exc:
            raise ValueError(f"{name} must contain one-based component integers") from exc
    try:
        indices = list(value)
    except TypeError as exc:
        raise ValueError(f"{name} must be a list of one-based component integers") from exc
    if not minimum <= len(indices) <= maximum:
        raise ValueError(f"{name} must contain {minimum}–{maximum} components")
    indices = [_positive_integer(index, name) for index in indices]
    if len(indices) != len(set(indices)):
        raise ValueError(f"{name} components must be distinct")
    if max(indices) > selected_k:
        raise ValueError(f"{name} requests a component beyond the {selected_k} retained ICs")
    return indices


def _sample_distances(scores: np.ndarray, indices: np.ndarray) -> np.ndarray:
    # Differences avoid cancellation for close points. The sample is bounded
    # at 64 observations, independent of the full trait count.
    sampled = scores[indices]
    rows, columns = np.triu_indices(len(indices), 1)
    distances = np.empty(len(rows), dtype=np.float64)
    for position, (row, column) in enumerate(zip(rows, columns)):
        delta = sampled[row] - sampled[column]
        distances[position] = np.linalg.norm(delta)
    return distances


def _reconstruction_signs(mixing: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Find sign pivots without allocating another full SNP coefficient matrix."""
    components = mixing.shape[1]
    maximum_values = np.full(components, -1.0)
    sign_features = np.zeros(components, dtype=int)
    component_positions = np.arange(components)
    for first in range(0, mixing.shape[0], 4096):
        block = np.abs(mixing[first:first + 4096])
        positions = np.argmax(block, axis=0)
        values = block[positions, component_positions]
        # Strict comparison preserves the first original feature on ties.
        larger = values > maximum_values
        sign_features[larger] = first + positions[larger]
        maximum_values[larger] = values[larger]
    signs = np.where(mixing[sign_features, component_positions] < 0, -1.0, 1.0)
    return sign_features, signs


def _geometry_diagnostics(whitened: np.ndarray, scores: np.ndarray,
                          numerical_rank: int) -> dict[str, Any]:
    traits, retained = scores.shape
    indices = np.linspace(0, traits - 1, min(traits, 64), dtype=int)
    pca_distances = _sample_distances(whitened, indices)
    ica_distances = _sample_distances(scores, indices)
    scale = max(float(pca_distances.max()), np.finfo(np.float64).tiny)
    error = float(np.max(np.abs(pca_distances - ica_distances)) / scale)
    tolerance = 1e-7
    full_row_rank = numerical_rank == traits - 1 and retained == traits - 1
    simplex: dict[str, Any] = {
        "full_row_rank_retained": full_row_rank,
        "sampled_observations": len(indices),
        "sampled_pairs": len(ica_distances),
        "relative_tolerance": tolerance,
    }
    if full_row_rank:
        expected = math.sqrt(2.0 * traits)
        deviation = float(np.max(np.abs(ica_distances - expected)) / expected)
        simplex.update({
            "expected_pairwise_distance": expected,
            "observed_distance_min": float(ica_distances.min()),
            "observed_distance_max": float(ica_distances.max()),
            "max_relative_deviation": deviation,
            "equidistant_within_tolerance": deviation <= tolerance,
        })
    return {
        "euclidean_whitened_pca_equivalence": {
            "sampled_observations": len(indices),
            "sampled_pairs": len(ica_distances),
            "max_absolute_distance_error": float(np.max(np.abs(pca_distances - ica_distances))),
            "max_relative_distance_error": error,
            "relative_tolerance": tolerance,
            "equivalent_within_tolerance": error <= tolerance,
            "scope": "all retained dimensions; Euclidean distance only",
        },
        "simplex": simplex,
    }


def fit_ica(matrix: Any, parameters: Mapping[str, Any]) -> dict[str, Any]:
    """Fit one ICA representation, preserving the full retained score space.

    ``plot_components=None`` denotes the adaptive default. An explicitly
    supplied nonexistent axis is an error even when one IC was retained.
    Component selections are one-based; pair plots are optional and bounded.
    Nonconvergence raises :class:`ICAConvergenceError` before any representation
    can be handed to clustering. Other estimator failures raise
    :class:`ICAFitError` with available iteration and numerical diagnostics.
    There is no restart or alternative backend.
    """
    from sklearn import __version__ as sklearn_version
    from sklearn.decomposition import FastICA
    from sklearn.exceptions import ConvergenceWarning

    started = time.perf_counter()
    resolved = dict(parameters)
    seed = resolved.get("seed", 42)
    if (isinstance(seed, bool) or not isinstance(seed, numbers.Integral)
            or not 0 <= seed <= 2**32 - 1):
        raise ValueError("ICA seed must be an integer in [0, 2**32 - 1]")
    seed = int(seed)
    tol = resolved.get("tol", 1e-4)
    if isinstance(tol, (bool, np.bool_)):
        raise ValueError("ICA tol must be finite and positive")
    try:
        tol = float(tol)
    except (TypeError, ValueError) as exc:
        raise ValueError("ICA tol must be finite and positive") from exc
    if not math.isfinite(tol) or tol <= 0:
        raise ValueError("ICA tol must be finite and positive")
    max_iter = _positive_integer(resolved.get("max_iter", 1000), "ICA max_iter")
    threshold = resolved.get("variance_threshold", 0.99)
    retained_components = resolved.get("retained_components")
    pca = prepare_pca(matrix, variance_threshold=threshold,
                      retained_components=retained_components)
    pca_scores = pca["scores"]
    traits, selected_k = pca_scores.shape

    requested_plot = resolved.get("plot_components")
    plot_components = ([1] if selected_k == 1 else [1, 2]) if requested_plot is None else (
        _component_indices(requested_plot, "ICA plot_components", selected_k,
                           1 if selected_k == 1 else 2, 1 if selected_k == 1 else 2)
    )
    requested_pairplot = resolved.get("pairplot_components")
    pairplot_components = None if requested_pairplot is None else _component_indices(
        requested_pairplot, "ICA pairplot_components", selected_k, 2, 4)
    resolved.update({
        "variance_threshold": threshold,
        "retained_components": retained_components,
        "selection_mode": pca["selection_mode"],
        "seed": seed,
        "tol": tol,
        "max_iter": max_iter,
        "plot_components": plot_components,
        "pairplot_components": pairplot_components,
    })

    whitening_scale = math.sqrt(traits) / pca["singular_values"]
    whitened = pca_scores * whitening_scale
    reflector = _householder_reflector(selected_k)
    estimator_input = _reflect_right(pca_scores, reflector)
    if not np.isfinite(whitening_scale).all() or not np.isfinite(whitened).all():
        raise ValueError("ICA whitening overflowed float64 precision")
    diagnostics: dict[str, Any] = {
        "algorithm": "parallel",
        "fun": "logcosh",
        "logcosh_alpha": 1.0,
        "sklearn_version": sklearn_version,
        "sklearn_whiten": "unit-variance",
        "ica_whitening_solver": "svd",
        "whitening_stage": "single FastICA whitening of orthogonally rotated selected unwhitened PCA scores",
        "ica_input_basis": "deterministic Householder rotation; dimensions and unwhitened geometry preserved",
        "ica_input_basis_equation": "H = I - 2 v v.T; FastICA input = PCA scores @ H; H^-1 = H",
        "ica_input_basis_direction": "normalized [1, 2, ..., k]; dense and nonuniform",
        "whitening_convention": "unit empirical variance; denominator T (ddof=0)",
        "whitened": True,
        "variance_denominator": traits,
        "centering": "SNP/feature means across trait observations",
        "pca_solver": pca["solver"],
        "solver": pca["solver"],
        "rank_tolerance": float(pca["rank_tolerance"]),
        "eigenvalue_roundoff_tolerance": float(pca["eigenvalue_roundoff_tolerance"]),
        "numerical_rank": int(pca["numerical_rank"]),
        "selected_k": int(selected_k),
        "achieved_variance": float(pca["achieved_variance"]),
        "retention": retention_diagnostics(pca, traits, pca["components"].shape[1]),
        "trait_count": traits,
        "feature_count": pca["components"].shape[1],
        "seed": seed,
        "tol": tol,
        "max_iter": max_iter,
        "fits_attempted": 1,
        "component_order": "fitted FastICA order; no importance ranking",
        "sign_convention": "largest absolute original-SNP reconstruction coefficient positive; first feature breaks ties",
        "transform_equation": "scores = (X - feature_means) @ unmixing.T",
        "reconstruction_equation": "X_hat = scores @ mixing.T + feature_means",
        "parameters": resolved,
        "warnings": [],
    }
    estimator = FastICA(algorithm="parallel", whiten="unit-variance", whiten_solver="svd", fun="logcosh",
                        fun_args={"alpha": 1.0}, random_state=seed,
                        tol=tol, max_iter=max_iter)
    recorded: list[Any] = []
    try:
        with warnings.catch_warnings(record=True) as recorded:
            warnings.simplefilter("always", ConvergenceWarning)
            raw_scores = estimator.fit_transform(estimator_input)
    except Exception as exc:
        iterations = getattr(estimator, "n_iter_", None)
        convergence_warning = any(issubclass(item.category, ConvergenceWarning)
                                  for item in recorded)
        diagnostics.update({
            "status": "numerical_failure",
            "failure_stage": "FastICA.fit_transform",
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
            "warnings": [str(item.message) for item in recorded],
            "n_iter": None if iterations is None else int(iterations),
            "converged": None if iterations is None else not convergence_warning,
            "fit_completed": False,
            "runtime_seconds": time.perf_counter() - started,
            "fitted_rotation": _fitted_rotation_diagnostics(estimator, whitening_scale, reflector),
        })
        raise ICAFitError(
            f"ICA fitting failed ({type(exc).__name__}: {exc}); clustering skipped",
            diagnostics,
        ) from exc
    diagnostics["warnings"] = [str(item.message) for item in recorded]
    diagnostics["n_iter"] = int(estimator.n_iter_)
    diagnostics["converged"] = not any(
        issubclass(item.category, ConvergenceWarning) for item in recorded)
    diagnostics["runtime_seconds"] = time.perf_counter() - started
    diagnostics["fit_completed"] = True
    if not diagnostics["converged"]:
        diagnostics["status"] = "nonconverged"
        raise ICAConvergenceError(
            f"ICA did not converge after {estimator.n_iter_} iterations "
            f"(max_iter={max_iter}, tol={tol}); clustering skipped", diagnostics)
    if not np.isfinite(raw_scores).all():
        raise ValueError("ICA produced nonfinite component scores")
    expected_shapes = {'scores': (traits, selected_k), 'components': (selected_k, selected_k),
                       'mixing': (selected_k, selected_k), 'score_means': (selected_k,)}
    observed_shapes = {'scores': np.shape(raw_scores),
                       'components': np.shape(getattr(estimator, 'components_', None)),
                       'mixing': np.shape(getattr(estimator, 'mixing_', None)),
                       'score_means': np.shape(getattr(estimator, 'mean_', None))}
    if observed_shapes != expected_shapes:
        diagnostics.update({'status': 'numerical_integrity_failure', 'failure_stage': 'retained-dimension shape checks',
                            'expected_shapes': expected_shapes, 'observed_shapes': observed_shapes,
                            'runtime_seconds': time.perf_counter() - started})
        raise ICAFitError('ICA returned inconsistent retained dimensions; clustering skipped', diagnostics)

    # The public FastICA API already enforces the requested unit variance.
    # Preserve its complete fitted operator, including its selected-score
    # centering, rather than requesting an inverse of a bare orthogonal W.
    unit_scale = np.std(raw_scores, axis=0, ddof=0)
    if np.any(unit_scale <= 0) or not np.isfinite(unit_scale).all():
        raise ValueError("ICA produced a component with zero or nonfinite variance")
    selected_components = _reflect_right(estimator.components_, reflector)
    selected_mixing = estimator.mixing_ - 2.0 * np.outer(reflector, reflector @ estimator.mixing_)
    selected_score_means = _reflect_right(estimator.mean_[None, :], reflector)[0]
    integrity = _fit_integrity(pca_scores, raw_scores, selected_components,
                               selected_mixing, selected_score_means, whitening_scale)
    diagnostics["numerical_integrity"] = integrity
    if not integrity["passed"]:
        diagnostics.update({"status": "numerical_integrity_failure",
                            "failure_stage": "complete retained-subspace integrity checks",
                            "runtime_seconds": time.perf_counter() - started})
        raise ICAFitError("ICA failed retained-subspace numerical integrity checks; clustering skipped",
                          diagnostics)
    rotation = selected_components / whitening_scale
    unmixing = selected_components @ pca["components"]
    mixing = np.empty((pca["components"].shape[1], selected_k), dtype=np.float64)
    feature_means = pca["feature_means"] + selected_score_means @ pca["components"]
    # Generate complete original-feature coefficients in bounded blocks; do
    # not allocate a second, full weighted copy of the PCA component matrix.
    for first in range(0, mixing.shape[0], 4096):
        mixing[first:first + 4096] = (
            pca["components"][:, first:first + 4096].T @ selected_mixing
        )
    scores = raw_scores
    sign_features, signs = _reconstruction_signs(mixing)
    scores *= signs
    unmixing *= signs[:, None]
    mixing *= signs
    rotation *= signs[:, None]

    geometry = _geometry_diagnostics(whitened, scores, pca["numerical_rank"])
    diagnostics.update(geometry)
    diagnostics.update({
        "status": "converged",
        "selection_mode": pca["selection_mode"],
        "empirical_unit_variance_scale_max_abs_deviation": float(np.max(np.abs(unit_scale - 1.0))),
        "post_fit_unit_variance_rescaling": False,
        "selected_score_centering_max_abs": float(np.max(np.abs(selected_score_means))),
        "feature_means_composition": "PCA feature means + FastICA selected-score means @ PCA components",
        "empirical_component_variance_min": float(np.var(scores, axis=0, ddof=0).min()),
        "empirical_component_variance_max": float(np.var(scores, axis=0, ddof=0).max()),
        "sign_feature_positions": sign_features.tolist(),
        "component_signs": signs.astype(int).tolist(),
        "display_components": plot_components,
        "display_default_adapted_to_one_dimension": requested_plot is None and selected_k == 1,
        "pairplot_components": pairplot_components,
        "high_dimensionality": selected_k >= max(1, traits // 2),
    })
    if selected_k == 1:
        diagnostics["warnings"].append("Only one IC is retained; a two-dimensional IC display is unavailable.")
    if geometry["simplex"]["full_row_rank_retained"]:
        diagnostics["warnings"].append(
            "All T-1 nonzero dimensions are whitened; training traits form an "
            "equidistant simplex, so Euclidean density clustering has no distance separation.")
    if not geometry["euclidean_whitened_pca_equivalence"]["equivalent_within_tolerance"]:
        diagnostics["warnings"].append(
            "Sampled ICA/whitened-PCA distances exceed the numerical equivalence tolerance.")

    axis_metadata = [{
        "component": component,
        "name": f"IC{component}",
        "label": f"IC{component}",
        "kind": "ica",
        "importance_ordered": False,
    } for component in plot_components]
    elapsed = time.perf_counter() - started
    diagnostics["runtime_seconds"] = elapsed
    return {
        "backend": "ica",
        "embedding": scores,
        "visualization_embedding": scores[:, [index - 1 for index in plot_components]].copy(),
        "axis_metadata": axis_metadata,
        "arrays": {
            "unmixing": unmixing,
            "mixing": mixing,
            "feature_means": feature_means,
            "pca_feature_means": pca["feature_means"],
            "pca_score_means": selected_score_means,
            "ica_input_reflector": reflector,
            "pca_components": pca["components"],
            "pca_singular_values": pca["singular_values"],
            "pca_eigenvalues": pca["eigenvalues"],
            "pca_explained_variance_ratio": pca["explained_variance_ratio"],
            "pca_cumulative_variance_ratio": pca["cumulative_variance_ratio"],
            "whitening_scale": whitening_scale,
            "ica_rotation": rotation,
            "ica_internal_whitening": _reflect_right(estimator.whitening_, reflector),
            "unit_variance_scale": unit_scale,
        },
        "diagnostics": diagnostics,
        "parameters": resolved,
        "runtime_seconds": elapsed,
    }
