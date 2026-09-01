# Review-only mode

Read this file completely whenever `review_mode: true`. This is the normative review-only execution branch. Where it conflicts with an implementation instruction in `SKILL.md`, this file controls.

## Resolved behavior

`review_mode` defaults to `false`. When `true`, it is a shorthand preset with these resolved properties:

```yaml
review_mode: true
simple_mode: true
best_of_n: not_applicable(review_mode)
pipeline_waves: not_applicable(review_mode)
primary_role: slice_reviewer
workspace_policy: shared_review_snapshot
source_writes_allowed: false
verification_artifact_writes: isolated_only
followup_roles_allowed: false
```

- Record requested and resolved values. If the invocation explicitly supplied `simple_mode: false`, surface that review mode resolved it to `true`; do not reject or silently conceal the resolution.
- `worktree_mode` is an implementation-only control. Record any requested value and resolve it to `not_applicable(review_mode)`. Never create per-slice implementation worktrees. The only reviewer-specific worktree permitted is the disposable verification worktree required below when that reviewer must run an approved command that can write files.
- `best_of_n` is an implementation-only control. Record any requested valid value and resolve it to `not_applicable(review_mode)`; review mode never creates builder candidates.
- `slice_adversarial_review` and `wave_integrated_review` are full-implementation controls. Record any requested boolean values and resolve both to `not_applicable(review_mode)`. The former does not disable review mode's own required one-file adversarial pass, and review mode never creates an integrated wave reviewer.
- `pipeline_waves` is an implementation-only control. Record any requested boolean value and resolve it to `not_applicable(review_mode)`.
- Reject `review_mode: true` with `overengineering_review: true` or `style_review: true`. Review mode performs one bounded adversarial review pass per slice rather than additional reviewer layers.
- Review mode never creates a builder, fixer, remediation, escalation, integrated-review, or deployment role. It never authors or preserves tracked-source edits, stages, commits, merges, rebases, switches the user's branch, fixes a finding, or deploys anything. A verification command may create disposable changes only in its dedicated verification worktree under the rules below.
- The normal two-slot approval rule still applies to the parent orchestrator because it owns scope resolution, finding validation, deduplication, and the final review verdict. When a parent-runtime bypass is required, its intake or post-proposal acknowledgement may be combined with matrix approval as defined in `SKILL.md`.

## Optional reviewer pools

The invocation may supply `review_agents` as a list of additional reviewer-pool
options. These options augment the built-in Luna Max slice-reviewer pool; they do
not replace it or direct the orchestrator to use them. When the field is omitted,
explicitly set to YAML `null`, or set to `[]`, only the built-in pool is eligible.
Any other non-list value is malformed and must be rejected.

```yaml
review_agents:
  - max_concurrency: 5
    model: gpt-5.6-sol
    effort: medium
    id: sol-medium
```

- Always normalize the built-in Luna Max (`gpt-5.6-luna`, `max`) pool as `pool-01`, using the maximum useful concurrency the runtime safely permits. Reserve that ID for the built-in pool.
- `id` is optional for each supplied option. When present, it must be a non-empty
  string unique among the pools in this invocation and must not be `pool-01`.
  When omitted, assign the next deterministic unused ID in input order beginning
  with `pool-02`. Reserve explicit IDs before generating omitted IDs, and reject
  duplicate or reserved IDs.
