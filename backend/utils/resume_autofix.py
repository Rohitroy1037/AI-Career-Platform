from backend.utils.groq_client import call_groq


def auto_fix_resume(resume_text: str, job_description: str):

    try:
        prompt = f"""
Generate a professional resume EXACTLY like this structure:

NAME (center aligned)
LinkedIn | Email | Github | Phone

SECTION HEADINGS in UPPERCASE

SKILLS
Languages: ...
Frameworks/Concepts: ...
Tools/Platforms: ...
Soft Skills: ...

PROJECTS
Project Name | Github Month Year – Month Year
• Bullet point
• Bullet point
Tech: ...

TRAINING
...

CERTIFICATIONS
...

ACHIEVEMENTS
...

EDUCATION
...

INPUT:

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{job_description[:1500]}

RULES:
- Use exact format
- Keep headings uppercase
- Use bullet points (•)
- Keep clean spacing
- Tailor to job description
- No JSON

Return only resume text.
"""

        response = call_groq(prompt, max_tokens=1800)

        # ✅ Clean AI markdown if exists
        response = response.replace("```", "").strip()

        return response

    except Exception as e:
        return f"Error: {e}"