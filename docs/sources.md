# Dataset Sources — Smart Library Book Discovery Chatbot

## Primary Source
- **Name**: [School Name] Library OPAC
- **URL / Location**: [URL or "on-site catalog terminal"]
- **Access method**: [export / manual copy / screenshot + typing]
- **Date collected**: [YYYY-MM-DD]
- **Date verified**: [YYYY-MM-DD]
- **Verified by**: [Librarian Name]
- **Permission**: [Verbal / written permission from librarian]

## Test Query Source (Blind Set)
- **File**: `data/test_queries.csv`
- **Authors**: Group members (each writes 10 queries independently)
- **Rule**: None of these queries appear in `books.csv` or in the dev set.

## Team-Written Resources
- `data/synonyms.json` — authored by the group
- `data/difficulty_rules.json` — authored by the group
- `docs/data_dictionary.md`, `docs/cleaning_rules.md` — authored by the group

## Known Limitations
- Some records may lack `description`.
- Availability may be outdated.
- Categories were normalized to a controlled vocabulary; some nuance is lost.