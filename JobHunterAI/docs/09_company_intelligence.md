# 09 - Company Intelligence

## Extraction Targets
The Company Intelligence Engine researches and gathers key facts about target firms to customize outreach and cover letters:

- **Funding Stage & Amount**: Series A, B, C or Bootstrapped.
- **Venture Backing**: Active investors, Y Combinator affiliation.
- **Tech Stack**: Extracted from the engineering blog or job description requirements.
- **Products**: Key commercial offerings.
- **Recent News**: Dynamic announcements, updates, or releases used to hook cover letters.

## Data Schemas
Data is validated using Pydantic's `CompanyProfile` model, ensuring JSON formats conform to required schemas before ingestion.
