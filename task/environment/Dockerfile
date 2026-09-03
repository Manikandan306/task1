FROM public.ecr.aws/docker/library/python:3.11-slim@sha256:PASTE_REAL_DIGEST_HERE

WORKDIR /app

RUN pip install --no-cache-dir --break-system-packages pytest==8.4.1

COPY environment/data/personas/persona_v1.md /app/personas/persona_v1.md
COPY environment/data/personas/persona_alt.md /app/personas/persona_alt.md
COPY environment/data/requests/ /app/requests/
COPY environment/data/fixtures/responses/ /app/fixtures/responses/

RUN mkdir -p /app/personas /app/scoring /app/fixtures/responses_v2 /app/output