- `max_concurrency` is a required positive integer and is the maximum number of simultaneously active reviewers from that pool. It is a ceiling, not a guaranteed count and not a total-run agent limit. Multiple pools are additive. Schedule additional one-file slices in transparent batches.
- `model` and `effort` are required and must form an available supported pair. Hard-stop rather than substitute a different model or effort.
- Reject non-mapping list entries, unknown pool fields, duplicate pool definitions, duplicate or invalid `id` values, non-positive or non-integer `max_concurrency`, or a partial pool missing `max_concurrency`, `model`, or `effort`. Do not infer omitted required values or silently normalize malformed input.
- Pool capacity is eligible capacity, not a quota. Assign every slice to exactly one pool. For each coordinate, retain the built-in Luna Max pool unless the orchestrator determines that a supplied option is likely to produce a better outcome for that concrete review slice. Base that determination on the slice's actual demands and the option's role fit; mere availability, novelty, spare capacity, or presence in `review_agents` is not a reason to replace Luna Max. Do not round-robin or spread work across supplied options merely to use them. Record a concise rationale for every supplied option selected. A supplied pool receiving no work is valid and requires no corrective redistribution.
- Every pool creates only the plain `slice_reviewer` role. Do not infer or select a named specialized subagent preset such as `luna_max_reviewer_subagent`, `sol_high_fixer_subagent`, or any other agent type merely from a model or effort setting. Use the default/untyped child mechanism with the exact requested model and effort when the launcher supports those fields.
- When `review_agents` is omitted, YAML `null`, or an empty list, use only `pool-01`. Preserve one-primary-file slicing and use the maximum useful concurrency the runtime safely permits.
- A custom pool is an additional runtime option that changes only model, effort, and concurrency capacity when selected. It never changes or weakens the default slice boundaries, one-primary-file rule, child packet, adversarial rubric, read-context allowance, required checks, evidence standard, snapshot-integrity checks, continuation/replacement rules, or acceptance gates. Apply those defaults exactly to every pool. Never broaden a slice because a configured pool has fewer agents or a different runtime.
- Pools supply capacity defaults; they do not prevent matrix-position selection. A user may request a model or effort for any reviewer coordinate before or after proposal. A position-specific choice supersedes the pool runtime only for the explicitly targeted coordinate or set, retains the same reviewer role and scope, and must be shown as a direct assignment in the settled matrix. If multiple coordinates share the same direct runtime, they may be scheduled together without turning the request into a broader override. Keep runtime `selection_source` (for example, `roster_default`, `translation_guide`, or `user_selected`) separate from assignment provenance: a pool-assigned coordinate records `assignment_source: pool:<id>`, while a direct position-specific assignment records `assignment_source: direct:<coordinate>`. Never overload `selection_source` with assignment provenance.
- If a position-specific request names only a model, resolve its effort through the dated runtime translation guide. Preserve an explicit effort. An unavailable model or effort leaves that coordinate `unresolved`; never silently return it to a pool default.
- Any position-specific runtime request after matrix emission invalidates that version and its approval. Finish resolving every affected coordinate, then re-emit the complete affected review matrix and obtain a later version-specific approval before creating the shared snapshot or spawning a reviewer.

Record the raw requested pool value (including omitted, YAML `null`, or `[]`), the always-present built-in pool, normalized additional pools and IDs, every reviewer coordinate and raw position-specific request, canonical default, pool or direct assignment, the rationale for each selected supplied option, resolved host/model/effort, runtime `selection_source`, `assignment_source` (such as `pool:<id>`), translation class and guide version, caps, actual maximum concurrency reached, slice assignments, and any launcher-caused unused-capacity disclosure.

## Resolve review source and scope

- Always materialize the review source as one frozen snapshot. An explicitly requested Git ref, commit, or working-tree source controls the snapshot contents; otherwise snapshot the current working tree at one capture boundary, including tracked and non-ignored untracked changes. A clean working tree still produces a snapshot whose contents equal captured `HEAD`; reviewers never use `HEAD` or the live checkout directly. Record exact inclusions and exclusions.
- Resolve the comparison base with this precedence: (1) an explicit user-supplied base, (2) the PR or merge target when the review is attached to one and that target is available, (3) captured `HEAD` when the default working-tree snapshot contains uncommitted changes, (4) the merge base between the snapshot's captured commit and the upstream/default branch when available, and otherwise (5) a concise clarification request naming the missing or ambiguous base. Do not silently choose another ref or broaden a changes-only review to the entire repository. Default review scope to files changed between the resolved comparison base and frozen snapshot. If the request explicitly names paths or asks for repository-wide review, use that scope instead. Resolve and surface the comparison base, snapshot source, included files, and exclusions before spawning reviewers.
- Extract every explicit user prohibition and non-goal as a negative constraint under the `SKILL.md` negative-scope contract. Preserve constraints such as no fallback, defensive measure, speculative hardening, compatibility behavior, extra validation, or scope expansion exactly enough that a reviewer cannot weaken them into a preference. Unless the user explicitly requested test creation or modification, also add the default `no test creation or modification` constraint.
- Never silently omit a changed file. List binary, generated, vendored, ignored, inaccessible, or otherwise non-reviewable paths in the proposal with the exact reason and give each a final `NOT_REVIEWED` status.
- Capture later user edits only in a new review run. The current run's findings always refer to the recorded snapshot, even while the user continues working in the main worktree.

## Shared immutable snapshot

After emitting and obtaining approval for the complete pre-run proposal and deployment-wave matrix, create exactly one run-scoped detached review worktree or equivalent frozen Git-backed snapshot from the resolved source. All slice reviewers and the orchestrator read that same absolute path.

