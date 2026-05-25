"""
roadmap.py — AI-powered learning roadmap using Groq
"""
import json
from backend.utils.groq_client import call_groq


def generate_roadmap(missing_skills: list, semantic_score: float,
                     resume_text: str = "", job_description: str = "") -> list:
    """
    Groq/llama3 se prioritized JSON roadmap generate karo.
    Fallback: template-based roadmap agar API fail ho.
    """
    try:
        context = ""
        if resume_text:
            context += f"\n\nCANDIDATE RESUME:\n{resume_text[:2500]}"
        if job_description:
            context += f"\n\nTARGET JOB / ROLE:\n{job_description[:2500]}"
        if missing_skills:
            context += f"\n\nSKILLS ALREADY IDENTIFIED AS MISSING: {', '.join(missing_skills)}"

        prompt = f"""You are an expert career coach and technical mentor.
{context}

Your task:
1. Analyse the candidate resume against the job description.
2. Identify ALL important skills required for this role (technical + soft skills).
3. Rank skills by importance — most critical first.
4. For each skill, state whether the candidate HAS it or is MISSING it.
5. For each MISSING skill, write a concrete 3-step learning plan specific to this role.
6. Mark the TOP 3 most critical missing skills with focus_first=true.

IMPORTANT: Respond ONLY with a valid JSON array. No explanation, no markdown fences, nothing else.

Each item must have EXACTLY these fields:
[
  {{
    "skill": "skill name",
    "status": "missing",
    "priority": "critical",
    "importance_reason": "Why this skill matters for this specific role (1-2 sentences).",
    "plan": "Step 1 → Step 2 → Step 3",
    "focus_first": true
  }}
]

Rules:
- "status" must be exactly "missing" or "have"
- "priority" must be exactly "critical", "important", or "nice-to-have"
- focus_first = true only for the top 3 missing skills
- For "have" skills: plan = "", focus_first = false
- Include 8 to 15 skills total
- Output ONLY the JSON array"""

        raw = call_groq(prompt, max_tokens=2000,
                        system="You are a career coach. Output only valid JSON arrays.")

        # Robust JSON extraction
        if "```" in raw:
            for part in raw.split("```"):
                part = part.strip().lstrip("json").strip()
                if part.startswith("["):
                    raw = part
                    break

        start, end = raw.find("["), raw.rfind("]")
        if start != -1 and end != -1:
            roadmap = json.loads(raw[start:end + 1])
            if isinstance(roadmap, list) and roadmap:
                return roadmap

    except Exception as e:
        print(f"[roadmap] Groq error: {e} — using fallback")

    # ── Fallback template ─────────────────────────────────────────────────────
    if missing_skills:
        return [
            {
                "skill": skill,
                "status": "missing",
                "priority": "critical" if i < 3 else "important",
                "importance_reason": f"{skill} is required for this role.",
                "plan": (f"Learn {skill} fundamentals via official docs or a course"
                         f" → Build a hands-on project using {skill}"
                         f" → Add to GitHub portfolio with documentation"),
                "focus_first": i < 3,
            }
            for i, skill in enumerate(missing_skills)
        ]

    if semantic_score < 50:
        return [
            {"skill": "Real-world Projects", "status": "missing", "priority": "critical",
             "importance_reason": "Demonstrable project experience is essential.",
             "plan": "Choose 2 role-relevant projects → Build and document them → Deploy publicly",
             "focus_first": True},
            {"skill": "Resume Optimisation", "status": "missing", "priority": "important",
             "importance_reason": "Tailored resume improves ATS pass rates significantly.",
             "plan": "Rewrite bullets with action verbs + metrics → Add job keywords → ATS check",
             "focus_first": True},
            {"skill": "Domain Knowledge", "status": "missing", "priority": "important",
             "importance_reason": "Deep domain knowledge differentiates you in interviews.",
             "plan": "Study advanced role-specific topics → Follow industry blogs → Join communities",
             "focus_first": True},
        ]
    return []
