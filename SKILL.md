---
name: luna-swarm
description: Orchestrate explicitly invoked, large repository implementation or review swarms. Implementation runs use collision-free waves, selectable isolated-worktree or verified zero-overlap same-worktree execution, optional single-role simple mode, gated review and repair, matrix-settled per-position runtimes, and a mandatory post-warning `obp` acknowledgement for parent-runtime bypass. Review-only runs use one-file reviewer slices over one immutable shared snapshot with optional reviewer pools and no implementation changes. Do not use for small edits or ordinary analysis unless the user explicitly invokes this skill.
---

# Luna Swarm

Execute a repository task autonomously by decomposing it into the smallest coherent, independently verifiable slices. Implementation runs use isolated worktrees by default, or the orchestrator worktree only after a requested same-worktree run passes its zero-file-overlap preflight. Full implementation mode uses gated build, review, and repair roles. Simple implementation mode keeps only the slice-builder role. `review_mode: true` is a stricter review-only preset of simple mode: it keeps only the slice-reviewer role, uses one shared immutable snapshot, permits no authored source changes, and confines write-producing checks to disposable verification worktrees.

## Non-negotiable operating model

- The invoking parent thread is the orchestrator. Sol at `high` effort or higher remains the recommended parent runtime, but this is a bypassable quality warning rather than an absolute requirement. If the parent does not meet it, state the actual parent model/effort, warn that orchestration, finding adjudication, merge control, and release gating may be weaker, then hard-pause before creating worktrees, spawning children, or changing repository state. Define `obp` as “orchestrator bypass proceed.” The only valid acknowledgement is the next post-warning user message whose entire contents, after trimming surrounding whitespace, equal lowercase `obp`. An `obp` present in the invoking prompt, an earlier message or run, a quoted example, generic approval, skill invocation, or any longer response does not count. If the next response is not exactly `obp`, remain paused; before offering another opportunity, reissue the warning and again require the immediately following response to be exactly `obp`. A valid `obp` is one-time authorization for the current run only. Record the warning, the exact acknowledgement, and their message order. Do not spawn a replacement orchestrator. Child runtime selections never change an already-running parent model or effort.
- The orchestrator owns the full task, dependency graph, file ownership, finding validation, merges, gates, evidence, retry accounting, and cleanup.
- After any required post-warning `obp` acknowledgement and the mandatory version-scoped deployment-wave-matrix approval have both been resolved, run autonomously without further routine wave, merge, review, or remediation approval checkpoints. Stop for a missing valid `obp`, missing approval of the current matrix version, an invalid entry-flag combination, a failed same-worktree overlap preflight, a real permission/safety barrier, an unrecoverable repository or review-snapshot state, unavailable resolved model/effort, or the applicable retry hard stop: three unsuccessful same-role continuations in simple or review mode, or five unsuccessful retries in full implementation mode.
- Optimize for zero collision risk, not minimum agent count. A logical wave may contain 60–100 or more agents when the slices are genuinely independent.
- Resolve `review_mode`, `worktree_mode`, and `simple_mode` before spawning any child or changing repository state. Apply only the explicit preset resolutions documented below; never silently repair or downgrade any other invalid combination.
- Before creating an implementation worktree or shared review snapshot, spawning a child, or editing tracked source, present the user with a proposal that includes the mandatory deployment-wave matrix defined below. This is required for every run and every mode, including a one-wave simple-mode or review-only run.
- Never replace an agent thread silently. Before spawning any replacement because the original thread is technically unavailable, surface a user-visible notice stating the run, wave, slice, original role and thread identifier, exact evidence of unavailability, replacement role and runtime, and unchanged bounded scope. Record the notice and replacement relationship in `state.jsonl`. This disclosure is informational rather than an approval checkpoint unless the replacement changes authority, scope, permissions, workspace policy, or another user-controlled choice.
- In full implementation mode, never pipeline logical waves. A wave must be completely built, integrated, remediated, and accepted by a fresh integrated reviewer using that matrix position's approved runtime before any next-wave implementation begins. Simple mode keeps one primary child role: slice builder in implementation mode or slice reviewer in review mode. Clarifying, resuming, or directing the same primary-role agent to complete its bounded work is permitted continuation, not a prohibited follow-up role.
- In `isolated_worktrees` mode, “land” means the orchestrator merges the accepted slice branch into the branch currently checked out in the orchestrator worktree. Only the orchestrator merges. In `same_worktree` mode, builders never stage or commit; the orchestrator alone stages each exclusive allowlist and creates the slice commits after builder completion and verification.

## Entry flags

Resolve these flags independently from the post-warning `obp` acknowledgement and matrix runtime settlement:

- `review_mode: true | false`; default to `false`.
  - `false`: use the implementation workflow in this file.
  - `true`: before planning or execution, read and follow [references/review-mode.md](references/review-mode.md) completely. That reference defines the review-only lifecycle and replaces every implementation-only builder, writable-file, worktree, dirty-worktree, gate-repair, merge, commit, deployment, final-review, and cleanup instruction in this file where they conflict.
  - `review_mode: true` deterministically resolves `simple_mode` to `true`, even when `simple_mode` was omitted or explicitly requested as `false`. This is the preset's defined behavior, not a silent repair. Surface and record both the requested and resolved values.
  - In review mode, implementation `worktree_mode` is not executed. Surface and record any requested value, resolve it to `not_applicable(review_mode)`, and use the reference's single `shared_review_snapshot` workspace policy.
