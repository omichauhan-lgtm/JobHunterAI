import sqlite3
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

db_path = "JobHunterAI/data/candidate.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

jobs = cursor.execute("""
    SELECT id, title, company_name, overall_score, status, url 
    FROM job_opportunities 
    WHERE status = 'discovered' 
    ORDER BY overall_score DESC 
    LIMIT 25
""").fetchall()

print(f"Testing top {len(jobs)} remaining discovered jobs...\n")

for j in jobs:
    url = j['url']
    if not url:
        continue
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=4, context=ctx) as response:
            html = response.read().decode('utf-8', errors='ignore')
            if 'posting":null' in html or response.status != 200:
                cursor.execute("UPDATE job_opportunities SET status = 'closed' WHERE id = ?", (j['id'],))
                print(f"[CLOSED] ID {j['id']}: {j['company_name']} - {j['title']}")
            else:
                print(f"[LIVE] ID {j['id']}: {j['company_name']} - {j['title']} (Score: {j['overall_score']}%) -> {url}")
    except Exception:
        cursor.execute("UPDATE job_opportunities SET status = 'closed' WHERE id = ?", (j['id'],))
        print(f"[CLOSED] ID {j['id']}: {j['company_name']} - {j['title']}")

conn.commit()
