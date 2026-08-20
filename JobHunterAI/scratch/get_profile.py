import sqlite3
import json

db_path = "data/candidate.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

tables = [t[0] for t in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print("Tables:", tables)

for t in ['candidate_profile', 'skills', 'experiences', 'projects', 'education', 'knowledge_nodes', 'knowledge_edges']:
    if t in tables:
        rows = cursor.execute(f"SELECT * FROM {t}").fetchall()
        print(f"\n=== {t} ({len(rows)} rows) ===")
        for r in rows[:15]:
            print(dict(r))

conn.close()
