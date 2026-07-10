import os
import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger("JobHunterAI.Firestore")

USE_FIRESTORE = False
db_fs = None

# Look for credentials
firebase_creds_path = os.getenv("FIREBASE_SERVICE_ACCOUNT") or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if firebase_creds_path and os.path.exists(firebase_creds_path):
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
        
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_creds_path)
            firebase_admin.initialize_app(cred)
            
        db_fs = firestore.client()
        USE_FIRESTORE = True
        logger.info("Successfully connected to Firestore!")
    except Exception as e:
        logger.error(f"Failed to initialize Firestore client: {e}")
        USE_FIRESTORE = False

def get_candidate_fs(candidate_id: int = 1):
    if not USE_FIRESTORE:
         return None
    try:
        doc_ref = db_fs.collection("candidates").document(str(candidate_id))
        doc = doc_ref.get()
        if doc.exists:
             return doc.to_dict()
    except Exception as e:
         logger.error(f"Firestore get_candidate error: {e}")
    return None

def get_candidate_profile_data_fs(candidate_id: int = 1):
    if not USE_FIRESTORE:
         return None
    try:
        candidate_ref = db_fs.collection("candidates").document(str(candidate_id))
        candidate_doc = candidate_ref.get()
        if not candidate_doc.exists:
             return None
        candidate = candidate_doc.to_dict()
        
        # Read subcollections
        exps = [doc.to_dict() for doc in candidate_ref.collection("experiences").stream()]
        projs = [doc.to_dict() for doc in candidate_ref.collection("projects").stream()]
        skills = [doc.to_dict() for doc in candidate_ref.collection("skills").stream()]
        star_stories = [doc.to_dict() for doc in candidate_ref.collection("star_stories").stream()]
        
        # Format mapping compatibility
        return {
            "id": candidate_id,
            "name": candidate.get("name", ""),
            "email": candidate.get("email", ""),
            "phone": candidate.get("phone", ""),
            "github": candidate.get("github", ""),
            "linkedin": candidate.get("linkedin", ""),
            "website": candidate.get("website", ""),
            "experiences": exps,
            "projects": projs,
            "skills": skills,
            "star_stories": star_stories
        }
    except Exception as e:
         logger.error(f"Firestore get_profile error: {e}")
         return None

def get_all_jobs_fs():
    if not USE_FIRESTORE:
         return []
    try:
        jobs_ref = db_fs.collection("job_opportunities")
        stream = jobs_ref.stream()
        jobs = []
        for doc in stream:
             d = doc.to_dict()
             # Set primary key field compatible with DB id
             d["id"] = doc.id
             jobs.append(d)
        jobs.sort(key=lambda x: x.get("overall_score", 0.0) or 0.0, reverse=True)
        return jobs
    except Exception as e:
         logger.error(f"Firestore get_all_jobs error: {e}")
         return []

def get_job_fs(job_id: str):
    if not USE_FIRESTORE:
         return None
    try:
        doc_ref = db_fs.collection("job_opportunities").document(str(job_id))
        doc = doc_ref.get()
        if doc.exists:
             d = doc.to_dict()
             d["id"] = doc.id
             return d
    except Exception as e:
         logger.error(f"Firestore get_job error: {e}")
    return None

def save_job_opportunity_fs(job_dict: dict):
    if not USE_FIRESTORE:
         return None
    try:
        company = job_dict.get("company_name", "Unknown")
        title = job_dict.get("title", "Developer")
        # Generate stable, clean document key
        slug = f"{company.lower().replace(' ', '_')}_{title.lower().replace(' ', '_')}"
        doc_ref = db_fs.collection("job_opportunities").document(slug)
        doc_ref.set(job_dict, merge=True)
        job_dict["id"] = slug
        return job_dict
    except Exception as e:
         logger.error(f"Firestore save_job error: {e}")
         return None

def create_application_fs(app_dict: dict):
    if not USE_FIRESTORE:
         return None
    try:
        doc_ref = db_fs.collection("applications").document()
        app_dict["date_applied"] = datetime.now(timezone.utc).isoformat()
        doc_ref.set(app_dict)
        app_dict["id"] = doc_ref.id
        return app_dict
    except Exception as e:
         logger.error(f"Firestore create_application error: {e}")
         return None

def update_job_status_fs(job_id: str, status: str):
    if not USE_FIRESTORE:
         return None
    try:
        doc_ref = db_fs.collection("job_opportunities").document(str(job_id))
        doc_ref.update({"status": status})
        return True
    except Exception as e:
         logger.error(f"Firestore update_job_status error: {e}")
         return False

def get_stats_fs():
    if not USE_FIRESTORE:
         return {}
    try:
        jobs = get_all_jobs_fs()
        total_jobs = len(jobs)
        matched_jobs = len([j for j in jobs if (j.get("overall_score") or 0.0) >= 70.0])
        pending_review = len([j for j in jobs if j.get("status") == "discovered"])
        
        apps_ref = db_fs.collection("applications")
        apps = [doc.to_dict() for doc in apps_ref.stream()]
        total_apps = len(apps)
        
        interview_rate = 0.0
        if total_apps > 0:
             interviews = len([a for a in apps if a.get("status") == "Interview"])
             interview_rate = round((interviews / total_apps) * 100, 1)
             
        return {
            "total_jobs": total_jobs,
            "matched_jobs": matched_jobs,
            "pending_review": pending_review,
            "interview_rate": interview_rate
        }
    except Exception as e:
         logger.error(f"Firestore get_stats error: {e}")
         return {}
