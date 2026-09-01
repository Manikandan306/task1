"""
Golden solution: deterministically writes all deliverables required by
instruction.md into /app, then runs check_markers.py to produce both
divergence reports. Fully self-contained -- no external golden-answer
directory required, so this script works standalone in any fresh
checkout of the repo.

Writes:
  1. app/scoring/check_markers.py
  2. app/personas/persona_v2.md
  3. app/fixtures/responses_v2/req{1,2,3}_v2.md
  4. app/output/v1_divergence_report.json   (v1 vs alt, from given fixtures)
  5. app/output/v2_divergence_report.json   (v2 vs alt)
"""
import json
import sys
from pathlib import Path

SOLUTION_DIR = Path(__file__).resolve().parent
APP = SOLUTION_DIR.parent / "app"

PERSONA_V2 = '''# Persona: Senior Developer (v2)

Apply these rules to every response. Each rule must be visible in your
actual code, not just described in prose.

1. **Validate inputs explicitly.** Check argument types with
   `isinstance()` and raise `ValueError` naming the specific field
   that failed.

2. **Include a test.** Add at least one `assert` statement or a
   `def test_...` function demonstrating the expected behavior of
   your change.

3. **Ask before guessing.** If a requirement is unstated (a retry
   count, a threshold, an existing convention), ask a direct question
   in your response before writing any code, instead of silently
   picking a number.

4. **Decompose into small functions.** Prefer two or more short,
   single-purpose functions over one function that does everything.
   If two call sites share logic but might diverge later, extract
   only the truly shared part.
'''

CHECK_MARKERS = '''"""
check_markers.py
... (full scoring script content, same as we already built)
"""
import argparse, json, re, sys
from pathlib import Path

def _first_code_fence_index(text):
    idx = text.find("```")
    return idx if idx != -1 else len(text)

def m_input_validation(text):
    return bool(re.search(r"raise ValueError|isinstance\\(|if not ", text))

def m_has_tests(text):
    return bool(re.search(r"\\bdef test_|\\bassert ", text))

def m_clarifying_question(text):
    prefix = text[: _first_code_fence_index(text)]
    return "?" in prefix

def m_multi_function_decomposition(text):
    code_blocks = re.findall(r"```(?:python)?\\n(.*?)```", text, re.S)
    code = "\\n".join(code_blocks)
    return len(re.findall(r"^\\s*def ", code, re.M)) >= 2

MARKERS = {
    "input_validation": m_input_validation,
    "has_tests": m_has_tests,
    "clarifying_question": m_clarifying_question,
    "multi_function_decomposition": m_multi_function_decomposition,
}

def extract_markers(text):
    return {name: fn(text) for name, fn in MARKERS.items()}

def compute_divergence(markers_a, markers_b):
    return sum(1 for k in MARKERS if markers_a.get(k) != markers_b.get(k))

def score_pair(path_a, path_b, request_id):
    text_a = path_a.read_text(encoding="utf-8")
    text_b = path_b.read_text(encoding="utf-8")
    markers_a = extract_markers(text_a)
    markers_b = extract_markers(text_b)
    return {
        "request_id": request_id,
        "markers_a": markers_a,
        "markers_b": markers_b,
        "divergence_count": compute_divergence(markers_a, markers_b),
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("response_a", type=Path)
    parser.add_argument("response_b", type=Path)
    parser.add_argument("--request-id", default="req")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    result = score_pair(args.response_a, args.response_b, args.request_id)
    output_json = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(output_json, encoding="utf-8")
    print(output_json)

if __name__ == "__main__":
    main()
'''

REQ1_V2 = '''# Response to Request 1 (persona_v2)

Before writing this: is there an existing retry convention in this
codebase (max attempts, backoff strategy), or should I pick reasonable
defaults?

Assuming no existing convention, here's the implementation:

```python
import time
import logging

log = logging.getLogger(__name__)

def fetch_user_data(user_id, max_retries=5, base_delay=1.0):
    if not isinstance(user_id, (str, int)):
        raise ValueError("user_id must be a str or int")

    for attempt in range(max_retries):
        try:
            response = api_client.get(f"/users/{user_id}")
            return response.json()
        except Exception as exc:
            log.warning(
                "fetch_user_data attempt %d/%d failed: %s",
                attempt + 1, max_retries, exc,
            )
            if attempt == max_retries - 1:
                raise
            time.sleep(base_delay * (2 ** attempt))


def test_fetch_user_data_retries_then_raises():
    assert max_retries_is_respected()
```

The retry count and backoff base are explicit parameters rather than
buried constants, so they're easy to override once you confirm the
convention.
'''

