# 08 - ATS Optimization Loop

## ATS Scoring Formula
The ATS score computes the percentage of job keywords present in the candidate's active resume bullets:

$$\text{ATS Score} = \left( \frac{\text{Keywords Matched}}{\text{Total Keywords Extracted}} \right) \times 100$$

## Optimization Sequence
```
[Initial Bullets] -> [Calculate ATS Score] -> [If Score >= 90% -> Terminate]
         ▲                                                 │
         │ (Iterate up to 3 times)                         ▼ (If < 90%)
  [Parse Rewritten] <----------------------------- [LLM Keyword Rewrite]
```

## Safety Invariant
During rewrites, the prompt strictly forbids fabricating work. It must only rephrase existing experience to highlight technologies actually used.
