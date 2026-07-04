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
            title_tag = soup.find("h2")
            title = title_tag.get_text().strip() if title_tag else "Backend Engineer"
            
            # Company
            # Lever pages typically have the logo or company name in page metadata or footer
            meta_title = soup.find("title")
            company = "Target Company"
            if meta_title:
                match = re.search(r"-\s*([^-\n]+)$", meta_title.get_text())
                if match:
                    company = match.group(1).strip()
            
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
            title_tag = soup.find("h1", class_="app-title")
            title = title_tag.get_text().strip() if title_tag else "Backend Engineer"
            
            # Company
            company_tag = soup.find("span", class_="company-name")
            company = company_tag.get_text().replace("at ", "").strip() if company_tag else "Target Company"
            
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
        # Fallback to generic URL or manual parse
        job_data = {
            "title": "Software Engineer",
            "company_name": "Tech Startup",
            "jd_text": f"Manual scrape from URL: {url}. Please configure requirements.",
            "url": url,
            "source": "Direct URL",
            "remote_status": "Remote"
        }
        
    db_job = JobOpportunityTable(
        title=job_data["title"],
        company_name=job_data["company_name"],
        jd_text=job_data["jd_text"],
        url=job_data["url"],
        source=job_data["source"],
        remote_status=job_data["remote_status"],
        status="discovered"
    )
    return save_job_opportunity(db, db_job)

def run_mock_discovery(db: Session) -> list:
    """Generate high-quality mock opportunities for testing and demonstration."""
    mock_jobs = [
        {
            "title": "Senior Backend Engineer",
            "company_name": "Stripe",
            "jd_text": """
            We are looking for a Senior Backend Engineer to join our core payments infrastructure team.
            Requirements:
            - 5+ years of experience building highly available, distributed systems.
            - Deep experience with Python, FastAPI, and PostgreSQL database optimizations.
            - Hands-on knowledge of Docker containers and Kubernetes orchestration.
            - Strong track record of designing latency-sensitive transaction gateways.
            - Familiarity with prompt routing and LLM infrastructures is a major plus.
            - Location: Remote
            """,
            "url": "https://jobs.lever.co/stripe/senior-backend-engineer",
            "source": "Lever",
            "remote_status": "Remote",
            "salary_range": "$160,000 - $210,000",
            "tech_stack": ["Python", "FastAPI", "PostgreSQL", "Docker", "LLM Routing"]
        },
        {
            "title": "Full Stack Developer",
            "company_name": "Y Combinator Startup",
            "jd_text": """
            Build the next generation AI coding assistant.
            Requirements:
            - React, TypeScript, FastAPI backend development.
            - Experience contributing to open-source software libraries.
            - Familiarity with YC workflows and fast-paced engineering environments.
            - Location: Hybrid
            """,
            "url": "https://boards.greenhouse.io/ycstartup/fullstack-developer",
            "source": "Greenhouse",
            "remote_status": "Hybrid",
            "salary_range": "$120,000 - $150,000 + Equity",
            "tech_stack": ["React", "FastAPI", "Python"]
        }
    ]
    
    db_jobs = []
    for job in mock_jobs:
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
