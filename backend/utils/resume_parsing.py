from spacy.matcher import PhraseMatcher
import spacy

nlp = spacy.load("en_core_web_sm")
pm = PhraseMatcher(nlp.vocab)

def extract_skills_experience(resume_txt):
    # -------------------
    # Normalize headers (case-insensitive)
    # -------------------
    lines = resume_txt.splitlines()
    normalized_lines = []
    for line in lines:
        l = line.strip()
        if l.lower() == "skills":
            normalized_lines.append("Skills:")
        elif l.lower() == "experience":
            normalized_lines.append("Experience:")
        elif l.lower() == "education":
            normalized_lines.append("Education:")
        elif l.lower() == "projects":
            normalized_lines.append("Projects:")
        else:
            normalized_lines.append(line)
    
    # -------------------
    # Split into sections without regex
    # -------------------
    sections = {}
    current_section = None
    for line in normalized_lines:
        line_strip = line.strip()
        if line_strip.endswith(":") and line_strip[:-1].lower() in ["skills", "experience", "education", "projects"]:
            current_section = line_strip[:-1].lower()
            sections[current_section] = []
        elif current_section:
            sections[current_section].append(line_strip)
    
    for key in sections:
        sections[key] = "\n".join(sections[key])
    
    # -------------------
    # Extract skills from Skills section
    # -------------------
    skill_list = [
        "python", "java", "sql", "machine learning", "html", "css",
        "javascript", "node.js", "react", "c++", "c#", "ruby", "go",
        "typescript", "kotlin", "swift", "php", "rust", "dart", "deep learning",
        "tensorflow", "pytorch", "flask", "django", "aws", "dbms", "pandas", "matplotlib"
    ]
    skills = set()
    skills_text = sections.get("skills", "")
    doc = nlp(skills_text.lower())
    patterns = [nlp(skill) for skill in skill_list]
    pm.add("SKILLS", patterns)
    matches = pm(doc)
    for match_id, start, end in matches:
        skills.add(doc[start:end].text.lower())
    skills = list(skills)
    
    # -------------------
    # Extract experiences
    # -------------------
    experience_text = sections.get("experience", "")
    experience_doc = nlp(experience_text)
    experience_keywords = ["intern", "worked", "experience", "company", "role",
                           "participated", "collaborated", "contributed"]
    experiences = [sent.text.strip() for sent in experience_doc.sents
                   if any(kw in sent.text.lower() for kw in experience_keywords)]
    
    # -------------------
    # Extract projects
    # -------------------
    projects_text = sections.get("projects", "")
    project_keywords = ["project", "built", "developed"]
    projects = [line.strip() for line in projects_text.splitlines()
                if any(kw in line.lower() and not line.strip().isupper() for kw in project_keywords)]
    projects = list(set(projects))
    
    # -------------------
    # Extract education
    # -------------------
    education_text = sections.get("education", "")
    
    return {
        "skills": skills,
        "experience": experiences,
        "projects": projects,
        "education": education_text
    }
