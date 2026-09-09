"""Stable, dependency-light visual artifacts for original-space interpretation."""

from __future__ import annotations

import base64
import html
from io import BytesIO
from pathlib import Path
from typing import Sequence


def _label_key(value) -> tuple[int, float | str]:
    text = str(value).strip()
    if text in {"-1", "-1.0", "noise", "Noise", "NOISE"}:
        return (2, text)
    try:
        return (0, float(text))
    except ValueError:
        return (1, text)


def sample_block_preserving(labels: Sequence, maximum: int):
    """Return ordered indices, retaining every consecutive label block."""

    import numpy as np

    count = len(labels)
    if maximum < 1:
        raise ValueError("maximum must be >= 1")
    if count <= maximum:
        return np.arange(count, dtype=int)
    blocks: list[tuple[int, int]] = []
    start = 0
    for index in range(1, count + 1):
        if index == count or labels[index] != labels[start]:
            blocks.append((start, index))
            start = index
    if len(blocks) > maximum:
        raise ValueError(
            f"max_full_heatmap={maximum} cannot retain all {len(blocks)} label blocks"
        )
    allocation = [1] * len(blocks)
    remaining = maximum - len(blocks)
    capacities = [end - start - 1 for start, end in blocks]
    while remaining and any(value > 0 for value in capacities):
        best = max(range(len(blocks)), key=lambda i: (capacities[i], -i))
        allocation[best] += 1
        capacities[best] -= 1
        remaining -= 1
    chosen: list[int] = []
    for (start, end), size in zip(blocks, allocation):
        if size == 1:
            chosen.append(start + (end - start - 1) // 2)
        else:
            chosen.extend(
                np.linspace(start, end - 1, num=size, dtype=int).tolist()
            )
    return np.asarray(chosen, dtype=int)


def _correlation_rgb(values):
    import numpy as np

    clipped = np.clip(values, -1.0, 1.0)
    red = np.where(clipped >= 0, 255, 255 * (1 + clipped))
    blue = np.where(clipped <= 0, 255, 255 * (1 - clipped))
    green = 255 * (1 - np.abs(clipped))
    return np.stack([red, green, blue], axis=-1).astype("uint8")


def render_heatmap(
    correlation,
    labels: Sequence,
    vector_ids: Sequence[str],
    *,
    png_path: str | Path,
    html_path: str | Path,
    maximum: int,
) -> dict:
    """Write a sampled PNG and a self-contained HTML wrapper."""

    import numpy as np
    from PIL import Image, ImageDraw

    selected = sample_block_preserving(list(labels), int(maximum))
    values = np.asarray(correlation, dtype=float)[np.ix_(selected, selected)]
    selected_labels = [labels[index] for index in selected]
    selected_ids = [str(vector_ids[index]) for index in selected]

    matrix_image = Image.fromarray(_correlation_rgb(values), mode="RGB")
    scale = max(1, min(6, 1000 // max(1, len(selected))))
    matrix_image = matrix_image.resize(
        (len(selected) * scale, len(selected) * scale),
        resample=Image.Resampling.NEAREST,
    )
    track = Image.new("RGB", (max(12, 3 * scale), matrix_image.height), "white")
    draw = ImageDraw.Draw(track)
    palette = [
        (31, 119, 180), (255, 127, 14), (44, 160, 44), (214, 39, 40),
        (148, 103, 189), (140, 86, 75), (227, 119, 194), (127, 127, 127),
        (188, 189, 34), (23, 190, 207),
    ]
    unique = sorted(set(selected_labels), key=_label_key)
    colors = {
        label: ((70, 70, 70) if _label_key(label)[0] == 2 else palette[index % len(palette)])
        for index, label in enumerate(unique)
    }
    for row, label in enumerate(selected_labels):
        draw.rectangle(
            (0, row * scale, track.width, (row + 1) * scale - 1),
            fill=colors[label],
        )
    canvas = Image.new("RGB", (track.width + matrix_image.width, matrix_image.height), "white")
    canvas.paste(track, (0, 0))
    canvas.paste(matrix_image, (track.width, 0))
    png = Path(png_path)
    png.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(png, format="PNG", optimize=True)

    buffer = BytesIO()
    canvas.save(buffer, format="PNG", optimize=True)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    rows = "\n".join(
        f"<tr><td>{rank}</td><td>{html.escape(vector_id)}</td>"
        f"<td>{html.escape(str(label))}</td></tr>"
        for rank, (vector_id, label) in enumerate(zip(selected_ids, selected_labels), start=1)
    )
    document = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>DIMPLE-GWAS original-space similarity</title>
<style>body{{font-family:system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem}}
img{{max-width:100%;image-rendering:pixelated;border:1px solid #bbb}} table{{border-collapse:collapse}}
td,th{{border:1px solid #ddd;padding:.25rem .5rem}} code{{background:#eee;padding:.1rem .25rem}}</style></head>
<body><h1>Original-space vector similarity</h1>
<p>This is a post-run diagnostic. It does not change UMAP, HDBSCAN labels, or model ranking.
Blue denotes negative correlation, white zero, and red positive correlation. The left strip shows retained labels.</p>
<p>Rendered {len(selected)} of {len(labels)} vectors using block-preserving sampling. Complete ordering and
machine-readable similarity tables are separate artifacts.</p>
<img alt="Original-space correlation heatmap" src="data:image/png;base64,{encoded}">
<h2>Rendered vectors</h2><table><thead><tr><th>render rank</th><th>feature_id</th><th>label</th></tr></thead>
<tbody>{rows}</tbody></table></body></html>"""
    html_destination = Path(html_path)
    html_destination.write_text(document, encoding="utf-8")
    return {
        "rendered_vectors": int(len(selected)),
        "total_vectors": int(len(labels)),
        "sampling": "none" if len(selected) == len(labels) else "block_preserving",
        "selected_order_indices": selected.tolist(),
    }
