import requests
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"


def call_groq(prompt: str,
              max_tokens: int = 1000,
              system: str = "You are a helpful assistant."):

    if not GROQ_API_KEY:
        print("Missing GROQ_API_KEY")
        return "⚠️ AI service temporarily unavailable."

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens
        }

        response = requests.post(
            GROQ_API_URL,
            headers=headers,
            json=body,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print(f"Groq Error: {str(e)}")
        return "⚠️ AI service temporarily unavailable."