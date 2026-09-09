from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


if len(sys.argv) != 3:
    raise SystemExit("usage: postprocess_docx.py INPUT.docx OUTPUT.docx")
source, output = map(Path, sys.argv[1:])
doc = Document(source)
BLUE = RGBColor(0x23, 0x57, 0x89)
DARK_BLUE = RGBColor(0x1F, 0x4D, 0x78)
INK = RGBColor(0x20, 0x34, 0x47)
MUTED = RGBColor(0x5B, 0x65, 0x70)


def font(style, name, size, color, bold=None):
    style.font.name = name
    rpr = style._element.get_or_add_rPr()
    rpr.rFonts.set(qn("w:ascii"), name)
    rpr.rFonts.set(qn("w:hAnsi"), name)
    style.font.size = Pt(size)
    style.font.color.rgb = color
    if bold is not None:
        style.font.bold = bold


for section in doc.sections:
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.header_distance = Inches(0.492)
    section.footer_distance = Inches(0.492)
    section.different_first_page_header_footer = True
    header_p = section.header.paragraphs[0]
    header_p.text = "DIMPLE-GWAS Freeze 3 RC1  |  Documentation Edition 3"
    header_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for run in header_p.runs:
        run.font.name = "Calibri"
        run.font.size = Pt(8.5)
        run.font.color.rgb = MUTED
    footer_p = section.footer.paragraphs[0]
    footer_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = footer_p.add_run("Reader draft  |  ")
    run.font.name = "Calibri"
    run.font.size = Pt(8.5)
    run.font.color.rgb = MUTED
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    footer_p._p.append(fld)

