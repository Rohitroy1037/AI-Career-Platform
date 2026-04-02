"""
semantic.py — Lightweight semantic similarity using TF-IDF + cosine similarity.
Replaces sentence-transformers (which pulls PyTorch ~800MB, too heavy for Vercel).
TF-IDF gives good enough similarity for resume vs job description comparison.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def semantic_match(resume_text: str, job_text: str) -> float:
    """
    Returns a 0–100 similarity score between resume and job description.
    Uses TF-IDF vectorization + cosine similarity — no heavy ML model needed.
    """
    if not resume_text or not job_text:
        return 0.0

    try:
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        tfidf = vectorizer.fit_transform([resume_text, job_text])
        score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return float(score) * 100
    except Exception:
        return 0.0