- `worktree_mode: isolated_worktrees | same_worktree`; default to `isolated_worktrees`.
  - This flag controls implementation runs only.
  - `isolated_worktrees`: use the normal per-slice branch and worktree workflow.
  - `same_worktree`: complete the full implementation plan and exclusive write map before any child spawn or edit. Permit execution only when every slice's writable file set is pairwise disjoint across the complete plan. If any writable file appears in more than one slice, hard-stop with the conflicting slice IDs and paths. Do not fall back to isolated worktrees, serialize the overlap, or alter ownership to make the bypass pass.
  - In `same_worktree`, all builders edit the orchestrator worktree. Builders must not stage, commit, merge, rebase, switch branches, or manipulate the Git index. The orchestrator waits for the active builders, verifies ownership and gates, then stages and commits only the exact allowlist for each accepted slice. Account for shared non-file resources separately and isolate or serialize their use without weakening the zero-file-overlap precondition.
- `simple_mode: true | false`; default to `false`.
  - `false`: run the full builder, review, fixer, remediation, escalation, and integrated-review workflow.
  - `true` with `review_mode: false`: use only the slice-builder role. Spawn no adversarial, overengineering, style, post-fix, remediation, integrated-wave, final-task, fixer, or escalation roles. This restricts agent roles, not communication or continuation with a builder. The orchestrator may answer questions, clarify planned paths and dependencies, correct factual packet errors, wait for a planned dependency, send follow-up instructions, resume or reuse the same builder thread, and direct that builder to repair its own slice within the authorized write allowlist and rerun checks. Prefer the original builder; if it is technically unavailable, a replacement may be spawned only in the same slice-builder role with the same bounded scope and only after the mandatory user-visible replacement disclosure. Do not terminate unrelated builders merely because one builder pauses, refuses, or reports a resolvable blocker. The orchestrator still verifies the live diff, exclusive ownership, required checks, commits or merges accepted work as appropriate, and enforces wave barriers.
  - `true` with `review_mode: true`: use only the slice-reviewer role and the review-mode reference. The reviewer may be clarified, resumed, or reused, but neither it nor any other child may fix code.
  - Reject `simple_mode: true` combined with `overengineering_review: true` or `style_review: true`. Do not silently ignore incompatible review toggles.

Record the requested and resolved values of all three flags in `state.jsonl` and the final report.

## Mandatory pre-run proposal

After repository inspection, baseline checks, runtime settlement, and complete dependency/ownership or review-scope planning, present a user-facing proposal before creating implementation worktrees or the shared review snapshot, spawning children, or editing tracked source. The proposal must always include a Markdown deployment-wave matrix, even when the plan has only one wave or one slice. In review mode, use the mode-specific matrix in [references/review-mode.md](references/review-mode.md).

Use one matrix row per planned slice and include at least these columns:

| Wave | Slice / gate | Depends on | Objective | Exclusive writable files | Workspace | Runtime placements | Review sequence | Gates / acceptance |
|---|---|---|---|---|---|---|---|---|

- List every planned deployment wave in dependency order and group rows by wave ID.
- Include one row for every implementation slice and an explicit gate row for every wave-level integrated reviewer and final integrated reviewer. Do not bury a run-level reviewer in an unrelated slice row. Conditional slice-local fixer, post-fix, remediation, and escalation coordinates may remain enumerated in their owning row's runtime cell.
- Use exact slice IDs, exact repository-relative writable paths, and explicit dependency IDs. Write `none` when a cell has no value; never omit a required column.
- State the resolved `review_mode`, `worktree_mode`, `simple_mode`, runtime placements, review toggles, and any shared mutable-resource or snapshot isolation immediately before or after the matrix.
- Give every planned or conditional child spawn a stable coordinate using `<wave>/<slice-or-gate>/<role>/<occurrence>`, such as `W01/S03/builder/1`, `W01/S03/adversarial-reviewer/1`, `W01/S03/review-fixer/1`, `W01/integrated-reviewer/1`, or `FINAL/integrated-reviewer/1`. The runtime cell must enumerate every builder, enabled review-layer occurrence, conditional fixer/post-fix occurrence, remediation role, retry escalation role, integrated-wave reviewer, and final reviewer that the row can deploy.
- For each coordinate, show the canonical roster default, host, resolved model, effort, requested and resolved speed behavior, selection source (`roster_default`, `translation_guide`, or `user_selected`), translation class (`exact`, `vetted_role_equivalent`, `user_selected_nondefault`, or `unresolved`), and translation-guide version. A matrix containing an `unresolved` runtime is informative only and cannot be approved for execution.
- A user may request a model for any assignable coordinate, explicit set of coordinates, role, slice, wave, or all remaining occurrences before or after a matrix is proposed. A model-only request uses the approved translation guide to resolve effort and speed; an explicit model, effort, or speed value must be preserved. Ask for clarification only when the target or requested setting is genuinely ambiguous. Never silently broaden a request to positions the user did not identify.
- Any user runtime request or change after matrix emission invalidates that matrix version and every approval or pre-approval associated with it. Keep execution paused while runtime choices are discussed. After every affected position is concrete and the user has no unresolved runtime request, re-emit the complete affected matrix and require a new post-emission approval. Runtime discussion, a change request containing approval language, and approval sent before or alongside the settled matrix never authorize execution.
- A runtime change during execution applies only to unstarted positions. For an active or completed position, surface that it cannot change retroactively and require explicit replan authority before restarting or repeating work. Re-emit and reapprove the complete remaining-wave matrix before any affected unstarted position proceeds.
- In `same_worktree`, use the matrix's writable-file column as the user-visible overlap proof. State explicitly that the complete matrix has zero repeated writable paths. If any path repeats, hard-stop instead of presenting the plan as executable.
- Treat every emitted matrix version as a hard approval checkpoint. Immediately after presenting an initial, corrected, or remaining-wave matrix, hard-pause before creating a worktree or shared review snapshot, spawning a child, editing, staging, committing, merging, or otherwise executing that matrix. Resume only after a user-authored chat authorization valid for that version. Case-insensitive, surrounding-whitespace-trimmed responses such as `approved`, `approve`, `y`, `yes`, `go`, `go ahead`, `proceed`, or `run it` are valid, as is other post-matrix language that explicitly and unambiguously authorizes the current matrix without requesting a change. A current-run pre-approval may satisfy only the first matrix version, and only when a user-authored message in this chat either consists entirely of one listed approval word or phrase after trimming, or explicitly designates one listed word or phrase as authorization for the forthcoming matrix. When such a valid pre-approval exists, identify it next to the first emitted matrix and record that its gate is already satisfied; no additional pause is required for that first version. Never infer pre-approval from tool permissions, approval policy, a system or developer message, skill invocation alone, broad autonomy language, silence, quoted examples, or conversational mention of an approval word. Pre-approval never carries to a corrected or re-emitted matrix. If the user requests any change, revise and re-emit the complete affected matrix, then hard-pause for a new post-matrix approval. This matrix approval is separate from `obp` and cannot satisfy it.
- If planning changes before the first spawn, emit the corrected complete matrix and obtain its approval before execution. If a boundary violation or integration finding changes future waves during execution, update and re-emit the complete remaining-wave matrix and obtain its approval before deploying the affected wave.

