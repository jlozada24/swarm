# Review-only mode

Read this file completely whenever `review_mode: true`. This is the normative review-only execution branch. Where it conflicts with an implementation instruction in `SKILL.md`, this file controls.

## Resolved behavior

`review_mode` defaults to `false`. When `true`, it is a shorthand preset with these resolved properties:

```yaml
review_mode: true
simple_mode: true
primary_role: slice_reviewer
workspace_policy: shared_review_snapshot
source_writes_allowed: false
verification_artifact_writes: isolated_only
followup_roles_allowed: false
```

- Record requested and resolved values. If the invocation explicitly supplied `simple_mode: false`, surface that review mode resolved it to `true`; do not reject or silently conceal the resolution.
- `worktree_mode` is an implementation-only control. Record any requested value and resolve it to `not_applicable(review_mode)`. Never create per-slice implementation worktrees. The only reviewer-specific worktree permitted is the disposable verification worktree required below when that reviewer must run an approved command that can write files.
- Reject `review_mode: true` with `overengineering_review: true` or `style_review: true`. Review mode performs one bounded adversarial review pass per slice rather than additional reviewer layers.
- Review mode never creates a builder, fixer, remediation, escalation, integrated-review, or deployment role. It never authors or preserves tracked-source edits, stages, commits, merges, rebases, switches the user's branch, fixes a finding, or deploys anything. A verification command may create disposable changes only in its dedicated verification worktree under the rules below.
- The normal post-warning `obp` rule still applies to the parent orchestrator because it owns scope resolution, finding validation, deduplication, and the final review verdict.

## Optional reviewer pools

The invocation may supply `review_agents` as a list of reviewer-pool mappings:

```yaml
review_agents:
  - max_concurrency: 20
    model: gpt-5.6-luna
    effort: max
    fast: true
  - max_concurrency: 5
    model: gpt-5.6-sol
    effort: medium
    fast: false
```

- `max_concurrency` is a required positive integer and is the maximum number of simultaneously active reviewers from that pool. It is a ceiling, not a guaranteed count and not a total-run agent limit. Multiple pools are additive. Schedule additional one-file slices in transparent batches.
- `model` and `effort` are required and must form an available supported pair. Hard-stop rather than substitute a different model or effort.
- `fast` is optional and defaults to `false`. Treat it as an explicit speed-tier request, not as permission to change model, effort, scope, or review depth.
- Reject a non-list `review_agents` value, unknown pool fields, duplicate pool definitions, non-boolean `fast`, non-positive or non-integer `max_concurrency`, or a partial pool missing `max_concurrency`, `model`, or `effort`. Do not infer omitted required values or silently normalize malformed input.
- If the launch interface can enforce the requested `fast` value, pin and record it. If it cannot expose or honor that value, do not stop and do not ask for approval. Before the first spawn from that pool, surface a user-visible, non-blocking disclosure stating the pool, requested `fast` value, exact launcher limitation, and resolved behavior. Continue with the requested model and effort under the launcher's available default speed behavior. Record the disclosure and requested-versus-resolved speed behavior in `state.jsonl` and the final report. Never silently claim that `fast` was honored.
- Pool capacity is eligible capacity, not a quota. Assign every slice to exactly one pool. Fill the maximal useful concurrent set allowed by slice demand, configured caps, dependency readiness, and platform capacity. Surface in the proposal and final report any configured pool that receives no slice or any material unused capacity caused by a launcher constraint.
- Every pool creates only the plain `slice_reviewer` role. Do not infer or select a named specialized subagent preset such as `luna_max_reviewer_subagent`, `sol_high_fixer_subagent`, or any other agent type merely from a model, effort, or speed setting. Use the default/untyped child mechanism with the exact requested model and effort when the launcher supports those fields.
- When `review_agents` is omitted or an empty list, use the built-in slice-reviewer default: Luna Max (`gpt-5.6-luna`, `max`) with the launcher's default speed behavior. Preserve one-primary-file slicing and use the maximum useful concurrency the runtime safely permits.
- A custom pool changes only model, effort, requested speed behavior, and concurrency capacity. It never changes or weakens the default slice boundaries, one-primary-file rule, child packet, adversarial rubric, read-context allowance, required checks, evidence standard, snapshot-integrity checks, continuation/replacement rules, or acceptance gates. Apply those defaults exactly to every pool. Never broaden a slice because a configured pool has fewer agents or a different runtime.
- Pools supply capacity defaults; they do not prevent matrix-position selection. A user may request a model, effort, or speed for any reviewer coordinate before or after proposal. A position-specific choice supersedes the pool runtime only for the explicitly targeted coordinate or set, retains the same reviewer role and scope, and must be shown as a direct assignment in the settled matrix. If multiple coordinates share the same direct runtime, they may be scheduled together without turning the request into a broader override.
- If a position-specific request names only a model, resolve its effort and normal speed behavior through the dated runtime translation guide. Preserve explicit effort or speed values. An unavailable model or effort leaves that coordinate `unresolved`; never silently return it to a pool default.
- Any position-specific runtime request after matrix emission invalidates that version and its approval. Finish resolving every affected coordinate, then re-emit the complete affected review matrix and obtain a later version-specific approval before creating the shared snapshot or spawning a reviewer.

