#!/usr/bin/env python3
"""Create numbered contact sheets so every rendered PDF page can be inspected."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageStat


MANUAL = Path(__file__).resolve().parents[2]
PAGES = MANUAL / "build" / "qa" / "pdf_pages_v4"
CONTACTS = MANUAL / "build" / "qa" / "pdf_contacts_v4"


def main() -> None:
    CONTACTS.mkdir(parents=True, exist_ok=True)
    pages = sorted(PAGES.glob("page-*.png"), key=lambda p: int(p.stem.split("-")[-1]))
    font = ImageFont.load_default(size=18)
    diagnostics = []
    for sheet_index, offset in enumerate(range(0, len(pages), 12), start=1):
        batch = pages[offset:offset + 12]
        canvas = Image.new("RGB", (1240, 1740), "#d7dde2")
        draw = ImageDraw.Draw(canvas)
        for position, path in enumerate(batch):
            page_number = int(path.stem.split("-")[-1])
            with Image.open(path) as source:
                image = source.convert("RGB")
                image.thumbnail((290, 400), Image.Resampling.LANCZOS)
                x = 15 + (position % 4) * 305
                y = 40 + (position // 4) * 560
                canvas.paste(image, (x, y))
                draw.text((x, y - 25), f"Page {page_number}", fill="#13293d", font=font)
                grey = image.convert("L")
                stat = ImageStat.Stat(grey)
                diagnostics.append({
                    "page": page_number,
                    "render": str(path.relative_to(MANUAL)),
                    "mean_luminance": stat.mean[0],
                    "std_luminance": stat.stddev[0],
                    "size": [source.width, source.height],
                })
        canvas.save(CONTACTS / f"contact_{sheet_index:02d}_pages_{offset + 1:03d}_{offset + len(batch):03d}.png")
    (MANUAL / "build" / "qa" / "pdf_page_diagnostics.json").write_text(json.dumps(diagnostics, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
