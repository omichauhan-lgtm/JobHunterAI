import sqlite3
from datetime import datetime

db_path = "data/candidate.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Mark Scale AI as expired/closed
cursor.execute("UPDATE job_opportunities SET status = 'expired' WHERE id = 93")
print("Marked Scale AI (id=93) as 'expired' - listing no longer active")

conn.commit()
conn.close()