Record proposal emission, the current matrix version, the qualifying user-authored approval or pre-approval message, whether it preceded or followed emission, its ordering, and the exact approved version in `state.jsonl`. Do not claim that implementation or review execution started before this evidence exists.

## Runtime positions and default roster

In full implementation mode, use a new agent thread for every role and every retry. Never reuse a builder as a reviewer or fixer, never resume an earlier role thread, and never pass one agent's hidden reasoning to another. In simple implementation mode, use only the slice-builder row. In review mode, use only the configured or default slice-reviewer pools in the review-mode reference. Same-role clarification and continuation are allowed in either simple branch; do not create a different follow-up role.

Before resolving child runtimes or emitting a matrix, read and follow [references/runtime-translation.md](references/runtime-translation.md) completely. Its dated mappings are operational role equivalents, not claims that different models are identical.

| Role | Canonical default model and effort | Workspace |
|---|---|---|
| Slice builder | Luna Max (`gpt-5.6-luna`, `max`) | Its resolved slice workspace |
| Slice adversarial reviewer | Fresh Luna Max | Slice workspace, review-only |
| Slice overengineering reviewer, when enabled | Fresh Luna Max | Slice workspace, review-only |
| Slice style reviewer, when enabled | Fresh Luna Max for every occurrence | Slice workspace, review-only |
| Slice review-layer fixer | Fresh Luna Max | Slice workspace |
| Post-fix layer reviewer | Fresh Luna Max | Slice workspace, review-only |
| Non-escalated remediation fixer/reviewer | Fresh Luna Max | Its resolved remediation workspace |
| Integrated wave reviewer | Fresh Sol XHigh (`gpt-5.6-sol`, `xhigh`) | Orchestrator branch, review-only |
| Final integrated-task reviewer | Fresh Sol XHigh (`gpt-5.6-sol`, `xhigh`) | Orchestrator branch, review-only |
| Escalated builder after retry 3 | Fresh Sol High (`gpt-5.6-sol`, `high`) | The affected workspace |
| Escalated reviewer | Fresh Sol XHigh (`gpt-5.6-sol`, `xhigh`) | The affected workspace, review-only |
| Escalated fixer | Fresh Sol XHigh (`gpt-5.6-sol`, `xhigh`) | The affected workspace |

- Defaults apply per runtime coordinate, not through a global power tier. There is no global or categorized child-runtime override.
- A user's explicit coordinate-specific or scope-specific runtime choice takes precedence over the roster and translation guide only for the positions the user identified. Record the raw request and every affected coordinate.
- If the user supplies only a model, use the translation guide's role-specific effort and normal speed behavior for that model and host. If the user supplies effort or speed too, preserve each supplied value exactly.
- If a requested or guide-resolved model/effort pair is unavailable, surface exact evidence and keep the position `unresolved`; do not substitute. The user may choose another runtime, after which the settled matrix must be re-emitted and newly approved.
- If an explicit spawn interface exposes model and effort, pin both to the matrix-approved values. If the launcher cannot honor the approved model or effort, do not start that position. If it cannot honor speed, use the existing nonblocking speed disclosure rule rather than claiming support.
- Full-mode fresh-role requirements prohibit reused contexts. Simple-mode builder continuation should resume or reuse the builder's existing context when possible and retain the runtime approved for that same builder coordinate.
- Retry counting, role changes, and the escalation boundary remain mandatory. Each ordinary retry and escalation role uses its own matrix-approved coordinate rather than inheriting a power category.

## Protect child context

The orchestrator retains global context. Child agents receive only the smallest full-fidelity packet needed for one role on one slice.

