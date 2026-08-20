import sys
import os
import sqlite3

sys.path.append(os.path.abspath("JobHunterAI"))

from storage.db import SessionLocal, JobOpportunityTable
from storage.crud import save_job_opportunity
from engines.discovery import discover_job_from_url
from orchestrator import run_application_pipeline
from engines.compiler import render_cover_letter_latex, compile_latex_to_pdf
from storage.crud import get_candidate_profile_data
from config import GEN_DIR

db = SessionLocal()
profile = get_candidate_profile_data(db, candidate_id=1)

# Ingest live high-quality engineering postings
sample_urls = [
    "https://jobs.lever.co/posthog/full-stack-engineer",
    "https://boards.greenhouse.io/vapi/jobs/software-engineer-ai",
    "https://jobs.ashbyhq.com/resend/software-engineer",
    "https://jobs.ashbyhq.com/unkey/full-stack-engineer"
]

print("Ingesting fresh live job postings...")

for url in sample_urls:
    try:
        job = discover_job_from_url(db, url)
        if job:
            print(f"✅ Ingested: [{job.company_name}] {job.title} (ID: {job.id})")
            # Auto-run pipeline to generate assets
            res = run_application_pipeline(db, job.id, template_name="backend.tex", mark_applied=False)
            
            # Render and compile PDF cover letter
            cl_md_path = GEN_DIR / f"{job.company_name.replace(' ', '_')}_cover_letter.md"
            if cl_md_path.exists():
                with open(cl_md_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                body_lines = [line for line in lines if not line.startswith("#") and not line.startswith("**") and not line.startswith("Dear") and not line.startswith("Sincerely") and not line.startswith("Omi") and not line.startswith("omichauhan") and not line.startswith("GitHub:")]
                body = "".join(body_lines).strip()
                
                latex_str = render_cover_letter_latex(
                    profile["name"], job.company_name, job.title, body,
                    {"email": profile["email"], "phone": profile["phone"], "github": profile["github"], "linkedin": profile["linkedin"]}
                )
                cl_tex_path = GEN_DIR / f"{job.company_name.replace(' ', '_')}_cover_letter.tex"
                with open(cl_tex_path, "w", encoding="utf-8") as f:
                    f.write(latex_str)
                compile_latex_to_pdf(str(cl_tex_path))
    except Exception as e:
        print(f"Error ingesting {url}: {e}")

print("Done ingesting fresh opportunities.")
