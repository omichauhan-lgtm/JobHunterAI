import json
from sqlalchemy.orm import Session
from sqlalchemy import func
from .db import (
    CandidateTable, ExperienceTable, ProjectTable, SkillTable, 
    EvidenceTable, STARStoryTable, JobOpportunityTable, 
    ResumeVariantTable, ApplicationTable, RecruiterCRMTable, 
    RelationshipTable, init_db
)
from models.schemas import MasterProfile
from .firestore_db import (
    USE_FIRESTORE,
    get_candidate_fs,
    get_candidate_profile_data_fs,
    get_all_jobs_fs,
    get_job_fs,
    save_job_opportunity_fs,
    create_application_fs,
    update_job_status_fs,
    get_stats_fs
)

def get_candidate(db: Session, candidate_id: int = 1):
    if USE_FIRESTORE:
        return get_candidate_fs(candidate_id)
    return db.query(CandidateTable).filter(CandidateTable.id == candidate_id).first()

def get_candidate_profile_data(db: Session, candidate_id: int = 1):
    """Retrieve full candidate knowledge graph as standard dictionary/JSON structure."""
    if USE_FIRESTORE:
        return get_candidate_profile_data_fs(candidate_id)
    candidate = get_candidate(db, candidate_id)
    if not candidate:
        return None
    
    experiences = []
    for exp in candidate.experiences:
        experiences.append({
            "id": exp.id,
            "company": exp.company,
            "role": exp.role,
            "org_type": exp.org_type,
            "is_open_source": exp.is_open_source,
            "start_date": exp.start_date,
            "end_date": exp.end_date,
            "bullets": json.loads(exp.bullets_json),
            "skills": json.loads(exp.skills_json),
            "evidence": [{
                "id": ev.id,
                "type": ev.type,
                "description": ev.description,
                "url": ev.url,
                "metrics": ev.metrics
            } for ev in exp.evidence]
        })
        
    projects = []
    for proj in candidate.projects:
        projects.append({
            "id": proj.id,
            "name": proj.name,
            "category": proj.category,
            "description_bullets": json.loads(proj.description_json),
            "skills": json.loads(proj.skills_json),
            "github_url": proj.github_url,
            "evidence": [{
                "id": ev.id,
                "type": ev.type,
                "description": ev.description,
                "url": ev.url,
                "metrics": ev.metrics
            } for ev in proj.evidence]
        })

    skills = [{"name": s.name, "category": s.category} for s in candidate.skills]
    
    star_stories = [{
        "project_or_company": st.project_or_company,
        "situation": st.situation,
        "task": st.task,
        "action": st.action,
        "result": st.result
    } for st in candidate.star_stories]

    return {
        "id": candidate.id,
        "name": candidate.name,
        "email": candidate.email,
        "phone": candidate.phone,
        "github": candidate.github,
        "linkedin": candidate.linkedin,
        "website": candidate.website,
        "experiences": experiences,
        "projects": projects,
        "skills": skills,
        "star_stories": star_stories
    }

