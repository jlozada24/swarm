#!/usr/bin/env python3
"""Render simple-mode plans and packets, record facts, and summarize ledgers."""

import argparse
import hashlib
import html
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from append_receipt import append_receipt


def compact(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False)


def cell(value):
    text = value if isinstance(value, str) else compact(value)
    return html.escape(text, quote=False).replace("|", "&#124;").replace("\n", "<br>")


def table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    lines.extend("| " + " | ".join(cell(v) for v in row) + " |" for row in rows)
    return "\n".join(lines)


def load_plan(path):
    plan = json.loads(path.read_text(encoding="utf-8"))
    if plan["settings"]["simple_mode"] is not True or plan["settings"]["review_mode"] is not False:
        raise ValueError("swarm.py supports simple implementation mode only")
    if not plan["run_id"] or type(plan["version"]) is not int or plan["version"] < 1:
        raise ValueError("plan needs a run_id and a positive integer version")
    targets = {"RUN": ({}, {})}
    for row in plan["rows"]:
        if row["kind"] not in ("slice", "gate"):
            raise ValueError("row kind must be slice or gate")
        if row["kind"] == "slice" and not 1 <= len(row["builders"]) <= 3:
            raise ValueError("slice needs one to three settled builder positions")
        if row["kind"] == "gate" and row["builders"]:
            raise ValueError("simple-mode gates cannot spawn agents")
        for coordinate, builder in [(row["id"], {})] + [(b["coordinate"], b) for b in row["builders"]]:
            if coordinate in targets:
                raise ValueError(f"duplicate coordinate: {coordinate}")
            targets[coordinate] = (row, builder)
    return plan, targets, hashlib.sha256(compact(plan).encode("utf-8")).hexdigest()


def matrix(plan):
    rows = []
    shared = plan["shared"]["constraints"]
    for row in plan["rows"]:
        builders = row["builders"]
        workspaces = [{k: v for k, v in b.items() if k != "runtime"} for b in builders]
        runtime = [{"coordinate": b["coordinate"], **b["runtime"]} for b in builders]
        gates = shared + row.get("constraints", []) + row["checks"] + row["acceptance"]
        if row["kind"] == "slice":
            gates = gates + [{"candidates": len(builders), **row["classification"]}]
        rows.append([row["wave"], row["id"], row["depends_on"], row["objective"],
                     row["write_files"] or "none", workspaces or row["workspace"], runtime or "none",
                     "builder only" if builders else "orchestrator verification; not_run_by_design(simple_mode)",
                     gates])
    output = [f"Deployment-wave matrix — {plan['run_id']} v{plan['version']}",
              "Settings: " + compact(plan["settings"]),
              "Proposal facts: " + compact(plan["metadata"]),
              table(["Wave", "Slice / gate", "Depends on", "Objective", "Exclusive writable files",
                     "Workspace", "Runtime placements", "Review sequence", "Gates / acceptance"], rows)]
    for row in plan["rows"]:
        if row.get("atomicity"):
            output.append(f"Atomicity — {row['id']}: {compact(row['atomicity'])}")
    return "\n\n".join(output)


def prompt(plan, row, builder, base):
    if not builder:
        raise ValueError("prompt requires a builder coordinate")
    policy = builder["git_policy"]
    if policy not in ("orchestrator", "builder"):
        raise ValueError("git_policy must be orchestrator or builder")
    lines = [f"Slice builder: {builder['coordinate']}", f"Objective: {row['objective']}",
             f"Workspace: {builder['workspace']}\nBase commit: {base}",
             "Writable files: " + compact(row["write_files"])]
    fields = [("Read context / dependency facts", row.get("read_context", [])),
              ("Repository instructions", plan["shared"]["instructions"]),
              ("Negative constraints", plan["shared"]["constraints"] + row.get("constraints", [])),
              ("Acceptance", row["acceptance"]), ("Assigned checks", row["checks"]),
              ("Atomicity proof", row.get("atomicity"))]
    lines.extend(f"{label}: {compact(value)}" for label, value in fields if value)
    lines.append("Read applicable AGENTS.md. Other agents are active: preserve their work and edit only "
                 "your allowlist in this workspace. Read related files as needed. Never merge, rebase, "
                 "switch branches, or expand scope. Obey the negative constraints; add no speculative "
                 "fallbacks, hardening, or compatibility behavior. A guard is allowed only for the "
                 "smallest orchestrator-validated in-scope bug repair without contract expansion. "
                 "Run only assigned, permitted checks and report failures. For missing facts or a needed "
                 "out-of-scope edit, ask the orchestrator and remain available to continue this slice.")
    lines.append("Do not stage, commit, or modify the Git index; the orchestrator owns commits."
                 if policy == "orchestrator" else
                 "Commit only your owned changes in this dedicated worktree before reporting.")
    lines.append('Return a compact JSON object with status, commit (or null), files, checks, and blockers. '
                 'Each check contains command, exit_status, and decisive evidence. Include no plan or '
                 'runtime metadata. A formatting difference is not a work failure.')
    lines.append("APPROVED, PROCEED")
    return "\n\n".join(lines)


