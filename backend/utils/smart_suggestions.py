"""
smart_suggestions.py — Role-based skill suggestions using Groq
"""
import json
import re
from backend.utils.groq_client import call_groq


def smart_role_suggestions(resume_skills: list, target_role: str) -> dict:
    prompt = f"""You are an AI Career Coach.

Candidate's current skills: {resume_skills}
Target role: {target_role}

Analyze the gap and return ONLY this exact JSON (no extra text):
{{
  "required_skills": ["skill1", "skill2", "skill3"],
  "missing_skills": ["skill1", "skill2"],
  "message": "One sentence summary of the gap."
}}"""

    try:
        output     = call_groq(prompt, max_tokens=400, system="You are a career coach. Output only valid JSON.")
        json_match = re.search(r"\{.*\}", output, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        print(f"[smart_suggestions] Groq failed: {e}")

    return {"required_skills": [], "missing_skills": [], "message": "AI suggestions unavailable"}
