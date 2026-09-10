#!/usr/bin/env python3
"""Append one orchestrator-verified receipt from stdin to a JSONL ledger."""

import argparse
import json
import sys
from pathlib import Path


def append_receipt(ledger, receipt):
    """Serialize a supplied receipt; acceptance remains the caller's decision."""
    fields = {"context", "result", "validation"}
    if not isinstance(receipt, dict) or set(receipt) != fields:
        raise ValueError("receipt must contain context, result, and validation")
    if any(not isinstance(receipt[field], dict) for field in fields):
        raise ValueError("context, result, and validation must be JSON objects")
    line = json.dumps(receipt, ensure_ascii=False, sort_keys=True, allow_nan=False)
    with Path(ledger).open("a", encoding="utf-8") as stream:
        stream.write(line + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    args = parser.parse_args()
    try:
        append_receipt(args.ledger, json.load(sys.stdin))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
