import re
import json
from config import call_llm, OFFLINE_MODE, logger, BASE_DIR, retrieve_doc

def validate_wording_proportionality(original_text: str, tailored_text: str) -> bool:
    """Check if tailored wording is proportional (no huge inflation of scope)."""
    if len(tailored_text) > len(original_text) * 3:
        return False
    return True

def run_truth_validation(generated_data: dict, database_profile: dict) -> dict:
    """
    Validates generated resume and application details against database records.
    Enforces programmatic rules and performs LLM-based truth checks.
    """
    errors = []
    warnings = []
    
    # 1. Gather all canonical metrics from DB to prevent metric fabrication
    canonical_metrics = set()
    for exp in database_profile["experiences"]:
        for ev in exp["evidence"]:
            if ev.get("metrics"):
                for match in re.findall(r'\b\d+(?:%\b|ms\b|x\b)', ev["metrics"].lower()):
                    canonical_metrics.add(match)
    for proj in database_profile["projects"]:
        for ev in proj["evidence"]:
            if ev.get("metrics"):
                for match in re.findall(r'\b\d+(?:%\b|ms\b|x\b)', ev["metrics"].lower()):
                    canonical_metrics.add(match)
                    
    logger.info("Executing Programmatic Rule checks...")
    
    db_exp_map = {exp["company"].lower(): exp for exp in database_profile["experiences"]}
    db_proj_map = {proj["name"].lower(): proj for proj in database_profile["projects"]}
    
    # Check Experiences
    for exp in generated_data.get("experiences", []):
        company_key = exp["company"].lower()
        if company_key in db_exp_map:
            db_exp = db_exp_map[company_key]
            
            # ADEN / Open Source Rule
            if db_exp.get("is_open_source", False):
                if exp.get("role") != "Open Source Contributor":
                    errors.append(
                        f"ADEN Rule Violation: Role for '{exp['company']}' was changed to '{exp.get('role')}'. "
                        f"Must remain exactly 'Open Source Contributor'."
                    )
                # Verify bullets do not imply core employee status
                employment_indicators = ["hired", "employed", "salary", "team lead", "joined as", "staff engineer", "intern", "employee"]
                for bullet in exp.get("bullets", []):
                    if any(indicator in bullet.lower() for indicator in employment_indicators):
                        errors.append(
                            f"Employment Implication: Bullet in ADEN experience implies employee status: '{bullet}'"
                        )
                        
            # Verify dates are unchanged
            if db_exp.get("start_date") and exp.get("start_date") != db_exp["start_date"]:
                errors.append(f"Date Alteration: Start date for {exp['company']} was changed from {db_exp['start_date']} to {exp.get('start_date')}")
            if db_exp.get("end_date") and exp.get("end_date") != db_exp["end_date"]:
                errors.append(f"Date Alteration: End date for {exp['company']} was changed from {db_exp['end_date']} to {exp.get('end_date')}")
                
            # Verify bullets content
            for bullet in exp.get("bullets", []):
                # Check for evidence tags
                has_pr = "pr" in bullet.lower() or "#" in bullet
                has_commit = "commit" in bullet.lower() or re.search(r'\b[0-9a-f]{6,8}\b', bullet.lower())
                if not (has_pr or has_commit):
                    errors.append(f"Evidence Tag Missing: Bullet in experience '{exp['company']}' lacks PR or commit trace reference: '{bullet}'")
                
                # Check for fabricated metrics
                for match in re.findall(r'\b\d+(?:%\b|ms\b|x\b)', bullet.lower()):
                    if match not in canonical_metrics:
                        errors.append(f"Metric Fabrication: Bullet in '{exp['company']}' contains unsupported metric '{match}': '{bullet}'")

                # Grounding validation: Gather allowed evidence tags from DB for this experience
                allowed_evidence_tags = []
                for ev in db_exp.get("evidence", []):
                    for match in re.findall(r'\b(?:pr\s*#\d+|commit\s*[0-9a-f]{5,8})\b', ev.get("description", "").lower()):
                        allowed_evidence_tags.append(match)
                        
                if allowed_evidence_tags:
                    bullet_lower = bullet.lower()
                    if not any(tag in bullet_lower for tag in allowed_evidence_tags):
                        errors.append(
                            f"Evidence Grounding Violation: Bullet in '{exp['company']}' "
                            f"references an untraceable source. Must reference one of: {', '.join(allowed_evidence_tags)}."
                        )
        else:
            errors.append(f"Fabricated Experience: Company '{exp['company']}' is not present in candidate's database.")

    # Check Projects
    for proj in generated_data.get("projects", []):
        proj_key = proj["name"].lower()
        if proj_key in db_proj_map:
            db_proj = db_proj_map[proj_key]
            
            for bullet in proj.get("description_bullets", []):
                # Check for evidence tags
                has_pr = "pr" in bullet.lower() or "#" in bullet
                has_commit = "commit" in bullet.lower() or re.search(r'\b[0-9a-f]{6,8}\b', bullet.lower())
                if not (has_pr or has_commit):
                    errors.append(f"Evidence Tag Missing: Bullet in project '{proj['name']}' lacks PR or commit trace reference: '{bullet}'")
                    
                # Check for fabricated metrics
                for match in re.findall(r'\b\d+(?:%\b|ms\b|x\b)', bullet.lower()):
                    if match not in canonical_metrics:
                        errors.append(f"Metric Fabrication: Bullet in project '{proj['name']}' contains unsupported metric '{match}': '{bullet}'")

                # Grounding validation: Gather allowed evidence tags from DB for this project
                allowed_evidence_tags = []
                for ev in db_proj.get("evidence", []):
                    for match in re.findall(r'\b(?:pr\s*#\d+|commit\s*[0-9a-f]{5,8})\b', ev.get("description", "").lower()):
                        allowed_evidence_tags.append(match)
                        
                if allowed_evidence_tags:
                    bullet_lower = bullet.lower()
                    if not any(tag in bullet_lower for tag in allowed_evidence_tags):
                        errors.append(
                            f"Evidence Grounding Violation: Bullet in project '{proj['name']}' "
                            f"references an untraceable source. Must reference one of: {', '.join(allowed_evidence_tags)}."
                        )

        else:
            errors.append(f"Fabricated Project: Project '{proj['name']}' is not present in candidate's database.")

    # 3. LLM-Based Validator
    if not OFFLINE_MODE and not errors:
        logger.info("Executing LLM-assisted verification...")
        
        # Load prompt template
        critic_prompt_path = BASE_DIR / "prompts" / "critic.md"
        if critic_prompt_path.exists():
            with open(critic_prompt_path, "r", encoding="utf-8") as f:
                prompt_template = f.read()
                
            # Collect evidence logs
            evidence_list = []
            for exp in database_profile["experiences"]:
                for ev in exp["evidence"]:
                    evidence_list.append(f"[{exp['company']}] {ev['type']}: {ev['description']} (Metrics: {ev.get('metrics')})")
            for proj in database_profile["projects"]:
                for ev in proj["evidence"]:
                    evidence_list.append(f"[{proj['name']}] {ev['type']}: {ev['description']} (Metrics: {ev.get('metrics')})")
                    
            prompt = prompt_template.format(
                evidence_logs="\n".join(evidence_list),
                generated_bullets=json.dumps(generated_data, indent=2)
            )
            
            # Retrieve RAG context
            doc_context = retrieve_doc("06_rule_engine.md")
            if doc_context:
                prompt = f"System Rules and Guidelines:\n{doc_context}\n\nTask:\n{prompt}"
                
            critic_response = call_llm(prompt)
            
            # Simple check if critic output contains "No" answers
            no_matches = re.findall(r"\bno\b", critic_response.lower())
            if no_matches:
                warnings.append(f"LLM Critic Audit Alert: Potential claim discrepancy found: {critic_response[:400]}...")
        else:
            logger.error("Critic prompt template not found.")

    passed = len(errors) == 0
    return {
        "passed": passed,
        "errors": errors,
        "warnings": warnings
    }

