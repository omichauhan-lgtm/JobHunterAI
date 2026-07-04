# 02 - System Architecture

## Architecture Overview
JobHunterAI is built on a modular design dividing deterministic system logic from LLM text generation to maximize predictability and debuggability.

```
                    INTERNET (Lever/Greenhouse)
                              │
                              ▼
                     Job Discovery Engine
                              │
                              ▼
                     Company Intelligence
                              │
                              ▼
                   Opportunity Match Scoring (Deterministic)
                              │
                              ▼
                     Knowledge Graph Query (Deterministic)
                              │
                              ▼
                     Resume Compiler (LaTeX Rendering)
                              │
                              ▼
                     ATS Optimization Engine (LLM Loop)
                              │
                              ▼
                     Truth Validator (Critic Checks)
                              │
                              ▼
                     Human Approval Gate (Streamlit)
```

## Logic Partitioning
| Module | Type | Tech |
|---|---|---|
| Discovery & Ingestion | Deterministic | HTTP Requests / BeautifulSoup4 |
| Opportunity Scoring | Deterministic | Regex Keyword Matching |
| Project & Experience Ranking | Deterministic | Tech Stack Vector Intersections |
| Resume Compilation | Deterministic | Jinja2 LaTeX compiler |
| Bullets Customization | LLM-assisted | Gemini/OpenAI Structured JSON |
| Truth Validation / Auditing | Hybrid | Programmatic Rules + LLM Critic |
| CRM Funnel Analytics | Deterministic | SQL Queries |
