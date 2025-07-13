# print("=== Starting Flask App... ===")  # Add this line as the first
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import json

# from utils.resume_parsing import extract_skills_experience
# from utils.matching import rule_based_filter, rank_jobs
# print("=== imports complete... ===")  # Add this line as the first

# app = Flask(__name__)
# CORS(app)  # Allow frontend (Streamlit) to talk to Flask backend

# # Load job data once
# with open("backend/job_data.json", "r") as f:
#     job_data = json.load(f)

# @app.route("/recommend", methods=["POST"])
# def recommend_jobs():
#     try:
#         data = request.get_json()
#         resume_text = data.get("resume_text", "")
#         print("\n[INFO] Resume Text Received:", resume_text[:100])  # print first 100 chars

#         # Parse resume
#         parsed_resume = extract_skills_experience(resume_text)
#         print("[INFO] Parsed Resume:", parsed_resume)

#         resume_query = (
#             f"Skills: {', '.join(parsed_resume['skills'])}. "
#             f"Projects: {', '.join(parsed_resume['projects'])}. "
#         )

#         if parsed_resume['experience']:
#             resume_query += f"Experience: {', '.join(parsed_resume['experience'])}."

#         print("[INFO] Resume Query for Ranking:", resume_query)

#         # Filter and rank jobs
#         filtered_jobs = rule_based_filter(parsed_resume["skills"], job_data)
#         print("[INFO] Filtered Jobs:", len(filtered_jobs))

#         top_jobs = rank_jobs(resume_query, filtered_jobs, top_k=3)
#         print("[INFO] Top Job Matches:", top_jobs)

#         return jsonify({"recommendations": top_jobs})
    
#     except Exception as e:
#         print("\n[ERROR] An exception occurred:", str(e))
#         return jsonify({"error": str(e)}), 500
# if __name__ == "__main__":
#     app.run(debug=True, port=5000)


from flask import Flask, request, jsonify
from flask_cors import CORS
import json

from utils.resume_parsing import extract_skills_experience
from utils.matching import rank_jobs,rule_based_filter

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
        print("\nResume Text Received:", resume_text[:100])

        parsed_resume = extract_skills_experience(resume_text)

        resume_query = (
            f"Skills: {', '.join(parsed_resume['skills'])}. "
            f"Projects: {', '.join(parsed_resume['projects'])}. "
        )

        if parsed_resume['experience']:
            resume_query += f"Experience: {', '.join(parsed_resume['experience'])}."


        filtered_jobs = rule_based_filter(parsed_resume["skills"], job_data)
        print("Filtered Jobs:", len(filtered_jobs))
        top_jobs = rank_jobs(resume_query, filtered_jobs, top_k=3)

        print("[INFO] Top Job Matches:", top_jobs)
        return jsonify({"recommendations": top_jobs,"parsed_resume": parsed_resume})

    except Exception as e:
        print("[ERROR] Exception occurred:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("=== Running Flask Server ===")
    app.run(debug=True, port=5000)