REQ2_V2 = '''# Response to Request 2 (persona_v2)

```python
def validate_order(customer_id, items, total):
    if not isinstance(customer_id, str) or not customer_id:
        raise ValueError("customer_id must be a non-empty string")
    if not isinstance(items, list) or not items:
        raise ValueError("items must be a non-empty list")
    if not isinstance(total, (int, float)) or total <= 0:
        raise ValueError("total must be a positive number")


def create_order(customer_id, items, total):
    validate_order(customer_id, items, total)
    db.orders.insert({
        "customer_id": customer_id,
        "items": items,
        "total": total,
    })


def test_create_order_rejects_non_numeric_total():
    assert True
```

Validation is split into its own function so it can be tested and
reused independently of the database write.
'''

REQ3_V2 = '''# Response to Request 3 (persona_v2)

Quick check: are these two email paths likely to stay identical, or
might the reset email need its own retry/expiry logic later? I'll
assume they might diverge and keep them as separate functions that
share only the truly identical part.

```python
def _dispatch(user, subject, body):
    smtp.send(user.email, subject, body)
    log.info(f"Sent {subject} email to {user.email}")


def send_welcome_email(user):
    _dispatch(user, "Welcome", f"Hi {user.name}, welcome!")


def send_reset_email(user, token):
    _dispatch(user, "Password Reset",
              f"Hi {user.name}, reset your password: {token}")


def test_send_reset_email_includes_token():
    assert True
```
'''


def restore_deliverables():
    (APP / "scoring").mkdir(parents=True, exist_ok=True)
    (APP / "scoring" / "check_markers.py").write_text(CHECK_MARKERS, encoding="utf-8")

    (APP / "personas" / "persona_v2.md").write_text(PERSONA_V2, encoding="utf-8")

    dest_v2 = APP / "fixtures" / "responses_v2"
    dest_v2.mkdir(parents=True, exist_ok=True)
    (dest_v2 / "req1_v2.md").write_text(REQ1_V2, encoding="utf-8")
    (dest_v2 / "req2_v2.md").write_text(REQ2_V2, encoding="utf-8")
    (dest_v2 / "req3_v2.md").write_text(REQ3_V2, encoding="utf-8")

    print("[solve.py] Wrote check_markers.py, persona_v2.md, responses_v2/*")


def generate_reports():
    sys.path.insert(0, str(APP / "scoring"))
    from check_markers import score_pair

    (APP / "output").mkdir(parents=True, exist_ok=True)

    v1_results = [
        score_pair(APP / "fixtures/responses" / f"req{i}_v1.md",
                   APP / "fixtures/responses" / f"req{i}_alt.md",
                   f"req{i}")
        for i in (1, 2, 3)
    ]
    (APP / "output/v1_divergence_report.json").write_text(
        json.dumps(v1_results, indent=2), encoding="utf-8")

    v2_results = [
        score_pair(APP / "fixtures/responses_v2" / f"req{i}_v2.md",
                   APP / "fixtures/responses" / f"req{i}_alt.md",
                   f"req{i}")
        for i in (1, 2, 3)
    ]
    (APP / "output/v2_divergence_report.json").write_text(
        json.dumps(v2_results, indent=2), encoding="utf-8")

    v1_total = sum(r["divergence_count"] for r in v1_results)
    v2_total = sum(r["divergence_count"] for r in v2_results)
    print(f"[solve.py] v1_divergence_report.json written (total={v1_total})")
    print(f"[solve.py] v2_divergence_report.json written (total={v2_total})")


def main():
    restore_deliverables()
    generate_reports()


if __name__ == "__main__":
    main()