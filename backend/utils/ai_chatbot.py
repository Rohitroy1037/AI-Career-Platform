"""
ai_chatbot.py
"""

from backend.utils.memory import get_memory
from backend.utils.groq_client import call_groq


def ai_chatbot(
        user_input: str,
        resume_text: str="",
        user_id: str="default"
):

    history = get_memory(user_id)

    # Keep only recent user questions
    recent_questions = []

    for item in history[-3:]:
        if item.get("question"):
            recent_questions.append(item["question"])

    history_text = "\n".join(recent_questions)

    prompt = f"""
Recent User Questions:
{history_text if history_text else "None"}

Current Question:
{user_input}

Resume:
{resume_text[:500] if resume_text else "None"}

Instructions:

- Focus ONLY on Current Question.
- Use previous questions only if related.
- Ignore previous assistant responses.
- Use resume only when relevant.
- Do not assume user intent.
- Give direct answer.
"""

    return call_groq(
        prompt=prompt,
        max_tokens=500,
        system="""
You are an intelligent AI assistant.

Important:
- Current Question has highest priority.
- Ignore unrelated conversation history.
- Do not mention previous conversations unless needed.
- Do not say "based on previous conversation".
- Answer naturally.
"""
    )