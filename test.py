import requests
import time
from PyPDF2 import PdfReader
from docx import Document
import os,json
from PyPDF2 import PdfReader
accuracy=[]
precision=[]
ground_truth_jobs={
    1:["Data Scientist", "Machine Learning Engineer", "Cloud Engineer", "Software Engineer", "Full Stack Developer"],
    2:["Machine Learning Engineer", "AI Researcher", "Data Scientist", "Software Engineer", "Cloud Engineer"],
    3:["AI Researcher", "Machine Learning Engineer", "Data Scientist", "Software Engineer", "Cybersecurity Analyst"],
    4:["Product Manager", "Machine Learning Engineer", "Software Engineer", "Cloud Engineer", "Full Stack Developer"],
    5:["Data Scientist", "Machine Learning Engineer", "Cybersecurity Analyst", "Cloud Engineer", "Software Engineer"],
    6:["Data Scientist", "Machine Learning Engineer", "Product Manager", "Cloud Engineer", "AI Researcher"],
    7:["Machine Learning Engineer", "Data Scientist", "Software Engineer", "Full Stack Developer", "AI Researcher"],
    8:["AI Researcher", "Machine Learning Engineer", "Software Engineer", "Product Manager", "Cybersecurity Analyst"],
    9:["Product Manager", "Cloud Engineer", "Software Engineer", "Full Stack Developer", "Cybersecurity Analyst"],
    10:["Data Scientist", "Machine Learning Engineer", "Cloud Engineer", "Software Engineer", "Cybersecurity Analyst"],
    11:["Machine Learning Engineer", "Data Scientist", "AI Researcher", "Cloud Engineer", "Software Engineer"],
    12:["Data Scientist", "Machine Learning Engineer", "Cloud Engineer", "Cybersecurity Analyst", "Software Engineer"],
    13:["Machine Learning Engineer", "Data Scientist", "Software Engineer", "Product Manager", "Cybersecurity Analyst"],
    14:["Data Scientist", "Machine Learning Engineer", "Cloud Engineer", "AI Researcher", "Software Engineer"],
    15:["Data Scientist", "Machine Learning Engineer", "Product Manager", "Cloud Engineer", "Full Stack Developer"],
    16:["Machine Learning Engineer", "Data Scientist", "AI Researcher", "Cloud Engineer", "Software Engineer"],
    17:["Product Manager", "Cloud Engineer", "Software Engineer", "Full Stack Developer", "Cybersecurity Analyst"],
    18:["Machine Learning Engineer", "Product Manager", "Software Engineer", "Full Stack Developer", "AI Researcher"],
    19:["Product Manager", "Cloud Engineer", "Machine Learning Engineer", "AI Researcher", "Software Engineer"],
    20:["Cybersecurity Analyst", "Cloud Engineer", "Software Engineer", "Full Stack Developer", "DevOps Engineer"],
    21:["Machine Learning Engineer", "Data Scientist", "AI Researcher", "Cloud Engineer", "Full Stack Developer"],
    22:["Machine Learning Engineer", "Data Scientist", "AI Researcher", "Software Engineer", "Product Manager"],
    23:["Data Scientist", "Machine Learning Engineer", "Software Engineer", "Cybersecurity Analyst", "Cloud Engineer"],
    24:["Product Manager", "Cloud Engineer", "Data Scientist", "Machine Learning Engineer", "Software Engineer"],
    25:["AI Researcher", "Machine Learning Engineer", "Cybersecurity Analyst", "Cloud Engineer", "Software Engineer"],
    26:["Machine Learning Engineer", "Software Engineer", "Cybersecurity Analyst", "Cloud Engineer", "Data Scientist"],
    27:["AI Researcher", "Machine Learning Engineer", "Product Manager", "Software Engineer", "Cybersecurity Analyst"],
    28:["Data Scientist", "Machine Learning Engineer", "Cybersecurity Analyst", "Cloud Engineer", "Software Engineer"],
    29:["Data Scientist", "Machine Learning Engineer", "Cloud Engineer", "AI Researcher", "Cybersecurity Analyst"],
    30:["Data Scientist", "Machine Learning Engineer", "Software Engineer", "Full Stack Developer", "Cloud Engineer"],
    31:["Data Scientist", "Machine Learning Engineer", "Cloud Engineer", "Cybersecurity Analyst", "Software Engineer"],
    32:["Data Scientist", "Machine Learning Engineer", "Software Engineer", "Full Stack Developer", "Cloud Engineer"],
    33:["AI Researcher", "Machine Learning Engineer", "Software Engineer", "Data Scientist", "Product Manager"],
    34:["AI Researcher", "Machine Learning Engineer", "Cybersecurity Analyst", "Cloud Engineer", "Software Engineer"],
    35:["Machine Learning Engineer", "Data Scientist", "Product Manager", "Software Engineer", "Cybersecurity Analyst"]
    }

with open("backend/job_data.json", "r") as f:
    job_data = json.load(f)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

for i in range(1,36):
    file=f"resume{i}.pdf"
    file_path = os.path.join(BASE_DIR, "CVs1", file)
    print(file_path,i)
    reader = PdfReader(file_path)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text() or ""
    response = requests.post("http://127.0.0.1:5000/recommend", json={"resume_text": resume_text})


    print("Response Status Code:", response.status_code)
    if response.status_code == 200:
        result = response.json()
        hit = 0
        relevant_c=0
        recom_jobs = result.get("recommendations", [])
        for job in recom_jobs:
            if job["title"] in ground_truth_jobs[i]:
                print("Matched with ground truth:", job["title"],job['score'])
                hit=1
                relevant_c+=1
                
        accuracy.append(hit)
        precision.append(relevant_c/len(recom_jobs) if len(recom_jobs)>0 else 0)

    else:
        print("Failed to get recommendations.")
print(len(accuracy),accuracy,len(precision),precision)
print("Top-3 Accuracy:", (sum(accuracy)/len(accuracy))*100, "%")
print("Avg Precision for top 3:", (sum(precision)/len(precision))*100, "%")    