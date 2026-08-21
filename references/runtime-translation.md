# Runtime translation guide

Read this file completely before resolving child runtimes or emitting any implementation or review matrix. This guide is version `2026-08-21`. Its mappings are operational role equivalents for Luna Swarm, not claims that models from different providers are identical.

## Resolution order

Resolve every child runtime coordinate independently:

1. Use an explicit user selection for the exact coordinate or explicitly named set of coordinates.
2. Otherwise use the canonical roster default on Codex or the dated host-native mapping below on Claude Code or Cursor.
3. If the model is known but the user omitted effort or speed, apply the role-specific values below and record that they came from this guide.
4. If the host cannot expose or honor the resolved model or effort, leave the coordinate `unresolved`, surface exact evidence, and wait for a user selection. Never silently substitute another runtime.
5. If only speed cannot be enforced, surface the required nonblocking disclosure, record requested and resolved behavior, and continue with the approved model and effort.

The parent orchestrator is already running and is not an assignable child coordinate. Detect its host and evaluate its actual runtime using the parent-runtime eligibility rules below. Never claim a child-matrix edit changed the parent retroactively. If the user requests another parent runtime and the host cannot switch and verify it in place, surface that a new parent session is required; the current session still follows the eligibility and `obp` rules below.

## Parent-runtime eligibility

Select the normative parent recommendation from the detected host, not from a child selection or a cross-host model translation:

| Detected host | Normative parent recommendation | Matching-or-stronger eligible runtime |
|---|---|---|
| Codex | Sol High+ | Sol at `high` or higher effort (or a verified stronger host runtime) |
| Claude Code | Opus 5 XHigh or Fable 5 High | Opus 5 at `xhigh`, or Fable 5 at `high` (or a verified stronger host runtime) |
| Cursor | Grok 4.6 XHigh | Grok 4.6 at `xhigh` (or a verified stronger host runtime) |

Inspect and record the host-reported parent model and effort before deciding eligibility. A verified matching-or-stronger runtime continues without a bypass. For a below-recommendation parent, surface `actual: <model>, <effort>`; when the host cannot expose or verify the parent, surface `actual: unknown` together with the evidence of unavailability or unverifiability. In either case, issue the existing quality warning that orchestration, finding adjudication, merge control, and release gating may be weaker, then hard-pause before creating worktrees, spawning children, or changing repository state.

The only bypass is a one-time `obp` acknowledgement: the immediately following user message, after trimming surrounding whitespace, must consist entirely of lowercase `obp`. Do not accept an `obp` in the invoking prompt, an earlier message, a quoted example, preauthorization, generic approval, or any longer response. If the next message is not exactly `obp`, reissue the warning and require a newly following exact `obp`; record the warning, acknowledgement, message order, and current-run scope. A child runtime selection never satisfies this gate, upgrades an ineligible parent, or changes the already-running parent.

## Dated role mappings

| Responsibility | Codex baseline | Claude Code | Cursor native |
|---|---|---|---|
| Bounded builder | Luna Max (`gpt-5.6-luna`, `max`) | Sonnet 5 (`claude-sonnet-5`, `high`) | Composer 2.5 Standard (`composer-2.5`, adaptive effort, non-fast); Grok 4.6 (`grok-4.6`, `medium`, non-fast) when explicitly selected |
| File-level adversarial, overengineering, style, post-fix, or non-escalated remediation reviewer | Luna Max (`gpt-5.6-luna`, `max`) | Opus 5 (`claude-opus-5`, `medium`) | Grok 4.6 (`grok-4.6`, `high`, non-fast) |
| Ordinary fixer or non-escalated remediation fixer | Luna Max (`gpt-5.6-luna`, `max`) | Sonnet 5 (`claude-sonnet-5`, `high`) | Composer 2.5 Standard (`composer-2.5`, adaptive effort, non-fast) |
| Strong or escalated builder | Sol High (`gpt-5.6-sol`, `high`) | Opus 5 (`claude-opus-5`, `high`) | Grok 4.6 (`grok-4.6`, `high`, non-fast) |
| Escalated reviewer/fixer or integrated/final reviewer | Sol XHigh (`gpt-5.6-sol`, `xhigh`) | Opus 5 (`claude-opus-5`, `xhigh`) | Grok 4.6 (`grok-4.6`, `xhigh`, non-fast) |
| Parent orchestrator recommendation | Sol High or higher | Opus 5 XHigh or Fable 5 High | Grok 4.6 XHigh |

For Cursor-native bounded work, prefer Composer 2.5 Standard by default. Grok 4.6 Medium is an explicitly selectable, overqualified bounded-work alternative rather than evidence that Grok belongs to Luna's model tier. For Cursor-native difficult building, adjudication, or integrated review, use the Grok High or XHigh mappings shown above.

## Matrix recording

Every runtime coordinate must record:

- stable coordinate;
- canonical roster default;
- detected host;
- raw user request, if any;
- resolved model, effort, and requested/resolved speed behavior;
- selection source: `roster_default`, `translation_guide`, or `user_selected`;
- translation class: `exact`, `vetted_role_equivalent`, `user_selected_nondefault`, or `unresolved`;
- this guide version.

Use `exact` only when the resolved model and effort equal the canonical roster default. Use `vetted_role_equivalent` only for a mapping in the dated table. Use `user_selected_nondefault` for an available user choice that differs from both. A position remains `unresolved` until model and effort are concrete and supported; an unresolved matrix cannot execute.

## User-directed matrix edits

A user may select a model for one coordinate, multiple explicitly named coordinates, a role, slice, wave, or all remaining occurrences. Do not infer a broader scope than the user named. If a role selector could refer to materially different occurrences, list the affected coordinates or ask a concise clarification before settling them.

Requests made before the first proposal appear in that proposal. Any request made after emission invalidates the emitted version and its approval evidence. Finish runtime discussion, resolve every affected position, then emit the complete affected matrix. Only a user approval sent after that settled matrix authorizes execution.

A mid-run request changes only unstarted positions. Do not claim that an active or completed agent used a newly requested runtime. Restarting or repeating one requires explicit replan authority, a settled remaining-work matrix, and new approval.
