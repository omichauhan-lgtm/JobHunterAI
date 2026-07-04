from storage.db import SessionLocal, JobOpportunityTable, ApplicationTable

db = SessionLocal()
try:
    print("=== OPPORTUNITIES IN DATABASE ===")
    jobs = db.query(JobOpportunityTable).all()
    for j in jobs:
        app = db.query(ApplicationTable).filter(ApplicationTable.job_id == j.id).first()
        print(f"ID: {j.id} | {j.company_name} | {j.title} | Score: {j.overall_score}% | Status: {j.status} | App Ready: {app is not None}")
finally:
    db.close()