- Never create a reviewer-specific worktree, branch, clone, or writable copy merely for code inspection. The write-producing verification rule below is the sole exception.
- Do not stash, reset, commit, clean, or otherwise alter the user's main worktree. A dirty main worktree is allowed because reviewers never use it as their live workspace.
- Record the snapshot path, resolved commit, captured working-tree delta if any, initial `git status`, and a content fingerprint before the first child spawn.
- Treat the snapshot as immutable. Reviewers may read any necessary file but may not modify files, create artifacts, stage, commit, switch branches, or run commands that write into the snapshot.
- Verify the snapshot status and fingerprint after every batch and before the final verdict. If a reviewer mutates it, surface the mutation, invalidate that reviewer's result and any later result that could have observed the mutation, recreate the shared snapshot from the recorded source, and rerun only the invalidated slices. Do not modify the user's main worktree.
- A build, test, formatter, generator, package installer, or analysis command that may write caches, outputs, lockfiles, generated sources, or any other path must not run in the shared snapshot. Run it only under the reviewer-specific verification-worktree rule below.

## Write-producing verification worktrees

When a reviewer must run a required or orchestrator-approved command that may create or modify any file, give that reviewer one dedicated, run-scoped, disposable verification worktree. This is a worktree per reviewer who needs write-producing verification, not a worktree per ordinary read-only reviewer and not a worktree per command.

- Plan every known write-producing check in the deployment-wave matrix. The row must name the command or gate and its planned `per-reviewer disposable worktree`. If the need is discovered later, update and re-emit the affected matrix, then obtain the mandatory version-specific approval before creating the worktree or running the command.
- Create the verification worktree from the same pinned commit and captured content state as the shared snapshot. For a frozen working-tree review, reproduce the recorded tracked delta and in-scope untracked files so its pre-command content fingerprint matches the shared snapshot.
- Do not use `git stash`, including `git stash create`, as the transport or capture mechanism. Do not stash, reset, clean, commit, or otherwise touch the user's main worktree. Reconstruct the disposable worktree from the recorded snapshot source and captured content manifest.
- Assign the worktree exclusively to that reviewer. Do not share it with another reviewer or reuse it for another slice. The reviewer may run only the approved verification commands and may not intentionally edit source, fix findings, stage, commit, merge, rebase, or switch branches.
- Record the worktree path, reviewer thread, slice, base commit, pre-command fingerprint, commands, exit statuses, decisive evidence, post-command tracked diff, and every created artifact. Treat command-produced changes only as verification evidence; never copy or merge them into the shared snapshot or user's worktree.
- After collecting the decisive receipt and evidence, remove that exact disposable worktree and its run-scoped external outputs before marking the slice complete. Verify its path, lock, process, and any run-created branch are gone without repository-wide worktree pruning.
- Cleanup is mandatory after success, failure, a blocked slice, replacement, interruption recovery, or any retry hard stop. Preserve the smallest decisive logs or fingerprints in the ledger first, then remove every disposable verification worktree. If exact cleanup cannot be verified, the run remains incomplete and the final report must surface each remaining path, process, lock, or branch.

## Plan one-file review waves

Default every review slice to exactly one primary repository file. The reviewer may read related files and interfaces, but every finding must name its primary affected file and exact evidence. Do not give one reviewer an entire feature, directory, subsystem, or repository merely because the files are conceptually related.

- Create one slice for every in-scope reviewable file. Read overlap is unrestricted because the shared snapshot is immutable.
- Use dependencies only when reviewing one primary file requires the orchestrator to first resolve context or evidence from another slice. Otherwise place all file slices in the maximal first review wave.
- Assign every slice to exactly one configured/default reviewer pool or one matrix-approved direct runtime placement. Use transparent batches when pool or platform concurrency is smaller than a logical wave.
- There is no multi-file atomicity exception in review mode because no file is writable. Cross-file implications are handled by allowing related reads and by orchestrator consolidation, not by assigning multiple primary files to one reviewer.
- The orchestrator performs cross-file synthesis itself. Do not spawn an integrated, global, post-fix, or follow-up reviewer.
- Keep a slice pending until its reviewer has inspected the primary file and necessary related context, run every planned permissible check, returned a usable receipt, passed orchestrator evidence validation, and passed shared-snapshot plus verification-worktree integrity and cleanup checks. Do not waive any gate because a non-default pool was selected.

## Mandatory pre-run proposal

Before creating the shared snapshot or spawning a reviewer, present the review proposal and a complete Markdown matrix titled `Deployment-wave matrix (review-only)`. Use the same columns as the implementation matrix, with one row per primary review file:

