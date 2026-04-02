"""
groq_client.py — Central Groq API helper
All AI calls in this project go through this single function.
Model: llama-3.1-8b-instant (fast, free tier available on Groq)

On Vercel: Set GROQ_API_KEY in your Vercel project dashboard under Settings → Environment Variables
Locally:   Set it in backend/.env file
"""
import requests
import os

try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))
except Exception:
    pass

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL   = "llama-3.1-8b-instant"


def call_groq(prompt: str, max_tokens: int = 1000, system: str = "You are a helpful assistant.") -> str:
    if not GROQ_API_KEY:
        return "⚠️ GROQ_API_KEY not configured. Set it in Vercel dashboard → Settings → Environment Variables."

    if not prompt or not prompt.strip():
        return "⚠️ Empty input."

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        body = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user",   "content": prompt.strip()[:4000]},
            ],
            "max_tokens": max_tokens,
            "temperature": 0.3,
        }
        response = requests.post(GROQ_API_URL, headers=headers, json=body, timeout=30)

        print(f"[groq] status={response.status_code}")

        if response.status_code != 200:
            print(f"[groq] error body: {response.text[:300]}")
            return "⚠️ AI service error. Please try again."

        return response.json()["choices"][0]["message"]["content"].strip()

    except requests.exceptions.Timeout:
        return "⚠️ Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return "⚠️ Network error. Check your internet connection."
    except Exception as e:
        print(f"[groq] exception: {e}")
        return "⚠️ Something went wrong. Please try again."
