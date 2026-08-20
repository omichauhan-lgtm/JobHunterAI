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

def sanitize_tex_dict(d):
    """Recursively sanitize special TeX characters in strings within dicts/lists."""
    if isinstance(d, str):
        # Only sanitize unescaped #, %, &, $, _
        s = d
        # Avoid double-escaping
        if "\\" not in s:
            s = s.replace("#", r"\#").replace("%", r"\%").replace("&", r"\&").replace("$", r"\$")
        return s
    elif isinstance(d, list):
        return [sanitize_tex_dict(item) for item in d]
    elif isinstance(d, dict):
        return {k: sanitize_tex_dict(v) for k, v in d.items()}
    return d

def render_resume(data: dict, skills_categorized: dict, template_name: str = "backend.tex") -> str:
    """Render LaTeX resume using Jinja2."""
    env = get_latex_jinja_env()
    clean_data = sanitize_tex_dict(data)
    clean_skills = sanitize_tex_dict(skills_categorized)
    template = env.get_template(template_name)
    return template.render(data=clean_data, skills=clean_skills)


def compile_latex_to_pdf(tex_path: str) -> bool:
    """Attempt to compile a LaTeX file using pdflatex if available."""
    try:
        abs_tex_path = os.path.abspath(tex_path)
        dest_dir = os.path.dirname(abs_tex_path)
        
        # Check if pdflatex exists
        subprocess.run(["pdflatex", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        # Run compilation
        cmd = ["pdflatex", "-interaction=nonstopmode", f"-output-directory={dest_dir}", abs_tex_path]
        logger.info(f"Compiling LaTeX: {abs_tex_path}")
        
        # Run twice to resolve page counts/references if any
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        logger.info("PDF compilation complete.")
        return True
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        logger.warning(f"pdflatex compilation error or not installed: {e}")
        return False


def render_cover_letter_latex(candidate_name: str, company_name: str, job_title: str, body: str, contact_info: dict) -> str:
    """Render LaTeX cover letter using Jinja2."""
    env = get_latex_jinja_env()
    try:
        template = env.get_template("cover_letter.tex")
        # Sanitize special LaTeX characters in body/company_name/job_title if any
        clean_body = body.replace("&", r"\&").replace("%", r"\%").replace("$", r"\$").replace("#", r"\#")
        clean_company = company_name.replace("&", r"\&").replace("%", r"\%").replace("$", r"\$").replace("#", r"\#")
        clean_title = job_title.replace("&", r"\&").replace("%", r"\%").replace("$", r"\$").replace("#", r"\#")
        
        return template.render(
            candidate_name=candidate_name,
            company_name=clean_company,
            job_title=clean_title,
            body=clean_body,
            date=str(os.getenv("CURRENT_DATE", "2026-08-14")),
            email=contact_info.get("email", ""),
            phone=contact_info.get("phone", ""),
            github=contact_info.get("github", ""),
            linkedin=contact_info.get("linkedin", "")
        )
    except Exception as e:
        logger.error(f"Error rendering LaTeX cover letter template: {e}")
        return ""

def render_cover_letter(candidate_name: str, company_name: str, body: str, contact_info: dict) -> str:
    """Render Markdown cover letter using template."""
    template_path = BASE_DIR / "templates" / "cover_letter.md"
    if not template_path.exists():
        return f"# Cover Letter for {company_name}\n\n{body}"
        
    with open(template_path, "r") as f:
        content = f.read()
        
    content = content.replace(r"\VAR{company_name}", company_name)
    content = content.replace(r"\VAR{candidate_name}", candidate_name)
    content = content.replace(r"\VAR{date}", str(os.getenv("CURRENT_DATE", "2026-08-14")))
    content = content.replace(r"\VAR{body}", body)
    content = content.replace(r"\VAR{email}", contact_info.get("email", ""))
    content = content.replace(r"\VAR{phone}", contact_info.get("phone", ""))
    content = content.replace(r"\VAR{github}", contact_info.get("github", ""))
    content = content.replace(r"\VAR{linkedin}", contact_info.get("linkedin", ""))
    
    return content

