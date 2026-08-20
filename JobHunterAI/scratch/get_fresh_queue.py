import sqlite3

db_path = "data/candidate.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("=== TOP SCORES: NEWEST FRESH JOBS ===")
jobs = cursor.execute("""
    SELECT id, title, company_name, overall_score, url, remote_status
    FROM job_opportunities 
    WHERE status = 'discovered' 
    ORDER BY overall_score DESC 
    LIMIT 10
""").fetchall()

for i, j in enumerate(jobs, 1):
    d = dict(j)
    print(f"{i:<3} {d['company_name'][:19]:<20} {d['title'][:33]:<35} {d['overall_score']:<7} {d['remote_status'][:9]:<10}")
    print(f"    URL: {d['url']}\n")

conn.close()
