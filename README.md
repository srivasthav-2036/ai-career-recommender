# AI Career Recommendation System

This is a resume-based job recommendation system that uses natural language processing (NLP) and semantic similarity to suggest the most relevant job roles. Users can upload their resume in PDF or DOCX format, and the system will extract key details and match them with suitable job descriptions.

## Features

- Upload resume (PDF or DOCX)
- Extract skills, experience, and projects using NLP
- Compute semantic similarity between resume and job descriptions
- Return top job recommendations with relevance scores
- Simple Streamlit interface with real-time feedback

## Tech Stack

| Component     | Technology                        |
|---------------|-----------------------------------|
| Language      | Python                            |
| Frontend      | Streamlit                         |
| Backend       | Flask                             |
| NLP           | spaCy (`en_core_web_sm`)          |
| Embedding     | Sentence Transformers (`paraphrase-MiniLM-L3-v2`) |
| File Parsing  | PyPDF2, python-docx               |

## Installation

1. Clone the repository:

```bash
git clone https://github.com/srivasthav-2036/ai-career-recommender.git
cd ai-career-recommender
```

2. Install dependencies:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## How to Run

Run the backend (Flask) and frontend (Streamlit) in separate terminals.

Step 1: Run Flask Backend
```bash
cd backend
python app.py
```
This starts the Flask server at http://localhost:5000.

Step 2: Run Streamlit Frontend
Open a second terminal:
```bash
cd frontend
streamlit run streamlit_app.py
```
This opens the UI at http://localhost:8501.

## Project Structure

```
├── backend/
│   ├── app.py
│   ├── job_data.json
│   └── utils/
│       ├── resume_parsing.py
│       └── matching.py
│
├── frontend/
│   └── streamlit_app.py
│
├── requirements.txt
└── README.md
```

## License
This project is for educational/demo purposes.
