# 04 - Database Schema

## Relational Layout
The database is managed via SQLite (`candidate.db`) using SQLAlchemy 2.0 ORM schemas.

### Primary Tables
- **`candidates`**: Master candidate profile attributes (id, name, email, github, linkedin).
- **`experiences`**: Candidate professional work history. Includes `is_open_source` flag.
- **`projects`**: Custom projects category details.
- **`skills`**: Master skills registry.
- **`evidence`**: Traces mapping to Git commits, pull requests, issues, or deployments.
- **`star_stories`**: Structured STAR profiles for interview mapping.
- **`job_opportunities`**: Scraped or manually added job details.
- **`resume_variants`**: Tracks versioned LaTeX resume sources.
- **`applications`**: Funnel log of applied opportunities, templates used, and outreach files.
- **`recruiter_crm`**: Communication logs mapped to recruiters.
- **`relationships`**: Graph link helper for mapping arbitrary edges (e.g. Skill -> Project).
