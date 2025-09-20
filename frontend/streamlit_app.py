import streamlit as st
import requests
import time
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(page_title="AI Career Recommender", layout="wide")
st.title("AI-Powered Career Recommendation System")

# -------------------
# Session State Setup
# -------------------
if "parsed" not in st.session_state:
    st.session_state.parsed = {}
if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "jobs_title" not in st.session_state:
    st.session_state.jobs_title = []
if "guidance" not in st.session_state:
    st.session_state.guidance = ""

# -------------------
# File Upload
# -------------------
uploaded_file = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])

def extract_text(file):
    text = ""
    if file.type == "application/pdf":
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

loading_steps = [
    "🔍 Scanning your profile...",
    "📑 Extracting experience and projects...",
    "🧠 Matching your skills to roles...",
    "🤖 Finding best-matching jobs...",
    "✅ Processing completed!"
]

# -------------------
# Step 1: Recommendations
# -------------------
if uploaded_file and st.button("Find Matching Jobs"):
    resume_text = extract_text(uploaded_file)

    status_placeholder = st.empty()
    for msg in loading_steps:
        status_placeholder.info(msg)
        time.sleep(1)

    with st.spinner("Generating results..."):
        response = requests.post("https://ai-career-recommender-three.vercel.app/recommend", json={"resume_text": resume_text})
        print("Response Status Code:", response.status_code)

        if response.status_code == 200:
            result = response.json()
            st.session_state.jobs = result.get("recommendations", [])
            st.session_state.parsed = result.get("parsed_resume", {})
            st.session_state.guidance = ""  # reset old guidance
            for job in st.session_state.jobs:
                st.session_state.jobs_title.append(job['title'])
        else:
            st.error("Failed to get recommendations.")


# -------------------
# Step 2: Display Extracted Info & Jobs
# -------------------
if st.session_state.jobs or st.session_state.parsed:
    left_col, spacer, right_col = st.columns([2.5, 1.5, 2.5])

    # Right column: Extracted Info
    with right_col:
        st.subheader("Extracted Info")
        parsed = st.session_state.parsed
        if parsed:
            if parsed.get("skills"):
                st.markdown("**Skills:**")
                st.write(", ".join(parsed.get("skills", [])))

            if parsed.get("experience"):
                st.markdown("**Experience:**")
                for exp in parsed.get("experience", []):
                    st.write("- " + exp)

            if parsed.get("projects"):
                st.markdown("**Projects:**")
                for proj in parsed.get("projects", []):
                    st.write("- " + proj)

    # Left column: Job Matches
    with left_col:
        if st.session_state.jobs:
            st.success("Top Job Matches:")
            for job in st.session_state.jobs:
                st.markdown(f"### {job['title']}")
                st.write(job['description'])
                st.write(f"**Match Score:** {job['score']}%")
                st.markdown("---")
        else:
            st.warning("No matching jobs found.")


# -------------------
# Step 3: Guidance
# -------------------

st.subheader("Get guidance for your target role")
user_input = st.text_input("Enter your target job role (e.g., Data Scientist, Web Developer):")
if st.button("Get Guidance"):
    with st.spinner("Generating career guidance..."):
        response = requests.post(
            "https://ai-career-recommender-three.vercel.app/guidance",
            json={
                "skills": st.session_state.parsed.get("skills", []),
                "recommended_jobs": st.session_state.jobs_title,
                "target_role": user_input,
            },
        )
        print("Response Status Code:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            st.session_state.guidance = data.get("guidance", "")
        else:
            st.error("Failed to get guidance.")


# -------------------
# Step 4: Display Guidance
# -------------------
if st.session_state.guidance:
    st.subheader("Career Guidance Plan")
    st.markdown(st.session_state.guidance,unsafe_allow_html=True)
