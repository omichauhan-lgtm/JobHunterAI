import sqlite3
import urllib.request
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')


db_path = "data/candidate.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

jobs = cursor.execute("""
    SELECT id, title, company_name, overall_score, url, remote_status, jd_text
    FROM job_opportunities 
    WHERE status = 'discovered' 
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
                # If greenhouse redirects or says "Job not found"
                if 'This job is no longer available' in html or 'redirect' in response.geturl():
                    return False
            
            return True
    except Exception as e:
        print(f"Error checking {url}: {e}")
        return False

for j in jobs:
    d = dict(j)
    print(f"Checking {d['company_name']} - {d['title']}...")
    if is_active(d['url']):
        print(f"\n✅ LIVE: {d['company_name']} - {d['title']}")
        print(f"URL: {d['url']}")
        break
    else:
        print(f"❌ Expired. Marking in DB...")
        cursor.execute("UPDATE job_opportunities SET status = 'expired' WHERE id = ?", (d['id'],))
        conn.commit()

conn.close()
