"""
AI Career Intelligence Platform
================================
    python run.py
Then open: http://localhost:8000

Powered by: FastAPI + Groq API (llama3-8b-8192) + Sentence Transformers

IMPORTANT: Groq API key is already set in groq_client.py
If you want to use environment variable instead:
    export GROQ_API_KEY=gsk_your_key_here
    python run.py
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
