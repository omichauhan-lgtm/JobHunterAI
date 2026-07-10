import json
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from storage.db import ApplicationTable, JobOpportunityTable, ResumeVariantTable

def get_detailed_analytics(db: Session) -> dict:
    """
    Computes comprehensive career CRM analytics:
    - Overall application funnel counts
    - Conversion rates by resume variant/template type
    - Interview rates by company size / YC status
    """
    total_apps = db.query(func.count(ApplicationTable.id)).scalar() or 0
    if total_apps == 0:
        return {
            "total_applications": 0,
            "funnel": {},
            "response_rate_percent": 0.0,
            "template_performance": {},
            "yc_response_rate": 0.0
        }
        
    funnel = db.query(ApplicationTable.status, func.count(ApplicationTable.id)).group_by(ApplicationTable.status).all()
    funnel_dict = {status: count for status, count in funnel}
    
    # Calculate response rate (applied -> OA/Interview/Offer)
    non_applied = db.query(func.count(ApplicationTable.id)).filter(
        ApplicationTable.status.in_(["OA", "Interview", "Offer", "Rejected", "Final"])
    ).scalar() or 0
    response_rate = round((non_applied / total_apps) * 100, 2)
    
    # Conversion by Resume template type (e.g. backend, frontend)
    template_stats = db.query(
        ResumeVariantTable.resume_type,
        func.count(ApplicationTable.id).label("total"),
        func.sum(
            case(
                (ApplicationTable.status.in_(["OA", "Interview", "Offer"]), 1),
                else_=0
            )
        ).label("converted")
    ).join(ApplicationTable, ResumeVariantTable.id == ApplicationTable.resume_variant_id)\
     .group_by(ResumeVariantTable.resume_type).all()

     
    template_perf = {}
    for row in template_stats:
        conv_rate = (row.converted / row.total * 100) if row.total > 0 else 0.0
        template_perf[row.resume_type] = {
            "total": row.total,
            "converted": int(row.converted or 0),
            "rate_percent": round(conv_rate, 2)
        }
        
    return {
        "total_applications": total_apps,
        "funnel": funnel_dict,
        "response_rate_percent": response_rate,
        "template_performance": template_perf
    }

def compare_offers(offers: list) -> list:
    """
    Deterministically ranks job offers.
    Scores each offer based on:
    - Base Salary (40 points max, scaled relative to $200k)
    - Equity Valuation / Growth potential (25 points max)
    - Work Policy / Remote status (15 points max)
    - Company stage and brand value (20 points max)
    """
    ranked_offers = []
    for offer in offers:
        score = 0.0
        
        # 1. Base Salary (scaled to 40 max, using $200,000 as high benchmark)
        base_salary = float(offer.get("base_salary", 0))
        salary_score = min((base_salary / 200000.0) * 40.0, 40.0)
        score += salary_score
        
        # 2. Equity (max 25)
        equity_val = float(offer.get("equity_annual_val", 0))
        equity_score = min((equity_val / 50000.0) * 25.0, 25.0)
        score += equity_score
        
        # 3. Remote Policy (max 15)
        policy = offer.get("work_policy", "").lower()
        if policy == "remote":
            score += 15.0
        elif policy == "hybrid":
            score += 10.0
        else:
            score += 5.0
            
        # 4. Brand & Quality (max 20)
        stage = offer.get("company_stage", "").lower()
        if "yc" in stage or "series a" in stage or "stripe" in offer.get("company_name", "").lower():
            score += 20.0
        else:
            score += 12.0
            
        ranked_offers.append({
            "company_name": offer.get("company_name"),
            "base_salary": base_salary,
            "equity_annual_val": equity_val,
            "work_policy": policy,
            "total_score": round(score, 2)
        })
        
    ranked_offers.sort(key=lambda x: x["total_score"], reverse=True)
    return ranked_offers
