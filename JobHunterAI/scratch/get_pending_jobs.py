import sqlite3
import os
import json

db_path = "JobHunterAI/data/candidate.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

jobs = cursor.execute("""
    SELECT id, title, company_name, overall_score, status, url, source, remote_status, salary_range 
    FROM job_opportunities 
    WHERE status = 'discovered' 
    ORDER BY overall_score DESC 
    LIMIT 15
""").fetchall()

print(f"Found {len(jobs)} discovered jobs for application review:\n")
for idx, j in enumerate(jobs, 1):
    job_id = j['id']
    comp = j['company_name']
    title = j['title']
    score = j['overall_score']
    url = j['url']
    
    # Check generated files
    gen_dir = "JobHunterAI/data/generated"
    pdf_files = [f for f in os.listdir(gen_dir) if f.startswith(comp.replace(" ", "_")) and f.endswith(".pdf")] if os.path.exists(gen_dir) else []
    cl_files = [f for f in os.listdir(gen_dir) if f.startswith(comp.replace(" ", "_")) and f.endswith("cover_letter.md")] if os.path.exists(gen_dir) else []
    
    print(f"{idx}. [{comp}] {title}")
    print(f"   - Match Score: {score}%")
    print(f"   - Job URL: {url}")
    print(f"   - Tailored Resume PDF: {pdf_files[0] if pdf_files else 'Not compiled'}")
    print(f"   - Cover Letter: {cl_files[0] if cl_files else 'Not compiled'}")
    print(f"   - Status: Pending User Approval\n")
