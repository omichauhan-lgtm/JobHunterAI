import urllib.request
import re
import json
import logging
from bs4 import BeautifulSoup
from storage.db import JobOpportunityTable
from storage.crud import save_job_opportunity
from sqlalchemy.orm import Session
from config import logger

def clean_html(html_content: str) -> str:
    """Helper to convert HTML to clean, readable text."""
    soup = BeautifulSoup(html_content, "html.parser")
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    # Get text
    text = soup.get_text()
    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Drop blank lines
    return "\n".join(chunk for chunk in chunks if chunk)

def parse_lever_job(url: str) -> dict:
    """Fetch and parse a public Lever job page."""
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            soup = BeautifulSoup(html, "html.parser")
            
            # Title
            title_tag = soup.find("h2") or soup.find("h1")
            if not title_tag:
                logger.warning(f"Lever title element not found for {url}. Posting may have expired.")
                return None
            title = title_tag.get_text().strip()
            if any(term in title.lower() for term in ["current openings", "jobs at", "open positions", "openings at"]):
                logger.warning(f"URL redirected to company index page: {title}. Posting may have expired.")
                return None
            
            # Company parsed deterministically from Lever URL slug
            company = "Target Company"
            if "lever.co/" in url:
                try:
                    company = url.split("lever.co/")[1].split("/")[0].capitalize()
                except:
                    pass
            
            # JD Description
            jd_text = clean_html(html)
            
            return {
                "title": title,
                "company_name": company,
                "jd_text": jd_text,
                "url": url,
                "source": "Lever",
                "remote_status": "Remote" if "remote" in jd_text.lower() else "Onsite"
            }
    except Exception as e:
        logger.error(f"Error parsing Lever job: {e}")
        return None

def parse_greenhouse_job(url: str) -> dict:
    """Fetch and parse a public Greenhouse job page."""
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            soup = BeautifulSoup(html, "html.parser")
            
            # Title
            title_tag = soup.find("h1", class_="app-title") or soup.find("h1", class_="section-header") or soup.find("h1")
            if not title_tag:
                logger.warning(f"Greenhouse title element not found for {url}. Posting may have expired.")
                return None
            title = title_tag.get_text().strip()
            if any(term in title.lower() for term in ["current openings", "jobs at", "open positions", "openings at"]):
                logger.warning(f"URL redirected to company index page: {title}. Posting may have expired.")
                return None
            
            # Company parsed deterministically from Greenhouse URL slug
            company = "Target Company"
            if "greenhouse.io/" in url:
                try:
                    company = url.split("greenhouse.io/")[1].split("/")[0].capitalize()
                except:
                    pass
            
            # JD Description
            jd_text = clean_html(html)
            
            return {
                "title": title,
                "company_name": company,
                "jd_text": jd_text,
                "url": url,
                "source": "Greenhouse",
                "remote_status": "Remote" if "remote" in jd_text.lower() else "Onsite"
            }
    except Exception as e:
        logger.error(f"Error parsing Greenhouse job: {e}")
        return None

def discover_job_from_url(db: Session, url: str) -> JobOpportunityTable:
    """Ingest a job from a URL, parse it, and write it to the database."""
    job_data = None
    if "lever.co" in url:
        job_data = parse_lever_job(url)
    elif "greenhouse.io" in url:
        job_data = parse_greenhouse_job(url)
        
    if not job_data:
        logger.error(f"Failed to parse active job details from URL: {url} (Page may be expired, redirected, or invalid)")
        return None
        
    db_job = JobOpportunityTable(
        title=job_data["title"],
        company_name=job_data["company_name"],
        jd_text=job_data["jd_text"],
        url=job_data["url"],
        source=job_data["source"],
        remote_status=job_data["remote_status"],
        status="discovered"
    )
    
    # Calculate fit score immediately upon ingestion
    from engines.ranking import compute_job_score
    from storage.crud import get_candidate
    candidate = get_candidate(db, 1)
    if candidate:
        skills_list = [s.name for s in candidate.skills]
        db_job.overall_score = compute_job_score(
            db_job.jd_text,
            db_job.title,
            False,
            db_job.remote_status,
            skills_list
        )
    else:
        db_job.overall_score = 50
        
    return save_job_opportunity(db, db_job)

