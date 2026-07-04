# 07 - Resume Compiler

## LaTeX Jinja Delimiters
Standard Jinja braces (`{{` and `}}`) conflict with LaTeX formatting. The compiler utilizes custom delimiters configured in `engines/compiler.py`:

- **Block Start**: `\BLOCK{`
- **Block End**: `}`
- **Variable Start**: `\VAR{`
- **Variable End**: `}`
- **Comment Start**: `\#{`
- **Comment End**: `}`

## Compilation Workflow
1. The compiler retrieves the configured template (e.g. `backend.tex`) from the `templates/` folder.
2. Jinja2 renders the LaTeX string with the tailored projects, skills, and experiences.
3. The raw source is saved under `data/generated/`.
4. If `pdflatex` is available, the orchestrator invokes a subprocess to compile the source into a machine-readable PDF document. If pdflatex is missing, it logs a warning.
