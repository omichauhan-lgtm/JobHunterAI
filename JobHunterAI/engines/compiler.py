import os
import subprocess
import jinja2
from pathlib import Path
from config import logger, GEN_DIR, BASE_DIR

def get_latex_jinja_env():
    return jinja2.Environment(
        block_start_string='\BLOCK{',
        block_end_string='}',
        variable_start_string='\VAR{',
        variable_end_string='}',
        comment_start_string='\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(str(BASE_DIR / "templates"))
    )

def render_resume(data: dict, skills_categorized: dict, template_name: str = "backend.tex") -> str:
    """Render LaTeX resume using Jinja2."""
    env = get_latex_jinja_env()
    template = env.get_template(template_name)
    return template.render(data=data, skills=skills_categorized)

def compile_latex_to_pdf(tex_path: str) -> bool:
    """Attempt to compile a LaTeX file using pdflatex if available."""
    try:
        # Check if pdflatex exists
        subprocess.run(["pdflatex", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        # Run compilation
        dest_dir = os.path.dirname(tex_path)
        cmd = ["pdflatex", "-interaction=nonstopmode", f"-output-directory={dest_dir}", tex_path]
        logger.info(f"Compiling LaTeX: {tex_path}")
        
        # Run twice to resolve page counts/references if any
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        logger.info("PDF compilation complete.")
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        logger.warning("pdflatex is not installed locally. Raw LaTeX .tex generated successfully. Copy to Overleaf.com to compile.")
        return False

def render_cover_letter(candidate_name: str, company_name: str, body: str, contact_info: dict) -> str:
    """Render Markdown cover letter using template."""
    template_path = BASE_DIR / "templates" / "cover_letter.md"
    if not template_path.exists():
        return f"# Cover Letter for {company_name}\n\n{body}"
        
    with open(template_path, "r") as f:
        content = f.read()
        
    # Standard replacement for simple markdown (non-LaTeX) template
    content = content.replace(r"\VAR{company_name}", company_name)
    content = content.replace(r"\VAR{candidate_name}", candidate_name)
    content = content.replace(r"\VAR{date}", str(os.getenv("CURRENT_DATE", "2026-07-02")))
    content = content.replace(r"\VAR{body}", body)
    content = content.replace(r"\VAR{email}", contact_info.get("email", ""))
    content = content.replace(r"\VAR{phone}", contact_info.get("phone", ""))
    content = content.replace(r"\VAR{github}", contact_info.get("github", ""))
    content = content.replace(r"\VAR{linkedin}", contact_info.get("linkedin", ""))
    
    return content
