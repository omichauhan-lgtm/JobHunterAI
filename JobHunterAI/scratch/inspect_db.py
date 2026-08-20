import sqlite3
import os

db_path = "JobHunterAI/data/candidate.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    print("Tables in DB:", [t[0] for t in tables])
    for t in tables:
        tname = t[0]
        cnt = cursor.execute(f"SELECT COUNT(*) FROM {tname}").fetchone()[0]
        print(f"Table '{tname}': {cnt} rows")

print("\nPDF files outside generated folder:")
for root, dirs, files in os.walk("."):
    if "generated" in root:
        continue
    for f in files:
        if f.endswith(('.pdf', '.csv', '.xlsx', '.sheet')) or 'final' in f.lower() or 'application' in f.lower():
            print(os.path.join(root, f))
