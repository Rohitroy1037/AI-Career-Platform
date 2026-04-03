"""
pdf_generator.py — Generates a downloadable PDF resume.
Uses reportlab if available, falls back to plain text .txt file.
"""
import os
import tempfile


def generate_pdf(resume_text: str) -> str:
    """
    Returns path to a generated file (PDF if reportlab available, else .txt).
    Always writes to /tmp which is writable on Vercel.
    """
    tmp_dir = tempfile.gettempdir()

    try:
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.pagesizes import A4

        out_path = os.path.join(tmp_dir, "resume_output.pdf")
        doc = SimpleDocTemplate(out_path, pagesize=A4,
                                rightMargin=50, leftMargin=50,
                                topMargin=50, bottomMargin=50)
        styles = getSampleStyleSheet()
        story = []
        for line in resume_text.split("\n"):
            if line.strip():
                story.append(Paragraph(line.strip(), styles["Normal"]))
                story.append(Spacer(1, 6))
        doc.build(story)
        return out_path

    except ImportError:
        # reportlab not installed — return as plain text file
        out_path = os.path.join(tmp_dir, "resume_output.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(resume_text)
        return out_path
