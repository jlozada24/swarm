# Runtime translation guide

Read this file completely before resolving child runtimes or emitting any implementation or review matrix. This guide is version `2026-08-26`. Its mappings are operational role equivalents for Luna Swarm, not claims that models from different providers are identical.

## Resolution order

Resolve every child runtime coordinate independently:

1. Use an explicit user selection for the exact coordinate or explicitly named set of coordinates.
2. Otherwise use the canonical roster default on Codex or the dated host-native mapping below on Claude Code or Cursor.
3. If the model is known but the user omitted effort, apply the role-specific value below and record that it came from this guide.
4. If the host cannot expose or honor the resolved model or effort, leave the coordinate `unresolved`, surface exact evidence, and wait for a user selection. Never silently substitute another runtime.

An entry in review-mode `review_agents` is not an explicit selection under step 1. It is an additional eligible pool, and the review-mode reference requires the orchestrator to retain the built-in Luna Max pool and choose a supplied option only when it is likely to improve the outcome for a concrete slice. A direct user instruction assigning a runtime to named coordinates or scope remains an explicit selection.

The parent orchestrator is already running and is not an assignable child coordinate. Detect its host and evaluate its actual runtime using the parent-runtime eligibility rules below. Never claim a child-matrix edit changed the parent retroactively. If the user requests another parent runtime and the host cannot switch and verify it in place, surface that a new parent session is required; the current session still follows the two-slot approval rules below.

## Parent-runtime eligibility

Select the normative parent recommendation from the detected host, not from a child selection or a cross-host model translation:

| Detected host | Normative parent recommendation | Matching-or-stronger eligible runtime |
|---|---|---|
| Codex | Sol High+ | Sol at `high` or higher effort (or a verified stronger host runtime) |
| Claude Code | Opus 5 XHigh or Fable 5 High | Opus 5 at `xhigh`, or Fable 5 at `high` (or a verified stronger host runtime) |
| Cursor | Grok 4.6 XHigh | Grok 4.6 at `xhigh` (or a verified stronger host runtime) |

Inspect and record the host-reported parent model and effort before deciding eligibility. A verified matching-or-stronger runtime marks the orchestrator-bypass slot `not_required`. For a below-recommendation parent, surface `actual: <model>, <effort>`; when the host cannot expose or verify the parent, surface `actual: unknown` together with the evidence of unavailability or unverifiability. In either case, issue the existing quality warning that orchestration, finding adjudication, merge control, and release gating may be weaker, then resolve the required orchestrator-bypass slot together with the matrix-approval slot under `SKILL.md` before creating worktrees, spawning children, or changing repository state.

The required bypass is one approval slot, not an exact-token checkpoint. A user-authored intake `obp` flag or equivalent explicit preauthorization can fill it before the warning/proposal response. If it remains missing after the warning and proposal are emitted, flexible post-proposal language can fill it alone or together with the matrix-approval slot according to `SKILL.md`; do not require a separate message or the literal token `obp`. Record the slot state, evidence, interpretation, message order, and current-run scope. A child runtime selection never satisfies this gate, upgrades an ineligible parent, or changes the already-running parent.

## Dated role mappings

| Responsibility | Codex baseline | Claude Code | Cursor native |
|---|---|---|---|
| Bounded builder | Luna Max (`gpt-5.6-luna`, `max`) | Sonnet 5 (`claude-sonnet-5`, `high`) | Composer 2.5 Standard (`composer-2.5`, adaptive effort); Grok 4.6 (`grok-4.6`, `medium`) when explicitly selected |
| File-level adversarial, overengineering, style, post-fix, or non-escalated remediation reviewer | Luna Max (`gpt-5.6-luna`, `max`) | Opus 5 (`claude-opus-5`, `medium`) | Grok 4.6 (`grok-4.6`, `high`) |
| Ordinary fixer or non-escalated remediation fixer | Luna Max (`gpt-5.6-luna`, `max`) | Sonnet 5 (`claude-sonnet-5`, `high`) | Composer 2.5 Standard (`composer-2.5`, adaptive effort) |
| Strong or escalated builder | Sol High (`gpt-5.6-sol`, `high`) | Opus 5 (`claude-opus-5`, `high`) | Grok 4.6 (`grok-4.6`, `high`) |
| Escalated reviewer/fixer or integrated/final reviewer | Sol XHigh (`gpt-5.6-sol`, `xhigh`) | Opus 5 (`claude-opus-5`, `xhigh`) | Grok 4.6 (`grok-4.6`, `xhigh`) |
| Parent orchestrator recommendation | Sol High or higher | Opus 5 XHigh or Fable 5 High | Grok 4.6 XHigh |

For Cursor-native bounded work, prefer Composer 2.5 Standard by default. Grok 4.6 Medium is an explicitly selectable, overqualified bounded-work alternative rather than evidence that Grok belongs to Luna's model tier. For Cursor-native difficult building, adjudication, or integrated review, use the Grok High or XHigh mappings shown above.

## Matrix recording

Every runtime coordinate must record:

- stable coordinate;
- canonical roster default;
- detected host;
- raw user request, if any;
- resolved model and effort;
- selection source: `roster_default`, `translation_guide`, or `user_selected`;
- translation class: `exact`, `vetted_role_equivalent`, `user_selected_nondefault`, or `unresolved`;
- this guide version.

Use `exact` only when the resolved model and effort equal the canonical roster default. Use `vetted_role_equivalent` only for a mapping in the dated table. Use `user_selected_nondefault` for an available user choice that differs from both. A position remains `unresolved` until model and effort are concrete and supported; an unresolved matrix cannot execute.

## User-directed matrix edits

A user may select a model for one coordinate, multiple explicitly named coordinates, a role, slice, wave, or all remaining occurrences. Do not infer a broader scope than the user named. If a role selector could refer to materially different occurrences, list the affected coordinates or ask a concise clarification before settling them.

Requests made before the first proposal appear in that proposal. Any request made after emission invalidates the emitted version and its approval evidence. Finish runtime discussion, resolve every affected position, then emit the complete affected matrix. Only a user approval sent after that settled matrix authorizes execution.

A mid-run request changes only unstarted positions. Do not claim that an active or completed agent used a newly requested runtime. Restarting or repeating one requires explicit replan authority, a settled remaining-work matrix, and new approval.
