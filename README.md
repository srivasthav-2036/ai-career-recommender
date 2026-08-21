# 🤖 AI-Powered Career Recommendation System

> An intelligent resume-driven career guidance platform that extracts skills from uploaded resumes, matches them to job roles using semantic NLP, and generates personalized career roadmaps via Google Gemini AI.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-REST%20API-black?logo=flask)](https://flask.palletsprojects.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red?logo=streamlit)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-orange?logo=google)](https://ai.google.dev)
[![spaCy](https://img.shields.io/badge/spaCy-NLP-09A3D5?logo=spacy)](https://spacy.io)

---

## 📌 Overview

This project is an end-to-end AI application that helps users discover the most relevant tech career paths based on their resume content. It combines **rule-based NLP** for resume parsing, **semantic vector similarity** for job matching, and **Google Gemini LLM** for generating actionable career guidance plans — all served through a clean Streamlit UI backed by a Flask REST API.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **Resume Parsing** | Extracts skills, experience, and projects from PDF/DOCX resumes using spaCy NLP |
| 🔍 **Rule-Based Filtering** | Pre-filters jobs by skill keyword matching before semantic search |
| 🧠 **Semantic Job Matching** | Encodes resume and job descriptions as sentence embeddings; ranks by cosine similarity |
| 🤖 **AI Career Guidance** | Uses Google Gemini 2.5 Flash to generate personalized skill-gap analysis and learning roadmaps |
| 🎯 **Target Role Mode** | User can input a specific target role to get a focused career plan |
| 📊 **Match Score Display** | Returns top-3 job recommendations with percentage similarity scores |
| ⚡ **REST API Backend** | Flask REST endpoints (`/recommend`, `/guidance`) decoupled from the frontend |

---

## 🏗️ Architecture

```
┌─────────────────────┐         HTTP POST          ┌──────────────────────────────────┐
│   Streamlit Frontend │ ──────────────────────────▶ │        Flask REST API             │
│  (streamlit_app.py)  │                             │           (app.py)                │
│                      │ ◀────────────────────────── │                                   │
│  • Upload PDF/DOCX   │       JSON Response         │  ┌─────────────────────────────┐  │
│  • Display job cards │                             │  │   utils/resume_parsing.py   │  │
│  • Show guidance     │                             │  │   (spaCy PhraseMatcher NLP) │  │
└─────────────────────┘                             │  └─────────────────────────────┘  │
                                                    │  ┌─────────────────────────────┐  │
                                                    │  │     utils/matching.py       │  │
                                                    │  │   (Sentence Transformers +  │  │
                                                    │  │    Cosine Similarity)       │  │
                                                    │  └─────────────────────────────┘  │
                                                    │  ┌─────────────────────────────┐  │
                                                    │  │     utils/guidance.py       │  │
                                                    │  │   (Google Gemini 2.5 Flash) │  │
                                                    │  └─────────────────────────────┘  │
                                                    └──────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.10+ | Core programming language |
| **Frontend** | Streamlit | Interactive web UI with real-time session state |
| **Backend** | Flask + Flask-CORS | REST API server |
| **NLP / Parsing** | spaCy (`en_core_web_sm`) + PhraseMatcher | Resume section extraction & skill recognition |
| **Embeddings** | Sentence Transformers (`paraphrase-MiniLM-L3-v2`) | Semantic vector representations |
| **Similarity** | scikit-learn (`cosine_similarity`) | Job ranking by vector proximity |
| **Generative AI** | Google Gemini 2.5 Flash API | LLM-powered career guidance generation |
| **File Parsing** | PyPDF2, python-docx | Extracting text from PDF and DOCX resumes |
| **Config** | python-dotenv | Secure API key management |

---

## 📁 Project Structure

```
ai-career-recommender/
│
├── backend/
│   ├── app.py                  # Flask app with /recommend & /guidance endpoints
│   ├── job_data.json           # Curated job descriptions dataset (20 roles)
│   ├── requirements.txt        # Backend dependencies
│   ├── .env                    # Environment variables (GOOGLE_API_KEY)
│   └── utils/
│       ├── resume_parsing.py   # spaCy-based resume section & skill extractor
│       ├── matching.py         # Rule-based filter + Sentence Transformer ranker
│       └── guidance.py         # Gemini LLM prompt engineering & guidance generator
│
├── frontend/
│   ├── streamlit_app.py        # Streamlit UI — upload, results, guidance display
│   └── requirements.txt        # Frontend dependencies
│
├── CVs1/                       # Sample resumes for testing
├── test.py                     # Standalone test/debug script
├── .gitignore
└── README.md
```

---

## ⚙️ How It Works

### Step 1 — Resume Parsing (`utils/resume_parsing.py`)
- Reads the uploaded PDF/DOCX and splits it into sections: **Skills**, **Experience**, **Projects**, **Education**
- Uses **spaCy's PhraseMatcher** to identify known tech skills (Python, React, TensorFlow, etc.) from the Skills section
- Extracts experience sentences using keyword heuristics and project lines from the Projects section

### Step 2 — Job Matching (`utils/matching.py`)
- **Rule-based filter**: Scans all 20 job descriptions for any skill keyword overlap — pre-filters the search space
- **Semantic ranking**: Encodes the resume query and filtered job descriptions into dense vectors using `paraphrase-MiniLM-L3-v2`
- Computes **cosine similarity** and returns the top-3 matches with % scores

### Step 3 — AI Guidance (`utils/guidance.py`)
- Sends a structured prompt to **Google Gemini 2.5 Flash**
- **Exploratory mode**: Analyzes matched roles and suggests a general roadmap
- **Focused mode**: Takes a user-specified target role and generates a personalized skill-gap analysis + learning plan in Markdown

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A [Google AI Studio](https://aistudio.google.com) API key for Gemini

### 1. Clone the Repository

```bash
git clone https://github.com/srivasthav-2036/ai-career-recommender.git
cd ai-career-recommender
```

### 2. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Install Frontend Dependencies

```bash
cd ../frontend
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file inside the `backend/` directory:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

### 5. Run the Application

**Terminal 1 — Start the Flask backend:**
```bash
cd backend
python app.py
# Flask server running at http://localhost:5000
```

**Terminal 2 — Start the Streamlit frontend:**
```bash
cd frontend
streamlit run streamlit_app.py
# UI available at http://localhost:8501
```

---

## 🔌 API Reference

### `POST /recommend`
Accepts raw resume text and returns top job matches with parsed resume data.

**Request:**
```json
{
  "resume_text": "Skills: Python, Machine Learning, Flask..."
}
```

**Response:**
```json
{
  "recommendations": [
    { "title": "Machine Learning Engineer", "score": 87.34, "description": "..." }
  ],
  "parsed_resume": {
    "skills": ["python", "machine learning"],
    "experience": ["Worked as intern at XYZ..."],
    "projects": ["Built a recommendation system..."],
    "education": "B.Tech in Computer Science..."
  }
}
```

---

### `POST /guidance`
Generates a personalized AI career guidance plan using Gemini.

**Request:**
```json
{
  "skills": ["python", "flask", "sql"],
  "recommended_jobs": ["Backend Developer", "Software Engineer"],
  "target_role": "Data Scientist"
}
```

**Response:**
```json
{
  "status": "success",
  "guidance": "### 1. Skill Gap Analysis\n..."
}
```

---

## 🧪 Sample Job Roles in Dataset

The system matches against 20 curated tech roles including:

`Machine Learning Engineer` · `Backend Developer` · `Frontend Developer` · `Data Scientist` · `AI Engineer` · `Full Stack Developer` · `Cloud Engineer` · `DevOps Engineer` · `Data Analyst` · `AI Research Intern` · `Software Engineer` · `Cybersecurity Analyst` · `Mobile App Developer` · `UI/UX Designer` · `Product Manager` · `QA Engineer` · `Systems Engineer` · `Business Analyst` · `Cloud Architect` · `Research Intern`

---

## 🔮 Future Improvements

- [ ] Add support for LinkedIn profile URL parsing
- [ ] Integrate a larger job dataset via job board APIs (LinkedIn, Indeed)
- [ ] Replace static `job_data.json` with a vector database (e.g., Pinecone, ChromaDB) for scalable retrieval
- [ ] Add user authentication and resume history tracking
- [ ] Deploy backend on AWS/GCP with Streamlit Cloud frontend
- [ ] Fine-tune embedding model on domain-specific job description data

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

> Built with ❤️ using Flask · Streamlit · spaCy · Sentence Transformers · Google Gemini
