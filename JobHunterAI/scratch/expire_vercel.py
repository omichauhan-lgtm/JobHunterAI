import sqlite3

db_path = "data/candidate.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Mark Vercel listing as expired
cursor.execute("UPDATE job_opportunities SET status = 'expired' WHERE company_name = 'Vercel' AND status = 'discovered'")
print(f"Marked Vercel as expired (rows affected: {cursor.rowcount})")

conn.commit()
conn.close()
