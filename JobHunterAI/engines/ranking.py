import json
import re

def compute_job_score(job_jd: str, job_title: str, company_yc: bool, remote_status: str, candidate_skills: list) -> float:
    """
    Deterministically computes a suitability score (0-100) for a job opportunity.
    Formula balances:
    - Skill Match (50% weight)
    - Remote Fit (20% weight)
    - Startup/YC Preference (15% weight)
    - Seniority/Role alignment (15% weight)
    Multiplied by Job Tier:
    - Tier 1 (1.2x): AI Infrastructure, Dev tools, SaaS, YC
    - Tier 2 (1.0x): Remote-first Fintech/Data
    - Tier 3 (0.7x): Large Enterprise Corporate
    """
    score = 0.0
    jd_lower = job_jd.lower()
    
    # 1. Skill Match (up to 50 points)
    matched_skills = 0
    for skill in candidate_skills:
        # Check word boundaries for clean matching
        pattern = rf"\b{re.escape(skill.lower())}\b"
        if re.search(pattern, jd_lower):
            matched_skills += 1
            
    # Scale matching score without penalizing extra candidate skills: 5+ matching skills gets 50 points
    score += min(matched_skills, 5) / 5.0 * 50.0

    
    # 2. Remote Fit (up to 20 points)
    if remote_status.lower() == "remote":
        score += 20.0
    elif remote_status.lower() == "hybrid":
        score += 10.0
    else:
        score += 5.0 # Onsite has lower weight
        
    # 3. Company Quality & YC backing (up to 15 points)
    if company_yc:
        score += 15.0
    else:
        score += 5.0

    # 4. Seniority & Experience Alignment (up to 15 points, with compatibility penalty)
    title_lower = job_title.lower()
    is_senior_role = any(w in title_lower for w in ["senior", "sr.", "staff", "lead", "principal", "architect"])
    
    requires_high_exp = False
    exp_matches = re.findall(r"(\d+)\+?\s*years?", jd_lower)
    for match in exp_matches:
        years = int(match)
        if years >= 3:
            requires_high_exp = True
            break
            
    if is_senior_role or requires_high_exp:
        score -= 30.0 # Heavy deduction to filter out senior roles below threshold
    else:
        score += 15.0 # Full alignment for junior/mid-level roles

    # 5. Remote Job Stratification (Tiers)
    tier = 2 # default
    is_tier1 = company_yc or any(w in jd_lower for w in ["ai infrastructure", "developer tooling", "dev tools", "saas", "seed startup", "early stage"])
    is_tier3 = any(w in jd_lower for w in ["fortune 500", "large enterprise", "corporation", "enterprise scale"])
    
    if is_tier1:
        tier = 1
    elif is_tier3:
        tier = 3
        
    multiplier = 1.0
    if tier == 1:
        multiplier = 1.2
    elif tier == 3:
        multiplier = 0.7
        
    # 6. Remote-Readiness Competency Boost (up to 5 points)
    remote_competency_terms = ["async", "asynchronous", "self-starter", "self-motivated", "documentation", "independent", "autonomous", "written communication", "git workflow"]
    if any(w in jd_lower for w in remote_competency_terms):
        has_distributed_stack = any(s in [sk.lower() for sk in candidate_skills] for s in ["fastapi", "react", "docker", "redis"])
        if has_distributed_stack:
            score += 5.0

    score = score * multiplier
    return min(round(score, 2), 100.0)

def classify_role(job_title: str) -> str:
    title_lower = job_title.lower()
    if "ai" in title_lower or "ml" in title_lower or "machine learning" in title_lower or "nlp" in title_lower or "routing" in title_lower:
        return "AI"
    elif "analytics" in title_lower or "data" in title_lower or "quant" in title_lower or "analyst" in title_lower:
        return "Analytics"
    elif "frontend" in title_lower or "react" in title_lower or "typescript" in title_lower or "ui" in title_lower:
        return "Frontend"
    else:
        return "Backend"

def rank_projects(projects: list, job_tech_stack: list, job_title: str = "") -> list:
    """
    Ranks projects based on technical stack overlap.
    Returns a sorted list of projects with role-based priority boosts.
    """
    ranked = []
    role = classify_role(job_title)
    job_stack_set = set(tech.lower() for tech in job_tech_stack)
    
    for proj in projects:
        proj_skills = set(s.lower() for s in proj.get("skills", []))
        overlap = job_stack_set.intersection(proj_skills)
        score = float(len(overlap))
        
        # Apply role-based boost
        proj_name = proj.get("name", "").lower()
        if role == "Backend" and "omi gateway" in proj_name:
            score += 5.0
        elif role == "AI" and "omi gateway" in proj_name:
            score += 4.0
        elif role == "AI" and "credit risk" in proj_name:
            score += 5.0
        elif role == "Analytics" and "credit risk" in proj_name:
            score += 5.0
        elif role == "Frontend" and "autosight" in proj_name:
            score += 5.0
            
        ranked.append({
            "score": score,
            "project": proj,
            "matched_skills": list(overlap)
        })
        
    # Sort descending by skill overlap score
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return [item["project"] for item in ranked]

def rank_experiences(experiences: list, job_tech_stack: list, job_title: str = "") -> list:
    """
    Ranks work experiences based on tech stack alignment.
    Surfaces high-relevance experience dynamically based on role profiles.
    """
    ranked = []
    role = classify_role(job_title)
    job_stack_set = set(tech.lower() for tech in job_tech_stack)
    
    for exp in experiences:
        exp_skills = set(s.lower() for s in exp.get("skills", []))
        overlap = job_stack_set.intersection(exp_skills)
        score = float(len(overlap))
        
        company_lower = exp.get("company", "").lower()
        
        # Apply role-based boost to experiences
        if role == "Analytics" and "rajputana" in company_lower:
            score += 5.0
        elif role == "Backend" and "aden" in company_lower:
            score += 4.0
        elif role == "AI" and "aden" in company_lower:
            score += 4.0
            
        # Open source multiplier or boost
        if exp.get("is_open_source", False):
            score += 1.5 # Boost relevance of open source contributions
            
        ranked.append({
            "score": score,
            "experience": exp
        })
        
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return [item["experience"] for item in ranked]
