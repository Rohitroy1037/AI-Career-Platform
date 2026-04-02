"""
smart_skills.py — 3-layer skill extraction (no spacy — Vercel compatible)
Layer 1: Static database (skills.json)
Layer 2: Synonym expansion
Layer 3: Groq AI-powered extraction
"""
import json
import os
from backend.utils.groq_client import call_groq

skill_map = {
    "ml": "machine learning", "nlp": "natural language processing",
    "dl": "deep learning", "ai": "artificial intelligence",
    "cv": "computer vision", "nn": "neural networks",
    "bi": "power bi", "gcp": "google cloud", "k8s": "kubernetes",
    "tf": "tensorflow", "js": "javascript", "ts": "typescript",
    "oop": "object oriented programming", "dsa": "data structures",
}


def load_skills():
    # Try multiple paths — works locally and on Vercel
    candidates = [
        "data/skills.json",
        os.path.join(os.path.dirname(__file__), "../../../data/skills.json"),
        os.path.join(os.path.dirname(__file__), "../../data/skills.json"),
    ]
    for path in candidates:
        try:
            with open(os.path.abspath(path), "r") as f:
                return json.load(f)["skills"]
        except Exception:
            continue
    return []


def _groq_extract_skills(text: str) -> list:
    prompt = f"""Extract ALL technical and professional skills from the text below.

TEXT:
{text[:3000]}

Rules:
- Extract every skill, tool, technology, framework, programming language, and soft skill mentioned.
- Include skills implied by the role even if not explicitly named.
- Return ONLY a JSON array of lowercase skill strings.
- Example: ["python", "machine learning", "sql", "communication"]
- Output ONLY the JSON array. Nothing else."""

    try:
        raw = call_groq(prompt, max_tokens=500,
                        system="You are a skill extraction expert. Output only valid JSON arrays.")
        start, end = raw.find("["), raw.rfind("]")
        if start != -1 and end != -1:
            skills = json.loads(raw[start:end + 1])
            if isinstance(skills, list):
                return [str(s).lower().strip() for s in skills if s]
    except Exception as e:
        print(f"[smart_skills] Groq extraction failed: {e}")
    return []


def smart_extract_skills(text: str) -> list:
    text_lower = text.lower()
    skills_db  = load_skills()
    found      = set()

    # Layer 1: Static DB matching
    for skill in skills_db:
        if skill in text_lower:
            found.add(skill)

    # Layer 2: Synonym expansion
    for key, value in skill_map.items():
        if f" {key} " in f" {text_lower} ":
            found.add(value)

    # Layer 3: Groq AI extraction
    ai_skills = _groq_extract_skills(text)
    found.update(ai_skills)

    return list(found)
