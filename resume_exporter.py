"""
Renders a structured resume dict (from resume_polisher.py) into a
professionally formatted .docx, then optionally converts to .pdf.
Matches the clean two-column style of Jeremy's original resume.
"""
import io

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from resume_context import CANDIDATE_NAME, CANDIDATE_EMAIL, CANDIDATE_PHONE

# ── Helpers ────────────────────────────────────────────────────────────────

def _para(doc, space_before=0, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    return p


def _run(para, text, bold=False, size=10.5, font="Calibri", color=None, italic=False):
    r = para.add_run(text)
    r.font.name = font
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    if color:
        r.font.color.rgb = RGBColor(*color)
    return r


def _section_header(doc, title):
    """Bold section title with a bottom border line."""
    p = _para(doc, space_before=8, space_after=2)
    _run(p, title, bold=True, size=11)
    # Add bottom border to the paragraph
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "000000")
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p


def _two_col_row(doc, left, right, left_bold=False, right_bold=False,
                 left_italic=False, right_italic=False, size=10.5):
    """Single paragraph: left text + right-aligned text via tab stop."""
    p = _para(doc, space_before=0, space_after=1)
    # Set right tab stop at the right margin
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    pPr = p._p.get_or_add_pPr()
    tabs = OxmlElement("w:tabs")
    tab = OxmlElement("w:tab")
    tab.set(qn("w:val"), "right")
    tab.set(qn("w:pos"), "9360")  # 6.5 inches content width in twips
    tabs.append(tab)
    pPr.append(tabs)

    _run(p, left, bold=left_bold, italic=left_italic, size=size)
    _run(p, "\t", size=size)
    _run(p, right, bold=right_bold, italic=right_italic, size=size)
    return p


def _bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.first_line_indent = Inches(-0.15)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10.5)
    return p


# ── Main export ────────────────────────────────────────────────────────────

def resume_to_docx(data: dict) -> bytes:
    doc = Document()

    # Page: US Letter, 0.75" margins (standard for resumes)
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)

    # Default style
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10.5)

    # ── Header ──────────────────────────────────────────────────────────────
    name_p = _para(doc, space_before=0, space_after=2)
    name_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _run(name_p, CANDIDATE_NAME, bold=True, size=16)

    contact_p = _para(doc, space_before=0, space_after=6)
    contact_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _run(contact_p, f"{CANDIDATE_PHONE}  |  {CANDIDATE_EMAIL}  |  U.S. Citizen", size=10)

    # ── Education (static — never modified) ─────────────────────────────────
    _section_header(doc, "EDUCATION")
    _two_col_row(doc, "University of California, San Diego", "La Jolla, CA",
                 left_bold=True, right_bold=False)
    _two_col_row(doc, "Bachelor of Science in Data Science, Business Minor",
                 "Sept 2018 – Sept 2024", left_italic=True, right_italic=True, size=10.5)
    courses_p = _para(doc, space_before=0, space_after=4)
    _run(courses_p,
         "Relevant Coursework: Data Analytics, Business Analytics, Strategic Planning, "
         "Financial Analytics, Risk Assessment, Data Structures & Algorithms, Probability & "
         "Statistics, Machine Learning & Deep Learning, Data Science, Market Management",
         italic=True, size=10)

    # ── Skills ───────────────────────────────────────────────────────────────
    _section_header(doc, "SKILLS")
    skills = data.get("skills", {})
    for category, items in skills.items():
        p = _para(doc, space_before=0, space_after=2)
        _run(p, f"{category}: ", bold=True, size=10.5)
        _run(p, items, size=10.5)

    # ── Summary (optional) ───────────────────────────────────────────────────
    summary = data.get("summary", "").strip()
    if summary:
        _section_header(doc, "SUMMARY")
        p = _para(doc, space_before=0, space_after=4)
        _run(p, summary, size=10.5)

    # ── Professional Experience ──────────────────────────────────────────────
    _section_header(doc, "PROFESSIONAL EXPERIENCE")
    for job in data.get("experience", []):
        _two_col_row(doc, job["company"], job["location"], left_bold=True)
        _two_col_row(doc, job["title"], job["dates"], left_italic=True, right_italic=True)
        for bullet in job.get("bullets", []):
            _bullet(doc, bullet)

    # ── Project Experience ───────────────────────────────────────────────────
    _section_header(doc, "PROJECT EXPERIENCE")
    for proj in data.get("projects", []):
        _two_col_row(doc, proj["name"], proj.get("dates", ""), left_bold=True)
        for bullet in proj.get("bullets", []):
            _bullet(doc, bullet)

    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


def resume_to_pdf(docx_bytes: bytes) -> bytes | None:
    import os, tempfile
    try:
        from docx2pdf import convert
    except ImportError:
        return None

    with tempfile.TemporaryDirectory() as tmp:
        docx_path = os.path.join(tmp, "resume.docx")
        pdf_path = os.path.join(tmp, "resume.pdf")
        with open(docx_path, "wb") as f:
            f.write(docx_bytes)
        try:
            convert(docx_path, pdf_path)
            with open(pdf_path, "rb") as f:
                return f.read()
        except Exception:
            return None