- Target each initial child packet at no more than 1,200 tokens; 2,000 tokens is a hard ceiling. If a complete packet needs more, split the slice further instead of sending a larger prompt.
- Do not paste the global task, the full plan, the full ledger, unrelated requirements, source files, large diffs, raw logs, prior transcripts, or another agent's reasoning.
- Point to live repository paths, symbols, commits, commands, and compact receipt files instead of copying their contents.
- Give one agent exactly one role and one bounded objective.
- A builder receives only its objective, exclusive write allowlist, the orchestrator-validated atomicity proof when a multi-file exception applies, necessary interface/dependency facts, acceptance criteria, repo instructions/gates, base commit, and receipt format.
- A reviewer receives the same compact slice contract, the rubric for exactly one active review layer, and the live commit/diff to inspect. It does not receive the builder transcript or another layer's reviewer transcript.
- A fixer receives only orchestrator-validated findings from one active review layer with their evidence and the slice contract. It does not receive the raw reviewer transcript, rejected findings, or another layer's findings.
- A post-fix reviewer receives the live fixed state, slice contract, and the same active-layer rubric, not the fixer transcript.
- Agent responses must be concise factual receipts. Exact headings, field order, and prose format are not acceptance requirements. Keep full command output on disk only while needed; return command, exit status, and the smallest decisive excerpt or path.
- If a child agent must understand broad architecture to perform the slice, the slice is not yet small or well bounded enough. Replan it.

Every child packet must include this compact contract, expressed without duplicating already supplied fields:

1. Read and obey applicable `AGENTS.md` and repository-local instructions.
2. Work only in the supplied workspace and base state.
3. Modify only the exclusive write allowlist. Reading other files is allowed when necessary.
4. Preserve unrelated work. Do not merge, rebase, switch branches, broaden scope, or edit shared files not assigned to this slice.
5. Run the specified checks. Do not call a failure “preexisting” and waive it.
6. In `isolated_worktrees`, commit implementation/fix work before reporting. In `same_worktree`, never stage or commit; the orchestrator owns the Git index and commits. Reviewers make no code changes.
7. If another file must change, pause and report the exact boundary violation to the orchestrator; do not expand ownership yourself. Remain available for the orchestrator to clarify the existing plan or resume the work after it safely revises ownership and dependencies.
8. Return a concise receipt containing status, commit when applicable, files changed or findings, checks/evidence, and blockers. Labels and ordering may vary.
9. In simple mode, treat an uncertain path, a not-yet-visible but planned destination, a dependency timing issue, or another resolvable packet ambiguity as a request for orchestrator clarification, not as a terminal refusal. Continue in the same builder role when the orchestrator responds.

## Initialize the run

1. Confirm this is a Git repository and record:
   - original branch and `HEAD`;
   - repository root and Git common directory;
   - applicable `AGENTS.md` files and repository-defined build, test, lint, formatting, review, and commit rules.
2. Inspect the parent orchestrator's actual model/effort. If it is not Sol at `high` or higher, emit the required warning and hard-pause before creating worktrees, spawning children, or changing repository state. Accept no preauthorization. Resume only after the immediately following user message consists solely of lowercase `obp` after trimming surrounding whitespace. If that response does not match, remain paused and require a newly issued warning followed immediately by an exact `obp`. Record the actual runtime, warning message, exact acknowledgement, message ordering, and one-time current-run scope.
3. Resolve `review_mode`, defaulting to `false`. If it resolves to `true`, read [references/review-mode.md](references/review-mode.md) completely and follow its `R01`–`R08` lifecycle instead of steps 4–13 and the implementation `P01`–`P10` lifecycle below. If it resolves to `false`, resolve `worktree_mode`, defaulting to `isolated_worktrees`, and `simple_mode`, defaulting to `false`; reject unknown values.
4. Read the runtime translation guide and resolve every planned or conditional child coordinate from its canonical default, the detected host, and any user runtime requests. Keep unavailable, unsupported, or ambiguous positions `unresolved` instead of silently repairing them. Do not emit an executable matrix until every position is concrete.
5. Resolve the two optional per-slice review toggles from the invocation. Both default to off unless the invocation explicitly enables them:
   - `overengineering_review`: add an overengineering layer after the required adversarial layer;
   - `style_review`: add a style layer immediately after every other layer that runs, so it runs once after adversarial review and, when overengineering review is also enabled, again after overengineering review.
   Reject either enabled toggle when `simple_mode` is `true`.
6. Record the exact per-slice layer sequence for the run:
   - simple mode: builder only; no review layers;
   - neither optional toggle: adversarial;
   - style only: adversarial → style;
   - overengineering only: adversarial → overengineering;
   - both toggles: adversarial → style → overengineering → style.
7. Do not start from a dirty orchestrator worktree. Never stash, reset, or overwrite unrelated user changes. Resolve task-owned changes into a safe baseline commit when clearly authorized by the task; otherwise hard-stop with exact evidence.
8. Discover and run the repository's required baseline gates when feasible. A failing baseline is a blocking defect, not an acceptable “preexisting failure.” Put its repair in a blocking wave or stop if it cannot be safely repaired within task authority.
9. Build the complete dependency DAG and ownership map before execution. When `worktree_mode` is `same_worktree`, prove that writable file sets are pairwise disjoint across the complete plan. Hard-stop before spawning children or editing if the proof fails.
10. Present the mandatory pre-run proposal and complete deployment-wave matrix. Verify that every planned slice, dependency, exclusive writable path, workspace, runtime coordinate and resolved assignment, review sequence, and gate appears in it. For each multi-file exception, also show the attempted dependency-ordered one-file plan and concrete atomicity proof. Unless a qualifying user-authored current-run pre-approval already satisfies an unchanged first version, hard-pause and obtain a later explicit approval of that exact matrix version. Any runtime discussion or change requires the settled matrix to be emitted afterward and approved by a later message. Record proposal emission, matrix version, runtime-settlement evidence, approval or pre-approval message, and ordering before implementation begins.
11. Create one run-scoped temporary directory under the Git common directory, for example `<git-common-dir>/luna-swarm/<run-id>/`.
12. Maintain only two compact orchestrator artifacts during execution:
   - `state.jsonl`: canonical phase ID/status, parent runtime, warning and exact post-warning `obp` acknowledgement evidence when required, message ordering and one-time run scope, review mode, worktree mode, simple mode, proposal-emission evidence, deployment-wave matrix version, qualifying approval or pre-approval message and approved-version ordering, wave, slice, dependencies, exclusive owned files, attempted one-file landing order and concrete atomicity proof for every multi-file exception, branch/workspace, every runtime coordinate, canonical default, raw user request, resolved host/model/effort/speed, selection source, translation class and guide version, enabled review toggles, current review layer, status, retry count, replacement relationship and user-visible disclosure evidence when applicable, and accepted commit;
   - `receipts.jsonl`: concise agent result, command/evidence references, and orchestrator validation verdict.
