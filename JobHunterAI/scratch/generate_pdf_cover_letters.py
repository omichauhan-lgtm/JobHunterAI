import sqlite3
import os
import sys
from pathlib import Path

# Add project directory to sys.path
sys.path.append(os.path.abspath("JobHunterAI"))

from storage.db import SessionLocal, JobOpportunityTable
from storage.crud import get_candidate_profile_data
from engines.compiler import render_cover_letter_latex, compile_latex_to_pdf
from engines.cover_letter import generate_tailored_cover_letter
from engines.company_intel import run_company_intelligence
from config import GEN_DIR

db = SessionLocal()
profile = get_candidate_profile_data(db, candidate_id=1)

jobs = db.query(JobOpportunityTable).order_by(JobOpportunityTable.overall_score.desc()).limit(20).all()

print(f"Generating PDF cover letters for top {len(jobs)} jobs...")

compiled_count = 0
for j in jobs:
    safe_company_name = j.company_name.replace(" ", "_")
    cl_md_path = GEN_DIR / f"{safe_company_name}_cover_letter.md"
    cl_tex_path = GEN_DIR / f"{safe_company_name}_cover_letter.tex"
    cl_pdf_path = GEN_DIR / f"{safe_company_name}_cover_letter.pdf"
    
    # Read existing markdown body if available or generate
    if cl_md_path.exists():
        with open(cl_md_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        body_lines = [line for line in lines if not line.startswith("#") and not line.startswith("**") and not line.startswith("Dear") and not line.startswith("Sincerely") and not line.startswith("Omi") and not line.startswith("omichauhan") and not line.startswith("GitHub:")]
        body = "".join(body_lines).strip()
        if not body:
            company_intel = run_company_intelligence(j.company_name, j.jd_text)
            body = generate_tailored_cover_letter(profile, {"title": j.title, "company_name": j.company_name}, company_intel)
    else:
        company_intel = run_company_intelligence(j.company_name, j.jd_text)
        body = generate_tailored_cover_letter(profile, {"title": j.title, "company_name": j.company_name}, company_intel)
        
    # Render LaTeX cover letter
    latex_str = render_cover_letter_latex(
        profile["name"], j.company_name, j.title, body,
        {"email": profile["email"], "phone": profile["phone"], "github": profile["github"], "linkedin": profile["linkedin"]}
    )
    
    with open(cl_tex_path, "w", encoding="utf-8") as f:
        f.write(latex_str)
        
    success = compile_latex_to_pdf(str(cl_tex_path))
    if success and cl_pdf_path.exists():
        print(f"[OK] [{j.company_name}] Cover Letter PDF: {cl_pdf_path.name}")
        compiled_count += 1
    else:
        print(f"[FAIL] [{j.company_name}] Failed to compile PDF")

print(f"\nCompleted! Generated {compiled_count} Cover Letter PDFs.")
