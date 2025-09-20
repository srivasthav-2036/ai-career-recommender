# import google.generativeai as genai

# genai.configure(api_key="AIzaSyD3S-I13cK5Vfnx8ljd87vy_kwa3wlX58M")
# model = genai.GenerativeModel("gemini-2.5-flash")  

# # response = model.generate_content("ill send you the skills and target job. give him a guide")

# def generate_guidance(user_skills, recommended_jobs, target_role):
#     user_skills=",".join(user_skills)
#     target_job = target_role.strip()
#     recommended_jobs = recommended_jobs

#     if target_job:
#         # Focused Mode
#         prompt = f"""
#         You are an expert career advisor. 

#         The candidate has the following skills: {user_skills}  
#         The target job role is: {target_job}.  

#         Create a **personalized career guidance plan** in Markdown format with these sections:

#         ### 1. Skill Gap Analysis  
#         - Compare the given skills with the target role requirements.  
#         - Highlight missing or weak areas.  

#         ### 2. Must-Learn Skills & Tools  
#         - List key technologies, frameworks, or concepts to focus on.  

#         ### 3. Learning Roadmap  
#         - Suggest a step-by-step path (courses, projects, certifications).  
#         - Provide approximate learning order.  

#         ### 4. Alternative Relevant Roles  
#         - Suggest related job titles where the current skills are valuable.  

#         ### 5. Actionable Next Steps  
#         - Give 3–5 clear, motivating steps to help the user move toward their target role.  

#         Keep the tone encouraging, concise, and practical.
#         """
#     else:
#         # Exploratory Mode (fallback to recommended jobs)
#         prompt = f"""
#         You are an expert career advisor. 

#         The candidate has the following skills: {", ".join(skills)}  
#         Based on resume analysis, the recommended job matches are: {", ".join(recommended_jobs)}.  

#         Provide a **career guidance plan** in Markdown format including:

#         ### 1. Best-Fit Role Analysis  
#         - Evaluate which recommended roles fit best and why.  

#         ### 2. Skill Gap for Top Roles  
#         - Highlight missing skills for the top 1–2 roles.  

#         ### 3. Learning Roadmap  
#         - Suggest a step-by-step path to move closer to those roles.  

#         ### 4. Alternative Career Paths  
#         - Mention any other roles worth considering.  

#         ### 5. Actionable Next Steps  
#         - Give 3–5 practical steps the candidate can start with right away.  

#         Keep the advice clear, structured, and motivating.
#         """
#     response = model.generate_content(prompt)
#     print("\n=== GUIDANCE OUTPUT ===\n")
#     print(response.text)

import google.generativeai as genai

genai.configure(api_key="AIzaSyD3S-I13cK5Vfnx8ljd87vy_kwa3wlX58M")
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_guidance(user_skills, recommended_jobs, target_role):
    user_skills_str = ", ".join(user_skills) if user_skills else "None"
    target_job = target_role.strip()
    recommended_jobs_str = ", ".join(recommended_jobs) if recommended_jobs else "None"

    if target_job:
        # Focused Mode
        prompt = f"""
        You are an expert career advisor. 

        The candidate has the following skills: {user_skills_str}  
        The target job role is: {target_job}.  

        Create a **personalized career guidance plan** in Markdown format with these sections:

        ### 1. Skill Gap Analysis  
        ### 2. Must-Learn Skills & Tools  
        ### 3. Learning Roadmap  
        ### 4. Alternative Relevant Roles  
        ### 5. Actionable Next Steps  
        Keep the response short simple and concise and effective
        """
    else:
        # Exploratory Mode
        prompt = f"""
        You are an expert career advisor. 

        The candidate has the following skills: {user_skills_str}  
        Based on resume analysis, the recommended job matches are: {recommended_jobs_str}.  

        Provide a **career guidance plan** in Markdown format including:

        ### 1. Best-Fit Role Analysis  
        ### 2. Skill Gap for Top Roles  
        ### 3. Learning Roadmap  
        ### 4. Alternative Career Paths  
        ### 5. Actionable Next Steps  
        keep the response short simple and concise and effective
        """

    response = model.generate_content(prompt)
    print("\n=== GUIDANCE OUTPUT ===\n", flush=True)
    print(response.text, flush=True)  # flush=True ensures immediate print
    return response.text  # return text if you also want Streamlit to show it
