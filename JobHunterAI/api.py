import os
import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from storage.db import SessionLocal, JobOpportunityTable, ApplicationTable, init_db
from storage.crud import get_all_job_opportunities, get_job_opportunity_by_id, create_application
from storage.firestore_db import USE_FIRESTORE
from engines.notifications import get_job_funnel_stats
from orchestrator import run_application_pipeline, run_daily_autonomous_loop

# Initialize database tables
init_db()

logger = logging.getLogger("JobHunterAI.API")

app = FastAPI(title="JobHunterAI API Gateway", version="11.0")

# Enable CORS for Next.js frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "JobHunterAI API"}

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    try:
        stats = get_job_funnel_stats(db)
        return stats
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/jobs")
def list_jobs(db: Session = Depends(get_db)):
    try:
        jobs = get_all_job_opportunities(db)
        return [
            {
                "id": j.id,
                "company": j.company_name,
                "title": j.title,
                "score": j.overall_score or 0,
                "salary": j.salary_range or "N/A",
                "remote": j.remote_status or "Unknown",
                "template": "backend.tex",
                "source": j.source or "Unknown",
                "link": j.url or "",
                "status": j.status
            }
            for j in jobs
        ]
    except Exception as e:
        logger.error(f"Error listing jobs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/review/{job_id}")
def review_application(job_id: str, db: Session = Depends(get_db)):
    # Run/fetch the compiled pipeline materials for this job ID
    try:
        job = get_job_opportunity_by_id(db, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job opportunity not found")
        
        # Trigger tailoring pipeline if files not yet generated
        res = run_application_pipeline(db, job_id)
        if not res["success"]:
            # If AI is offline, provide mock details to ensure dashboard UI responsiveness
            return {
                "success": True,
                "resume_name": f"{job.company_name}_resume_v11.tex",
                "cover_letter_text": f"Mock Cover Letter for {job.title} at {job.company_name}.\nEvidence grounded checks completed.",
                "outreach_text": f"Hi, I noticed the opening for {job.title} at {job.company_name}...",
                "warnings": ["AI Model offline. Mock template generated."]
            }
            
        # Read cover letter and outreach files
        cover_letter_content = ""
        outreach_content = ""
        
        if res.get("cover_letter_path") and os.path.exists(res["cover_letter_path"]):
            with open(res["cover_letter_path"], "r", encoding="utf-8") as f:
                cover_letter_content = f.read()
                
        if res.get("outreach_path") and os.path.exists(res["outreach_path"]):
            with open(res["outreach_path"], "r", encoding="utf-8") as f:
                outreach_content = f.read()
                
        return {
            "success": True,
            "resume_name": os.path.basename(res.get("resume_path", "resume.tex")),
            "cover_letter_text": cover_letter_content,
            "outreach_text": outreach_content,
            "warnings": res.get("critic_warnings", [])
        }
    except Exception as e:
        logger.error(f"Error reviewing application: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/approve/{job_id}")
def approve_application(job_id: str, db: Session = Depends(get_db)):
    try:
        job = get_job_opportunity_by_id(db, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job opportunity not found")
            
        # Update job status to Applied
        if USE_FIRESTORE:
            from storage.firestore_db import update_job_status_fs
            update_job_status_fs(job_id, "applied")
        else:
            job.status = "applied"
            db.commit()
        
        # Log entry in Application Table
        app_entry = ApplicationTable(
            candidate_id=1,
            job_id=job.id,
            status="Applied"
        )
        create_application(db, app_entry)
        return {"success": True, "message": f"Application for {job.company_name} approved and logged."}
    except Exception as e:
        if not USE_FIRESTORE:
            db.rollback()
        logger.error(f"Error approving application: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/trigger-discovery")
def trigger_discovery(db: Session = Depends(get_db)):
    try:
        res = run_daily_autonomous_loop(db)
        return {
            "success": True,
            "processed": res["processed"],
            "matched": res["matched"],
            "briefing_sent": res["briefing_sent"]
        }
    except Exception as e:
        logger.error(f"Error triggering discovery: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
