"""
Deterministic binary verifier for Task_06, matching instruction.md's
"Success criteria (evaluated automatically)" exactly:

  1. v1_divergence_report.json shows total divergence <= 1 across all 3 requests.
  2. v2_divergence_report.json shows total divergence >= 3 across all 3 requests.
  3. persona_v2.md is present, under the word limit, and none of its trait
     descriptions match a list of banned generic adjectives.

Exit 0 on pass, non-zero on failure. No network access.
"""
import json
import re
import sys
from pathlib import Path

APP = Path(__file__).resolve().parent.parent / "app"

V1_REPORT = APP / "output" / "v1_divergence_report.json"
V2_REPORT = APP / "output" / "v2_divergence_report.json"
PERSONA_V2 = APP / "personas" / "persona_v2.md"

V1_MAX_TOTAL = 1
V2_MIN_TOTAL = 3
WORD_LIMIT = 200

BANNED_ADJECTIVES = [
    "thoughtful", "thorough", "pragmatic", "meticulous", "diligent",
    "careful", "skilled", "experienced", "clean", "conscientious",
    "detail-oriented", "quality-focused", "professional", "expert",
    "knowledgeable", "seasoned", "polished", "rigorous",
]

REQUIRED_SCHEMA_KEYS = {"request_id", "markers_a", "markers_b", "divergence_count"}


def fail(msg: str):
    print(f"FAIL: {msg}")
    sys.exit(1)


def load_report(path: Path) -> list:
    if not path.exists():
        fail(f"missing file {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path} is not valid JSON: {exc}")
    if not isinstance(data, list) or len(data) != 3:
        fail(f"{path} must be a list of exactly 3 objects, got {type(data)} "
             f"len={len(data) if isinstance(data, list) else 'n/a'}")
    for i, entry in enumerate(data):
        if not REQUIRED_SCHEMA_KEYS.issubset(entry.keys()):
            fail(f"{path} entry {i} missing required keys "
                 f"(need {REQUIRED_SCHEMA_KEYS}, got {set(entry.keys())})")
        if not isinstance(entry["divergence_count"], int):
            fail(f"{path} entry {i}: divergence_count must be an int")
    return data


def check_persona_v2():
    if not PERSONA_V2.exists():
        fail(f"missing file {PERSONA_V2}")

    text = PERSONA_V2.read_text(encoding="utf-8")
    word_count = len(text.split())
    if word_count >= WORD_LIMIT:
        fail(f"persona_v2.md is {word_count} words, must be under {WORD_LIMIT}")

    lowered = text.lower()
    hits = [w for w in BANNED_ADJECTIVES if re.search(rf"\b{re.escape(w)}\b", lowered)]
    if hits:
        fail(f"persona_v2.md contains banned generic adjectives: {hits}")

    print(f"persona_v2.md OK ({word_count} words, no banned adjectives)")


def main():
    v1_data = load_report(V1_REPORT)
    v1_total = sum(e["divergence_count"] for e in v1_data)
    print(f"v1 total divergence: {v1_total} (need <= {V1_MAX_TOTAL})")
    if v1_total > V1_MAX_TOTAL:
        fail(f"v1 total divergence {v1_total} exceeds max {V1_MAX_TOTAL} "
             f"-- persona_v1 wasn't shown to be overgeneralized")

    v2_data = load_report(V2_REPORT)
    v2_total = sum(e["divergence_count"] for e in v2_data)
    print(f"v2 total divergence: {v2_total} (need >= {V2_MIN_TOTAL})")
    if v2_total < V2_MIN_TOTAL:
        fail(f"v2 total divergence {v2_total} below min {V2_MIN_TOTAL} "
             f"-- rewrite did not produce a real behavioral change")

    check_persona_v2()

    print("PASS: v1 confirmed overgeneralized "
          f"(total={v1_total}); v2 shows real divergence (total={v2_total}); "
          "persona_v2.md meets format constraints.")
    sys.exit(0)


if __name__ == "__main__":
    main()