"""
matcher.py — Skills comparison + Groq-powered suggestions
"""
import json
from backend.utils.groq_client import call_groq


def match_skills(resume_skills, job_skills):
    resume_set = set(s.lower() for s in resume_skills)
    job_set    = set(s.lower() for s in job_skills)
    matched    = list(resume_set & job_set)
    missing    = list(job_set - resume_set)
    score      = (len(matched) / len(job_set)) * 100 if job_set else 0
    return {"match_score": round(score, 2), "matched_skills": matched, "missing_skills": missing}


def generate_suggestions(missing_skills: list, job_description: str = "") -> list:
    if not missing_skills:
        return []

    prompt = f"""A job candidate is missing these skills: {', '.join(missing_skills[:15])}
{f'Job context: {job_description[:400]}' if job_description else ''}

For each missing skill, give ONE short, specific, actionable suggestion (max 15 words each).
Return ONLY a JSON array of suggestion strings.
Example: ["Take Python course on Coursera and build 2 projects", "Practice SQL on LeetCode daily"]
Output ONLY the JSON array, nothing else."""

    try:
        raw   = call_groq(prompt, max_tokens=600, system="You are a career coach. Output only valid JSON arrays.")
        start, end = raw.find("["), raw.rfind("]")
        if start != -1 and end != -1:
            suggestions = json.loads(raw[start:end + 1])
            if isinstance(suggestions, list) and suggestions:
                return [str(s) for s in suggestions]
    except Exception as e:
        print(f"[matcher] Groq suggestions failed: {e}")

    return [f"Build hands-on projects with {skill} to demonstrate proficiency" for skill in missing_skills[:8]]
