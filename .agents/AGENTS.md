# FLEET LOOP ENGINEERING CONSTITUTION

## Project: JobHunterAI — Career Intelligence Platform

### Version: Version 8.0 Enterprise Engineering Directive

---

## 1. Mission
Build JobHunterAI into a cloud-native Career Intelligence Platform that assists candidates throughout the hiring lifecycle.

The platform must:
- Discover high-quality opportunities.
- Prioritize opportunities intelligently.
- Generate evidence-backed application materials.
- Support networking.
- Support interview preparation.
- Track outcomes.
- Improve from measurable results.

Success is measured by:
- recruiter responses
- interview rate
- assessment rate
- offer rate
- user productivity

Never optimize solely for application volume.

---

## 2. Product Vision
The product is not:
- a resume generator
- a cover-letter generator
- an auto-apply bot

The product is:
- Career Intelligence Platform
- Recruitment Operating System
- Opportunity Intelligence Engine
- Knowledge-driven Career Assistant

---

## 3. Core Principles
Every engineering decision must satisfy:
- Evidence First
- Truthfulness
- Explainability
- Deterministic Before AI
- Human-in-the-Loop
- Retrieval Before Fine-Tuning
- Modular Architecture
- Cloud-First Design
- Security by Default
- Production Readiness

---

## 4. Technology Strategy
Preferred technologies (replace only with justified alternatives):

### Frontend
- React
- TypeScript
- Next.js
- Tailwind CSS

### Design
- Figma
- 21st.dev
- ShaderGradient
- AutoAnimate
- Lucide Icons

### Design Language
- Claymorphism
- Brutalism

### Backend
- Firebase (Authentication, Firestore, Storage, Hosting where appropriate)
- Python services for AI orchestration
- SQLAlchemy for relational components where needed

### AI Workflow
- Paperclip (preferred workflow orchestration if appropriate)
- Retrieval-Augmented Generation
- Pluggable LLM providers

### Developer Experience
- CodeRabbit
- GitHub Actions
- Ruff
- Black
- mypy
- pytest
- Docker

### Demonstration
- Storylane for interactive product walkthroughs

---

## 5. Cloud-Native Architecture
Do not build a localhost-dependent system. The platform must support deployment as a continuously running web application with:
- authentication
- scheduled background jobs
- secure APIs
- persistent storage
- remote access
- responsive web interface

Local execution is for development only.

---

## 6. User Experience
The interface should feel: Professional, Minimal, Fast, Accessible, Modern, Premium.
Characteristics:
- responsive
- keyboard accessible
- dark mode first
- smooth motion
- consistent spacing
- readable typography
- subtle animations
- meaningful empty states

Never sacrifice usability for visual effects.

---

## 7. AI Architecture
Use deterministic logic whenever practical.

### Deterministic:
- ranking
- validation
- scoring
- graph traversal
- analytics
- scheduling
- caching
- business rules

### LLM:
- summarization
- resume wording
- cover letters
- outreach
- interview preparation

Never use AI where deterministic logic provides a better solution.

---

## 8. Resume Intelligence
Generate resumes by:
```
Job Description ➔ Knowledge Graph Query ➔ Evidence Selection ➔ Project Ranking ➔ Resume Compilation ➔ ATS Optimization ➔ Truth Validation ➔ Human Review ➔ Output
```
Never generate unsupported claims.

---

## 9. Knowledge Graph
Every statement must trace back to:
```
Evidence ➔ Skill ➔ Project ➔ Experience ➔ Resume Bullet ➔ Resume Version ➔ Application ➔ Interview ➔ Offer
```
Complete traceability is mandatory.

---

## 10. ATS Strategy
Optimize for truthful compatibility. Never fabricate experience.
Improve:
- keyword coverage
- formatting
- structure
- relevance

Stop optimization when no truthful improvements remain.

---

## 11. Validation Pipeline
Every feature must pass:
1. Static analysis
2. Type checking
3. Unit tests
4. Integration tests
5. End-to-end tests
6. Accessibility checks
7. Performance checks
8. Security checks
9. Manual review where appropriate

Outputs failing validation must not be merged.

---

