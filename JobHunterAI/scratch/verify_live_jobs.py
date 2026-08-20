import sqlite3
import urllib.request
import json
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
    LIMIT 40
""").fetchall()

print(f"Checking live status of top {len(jobs)} discovered jobs...\n")

active_jobs = []

for j in jobs:
    url = j['url']
    is_active = False
    
    if not url:
        continue
        
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=5, context=ctx) as response:
            html = response.read().decode('utf-8', errors='ignore')
            if "jobs.ashbyhq.com" in url:
                if '"posting":null' in html:
                    is_active = False
                else:
                    is_active = True
            elif "lever.co" in url or "greenhouse.io" in url:
                is_active = response.status == 200
            else:
                is_active = response.status == 200
    except Exception as e:
        is_active = False
        
    if not is_active:
        cursor.execute("UPDATE job_opportunities SET status = 'closed' WHERE id = ?", (j['id'],))
        print(f"[CLOSED] {j['company_name']} - {j['title']} (ID: {j['id']})")
    else:
        active_jobs.append(j)
        print(f"[ACTIVE] {j['company_name']} - {j['title']} (ID: {j['id']}) -> {url}")

conn.commit()
print(f"\nFound {len(active_jobs)} verified active opportunities!")
