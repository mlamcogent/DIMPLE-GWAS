from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION_START
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "build" / "edition3_reference.docx"
BLUE = RGBColor(0x23, 0x57, 0x89)
DARK_BLUE = RGBColor(0x1F, 0x4D, 0x78)
INK = RGBColor(0x20, 0x34, 0x47)
MUTED = RGBColor(0x5B, 0x65, 0x70)


def set_font(style, name: str, size: float, color: RGBColor | None = None, bold: bool | None = None):
    style.font.name = name
    style._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    style._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    style.font.size = Pt(size)
    if color is not None:
        style.font.color.rgb = color
    if bold is not None:
        style.font.bold = bold


doc = Document()
section = doc.sections[0]
section.start_type = WD_SECTION_START.NEW_PAGE
section.page_width = Inches(8.5)
section.page_height = Inches(11)
section.top_margin = Inches(1)
section.bottom_margin = Inches(1)
section.left_margin = Inches(1)
section.right_margin = Inches(1)
section.header_distance = Inches(0.492)
section.footer_distance = Inches(0.492)

styles = doc.styles
normal = styles["Normal"]
set_font(normal, "Calibri", 11, INK)
normal.paragraph_format.space_before = Pt(0)
normal.paragraph_format.space_after = Pt(8)
normal.paragraph_format.line_spacing = 1.333
normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

title = styles["Title"]
set_font(title, "Calibri", 30, INK, True)
title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.paragraph_format.space_before = Pt(132)
title.paragraph_format.space_after = Pt(8)

subtitle = styles["Subtitle"]
set_font(subtitle, "Calibri", 15, DARK_BLUE, False)
subtitle.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
subtitle.paragraph_format.space_after = Pt(12)

for name, size, color, before, after in (
    ("Heading 1", 16, BLUE, 18, 10),
    ("Heading 2", 13, BLUE, 12, 6),
    ("Heading 3", 12, DARK_BLUE, 8, 4),
    ("Heading 4", 11, DARK_BLUE, 7, 3),
):
    style = styles[name]
    set_font(style, "Calibri", size, color, True)
    style.paragraph_format.space_before = Pt(before)
    style.paragraph_format.space_after = Pt(after)
    style.paragraph_format.keep_with_next = True

for name in ("List Bullet", "List Number"):
    style = styles[name]
    set_font(style, "Calibri", 11, INK)
    style.paragraph_format.left_indent = Inches(0.375)
    style.paragraph_format.first_line_indent = Inches(-0.194)
    style.paragraph_format.space_after = Pt(4)
    style.paragraph_format.line_spacing = 1.208

caption = styles["Caption"]
set_font(caption, "Calibri", 9, MUTED)
caption.paragraph_format.space_before = Pt(4)
caption.paragraph_format.space_after = Pt(8)
caption.paragraph_format.keep_with_next = True

for name in ("Source Code", "Verbatim Char"):
    if name not in styles:
        styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH if name == "Source Code" else WD_STYLE_TYPE.CHARACTER)
    set_font(styles[name], "Consolas", 8.5, INK)

doc.core_properties.title = "DIMPLE-GWAS Freeze 3 RC1 Documentation Edition 3"
doc.core_properties.subject = "Academic textbook, analyst workbook, and technical reference"
doc.core_properties.author = "DIMPLE-GWAS authors"
doc.core_properties.keywords = "DIMPLE-GWAS, UMAP, densMAP, HDBSCAN, GWAS, documentation"
OUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUT)
print(OUT)
