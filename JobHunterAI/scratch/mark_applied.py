import sqlite3
from datetime import datetime

db_path = "data/candidate.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

now = datetime.now().isoformat()

existing = cursor.execute("SELECT id FROM applications WHERE job_id = 23").fetchone()
if existing:
    cursor.execute("UPDATE applications SET status = 'applied', date_applied = ? WHERE job_id = 23", (now,))
    print(f"Updated existing application for Conga (job_id=23) to 'applied'")
else:
    cursor.execute(
        "INSERT INTO applications (candidate_id, job_id, status, date_applied, cover_letter_path) VALUES (?, ?, ?, ?, ?)",
        (1, 23, "applied", now, "Conga_cover_letter.pdf")
    )
    print(f"Created new application record for Conga (job_id=23)")

cursor.execute("UPDATE job_opportunities SET status = 'applied' WHERE id = 23")
print("Updated job_opportunities status to 'applied'")

conn.commit()

print("\n=== ALL APPLIED JOBS ===")
apps = cursor.execute("""
    SELECT a.id, a.job_id, a.status, a.date_applied, j.title, j.company_name
    FROM applications a
    JOIN job_opportunities j ON a.job_id = j.id
    WHERE a.status = 'applied'
    ORDER BY a.date_applied DESC
""").fetchall()
for a in apps:
    print(dict(a))

conn.close()
