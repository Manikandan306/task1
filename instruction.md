# Task: Detect and Fix Overgeneralization in a Developer Persona

## Working directory
/app

## What's provided
- `/app/personas/persona_v1.md` — a system prompt describing a developer persona
- `/app/personas/persona_alt.md` — a different, equally plausible developer persona
- `/app/requests/request_1.md`, `request_2.md`, `request_3.md` — three coding requests
- `/app/fixtures/responses/` — pre-recorded responses: for each request, one response
  written under persona_v1's instructions and one written under persona_alt's
  instructions, named `req{N}_v1.md` and `req{N}_alt.md`

## What you must produce
1. `/app/scoring/check_markers.py` — a script that, given two response files, extracts
   at least 4 named behavioral markers (e.g. presence of input validation, presence
   of tests, whether a clarifying question is asked, function decomposition style) and
   outputs a divergence count: how many of the markers differ between the two responses.
2. `/app/output/v1_divergence_report.json` — the result of running your scoring script
   against all 3 request pairs in `/app/fixtures/responses/` (persona_v1 vs persona_alt).
3. `/app/personas/persona_v2.md` — a rewritten version of persona_v1 that replaces vague
   adjective-based traits with specific, behaviorally checkable traits.
4. `/app/fixtures/responses_v2/` — for each of the 3 requests, write the response you
   believe persona_v2 would produce, following persona_v2's stated traits exactly.
5. `/app/output/v2_divergence_report.json` — the result of running your scoring script
   against persona_v2's responses vs persona_alt's responses (same 3 requests).

## Constraints
- Your scoring script must not call any external API or network resource.
- Marker checks must be based on textual/structural properties of the response files
  (e.g. presence of specific keywords, code patterns, question marks before any code
  block) — not subjective judgment calls.
- `persona_v2.md` must be under 200 words.
- All output JSON must follow this schema:
  `{"request_id": str, "markers_a": {...}, "markers_b": {...}, "divergence_count": int}`
  as a list of 3 objects.

## Success criteria (evaluated automatically)
- `v1_divergence_report.json` shows total divergence ≤ 1 across all 3 requests.
- `v2_divergence_report.json` shows total divergence ≥ 3 across all 3 requests.
- `persona_v2.md` is present, under the word limit, and none of its trait
  descriptions match a list of banned generic adjectives.

You have 1800 seconds to complete this task.


del app\personas\persona_v2.md
rmdir /s /q app\fixtures\responses_v2
rmdir /s /q app\scoring
rmdir /s /q app\output

docker build -t task01 .

docker run -v "%cd%\tests:/app_tests" -v "%cd%\app:/app" task06 python3 /app_tests/eval.py

docker run -v "%cd%\solution:/app_solution" -v "%cd%\app:/app" task06 python3 /app_solution/solve.py

docker run -v "%cd%\tests:/app_tests" -v "%cd%\app:/app" task06 python3 /app_tests/eval.py