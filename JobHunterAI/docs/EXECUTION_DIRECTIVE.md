# FLEET LOOP EXECUTION DIRECTIVE

# JobHunterAI — Cloud-Native SaaS Platform (V11)

## Mission

Evolve **JobHunterAI** into a cloud-native SaaS application accessible through a public domain, with continuous background processing, secure authentication, persistent storage, scheduled workflows, and daily email reporting. Localhost is reserved exclusively for development, testing, and debugging.

---

## Primary Goal

Optimize the system for **maximizing high-quality remote offers** and candidate productivity, rather than application volume.

Primary KPIs:
- Recruiter Response Rate
- Interview Rate
- Assessment Rate
- Offer Rate
- Candidate Productivity

---

## V11 Service Architecture

The system is split into separate, portable service modules:

```
                    Internet
                         │
          ┌──────────────┴──────────────┐
          │                             │
     Frontend (Next.js)            Firebase Auth
          │                             │
          └──────────────┬──────────────┘
                         │
                    API Gateway
                         │
         ┌───────────────┼────────────────┐
         │               │                │
  Job Discovery     Resume Engine     Analytics
         │               │                │
         └───────────────┼────────────────┘
                         │
                PostgreSQL / Firestore
                         │
               Background Worker
                         │
         Daily Discovery Every Morning
                         │
                Gmail Report
                         │
                     Your Inbox
```

- **Frontend**: Next.js React TypeScript web dashboard deployed on **Vercel** with a responsive layout combining **Claymorphism** and **Brutalist** card designs.
- **Backend APIs**: FastAPI Python microservices deployed to **Railway / Render / Google Cloud Run / Fly.io**.
- **Database**: **Firebase Firestore / PostgreSQL** for application states and CRM.
- **File Storage**: **Firebase Storage** for rendered PDF resumes.
- **Scheduled Background Worker**: Containerized scheduler executing daily loops (job discovery, match scoring, resume compilers, CSV spreadsheet generation, and Gmail SMTP delivery) at 08:00 AM every morning.

---

## Design System: Claymorphism + Brutalism
Inspired by the clean aesthetics of Linear.app, Vercel, Cursor, Apple, and Arc:
- **Brutalist Layouts**: Thick black outlines (`border-4 border-black`), blocky drop-shadow offset panels (`shadow-[6px_6px_0px_0px_rgba(0,0,0,1)]`), and interactive mouse translation effects.
- **Claymorphism Controls**: Soft inset lights (`shadow-[inset_0_2px_4px_rgba(255,255,255,0.6)]`), clean rounded borders (`rounded-3xl`), and glassy backdrop blurs.

---

## Morning Spreadsheet & Email Delivery
Every morning at **08:00 AM**, the background worker will:
1. Search public platforms and target watchlist pages.
2. Filter duplicates and score opportunities against your backend/AI systems profile.
3. Tailor resume LaTeX builds and drafts cover letters for matches above 70%.
4. Generate a CSV spreadsheet report containing:
   `Match % | Company | Role | Salary | Country | Remote Status | Direct Application Link | Notes | Status`
5. Dispatch the HTML daily brief with the CSV spreadsheet attached directly to your personal Gmail.

---

## Operational Constraints
- **Human-in-the-Loop**: The platform auto-discovers, auto-researches, and auto-tailors, but **never** submits applications automatically. Explicit user approval is mandatory for all external submittals.
- **Grounded validation**: Generated resume bullets must contain verifiable PR or Commit references to prevent model hallucinations.
