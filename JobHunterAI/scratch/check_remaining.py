import sqlite3
from datetime import datetime

db_path = "data/candidate.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Mark Notion listing as expired since posting:null on Ashby
cursor.execute("UPDATE job_opportunities SET status = 'expired' WHERE company_name = 'Notion' AND status = 'discovered'")
print(f"Marked Notion as expired (rows affected: {cursor.rowcount})")

conn.commit()

# Get remaining discovered jobs in the fresh batch
fresh_companies = ['Primer.io', 'HospiChef', 'Retell AI', 'Netic']
print("\n=== REMAINING FRESH BATCH ===")
for c in fresh_companies:
    job = cursor.execute(
        "SELECT id, title, company_name, overall_score, url, status FROM job_opportunities WHERE company_name LIKE ? AND status = 'discovered'",
        (f"%{c}%",)
    ).fetchone()
    if job:
        print(f"  {job[2]} — {job[1]} (Score: {job[3]}%, URL: {job[4]})")

# Also get top 5 from full queue
print("\n=== TOP 5 FROM FULL QUEUE (not fresh batch) ===")
jobs = cursor.execute("""
    SELECT id, title, company_name, overall_score, url 
    FROM job_opportunities 
    WHERE status = 'discovered' 
    AND company_name NOT IN ('Primer.io', 'HospiChef', 'Retell AI', 'Netic')
    ORDER BY overall_score DESC 
    LIMIT 5
""").fetchall()
for j in jobs:
    print(f"  {j[2]} — {j[1]} (Score: {j[3]}%, URL: {j[4]})")

conn.close()
