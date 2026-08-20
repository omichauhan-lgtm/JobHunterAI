import sys
import os
from sqlalchemy import text

sys.path.append(os.path.abspath("JobHunterAI"))

from storage.db import SessionLocal, JobOpportunityTable
from orchestrator import run_application_pipeline
from engines.compiler import render_cover_letter_latex, compile_latex_to_pdf
from storage.crud import get_candidate_profile_data
from config import GEN_DIR

db = SessionLocal()
profile = get_candidate_profile_data(db, candidate_id=1)

top_jobs = db.query(JobOpportunityTable).filter(
    JobOpportunityTable.status == "discovered"
).filter(
    (JobOpportunityTable.source.like("%aug20%")) | 
    (JobOpportunityTable.source.like("%Arbeitnow%")) | 
    (JobOpportunityTable.source.like("%Remotive%"))
).order_by(JobOpportunityTable.overall_score.desc()).limit(5).all()

print(f"Prepping PDF Resume & PDF Cover Letter for top {len(top_jobs)} fresh opportunities...")

for job in top_jobs:
    company = job.company_name
    title = job.title
    safe_company = company.replace(" ", "_")
    try:
        # Run orchestrator pipeline
        res = run_application_pipeline(db, job_id=job.id, template_name="backend.tex", mark_applied=False)
        
        # Compile PDF cover letter
        cl_md_path = GEN_DIR / f"{safe_company}_cover_letter.md"
        if cl_md_path.exists():
            with open(cl_md_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            body_lines = [line for line in lines if not line.startswith("#") and not line.startswith("**") and not line.startswith("Dear") and not line.startswith("Sincerely") and not line.startswith("Omi") and not line.startswith("omichauhan") and not line.startswith("GitHub:")]
            body = "".join(body_lines).strip()
            
            latex_str = render_cover_letter_latex(
                profile["name"], company, title, body,
                {"email": profile["email"], "phone": profile["phone"], "github": profile["github"], "linkedin": profile["linkedin"]}
            )
            cl_tex_path = GEN_DIR / f"{safe_company}_cover_letter.tex"
            cl_pdf_path = GEN_DIR / f"{safe_company}_cover_letter.pdf"
            with open(cl_tex_path, "w", encoding="utf-8") as f:
                f.write(latex_str)
            compile_latex_to_pdf(str(cl_tex_path))
            print(f"[OK] [{company}] PDF Cover Letter & Resume prepped cleanly!")
    except Exception as e:
        print(f"[FAIL] Error prepping [{company}]: {e}")

print("\nBatch prep complete!")
