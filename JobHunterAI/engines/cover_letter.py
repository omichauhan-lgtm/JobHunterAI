from config import call_llm, OFFLINE_MODE, BASE_DIR, retrieve_doc

def generate_tailored_cover_letter(candidate_profile: dict, job_opportunity: dict, company_profile: dict) -> str:
    """Generates an engineering-focused, company-aware cover letter."""
    if OFFLINE_MODE:
        return f"""
# Cover Letter for {job_opportunity['company_name']}

Dear Hiring Team at {job_opportunity['company_name']},

I am writing to you regarding the {job_opportunity['title']} opening. Based on my experience with {', '.join(company_profile.tech_stack)}, I believe there is an immediate overlap in technical capabilities.

Specifically, in my work on the OMI Gateway, I developed an intelligent routing system using FastAPI and Docker, optimizing system latency to a 45ms ceiling. Additionally, as an Open Source Contributor to the YC-backed startup ADEN, I engineered caching subsystems resulting in a 15% latency drop.

I am eager to apply these systems design capabilities to the engineering problems you are solving.

Best regards,
{candidate_profile['name']}
"""

    # Online mode: load cover letter prompt template
    prompt_path = BASE_DIR / "prompts" / "cover_letter.md"
    if not prompt_path.exists():
        return f"Cover letter generation failed. Prompt template missing."
        
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_template = f.read()
        
    prompt = prompt_template.format(
        candidate_profile=json.dumps(candidate_profile, indent=2),
        job_context=json.dumps({
            "job_title": job_opportunity["title"],
            "company_name": job_opportunity["company_name"],
            "tech_stack": company_profile.tech_stack,
            "recent_news": company_profile.recent_news,
            "products": company_profile.products
        }, indent=2)
    )
    
    # Retrieve RAG context
    doc_context = retrieve_doc("10_networking.md")
    if doc_context:
        prompt = f"System Rules and Guidelines:\n{doc_context}\n\nTask:\n{prompt}"
        
    cover_letter_body = call_llm(prompt)

    
    # Strip markdown headers if the LLM outputted them
    if cover_letter_body.strip().startswith("#"):
        # Just return body as is
        return cover_letter_body
        
    return cover_letter_body
