import os
import json
from pathlib import Path
from config import call_llm, OFFLINE_MODE, logger, BASE_DIR, retrieve_doc

def load_prompt_template(name: str) -> str:
    path = BASE_DIR / "prompts" / name
    if not path.exists():
        return ""
    with open(path, "r") as f:
        return f.read()

def calculate_ats_score(bullets: list, keywords: list) -> float:
    """Deterministically compute ATS keyword match score (0-100)."""
    if not keywords:
        return 100.0
    text = " ".join(bullets).lower()
    matched = 0
    for kw in keywords:
        # Check simple substring match for flexibility (ATS engines typically do substring)
        if kw.lower() in text:
            matched += 1
    return round((matched / len(keywords)) * 100, 2)

def run_ats_optimization(bullets: list, keywords: list) -> dict:
    """Iteratively optimize resume bullets against target ATS keywords."""
    initial_score = calculate_ats_score(bullets, keywords)
    logger.info(f"Initial ATS Match Score: {initial_score}%")
    
    if initial_score >= 90.0:
        return {
            "optimized_bullets": bullets,
            "initial_score": initial_score,
            "final_score": initial_score,
            "iterations": 0
        }
        
    optimized = bullets.copy()
    
    if OFFLINE_MODE:
        logger.info("Running in OFFLINE mode. Applying deterministic keyword injection.")
        for kw in keywords:
            text = " ".join(optimized).lower()
            if kw.lower() in text:
                continue
            
            injected = False
            for i, b in enumerate(optimized):
                if "skills:" in b.lower() or "tech stack:" in b.lower():
                     optimized[i] = b.rstrip(".") + f", {kw}."
                     injected = True
                     break
            
            if not injected and optimized:
                optimized[0] = optimized[0].rstrip(".") + f" (utilizing {kw})."
                
        final_score = calculate_ats_score(optimized, keywords)
        logger.info(f"Offline injection complete. Final ATS score: {final_score}%")
        return {
            "optimized_bullets": optimized,
            "initial_score": initial_score,
            "final_score": final_score,
            "iterations": 1
        }
        
    current_score = initial_score
    iterations = 0
    max_iterations = 3
    
    prompt_template = load_prompt_template("ats_optimizer.md")
    if not prompt_template:
        logger.error("ATS Optimizer prompt template not found.")
        return {
            "optimized_bullets": bullets,
            "initial_score": initial_score,
            "final_score": initial_score,
            "iterations": 0
        }
    
    while current_score < 90.0 and iterations < max_iterations:
        iterations += 1
        logger.info(f"ATS Optimization Iteration {iterations}...")
        
        prompt = prompt_template.format(
            bullets=json.dumps(optimized, indent=2),
            keywords=", ".join(keywords)
        )
        
        # Retrieve RAG context
        doc_context = retrieve_doc("08_ats_engine.md")
        if doc_context:
            prompt = f"System Rules and Guidelines:\n{doc_context}\n\nTask:\n{prompt}"
            
        response = call_llm(prompt)

        
        if response.startswith("MOCK_RESPONSE") or response.startswith("ERROR"):
            break
            
        # Simple extraction of bullets from response text
        lines = [line.strip().lstrip("-* ").strip() for line in response.splitlines() if line.strip()]
        
        # Strip code blocks
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
            
        parsed_bullets = []
        for line in lines:
            if line.startswith("[") and line.endswith("]"):
                try:
                    parsed_bullets.extend(json.loads(line))
                    continue
                except:
                    pass
            if len(line) > 10:
                parsed_bullets.append(line)
                
        if parsed_bullets:
            optimized = parsed_bullets
            current_score = calculate_ats_score(optimized, keywords)
            logger.info(f"Iteration {iterations} ATS score: {current_score}%")
        else:
            logger.warning("LLM returned unparseable text in ATS loop. Retaining current bullets.")
            break
            
    return {
        "optimized_bullets": optimized,
        "initial_score": initial_score,
        "final_score": current_score,
        "iterations": iterations
    }
