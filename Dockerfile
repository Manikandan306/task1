FROM python:3.11-slim

WORKDIR /app

COPY app/personas/persona_v1.md /app/personas/persona_v1.md
COPY app/personas/persona_alt.md /app/personas/persona_alt.md
COPY app/requests/ /app/requests/
COPY app/fixtures/responses/ /app/fixtures/responses/

CMD ["/bin/bash"]
