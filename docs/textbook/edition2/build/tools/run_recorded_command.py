#!/usr/bin/env python3
"""Run one local evidence-producing command and retain a sanitized record."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


FREEZE3 = Path(__file__).resolve().parents[5]


def safe(text: str) -> str:
    return text.replace(str(FREEZE3), "<FREEZE3>").replace(str(Path.home()), "<HOME>")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--record-dir", required=True)
    parser.add_argument("--input", action="append", default=[])
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("a command is required after --")
    record_dir = Path(args.record_dir)
    record_dir.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc)
    process = subprocess.run(command, cwd=FREEZE3, text=True, capture_output=True)
    ended = datetime.now(timezone.utc)
    stdout = safe(process.stdout)
    stderr = safe(process.stderr)
    (record_dir / f"{args.name}.stdout.log").write_text(stdout, encoding="utf-8")
    (record_dir / f"{args.name}.stderr.log").write_text(stderr, encoding="utf-8")
    inputs = []
    for raw in args.input:
        path = FREEZE3 / raw
        inputs.append({"path": raw, "exists": path.is_file(), "sha256": sha256(path) if path.is_file() else None})
    record = {
        "schema": "dimple-gwas.textbook-command-record.v1",
        "name": args.name,
        "command": [safe(part) for part in command],
        "command_display": " ".join(safe(part) for part in command),
        "working_directory": "<FREEZE3>",
        "start_utc": started.isoformat(),
        "end_utc": ended.isoformat(),
        "runtime_seconds": (ended - started).total_seconds(),
        "exit_code": process.returncode,
        "python": platform.python_version(),
        "os": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "thread_controls": {key: os.environ.get(key) for key in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMBA_NUM_THREADS"]},
        "inputs": inputs,
        "stdout_log": f"{args.name}.stdout.log",
        "stderr_log": f"{args.name}.stderr.log",
    }
    (record_dir / f"{args.name}.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    sys.stdout.write(stdout)
    sys.stderr.write(stderr)
    return process.returncode


if __name__ == "__main__":
    raise SystemExit(main())
