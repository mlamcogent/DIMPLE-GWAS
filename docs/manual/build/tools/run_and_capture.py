#!/usr/bin/env python3
"""Run a command, capture an auditable log, and emit timing/status metadata."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from time import monotonic


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True, type=Path)
    parser.add_argument("--meta", required=True, type=Path)
    parser.add_argument("--cwd", required=True, type=Path)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if not args.command:
        raise SystemExit("command is required")
    command = args.command[1:] if args.command[0] == "--" else args.command
    args.log.parent.mkdir(parents=True, exist_ok=True)
    args.meta.parent.mkdir(parents=True, exist_ok=True)

    started = datetime.now(timezone.utc)
    timer = monotonic()
    process = subprocess.run(command, cwd=args.cwd, text=True, capture_output=True)
    duration = monotonic() - timer
    ended = datetime.now(timezone.utc)
    combined = (
        f"COMMAND: {json.dumps(command)}\n"
        f"WORKING_DIRECTORY: {args.cwd.resolve()}\n"
        f"STARTED_UTC: {started.isoformat()}\n"
        f"ENDED_UTC: {ended.isoformat()}\n"
        f"DURATION_SECONDS: {duration:.6f}\n"
        f"EXIT_CODE: {process.returncode}\n\n"
        "===== STDOUT =====\n"
        f"{process.stdout}\n"
        "===== STDERR =====\n"
        f"{process.stderr}\n"
    )
    args.log.write_text(combined, encoding="utf-8")
    args.meta.write_text(
        json.dumps(
            {
                "command": command,
                "working_directory": str(args.cwd.resolve()),
                "started_utc": started.isoformat(),
                "ended_utc": ended.isoformat(),
                "duration_seconds": duration,
                "exit_code": process.returncode,
                "log": str(args.log.resolve()),
                "selected_environment": {
                    "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"),
                    "OPENBLAS_NUM_THREADS": os.environ.get("OPENBLAS_NUM_THREADS"),
                    "MKL_NUM_THREADS": os.environ.get("MKL_NUM_THREADS"),
                    "NUMBA_NUM_THREADS": os.environ.get("NUMBA_NUM_THREADS"),
                },
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    raise SystemExit(process.returncode)


if __name__ == "__main__":
    main()
