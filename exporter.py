import io
import os
import tempfile
from datetime import date

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

from resume_context import CANDIDATE_NAME, CANDIDATE_EMAIL, CANDIDATE_PHONE


def _set_font(run, name="Calibri", size=11, bold=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = RGBColor(*color)


def _add_paragraph(doc, text, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    return p, p.add_run(text)


def to_docx(letter_body: str, company: str = "") -> bytes:
    doc = Document()

    # Margins: 0.75" top/bottom, 1" left/right — tight but professional
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)

    # Header: name
    p, run = _add_paragraph(doc, CANDIDATE_NAME, WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    _set_font(run, size=14, bold=True)

    # Header: contact
    p, run = _add_paragraph(
        doc,
        f"{CANDIDATE_PHONE} | {CANDIDATE_EMAIL}",
        WD_ALIGN_PARAGRAPH.CENTER,
        space_after=8,
    )
    _set_font(run, size=11)

    # Date
    today = date.today().strftime("%B %-d, %Y") if os.name != "nt" else date.today().strftime("%B %#d, %Y")
    p, run = _add_paragraph(doc, today, space_after=6)
    _set_font(run, size=11)

    # Recipient block
    if company:
        p, run = _add_paragraph(doc, "Hiring Team", space_after=0)
        _set_font(run, size=11)
        p, run = _add_paragraph(doc, company, space_after=8)
        _set_font(run, size=11)

    # Letter body — split on blank lines into paragraphs
    paragraphs = [p.strip() for p in letter_body.split("\n\n") if p.strip()]
    for i, para_text in enumerate(paragraphs):
        space = 8 if i < len(paragraphs) - 1 else 0
        p, run = _add_paragraph(doc, para_text, space_after=space)
        _set_font(run, size=11)

    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


def to_pdf(docx_bytes: bytes) -> bytes | None:
    try:
        from docx2pdf import convert  # noqa: PLC0415
    except ImportError:
        return None

    with tempfile.TemporaryDirectory() as tmp:
        docx_path = os.path.join(tmp, "cover_letter.docx")
        pdf_path = os.path.join(tmp, "cover_letter.pdf")
        with open(docx_path, "wb") as f:
            f.write(docx_bytes)
        try:
            convert(docx_path, pdf_path)
            with open(pdf_path, "rb") as f:
                return f.read()
        except Exception:
            return None
