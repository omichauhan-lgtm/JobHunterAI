import json
from models.schemas import CompanyProfile
from config import call_llm, OFFLINE_MODE, BASE_DIR, retrieve_doc, logger

def run_company_intelligence(company_name: str, jd_text: str) -> CompanyProfile:
    """Generate or retrieve intelligence on the company."""
    if OFFLINE_MODE:
        name_lower = company_name.lower()
        if "stripe" in name_lower:
            return CompanyProfile(
                name="Stripe",
                funding_stage="Late Stage (Series I)",
                funding_amount="$9B+",
                investors=["Sequoia Capital", "Andreessen Horowitz", "Peter Thiel"],
                is_yc=True,
                tech_stack=["Ruby", "Python", "Go", "PostgreSQL", "React"],
                recent_news="Expanding support for crypto pay-ins and global checkout optimization.",
                products=["Stripe Payments", "Stripe Billing", "Stripe Radar"]
            )
        elif "aden" in name_lower:
            return CompanyProfile(
                name="ADEN",
                funding_stage="Early Stage (Seed)",
                funding_amount="$2M",
                investors=["Y Combinator", "General Catalyst"],
                is_yc=True,
                tech_stack=["Python", "FastAPI", "React", "Docker"],
                recent_news="Launched open-source LLM prompt routing gateway.",
                products=["ADEN Router", "ADEN Agent Hub"]
            )
        elif "vectorshift" in name_lower:
            return CompanyProfile(
                name="VectorShift",
                funding_stage="Early Stage (Seed)",
                funding_amount="$3M",
                investors=["Y Combinator", "Sequoia Capital"],
                is_yc=True,
                tech_stack=["Python", "FastAPI", "React", "Docker", "PostgreSQL", "LLM Routing"],
                recent_news="Launched automated LLM pipeline and vector search orchestrator.",
                products=["VectorShift Platform", "Agent Studio"]
            )
        else:

            return CompanyProfile(
                name=company_name,
                funding_stage="Private / Early Stage",
                investors=["Various Venture Funds"],
                is_yc=False,
                tech_stack=["Python", "FastAPI", "PostgreSQL"],
                recent_news="Expanding engineering team to accelerate product delivery.",
                products=["Core Platform SaaS"]
            )
            
    # Online mode: Call LLM with dynamic documentation context (RAG) and Prompt Registry
    prompt_path = BASE_DIR / "prompts" / "company_intelligence.md"
    if prompt_path.exists():
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_template = f.read()
    else:
        prompt_template = "Analyze the company '{company_name}' based on the Job Description:\n{jd_text}"
        
    prompt = prompt_template.format(company_name=company_name, jd_text=jd_text)
    
    # Retrieve RAG context
    doc_context = retrieve_doc("09_company_intelligence.md")
    if doc_context:
        prompt = f"System Rules and Guidelines:\n{doc_context}\n\nTask:\n{prompt}"
        
    try:
        response_text = call_llm(prompt, response_schema=CompanyProfile)
        profile = CompanyProfile.model_validate_json(response_text)
        return profile
    except Exception as e:
        logger.error(f"Error validating company profile: {e}")
        return CompanyProfile(
            name=company_name,
            funding_stage="Unknown",
            investors=[],
            is_yc=False,
            tech_stack=["Python"],
            recent_news="Scraping profile generation failed. Standard tech startup.",
            products=[]
        )