13. Do not place orchestration artifacts in tracked source paths or include them in child prompts wholesale.

## Implementation-mode canonical orchestrator todo

When `review_mode` is `false`, follow these phases in order. Review mode uses the `R01`–`R08` lifecycle in its reference instead.

1. `P01` Initialize controls and ledger.
2. `P02` Inspect repository and baseline.
3. `P03` Plan dependencies and ownership, then emit the proposal and deployment-wave matrix.
4. `P04` Prepare the next wave.
5. `P05` Build slices.
6. `P06` Review and accept slices.
7. `P07` Merge and gate the wave.
8. `P08` Review and remediate integration.
9. `P09` Run final gates and review.
10. `P10` Clean up and report.

Anti-drift rules:

- Keep one active phase in `state.jsonl`.
- Advance only from orchestrator-verified evidence.
- Do not advance from `P03` to `P04` until every runtime coordinate is settled, the complete deployment-wave matrix has been presented after the last runtime request or change, a qualifying user-authored chat approval has explicitly authorized that exact version, and all events and their ordering are recorded. Only an unchanged first version may rely on qualifying pre-approval; every changed or later version requires post-emission approval.
- After `P08`, loop to `P04` when another wave remains.
- After interruption, resume from the ledger and recheck live Git state.
- Claim completion only when `P01` through `P10` are complete and nothing remains active or blocked.

## Decompose into collision-free waves

Build a dependency DAG before implementation.

- Define each logical wave as the maximal set of currently dependency-ready slices whose exclusive write sets and mutable resources are pairwise disjoint.
- Use a blocking slice or wave mainly to serialize shared-file or mutable-resource collisions or to land a changed contract required by downstream slices. After it is accepted, recompute readiness and form the next maximal collision-free wave.
- Default every slice to exactly one writable file, including ordinary application code, tests, configuration, migrations, manifests, and generated artifacts. Reading other files is unrestricted when necessary.
- Before allowing a multi-file slice, construct and evaluate at least one dependency-ordered plan of one-file slices. Try compatibility-preserving intermediate steps where the repository permits them, such as introducing a new API or destination, migrating consumers, and only then removing the old API or source.
- “Atomic” means no ordering of separate one-file commits can keep every intermediate accepted repository state valid, testable under its required gates, and safely landable. Files are not atomic merely because they implement one feature, migration, refactor, final invariant, conceptual operation, or mutually refer to one another. Dependency coupling calls for ordered slices and blocking waves, not automatic bundling.
- Use a multi-file slice only after the orchestrator proves the one-file alternative fails. Record the attempted order, the exact intermediate compile, contract, generation, or required-gate failure, and why no compatibility bridge or different ordering resolves it. A conclusion such as “these files must stay consistent” is not proof.
- Split independently writable files into separate dependent slices whenever practical. Never bundle files for convenience, fewer agents, feature-level grouping, or to let one builder own an entire semantically coherent change.
- Assign an exclusive write set to every slice. Two concurrently active slices must never modify the same file, generated output, manifest, registry, migration, project file, shared test file, or other mutable resource.
- Assign every shared manifest, registry, migration, project file, generated output, or other shared file to one dedicated owner slice. Serialize it in a low-count or single-agent wave when it blocks other work.
- Prefer a separate test slice when the test file can be changed and verified independently. Keep source and test files together only under the same recorded multi-file atomicity exception. A shared test file belongs to one slice only.
- Account for non-source collisions: build output directories, DerivedData, caches, ports, databases, simulators, generated files, and external mutable state. Give each worktree isolated paths/resources or serialize the affected slices.
- In `isolated_worktrees`, all slices in one logical wave branch from the same accepted wave-base commit. In `same_worktree`, all slices use the same recorded wave-base commit as their comparison base while editing the orchestrator worktree.
- Maximize available concurrency. If the runtime cannot open the full logical wave at once, schedule transparent batches within the same wave. Keep the same wave base and do not begin the next logical wave until every batch has completed and the entire wave has passed integrated review in full mode or orchestrator verification and gates in simple mode.
- Record the full DAG and ownership map only in orchestrator state. Each child sees only its slice.
- When `worktree_mode` is `same_worktree`, validate the complete ownership map before implementation: every slice write set must be pairwise disjoint across all waves, not merely within one wave. Any duplicate writable path is a hard stop. Record the proof or the exact conflicts in `state.jsonl`.
- Make the user-facing deployment-wave matrix a faithful projection of the complete DAG and ownership map. Do not hide a planned slice, file, dependency, workspace, review layer, or gate from the matrix.
- For every proposed multi-file slice, show the attempted one-file landing order and atomicity proof immediately adjacent to its deployment-wave matrix row. If that proof is absent or only states semantic relatedness or final consistency, reject the multi-file slice and replan it as dependency-ordered one-file slices before spawning builders.

