import os
import pdfplumber

def extract_text_from_pdf(file):
    """
    Extract text from PDF, DOCX, DOC, or TXT files.
    Function name kept as-is so no other backend file needs changes.
    """
    ext = os.path.splitext(str(file))[-1].lower()

    # ── PDF ──────────────────────────────────────────────────────────────────
    if ext == ".pdf" or ext == "":
        text = ""
        try:
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    if page.extract_text():
                        text += page.extract_text()
        except Exception:
            pass
        return text.lower()

    # ── DOCX ─────────────────────────────────────────────────────────────────
    elif ext in (".docx", ".doc"):
        try:
            from docx import Document
            doc = Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text.lower()
        except Exception as e:
            return f"could not read docx file: {e}"

    # ── TXT / others ─────────────────────────────────────────────────────────
    else:
        try:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                return f.read().lower()
        except Exception as e:
            return f"could not read file: {e}"
