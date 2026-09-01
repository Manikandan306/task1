## Proposal: Detect and fix overgeneralization in a developer persona
## 1. Task

Task: Detect and fix overgeneralization in a developer persona
Goal: Prove a "senior developer" persona is too generic to predict any actual decision, then rewrite it so it isn't.

## Category

Category: LLM / Prompt Engineering
Sub-category: System Prompt Tuning / Persona

## Difficulty

Personas like "senior engineer who cares about quality" read fine on the page but don't predict any actual decision — and you can't tell that by reading, only by testing. Run two different personas against the same request and most of the time their outputs are indistinguishable, but nobody checks. Even rewritten "specific-sounding" traits ("thoughtful, thorough") often still fail this test — specific-sounding isn't the same as decision-relevant. ~Half a day for someone who's written a few of these; the hard part is building a test honest enough to catch your own first draft.

## Intended Approach

Write an overgeneralized persona as a control. Pick a second, equally plausible persona. Run both against the same 3 coding requests and diff the outputs. Near-zero difference = overgeneralized, regardless of how it reads. Rewrite it trait-by-trait, where each trait is something checkable in actual output (writes the failing test first, stops to ask before guessing) instead of an adjective. Re-run the same 3 requests and confirm the outputs now diverge from the alternative persona.

## Verification

- Different actual output (code + reasoning) across 2 personas × 3 requests.
- Pass: v1 shows ~no divergence (proves generic); v2 shows real divergence on ≥1 of 3 (proves the fix worked).
- Anti-cheat: adding adjectives without behavioral change still fails — only actual output differences count.
- Outcome-only grading: any rewrite producing real divergence passes.

