# Project Execution Directive: JobHunterAI

This document serves as the active project directive, defining the active product specifications, target metrics, constraints, and operational focus areas. It changes as the product evolves.

---

## 1. Product Vision & Success Metrics
JobHunterAI is a high-precision **Career Intelligence Platform** to maximize the probability of securing high-quality remote offers.

### Core Funnel Metrics:
- **Response Rate**: Recruiter replies / applications submitted.
- **Interview Rate**: Technical or recruiter interviews secured / applications submitted.
- **Assessment Rate**: Online coding assessments (OAs) received.
- **Offer Rate**: Written job offers received.
- **User Productivity**: Time spent reviewing, optimizing, and approving materials.

---

## 2. Target Candidate & Role Focus
- **Candidate Profile**: Omi Chauhan (NIT Warangal, specializing in high-performance Python backends, FastAPI gateways, Docker orchestrations, and LLM routing).
- **Target Positions**:
  - Founding Engineer
  - Backend Engineer (Python/FastAPI)
  - AI Engineer / AI Infrastructure Engineer
  - Full Stack Engineer
  - Software Engineer / Systems Engineer
  - Technical Implementation Engineer / Solutions Engineer

---

## 3. Technology Stack & Design System
- **Preferred Frontend**: React, TypeScript, Next.js, Tailwind CSS.
- **Preferred Design Language**: Claymorphism and Brutalism dashboard layouts.
- **Preferred Backend & Storage**: Python, FastAPI, SQLAlchemy, SQLite (local dev), Firebase (cloud authentication, storage, hosting).
- **Preferred AI Orchestration**: Paperclip / pluggable LLM integrations (Gemini, OpenAI).

---

## 4. Multi-Stage Validation Pipeline
No feature is considered complete until it passes the following gates:
1. **Static Analysis & Linting**: Verified via code checkers (e.g. Ruff, Black, mypy).
2. **Unit Testing**: 100% test passing (e.g. `tests/test_pipeline.py`).
3. **Integration Testing**: End-to-end matching, scoring, and output compilers.
4. **Factual Grounding Checks**: Every PR or Commit tag in generated resumes must resolve to candidate database evidence logs.
5. **Accessibility Checks**: Semantic HTML structure and screen reader compatibility.
6. **Performance Checks**: Latency ceilings (e.g. OMI Gateway <= 45ms routing limits).
7. **Security Scans**: Protection of user profiles and API credentials.
8. **Manual UX Review**: Human validation for layout spacing, typographies, and alerts.

---

## 5. Active Target Channels (The Discovery Universe)
1. **ATS Portals**: Greenhouse, Lever, Ashby, SmartRecruiters, Workable, Teamtailor, Recruitee, BambooHR, Jobvite, iCIMS.
2. **Remote Boards**: Wellfound, Himalayas, Otta, We Work Remotely, Remote.co, Remotive, Arc, Turing, FlexJobs.
3. **Startup Ecosystem**: YC companies, AI startups, DevTools startups, SaaS startups, Infrastructure startups.
4. **Watchlist Pages**: Custom targets (e.g. Stripe, VectorShift, ADEN).
5. **Networking Intelligence**: EM/Founder recruiter leads on LinkedIn.

---

## 6. Constraints & Guiding Rules
- **No Exaggeration**: Never fabricate experience, metrics, or technologies.
- **Human-in-the-Loop**: The platform compiles resumes, cover letters, and outreach sequences, but **never** submits them automatically.
- **Cloud-First Deployment**: Run background workers, database volumes, and web containers persistently on cloud nodes. Localhost is for development and testing only.
