#!/usr/bin/env python3
"""Fetch the audited target wheels without installing or resolving host packages.

Standard library only, Python >=3.9. The checked-in plan specifies every version,
filename and expected SHA256. Downloads must agree with both the frozen plan and
the exact-version PyPI metadata. Existing files are verified, never replaced.
"""

import argparse
import concurrent.futures
import datetime
import email.parser
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import sys
import threading
import time
import urllib.parse
import urllib.request
import uuid
import zipfile


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def immutable_write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != payload:
            raise RuntimeError("Refusing to replace existing different artifact: " + str(path))
        return
    with path.open("xb") as handle:
        handle.write(payload)


def canonical_name(name):
    return re.sub(r"[-_.]+", "-", name).lower()


class Fetcher:
    def __init__(self, build_root, event_path):
        self.build_root = build_root
        self.event_path = event_path
        self.event_lock = threading.Lock()

    def event(self, **values):
        record = {"at": now(), **values}
        with self.event_lock:
            with self.event_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, sort_keys=True) + "\n")

    def fetch(self, url, destination, allowed_host, expected_sha256=None):
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme != "https" or parsed.hostname != allowed_host or parsed.username or parsed.password:
            raise ValueError("Disallowed download URL: " + url)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            digest = sha256_file(destination)
            if expected_sha256 and digest != expected_sha256:
                raise RuntimeError("Existing artifact checksum mismatch: " + str(destination))
            self.event(operation="verify_existing", url=url, path=str(destination), sha256=digest)
            return digest
        part = destination.with_name(destination.name + "." + uuid.uuid4().hex + ".part")
        for attempt in range(1, 4):
            try:
                request = urllib.request.Request(url, headers={"User-Agent": "DIMPLE-GWAS-locked-wheel-fetch/1"})
                with urllib.request.urlopen(request, timeout=60) as response:
                    final_url = urllib.parse.urlparse(response.geturl())
                    if final_url.scheme != "https" or final_url.hostname != allowed_host:
                        raise ValueError("Download redirected outside the approved HTTPS host")
                    with part.open("xb") as handle:
                        for chunk in iter(lambda: response.read(1024 * 1024), b""):
                            handle.write(chunk)
                digest = sha256_file(part)
                if expected_sha256 and digest != expected_sha256:
                    raise RuntimeError("Downloaded artifact checksum mismatch: " + str(destination))
                # Atomic no-overwrite publication on the same filesystem.
                os.link(str(part), str(destination))
                part.unlink()
                self.event(operation="download_verified", url=url, path=str(destination),
                           sha256=digest, bytes=destination.stat().st_size, attempt=attempt)
                return digest
            except Exception as error:
                if part.exists():
                    part.unlink()
                self.event(operation="download_error", url=url, attempt=attempt,
                           error=type(error).__name__ + ": " + str(error))
                if attempt == 3 or isinstance(error, (ValueError, RuntimeError, FileExistsError)):
                    raise
                time.sleep(attempt)

    def wheel(self, entry):
        name, version = entry["package"], entry["version"]
        expected_metadata_url = "https://pypi.org/pypi/{}/{}/json".format(name, version)
        if entry["metadata_url"] != expected_metadata_url:
            raise ValueError("Plan must use exact-version primary PyPI metadata")
        filename = entry["filename"]
        if Path(filename).name != filename or not filename.endswith(".whl"):
            raise ValueError("Invalid wheel filename")
        if not (filename.endswith("-none-any.whl") or
                ("-cp312-cp312-" in filename and "manylinux" in filename and "x86_64" in filename)):
            raise ValueError("Wheel does not match audited CPython3.12 Linux AMD64 target")
        metadata_path = self.build_root / "metadata" / (canonical_name(name) + "-" + version + ".json")
        metadata_sha = self.fetch(expected_metadata_url, metadata_path, "pypi.org")
        metadata = json.loads(metadata_path.read_text())
        if canonical_name(metadata["info"]["name"]) != canonical_name(name) or metadata["info"]["version"] != version:
            raise ValueError("PyPI distribution identity differs from frozen plan")
        matches = [item for item in metadata["urls"] if item["filename"] == filename]
        if len(matches) != 1 or matches[0].get("yanked"):
            raise ValueError("Audited wheel missing or yanked: " + filename)
        artifact = matches[0]
        if artifact["digests"]["sha256"] != entry["sha256"]:
            raise ValueError("PyPI wheel hash differs from frozen audit: " + filename)
        wheel_path = self.build_root / "wheelhouse" / filename
        digest = self.fetch(artifact["url"], wheel_path, "files.pythonhosted.org", entry["sha256"])
        if wheel_path.stat().st_size != artifact["size"]:
            raise ValueError("Wheel length differs from PyPI metadata")
        with zipfile.ZipFile(wheel_path) as archive:
            names = [item for item in archive.namelist()
                     if item.endswith(".dist-info/METADATA") and item.count("/") == 1]
            if len(names) != 1:
                raise ValueError("Wheel has ambiguous distribution metadata")
            wheel_metadata = email.parser.BytesParser().parsebytes(archive.read(names[0]))
            if canonical_name(wheel_metadata["Name"]) != canonical_name(name) or wheel_metadata["Version"] != version:
                raise ValueError("Wheel metadata identity differs from plan")
        return {**entry, "artifact_url": artifact["url"], "bytes": wheel_path.stat().st_size,
                "downloaded_sha256": digest, "metadata_file": str(metadata_path.relative_to(self.build_root)),
                "metadata_sha256": metadata_sha, "wheel_file": "wheelhouse/" + filename,
                "upload_time": artifact["upload_time_iso_8601"],
                "requires_python": wheel_metadata["Requires-Python"],
                "requires_dist": wheel_metadata.get_all("Requires-Dist", [])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--phase", choices=("build", "all"), default="all")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if not 1 <= args.workers <= 8:
        parser.error("--workers must be between 1 and 8")
    script_root = Path(__file__).resolve().parent
    plan_path = script_root / "wheel_plan.json"
    plan = json.loads(plan_path.read_text())
    build_root = args.run_root.resolve() / "builds" / "lane_c"
    log_root = args.run_root.resolve() / "logs" / "lane_c"
    build_root.mkdir(parents=True, exist_ok=True)
    log_root.mkdir(parents=True, exist_ok=True)
    invocation = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    event_path = log_root / ("fetch-" + invocation + ".jsonl")
    command_path = log_root / ("command-" + invocation + ".json")
    immutable_write(command_path, (json.dumps({"started_at": now(), "argv": sys.argv,
                    "working_directory": str(Path.cwd()), "host_python": sys.version,
                    "host_platform": platform.platform(), "script_sha256": sha256_file(Path(__file__)),
                    "plan_sha256": sha256_file(plan_path), "purpose": "download only; no host install or resolution"},
                    indent=2, sort_keys=True) + "\n").encode())
    immutable_write(build_root / "wheel_plan.json", plan_path.read_bytes())
    lock_records = {}
    for group, entries in plan["groups"].items():
        content = "# DIMPLE-GWAS Freeze3 {} lock; selected {}\n".format(group, plan["selection_date"])
        content += "# Target CPython {} {}; exact audited wheel bytes; no optional extras\n".format(plan["python"], plan["platform"])
        content += "# Install offline with --no-index --find-links=/wheelhouse --require-hashes\n"
        for entry in sorted(entries, key=lambda item: canonical_name(item["package"])):
            content += "{}=={} --hash=sha256:{}\n".format(entry["package"], entry["version"], entry["sha256"])
        for root in (script_root, build_root / "locks"):
            immutable_write(root / (group + ".lock"), content.encode())
        lock_records[group] = {"file": "locks/" + group + ".lock",
                               "sha256": hashlib.sha256(content.encode()).hexdigest(),
                               "package_count": len(entries)}
    selected_groups = ("build",) if args.phase == "build" else ("build", "runtime", "test")
    unique = {}
    membership = {}
    for group in selected_groups:
        for entry in plan["groups"][group]:
            key = canonical_name(entry["package"])
            if key in unique and unique[key] != entry:
                raise ValueError("Conflicting group pins: " + key)
            unique[key] = entry
            membership.setdefault(key, []).append(group)
    fetcher = Fetcher(build_root, event_path)
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            artifacts = list(pool.map(fetcher.wheel, unique.values()))
        for artifact in artifacts:
            artifact["groups"] = membership[canonical_name(artifact["package"])]
        manifest = {"schema_version": 1, "selection_date": plan["selection_date"],
                    "python": plan["python"], "platform": plan["platform"], "base_image": plan["base_image"],
                    "source_identity": plan["source_identity"], "plan_sha256": sha256_file(plan_path),
                    "locks": lock_records, "phase": args.phase, "artifact_count": len(artifacts),
                    "artifacts": sorted(artifacts, key=lambda item: canonical_name(item["package"]))}
        manifest_path = build_root / ("build-artifacts.json" if args.phase == "build" else "artifact-manifest.json")
        immutable_write(manifest_path, (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode())
        fetcher.event(operation="complete", phase=args.phase, artifacts=len(artifacts),
                      manifest=str(manifest_path), manifest_sha256=sha256_file(manifest_path))
        print("BUILD_TOOL_WHEELS_READY" if args.phase == "build" else "ALL_LOCKED_WHEELS_READY", flush=True)
        print(json.dumps({"manifest": str(manifest_path), "artifacts": len(artifacts),
                          "wheelhouse": str(build_root / "wheelhouse"), "events": str(event_path)}, sort_keys=True))
    except Exception as error:
        fetcher.event(operation="failed", phase=args.phase, error=type(error).__name__ + ": " + str(error))
        raise


if __name__ == "__main__":
    main()
