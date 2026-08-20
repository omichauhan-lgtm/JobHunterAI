import sqlite3

db_path = "data/candidate.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Mark Augment Code listing as expired
cursor.execute("UPDATE job_opportunities SET status = 'expired' WHERE company_name = 'Augment Code' AND status = 'discovered'")
print(f"Marked Augment Code as expired (rows affected: {cursor.rowcount})")

conn.commit()
conn.close()