## 12. Quality Gates
Every completed feature must satisfy:
- [x] Clean Architecture
- [x] Documentation
- [x] Tests
- [x] Explainability
- [x] Accessibility
- [x] Security
- [x] Maintainability
- [x] Performance
- [x] Production Readiness

---

## 13. Code Review
Every PR should undergo:
- automated linting
- automated formatting
- automated testing
- automated review (e.g. CodeRabbit)
- human review before merge

---

## 14. Documentation
Maintain: README, Architecture, Database, Knowledge Graph, Deployment, API, Testing, Contributing, Changelog, and Decision Records.
Documentation must remain synchronized with implementation.

---

## 15. UI/UX Standards
Build a premium experience inspired by Claymorphism, Brutalist layouts, and modern SaaS dashboards.
Use:
- consistent spacing
- reusable design system
- accessible color contrast
- semantic HTML
- responsive layouts

Avoid unnecessary visual complexity.

---

## 16. Deployment
Support Docker, CI/CD, cloud deployment, environment separation, secrets management, backups, monitoring, and logging.

---

## 17. Notifications
Generate Daily Brief, Weekly Summary, and Monthly Career Analytics containing:
- opportunities
- applications
- interviews
- recruiter activity
- recommendations
- action items

---

## 18. Continuous Learning
Improve using:
- interview outcomes
- recruiter responses
- ATS trends
- resume performance

Do not reinforce unsupported information.

---

## 19. Security
Protect user data, API keys, credentials, uploaded resumes, and recruiter information. Never expose secrets.

---

## 20. Constraints
Never:
- fabricate experience, metrics, or technologies
- overstate open-source work
- bypass validation
- auto-submit applications without explicit user approval
- violate website terms of service

Always preserve human review before external actions.

---

## 21. Completion Criteria
A feature is complete only when implementation is correct, tests pass, documentation is updated, code review passes, accessibility requirements are met, performance is acceptable, security review passes, deployment succeeds, and the feature demonstrably improves the platform's objectives.

---

## 22. Master Execution Directive

The following directive serves as the primary guidance for the lead software and product engineer of JobHunterAI.

### Mission & Focus
Refine, deploy, and operate JobHunterAI as a production-grade, cloud-hosted Career Intelligence Platform. Optimize for measurable product quality and real-world outcomes over internal refactors alone.

### Guiding Principles
- Evidence before generation.
- Deterministic logic before LLM reasoning.
- Retrieval before fine-tuning.
- Human approval before external actions.
- Cloud-first architecture.
- Production-ready engineering.
- Simplicity over unnecessary complexity.
- Visible product improvements over internal refactors.

### Current Priorities
1. Preserve the existing backend, knowledge graph, ranking engine, validation pipeline, analytics, and CRM.
2. Replace any remaining prototype UI with a polished Next.js frontend.
3. Ensure the frontend consumes backend APIs rather than duplicating logic.
4. Deploy the complete application to cloud infrastructure. Localhost is for development only.
5. Ensure scheduled background jobs continue running independently of the developer's machine.
6. Continue discovering opportunities from supported public sources and official company career pages where appropriate.
7. Produce a daily spreadsheet and email briefing of ranked opportunities.
8. Require explicit user approval before submitting any application.

### Product Requirements
The platform must provide: Landing page, Authentication, Dashboard, Job discovery, Ranked opportunity queue, Resume generation, ATS optimization, Truth validation, Recruiter CRM, Knowledge graph explorer, Interview preparation, Analytics, Explainability, and Daily reports.

### Design Language
Express a cohesive blend of Claymorphism and Brutalist layouts (responsive, accessible, fast, and visually consistent).

### Engineering Workflow & Quality Gates
Every feature follows the lifecycle: Research ➔ Plan ➔ Implement ➔ Test ➔ Review ➔ Document ➔ Deploy ➔ Validate.
No feature is complete until it passes static analysis, type checking, unit tests, integration tests, accessibility review, performance review, security review, documentation updates, and manual UX review.

### Success Metrics
Measure success using: Recruiter responses, Interview invitations, Assessment invitations, Offer rate, User productivity, Product reliability, and User-visible quality.

### Constraints
Never fabricate experience, metrics, or evidence; never overstate open-source work; never bypass validation; never auto-submit applications; and never claim production success without verification.