def discover_arbeitnow_jobs(db: Session) -> list:
    """Fetch and ingest real remote software engineering jobs from Arbeitnow public API."""
    import urllib.request
    import json
    
    url = "https://www.arbeitnow.com/api/job-board-api"
    try:
        logger.info("Querying Arbeitnow API for live remote engineering roles...")
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            jobs_list = res_data.get("data", [])
            
            db_jobs = []
            for j in jobs_list:
                title = j.get("title", "Software Engineer")
                company = j.get("company_name", "Unknown Company")
                description = clean_html(j.get("description", ""))
                job_url = j.get("url", "")
                tags = j.get("tags", [])
                
                # Filter for target developer roles
                keywords = ["engineer", "developer", "software", "backend", "fullstack", "data", "analytics", "ai", "machine learning"]
                if not any(k in title.lower() for k in keywords):
                    continue
                    
                # Ensure remote
                is_remote = j.get("remote", False) or "remote" in title.lower() or "remote" in description.lower()
                if not is_remote:
                    continue
                
                # Deduplicate
                existing = db.query(JobOpportunityTable).filter(JobOpportunityTable.url == job_url).first()
                if existing:
                    continue
                    
                db_job = JobOpportunityTable(
                    title=title,
                    company_name=company,
                    jd_text=description,
                    url=job_url,
                    source="Arbeitnow API",
                    remote_status="Remote",
                    tech_stack_json=json.dumps(tags),
                    status="discovered"
                )
                
                # Dynamic scoring
                from engines.ranking import compute_job_score
                from storage.crud import get_candidate
                candidate = get_candidate(db, 1)
                if candidate:
                    skills_list = [s.name for s in candidate.skills]
                    score = compute_job_score(
                        db_job.jd_text,
                        db_job.title,
                        False,
                        db_job.remote_status,
                        skills_list
                    )
                    db_job.overall_score = score
                else:
                    db_job.overall_score = 50
                    
                saved = save_job_opportunity(db, db_job)
                db_jobs.append(saved)
                
            logger.info(f"Arbeitnow Scraper complete. Ingested {len(db_jobs)} matching remote tech roles.")
            return db_jobs
    except Exception as e:
        logger.error(f"Failed to scrape Arbeitnow API: {e}")
        return None

def run_mock_discovery(db: Session) -> list:
    """Run real API discovery first, and fallback to mock list for demo robustness."""
    real_jobs = discover_arbeitnow_jobs(db)
    if real_jobs is not None:
        return real_jobs
        
    # Mock fallback
    mock_jobs = [
        {
            "title": "Senior Backend Engineer",
            "company_name": "Stripe",
            "jd_text": """
            We are looking for a Senior Backend Engineer to join our payments infra team.
            Requirements: FastAPI, Python, PostgreSQL, Docker, Kubernetes, prompt routing.
            """,
            "url": "https://jobs.lever.co/stripe/senior-backend-engineer",
            "source": "Lever",
            "remote_status": "Remote",
            "salary_range": "$160,000 - $210,000",
            "tech_stack": ["Python", "FastAPI", "PostgreSQL", "Docker", "LLM Routing"]
        }
    ]
    
    db_jobs = []
    for job in mock_jobs:
        # Deduplicate
        existing = db.query(JobOpportunityTable).filter(JobOpportunityTable.url == job["url"]).first()
        if existing:
            db_jobs.append(existing)
            continue
            
        db_job = JobOpportunityTable(
            title=job["title"],
            company_name=job["company_name"],
            jd_text=job["jd_text"],
            url=job["url"],
            source=job["source"],
            salary_range=job.get("salary_range"),
            remote_status=job["remote_status"],
            tech_stack_json=json.dumps(job.get("tech_stack", [])),
            status="discovered"
        )
        saved = save_job_opportunity(db, db_job)
        db_jobs.append(saved)
        
    return db_jobs