## Conservative test scope

Minimize newly authored test code, not required test execution.

- Run every repository-required targeted, integration, and full gate.
- Add a test only for an explicit acceptance requirement, changed behavior not already proven, or a validated defect needing regression coverage.
- Use the smallest focused case and fewest assertions that decisively prove that behavior. Avoid speculative permutations and broad snapshots.
- Reuse existing test infrastructure. Do not introduce helpers, fixtures, mocks, or harnesses unless the required case cannot stay clear and local without them.
- Prefer a separate one-file test slice when practical, following the normal ownership rules.
- Never delete or weaken existing tests, lower thresholds, skip mandatory checks, or game coverage metrics to stay minimal.
- A reviewer may request a test only by naming the concrete changed behavior or validated defect that existing tests and gates do not prove. A preference for more coverage is not a finding.

## Execute each build slice

For every slice in the wave:

1. In `isolated_worktrees`, the orchestrator creates a uniquely named branch and worktree from the wave-base commit. In `same_worktree`, use the clean orchestrator worktree and create no slice branch or worktree.
2. Spawn a fresh builder using the runtime approved for that slice's builder coordinate with the compact slice packet.
3. Verify the builder's actual diff, owned-file compliance, and required targeted gates. In `isolated_worktrees`, also verify its commit. In `same_worktree`, verify that it did not stage, commit, switch branches, or modify the Git index. Do not trust self-report alone.
4. When `simple_mode` is `true`, spawn no separate follow-up role. If the builder diff and gates are acceptable, mark the slice builder-accepted. Otherwise inspect the live state, resolve factual ambiguity, and send the same builder a targeted clarification, correction, or repair request within its write allowlist. Resume or reuse that builder and re-verify its work under the simple-mode retry rule below. A builder question, pause, refusal based on a resolvable packet fact, incomplete first result, or initial gate failure is not by itself a hard stop. Continue to step 13 only after the slice is accepted or an actual hard-stop condition is reached. When `simple_mode` is `false`, use the invocation's recorded review-layer sequence. The required adversarial layer always runs; optional layers run only where the sequence places them. Every occurrence, including both style occurrences when both toggles are enabled, is a separate layer with fresh agents and no reused context.
5. Apply the active layer's bounded rubric:
   - adversarial: actively search for requirement misses, correctness defects, edge cases, regressions, architecture violations, security/performance issues, concrete changed behavior or validated defects left unproven by tests, documentation defects, and valid nits;
   - overengineering: remain read-only and review only this slice, then:
     1. derive the minimum required behavior and smallest plausible implementation shape from the slice contract before reading code; distinguish core operations from required safeguards;
     2. inspect only owned/changed files and necessary call sites;
     3. map each abstraction, helper, state machine, dependency, and file to an explicit requirement; for any multi-file slice, independently test the recorded one-file landing order and reject semantic relatedness or final consistency as atomicity proof;
     4. treat file count and LoC as signals only; report a finding only when concrete machinery can be removed or simplified while preserving behavior, contracts, and gates;
     5. treat required error handling, concurrency, recovery, boundaries, and repository conventions as justified; begin neutral.
     Return `CLEAN` or evidence-backed findings naming the mechanism, exact evidence, smaller replacement, and requirements preserved. Exact formatting is optional;
   - style: actively check the changed code against applicable `AGENTS.md`, repository format and lint rules, established local conventions, and any explicit style directives in the invocation. Do not invent personal-preference findings without a concrete governing convention.
6. Spawn a fresh specialist reviewer using the runtime approved for that slice's active review-layer coordinate in the resolved slice workspace. It returns only evidence-backed findings within that layer's rubric or `CLEAN`.
7. The orchestrator validates every finding against live code, executable behavior, or the active layer's governing evidence. Validation requires a reproducible code path, exact file/symbol, failing command, removable concrete complexity, violated style rule or local convention, or other logically decisive proof. Vague possibility or preference is not enough.
8. Reject unsupported findings with a one-line evidence-based reason. Every validated finding, including every valid nit, must be fixed; there is no severity threshold for acceptance.
9. When findings exist, spawn a fresh review-layer fixer using the runtime approved for that slice and layer's fixer coordinate in the resolved slice workspace with only the active layer's validated findings and compact slice contract. Verify its diff, ownership, checks, and commit when applicable.
10. Spawn a fresh post-fix reviewer using the runtime approved for that slice and layer's post-fix-reviewer coordinate in the resolved slice workspace. Repeat validation and fresh fixer/reviewer cycles until the active layer has zero validated findings and all required checks pass.
11. After one layer is clean, advance to the next recorded layer and use entirely fresh agents. A clean style layer after adversarial review does not satisfy the later style occurrence after overengineering review.
12. If any agent discovers a needed edit outside the write allowlist, pause that slice and return control to the orchestrator; never permit opportunistic scope expansion. In full mode, recompute ownership/dependencies and redeploy fresh agents. In simple mode, first determine whether clarification of the existing planned mapping resolves the blocker. If the plan truly must change, recompute ownership/dependencies, preserve every collision rule, update and re-emit the affected deployment-wave matrix as required, then resume the same builder thread with the corrected bounded packet. Use a replacement slice builder only if the original thread is technically unavailable and only after the mandatory user-visible replacement disclosure.
13. In `same_worktree`, wait for all active builders and any enabled full-mode slice review/fix cycles to finish. Re-verify the complete live diff and exclusive ownership, stage only the exact allowlist for one accepted slice, commit it, and repeat per slice. Never use broad staging commands. If files overlap or the Git index contains unowned changes, hard-stop without committing.

