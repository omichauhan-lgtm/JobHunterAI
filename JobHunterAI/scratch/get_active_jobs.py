import sqlite3

db_path = "JobHunterAI/data/candidate.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

jobs = cursor.execute("""
    SELECT id, title, company_name, overall_score, status, url 
    FROM job_opportunities 
    WHERE status = 'discovered' 
    ORDER BY overall_score DESC 
    LIMIT 10
""").fetchall()

print(f"Top {len(jobs)} active discovered jobs:\n")
for idx, j in enumerate(jobs, 1):
    print(f"{idx}. [{j['company_name']}] {j['title']} (Score: {j['overall_score']}%)")
    print(f"   URL: {j['url']}\n")
