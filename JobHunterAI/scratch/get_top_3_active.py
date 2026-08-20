import sqlite3
import urllib.request
import sys
sys.stdout.reconfigure(encoding='utf-8')

db_path = "data/candidate.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

jobs = cursor.execute("""
    SELECT id, title, company_name, overall_score, url, remote_status
    FROM job_opportunities 
    WHERE status = 'discovered' AND company_name NOT IN ('Figma', 'Neon', 'Vercel', 'Augment Code', 'Dust', 'Windsurf', 'Reflect')
    ORDER BY overall_score DESC 
    LIMIT 20
""").fetchall()

def is_active(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            if 'jobs.ashbyhq.com' in url:
                if '"posting":null' in html:
                    return False
            elif 'greenhouse.io' in url:
                if 'This job is no longer available' in html or 'redirect' in response.geturl():
                    return False
            return True
    except Exception as e:
        return False

print("=== NEW LIVE JOBS ===")
count = 0
for j in jobs:
    d = dict(j)
    if is_active(d['url']):
        count += 1
        print(f"{count}. {d['company_name']} - {d['title']} ({d['overall_score']}%)")
        print(f"URL: {d['url']}\n")
        if count >= 3:
            break
    else:
        cursor.execute("UPDATE job_opportunities SET status = 'expired' WHERE id = ?", (d['id'],))
        conn.commit()

conn.close()