In full mode, a slice is clean only when every recorded review-layer occurrence has completed in order with zero orchestrator-validated findings, its accepted commit changes only its owned files, and all applicable gates pass. In simple mode, a slice is accepted only when the slice-builder role's work, including any permitted clarification and repair continuations, passes orchestrator diff, ownership, and gate verification; no clean-review claim is made.

## Retry escalation and hard stop

Track retries independently per bounded unit.

- In full mode, a retry is one completed fix-and-fresh-review cycle that still leaves a validated finding or required-gate failure. The initial build and first review of an active layer do not count as a retry.
- In simple mode, a retry is one completed orchestrator-directed repair continuation by the same slice builder that still leaves its bounded work unacceptable or a required gate failing. A question, pause, blocker report, or refusal caused by missing or incorrect packet facts does not count as a retry until the orchestrator supplies the needed clarification and the builder has a fair opportunity to continue. Resume or reuse the original builder at its matrix-approved builder runtime; if that thread is technically unavailable, a replacement may continue only as the same bounded slice-builder role and only after the mandatory user-visible replacement disclosure. Do not spawn a reviewer, fixer, remediation, or escalation role.

Receipt wording, headings, ordering, or formatting defects never count as retries.

The escalation boundary changes roles, not a global power tier. Preserve retry rules and fresh-role boundaries, and use the separately approved runtime coordinate for every ordinary fixer, reviewer, escalated builder, escalated reviewer, and escalated fixer occurrence.

- Simple-mode retries 1–3 reuse or resume the slice-builder role at its matrix-approved builder runtime. The orchestrator supplies only verified corrections, clarified dependencies or destinations, validated repair instructions, and required checks. After each continuation, independently verify the live diff, ownership, and gates. Do not cancel other active, disjoint builders while this occurs. After the third unsuccessful repair continuation, stop scheduling dependent work, allow already-running disjoint builders to finish safely when doing so cannot worsen the state, then hard-stop with the exact evidence and preserved partial results.
- Full-mode retries 1–3: use a new fixer and a new reviewer with their matrix-approved ordinary retry coordinates for the same active layer each time.
- After the third unsuccessful retry, escalate the same bounded unit in the same resolved workspace:
  1. spawn a fresh builder using the matrix-approved escalated-builder coordinate to diagnose and reimplement/repair within the existing write allowlist;
  2. spawn a fresh reviewer using the matrix-approved escalated-reviewer coordinate and the same active-layer rubric;
  3. have the orchestrator validate findings from live evidence;
  4. spawn a fresh fixer using the matrix-approved escalated-fixer coordinate for validated findings, followed by another fresh reviewer using the matrix-approved escalated-reviewer coordinate.
- Full-mode retries 4–5 remain on the approved escalation coordinates with fresh contexts every cycle.
- After the fifth unsuccessful full-mode retry, hard-stop the swarm. Do not waive findings, downgrade gates, expand ownership ad hoc, or continue to later waves. Report the exact unit, commits, evidence, remaining findings/failures, and current branch state.

## Land and review a full wave

1. Wait until every build slice in the logical wave is clean in full mode or builder-accepted in simple mode. Do not integrate a slice that is incomplete.
2. In `isolated_worktrees`, the orchestrator merges accepted slice branches into its current branch in dependency-safe order, following repository merge conventions. In `same_worktree`, the orchestrator-created allowlist commits are already on the current branch. No child agent merges.
3. Verify each accepted commit is present, ownership remained disjoint, and repository-specified integration gates pass. Any failure blocks the wave and must be repaired; do not accept it as preexisting.
4. When `simple_mode` is `true`, spawn no integrated reviewer or remediation role. On an integration-gate failure, identify the responsible owned slice or slices, give the original owning builder threads the verified failure evidence, and resume or reuse them to repair only their respective allowlists under the simple-mode retry rule. Serialize those continuations when integration safety requires it, then reintegrate and rerun the gates. Accept the wave only from orchestrator verification and passing integration gates. Hard-stop only when an applicable retry limit or another defined terminal condition is reached. Then continue with the next wave. When `simple_mode` is `false`, spawn a fresh reviewer using the runtime approved for that wave's integrated-reviewer coordinate over the fully integrated wave, comparing the current branch to the recorded wave base and checking both the task requirements and emergent cross-slice behavior. The reviewer is read-only and returns only evidence-backed findings or `CLEAN`.
5. Steps 5–10 apply only in full mode. The orchestrator validates every finding from live code/behavior. Every validated finding and nit must be fixed.
6. Partition validated findings into the smallest remediation slices with mutually exclusive write sets. Findings touching the same file belong to one remediation slice; use serial remediation waves when shared files or dependencies require it.
7. For each remediation slice in `isolated_worktrees`, create a separate worktree from the current integrated branch. In `same_worktree`, use the orchestrator worktree, require remediation write sets to be disjoint when run concurrently, and let only the orchestrator stage and commit exact remediation allowlists. Spawn a fresh fixer and then a fresh reviewer in the resolved remediation workspace. Apply the normal validation and retry/escalation rules until clean.
8. In `isolated_worktrees`, merge all clean remediation branches into the orchestrator branch. In `same_worktree`, verify the orchestrator-created remediation commits are present. Run required integration gates and spawn another fresh full-wave reviewer using the approved next occurrence of that wave's integrated-reviewer coordinate.
9. Repeat the full-wave review/remediation loop until a fresh matrix-approved integrated review yields zero orchestrator-validated findings and all wave gates pass.
10. Only then mark the full-mode wave accepted, remove its completed run-created worktrees after collecting receipts, and plan/start the next wave. In simple mode, collect the equivalent receipts after step 4 accepts the wave, but keep original builder threads and any run-created worktrees available through final gates so permitted builder-role continuation remains possible. Remove them during final cleanup.

