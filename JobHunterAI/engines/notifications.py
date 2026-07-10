import os
import csv
import io
import smtplib
import datetime
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from sqlalchemy.orm import Session
from storage.db import JobOpportunityTable, ApplicationTable, ResumeVariantTable
from config import BASE_DIR, GEN_DIR, APPLY_THRESHOLD

logger = logging.getLogger("JobHunterAI.Notifications")

def get_job_funnel_stats(db: Session) -> dict:
    """Computes high-level conversion stats for the briefing."""
    total_jobs = db.query(JobOpportunityTable).count()
    matched_jobs = db.query(JobOpportunityTable).filter(JobOpportunityTable.overall_score >= APPLY_THRESHOLD).count()
    
    total_apps = db.query(ApplicationTable).count()
    interview_apps = db.query(ApplicationTable).filter(ApplicationTable.status == "Interview").count()
    offer_apps = db.query(ApplicationTable).filter(ApplicationTable.status == "Offer").count()
    
    interview_rate = round((interview_apps / total_apps * 100.0), 2) if total_apps > 0 else 0.0
    
    # Exclude applied to find queue pending review
    pending_review = db.query(JobOpportunityTable).filter(
        JobOpportunityTable.status == "discovered",
        JobOpportunityTable.overall_score >= APPLY_THRESHOLD
    ).count()
    
    # Identify popular technologies (trending skills) from matched JDs
    matched_opportunities = db.query(JobOpportunityTable).filter(
        JobOpportunityTable.overall_score >= APPLY_THRESHOLD
    ).limit(10).all()
    
    all_tech = []
    for opp in matched_opportunities:
        # Check standard tech words in description
        for tech in ["Docker", "Kubernetes", "AWS", "Terraform", "React", "PostgreSQL", "Redis", "FastAPI", "Python"]:
            if tech.lower() in opp.jd_text.lower():
                all_tech.append(tech)
                
    tech_counts = {}
    for t in all_tech:
        tech_counts[t] = tech_counts.get(t, 0) + 1
        
    trending_skills = sorted(tech_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    trending_labels = [s[0] for s in trending_skills]
    
    return {
        "total_jobs": total_jobs,
        "matched_jobs": matched_jobs,
        "pending_review": pending_review,
        "interview_apps": interview_apps,
        "offer_apps": offer_apps,
        "interview_rate": interview_rate,
        "trending_skills": trending_labels if trending_labels else ["Kubernetes", "AWS", "Terraform"]
    }

def generate_csv_report(db: Session) -> bytes:
    """Compiles all opportunities in the DB into a CSV byte string."""
    output = io.StringIO()
    writer = csv.writer(output)
    # Write headers
    writer.writerow([
        "Company", "Role", "Location", "Remote Status", 
        "Match Score", "Salary", "Source", "Direct Application Link", 
        "Notes", "Status"
    ])
    
    # Query all jobs
    jobs = db.query(JobOpportunityTable).order_by(JobOpportunityTable.overall_score.desc()).all()
    for j in jobs:
        remote_val = j.remote_status or "Unknown"
        score_val = f"{j.overall_score}%" if j.overall_score is not None else "N/A"
        salary_val = j.salary_range or "N/A"
        
        # Clean JD snippet for notes
        notes = (j.jd_text[:120].strip() + "...") if j.jd_text else ""
        clean_notes = notes.replace("\n", " ").replace("\r", "").replace(",", ";")
        
        writer.writerow([
            j.company_name,
            j.title,
            "Remote" if remote_val.lower() == "remote" else "Onsite/Hybrid",
            remote_val,
            score_val,
            salary_val,
            j.source or "Manual",
            j.url or "",
            clean_notes,
            j.status
        ])
        
    return output.getvalue().encode("utf-8")

def generate_html_report(db: Session) -> str:
    """Compiles dashboard analytics into a premium responsive HTML brief template."""
    stats = get_job_funnel_stats(db)
    today_str = datetime.date.today().strftime("%d %B %Y")
    
    # Fetch top matched jobs
    top_jobs = db.query(JobOpportunityTable).filter(
        JobOpportunityTable.overall_score >= APPLY_THRESHOLD
    ).order_by(JobOpportunityTable.overall_score.desc()).limit(3).all()
    
    jobs_list_html = ""
    for j in top_jobs:
        jobs_list_html += f"""
        <li style="margin-bottom: 12px; padding: 10px; border-left: 4px solid #4F46E5; background-color: #F9FAFB; list-style: none;">
            <strong style="color: #111827;">{j.title}</strong> at <span style="color: #4F46E5; font-weight: bold;">{j.company_name}</span><br/>
            <span style="font-size: 13px; color: #6B7280;"> Viability Match: <strong>{j.overall_score}%</strong> | Source: {j.source}</span>
        </li>
        """
        
    if not jobs_list_html:
        jobs_list_html = "<p style='color: #6B7280;'>No high-priority matches generated for today.</p>"
        
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>JobHunterAI Daily briefing</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #F3F4F6; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); margin: 0 auto; }}
            .header {{ background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%); color: #ffffff; padding: 24px; text-align: center; }}
            .content {{ padding: 24px; color: #374151; }}
            .stat-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 20px; }}
            .stat-card {{ background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 8px; padding: 16px; text-align: center; }}
            .stat-value {{ font-size: 24px; font-weight: bold; color: #4F46E5; }}
            .section-title {{ font-size: 18px; font-weight: bold; border-bottom: 2px solid #E5E7EB; padding-bottom: 6px; margin-top: 24px; color: #111827; }}
            .btn {{ display: block; width: 200px; margin: 20px auto 0; text-align: center; background: #4F46E5; color: #ffffff; padding: 12px; text-decoration: none; border-radius: 6px; font-weight: bold; }}
            .footer {{ background: #F9FAFB; color: #9CA3AF; font-size: 12px; text-align: center; padding: 16px; border-top: 1px solid #E5E7EB; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 style="margin: 0; font-size: 24px;">JobHunterAI Daily briefing</h1>
                <p style="margin: 4px 0 0; opacity: 0.9;">{today_str}</p>
            </div>
            <div class="content">
                <h3 style="margin-top: 0; color: #111827;">System Status Overview</h3>
                <div class="stat-grid">
                    <div class="stat-card">
                        <div class="stat-value">{stats['total_jobs']}</div>
                        <div style="font-size: 12px; color: #6B7280;">Jobs Discovered</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{stats['matched_jobs']}</div>
                        <div style="font-size: 12px; color: #6B7280;">Opportunities Matched</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{stats['pending_review']}</div>
                        <div style="font-size: 12px; color: #6B7280;">Awaiting Approval</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{stats['interview_rate']}%</div>
                        <div style="font-size: 12px; color: #6B7280;">Interview Conversion</div>
                    </div>
                </div>
                
                <div class="section-title">Top Active Opportunities</div>
                <ul style="padding: 0; margin-top: 10px;">
                    {jobs_list_html}
                </ul>
                
                <div class="section-title">Trending Missing Tech Stack Skills</div>
                <p style="margin-bottom: 5px; color: #374151;">Popular skills found in target openings today:</p>
                <div style="margin-top: 5px;">
                    {" ".join([f"<span style='background:#EEF2F6; color:#4F46E5; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; margin-right: 6px;'>{s}</span>" for s in stats['trending_skills']])}
                </div>
                
                <div class="section-title">Today's Action Items</div>
                <ul style="padding-left: 20px; color: #4b5563; font-size: 14px; line-height: 1.6;">
                    <li>Review the <strong>{stats['pending_review']}</strong> applications pending in your approval queue.</li>
                    <li>Verify cover letter formulations and click "Submit Application" to mark as applied.</li>
                    <li>Inspect the attached CSV spreadsheet for a detailed breakdown of all listings.</li>
                </ul>
                
                <a href="http://localhost:8501" class="btn">Open CRM Dashboard</a>
            </div>
            <div class="footer">
                JobHunterAI Persistent Career Agent &bull; Maximize ATS match & Factual Grounding
            </div>
        </div>
    </body>
    </html>
    """
    return html

def send_daily_briefing(db: Session) -> bool:
    """Generates HTML report, compiles CSV spreadsheet, and delivers them via SMTP."""
    html_content = generate_html_report(db)
    csv_content = generate_csv_report(db)
    
    # Read environment configs
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    try:
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
    except:
        smtp_port = 587
        
    smtp_user = os.getenv("SMTP_USERNAME")
    smtp_pass = os.getenv("SMTP_PASSWORD")
    recipient = os.getenv("RECIPIENT_EMAIL", smtp_user)
    
    today_str = datetime.date.today().strftime('%Y_%m_%d')
    today_html_filename = f"daily_briefing_{today_str}.html"
    today_csv_filename = f"job_listings_{today_str}.csv"
    
    report_file_path = GEN_DIR / today_html_filename
    csv_file_path = GEN_DIR / today_csv_filename
    
    # Save a local record for archiving
    try:
        with open(report_file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        logger.info(f"Daily briefing HTML saved to: {report_file_path}")
        
        with open(csv_file_path, "wb") as f:
            f.write(csv_content)
        logger.info(f"Daily listings CSV saved to: {csv_file_path}")
    except Exception as e:
        logger.error(f"Failed to write local briefing archives: {e}")
        
    if not (smtp_user and smtp_pass and recipient):
        logger.warning("SMTP credentials or recipient email missing from environment. Written to local files only (Offline Mode).")
        return False
        
    # Attempt SMTP transmission
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Attempting to send daily brief email (Attempt {attempt}/{max_retries})...")
            msg = MIMEMultipart("mixed")
            msg["Subject"] = f"JobHunterAI Daily Career Report — {datetime.date.today().strftime('%d %B')}"
            msg["From"] = smtp_user
            msg["To"] = recipient
            
            # Attach HTML Body
            body_part = MIMEText(html_content, "html")
            msg.attach(body_part)
            
            # Attach CSV Spreadsheet
            csv_part = MIMEBase("application", "octet-stream")
            csv_part.set_payload(csv_content)
            encoders.encode_base64(csv_part)
            csv_part.add_header(
                "Content-Disposition",
                f"attachment; filename={today_csv_filename}"
            )
            msg.attach(csv_part)
            
            with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(smtp_user, recipient, msg.as_string())
                
            logger.info("Daily brief email with CSV attachment delivered successfully!")
            return True
        except Exception as e:
            logger.warning(f"SMTP delivery attempt {attempt} failed: {e}")
            if attempt == max_retries:
                logger.error("All email delivery attempts failed. Falling back to local files.")
                
    return False

