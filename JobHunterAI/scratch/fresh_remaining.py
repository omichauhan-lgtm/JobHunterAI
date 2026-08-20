import sqlite3

db_path = "data/candidate.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Fresh batch companies from the <48h list
fresh_companies = ['Primer.io', 'Primer', 'HospiChef', 'Scale AI', 'Notion', 'Retell AI', 'Retell', 'Netic']

print("=== FRESH <48H BATCH - REMAINING ===\n")
for company in fresh_companies:
    job = cursor.execute(
        "SELECT id, title, company_name, overall_score, url, remote_status, status FROM job_opportunities WHERE company_name LIKE ? AND status = 'discovered'",
        (f"%{company}%",)
    ).fetchone()
    if job:
        d = dict(job)
        print(f"  {d['company_name']} — {d['title']}")
        print(f"    Score: {d['overall_score']}% | Remote: {d['remote_status']} | URL: {d['url']}")
        print()

conn.close()
