# 06 - Programmatic Rule Engine

## Rules and Invariants
To prevent hallucinations and protect credibility, the following rules are enforced programmatically in Python code and cannot be modified by the LLM:

1. **The ADEN Rule**: Any experience with `is_open_source=True` must lock the role name to exactly `"Open Source Contributor"`.
2. **Metadata Integrity**: Experience start dates, end dates, and company names cannot be altered by the generator.
3. **No Fluff**: Cover letters must open directly with a tech stack, product, or news connection. Opening phrases like "I am excited to apply" are rejected.
4. **Factual Grounding**: Every tailored bullet point must reference a valid evidence ID (e.g. PR #142) found in the database.
5. **Wording Audit**: Rejects the file if open-source experiences contain forbidden indicators implying core employee status (e.g. salary, employee, staff engineer).
