from config import call_llm, OFFLINE_MODE, BASE_DIR, retrieve_doc

def generate_interview_prep_packet(candidate_profile: dict, job_opportunity: dict) -> str:
    """Generates a complete interview preparation guide."""
    if OFFLINE_MODE:
        return f"""
# Interview Prep Packet for {job_opportunity['company_name']} - {job_opportunity['title']}

## 1. Company & Tech Stack Summary
- **Company**: {job_opportunity['company_name']}
- **Core Tech**: FastAPI, PostgreSQL, Docker, LLM routing

## 2. Likely System Design & Technical Questions
1. How would you design a rate-limiting middleware for a FastAPI backend?
2. Explain database indexing strategies in PostgreSQL for latency-critical query paths.
3. How do you manage model fallbacks and caching in a distributed LLM gateway?

## 3. Mapped STAR Stories
- **Story: Router Latency Optimization at ADEN**
  - **Situation**: ADEN's LLM prompt router had high latency during peak API traffic.
  - **Task**: Reduce dynamic dispatch overhead.
  - **Action**: Developed hashed caching key mapping based on token length and parameters in Python.
  - **Result**: Reduced average latency by 15%, merging PR #142 into the open-source codebase.
"""

    prompt_path = BASE_DIR / "prompts" / "interview.md"
    if not prompt_path.exists():
        return "Interview prep prompt template missing."
        
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_template = f.read()
        
    prompt = prompt_template.format(
        candidate_profile=json.dumps(candidate_profile, indent=2),
        job_context=json.dumps(job_opportunity, indent=2)
    )
    
    # Retrieve RAG context
    doc_context = retrieve_doc("11_interview_engine.md")
    if doc_context:
        prompt = f"System Rules and Guidelines:\n{doc_context}\n\nTask:\n{prompt}"
        
    return call_llm(prompt)

