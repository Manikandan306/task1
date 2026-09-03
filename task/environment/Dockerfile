FROM public.ecr.aws/docker/library/python:3.11-slim@sha256:9534e5a8e315485d4061ed659af0fd78a284c015f9b73661b41d6bab25604534

WORKDIR /app

RUN pip install --no-cache-dir --break-system-packages pytest==8.4.1

COPY data/personas/persona_v1.md /app/personas/persona_v1.md
COPY data/personas/persona_alt.md /app/personas/persona_alt.md
COPY data/requests/ /app/requests/
COPY data/fixtures/responses/ /app/fixtures/responses/

RUN mkdir -p /app/personas /app/scoring /app/fixtures/responses_v2 /app/output