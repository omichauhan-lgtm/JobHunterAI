import sqlite3

conn = sqlite3.connect('JobHunterAI/data/candidate.db')
cursor = conn.cursor()
cursor.execute("UPDATE job_opportunities SET status = 'closed' WHERE id = 91")
conn.commit()
print("Updated Stability AI (ID: 91) status to 'closed'.")
