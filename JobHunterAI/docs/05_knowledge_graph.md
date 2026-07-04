# 05 - Career Knowledge Graph

## Relationship Graph
Everything in the candidate's career is structured as a connected graph to enable traceability from source evidence (PRs/commits) to job offers:

```
[Evidence] -> [Skills] -> [Projects] -> [Experience] -> [Resume Bullet] -> [Resume Version] -> [Application] -> [Interview] -> [Offer]
```

## Traceability Protocol
- **Evidence Node**: The root of the system. Represents a single merged PR, commit SHA, spec document, or deployment URL.
- **Skills Node**: Tech stacks are linked directly to projects and experiences.
- **Project/Experience Node**: Career achievements. Surfaced during database query rank based on job description overlap.
- **Resume Bullet Node**: Dynamically generated bullet points. Must contain an evidence ID trace tag to be compiled.
- **Application Node**: Ties the compiled resume version to recruiter communication logs and final offers.
