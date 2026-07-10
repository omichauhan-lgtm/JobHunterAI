import json
import os
import datetime
from pathlib import Path
from sqlalchemy.orm import Session
from storage.db import JobOpportunityTable, ResumeVariantTable, ApplicationTable
from storage.crud import get_candidate_profile_data, create_resume_variant, create_application
from engines.company_intel import run_company_intelligence
from engines.ranking import compute_job_score, rank_projects, rank_experiences
from engines.compiler import render_resume, render_cover_letter, compile_latex_to_pdf
from engines.ats import run_ats_optimization
from engines.critic import run_truth_validation
from engines.cover_letter import generate_tailored_cover_letter
from engines.networking import generate_outreach_sequence
from config import logger, GEN_DIR, APPLY_THRESHOLD
from engines.discovery import run_mock_discovery
from engines.notifications import send_daily_briefing

def run_application_pipeline(db: Session, job_id: int, template_name: str = "backend.tex", mark_applied: bool = True) -> dict:
    """Coordinates the deterministic matching and LLM generation pipeline. If mark_applied is False, pre-compiles assets but leaves status as discovered for human review."""
    # 1. Fetch Candidate Knowledge Graph
    logger.info("Stage 1: Fetching Candidate Career Graph from database...")
    profile = get_candidate_profile_data(db, candidate_id=1)
    if not profile:
        return {"success": False, "error": "Candidate profile not found in database. Seed the database first."}

    # 2. Fetch Job Details
    job = db.query(JobOpportunityTable).filter(JobOpportunityTable.id == job_id).first()
    if not job:
        return {"success": False, "error": f"Job opportunity {job_id} not found."}
        
    logger.info(f"Processing job application for {job.title} at {job.company_name}...")

    # 3. Retrieve Company Intelligence
    logger.info("Stage 2: Gaining Company Intelligence...")
    company_profile = run_company_intelligence(job.company_name, job.jd_text)

    # 4. Deterministic Ranking & Scoring
    logger.info("Stage 3: Running matching scoring rules...")
    flat_skills = [s["name"] for s in profile["skills"]]
    match_score = compute_job_score(
        job_jd=job.jd_text,
        job_title=job.title,
        company_yc=company_profile.is_yc,
        remote_status=job.remote_status,
        candidate_skills=flat_skills
    )
    job.overall_score = match_score
    db.commit()
    logger.info(f"Job viability match score: {match_score}%")

    if match_score < APPLY_THRESHOLD:
         logger.warning(f"Job score {match_score}% is below threshold {APPLY_THRESHOLD}%. Halting pipeline.")
         return {
             "success": False, 
             "error": f"Job fit score ({match_score}%) is below the configured threshold ({APPLY_THRESHOLD}%)."
         }

    # 5. Extract ATS Keywords
    job_keywords = company_profile.tech_stack if company_profile.tech_stack else flat_skills[:5]

    # Rank candidate projects & experiences
    top_projects = rank_projects(profile["projects"], job_keywords, job.title)
    top_experiences = rank_experiences(profile["experiences"], job_keywords, job.title)

    # Compile initial resume data
    tailored_resume_data = {
        "name": profile["name"],
        "email": profile["email"],
        "phone": profile["phone"],
        "github": profile["github"],
        "linkedin": profile["linkedin"],
        "experiences": top_experiences[:2], 
        "projects": top_projects[:2]
    }

    # 6. ATS Optimization Loop (Iterative Bullet Rewriter)
    logger.info("Stage 4: Running ATS Optimization loop...")
    all_bullets = []
    for exp in tailored_resume_data["experiences"]:
        all_bullets.extend(exp["bullets"])
    for proj in tailored_resume_data["projects"]:
        all_bullets.extend(proj["description_bullets"])
        
    ats_results = run_ats_optimization(all_bullets, job_keywords)
    optimized_bullets = ats_results["optimized_bullets"]
    
    # Distribute optimized bullets back
    bullet_idx = 0
    for exp in tailored_resume_data["experiences"]:
        num_bullets = len(exp["bullets"])
        # Slice safely
        if bullet_idx + num_bullets <= len(optimized_bullets):
            exp["bullets"] = optimized_bullets[bullet_idx : bullet_idx + num_bullets]
        bullet_idx += num_bullets
        
    for proj in tailored_resume_data["projects"]:
        num_bullets = len(proj["description_bullets"])
        if bullet_idx + num_bullets <= len(optimized_bullets):
            proj["description_bullets"] = optimized_bullets[bullet_idx : bullet_idx + num_bullets]
        bullet_idx += num_bullets

    # 7. Truth Validation Engine (AI Critic + Programmatic Rules)
    logger.info("Stage 5: Verifying claims against career graph evidence log...")
    critic_report = run_truth_validation(tailored_resume_data, profile)
    if not critic_report["passed"]:
        logger.error(f"Truth Validation Failed: {critic_report['errors']}")
        return {
            "success": False,
            "error": "Truth validation checks failed.",
            "report": critic_report
        }
    logger.info("Truth validation passed successfully.")

    # Categorize skills for LaTeX template
    skills_cat = {"Languages": [], "Frameworks": [], "Databases": [], "Tools": []}
    for s in profile["skills"]:
        cat = s["category"]
        if cat in ["Languages", "Frameworks", "Databases"]:
            skills_cat[cat].append(s["name"])
        else:
            skills_cat["Tools"].append(s["name"])

    # 8. Resume Compile & Render
    logger.info("Stage 6: Rendering LaTeX resume template...")
    latex_src = render_resume(tailored_resume_data, skills_cat, template_name)
    
    # Save variant to DB
    variant = create_resume_variant(db, candidate_id=1, resume_type=template_name.replace(".tex", ""), latex_source=latex_src)

    # Write files to disk
    safe_company_name = job.company_name.replace(" ", "_")
    tex_filename = f"{safe_company_name}_resume_v{variant.version}.tex"
    tex_path = GEN_DIR / tex_filename
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(latex_src)
        
    compile_latex_to_pdf(str(tex_path))

    # 9. Generate Cover Letter & Outreach sequence
    logger.info("Stage 7: Drafting Cover Letter...")
    cl_body = generate_tailored_cover_letter(profile, {"title": job.title, "company_name": job.company_name}, company_profile)
    cl_content = render_cover_letter(
        profile["name"], job.company_name, cl_body, 
        {"email": profile["email"], "phone": profile["phone"], "github": profile["github"], "linkedin": profile["linkedin"]}
    )
    cl_path = GEN_DIR / f"{safe_company_name}_cover_letter.md"
    with open(cl_path, "w", encoding="utf-8") as f:
        f.write(cl_content)

    logger.info("Stage 8: Generating outreach connection sequences...")
    outreach = generate_outreach_sequence({"title": job.title, "company_name": job.company_name}, company_profile)
    outreach_path = GEN_DIR / f"{safe_company_name}_outreach.txt"
    with open(outreach_path, "w", encoding="utf-8") as f:
        f.write(f"LINKEDIN CONNECTION NOTE:\n{outreach['linkedin_note']}\n\nFOLLOW-UP MESSAGE:\n{outreach['follow_up_message']}")

    # 9. Generate Explainability Metadata report
    logger.info("Stage 9: Generating platform explainability metadata report...")
    explainability_data = {
        "job_title": job.title,
        "company_name": job.company_name,
        "date_processed": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "decision_parameters": {
            "job_fit_score": match_score,
            "apply_threshold": APPLY_THRESHOLD,
            "template_selected": template_name,
            "keywords_integrated": job_keywords
        },
        "experience_selection": {
            "selected": [
                {
                    "company": exp["company"],
                    "role": exp["role"],
                    "reason": "Top tech stack match and seniority overlap."
                } for exp in tailored_resume_data["experiences"]
            ],
            "rejected": [
                {
                    "company": exp["company"],
                    "role": exp["role"],
                    "reason": "Exceeded maximum section limit of 2 entries."
                } for exp in profile["experiences"] if exp["company"] not in [se["company"] for se in tailored_resume_data["experiences"]]
            ]
        },
        "project_selection": {
            "selected": [
                {
                    "name": proj["name"],
                    "reason": "Highest matching keyword overlap index."
                } for proj in tailored_resume_data["projects"]
            ],
            "rejected": [
                {
                    "name": proj["name"],
                    "reason": "Lower skills alignment than selected project nodes."
                } for proj in profile["projects"] if proj["name"] not in [sp["name"] for sp in tailored_resume_data["projects"]]
            ]
        },
        "ats_score_comparison": {
            "initial_percent": ats_results.get("initial_score", 0.0),
            "final_percent": ats_results.get("final_score", 0.0),
            "iterations_run": ats_results.get("iterations", 0)
        },
        "evidence_trace_links": [
            {
                "source": item.get("company") or item.get("name"),
                "evidence_descriptions": [ev["description"] for ev in item.get("evidence", [])]
            } for item in tailored_resume_data["experiences"] + tailored_resume_data["projects"]
        ]
    }
    
    exp_path = GEN_DIR / f"{safe_company_name}_explainability.json"
    with open(exp_path, "w", encoding="utf-8") as f:
        json.dump(explainability_data, f, indent=2)

    # 10. Record Application Details (only if mark_applied is true to preserve human-in-the-loop review)
    if mark_applied:
        logger.info("Stage 10: Logging application details in SQLite CRM...")
        app = ApplicationTable(
            candidate_id=1,
            job_id=job.id,
            resume_variant_id=variant.id,
            cover_letter_path=str(cl_path),
            outreach_sequence_path=str(outreach_path),
            status="Applied"
        )
        create_application(db, app)
        job.status = "applied"
        db.commit()
        logger.info(f"Application recorded successfully for {job.company_name}!")
    else:
        logger.info(f"Assets auto-tailored for {job.company_name}. Leaving status as discovered for human review.")
    
    return {
        "success": True,
        "resume_variant_id": variant.id,
        "resume_path": str(tex_path),
        "cover_letter_path": str(cl_path),
        "outreach_path": str(outreach_path),
        "explainability_path": str(exp_path),
        "critic_warnings": critic_report["warnings"]
    }

