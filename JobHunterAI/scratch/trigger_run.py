import json
from storage.db import SessionLocal, JobOpportunityTable, ApplicationTable
from orchestrator import run_daily_autonomous_loop
from config import logger

def simulate_job_search_and_tailoring():
    db = SessionLocal()
    try:
        print("1. Injecting a new remote matching job opportunity...")
        
        # Check if already exists to prevent key violations
        existing = db.query(JobOpportunityTable).filter(
            JobOpportunityTable.company_name == "VectorShift",
            JobOpportunityTable.title == "AI Systems Engineer"
        ).first()
        
        if existing:
            db.delete(existing)
            db.commit()
            
        # Create VectorShift job in discovered state
        job = JobOpportunityTable(
            title="AI Systems Engineer",
            company_name="VectorShift",
            jd_text="""
            We are hiring an AI Systems Engineer to build core LLM orchestration pipelines.
            Requirements:
            - Strong experience with Python, FastAPI, Docker, and PostgreSQL.
            - Developed custom LLM prompt routing, evaluation frameworks, and middleware.
            - Experience with key caching algorithms and telemetry metrics is preferred.
            - Location: Remote
            """,
            url="https://boards.greenhouse.io/vectorshift/ai-systems-engineer",
            source="Greenhouse",
            remote_status="Remote",
            salary_range="$140,000 - $180,000",
            tech_stack_json=json.dumps(["Python", "FastAPI", "Docker", "PostgreSQL", "LLM Routing"]),
            status="discovered"
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        print(f"   Successfully injected [{job.id}] {job.title} at {job.company_name} (Status: {job.status})")
        
        print("\n2. Executing the daily autonomous loop...")
        res = run_daily_autonomous_loop(db)
        
        print("\n=== EXECUTION RESULTS ===")
        print(f"Processed opportunities: {res['processed']}")
        print(f"High-matching opportunities tailored: {res['matched']}")
        print(f"Daily Briefing Delivered: {res['briefing_sent']}")
        
        # Query generated app details
        app = db.query(ApplicationTable).filter(ApplicationTable.job_id == job.id).first()
        if app:
            print("\n=== TAILORED ASSETS GENERATED ===")
            print(f"- Resume version ID: {app.resume_variant_id}")
            print(f"- Cover letter path: {app.cover_letter_path}")
            print(f"- Outreach path: {app.outreach_sequence_path}")
            
            # Check explainability file
            import os
            safe_company = job.company_name.replace(" ", "_")
            exp_file = os.path.join(os.path.dirname(app.cover_letter_path), f"{safe_company}_explainability.json")
            if os.path.exists(exp_file):
                print(f"- Explainability report path: {exp_file}")
                with open(exp_file, "r") as f:
                    exp_data = json.load(f)
                print(f"  - Calculated Job Fit Score: {exp_data['decision_parameters']['job_fit_score']}%")
                print(f"  - ATS optimization: {exp_data['ats_score_comparison']['initial_percent']}% -> {exp_data['ats_score_comparison']['final_percent']}%")
        else:
            print("\nWarning: No application package was compiled for VectorShift. Check logs for validation failures.")
            
    finally:
        db.close()

if __name__ == "__main__":
    simulate_job_search_and_tailoring()
