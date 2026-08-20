import os
import sys

sys.path.append(os.path.abspath("JobHunterAI"))

from storage.db import SessionLocal
from orchestrator import run_application_pipeline
from engines.compiler import render_cover_letter_latex, compile_latex_to_pdf
from storage.crud import get_candidate_profile_data
from storage.db import JobOpportunityTable
from config import GEN_DIR

db = SessionLocal()
job_id = 71 # ecosio

res = run_application_pipeline(db, job_id=job_id, template_name="frontend.tex", mark_applied=False)
print("Pipeline result for ecosio:", res)

# Ensure PDF Cover Letter is compiled
job = db.query(JobOpportunityTable).filter(JobOpportunityTable.id == job_id).first()
profile = get_candidate_profile_data(db, candidate_id=1)

cl_md_path = GEN_DIR / "ecosio_cover_letter.md"
if cl_md_path.exists():
    with open(cl_md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    body_lines = [line for line in lines if not line.startswith("#") and not line.startswith("**") and not line.startswith("Dear") and not line.startswith("Sincerely") and not line.startswith("Omi") and not line.startswith("omichauhan") and not line.startswith("GitHub:")]
    body = "".join(body_lines).strip()
    
    latex_str = render_cover_letter_latex(
        profile["name"], job.company_name, job.title, body,
        {"email": profile["email"], "phone": profile["phone"], "github": profile["github"], "linkedin": profile["linkedin"]}
    )
    cl_tex_path = GEN_DIR / "ecosio_cover_letter.tex"
    cl_pdf_path = GEN_DIR / "ecosio_cover_letter.pdf"
    with open(cl_tex_path, "w", encoding="utf-8") as f:
        f.write(latex_str)
    compile_latex_to_pdf(str(cl_tex_path))
    print("ecosio Cover Letter PDF compiled:", cl_pdf_path.exists())