Record the raw requested pool list, normalized pools, every reviewer coordinate and raw position-specific request, canonical default, pool or direct assignment, resolved host/model/effort/speed, selection source, translation class and guide version, per-pool requested and resolved speed behavior, caps, actual maximum concurrency reached, slice assignments, and any unused-capacity disclosure.

## Resolve review source and scope

- Default the review source to the repository's captured `HEAD`. An explicitly requested Git ref or commit replaces that default.
- If the user explicitly requests current uncommitted work, create a frozen working-tree snapshot at one recorded capture boundary. Include tracked changes and the explicitly in-scope untracked files, record exact inclusions and exclusions, and fingerprint the captured contents. Never keep reading the live changing main worktree as the review source.
- Default review scope to files changed between the resolved comparison base and captured review source. If the request explicitly names paths or asks for repository-wide review, use that scope instead. Resolve and surface the comparison base, review source, included files, and exclusions before spawning reviewers. If a changes-only comparison base is genuinely ambiguous, ask for clarification rather than silently reviewing the entire repository.
- Never silently omit a changed file. List binary, generated, vendored, ignored, inaccessible, or otherwise non-reviewable paths in the proposal with the exact reason and give each a final `NOT_REVIEWED` status.
- Capture later user edits only in a new review run. The current run's findings always refer to the recorded snapshot, even while the user continues working in the main worktree.

## Shared immutable snapshot

After emitting and obtaining approval for the complete pre-run proposal and deployment-wave matrix, create exactly one run-scoped detached review worktree or equivalent frozen Git-backed snapshot from the resolved source. All slice reviewers and the orchestrator read that same absolute path.

- Never create a reviewer-specific worktree, branch, clone, or writable copy merely for code inspection. The write-producing verification rule below is the sole exception.
- Do not stash, reset, commit, clean, or otherwise alter the user's main worktree. A dirty main worktree is allowed because reviewers never use it as their live workspace.
- Record the snapshot path, resolved commit, intended dirty delta when a working-tree snapshot was requested, initial `git status`, and a content fingerprint before the first child spawn.
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
- After collecting the decisive receipt and evidence, remove that exact disposable worktree and its run-scoped external outputs before marking the slice complete. Verify its path, lock, process, and any run-created branch are gone, then run `git worktree prune` when safe.
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

Before creating the shared snapshot or spawning a reviewer, present the review proposal and a complete Markdown matrix titled `Deployment-wave matrix (review-only)`. Use one row per primary review file with at least these columns:

| Wave | Slice | Depends on | Objective | Primary review file | Read context | Exclusive writable files | Shared snapshot | Verification workspace | Reviewer runtime placement | Review sequence | Gates / acceptance |
|---|---|---|---|---|---|---|---|---|---|---|---|

- Use exact repository-relative file paths and slice IDs. `Exclusive writable files` must always be `none`; `Shared snapshot` must identify the one planned snapshot and source commit or capture fingerprint. `Verification workspace` must be `none` for inspection-only slices or identify the planned per-reviewer disposable worktree and write-producing commands.
- Give each reviewer a stable `<wave>/<slice>/slice-reviewer/<occurrence>` coordinate. `Reviewer runtime placement` must show canonical default, pool or direct assignment, host, resolved model/effort/speed, selection source, translation class, and guide version. A row with an `unresolved` runtime cannot execute.
- State `review_mode: true`, resolved `simple_mode: true`, resolved `worktree_mode: not_applicable(review_mode)`, review source, comparison base, inclusions/exclusions, requested and resolved pools, direct runtime assignments, per-pool concurrency caps, speed-tier support or disclosure, planned batching, rubric, and acceptance rule adjacent to the matrix.
- Do not hide files, slices, pool assignments, dependencies, exclusions, or launcher limitations. If planning changes, re-emit the complete remaining matrix before deploying the affected reviewer wave.
- Every initial or revised review matrix is a hard approval checkpoint under the rule in `SKILL.md`. Immediately after presenting it, stop before creating the shared snapshot or spawning a reviewer unless a qualifying user-authored current-run pre-approval satisfies an unchanged first matrix version. Identify and record that pre-approval next to the emitted first matrix. Every corrected or re-emitted matrix requires a later version-specific approval. Any runtime request or change invalidates the emitted version and all prior approval evidence; settle every affected coordinate, update and re-emit the complete affected matrix, then hard-pause for approval sent after that settled matrix. Matrix approval is separate from `obp`.

## Review lifecycle

Follow these phases instead of implementation phases `P01`–`P10`:

