\# 🚀 AI Career Platform



An AI-powered career guidance platform built using FastAPI and AI APIs that helps users improve resumes, analyze skills, prepare for interviews, and receive personalized career guidance.



\---



\## 📌 Features



\### 📄 Resume Analysis

\- Upload resume in PDF format

\- Extract resume information automatically

\- Analyze resume content

\- Improve resume quality using AI suggestions



\### 📊 ATS Score Checker

\- Calculates ATS (Applicant Tracking System) score

\- Identifies missing keywords

\- Suggests improvements to increase resume visibility



\### 🤖 AI Career Chatbot

\- Personalized AI career assistant

\- Maintains conversation memory

\- Gives career guidance

\- Answers technical and educational questions

\- Resume-aware responses



\### 🎯 Smart Skill Suggestions

\- Detects current skills from resume

\- Recommends missing skills

\- Suggests industry-relevant technologies



\### 🛣 Career Roadmap Generator

\- Generates personalized learning roadmap

\- Step-by-step career guidance

\- Helps users reach career goals



\### 💼 Resume Auto Fix

\- Detects weak sections

\- Improves content automatically

\- Suggests stronger wording



\### 🎤 AI Mock Interview

\- Generates interview questions

\- Simulates interview preparation



\### 📈 Success Prediction

\- Predicts career readiness

\- Uses skill matching and resume analysis



\---



\## 🛠 Tech Stack



\### Backend

\- FastAPI

\- Python

\- REST APIs



\### AI Integration

\- Groq API

\- Llama Models



\### Data Processing

\- Pandas

\- Scikit-learn

\- NumPy



\### Database

\- SQLite



\### Tools

\- Git

\- GitHub

\- Vercel



\---



\## 📂 Project Structure



```bash

AI-Career-Platform

│

├── backend/

│   ├── main.py

│   ├── utils/

│   │   ├── ai\_chatbot.py

│   │   ├── ats\_score.py

│   │   ├── groq\_client.py

│   │   ├── matcher.py

│   │   ├── roadmap.py

│   │   ├── parser.py

│   │   ├── smart\_skills.py

│   │   └── ...

│

├── frontend/

│   └── index.html

│

├── data/

│   └── skills.json

│

├── requirements.txt

├── run.py

└── README.md

```



\---



\## ⚙️ Installation



Clone repository:



```bash

git clone https://github.com/Rohitroy1037/AI-Career-Platform.git

```



Move into project:



```bash

cd AI-Career-Platform

```



Create virtual environment:



```bash

python -m venv venv

```



Activate virtual environment:



Windows:



```bash

venv\\Scripts\\activate

```



Linux/Mac:



```bash

source venv/bin/activate

```



Install dependencies:



```bash

pip install -r requirements.txt

```



\---



\## 🔑 Environment Variables



Create a `.env` file:



```env

GROQ\_API\_KEY=your\_api\_key\_here

```



\---



\## ▶️ Run Project



Start FastAPI server:



```bash

python run.py

```



or:



```bash

uvicorn backend.main:app --reload

```



\---



\## API Documentation



Open:



```bash

http://127.0.0.1:8000/docs

```



FastAPI automatically generates Swagger UI.



\---



\## 📷 Screenshots



Add screenshots here:



\- Home page

\- Resume upload page

\- AI chatbot

\- ATS score results

\- Roadmap generation



\---



\## Future Improvements



\- User authentication

\- JWT security

\- Real-time chat

\- Job recommendation engine

\- LinkedIn profile analysis

\- AI voice interviews

\- Email notifications



\---



\## Why This Project?



This project was built to solve real-world career problems by combining Artificial Intelligence with resume analysis and career guidance tools. It helps users understand their strengths, improve skills, and prepare for better job opportunities.



\---



\## 👨‍💻 Author



Rohit Roy



GitHub:

https://github.com/Rohitroy1037



LinkedIn:

(Add LinkedIn profile)



\---



⭐ If you like this project, give it a star.

