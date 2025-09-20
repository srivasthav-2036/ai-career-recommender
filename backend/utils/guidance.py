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
