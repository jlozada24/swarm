# Simple-mode automation

Use only for `simple_mode: true`, `review_mode: false`. One Python standard-library helper handles formatting and bookkeeping. The orchestrator still plans, obtains approval, launches agents, manages Git, verifies evidence, and decides acceptance. The helper never executes a check, launches an agent, or infers approval or completion.

## One plan, four commands

Write `plan-v1.json` once in an external temporary run directory while planning. Keep `state.jsonl`, `receipts.jsonl`, saved packets, and returned results there too. Use absolute paths. Preserve each emitted plan; revisions use a new version/file and the existing matrix approval rule. Do not overwrite an emitted plan or copy its static facts into every state event. Each recorded entry includes the version and content digest automatically. These files are temporary run artifacts covered by normal cleanup.

The plan mirrors the existing matrix; it adds no new planning decisions:

```json
{
  "run_id": "example",
  "version": 1,
  "settings": {"simple_mode": true, "review_mode": false, "worktree_mode": "auto"},
  "metadata": {},
  "shared": {"instructions": [], "constraints": []},
  "rows": [
    {
      "id": "S01", "kind": "slice", "wave": "W01",
      "depends_on": [], "objective": "Task-specific objective",
      "write_files": ["src/example.py"], "read_context": [],
      "constraints": [], "checks": [], "acceptance": [],
      "classification": {"matched_rule": "default", "facts": {}},
      "builders": [
        {
          "coordinate": "W01/S01/builder/1",
          "workspace": "/absolute/workspace", "placement": "same_worktree",
          "git_policy": "orchestrator",
          "runtime": {}
        }
      ]
    }
  ]
}
```

This illustrates shape, not an executable proposal. Fill the existing required facts: all resolved flags in `settings`; requested flags, normalized best-of-N policy, parent runtime, approval-slot facts, and any relocation disclosure in `metadata`; applicable repository instructions and shared negative constraints in `shared`. Include `no test creation or modification` unless explicitly requested, plus any stricter repository prohibition on running tests. Slice `read_context` holds exact paths/symbols and necessary dependency facts. `checks` contains the permitted command strings; `acceptance` contains the actual criteria.

Each builder's `runtime` holds its Task / selected-level baseline, shared policy and routing source paths and fingerprints, host, model, exact effort, configured route, exact tag/slug and invocation surface, route verification status/evidence, required capacity and verification evidence, raw request when any, assignment/selection sources, translation class, and guide version. Resolve these from the shared Delegate policy under `references/runtime-translation.md`; the helper passes them through without choosing models. List every initial best-of-N candidate. `git_policy` is `builder` only for dedicated isolated slice/candidate worktrees; use `orchestrator` for the orchestrator workspace and reused overlap groups. Add overlap-group membership, isolation reason, and serialized order to the relevant builder object. Multi-file exceptions carry the existing attempted order and atomicity proof in the row's `atomicity` object.

Include each wave gate and final gate as a `kind: "gate"` row with a unique `id`, explicit `depends_on`, objective, `workspace`, checks/acceptance, and empty `write_files`/`builders`. Keep all rows in the approved dependency order. The helper formats supplied rows; it does not invent omitted gates, resolve models, or validate the DAG.

Commands, with `HELPER` standing for the absolute path to `scripts/swarm.py`:

```text
python3 HELPER matrix PLAN
python3 HELPER prompt PLAN COORDINATE --base COMMIT
python3 HELPER record PLAN COORDINATE LEDGER < RESULT_JSON
python3 HELPER report PLAN RECEIPTS_LEDGER
```

- **Matrix:** prints the table, settings, proposal facts, and atomicity proofs to stdout. Inspect it for completeness and present it under the existing two-slot gate. Formatting does not grant approval.
- **Prompt:** after approval and dependency verification, pass the actual dependency-complete commit. Prints only that builder's packet, with shared constraints once, empty optional fields omitted, and no truncation. It ends with `APPROVED, PROCEED`; call it only for authorized dispatch. Save and send the output without rewriting it. Runtime metadata remains in the plan for the launcher, not in the child packet.
- **Record:** pipe the builder's compact JSON result directly to `receipts.jsonl`. Expected result fields are `status`, `commit` (or null), `files`, `checks`, and `blockers`; each check has `command`, `exit_status`, and decisive `evidence`. Identity, version, workspace, and runtime are attached automatically. A result is unverified until the orchestrator records its own verdict. For non-JSON responses, reconstruct only the missing structured facts from the response/live evidence; do not ask the builder to redo completed work for formatting.
- **Report:** reads the supplied receipt ledger and, when present, its adjacent `state.jsonl`. Prints statuses, recorded evidence, run events, settings, and placements. Unrecorded coordinates remain unverified. Earlier-plan records are shown separately and never silently become current-plan verification. Use the generated facts for the final response, then apply the existing completion criteria and cleanup rules.

## Results, verification, and state

Only the orchestrator writes either ledger. The helper accepts a raw result object or an envelope containing `result` and/or `validation`. To record verification, supply `{"validation":{"status":"accepted","evidence":["decisive evidence"]}}` to the same builder coordinate. A later result clears that coordinate's previous verdict in the report until fresh verification is recorded. Record the selected candidate and slice acceptance under the row ID; record integration gates under their gate row IDs. This separates candidate completion from accepted, integrated work without asking children to track it.

Use coordinate `RUN` and `state.jsonl` for small run events, for example `{"event":"phase","phase":"P05","status":"active"}`. Supply approval evidence, verified dependency bases, selection/merge facts, negative-constraint verdicts, replacement disclosures, and cleanup outcomes as events at the transitions that require them. Run events are printed as supplied; the helper does not advance phases or judge their validity. After a plan revision, record any carried-forward acceptance with its original evidence under the new plan only after verifying it still applies.

Use this versioned format for new simple-mode runs; it does not migrate older in-progress ledgers. Full implementation and review-only runs keep their current packet and ledger workflow. Their existing `append_receipt.py LEDGER` command and receipt envelope remain supported.
