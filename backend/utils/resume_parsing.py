
import spacy
from spacy.matcher import PhraseMatcher
nlp = spacy.load("en_core_web_sm")
def extract_skills_experience(resume_txt):
    # extracting skills

    skill_list= [
        "python", "java", "sql", "machine learning", "html", "css",
        "javascript", "node.js", "react", "c++", "c#", "ruby", "go",
        "typescript", "kotlin", "swift", "php", "rust", "dart","deeplearning",
        "tensorflow", "pytorch", "flask", "django", "aws","dbms","pandas","matplotlib"]
    skills=set()
    doc=nlp(resume_txt.lower())
    pm=PhraseMatcher(nlp.vocab)
    patterns=[nlp(skill) for skill in skill_list]
    pm.add("SKILLS", patterns)

    matches=pm(doc)
    for match_id, start, end in matches:
        skills.add(doc[start:end].text.lower())
    skills = list(skills)

    
    # extracting expereinces

    experience_keywords = ["intern", "worked", "experience", "company", "role","participated", "collaborated", "contributed"]
    experiences = []
    for sent in doc.sents:
        if any(kw in sent.text.lower() for kw in experience_keywords):
            experiences.append(sent.text.strip())


    # extracting projects
    project_keywords = ["project", "built", "developed"]
    projects = [line.strip() for line in resume_txt.splitlines() if any(kw in line.lower() and not line.strip().isupper() and len(line.strip()) > 10   for kw in project_keywords )]
    projects = list(set(projects))

    return {
        "skills": skills,
        "experience": experiences,
        "projects": projects
    }