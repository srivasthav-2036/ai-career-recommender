from flask import Flask, request, jsonify
from flask_cors import CORS
import json

from utils.resume_parsing import extract_skills_experience
from utils.matching import rank_jobs,rule_based_filter
from utils.guidance import generate_guidance


app = Flask(__name__)
CORS(app)  # Allow frontend (Streamlit) to talk to Flask backend

# Load job data once
with open("backend/job_data.json", "r") as f:
    job_data = json.load(f)

@app.route("/recommend", methods=["POST"])
def recommend_jobs():
    try:
        data = request.get_json()
        resume_text = data.get("resume_text", "")


        parsed_resume = extract_skills_experience(resume_text)

        resume_query = (
            f"Skills: {', '.join(parsed_resume['skills'])}. "
            f"Projects: {', '.join(parsed_resume['projects'])}. "
        )

        if parsed_resume.get('experience',[]):
            resume_query += f"Experience: {', '.join(parsed_resume['experience'])}."


        filtered_jobs = rule_based_filter(parsed_resume["skills"], job_data)

        top_jobs = rank_jobs(resume_query, filtered_jobs, top_k=3)

 
        return jsonify({"recommendations": top_jobs,"parsed_resume": parsed_resume})

    except Exception as e:
        print("[ERROR] Exception occurred:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/guidance", methods=["POST"])
def guidance():
    try:
        data = request.get_json()
        user_skills = data.get("skills", [])
        recommended_jobs = data.get("recommended_jobs", [])
        target_role = data.get("target_role", "")
        print("target role",target_role)
        print("skills",user_skills)
        print("recjobs",recommended_jobs)
        print("[DEBUG] Calling generate_guidance()", flush=True)
        guidance_text = generate_guidance(user_skills, recommended_jobs, target_role)

        # ✅ Print in console for debugging
        print("\n=== GUIDANCE OUTPUT ===\n", guidance_text, flush=True)

        # ✅ Return the guidance to Streamlit so it can be displayed
        return jsonify({
            "status": "success",
            "guidance": guidance_text
        })

    except Exception as e:
        print("[ERROR] Exception occurred:", e, flush=True)
        return jsonify({"error": str(e)}), 500
 


if __name__ == "__main__":
    print("=== Running Flask Server ===")
    app.run(debug=True, port=5000)
