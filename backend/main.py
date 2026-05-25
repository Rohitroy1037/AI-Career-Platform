import sys
import os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.utils.parser import extract_text_from_pdf
from backend.utils.smart_skills import smart_extract_skills
from backend.utils.matcher import match_skills
from backend.utils.semantic import semantic_match
from backend.utils.roadmap import generate_roadmap
from backend.utils.resume_improver import improve_resume
from backend.utils.success_predictor import predict_success
from backend.utils.ai_chatbot import ai_chatbot
from backend.utils.memory import save_memory
from backend.utils.db import init_db
from backend.utils.ats_score import advanced_ats_score
from backend.utils.ats_score import ats_ai_suggestions
from backend.utils.resume_autofix import auto_fix_resume
from backend.utils.ats_score import ats_score_breakdown
from backend.utils.matcher import match_skills, generate_suggestions
from backend.utils.smart_suggestions import smart_role_suggestions
from backend.utils.mock_interview import generate_question, evaluate_answer
import tempfile

# ✅ Step 1: App define
app = FastAPI()

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Frontend path ─────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = FRONTEND_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
# ─────────────────────────────────────────────────────────────────────────────

init_db()

# ── Helper: save upload keeping original extension ────────────────────────────
def save_upload(file_bytes: bytes, original_filename: str) -> str:
    ext = os.path.splitext(original_filename)[-1].lower() or ".pdf"
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(file_bytes)
        return tmp.name
# ─────────────────────────────────────────────────────────────────────────────

# ✅ Step 2: Feedback function
def generate_feedback(match_score, semantic_score):
    if semantic_score > 75:
        return "Excellent fit for this role 🚀"
    elif semantic_score > 50:
        return "Good match but can improve some areas 👍"
    else:
        return "Skills match but profile needs improvement ⚠️"

# ✅ Step 3: Home route — serves frontend UI
@app.get("/", response_class=HTMLResponse)
def home():
    return (FRONTEND_DIR / "index.html").read_text(encoding="utf-8")

# ✅ Step 4: Main API
@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    temp_path = save_upload(await file.read(), file.filename)

    resume_text = extract_text_from_pdf(temp_path)
    improved_resume = improve_resume(resume_text)
    resume_skills = smart_extract_skills(resume_text)

    # ✅ FIX: wrap Ollama calls in try/except so they never crash /analyze
    target_role = job_description[:200]  # use actual job description
    try:
        smart_data = smart_role_suggestions(resume_skills, target_role)
    except Exception:
        smart_data = {"required_skills": [], "missing_skills": [], "message": "AI suggestions unavailable (Ollama offline)"}

    job_skills = smart_extract_skills(job_description.lower())
    ats_result = advanced_ats_score(resume_text, job_skills)

    try:
        ats_ai = ats_ai_suggestions(resume_text, job_skills)
    except Exception:
        ats_ai = "ATS AI suggestions unavailable (Ollama offline)"

    breakdown = ats_score_breakdown(resume_text, job_skills)
    result = match_skills(resume_skills, job_skills)
    suggestions = generate_suggestions(result["missing_skills"], job_description)
    semantic_score = semantic_match(resume_text, job_description)
    success_probability = predict_success(result["match_score"], semantic_score)
    roadmap = generate_roadmap(result["missing_skills"], semantic_score,
                               resume_text=resume_text, job_description=job_description)
    feedback = generate_feedback(result["match_score"], semantic_score)

    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "analysis": result,
        "suggestions": suggestions,
        "smart_suggestions": smart_data,
        "semantic_score": round(semantic_score, 2),
        "feedback": feedback,
        "roadmap": roadmap,
        "improved_resume": improved_resume,
        "success_probability": success_probability,
        "ats_analysis": ats_result,
        "ats_ai_suggestions": ats_ai,
        "score_breakdown": breakdown
    }

# ✅ AI Career Chatbot Route
@app.post("/ai-chat")
async def chat(
    user_input: str = Form(...),
    user_id: str = Form("default"),
    file: UploadFile = File(None)
):
    resume_text = ""
    if file:
        temp_path = save_upload(await file.read(), file.filename)
        resume_text = extract_text_from_pdf(temp_path)

    response = ai_chatbot(user_input, resume_text, user_id)
    save_memory(user_id, user_input, response)
    return {"response": response}

# ✅ Auto Fix Route
@app.post("/auto-fix")
async def auto_fix(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    temp_path = save_upload(await file.read(), file.filename)
    resume_text = extract_text_from_pdf(temp_path)
    fixed_resume = auto_fix_resume(resume_text, job_description)
    return {"fixed_resume": fixed_resume}

@app.post("/job-match")
async def job_match_api(
    resume_skills: list,
    job_skills: list
):
    result = match_skills(resume_skills, job_skills)
    suggestions = generate_suggestions(result["missing_skills"])

    return {
        "match_score": result["match_score"],
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "suggestions": suggestions
    }

@app.post("/interview/question")
async def get_question(role: str = Form(...)):
    question = generate_question(role)
    return {"question": question}

@app.post("/interview/evaluate")
async def evaluate(role: str = Form(...), question: str = Form(...), answer: str = Form(...)):
    feedback = evaluate_answer(role, question, answer)
    return {"feedback": feedback}

# ✅ NEW: Dedicated CV Roadmap endpoint — works without Ollama
@app.post("/cv-roadmap")
async def cv_roadmap(
    file: UploadFile = File(...),
    target_role: str = Form(...)
):
    temp_path = save_upload(await file.read(), file.filename)
    resume_text = extract_text_from_pdf(temp_path)

    resume_skills = smart_extract_skills(resume_text)
    job_skills    = smart_extract_skills(target_role.lower())
    result        = match_skills(resume_skills, job_skills)
    ats_result    = advanced_ats_score(resume_text, job_skills)
    breakdown     = ats_score_breakdown(resume_text, job_skills)
    semantic_score = semantic_match(resume_text, target_role)
    success_probability = predict_success(result["match_score"], semantic_score)
    roadmap       = generate_roadmap(result["missing_skills"], semantic_score,
                                     resume_text=resume_text, job_description=target_role)
    suggestions   = generate_suggestions(result["missing_skills"], target_role)
    feedback      = generate_feedback(result["match_score"], semantic_score)

    return {
        "resume_skills":      resume_skills,
        "job_skills":         job_skills,
        "matched_skills":     result["matched_skills"],
        "missing_skills":     result["missing_skills"],
        "match_score":        round(result["match_score"], 2),
        "semantic_score":     round(semantic_score, 2),
        "success_probability": success_probability,
        "roadmap":            roadmap,
        "suggestions":        suggestions,
        "feedback":           feedback,
        "ats_analysis":       ats_result,
        "score_breakdown":    breakdown
    }
from fastapi.responses import FileResponse
from backend.utils.pdf_generator import generate_pdf


@app.post("/download-resume")
async def download_resume(resume_text: str = Form(...)):
    file_path = generate_pdf(resume_text)
    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename="resume.pdf"
    )
