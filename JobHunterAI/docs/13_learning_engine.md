# 13 - Learning Engine

## Learning Loop Strategy
The system updates weights based on application outcomes.

```
[Application Outcome] -> [Update CRM Table] -> [Adjust Template Weights] -> [Improve Future Matches]
```

## Adjustments Heuristic
- **Template Performance**: Tracks the conversion rate of specific resume styles (e.g. backend vs. frontend).
- **Match Tuning**: If a project repeatedly appears on resumes that convert to interviews, the ranking engine weights that project's skills higher in future calculations.
- **Skill Demand Analysis**: Tracks the most commonly requested skills across all discovered postings, suggesting target languages and tools to study.
