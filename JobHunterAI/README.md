# JobHunterAI: AI Career Intelligence & Recruitment Operating System

JobHunterAI is an enterprise-grade **Career Intelligence Platform & Recruitment Operating System** designed to treat your job search like a high-precision sales pipeline. 

Unlike simple "auto-apply" spam bots, JobHunterAI focuses on **conversion, credibility, and traceability**. It automates opportunity discovery, performs deterministic match scoring, iteratively refines resume bullets against ATS keywords, and guarantees factual credibility by verifying every generated claim against a personal **Career Knowledge Graph** using a programmatic **Rule Engine**.

---

## 🛠️ High-Level Architecture & Workflow

```
                    INTERNET (Job Boards)
                             │
                             ▼
                    Job Discovery Engine
                             │
                             ▼
                    Company Intelligence
                             │
                             ▼
                    Opportunity Ranking (Deterministic)
                             │
                             ▼
                    Knowledge Graph Query
                             │
                             ▼
                    Resume Compiler Engine
                             │
                             ▼
                    ATS Optimization Engine (Iterative Loop)
                             │
                             ▼
                    Truth Validation Engine (AI Critic + Rules)
                             │
                             ▼
                    Streamlit Approval Gate (Human in the loop)
                             │
                             ▼
                   Generated Tailored Assets
```

---

## 📂 Project Structure

```text
JobHunterAI/
│
├── config.py                 # System configuration, dotenv loading, API key config
├── orchestrator.py           # Pipeline Orchestrator coordinating deterministic & LLM stages
├── app.py                    # Streamlit Dashboard UI (approval gate, graph explorer, analytics)
├── main.py                   # CLI entrypoint for discovery and local compilation
│
├── prompts/                  # Prompt Registry (Markdown files, no prompts in python code)
│   ├── job_analysis.md
│   ├── ats_optimizer.md
│   ├── resume_generator.md
│   ├── critic.md
│   ├── cover_letter.md
│   ├── networking.md
│   └── interview.md
│
├── storage/                  # Database management (SQLite + SQLAlchemy 2.0)
│   ├── db.py                 # Database engine & tables
│   ├── crud.py               # Graph traversal queries & transactional CRUD operations
│   └── seed.py               # Seeds the database with candidate profile and evidence logs
│
├── models/                   # Pydantic validation schemas
│   └── schemas.py            # Pydantic schemas (Job, Project, Candidate, STAR story)
│
├── engines/                  # Independent functional modules
│   ├── discovery.py          # Scrapes Greenhouse, Lever, and Ashby postings
│   ├── company_intel.py      # Researches company stage, tech stack, and YC status
│   ├── ranking.py            # Deterministic job scoring and project ranking
│   ├── compiler.py           # Resumes renderer (Jinja2 LaTeX) & cover letter compiler
│   ├── ats.py                # ATS optimization checks & iterative loop
│   ├── critic.py             # Truth validator (Programmatic Rule Engine + LLM verification)
│   ├── networking.py         # outreach generator (LinkedIn notes)
│   ├── interview.py          # STAR interview prep generator
│   └── analytics.py          # CRM funnel metrics and offer evaluation comparisons
│
├── templates/                # Jinja2 templates for resumes and cover letters
│   ├── backend.tex
│   └── cover_letter.md
│
└── tests/                    # Automated testing suite
    └── test_pipeline.py      # Relational graph validation & pipeline tests
```

---

## 💾 Relational Knowledge Graph Schema

The database uses **SQLAlchemy 2.0** to model candidate records as a connected graph:
- **`Candidate`**: Roots the profile details.
- **`Experience`**: Traditional corporate jobs or open-source roles.
- **`Project`**: Engineering products built.
- **`Skill`**: Candidate tech stack mapped to relevant projects.
- **`Evidence`**: Verified links (PRs, commits, issues, docs, deployments) connected directly to projects/experiences to back up resume bullets.
- **`STARStory`**: Interview scenarios matching experiences.
- **`JobOpportunity`**: Tracks scraped positions and viability scores.
- **`Application`**: Relates jobs, resumes, outreach letters, and conversion statuses.
- **`RecruiterCRM`**: Tracks recruiters and conversation logs.

---

## ⚖️ Deterministic vs. AI Logic Separation

For maximum stability, JobHunterAI splits logic strictly:
* **Deterministic (Python)**: Database queries, scoring metrics, project/experience sorting, keyword counting, verification check gates, and funnel analytics.
* **LLM (Gemini / OpenAI)**: Synthesizing wording, composing cover letters, drafting outreach notes, and brainstorming interview questions.

### 🛡️ Programmatic Rule Engine
To prevent AI hallucination or exaggeration:
1. **The ADEN Rule**: Any experience marked `is_open_source=True` (like ADEN contribution) is hard-locked to the role **"Open Source Contributor"**. The pipeline fails if the LLM attempts to rename it or claim core employment status.
2. **Metadata Integrity**: Experience dates, titles, and companies are immutable.
3. **Traceability**: Every tailored bullet point must map back to a database-verified evidence record (e.g. PR #142, Commit 8f2c3d) or it is flagged.

---

## ⚡ Setup & Usage

### 1. Requirements
Ensure you have Python 3.12+ installed. Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your API key (`GEMINI_API_KEY` or `OPENAI_API_KEY`). If no keys are provided, JobHunterAI defaults to **Offline Mode**, using local mock text engines to compile the files.

### 3. Initialize & Seed Database
Build the tables and seed candidate graph data:
```bash
python storage/seed.py
```

### 4. CLI Execution
- **Auto-discover mock opportunities**:
  ```bash
  python main.py --discover
  ```
- **Ingest a live Lever or Greenhouse URL**:
  ```bash
  python main.py --url https://jobs.lever.co/stripe/senior-backend-engineer
  ```
- **Run the tailored generation pipeline** (e.g. for Job ID 1):
  ```bash
  python main.py --apply-job 1
  ```

### 5. Streamlit Interactive Dashboard
Run the dashboard to browse the Knowledge Graph, review tailored resume diffs, write recruiter outreach records, and compare offers:
```bash
streamlit run app.py
```
