import sqlite3

db_path = "data/candidate.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

job = cursor.execute("SELECT * FROM job_opportunities WHERE company_name LIKE '%Apaleo%'").fetchone()
if job:
    d = dict(job)
    for k, v in d.items():
        print(f"{k}: {v}")
else:
    print("No Apaleo job found")

conn.close()
