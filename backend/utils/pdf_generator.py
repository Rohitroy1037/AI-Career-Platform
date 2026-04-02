from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.colors import HexColor
import re

TEAL  = HexColor('#2E75B6')
DGRAY = HexColor('#404040')
BLACK = HexColor('#000000')


def _small_caps(text: str, big: int = 10, small: int = 8) -> str:
    if not text:
        return text
    return (f'<font size="{big}">{text[0].upper()}</font>'
            + f'<font size="{small}">{text[1:].upper()}</font>')


def generate_pdf(text: str, filename: str = "resume.pdf") -> str:

    PAGE_W, _ = A4
    LM = RM   = 54
    BODY_W    = PAGE_W - LM - RM   # 487 pt

    doc = SimpleDocTemplate(
        filename, pagesize=A4,
        leftMargin=LM, rightMargin=RM,
        topMargin=32, bottomMargin=32,
    )

    # ── Style helper ─────────────────────────────────────────────────────────
    def S(name, **kw):
        base = dict(fontName='Helvetica', fontSize=9, leading=12,
                    textColor=BLACK, spaceAfter=0, spaceBefore=0)
        base.update(kw)
        return ParagraphStyle(name, **base)

    name_sty    = S('Name',  fontName='Helvetica-Bold', fontSize=21, leading=24)
    cont_sty    = S('Cont',  fontSize=9, leading=12)
    cont_R_sty  = S('ContR', fontSize=9, leading=12, alignment=TA_RIGHT, textColor=TEAL)
    sec_sty     = S('Sec',   fontName='Helvetica', fontSize=9, textColor=DGRAY,
                    spaceBefore=5, spaceAfter=1, leading=11)
    lbl_sty     = S('Lbl',   fontName='Helvetica-Bold', textColor=TEAL,
                    fontSize=9, leading=12)
    val_sty     = S('Val',   fontSize=9, leading=12)
    etitle_sty  = S('ET',    fontName='Helvetica-Bold', textColor=TEAL,
                    fontSize=9, leading=12)
    date_sty    = S('Date',  fontSize=9, leading=12, alignment=TA_RIGHT)
    bull_sty    = S('Bull',  fontSize=9, leading=12, leftIndent=10)
    tech_sty    = S('Tech',  fontName='Helvetica-Bold', fontSize=9,
                    leading=12, spaceAfter=3)
    edu_i_sty   = S('EduI',  fontName='Helvetica-Bold', textColor=TEAL,
                    fontSize=9, leading=12)
    edu_l_sty   = S('EduL',  fontName='Helvetica-Bold', textColor=TEAL,
                    fontSize=9, leading=12, alignment=TA_RIGHT)
    edu_d_sty   = S('EduD',  fontSize=9, leading=12, spaceAfter=3)
    deg_d_sty   = S('DegD',  fontSize=9, leading=12, alignment=TA_RIGHT)
    cert_sty    = S('Cert',  fontSize=9, leading=12)
    cert_d_sty  = S('CertD', fontSize=9, leading=12, alignment=TA_RIGHT)
    norm_sty    = S('Norm',  fontSize=9, leading=12)

    # ── Flowable helpers ─────────────────────────────────────────────────────
    def HR():
        return HRFlowable(width='100%', thickness=0.5, color=DGRAY, spaceAfter=2)

    def tbl(data, widths, pad=0):
        t = Table(data, colWidths=widths)
        t.setStyle(TableStyle([
            ('VALIGN',        (0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',   (0,0),(-1,-1), pad),
            ('RIGHTPADDING',  (0,0),(-1,-1), pad),
            ('TOPPADDING',    (0,0),(-1,-1), 0),
            ('BOTTOMPADDING', (0,0),(-1,-1), 1),
        ]))
        return t

    def two_col(lp, rp, lf=0.65):
        lw, rw = BODY_W*lf, BODY_W*(1-lf)
        return tbl([[lp, rp]], [lw, rw])

    def section_block(txt):
        return [Paragraph(_small_caps(txt), sec_sty), HR()]

    # ── SKILLS table ─────────────────────────────────────────────────────────
    def skills_tbl(rows):
        lw, rw = BODY_W*0.30, BODY_W*0.70
        data = [[Paragraph(f'{l}:', lbl_sty), Paragraph(v, val_sty)]
                for l, v in rows]
        t = Table(data, colWidths=[lw, rw])
        t.setStyle(TableStyle([
            ('VALIGN',        (0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',   (0,0),(-1,-1), 0),
            ('RIGHTPADDING',  (0,0),(-1,-1), 0),
            ('TOPPADDING',    (0,0),(-1,-1), 1),
            ('BOTTOMPADDING', (0,0),(-1,-1), 1),
        ]))
        return t

    # ── CERT table ───────────────────────────────────────────────────────────
    def cert_tbl(rows):
        lw, rw = BODY_W*0.85, BODY_W*0.15
        data = [[Paragraph(f'• {t}', cert_sty), Paragraph(d, cert_d_sty)]
                for t, d in rows]
        t = Table(data, colWidths=[lw, rw])
        t.setStyle(TableStyle([
            ('VALIGN',        (0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',   (0,0),(-1,-1), 0),
            ('RIGHTPADDING',  (0,0),(-1,-1), 0),
            ('TOPPADDING',    (0,0),(-1,-1), 1),
            ('BOTTOMPADDING', (0,0),(-1,-1), 1),
        ]))
        return t

    # ── entry title: "CineMatch — Subtitle | Github  Feb' 26 – Mar' 26" ──────
    def entry_title_row(raw: str):
        raw = raw.strip()
        # Date pattern: "Mon' YY" at the end, possibly with em-dash range
        date_m = re.search(r"([A-Z][a-z]{2,}'\s*\d{2}\s*[–\-]\s*(?:[A-Z][a-z]{2,}'\s*\d{2}|Present))$", raw)
        if date_m:
            date_str = date_m.group(1).strip()
            title_str = raw[:date_m.start()].rstrip()
        else:
            # Fallback: split on last space cluster near end
            parts = raw.rsplit(None, 3)
            if len(parts) >= 3 and "'" in parts[-1]:
                date_str  = ' '.join(parts[-3:])
                title_str = ' '.join(parts[:-3])
            else:
                title_str = raw
                date_str  = ''
        return two_col(
            Paragraph(title_str, etitle_sty),
            Paragraph(date_str,  date_sty),
            lf=0.70,
        )

    # ── education institution: "Lovely Professional University Phagwara, Punjab" ─
    def edu_inst_row(raw: str):
        raw = raw.strip()
        # Find last comma: everything after last comma (stripped) = state
        # Everything from comma-word onward = location
        tokens = raw.split()
        loc_start = None
        for i in range(len(tokens)-1, 0, -1):
            if tokens[i-1].endswith(','):
                loc_start = i - 1   # index of "City,"
                break
        if loc_start is not None:
            inst = ' '.join(tokens[:loc_start]).rstrip(',')
            loc  = tokens[loc_start].rstrip(',') + ', ' + ' '.join(tokens[loc_start+1:])
        else:
            inst = raw
            loc  = ''
        lp = Paragraph(inst, edu_i_sty)
        rp = Paragraph(loc,  edu_l_sty)
        return two_col(lp, rp, lf=0.60)

    # ── education degree row: degree left, date range right ─────────────────
    DATE_RE = re.compile(
        r"([A-Z][a-z]{2,}'\s*\d{2}\s*[–\-]\s*(?:[A-Z][a-z]{2,}'\s*\d{2}|Present))"
    )
    def edu_degree_row(raw: str):
        raw = raw.strip()
        m = DATE_RE.search(raw)
        if m:
            date_str   = m.group(1).strip()
            degree_str = raw[:m.start()].rstrip('; ').rstrip()
        else:
            degree_str = raw
            date_str   = ''
        lp = Paragraph(degree_str, edu_d_sty)
        rp = Paragraph(date_str,   deg_d_sty)
        return two_col(lp, rp, lf=0.62)

    # ── Parse cert line: "Infosys … | Certificate Link | Certificate Sep' 25" ─
    def parse_cert(raw: str):
        raw = raw.lstrip('•').strip()
        # Date is the last token-group after the final "|"
        parts = raw.rsplit('|', 1)
        if len(parts) == 2:
            txt  = parts[0].strip()
            date_raw = parts[1].strip()
            # Strip leading "Certificate " prefix if present
            date_raw = re.sub(r'^Certificate\s+', '', date_raw).strip()
        else:
            txt      = raw
            date_raw = ''
        return txt, date_raw

    # ── Main parse loop ──────────────────────────────────────────────────────
    lines = [l.rstrip() for l in text.split('\n')]
    while lines and not lines[0].strip():  lines.pop(0)
    while lines and not lines[-1].strip(): lines.pop()

    content       = []
    idx           = 0
    cur_sec       = None
    skill_rows    = []
    cert_rows     = []

    def flush_skills():
        if skill_rows:
            content.append(skills_tbl(skill_rows))
            skill_rows.clear()

    def flush_certs():
        if cert_rows:
            content.append(cert_tbl(cert_rows))
            cert_rows.clear()

    def is_heading(s):
        return s.isupper() and len(s) > 2 and not s.startswith('•')

    # NAME
    content.append(Paragraph(lines[idx].strip(), name_sty))
    idx += 1

    # CONTACT BLOCK — until first uppercase heading
    while idx < len(lines) and not is_heading(lines[idx].strip()):
        s = lines[idx].strip()
        idx += 1
        if not s:
            continue
        # Split line on Email: / Mobile: / Phone: to put right side in teal+right-align
        for kw in ('Email:', 'Mobile:', 'Phone:'):
            if kw in s:
                pos   = s.index(kw)
                left  = s[:pos].rstrip()
                right = s[pos:].strip()
                content.append(two_col(
                    Paragraph(left,  cont_sty),
                    Paragraph(right, cont_R_sty),
                    lf=0.52,
                ))
                break
        else:
            content.append(Paragraph(s, cont_sty))

    content.append(Spacer(1, 5))

    # SECTIONS
    while idx < len(lines):
        line = lines[idx]
        s    = line.strip()
        idx += 1
        if not s:
            continue

        # ── Heading ───────────────────────────────────────────────────────
        if is_heading(s):
            flush_skills()
            flush_certs()
            cur_sec = s
            for e in section_block(s):
                content.append(e)
            continue

        # ── SKILLS ────────────────────────────────────────────────────────
        if cur_sec == 'SKILLS':
            if ':' in s:
                ci  = s.index(':')
                lbl = s[:ci].lstrip('•').strip()
                val = s[ci+1:].strip()
                skill_rows.append((lbl, val))
            continue

        # ── PROJECTS / TRAINING ───────────────────────────────────────────
        if cur_sec in ('PROJECTS', 'TRAINING'):
            # Tech line
            if re.match(r'^\s*Tech:', s, re.IGNORECASE):
                content.append(Paragraph(s.strip(), tech_sty))
                content.append(Spacer(1, 2))
                continue
            # Bullet
            if s.startswith('•'):
                content.append(Paragraph(s, bull_sty))
                continue
            # Entry title: has | and date
            if '|' in s and re.search(r"'\s*\d{2}", s):
                content.append(entry_title_row(s))
                continue
            content.append(Paragraph(s, norm_sty))
            continue

        # ── CERTIFICATION ─────────────────────────────────────────────────
        if 'CERTIF' in cur_sec.upper():
            txt, date = parse_cert(s)
            cert_rows.append((txt, date))
            continue

        # ── ACHIEVEMENTS ──────────────────────────────────────────────────
        if cur_sec == 'ACHIEVEMENTS':
            if not s.startswith('•'):
                s = '• ' + s
            content.append(Paragraph(s, bull_sty))
            continue

        # ── EDUCATION ─────────────────────────────────────────────────────
        if cur_sec == 'EDUCATION':
            flush_certs()
            # Degree / detail: contains ";" or "%" or "Present"
            if ';' in s or '%' in s or 'Present' in s:
                content.append(edu_degree_row(s))
                continue
            # Institution line
            content.append(edu_inst_row(s))
            continue

        content.append(Paragraph(s, norm_sty))

    flush_skills()
    flush_certs()

    doc.build(content)
    return filename
