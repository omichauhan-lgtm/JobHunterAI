import sqlite3

db_path = "JobHunterAI/data/candidate.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("--- TOP 20 JOB OPPORTUNITIES BY OVERALL_SCORE ---")
jobs = cursor.execute("SELECT id, title, company_name, overall_score, status, url, source FROM job_opportunities ORDER BY overall_score DESC LIMIT 20").fetchall()
for j in jobs:
    print(f"ID: {j['id']} | Score: {j['overall_score']} | Company: {j['company_name']} | Title: {j['title']} | Status: {j['status']} | URL: {j['url']}")
