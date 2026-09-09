#!/usr/bin/env python3
"""Build contact sheets and automated page geometry measurements."""

from __future__ import annotations

import csv
import math
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageStat


EDITION2 = Path(__file__).resolve().parents[2]
PAGES = EDITION2 / "build/pdf_render_final/pages"
SHEETS = EDITION2 / "build/pdf_render_final/contact_sheets"
QA = EDITION2 / "qa"


def page_number(path: Path) -> int:
    return int(path.stem.rsplit("-", 1)[-1])


def main() -> None:
    pages = sorted(PAGES.glob("page-*.png"), key=page_number)
    if not pages:
        raise SystemExit("No rendered pages found")
    SHEETS.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    rows = []
    thumb_w, thumb_h = 204, 264
    label_h, gutter = 28, 18
    columns, per_sheet = 4, 20
    for path in pages:
        with Image.open(path) as image:
            rgb = image.convert("RGB")
            gray = rgb.convert("L")
            ink = ImageChops.invert(gray).point(lambda x: 255 if x > 12 else 0)
            bbox = ink.getbbox()
            width, height = rgb.size
            nonwhite = sum(1 for value in gray.getdata() if value < 245) / (width * height)
            if bbox:
                left, top, right, bottom = bbox
                margin_left, margin_top = left, top
                margin_right, margin_bottom = width - right, height - bottom
            else:
                margin_left = margin_top = margin_right = margin_bottom = -1
            flags = []
            if nonwhite < 0.001:
                flags.append("blank_or_near_blank")
            if bbox and min(margin_left, margin_right, margin_top, margin_bottom) <= 1:
                flags.append("ink_touches_page_edge")
            rows.append({
                "page": page_number(path), "file": str(path.relative_to(EDITION2)), "rendered": "yes",
                "width_px": width, "height_px": height, "nonwhite_fraction": f"{nonwhite:.6f}",
                "ink_bbox": "" if not bbox else ",".join(map(str, bbox)),
                "margin_left_px": margin_left, "margin_right_px": margin_right,
                "margin_top_px": margin_top, "margin_bottom_px": margin_bottom,
                "automated_flags": ";".join(flags) or "none", "visual_status": "pending",
            })

    fields = list(rows[0])
    with (QA / "page_render_qa.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader(); writer.writerows(rows)

    inventory = []
    for sheet_index in range(math.ceil(len(pages) / per_sheet)):
        group = pages[sheet_index * per_sheet:(sheet_index + 1) * per_sheet]
        rows_n = math.ceil(len(group) / columns)
        canvas = Image.new("RGB", (columns * (thumb_w + gutter) + gutter, rows_n * (thumb_h + label_h + gutter) + gutter), "#d7dee5")
        draw = ImageDraw.Draw(canvas)
        for position, path in enumerate(group):
            col, row = position % columns, position // columns
            x = gutter + col * (thumb_w + gutter)
            y = gutter + row * (thumb_h + label_h + gutter)
            with Image.open(path) as source:
                image = source.convert("RGB")
                image.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                pane = Image.new("RGB", (thumb_w, thumb_h), "white")
                pane.paste(image, ((thumb_w - image.width)//2, (thumb_h - image.height)//2))
                canvas.paste(pane, (x, y))
            draw.rectangle((x, y, x + thumb_w, y + thumb_h), outline="#667788", width=1)
            draw.text((x, y + thumb_h + 5), f"Page {page_number(path)}", fill="#17324d")
        out = SHEETS / f"contact_{sheet_index+1:02d}_pages_{page_number(group[0]):03d}-{page_number(group[-1]):03d}.jpg"
        canvas.save(out, quality=90, optimize=True)
        inventory.append({"sheet": sheet_index + 1, "first_page": page_number(group[0]), "last_page": page_number(group[-1]), "file": str(out.relative_to(EDITION2)), "visual_status": "pending"})
    with (QA / "contact_sheet_inventory.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(inventory[0]), delimiter="\t")
        writer.writeheader(); writer.writerows(inventory)
    print(f"Measured {len(pages)} pages and created {len(inventory)} contact sheets")


if __name__ == "__main__":
    main()