1. `R01` Resolve controls, parent-runtime warning, flags, pool configuration, position-specific runtime requests, and ledger.
2. `R02` Inspect repository instructions; resolve review source, comparison base, scope, and exclusions without altering the main worktree.
3. `R03` Build one-file review slices and emit the proposal and complete deployment-wave matrix.
4. `R04` Create and fingerprint the single shared immutable snapshot.
5. `R05` Execute reviewer waves and transparent batches, creating and removing approved per-reviewer verification worktrees only where planned.
6. `R06` Validate evidence, request same-reviewer clarification when necessary, and deduplicate findings.
7. `R07` Verify complete file coverage and the unchanged snapshot; produce the consolidated verdict.
8. `R08` Remove only run-created review artifacts and report.

Keep one active phase in `state.jsonl`. Do not advance from `R03` until every reviewer coordinate is settled, the matrix has been presented after the last runtime request or change, a qualifying user-authored chat approval has explicitly authorized that exact version, and the emission, approval or pre-approval, version, and ordering are recorded. Only an unchanged first version may rely on qualifying pre-approval. Do not advance from `R06` until every slice is `CLEAN`, has validated findings, or is explicitly `BLOCKED`/`NOT_REVIEWED`. Do not claim a clean result unless `R01`–`R08` complete, every in-scope reviewable file completed, and the snapshot fingerprint remained valid.

## Slice-reviewer contract

Give each reviewer only its primary file, necessary read context, snapshot path and fingerprint, comparison base, bounded adversarial rubric, repository instructions, and concise receipt contract. When write-producing verification is planned, also give only that reviewer's dedicated verification-worktree path and exact approved commands.

The reviewer must:

1. Use the shared snapshot for inspection and remain read-only. Use a dedicated verification worktree only when one is explicitly assigned for approved write-producing checks.
2. Review exactly one primary file while reading related files when needed.
3. Search for requirement misses, correctness defects, edge cases, regressions, architecture violations, security or performance problems, concrete changed behavior left unproven by tests, documentation defects, and valid nits.
4. Run every assigned permissible check. In a verification worktree, run only the approved commands and treat every created or modified file as disposable evidence. Return `CLEAN` or evidence-backed findings with primary file, exact line or symbol, reproducible path or decisive logic, impact, and a concise repair direction. Do not edit or fix anything.
5. Report uncertainty or missing context as a clarification request, not a terminal refusal. Remain available for the orchestrator to respond and resume the same reviewer role.
6. Return a concise receipt with status, findings, checks/evidence, limitations, and blockers. Formatting differences are not failures.

The orchestrator validates every finding against the same snapshot, rejects unsupported findings with a concise evidence-based reason, deduplicates repeated findings, and consolidates cross-file implications. It does not fix findings and does not spawn another role to do so.

## Continuations, replacements, and completion

- A clarification, question, pause, blocker report, or request for missing packet facts does not consume a continuation. Resume or reuse the original reviewer after supplying the fact.
- Count one unsuccessful continuation only when the orchestrator gives the same reviewer a concrete evidence-completion request and the reviewer again fails to provide a usable `CLEAN` verdict, finding, or justified blocker for that same slice.
- Allow at most three unsuccessful continuations per slice. After the third, mark the slice `BLOCKED`, stop dependent review slices, and allow already-running independent reviewers to finish. Preserve all valid partial findings, but do not claim a complete or clean review.
- Use a replacement only when the original reviewer is technically unavailable. Before replacement, issue the mandatory user-visible notice with run, wave, slice, original role and thread ID, evidence of unavailability, replacement role/runtime, and unchanged scope. Record it. The replacement is still only the same bounded `slice_reviewer` role; no fixer, escalation, or specialized substitute is allowed.
- Receipt formatting alone never consumes a continuation or justifies replacement. Reconstruct evidence from the immutable snapshot where possible.

The final report must include snapshot source, commit/fingerprint, comparison base, captured working-tree inclusions/exclusions when applicable, requested and resolved flags, requested and resolved pools, every reviewer coordinate with canonical default, raw user request when any, pool or direct assignment, resolved host/model/effort/speed, selection source, translation class and guide version, every speed-tier disclosure, actual peak concurrency by pool, final matrix version and its qualifying approval or pre-approval evidence, every primary file with `CLEAN`, validated findings, `BLOCKED`, or `NOT_REVIEWED`, rejected findings with concise reasons, write-producing commands and evidence, replacements and their disclosures, snapshot-integrity verification, and cleanup verification for every disposable verification worktree. Never describe findings as fixed, claim deployment, or report implementation commits.

After recording the final evidence, remove every reviewer-specific verification worktree first, then the shared snapshot, run-scoped external caches/outputs, ledgers, and temporary artifacts created by this review run. Perform this cleanup on successful completion and on every blocked, failed, interrupted, replacement, or retry-hard-stop path. Never remove or alter preexisting worktrees, branches, stashes, artifacts, or user files. Run `git worktree prune` after run-created worktree removal, and verify that no run-created worktree, branch, path, process, lock, or temporary artifact bearing the run ID remains. Completion is prohibited until this mandatory cleanup is verified or the exact cleanup failure is reported as an unresolved blocker.
