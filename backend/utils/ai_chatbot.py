"""
ai_chatbot.py — AI Career Mentor chatbot using Groq
"""
from backend.utils.memory import get_memory
from backend.utils.groq_client import call_groq


def ai_chatbot(user_input: str, resume_text: str = "", user_id: str = "default") -> str:
    history      = get_memory(user_id)
    history_text = ""
    for item in history[-3:]:
        history_text += f"User: {item['question']}\nAssistant: {item['response']}\n\n"

    prompt = f"""Previous Conversation:
{history_text if history_text else 'None'}

{"Candidate's Resume:\n" + resume_text[:1500] if resume_text else ""}

Current Question: {user_input}

Give personalized, specific, and actionable career advice based on the above context."""

    return call_groq(
        prompt,
        max_tokens=700,
        system=(
            "You are an expert AI Career Mentor. Give personalized, practical, and encouraging "
            "career advice. Be specific, not generic. Focus on actionable next steps."
        )
    )
