# ATS System Guidelines

## Scoring Mechanics
The parser scores matching tech stacks. Typical ATS parsers match keywords based on lowercase substring intersections:

$$\text{ATS Score} = \frac{\text{Intersections}}{\text{Total Keywords}} \times 100$$

## Keyword Categories
- **Languages**: Python, SQL, C++, TypeScript, Go
- **Frameworks**: FastAPI, React, Streamlit, Next.js
- **Cloud/Databases**: PostgreSQL, Redis, Docker, Kubernetes
- **Methodologies**: LLM Routing, Data Science, CI/CD, Event Loops
