import json
from storage.db import SessionLocal, JobOpportunityTable, ApplicationTable
from orchestrator import run_daily_autonomous_loop

def ingest_research_opportunities():
    db = SessionLocal()
    try:
        # Define high-value target jobs discovered by the Deep Research session
        target_jobs = [
            {
                "company": "LiteLLM",
                "title": "Founding AI Platform Engineer",
                "jd": """
                We are hiring a Founding AI Platform Engineer to build high-performance LLM gateway scaling features.
                You will work on Python, FastAPI, Redis caching, and telemetry metrics.
                Experience with API keys, Docker multi-container setups, and unittest validation.
                Location: Remote (Global)
                """,
                "url": "https://www.workatastartup.com/companies/litellm/jobs",
                "source": "YC Startup Jobs",
                "remote": "Remote",
                "salary": "$120,000 - $160,000",
                "stack": ["Python", "FastAPI", "Docker", "Redis", "LLM Routing"]
            },
            {
                "company": "Supabase",
                "title": "Backend Systems Engineer (Python/FastAPI)",
                "jd": """
                We are seeking a Backend Systems Engineer to build secure data routers and caching middleware.
                Required: Strong knowledge of Python, FastAPI, Docker, and PostgreSQL.
                Experience with performance profiling, API routing, and DB connection pooling is highly preferred.
                Location: Remote (Global)
                """,
                "url": "https://boards.greenhouse.io/supabase/backend-engineer",
                "source": "Greenhouse",
                "remote": "Remote",
                "salary": "$130,000 - $170,000",
                "stack": ["Python", "FastAPI", "Docker", "PostgreSQL", "SQL"]
            },
            {
                "company": "LangChain",
                "title": "AI Integration Engineer",
                "jd": """
                We are hiring an AI Integration Engineer to work on core LLM routing, prompt evaluation, and agent frameworks.
                Key Skills: Python, FastAPI, Docker, agentic workflows, LLM routing, and evaluation.
                Familiarity with SQLite and SQL is preferred.
                Location: Remote
                """,
                "url": "https://boards.lever.co/langchain/ai-engineer",
                "source": "Lever",
                "remote": "Remote",
                "salary": "$140,000 - $180,000",
                "stack": ["Python", "FastAPI", "Docker", "LLM Routing", "SQL"]
            },
            {
                "company": "Docker",
                "title": "Backend Software Engineer",
                "jd": """
                We are looking for a Software Engineer to work on container orchestration, staging environments, and CLI tools.
                Requirements: Python, C++, Docker, Unix, and CI/CD pipelines.
                Location: Remote
                """,
                "url": "https://boards.greenhouse.io/docker/software-engineer",
                "source": "Greenhouse",
                "remote": "Remote",
                "salary": "$110,000 - $150,000",
                "stack": ["Python", "Docker", "C++"]
            }
        ]

        print("1. Ingesting Deep Research target opportunities into database...")
        for job_data in target_jobs:
            # Delete old entries to prevent unique constraints errors
            existing = db.query(JobOpportunityTable).filter(
                JobOpportunityTable.company_name == job_data["company"],
                JobOpportunityTable.title == job_data["title"]
            ).first()
            if existing:
                db.delete(existing)
                db.commit()

            job = JobOpportunityTable(
                company_name=job_data["company"],
                title=job_data["title"],
                jd_text=job_data["jd"],
                url=job_data["url"],
                source=job_data["source"],
                remote_status=job_data["remote"],
                salary_range=job_data["salary"],
                tech_stack_json=json.dumps(job_data["stack"]),
                status="discovered"
            )
            db.add(job)
            db.commit()
            db.refresh(job)
            print(f"   - Ingested: {job.title} at {job.company_name} (Status: {job.status})")

        print("\n2. Launching V8 Autonomous daily loop on new target opportunities...")
        res = run_daily_autonomous_loop(db)

        print("\n=== AUTO-SCHEDULER RUN COMPLETE ===")
        print(f"Total processed: {res['processed']}")
        print(f"Total high-matching tailored: {res['matched']}")
        print(f"HTML Briefing generated: {res['briefing_sent']}")

        # Print compiled assets
        print("\n=== ANALYZED MATCHING REPORT ===")
        for job_data in target_jobs:
            job = db.query(JobOpportunityTable).filter(
                JobOpportunityTable.company_name == job_data["company"],
                JobOpportunityTable.title == job_data["title"]
            ).first()
            app = db.query(ApplicationTable).filter(ApplicationTable.job_id == job.id).first()
            if app:
                print(f"\n[+] {job.company_name} - {job.title}")
                print(f"    - Calculated Fit Score: {job.overall_score}%")
                print(f"    - Resume template: {app.resume_variant_id}")
                print(f"    - Cover letter: {app.cover_letter_path}")
                print(f"    - Recruiter outreach: {app.outreach_sequence_path}")
            else:
                print(f"\n[-] {job.company_name} - {job.title}")
                print(f"    - Calculated Fit Score: {job.overall_score}% (Did not meet threshold or failed grounding checks)")

    finally:
        db.close()

if __name__ == "__main__":
    ingest_research_opportunities()
