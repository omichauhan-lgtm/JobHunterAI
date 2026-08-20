import sqlite3
conn = sqlite3.connect('data/candidate.db')
c = conn.cursor()
c.execute("SELECT id FROM job_opportunities WHERE company_name='Conga'")
res = c.fetchone()
print(f"Conga ID is: {res[0]}" if res else "Not found")
