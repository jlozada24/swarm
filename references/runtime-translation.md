# Runtime translation guide

Read this file completely before resolving child runtimes or emitting any implementation or review matrix. Guide version: `2026-09-10`. Model selection is harness-independent; harness resolution verifies the chosen identity, effort, route, and capacity.

## Shared source

The maintained grid lives in Delegate's `SKILL.md`, under **Configure and select models**, including **Selection cases** and **Context capacity and harness resolution**. Read only that section as model-policy data; do not activate Delegate or import its dispatch, freshness, approval, or default-level behavior. Swarm defaults to Budget; Delegate defaults to Performance.

Resolve `model_policy_source` when supplied. Otherwise use the Delegate skill location exposed by the host's skill catalog, or a sibling `../delegate/SKILL.md` relative to the installed Swarm directory. Resolve symlinks before interpreting sibling paths. Require the Budget / Express / Performance / Peak grid and its context rules; a stale scaffold is not a usable source. If unavailable, surface the missing source and request the updated Delegate location before settlement; never recreate a locally maintained grid or silently use an older roster. Record the exact resolved path and content fingerprint with the approved matrix. A source change requires fresh settlement and matrix approval before affected unstarted positions execute.

This dependency is intentional: install or distribute the updated Delegate alongside Swarm, or explicitly supply its accessible checkout path. Do not hard-code a machine-specific worktree into the portable skill. Do not move or use `references/model-matrix.md` as the runtime source: it is the separately maintained comparison snapshot, with locked ratings and measurements.

## Resolution order

1. Map the coordinate to Read, Write, or Task using `SKILL.md`. Resolve its selected level (Budget unless the user chooses otherwise), then read the exact baseline slot from Delegate.
2. Honor an explicit runtime selection for the exact coordinate or named scope, preserving effort and configured subscription, bridge, literal starred identity, or CLI route. These targeted selections take precedence over the baseline and optional arrays, without broadening role authority.
3. Otherwise retain the baseline, with `models` and review-only `review_agents` as additional eligible options. Shared-grid entries retain their role eligibility; an out-of-grid option needs explicit role eligibility and effort from the user. Select an additional option only when a concrete assignment requirement supports it. Listing a model neither forces its use nor overrides all coordinates.
4. Preserve the exact slot effort. A model-only request may take the slot effort only when unambiguous; otherwise resolve it from explicit configuration or clarification. Do not use a different model's effort or a host-specific default roster.
5. Verify the selected identity, effort, route, and required capacity against actual launcher/host information. If unsupported or unverifiable, leave it `unresolved`, surface the evidence, and obtain another approved selection. Never silently substitute or change global configuration.

Apply the shared selection cases: Budget prioritizes cost; Express is a lighter quick-completion option for known procedures or supplied plans with clear checks; Performance handles most work including difficult tasks; Peak requires unusually demanding reasoning identified at initial selection. These are not a routine retry ladder. Existing workflow escalation boundaries remain, using separately approved role coordinates without an automatic model increase.

Apply Delegate's context rules to every Astra Medium and High slot, including eligible options: the 828k alternative is available only when required working context necessitates it, and retains Medium or High respectively. Verify 828,000-token capacity from the host; a handoff request is not capacity evidence. Never invent launcher flags or confuse context capacity with output limits or task token budgets. Ordinary configurations use the verified harness default. Preserve explicit routes across harnesses rather than switching subscriptions or providers for convenience.

The parent orchestrator is already running and is not an assignable child coordinate. Child selections cannot change it retroactively. If a requested parent change cannot be switched and verified in place, surface that a new parent session is required; retain the existing two-slot approval behavior.

## Parent-runtime eligibility

Select the normative parent recommendation from the detected host, not from a child selection or a cross-host model translation:

| Detected host | Normative parent recommendation | Matching-or-stronger eligible runtime |
|---|---|---|
| Codex | Sol High+ | Sol at `high` or higher effort (or a verified stronger host runtime) |
| Claude Code | Opus 5 XHigh or Fable 5 High | Opus 5 at `xhigh`, or Fable 5 at `high` (or a verified stronger host runtime) |
| Cursor | Grok 4.6 XHigh | Grok 4.6 at `xhigh` (or a verified stronger host runtime) |

Inspect and record the host-reported parent model and effort before deciding eligibility. A verified matching-or-stronger runtime marks the orchestrator-bypass slot `not_required`. For a below-recommendation parent, surface `actual: <model>, <effort>`; when the host cannot expose or verify the parent, surface `actual: unknown` together with the evidence of unavailability or unverifiability. In either case, issue the existing quality warning that orchestration, finding adjudication, merge control, and release gating may be weaker, then resolve the required orchestrator-bypass slot together with the matrix-approval slot under `SKILL.md` before creating worktrees, spawning children, or changing repository state.

The required bypass is one approval slot, not an exact-token checkpoint. A user-authored intake `obp` flag or equivalent explicit preauthorization can fill it before the warning/proposal response. If it remains missing after the warning and proposal are emitted, flexible post-proposal language can fill it alone or together with the matrix-approval slot according to `SKILL.md`; do not require a separate message or the literal token `obp`. Record the slot state, evidence, interpretation, message order, and current-run scope. A child runtime selection never satisfies this gate, upgrades an ineligible parent, or changes the already-running parent.

## Matrix recording

Every coordinate records its stable identity, mapped grid role, selected level, role/level baseline, shared source path and fingerprint, detected host, raw user request, resolved model and exact effort, configured route, required capacity and verification evidence, assignment source, and this guide version.

`selection_source` is `grid_baseline`, `eligible_option`, or `user_selected`; `assignment_source` separately identifies a role default, pool, or direct coordinate assignment. Translation class is `exact` when model/effort equal the baseline, `user_selected_nondefault` for a selected additional option or explicit override differing from it, or `unresolved`. There are no implicit cross-provider role equivalents. A matrix cannot execute with unresolved identity, effort, required route, or required capacity.

## User-directed matrix edits

A user may select a model for one coordinate, multiple explicitly named coordinates, a role, slice, wave, or all remaining occurrences. Do not infer a broader scope than the user named. If a role selector could refer to materially different occurrences, list the affected coordinates or ask a concise clarification before settling them.

Requests made before the first proposal appear in that proposal. Any request made after emission invalidates the emitted version and its approval evidence. Finish runtime discussion, resolve every affected position, then emit the complete affected matrix. Only a user approval sent after that settled matrix authorizes execution.

A mid-run request changes only unstarted positions. Do not claim that an active or completed agent used a newly requested runtime. Restarting or repeating one requires explicit replan authority, a settled remaining-work matrix, and new approval.
