"""
groq_client.py — FIXED VERSION (Safe + Stable)

✔ No hardcoded API key
✔ No backend crash
✔ Debug logs added
✔ Handles 400/500 errors safely
✔ Prevents large prompt issues
"""
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# ✅ Only environment variable (NO hardcoded key)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not set. Please set environment variable.")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"


def call_groq(prompt: str, max_tokens: int = 1000, system: str = "You are a helpful assistant.") -> str:
    try:
        # ✅ Prevent empty input
        if not prompt or not prompt.strip():
            return "⚠️ Empty input."

        # ✅ Limit prompt size (prevents 400 error)
        prompt = prompt.strip()[:4000]

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }

        body = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": max_tokens,
            "temperature": 0.3,
        }

        response = requests.post(
            GROQ_API_URL,
            headers=headers,
            json=body,
            timeout=30
        )

        # 🔍 Debug logs (VERY IMPORTANT)
        print("Groq Status:", response.status_code)
        print("Groq Response:", response.text)

        # ❌ If error, return safe message instead of crash
        if response.status_code != 200:
            return "⚠️ AI service error. Please try again."

        data = response.json()

        return data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

    except requests.exceptions.Timeout:
        return "⚠️ Request timeout."

    except requests.exceptions.ConnectionError:
        return "⚠️ Network error."

    except Exception as e:
        print("Groq Exception:", str(e))
        return "⚠️ Something went wrong."