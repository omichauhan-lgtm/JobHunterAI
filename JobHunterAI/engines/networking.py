from config import call_llm, OFFLINE_MODE, BASE_DIR, retrieve_doc

def generate_outreach_sequence(job_opportunity: dict, company_profile: dict) -> dict:
    """Drafts LinkedIn connection request and follow-up sequence."""
    if OFFLINE_MODE:
        return {
            "linkedin_note": f"Hi, saw Stripe is building core payments infra. I've built backend gateways using FastAPI & Docker with 45ms latency, and contributed to YC-backed ADEN's LLM router (15% speedup). Would love to connect regarding the {job_opportunity['title']} role!",
            "follow_up_message": f"Hi,\n\nFollowing up on my application for the {job_opportunity['title']} role. My background in high-performance Python gateways matches your stack ({', '.join(company_profile.tech_stack[:3])}). You can view my code here: github.com/omichauhan/omi-gateway\n\nThanks,\nOmi"
        }
        
    prompt_path = BASE_DIR / "prompts" / "networking.md"
    if not prompt_path.exists():
        return {"linkedin_note": "Prompt template missing.", "follow_up_message": ""}
        
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_template = f.read()
        
    prompt = prompt_template.format(
        job_context=json.dumps({
            "job_title": job_opportunity["title"],
            "company_name": job_opportunity["company_name"],
            "tech_stack": company_profile.tech_stack,
            "recent_news": company_profile.recent_news
        }, indent=2)
    )
    
    # Retrieve RAG context
    doc_context = retrieve_doc("10_networking.md")
    if doc_context:
        prompt = f"System Rules and Guidelines:\n{doc_context}\n\nTask:\n{prompt}"
        
    response = call_llm(prompt)

    
    # Try to parse response sections
    linkedin_note = "Hi, saw your team is hiring. Let's connect!"
    follow_up = "Following up on my application..."
    
    try:
        # Simple extraction using headers
        sections = response.split("2.")
        if len(sections) >= 2:
            linkedin_note = sections[0].replace("1.", "").strip()
            follow_up = sections[1].strip()
        else:
            # Fallback to splitting lines
            linkedin_note = response[:300]
            follow_up = response[300:]
    except:
        pass
        
    return {
        "linkedin_note": linkedin_note,
        "follow_up_message": follow_up
    }
