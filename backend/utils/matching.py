from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
model = SentenceTransformer("all-MiniLM-L6-v2")

def rule_based_filter(user_skills, job_data):
    matched=set()
    for job in job_data:
        des= job["description"].lower()+" "+job["title"].lower()
        for skill in user_skills:
            skill = skill.lower()
            if skill in des:
                matched.add(job["id"])

    
    filtered_jobs = [job for job in job_data if job["id"] in matched]
    return filtered_jobs

def rank_jobs(resume_query, jobs, top_k=3):
    resume_embedding = model.encode([resume_query],normalize_embeddings=True)
    job_descriptions = [job["description"] for job in jobs]
    job_embeddings = model.encode(job_descriptions,normalize_embeddings=True)

    similarities = cosine_similarity(resume_embedding, job_embeddings)[0]

    top_matches = sorted(
        zip(jobs, similarities),
        key=lambda x: x[1],  # sort by similarity score
        reverse=True         # highest score first
    )
    print("Top Matches:", top_matches)  # Debugging line to check top matches
    
    return [
        {
            "title": job["title"],
            "score": round(float(score*100),2),
            "description": job["description"]
        }
        for job,score in top_matches[:top_k]
    ]


# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity

# model = SentenceTransformer("all-MiniLM-L6-v2")

# # rule_based_filter removed — not needed anymore

# def rank_jobs(resume_query, jobs, top_k=3):
#     resume_embedding = model.encode([resume_query], normalize_embeddings=True)
#     job_descriptions = [job["description"] for job in jobs]
#     job_embeddings = model.encode(job_descriptions, normalize_embeddings=True)

#     similarities = cosine_similarity(resume_embedding, job_embeddings)[0]

#     top_matches = sorted(
#         zip(jobs, similarities),
#         key=lambda x: x[1],
#         reverse=True
#     )[:top_k]

#     return [
#         {
#             "title": job["title"],
#             "score": round(float(score * 100), 2),
#             "description": job["description"]
#         }
#         for job, score in top_matches
#     ]
