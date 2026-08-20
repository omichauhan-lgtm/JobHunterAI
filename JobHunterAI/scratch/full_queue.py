import sqlite3
import os
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
    LIMIT 15
""").fetchall()

gen_dir = "data/generated"

print("=" * 80)
print(f"{'#':<3} {'Company':<20} {'Role':<40} {'Score':<7} {'Remote':<10} {'Assets'}")
print("=" * 80)

for i, j in enumerate(jobs[:15], 1):
    d = dict(j)
    company_safe = d['company_name'].replace(' ', '_')
    
    resume_ready = any(f.startswith(company_safe) and 'resume' in f.lower() and f.endswith('.pdf') for f in os.listdir(gen_dir))
    cl_ready = any(f.startswith(company_safe) and 'cover' in f.lower() and f.endswith('.pdf') for f in os.listdir(gen_dir))
    
    assets = ""
    if resume_ready and cl_ready:
        assets = "✓ Resume + CL PDF"
    elif resume_ready:
        assets = "✓ Resume only"
    else:
        assets = "✗ Need generation"
    
    print(f"{i:<3} {d['company_name']:<20} {d['title'][:38]:<40} {d['overall_score']:<7} {d['remote_status']:<10} {assets}")
    print(f"    URL: {d['url']}")
    
    # Show first 150 chars of JD for context
    jd_preview = (d['jd_text'] or '')[:150].replace('\n', ' ')
    print(f"    JD: {jd_preview}...")
    print()

conn.close()
