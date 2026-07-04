# 14 - Testing Framework

## Unit Testing
Testing uses Python's built-in `unittest` module, keeping the suite free of external test dependencies.

## Key Test Cases
- **Seeding Test**: Verifies SQLite tables and candidate graph mappings.
- **Scoring Test**: Evaluates deterministic job scoring algorithms against JDs.
- **ATS Intersection Test**: Validates ATS keyword matching scoring.
- **Rule Engine Test**: Enforces title locks, block dates, and open-source role assertions.

## Execution
Run tests from the root directory:
```bash
$env:PYTHONPATH="."
python -m unittest tests/test_pipeline.py
```
