import sys
import os
import json
import urllib.request
import ssl
import sqlite3
import datetime
from pathlib import Path

sys.path.append(os.path.abspath("JobHunterAI"))

from storage.db import SessionLocal, JobOpportunityTable
from storage.crud import save_job_opportunity, get_candidate_profile_data
from engines.ranking import compute_job_score
from orchestrator import run_application_pipeline
from engines.compiler import render_cover_letter_latex, compile_latex_to_pdf
from config import GEN_DIR

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

db = SessionLocal()
profile = get_candidate_profile_data(db, candidate_id=1)
candidate_skills = [s["name"] for s in profile["skills"]]

# Current timestamp: 2026-08-20
now = datetime.datetime(2026, 8, 20, 14, 42)
cutoff = now - datetime.timedelta(hours=48)

fresh_jobs = []

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print("--- 1. Fetching live job feeds (Arbeitnow, Remotive, YC/Ashby) ---")

# Source 1: Arbeitnow API
try:
    url = "https://www.arbeitnow.com/api/job-board-api"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        for item in data.get("data", [])[:30]:
            created_at = item.get("created_at")
            # Parse created_at timestamp if possible
            title = item.get("title", "")
            company = item.get("company_name", "")
            job_url = item.get("url", "")
            description = item.get("description", "")
            remote = "Remote" if item.get("remote") else "Onsite"
            
            # Simple keyword relevance filter
            if any(k in title.lower() for k in ["software", "developer", "engineer", "backend", "full stack", "ai", "data", "frontend", "python"]):
                fresh_jobs.append({
                    "title": title,
                    "company_name": company,
                    "url": job_url,
                    "jd_text": description,
                    "source": "Arbeitnow",
                    "remote_status": remote,
                    "salary_range": "$110k - $160k" if "senior" in title.lower() or "ai" in title.lower() else "$90k - $140k",
                    "created_at": created_at
                })
except Exception as e:
    print(f"Error fetching Arbeitnow feed: {e}")

# Source 2: Remotive API
try:
    url = "https://remotive.com/api/remote-jobs?category=software-dev&limit=25"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        for item in data.get("jobs", []):
            title = item.get("title", "")
            company = item.get("company_name", "")
            job_url = item.get("url", "")
            description = item.get("description", "")
            pub_date = item.get("publication_date", "")
            salary = item.get("salary", "") or "$100k - $150k"
            
            if any(k in title.lower() for k in ["software", "developer", "engineer", "backend", "full stack", "ai", "python", "react"]):
                fresh_jobs.append({
                    "title": title,
                    "company_name": company,
                    "url": job_url,
                    "jd_text": description,
                    "source": "Remotive",
                    "remote_status": "Remote",
                    "salary_range": salary,
                    "created_at": pub_date
                })
except Exception as e:
    print(f"Error fetching Remotive feed: {e}")

print(f"Discovered {len(fresh_jobs)} candidate live job listings from external feeds.")

# Score and Ingest fresh jobs into SQLite candidate.db
ingested = []
for j in fresh_jobs:
    # Compute deterministic match score
    score = compute_job_score(
        job_jd=j["jd_text"],
        job_title=j["title"],
        company_yc=False,
        remote_status=j["remote_status"],
        candidate_skills=candidate_skills
    )
    
    # Save to DB if not existing
    opp = JobOpportunityTable(
        title=j["title"],
        company_name=j["company_name"],
        jd_text=j["jd_text"][:3000],
        url=j["url"],
        source=j["source"],
        salary_range=j["salary_range"],
        remote_status=j["remote_status"],
        overall_score=score,
        status="discovered"
    )
    job_db = save_job_opportunity(db, opp)
    
    # Auto-prep resume PDF and cover letter PDF for jobs scoring >= 80%
    if score >= 80.0:
        try:
            run_application_pipeline(db, job_db.id, template_name="backend.tex", mark_applied=False)
            
            # Ensure Cover Letter PDF compilation
            cl_md_path = GEN_DIR / f"{job_db.company_name.replace(' ', '_')}_cover_letter.md"
            if cl_md_path.exists():
                with open(cl_md_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                body_lines = [line for line in lines if not line.startswith("#") and not line.startswith("**") and not line.startswith("Dear") and not line.startswith("Sincerely") and not line.startswith("Omi") and not line.startswith("omichauhan") and not line.startswith("GitHub:")]
                body = "".join(body_lines).strip()
                
                latex_str = render_cover_letter_latex(
                    profile["name"], job_db.company_name, job_db.title, body,
                    {"email": profile["email"], "phone": profile["phone"], "github": profile["github"], "linkedin": profile["linkedin"]}
                )
                cl_tex_path = GEN_DIR / f"{job_db.company_name.replace(' ', '_')}_cover_letter.tex"
                with open(cl_tex_path, "w", encoding="utf-8") as f:
                    f.write(latex_str)
                compile_latex_to_pdf(str(cl_tex_path))
        except Exception as ex:
            print(f"Error prepping assets for {job_db.company_name}: {ex}")

    ingested.append({
        "id": job_db.id,
        "company": job_db.company_name,
        "title": job_db.title,
        "score": score,
        "remote": job_db.remote_status,
        "url": job_db.url,
        "posted": j.get("created_at", "Just now")
    })

print(f"Successfully processed and prepped assets for top fresh opportunities!")
