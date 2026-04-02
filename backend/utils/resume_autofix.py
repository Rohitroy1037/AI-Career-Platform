from backend.utils.groq_client import call_groq


def auto_fix_resume(resume_text: str, job_description: str):

    try:
        prompt = f"""
You are a professional resume formatter. Generate a polished resume using EXACTLY the template structure and formatting rules below. Do NOT deviate from this structure.

=== EXACT TEMPLATE TO FOLLOW ===

[FULL NAME]
LinkedIn: [url]  Email: [email]
Github: [url]  Mobile: [phone]

SKILLS
 Languages: [comma-separated list]
 Frameworks/Concepts: [comma-separated list]
 Tools/Platforms: [comma-separated list]
 Soft Skills: [comma-separated list]

PROJECTS
[Project Title] — [Subtitle/Type] | Github [Month' YY] – [Month' YY]
• [Bullet point describing what was built/achieved, with technical detail and measurable impact]
• [Bullet point]
• [Bullet point]
 Tech: [Technology stack]

[Project Title 2] — [Subtitle] | Github [Month' YY] – [Month' YY]
• [Bullet point]
• [Bullet point]
 Tech: [Technology stack]

TRAINING
 [Training Title] | Certificate [Month' YY] – [Month' YY]
• [Bullet point]
• [Bullet point]
 Tech: [Technology stack]

CERTIFICATION / CERTIFICATES
• [Course Name] : [Provider] | Certificate Link | Certificate [Month' YY]
• [Course Name] | Certificate Link | Certificate [Month' YY]

ACHIEVEMENTS
• [Achievement with specific metrics or details]
• [Achievement]
• [Achievement]

EDUCATION
 [University Name] [City, State]
[Degree Name]-[Specialization]; [Month' YY] – Present
 [School Name] [City, State]
 [Level]; Percentage: [XX]% [Month' YY] – [Month' YY]

=== END TEMPLATE ===

STRICT RULES:
1. Follow the template EXACTLY — same section order, same symbols, same spacing style
2. Section headings must be UPPERCASE with no extra formatting
3. Skills lines start with a space then the category name (e.g., " Languages: ...")
4. Project title line format: "Name — Subtitle | Github Month' YY – Month' YY"
5. Training lines start with a space then title (e.g., " Title | Certificate Month' YY – Month' YY")
6. Tech lines start with a space then "Tech: ..." (e.g., " Tech: Python, ...")
7. Bullet points use • symbol
8. Tailor all content to match the job description provided
9. Keep bullet points detailed and action-oriented with measurable impact where possible
10. Return ONLY the resume text — no markdown, no backticks, no explanation

INPUT DATA:

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{job_description[:1500]}

Now generate the resume following the exact template:
"""

        response = call_groq(prompt, max_tokens=2000)

        # Clean AI markdown if exists
        response = response.replace("```", "").strip()

        return response

    except Exception as e:
        return f"Error: {e}"