## Final integrated-task review

After all waves are accepted:

1. Run the repository-defined full gates against the fully integrated task.
2. When `simple_mode` is `true`, spawn no final reviewer or remediation role. On a full-gate failure, identify the responsible original slice owners and resume or reuse those builder threads to make verified, in-allowlist repairs under the simple-mode retry rule; rerun the full gates after reintegration. If ownership or future execution planning must change, preserve the collision rules and update the deployment-wave matrix before affected work continues. Completion requires orchestrator verification and all full gates passing. Hard-stop only when an applicable retry limit or another defined terminal condition is reached, and record the final review result as `not_run_by_design(simple_mode)`. When `simple_mode` is `false`, spawn a fresh reviewer using the runtime approved for the final integrated-reviewer coordinate over the entire task, comparing the final branch to the original run base and reviewing requirements, architecture, cross-wave behavior, tests, documentation, security, performance, regressions, and valid nits.
3. Steps 3–5 apply only in full mode. Validate findings using live evidence.
4. Partition validated findings by exclusive file ownership and run the same matrix-approved remediation fixer/reviewer loop used for wave remediation, including the approved escalation coordinates after retry 3.
5. Integrate clean remediations according to `worktree_mode`, rerun full gates, and repeat with another fresh whole-task reviewer using the approved next occurrence of the final integrated-reviewer coordinate until there are zero validated findings.
6. Full-mode completion requires both a clean final matrix-approved integrated review and all required repository gates passing. Simple-mode completion requires orchestrator verification and all required repository gates passing, with no claim that an independent review occurred.

## Receipt discipline

Keep each receipt compact and factual. It only needs to communicate:

- role outcome and resulting commit;
- changed files or findings;
- checks and decisive evidence;
- blockers, if any.

The orchestrator adds run, wave, slice, runtime, review-layer, retry, merge, and verdict metadata when normalizing the receipt into `receipts.jsonl`.

- Do not reject otherwise usable work because headings, labels, ordering, or formatting differ.
- Do not respawn an agent, restart a phase, roll back a commit, or open remediation solely to repair a report format.
- When a receipt is malformed or incomplete, inspect the live commit, diff, worktree, and checks and reconstruct the facts directly.
- In full implementation mode, spawn a replacement only when a required outcome or evidence cannot be established from live state, not merely because the response format failed, and only after the mandatory user-visible replacement disclosure. In simple implementation mode, ask the same builder for clarification or resume it for genuinely missing work or evidence; receipt formatting alone never consumes a retry. If the original thread is technically unavailable and the outcome cannot be established from live state, a replacement may be spawned only as the same bounded slice-builder role, never as a reviewer, fixer, remediation, or escalation role, and only after that disclosure. Review mode applies the equivalent rule to its same bounded slice-reviewer role as defined in its reference.

Never use agent confidence, prose assurance, or “looks good” as evidence. The orchestrator independently inspects diffs and reruns decisive checks.

## Implementation-mode cleanup

When `review_mode` is `false`, collect all essential evidence into the compact final response before deleting temporary state. Review mode uses the cleanup and report contract in its reference instead.

1. Verify every accepted slice/remediation commit is an ancestor of the orchestrator branch and record final `HEAD` and gate results. In full mode, record the zero-finding final review; in simple mode, record `not_run_by_design(simple_mode)`.
2. Remove only worktrees created for this run, then delete only their run-scoped branches after merge verification. In `same_worktree`, no slice worktrees or slice branches should exist; verify that fact.
3. Delete run-scoped logs, prompt packets, patches, build outputs, and temporary artifacts after their decisive evidence has been compactly recorded.
4. Run `git worktree prune` and verify no worktree, branch, process, lock, or temporary directory bearing this run ID remains.
5. Never remove or alter preexisting worktrees, branches, artifacts, stashes, or user files.
6. On the applicable retry hard stop—three unsuccessful simple-mode repair continuations or five unsuccessful full-mode retries—clean all already-finished swarm worktrees but preserve the minimum failed worktree/branch and compact ledger required for intervention; report them explicitly rather than destroying the only recoverable failing state.

The final report must state canonical phase completion, original and final commits, parent runtime and any required post-warning `obp` acknowledgement evidence, requested and resolved `review_mode`, `worktree_mode`, and `simple_mode`, pre-run proposal emission, final deployment-wave matrix version and its qualifying approval evidence, same-worktree overlap-proof result when applicable, every runtime coordinate with canonical default, raw user request when any, resolved host/model/effort/speed, selection source, translation class and guide version, enabled per-slice review toggles and completed layer sequence, every replacement relationship and its user-visible disclosure when applicable, waves completed, accepted slice/remediation commits, full gate results, final integrated-task review result, and cleanup verification. In simple implementation mode, report the review result as `not_run_by_design(simple_mode)` and never claim a zero-finding independent review. No exact report layout is required. Do not claim completion when any phase, required full-mode layer occurrence, validated finding, failed gate, unmerged accepted commit, unresolved runtime, or run-created worktree remains incomplete.
