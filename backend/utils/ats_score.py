"""
ats_score.py — ATS scoring + Groq AI suggestions
"""
from backend.utils.groq_client import call_groq


def advanced_ats_score(resume_text, job_skills):
    text    = resume_text.lower()
    matched = [s for s in job_skills if s.lower() in text]
    missing = [s for s in job_skills if s.lower() not in text]

    score = (len(matched) / len(job_skills)) * 50 if job_skills else 0
    score += sum(2 for s in job_skills if text.count(s.lower()) >= 2)

    sections = {
        "skills":     "skills"     in text,
        "experience": "experience" in text,
        "projects":   "project"    in text,
        "education":  "education"  in text,
    }
    score += sum(5 for v in sections.values() if v)

    issues = []
    if len(text) < 300:
        issues.append("Resume content is too short")
    if not matched:
        issues.append("No relevant keywords found — add job-specific skills")
    if len(missing) > len(matched):
        issues.append("Many required skills are missing from your resume")

    return {
        "ats_score":        round(min(score, 100), 2),
        "matched_keywords": matched,
        "missing_keywords": missing,
        "sections":         sections,
        "issues":           issues,
    }


def ats_score_breakdown(resume_text, job_skills):
    text          = resume_text.lower()
    matched       = [s for s in job_skills if s.lower() in text] if job_skills else []
    keyword_score = int((len(matched) / len(job_skills)) * 100) if job_skills else 0

    sections = ["skills" in text, "experience" in text, "project" in text, "education" in text]
    formatting_score = int((sum(sections) / len(sections)) * 100)

    return {
        "skills_score":    keyword_score,
        "formatting_score": formatting_score,
        "keyword_score":   keyword_score,
    }


def ats_ai_suggestions(resume_text: str, job_skills: list) -> str:
    missing = [s for s in job_skills if s.lower() not in resume_text.lower()]

    prompt = f"""You are an expert ATS resume coach.

RESUME (excerpt):
{resume_text[:2000]}

REQUIRED SKILLS: {', '.join(job_skills) if job_skills else 'Not specified'}
MISSING FROM RESUME: {', '.join(missing) if missing else 'None'}

Give 4-6 specific, actionable suggestions to improve this resume for ATS optimization.
Focus on: missing skills to add, resume bullet improvements, keywords to include, structure fixes.
Be direct and specific. No generic advice."""

    try:
        return call_groq(prompt, max_tokens=600, system="You are an ATS resume expert. Give specific, actionable advice.")
    except Exception as e:
        return f"AI suggestions unavailable: {e}"