def import_master_profile(db: Session, profile: MasterProfile):
    """Seed the database with a Pydantic MasterProfile. Clears existing data first."""
    # Clear existing candidate records for ID=1 to enable simple re-seeding
    db.query(CandidateTable).filter(CandidateTable.id == 1).delete(synchronize_session=False)
    db.query(ExperienceTable).filter(ExperienceTable.candidate_id == 1).delete(synchronize_session=False)
    db.query(ProjectTable).filter(ProjectTable.candidate_id == 1).delete(synchronize_session=False)
    db.query(SkillTable).filter(SkillTable.candidate_id == 1).delete(synchronize_session=False)
    db.query(EvidenceTable).filter(EvidenceTable.candidate_id == 1).delete(synchronize_session=False)
    db.query(STARStoryTable).filter(STARStoryTable.candidate_id == 1).delete(synchronize_session=False)
    db.query(RelationshipTable).delete(synchronize_session=False)
    db.commit()

    # Create candidate
    candidate = CandidateTable(
        id=1,
        name=profile.name,
        email=profile.email,
        phone=profile.phone,
        github=profile.github,
        linkedin=profile.linkedin,
        website=profile.website
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    # Insert Skills
    for s in profile.skills:
        skill_db = SkillTable(candidate_id=1, name=s.name, category=s.category)
        db.add(skill_db)
    
    # Insert Experiences
    for exp in profile.experiences:
        exp_db = ExperienceTable(
            candidate_id=1,
            company=exp.company,
            role=exp.role,
            org_type=exp.org_type,
            is_open_source=exp.is_open_source,
            bullets_json=json.dumps(exp.bullets),
            skills_json=json.dumps(exp.skills)
        )
        db.add(exp_db)
        db.commit()
        db.refresh(exp_db)

        # Insert Evidence for Experience
        for ev in exp.evidence:
            ev_db = EvidenceTable(
                candidate_id=1,
                experience_id=exp_db.id,
                type=ev.type,
                description=ev.description,
                url=ev.url,
                metrics=ev.metrics
            )
            db.add(ev_db)
            db.commit()
            
            # Map Relationship
            rel = RelationshipTable(
                source_type="Evidence", source_id=ev_db.id,
                target_type="Experience", target_id=exp_db.id,
                rel_type="demonstrated_by"
            )
            db.add(rel)
            
        db.commit()

    # Insert Projects
    for proj in profile.projects:
        proj_db = ProjectTable(
            candidate_id=1,
            name=proj.name,
            category=proj.category,
            description_json=json.dumps(proj.description_bullets),
            skills_json=json.dumps(proj.skills),
            github_url=proj.github_url
        )
        db.add(proj_db)
        db.commit()
        db.refresh(proj_db)

        # Insert Evidence for Project
        for ev in proj.evidence:
            ev_db = EvidenceTable(
                candidate_id=1,
                project_id=proj_db.id,
                type=ev.type,
                description=ev.description,
                url=ev.url,
                metrics=ev.metrics
            )
            db.add(ev_db)
            db.commit()

            # Map Relationship
            rel = RelationshipTable(
                source_type="Evidence", source_id=ev_db.id,
                target_type="Project", target_id=proj_db.id,
                rel_type="demonstrated_by"
            )
            db.add(rel)
            
        db.commit()

    # Insert STAR Stories
    for st in profile.star_stories:
        st_db = STARStoryTable(
            candidate_id=1,
            project_or_company=st.project_or_company,
            situation=st.situation,
            task=st.task,
            action=st.action,
            result=st.result
        )
        db.add(st_db)
    
    db.commit()

def save_job_opportunity(db: Session, job: JobOpportunityTable) -> JobOpportunityTable:
    """Save or update discovered job opportunity."""
    if USE_FIRESTORE:
        job_dict = {
            "title": job.title,
            "company_name": job.company_name,
            "jd_text": job.jd_text,
            "url": job.url,
            "source": job.source,
            "salary_range": job.salary_range,
            "remote_status": job.remote_status,
            "tech_stack_json": job.tech_stack_json or "[]",
            "requirements_json": job.requirements_json or "[]",
            "ats_keywords_json": job.ats_keywords_json or "[]",
            "overall_score": job.overall_score or 0.0,
            "status": job.status or "discovered"
        }
        saved_dict = save_job_opportunity_fs(job_dict)
        if saved_dict:
            job.id = saved_dict.get("id")
        return job

    existing = db.query(JobOpportunityTable).filter(
        JobOpportunityTable.company_name == job.company_name,
        JobOpportunityTable.title == job.title
    ).first()
    if existing:
        existing.jd_text = job.jd_text
        existing.url = job.url
        existing.source = job.source
        existing.salary_range = job.salary_range
        existing.remote_status = job.remote_status
        existing.tech_stack_json = job.tech_stack_json
        existing.requirements_json = job.requirements_json
        existing.ats_keywords_json = job.ats_keywords_json
        existing.overall_score = job.overall_score
        db.commit()
        db.refresh(existing)
        return existing
    else:
        db.add(job)
        db.commit()
        db.refresh(job)
        return job

def get_next_resume_version(db: Session, candidate_id: int, resume_type: str) -> int:
    """Compute the next version number for resume variants."""
    max_ver = db.query(func.max(ResumeVariantTable.version)).filter(
        ResumeVariantTable.candidate_id == candidate_id,
        ResumeVariantTable.resume_type == resume_type
    ).scalar()
    return (max_ver or 0) + 1

def create_resume_variant(db: Session, candidate_id: int, resume_type: str, latex_source: str) -> ResumeVariantTable:
    version = get_next_resume_version(db, candidate_id, resume_type)
    variant = ResumeVariantTable(
        candidate_id=candidate_id,
        version=version,
        resume_type=resume_type,
        latex_source=latex_source
    )
    db.add(variant)
    db.commit()
    db.refresh(variant)
    return variant

def create_application(db: Session, app: ApplicationTable) -> ApplicationTable:
    if USE_FIRESTORE:
        app_dict = {
            "candidate_id": app.candidate_id,
            "job_id": app.job_id,
            "resume_variant_id": app.resume_variant_id,
            "cover_letter_path": app.cover_letter_path,
            "outreach_sequence_path": app.outreach_sequence_path,
            "status": app.status,
            "experiment_group": app.experiment_group,
            "outcomes_log": app.outcomes_log,
            "compensation_details": app.compensation_details
        }
        saved = create_application_fs(app_dict)
        if saved:
            app.id = saved.get("id")
        return app
    db.add(app)
    db.commit()
    db.refresh(app)
    return app

def update_application_status(db: Session, application_id: int, status: str):
    if USE_FIRESTORE:
        try:
            from .firestore_db import db_fs
            db_fs.collection("applications").document(str(application_id)).update({"status": status})
        except:
            pass
        return None
    app = db.query(ApplicationTable).filter(ApplicationTable.id == application_id).first()
    if app:
        app.status = status
        db.commit()
    return app

def save_recruiter_interaction(db: Session, application_id: int, name: str, title: str, contact_info: str, message: dict):
    crm = db.query(RecruiterCRMTable).filter(RecruiterCRMTable.application_id == application_id).first()
    if crm:
        history = json.loads(crm.message_history_json)
        history.append(message)
        crm.message_history_json = json.dumps(history)
        crm.last_interacted = func.now()
    else:
        crm = RecruiterCRMTable(
            application_id=application_id,
            name=name,
            title=title,
            contact_info=contact_info,
            message_history_json=json.dumps([message])
        )
        db.add(crm)
    db.commit()
    db.refresh(crm)
    return crm

def get_application_analytics(db: Session):
    """Retrieve funnel statistics for the dashboard."""
    if USE_FIRESTORE:
        stats = get_stats_fs()
        return {
            "total_applications": stats.get("total_jobs", 0),
            "funnel": {"Applied": stats.get("total_jobs", 0)},
            "response_rate_percent": stats.get("interview_rate", 0.0)
        }
    total_apps = db.query(func.count(ApplicationTable.id)).scalar() or 0
    funnel = db.query(ApplicationTable.status, func.count(ApplicationTable.id)).group_by(ApplicationTable.status).all()
    funnel_dict = {status: count for status, count in funnel}
    
    # Calculate response rate (any state beyond 'Applied')
    non_applied = sum([count for status, count in funnel if status not in ('Applied', 'Discovered')])
    response_rate = (non_applied / total_apps * 100) if total_apps > 0 else 0.0

    return {
        "total_applications": total_apps,
        "funnel": funnel_dict,
        "response_rate_percent": response_rate
    }

def get_all_job_opportunities(db: Session):
    if USE_FIRESTORE:
        fs_jobs = get_all_jobs_fs()
        job_objects = []
        for j in fs_jobs:
            job_obj = JobOpportunityTable(
                title=j.get("title", ""),
                company_name=j.get("company_name", ""),
                jd_text=j.get("jd_text", ""),
                url=j.get("url", ""),
                source=j.get("source", ""),
                salary_range=j.get("salary_range"),
                remote_status=j.get("remote_status", "Remote"),
                overall_score=j.get("overall_score", 0.0),
                status=j.get("status", "discovered")
            )
            job_obj.id = j.get("id")
            job_objects.append(job_obj)
        return job_objects
    return db.query(JobOpportunityTable).order_by(JobOpportunityTable.overall_score.desc()).all()

def get_job_opportunity_by_id(db: Session, job_id: str):
    if USE_FIRESTORE:
        j = get_job_fs(job_id)
        if not j:
            return None
        job_obj = JobOpportunityTable(
            title=j.get("title", ""),
            company_name=j.get("company_name", ""),
            jd_text=j.get("jd_text", ""),
            url=j.get("url", ""),
            source=j.get("source", ""),
            salary_range=j.get("salary_range"),
            remote_status=j.get("remote_status", "Remote"),
            overall_score=j.get("overall_score", 0.0),
            status=j.get("status", "discovered")
        )
        job_obj.id = j.get("id")
        return job_obj
    try:
        id_val = int(job_id)
    except:
        return None
    return db.query(JobOpportunityTable).filter(JobOpportunityTable.id == id_val).first()
