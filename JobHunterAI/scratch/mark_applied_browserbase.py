import sqlite3
import datetime

db_path = "JobHunterAI/data/candidate.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Job ID 88 is Browserbase
job_id = 88
cursor.execute("UPDATE job_opportunities SET status = 'applied' WHERE id = ?", (job_id,))

# Get resume variant for Browserbase
rv = cursor.execute("SELECT id FROM resume_variants WHERE latex_source LIKE '%Browserbase%' OR latex_source LIKE '%Full Stack%' ORDER BY id DESC LIMIT 1").fetchone()
variant_id = rv['id'] if rv else 1

cl_pdf_path = r"JobHunterAI\data\generated\Browserbase_cover_letter.pdf"
outreach_path = r"JobHunterAI\data\generated\Browserbase_outreach.txt"

cursor.execute("""
    INSERT INTO applications (candidate_id, job_id, resume_variant_id, cover_letter_path, outreach_sequence_path, status, date_applied)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", (1, job_id, variant_id, cl_pdf_path, outreach_path, 'Applied', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

conn.commit()
print("Successfully recorded Browserbase application in candidate.db!")