styles = doc.styles
normal = styles["Normal"]
font(normal, "Calibri", 11, INK)
normal.paragraph_format.space_before = Pt(0)
normal.paragraph_format.space_after = Pt(8)
normal.paragraph_format.line_spacing = 1.333
normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
font(styles["Title"], "Calibri", 30, INK, True)
styles["Title"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
styles["Title"].paragraph_format.space_before = Pt(132)
styles["Title"].paragraph_format.space_after = Pt(8)
font(styles["Subtitle"], "Calibri", 15, DARK_BLUE)
styles["Subtitle"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
styles["Subtitle"].paragraph_format.space_after = Pt(12)
for name, size, color, before, after in (
    ("Heading 1", 16, BLUE, 18, 10),
    ("Heading 2", 13, BLUE, 12, 6),
    ("Heading 3", 12, DARK_BLUE, 8, 4),
    ("Heading 4", 11, DARK_BLUE, 7, 3),
):
    style = styles[name]
    font(style, "Calibri", size, color, True)
    style.paragraph_format.space_before = Pt(before)
    style.paragraph_format.space_after = Pt(after)
    style.paragraph_format.keep_with_next = True
for name in ("List Bullet", "List Number"):
    if name in styles:
        style = styles[name]
        font(style, "Calibri", 11, INK)
        style.paragraph_format.left_indent = Inches(0.375)
        style.paragraph_format.first_line_indent = Inches(-0.194)
        style.paragraph_format.space_after = Pt(4)
        style.paragraph_format.line_spacing = 1.208
if "Verbatim Char" in styles:
    font(styles["Verbatim Char"], "Consolas", 9, BLUE)
if "Caption" in styles:
    style = styles["Caption"]
    font(style, "Calibri", 9, MUTED)
    style.paragraph_format.space_before = Pt(4)
    style.paragraph_format.space_after = Pt(8)

def format_contents_entry(paragraph):
    level, title, page = paragraph.text.split("|", 2)
    paragraph.clear()
    paragraph.style = styles["Normal"]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    paragraph.paragraph_format.left_indent = Inches(0 if level == "TOC1" else 0.25)
    paragraph.paragraph_format.right_indent = Inches(0)
    paragraph.paragraph_format.first_line_indent = Inches(0)
    paragraph.paragraph_format.space_before = Pt(2 if level == "TOC1" else 0)
    paragraph.paragraph_format.space_after = Pt(4)
    paragraph.paragraph_format.line_spacing = 1.0
    paragraph.paragraph_format.keep_together = True
    ppr = paragraph._p.get_or_add_pPr()
    old_tabs = ppr.find(qn("w:tabs"))
    if old_tabs is not None:
        ppr.remove(old_tabs)
    tabs = OxmlElement("w:tabs")
    tab = OxmlElement("w:tab")
    tab.set(qn("w:val"), "right")
    tab.set(qn("w:leader"), "dot")
    tab.set(qn("w:pos"), "9000")
    tabs.append(tab)
    ppr.append(tabs)
    title_run = paragraph.add_run(title)
    title_run.font.name = "Calibri"
    title_run.font.size = Pt(10)
    title_run.font.color.rgb = DARK_BLUE if level == "TOC1" else INK
    title_run.bold = level == "TOC1"
    page_run = paragraph.add_run("\t" + page)
    page_run.font.name = "Calibri"
    page_run.font.size = Pt(10)
    page_run.font.color.rgb = BLUE
    page_run.bold = True


first_h1_seen = False
for paragraph in doc.paragraphs:
    if paragraph.text.startswith(("TOC1|", "TOC2|")):
        format_contents_entry(paragraph)
        continue
    if paragraph.style and paragraph.style.name == "Heading 1":
        paragraph.paragraph_format.page_break_before = True
        paragraph.paragraph_format.keep_with_next = True
        first_h1_seen = True
    if paragraph.style and paragraph.style.name in {"Source Code", "Compact"}:
        paragraph.paragraph_format.keep_together = True
        paragraph.paragraph_format.space_after = Pt(6)
        for run in paragraph.runs:
            run.font.name = "Consolas"
            run.font.size = Pt(8.5)


def set_cell_margins(cell):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = tcPr.first_child_found_in("w:tcMar")
    if tcMar is None:
        tcMar = OxmlElement("w:tcMar")
        tcPr.append(tcMar)
    for side, value in (("top", 80), ("bottom", 80), ("start", 120), ("end", 120)):
        node = tcMar.find(qn(f"w:{side}"))
        if node is None:
            node = OxmlElement(f"w:{side}")
            tcMar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def widths_for(cols):
    presets = {
        1: [9360],
        2: [2600, 6760],
        3: [1600, 3000, 4760],
        4: [1250, 2350, 2750, 3010],
        5: [1200, 1700, 2100, 2100, 2260],
    }
    return presets.get(cols, [9360 // cols] * (cols - 1) + [9360 - (9360 // cols) * (cols - 1)])


def set_table_borders(table):
    """Write borders explicitly so Word and LibreOffice render the same grid."""
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.first_child_found_in("w:tblBorders")
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        node = borders.find(qn(f"w:{edge}"))
        if node is None:
            node = OxmlElement(f"w:{edge}")
            borders.append(node)
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), "4")
        node.set(qn("w:space"), "0")
        node.set(qn("w:color"), "B8C6D3")


for table in doc.tables:
    cols = len(table.columns)
    widths = widths_for(cols)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.autofit = False
    tblPr = table._tbl.tblPr
    tblW = tblPr.first_child_found_in("w:tblW")
    if tblW is None:
        tblW = OxmlElement("w:tblW")
        tblPr.append(tblW)
    tblW.set(qn("w:w"), "9360")
    tblW.set(qn("w:type"), "dxa")
    tblInd = tblPr.first_child_found_in("w:tblInd")
    if tblInd is None:
        tblInd = OxmlElement("w:tblInd")
        tblPr.append(tblInd)
    tblInd.set(qn("w:w"), "0")
    tblInd.set(qn("w:type"), "dxa")
    layout = tblPr.first_child_found_in("w:tblLayout")
    if layout is None:
        layout = OxmlElement("w:tblLayout")
        tblPr.append(layout)
    layout.set(qn("w:type"), "fixed")
    set_table_borders(table)
    grid = table._tbl.tblGrid
    for old in list(grid):
        grid.remove(old)
    for width in widths:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(width))
        grid.append(col)
    for row_index, row in enumerate(table.rows):
        if row_index == 0:
            trPr = row._tr.get_or_add_trPr()
            repeat = OxmlElement("w:tblHeader")
            repeat.set(qn("w:val"), "true")
            trPr.append(repeat)
            cant_split = OxmlElement("w:cantSplit")
            trPr.append(cant_split)
        for col_index, cell in enumerate(row.cells):
            cell.width = Inches(widths[min(col_index, len(widths)-1)] / 1440)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
            set_cell_margins(cell)
            tcPr = cell._tc.get_or_add_tcPr()
            tcW = tcPr.first_child_found_in("w:tcW")
            if tcW is not None:
                tcW.set(qn("w:w"), str(widths[min(col_index, len(widths)-1)]))
                tcW.set(qn("w:type"), "dxa")
            if row_index == 0:
                shading = tcPr.first_child_found_in("w:shd")
                if shading is None:
                    shading = OxmlElement("w:shd")
                    tcPr.append(shading)
                shading.set(qn("w:val"), "clear")
                shading.set(qn("w:color"), "auto")
                shading.set(qn("w:fill"), "E8F0F7")
            for paragraph in cell.paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
                paragraph.paragraph_format.keep_with_next = False
                paragraph.paragraph_format.keep_together = False
                paragraph.paragraph_format.space_after = Pt(2)
                paragraph.paragraph_format.line_spacing = 1.05
                for run in paragraph.runs:
                    run.font.name = "Calibri"
                    run.font.size = Pt(8.5)
                    if row_index == 0:
                        run.bold = True
                        run.font.color.rgb = DARK_BLUE


def all_paragraphs():
    yield from doc.paragraphs
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                yield from cell.paragraphs


for paragraph in all_paragraphs():
    if paragraph.style and paragraph.style.name in {"Source Code", "Compact"}:
        for run in paragraph.runs:
            run.font.color.rgb = DARK_BLUE
    for run in paragraph.runs:
        if run.style and run.style.name == "Verbatim Char":
            run.font.name = "Consolas"
            run.font.size = Pt(9)
            run.font.color.rgb = BLUE


# LibreOffice exposes Pandoc section/citation bookmarks as stray "X" glyphs
# in PDF output. This edition uses a static contents section, so preserve the
# visible text while removing Word-only internal links and their bookmarks.
for hyperlink in list(doc._element.iter(qn("w:hyperlink"))):
    parent = hyperlink.getparent()
    position = parent.index(hyperlink)
    for child in list(hyperlink):
        hyperlink.remove(child)
        parent.insert(position, child)
        position += 1
    parent.remove(hyperlink)
for tag in ("w:bookmarkStart", "w:bookmarkEnd"):
    for marker in list(doc._element.iter(qn(tag))):
        marker.getparent().remove(marker)

doc.core_properties.title = "DIMPLE-GWAS Freeze 3 RC1 Documentation Edition 3"
doc.core_properties.subject = "Reader draft of the academic textbook, analyst workbook, and technical reference"
doc.core_properties.author = "DIMPLE-GWAS authors"
doc.core_properties.last_modified_by = ""
output.parent.mkdir(parents=True, exist_ok=True)
doc.save(output)
print(output)
