# Architecture Patterns

## Separation of Concerns
1. **Deterministic Logic**: DB queries, graph traversal, and keyword calculations are kept in Python code.
2. **Generative Logic**: LLM prompt execution is reserved strictly for language generation.
3. **Registry**: Prompts are stored in the `prompts/` directory to separate system logic from generative instruction.
