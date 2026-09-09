"""Reproducibility metadata and file hashing."""

from __future__ import annotations

import hashlib
import importlib.metadata
import platform
import shlex
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from . import __version__


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def package_versions(names: Iterable[str] | None = None) -> dict[str, str | None]:
    packages = names or (
        "numpy", "pandas", "scipy", "scikit-learn", "umap-learn", "hdbscan",
        "joblib", "PyYAML", "pyarrow", "openpyxl", "xlrd", "Pillow",
        "plotly", "matplotlib",
    )
    versions = {}
    for name in packages:
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = None
    return versions


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def file_record(path: str | Path) -> dict[str, str | int]:
    source = Path(path).resolve()
    return {
        "path": str(source),
        "size_bytes": int(source.stat().st_size),
        "sha256": sha256_file(source),
    }


def package_source_digest() -> str:
    """Hash the installed package's Python sources in stable relative-path order."""

    root = Path(__file__).resolve().parent
    digest = hashlib.sha256()
    for source in sorted(root.glob("*.py"), key=lambda path: path.name):
        digest.update(source.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(source.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def base_manifest(command: list[str] | None = None) -> dict:
    return {
        "manifest_schema": "dimple-gwas.provenance.v3",
        "software": "DIMPLE-GWAS Freeze 3",
        "software_version": __version__,
        "started_at_utc": utc_now(),
        "status": "started",
        "command": shlex.join(command or sys.argv),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "operating_system": platform.system(),
        "architecture": platform.machine(),
        "git_commit": None,
        "package_source_sha256": package_source_digest(),
        "package_versions": package_versions(),
        "warnings": [],
        "exclusions": [],
        "failures": [],
    }
