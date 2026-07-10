# FLEET LOOP EXECUTION DIRECTIVE

# JobHunterAI — Production Readiness & Product Validation (V9)

## Mission

The architectural foundation of JobHunterAI is complete.

The objective is no longer to add architectural complexity.

The objective is to transform JobHunterAI into a reliable, production-grade Career Intelligence Platform that consistently produces measurable improvements in interview conversion while maintaining truthful, evidence-backed application generation.

The platform shall evolve through real-world validation, measurable outcomes, and continuous engineering improvement.

---

## Primary Goal

Optimize for:
- Interview Conversion
- Recruiter Response Rate
- Assessment Rate
- Offer Rate
- User Productivity
- Reliability
- Maintainability

Do **not** optimize for application volume.

---

## Engineering Philosophy

Every engineering decision must satisfy the following principles:
- Evidence First
- Deterministic Before AI
- Retrieval Before Fine-Tuning
- Human-in-the-Loop
- Cloud-First
- Security by Default
- Explainability
- Production Readiness
- Backward Compatibility
- Continuous Improvement

---

## Immediate Objectives

### 1. Production Deployment
Transition from local development to a continuously available cloud deployment.

Requirements:
- Cloud-hosted web application
- Secure authentication
- Background workers
- Scheduled jobs
- Environment separation
- Secret management
- Monitoring
- Structured logging
- Automated backups
- Health checks
- Graceful failure handling

Localhost is for development only.

---

### 2. Replace Mock Data
Identify and eliminate all remaining placeholder data.

Replace with:
- real job sources
- real company information
- real candidate data
- verified evidence
- genuine recruiter interactions

No demonstration-only data should remain in production.

---

### 3. Job Discovery
Expand discovery using supported public sources and official career pages where appropriate.

The discovery engine shall:
- normalize jobs
- remove duplicates
- classify role category
- identify remote eligibility
- compute deterministic match scores
- reject low-value opportunities

Prioritize:
- Backend Engineering
- AI Engineering
- Analytics Engineering
- Data Engineering
- Software Engineering

Focus on legitimate remote opportunities matching the candidate's profile.

---

### 4. Candidate Knowledge Graph
Complete the knowledge graph.

Import every verified:
- project
- internship
- leadership role
- certification
- publication
- GitHub repository
- pull request
- commit
- deployment
- presentation
- measurable achievement

Every generated statement must remain traceable to evidence.

---

### 5. Resume Intelligence
Continue generating dynamic resumes using:
```
Job ➔ Knowledge Graph ➔ Evidence Selection ➔ Role-Based Ranking ➔ Resume Compiler ➔ ATS Optimization ➔ Truth Validation ➔ Human Approval ➔ Application Package
```
Never generate unsupported claims.

---

### 6. OMI Integration
Treat OMI as a flagship engineering project.

Present different implemented aspects depending on role:
- **Backend**: FastAPI, API Architecture, Docker, PostgreSQL, Infrastructure
- **AI**: LLM Routing, Evaluation, Orchestration
- **Analytics**: Metrics, Telemetry, Evaluation Pipelines

Only expose completed, verifiable work.

---

### 7. ATS Optimization
Maximize truthful compatibility.
Do not pursue arbitrary numeric scores.

Instead maximize:
- relevant keyword coverage
- clean formatting
- project relevance
- skill relevance
- ATS compatibility

Stop optimization once no further truthful improvements exist.

---

### 8. Truth Validation
Every generated artifact must pass deterministic validation.

Reject immediately if any generated content:
- invents experience
- invents metrics
- invents technologies
- modifies employment dates
- modifies titles
- exaggerates open-source contributions
- implies employment incorrectly
- lacks supporting evidence

Validation failures block output generation.

---

### 9. Daily Autonomous Workflow
Execute recurring workflows that:
- discover new opportunities
- deduplicate jobs
- score opportunities
- research companies
- prepare application packages
- generate explainability reports
- update analytics
- prepare daily briefing
- queue applications for approval

Never submit applications automatically.
Require explicit user approval before any external action.

---

### 10. Notifications
Generate:
- Daily Report
- Weekly Report
- Monthly Career Summary

Reports should include:
- new opportunities
- pending applications
- recruiter activity
- interview schedule
- follow-up reminders
- recommended actions
- market trends
- learning recommendations

If email delivery is unavailable:
- archive reports
- retry delivery
- notify through dashboard

---

### 11. Dashboard
Maintain a production-quality dashboard containing:
- Application Queue
- Daily Briefing
- Knowledge Graph Explorer
- Resume Comparison
- Explainability
- Recruiter CRM
- Interview Tracker
- Offer Comparison
- Analytics
- System Health

---

### 12. Career Analytics
Measure:
- applications
- recruiter replies
- assessments
- interviews
- offers
- acceptance rate

Measure performance by:
- resume version
- project ordering
- company type
- job category
- outreach strategy

Use these results to improve future recommendations.

---

### 13. Portfolio Quality
Treat JobHunterAI itself as a flagship engineering project.

Maintain:
- professional README
- architecture diagrams
- database schema
- deployment guide
- API documentation
- screenshots
- demo assets
- changelog
- contribution guide

Documentation must reflect implementation.

---

### 14. UI / UX
Design goals:
- modern
- premium
- responsive
- accessible
- performant

Preferred visual direction:
- Claymorphism
- Brutalist structure

Preferred tooling where appropriate:
- Figma
- Lucide
- AutoAnimate
- ShaderGradient
- Storylane
- CodeRabbit

These are preferred implementation tools, not mandatory dependencies.
User experience always takes priority over visual effects.

---

### 15. Engineering Workflow
Every feature must complete:
```
Planning ➔ Implementation ➔ Static Analysis ➔ Type Checking ➔ Unit Tests ➔ Integration Tests ➔ Accessibility Review ➔ Performance Review ➔ Security Review ➔ Code Review ➔ Documentation Update ➔ Deployment Validation ➔ Human Review
```
Only then may the feature be considered complete.

---

### 16. Continuous Improvement
After every execution cycle:
- analyze outcomes
- identify bottlenecks
- reduce technical debt
- remove duplication
- improve modularity
- improve documentation
- increase test coverage

Only introduce new features when supported by measurable evidence or a clearly defined product requirement.

---

## Operational Constraints

Never:
- fabricate qualifications
- fabricate evidence
- fabricate metrics
- misrepresent open-source work
- bypass validation
- automatically submit applications
- violate employer or platform terms of service

Always preserve truthful representation and explicit user approval for external actions.

---

## Completion Criteria

JobHunterAI is considered production-ready when it:
- continuously discovers relevant opportunities,
- prepares high-quality evidence-backed application packages,
- supports networking and interview preparation,
- provides measurable analytics,
- improves recommendations through real-world outcomes,
- operates reliably as a cloud-hosted service,
- and maintains engineering quality through comprehensive validation, documentation, testing, and review.
