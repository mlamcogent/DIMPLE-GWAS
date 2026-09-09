"""Create a labelled contact sheet for read-only source-document QA."""

from __future__ import annotations

import argparse
import glob
import math
from pathlib import Path

from PIL import Image, ImageDraw


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pattern")
    parser.add_argument("output")
    parser.add_argument("--columns", type=int, default=4)
    parser.add_argument("--width", type=int, default=260)
    args = parser.parse_args()

    paths = [Path(path) for path in sorted(glob.glob(args.pattern))]
    if not paths:
        raise SystemExit(f"No images match {args.pattern!r}")

    thumbnails: list[Image.Image] = []
    for path in paths:
        source = Image.open(path).convert("RGB")
        height = round(source.height * args.width / source.width)
        source.thumbnail((args.width, height))
        labelled = Image.new("RGB", (args.width, height + 24), "white")
        labelled.paste(source, ((args.width - source.width) // 2, 24))
        ImageDraw.Draw(labelled).text((4, 4), path.name, fill="black")
        thumbnails.append(labelled)

    rows = math.ceil(len(thumbnails) / args.columns)
    cell_height = max(image.height for image in thumbnails)
    sheet = Image.new(
        "RGB", (args.columns * args.width, rows * cell_height), (220, 220, 220)
    )
    for index, image in enumerate(thumbnails):
        sheet.paste(
            image,
            ((index % args.columns) * args.width, (index // args.columns) * cell_height),
        )
    sheet.save(args.output)


if __name__ == "__main__":
    main()
