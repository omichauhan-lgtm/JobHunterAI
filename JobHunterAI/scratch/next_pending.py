import sqlite3

db_path = "data/candidate.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get next pending fresh jobs (not yet applied)
jobs = cursor.execute("""
    SELECT id, title, company_name, overall_score, url, remote_status, status
    FROM job_opportunities
    WHERE status = 'discovered'
    ORDER BY overall_score DESC
    LIMIT 10
""").fetchall()

print("=== NEXT PENDING JOBS (discovered, by score) ===")
for i, j in enumerate(jobs, 1):
    d = dict(j)
    print(f"\n#{i}: {d['company_name']} — {d['title']}")
    print(f"    Score: {d['overall_score']}% | Remote: {d['remote_status']} | Status: {d['status']}")
    print(f"    URL: {d['url']}")

    # Check if PDF assets exist
    import os
    company_safe = d['company_name'].replace(' ', '_').replace('.', '.')
    gen_dir = "data/generated"
    resume_files = [f for f in os.listdir(gen_dir) if f.startswith(company_safe) and f.endswith('.pdf') and 'resume' in f.lower()]
    cl_files = [f for f in os.listdir(gen_dir) if f.startswith(company_safe) and f.endswith('.pdf') and 'cover' in f.lower()]
    print(f"    Resume PDF: {resume_files[0] if resume_files else 'NOT FOUND'}")
    print(f"    Cover Letter PDF: {cl_files[0] if cl_files else 'NOT FOUND'}")

conn.close()
