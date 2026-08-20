import sqlite3

conn = sqlite3.connect('JobHunterAI/data/candidate.db')
cursor = conn.cursor()
cursor.execute("UPDATE job_opportunities SET status = 'closed' WHERE id = 84")
conn.commit()
print("Updated Together AI (ID: 84) status to 'closed'.")
