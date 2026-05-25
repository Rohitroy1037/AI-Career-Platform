from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER


def generate_pdf(text: str, filename="resume.pdf"):

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    # 🔥 Styles
    name_style = ParagraphStyle(
        name="Name",
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=6,
        fontName="Helvetica-Bold"
    )

    contact_style = ParagraphStyle(
        name="Contact",
        fontSize=9,
        alignment=TA_CENTER,
        spaceAfter=10
    )

    section_style = ParagraphStyle(
        name="Section",
        fontSize=11,
        spaceBefore=8,
        spaceAfter=4,
        fontName="Helvetica-Bold"
    )

    normal_style = ParagraphStyle(
        name="Normal",
        fontSize=9,
        leading=12
    )

    content = []

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # 🔥 NAME
    content.append(Paragraph(lines[0], name_style))

    # 🔥 CONTACT (single line like original CV)
    content.append(Paragraph(lines[1], contact_style))

    current_section = None

    for line in lines[2:]:

        # SECTION HEADINGS
        if line.isupper():
            content.append(Paragraph(line, section_style))
            current_section = line
            continue

        # PROJECT TITLE (bold)
        if "|" in line and not line.startswith("•"):
            content.append(Paragraph(f"<b>{line}</b>", normal_style))
            continue

        # BULLETS
        if line.startswith("•"):
            content.append(Paragraph(line, normal_style))
            continue

        # TECH LINE
        if "Tech:" in line:
            content.append(Paragraph(f"<i>{line}</i>", normal_style))
            content.append(Spacer(1, 4))
            continue

        # NORMAL TEXT
        content.append(Paragraph(line, normal_style))

    doc.build(content)
    return filename