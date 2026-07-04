# 03 - Pipeline Orchestration

## Pipeline Sequence
The `orchestrator.py` module manages the application pipeline using the following state machine:

1. **Ingest Job**: Ingests job title and description via manual copy-paste or live URL scrapers.
2. **Company Intelligence**: Gathers stage, funding, tech stack, and recent press/news.
3. **Deterministic Scoring**: Rates job compatibility. If below the `JOB_APPLY_THRESHOLD` (e.g. 70%), aborts application.
4. **Knowledge Retrieval**: Queries SQLite candidate graph, selecting top matching projects and experiences.
5. **ATS Optimization**: Integrates missing target keywords into resume bullets.
6. **Critic Audit**: Programmatically enforces dates, titles, and ADEN's open-source status.
7. **Asset Compilation**: Compiles `.tex` files, drafts cover letters, and generates outreach templates.
8. **Explainability Log**: Outputs a JSON metadata report outlining selection decisions.
9. **CRM Logging**: Creates job application records in the database.
