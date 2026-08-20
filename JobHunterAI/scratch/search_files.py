import os
import glob
from datetime import datetime

search_paths = [
    r"C:\Users\omich\OneDrive\Desktop",
    r"C:\Users\omich\Downloads",
    r"c:\Users\omich\OneDrive\Desktop\antigravity workspace\jobHunt"
]

print("Searching for files...")
for sp in search_paths:
    if os.path.exists(sp):
        for root, dirs, files in os.walk(sp):
            # limit depth
            if root.count(os.sep) - sp.count(os.sep) > 3:
                continue
            for f in files:
                f_lower = f.lower()
                if "final" in f_lower or "application" in f_lower or "sheet" in f_lower or "job" in f_lower or f.endswith(".pdf"):
                    fp = os.path.join(root, f)
                    try:
                        mtime = datetime.fromtimestamp(os.path.getmtime(fp))
                        print(f"{mtime} - {fp}")
                    except Exception:
                        pass
