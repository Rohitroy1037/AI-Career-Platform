import json

def load_skills():
    with open("data/skills.json", "r") as f:
        return json.load(f)["skills"]

def extract_skills(text):
    skills = load_skills()
    found = []

    for skill in skills:
        if skill in text:
            found.append(skill)

    return list(set(found))