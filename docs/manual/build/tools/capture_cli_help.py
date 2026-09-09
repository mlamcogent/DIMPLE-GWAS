#!/usr/bin/env python3
"""Capture top-level and subcommand help from the installed Freeze 3 CLI."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


COMMANDS = [
    "run",
    "inspect-config",
    "show-search-space",
    "score-existing",
    "summarize-models",
    "reproduce-model",
    "explain",
    "interpret",
    "compare",
    "validate",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--executable", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    for command in [None, *COMMANDS]:
        invocation = [str(args.executable)] + ([] if command is None else [command]) + ["--help"]
        process = subprocess.run(invocation, text=True, capture_output=True)
        name = "top_level" if command is None else command.replace("-", "_")
        output = process.stdout + (f"\n===== STDERR =====\n{process.stderr}" if process.stderr else "")
        output_path = args.output_dir / f"{name}.txt"
        output_path.write_text(output, encoding="utf-8")
        records.append(
            {
                "command": command or "<top-level>",
                "invocation": invocation,
                "exit_code": process.returncode,
                "output": str(output_path.resolve()),
            }
        )
    (args.output_dir / "help_capture_manifest.json").write_text(
        json.dumps(records, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    failures = [record for record in records if record["exit_code"] != 0]
    if failures:
        raise SystemExit(f"help capture failures: {failures}")


if __name__ == "__main__":
    main()