def run_daily_autonomous_loop(db: Session) -> dict:
    """Runs the daily autonomous career pipeline: Discover -> Rank -> Prep -> Report."""
    logger.info("Starting Daily Autonomous Pipeline Loop...")
    
    # 1. Discover new jobs
    logger.info("Executing job discovery connectors...")
    new_jobs = run_mock_discovery(db)
    logger.info(f"Discovered {len(new_jobs)} opportunities.")
    
    # 2. Score and Rank jobs
    profile = get_candidate_profile_data(db, candidate_id=1)
    if not profile:
        logger.error("No candidate profile found. Loop halted.")
        return {"success": False, "error": "No candidate profile found."}
        
    flat_skills = [s["name"] for s in profile["skills"]]
    
    processed_count = 0
    matched_count = 0
    
    discovered_jobs = db.query(JobOpportunityTable).filter(JobOpportunityTable.status == "discovered").all()
    for job in discovered_jobs:

            
        # Get company intelligence
        company_profile = run_company_intelligence(job.company_name, job.jd_text)
        
        # Calculate suitability score (using our tier logic)
        score = compute_job_score(
            job_jd=job.jd_text,
            job_title=job.title,
            company_yc=company_profile.is_yc,
            remote_status=job.remote_status,
            candidate_skills=flat_skills
        )
        
        job.overall_score = score
        processed_count += 1
        
        if score >= APPLY_THRESHOLD:
            matched_count += 1
            # Auto-prepare candidate resume variant and cover letter draft if not already generated
            app_exists = db.query(ApplicationTable).filter(ApplicationTable.job_id == job.id).first()
            if not app_exists:
                try:
                    logger.info(f"Auto-tailoring assets for matched opportunity: {job.title} at {job.company_name} (Score: {score}%)")
                    run_application_pipeline(db, job.id, mark_applied=False)
                except Exception as e:
                    logger.error(f"Error tailoring assets during daily loop: {e}")
                    
    db.commit()
    
    # 3. Generate and deliver report
    logger.info("Compiling and sending Daily Briefing...")
    sent = send_daily_briefing(db)
    
    return {
        "success": True,
        "processed": processed_count,
        "matched": matched_count,
        "briefing_sent": sent
    }


