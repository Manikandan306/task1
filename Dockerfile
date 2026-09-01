FROM python:3.11-slim

WORKDIR /app

# Given task files
COPY app/personas/persona_v1.md /app/personas/persona_v1.md
COPY app/personas/persona_alt.md /app/personas/persona_alt.md
COPY app/requests/ /app/requests/
COPY app/fixtures/responses/ /app/fixtures/responses/

# Your solved deliverables
COPY app/personas/persona_v2.md /app/personas/persona_v2.md
COPY app/scoring/ /app/scoring/
COPY app/fixtures/responses_v2/ /app/fixtures/responses_v2/
COPY app/output/ /app/output/

# Task documentation, grader, and reference solution
COPY instruction.md /instruction.md
COPY tests/ /tests/
COPY solution/ /solution/

CMD ["/bin/bash"]