| Wave | Slice / gate | Depends on | Objective | Exclusive writable files | Workspace | Runtime placements | Review sequence | Gates / acceptance |
|---|---|---|---|---|---|---|---|---|

- Use exact repository-relative primary file paths in each slice objective and exact slice IDs. `Exclusive writable files` must always be `none`. `Workspace` identifies the shared snapshot and source commit or capture fingerprint, plus any planned per-reviewer disposable verification worktree and write-producing commands; use `none` for the verification-worktree portion when inspection is read-only.
- Give each reviewer a stable `<wave>/<slice>/slice-reviewer/<occurrence>` coordinate. `Runtime placements` must show canonical default, pool or direct assignment, `assignment_source`, host, resolved model/effort, `selection_source`, translation class, and guide version. A row with an `unresolved` runtime cannot execute.
- State `review_mode: true`, resolved `simple_mode: true`, resolved `worktree_mode: not_applicable(review_mode)`, resolved `best_of_n: not_applicable(review_mode)`, resolved `slice_adversarial_review: not_applicable(review_mode)`, resolved `wave_integrated_review: not_applicable(review_mode)`, resolved `pipeline_waves: not_applicable(review_mode)`, review source, comparison base, inclusions/exclusions, exact negative constraints, the built-in pool and requested additional options, resolved pool assignments with supplied-option rationales, direct runtime assignments, per-pool concurrency caps, planned batching, rubric, and acceptance rule adjacent to the matrix. Put each applicable negative constraint in its row's acceptance gate.
- Do not hide files, slices, pool assignments, dependencies, exclusions, or launcher limitations. If planning changes, re-emit the complete remaining matrix before deploying the affected reviewer wave.
- Every initial or revised review matrix is an approval checkpoint under the two-slot rule in `SKILL.md`. Identify the intake-filled and still-missing slots next to the emitted matrix. Stop before creating the shared snapshot or spawning a reviewer only when a required slot remains missing; accept flexible post-proposal acknowledgement of one or both missing slots. A qualifying current-run intake preapproval satisfies only an unchanged first matrix version. Every corrected or re-emitted matrix clears the matrix-approval slot and requires later version-specific approval, while a satisfied run-scoped orchestrator-bypass slot remains valid. Any runtime request or change invalidates the emitted matrix version; settle every affected coordinate, update and re-emit the complete affected matrix, then resolve the missing slot or slots.

## Review lifecycle

Follow these phases instead of implementation phases `P01`–`P10`:

1. `R01` Resolve controls, parent-runtime warning, flags, negative constraints, pool configuration, position-specific runtime requests, and ledger.
2. `R02` Inspect repository instructions; resolve review source, comparison base, scope, and exclusions without altering the main worktree.
3. `R03` Build one-file review slices and emit the proposal and complete deployment-wave matrix.
4. `R04` Create and fingerprint the single shared immutable snapshot.
5. `R05` Execute reviewer waves and transparent batches, creating and removing approved per-reviewer verification worktrees only where planned.
6. `R06` Validate evidence, request same-reviewer clarification when necessary, and deduplicate findings.
7. `R07` Verify complete file coverage and the unchanged snapshot; produce the consolidated verdict.
8. `R08` Remove only run-created review artifacts and report.

Keep one active phase in `state.jsonl`. Do not advance from `R03` until every reviewer coordinate is settled, the matrix has been presented after the last runtime request or change, every required approval slot is satisfied, and the emission, slot evidence and interpretation, version, and ordering are recorded. Only an unchanged first version may rely on intake preapproval; every changed or later version requires post-emission matrix approval. Do not advance from `R06` until every slice is `CLEAN`, has validated findings, or is explicitly `BLOCKED`/`NOT_REVIEWED`. Do not claim a clean result unless `R01`–`R08` complete, every in-scope reviewable file completed, every negative constraint received an evidence-backed verdict, and the snapshot fingerprint remained valid.

## Slice-reviewer contract

Give each reviewer only its primary file, necessary read context, snapshot path and fingerprint, comparison base, exact applicable negative constraints, bounded adversarial rubric, repository instructions, and concise receipt contract. When write-producing verification is planned, also give only that reviewer's dedicated verification-worktree path and exact approved commands.

The reviewer must:

