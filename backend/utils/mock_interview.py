"""
mock_interview.py — Interview question generation + strict answer evaluation via Groq
"""
from backend.utils.groq_client import call_groq


def generate_question(role: str) -> str:
    prompt = f"""Generate exactly ONE challenging, specific technical interview question for the role: {role}

The question must:
- Test real technical knowledge, not generic personality
- Be specific to the core responsibilities of this role
- Be something a senior interviewer would actually ask

Output ONLY the question. No numbering, no preamble, no explanation."""

    return call_groq(prompt, max_tokens=200,
                     system="You are a strict senior technical interviewer. Output only the question.")


def evaluate_answer(role: str, question: str, answer: str) -> str:
    answer_stripped = answer.strip()
    word_count      = len(answer_stripped.split())

    # Copy-paste detection
    q_words        = set(question.lower().split())
    a_words        = set(answer_stripped.lower().split())
    overlap        = len(q_words & a_words) / max(len(q_words), 1)
    is_copy_paste  = overlap > 0.7 or answer_stripped.lower() == question.lower()

    prompt = f"""You are a RUTHLESSLY STRICT senior technical interviewer evaluating a candidate for: {role}

QUESTION: {question}

CANDIDATE'S ANSWER: {answer_stripped}

ANSWER WORD COUNT: {word_count}
COPY-PASTE DETECTED: {is_copy_paste}

=== MANDATORY SCORING RULES — STRICTLY FOLLOW, NO EXCEPTIONS ===

RULE 1 — INSTANT 0/10:
- COPY-PASTE DETECTED is True → score MUST be 0/10, no matter what
- Answer is completely off-topic or irrelevant → 0/10

RULE 2 — 1-2/10:
- Fewer than 15 words → 1/10
- Gibberish, "I don't know", or meaningless filler → 1-2/10

RULE 3 — 3-4/10:
- Vague with no technical depth
- Mentions concept but cannot explain it properly
- Generic definition, no real application

RULE 4 — 5-6/10:
- Partially correct, missing key technical points
- Some understanding but incomplete

RULE 5 — 7-8/10:
- Clear, accurate, technically sound
- Addresses question directly with relevant detail
- Shows genuine understanding

RULE 6 — 9-10/10:
- EXCEPTIONAL only — thorough, accurate, with examples and edge cases
- Must be extremely rare. Do NOT give 9-10 easily.

=== OUTPUT FORMAT — USE EXACTLY THIS STRUCTURE ===

Score: X/10

Strengths:
[What was good. Write "None" if answer was poor, too short, or copy-pasted.]

Weaknesses:
[Specific technical gaps, errors, or missing depth. Be precise and harsh.]

What a Strong Answer Looks Like:
[A model answer (3-5 sentences) that deserves 9/10. Be specific and technical.]

Tip to Improve:
[One concrete, actionable suggestion specific to this answer.]"""

    return call_groq(prompt, max_tokens=800,
                     system="You are a ruthlessly strict technical interviewer. Follow scoring rules exactly.")
