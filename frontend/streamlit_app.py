import streamlit as st
import requests
import time
from PyPDF2 import PdfReader
from docx import Document

st.title("AI-Powered Career Recommendation System")

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

if uploaded_file:
    resume_text = extract_text(uploaded_file)
    col1, col2 = st.columns([2, 1]) 

    with col1:
        st.subheader("Extracted Resume Text")
        st.text_area("Text", resume_text, height=600)

    if st.button("Find Matching Jobs"):
        status_placeholder = st.empty()
        for msg in loading_steps:
            status_placeholder.info(msg)
            time.sleep(2)
        with st.spinner("Generating results..."):
            response = requests.post("https://ai-career-recommender-flask-api.onrender.com/recommend", json={"resume_text": resume_text})
            print("Response Status Code:", response.status_code)

            if response.status_code == 200:
                result = response.json()
                jobs = result.get("recommendations", [])
                parsed = result.get("parsed_resume", {})  
                with col2:
                    st.subheader("Extracted Info")
                    if parsed:
                        st.markdown("**Skills:**")
                        st.write(", ".join(parsed.get("skills", [])))

                        st.markdown("**Experience:**")
                        for exp in parsed.get("experience", []):
                            st.write("- "+exp)

                        st.markdown("**Projects:**")
                        for proj in parsed.get("projects", []):
                            st.write("- "+proj)

                if not jobs:
                    st.warning("No matching jobs found.")
                    st.stop()
                st.success("Top Job Matches:")
                for job in jobs:
                    st.markdown(f"### {job['title']}")
                    st.write(job['description'])
                    st.write(f"**Match Score:** {job['score']}%")
                    st.markdown("---")
            else:
                st.error("Failed to get recommendations.")