1. Use the shared snapshot for inspection and remain read-only. Use a dedicated verification worktree only when one is explicitly assigned for approved write-producing checks.
2. Review exactly one primary file while reading related files when needed.
3. First search the reviewed change for concrete violations of the negative constraints, including unauthorized fallback, speculative defensive or hardening behavior, compatibility or scope-expanding machinery, or test changes that were not explicitly requested; frame each such finding as removal or reduction to the smallest allowed behavior. Then search for requirement misses, correctness defects, regressions, architecture violations, security or performance problems reachable within authorized behavior and supported inputs or environments, documentation defects, and valid nits. Existing tests may be used as evidence, but missing coverage or absent regression tests are findings only when the user explicitly requested tests. Do not treat a hypothetical unsupported state, excluded edge case, generic hardening preference, default desire for tests, or absence of explicitly prohibited behavior as a defect.
4. Run every assigned permissible check. In a verification worktree, run only the approved commands and treat every created or modified file as disposable evidence. Return `CLEAN` or evidence-backed findings with primary file, exact line or symbol, violated negative constraint or positive requirement, reproducible path or decisive logic, impact, and a concise in-scope repair direction. Do not edit or fix anything, propose new behavior outside the contract, or route a prohibited expansion through a repair recommendation.
5. Report uncertainty or missing context as a clarification request, not a terminal refusal. Remain available for the orchestrator to respond and resume the same reviewer role.
6. Return a concise receipt with status, findings, checks/evidence, limitations, and blockers. Formatting differences are not failures.

The orchestrator validates every finding against the same snapshot, exact negative constraints, explicit requirements, governing repository rules, and reproducible in-scope behavior. A reproducible defect within supported behavior remains valid even when its smallest repair would use a guard or validation; that is an ordinary bug finding, not speculative hardening. Reject speculative, generic-hardening, hypothetical-edge-case, fallback, compatibility, and scope-expanding findings with a concise evidence-based reason; a reviewer cannot override a user prohibition. Deduplicate valid findings and consolidate cross-file implications. Review mode remains report-only: neither the orchestrator nor any child fixes findings or spawns a repair role.

## Continuations, replacements, and completion

- A clarification, question, pause, blocker report, or request for missing packet facts does not consume a continuation. Resume or reuse the original reviewer after supplying the fact.
- Count one unsuccessful continuation only when the orchestrator gives the same reviewer a concrete evidence-completion request and the reviewer again fails to provide a usable `CLEAN` verdict, finding, or justified blocker for that same slice.
- Allow at most three unsuccessful continuations per slice. After the third, mark the slice `BLOCKED`, stop dependent review slices, and allow already-running independent reviewers to finish. Preserve all valid partial findings, but do not claim a complete or clean review.
- Use a replacement only when the original reviewer is technically unavailable. Before replacement, issue the mandatory user-visible notice with run, wave, slice, original role and thread ID, evidence of unavailability, replacement role/runtime, and unchanged scope. Record it. The replacement is still only the same bounded `slice_reviewer` role; no fixer, escalation, or specialized substitute is allowed.
- Receipt formatting alone never consumes a continuation or justifies replacement. Reconstruct evidence from the immutable snapshot where possible.

The final report must include snapshot source, commit/fingerprint, comparison base, captured working-tree inclusions/exclusions when applicable, requested and resolved flags including the `not_applicable(review_mode)` values for `slice_adversarial_review`, `wave_integrated_review`, and `pipeline_waves`, exact negative constraints and their review verdict, the built-in pool and requested additional options, resolved assignments and each supplied-option selection rationale, every reviewer coordinate with canonical default, raw user request when any, pool or direct assignment, `assignment_source`, resolved host/model/effort, `selection_source`, translation class and guide version, actual peak concurrency by pool, both approval-slot states and their intake or post-proposal evidence and interpretation, final matrix version, every primary file with `CLEAN`, validated findings, `BLOCKED`, or `NOT_REVIEWED`, rejected findings with concise reasons including every rejected scope-expanding recommendation, write-producing commands and evidence, replacements and their disclosures, snapshot-integrity verification, and cleanup verification for every disposable verification worktree. Never describe findings as fixed, claim deployment, or report implementation commits.

After recording the final evidence, remove every reviewer-specific verification worktree first, then the shared snapshot, run-scoped external caches/outputs, ledgers, and temporary artifacts created by this review run. Perform this cleanup on successful completion and on every blocked, failed, interrupted, replacement, or retry-hard-stop path. Never run repository-wide worktree pruning or remove or alter preexisting worktrees, branches, stashes, artifacts, or user files. Verify that no run-created worktree, branch, path, process, lock, or temporary artifact bearing the run ID remains. Completion is prohibited until this mandatory cleanup is verified or the exact cleanup failure is reported as an unresolved blocker.