def record(plan, digest, coordinate, row, builder, ledger, payload):
    if not isinstance(payload, dict) or not payload:
        raise ValueError("stdin must be a nonempty JSON object")
    if "result" not in payload and "validation" not in payload:
        payload = {"result": payload}
    if set(payload) - {"result", "validation"}:
        raise ValueError("enveloped input may contain only result and/or validation")
    context = {"run_id": plan["run_id"], "plan_version": plan["version"],
               "plan_digest": digest, "coordinate": coordinate}
    if row:
        context.update(wave=row["wave"], slice=row["id"])
    if builder:
        context.update(workspace=builder["workspace"], runtime=builder["runtime"])
    append_receipt(ledger, {"context": context, "result": payload.get("result", {}),
                            "validation": payload.get("validation", {})})


def report(plan, targets, digest, ledger):
    paths = [ledger]
    state = ledger.with_name("state.jsonl")
    if state != ledger and state.exists():
        paths.append(state)
    current, earlier, events = {}, [], []
    for path in paths:
        for line in path.read_text(encoding="utf-8").splitlines():
            item = json.loads(line)
            context = item["context"]
            if context["run_id"] != plan["run_id"]:
                continue
            if context["plan_version"] != plan["version"] or context["plan_digest"] != digest:
                earlier.append(item)
                continue
            coordinate = context["coordinate"]
            if coordinate not in targets:
                raise ValueError(f"unknown recorded coordinate: {coordinate}")
            if coordinate == "RUN":
                events.append({"result": item["result"], "validation": item["validation"]})
                continue
            latest = current.setdefault(coordinate, {"result": {}, "validation": {}})
            if item["result"]:
                latest["result"] = item["result"]
                latest["validation"] = {}  # A later result requires fresh verification.
            if item["validation"]:
                latest["validation"] = item["validation"]
    rows, placements = [], []
    details = []
    for coordinate in targets:
        if coordinate == "RUN":
            continue
        row, builder = targets[coordinate]
        if builder:
            placements.append({"coordinate": coordinate, **builder})
        item = current.get(coordinate, {"result": {}, "validation": {}})
        result, validation = item["result"], item["validation"]
        rows.append([coordinate, result.get("status", "not recorded"),
                     validation.get("status", "unverified"),
                     validation.get("commit", result.get("commit")), result.get("blockers", [])])
        if result or validation:
            details.append(f"{coordinate}: {compact(item)}")
    scopes = [{"slice": row["id"], "files": row["write_files"],
               "classification": row["classification"], "candidates": len(row["builders"])}
              for row in plan["rows"] if row["kind"] == "slice"]
    output = [f"Recorded results — {plan['run_id']} v{plan['version']}",
              "Recorded facts only; this report does not declare completion or independent review.",
              table(["Coordinate", "Reported status", "Orchestrator verdict", "Recorded commit", "Reported blockers"], rows),
              "Run events (phase, approval, integration, cleanup): " + (compact(events) if events else "not recorded"),
              "Evidence:\n" + ("\n".join(details) or "none recorded"),
              "Settings: " + compact(plan["settings"]), "Plan facts: " + compact(plan["metadata"]),
              "Slice scope / candidate policy: " + compact(scopes),
              "Runtime / workspace placements: " + compact(placements)]
    if earlier:
        output.append("Earlier plan records (not current-plan verification):\n" +
                      "\n".join(compact(item) for item in earlier))
    return "\n\n".join(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    descriptions = {"matrix": "Render the proposal table from a settled plan",
                    "prompt": "Render one builder packet after approval",
                    "record": "Append supplied facts with plan metadata; JSON on stdin",
                    "report": "Summarize receipts and adjacent state.jsonl"}
    for name, description in descriptions.items():
        command = commands.add_parser(name, help=description, description=description)
        command.add_argument("plan", type=Path)
        if name in ("prompt", "record"):
            command.add_argument("coordinate")
        if name == "prompt":
            command.add_argument("--base", required=True, help="Verified dependency-complete commit")
        if name in ("record", "report"):
            command.add_argument("ledger", type=Path)
    args = parser.parse_args()
    try:
        plan, targets, digest = load_plan(args.plan)
        if args.command == "matrix":
            print(matrix(plan))
        elif args.command == "prompt":
            print(prompt(plan, *targets[args.coordinate], args.base))
        elif args.command == "record":
            record(plan, digest, args.coordinate, *targets[args.coordinate], args.ledger, json.load(sys.stdin))
        else:
            print(report(plan, targets, digest, args.ledger))
    except (ValueError, KeyError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
