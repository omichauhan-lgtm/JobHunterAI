import sqlite3
conn = sqlite3.connect('data/candidate.db')
c = conn.cursor()
c.execute("SELECT id, company_name, title, overall_score, url FROM job_opportunities WHERE company_name IN ('Primer.io', 'Patlytics, Inc.') AND status='discovered' ORDER BY overall_score DESC")
for r in c.fetchall():
    print(r)
