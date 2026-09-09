#!/usr/bin/env python3
"""Task-scoped offline builds from immutable allowlisted inputs; never publishes."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import zipfile

DOCKER = Path(__file__).resolve().parents[1]
BASE = "python:3.12.14-slim-bookworm@sha256:9c47360a2a0355e2da18516d0b1c2126ec22c195d2185e97347c9d98398c5bef"
BUILDKIT = "moby/buildkit@sha256:2f5adac4ecd194d9f8c10b7b5d7bceb5186853db1b26e5abd3a657af0b7e26ec"
WHEEL = "dimple_gwas-3.0.0rc1-py3-none-any.whl"

def sha(p):
    h = hashlib.sha256()
    with Path(p).open("rb") as f:
        for block in iter(lambda: f.read(8*1024*1024), b""):
            h.update(block)
    return h.hexdigest()

def write_json(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        raise RuntimeError("refusing to overwrite " + str(p))
    p.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")

def copy_checked(src, dst, expected=None):
    if src.is_symlink() or not src.is_file():
        raise RuntimeError("not an ordinary file: " + str(src))
    if expected and sha(src) != expected:
        raise RuntimeError("checksum mismatch: " + str(src))
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        raise RuntimeError("refusing overwrite: " + str(dst))
    shutil.copy2(src, dst)

def run(root, label, cmd):
    wrapper = root / "coordination/run_command.py"
    subprocess.run([sys.executable, str(wrapper), "--label", label, "--", *map(str, cmd)], check=True)

def context_manifest(root, context):
    rows = []
    for p in sorted(context.rglob("*")):
        if p.is_symlink():
            raise RuntimeError("context symlink: " + str(p))
        if p.is_file():
            rel = str(p.relative_to(context))
            if any(part in {".git", ".env", ".venv", "test_data", "__pycache__"} for part in p.parts):
                raise RuntimeError("forbidden context file: " + rel)
            rows.append({"path": rel, "bytes": p.stat().st_size, "sha256": sha(p)})
    write_json(root / "manifests" / (context.name + "-context.json"), rows)

def verify_context(root, context):
    """Reject changed bytes or added files before Docker can read a context."""
    expected = json.loads((root/"manifests"/(context.name+"-context.json")).read_text())
    actual = []
    for item in sorted(context.rglob("*")):
        if item.is_symlink():
            raise RuntimeError("context symlink: " + str(item))
        if item.is_file():
            actual.append({"path":str(item.relative_to(context)), "bytes":item.stat().st_size, "sha256":sha(item)})
    if actual != expected:
        raise RuntimeError("frozen context differs from its recorded allowlist; refusing build")

def prepare(root, identity, kind):
    context = root / "contexts" / kind
    context.mkdir(exist_ok=False)
    copy_checked(DOCKER / "Dockerfile", context / "Dockerfile")
    (context / ".dockerignore").write_text(".git\n.env\n**/__pycache__\n**/*.pyc\n")
    data = root / "builds/lane_c"
    if kind == "wheel":
        records = json.loads((data / "build-artifacts.json").read_text())["artifacts"]
        for entry in identity["files"]:
            copy_checked(root/"source/freeze3"/entry["path"], context/"source"/entry["path"], entry["sha256"])
        copy_checked(data/"locks/build.lock", context/"locks/build.lock")
    else:
        # Artifact records, rather than resolver output, are the actual byte allowlist.
        manifests = [data / "artifact-manifest.json"]
        by_name = {}
        for manifest in manifests:
            for item in json.loads(manifest.read_text())["artifacts"]:
                groups = item["groups"]
                if "runtime" in groups or "test" in groups or item["package"] == "pip":
                    by_name[item["filename"]] = item
        records = list(by_name.values())
        if not records or not any(x["package"] == "numpy" for x in records):
            raise RuntimeError("runtime wheelhouse not complete")
        for group in ("runtime", "test"):
            copy_checked(data/"locks"/(group+".lock"), context/"locks"/(group+".lock"))
        pip_record = next(x for x in records if x["package"] == "pip")
        (context/"locks/pip.lock").write_text("pip=="+pip_record["version"]+" --hash=sha256:"+pip_record["sha256"]+"\n")
        frozen = json.loads((root/"wheel/wheel-manifest.json").read_text())
        copy_checked(root/"wheel"/WHEEL, context/"wheel"/WHEEL, frozen["sha256"])
        copy_checked(root/"source/freeze3/LICENSE", context/"LICENSE")
        write_json(context/"source.json", {"source_sha256":identity["source_sha256"], "git_commit":None, "identity_kind":"content-sha256", "version":"3.0.0rc1", "wheel_sha256":frozen["sha256"]})
    for entry in records:
        copy_checked(data/entry["wheel_file"], context/"wheelhouse"/entry["filename"], entry["sha256"])
    context_manifest(root, context)
    print("Prepared", context)

def build_args(identity, context):
    args = ["--build-arg", "PYTHON_BASE="+BASE, "--build-arg", "SOURCE_DATE_EPOCH="+str(identity["source_date_epoch"])]
    if (context/"wheel"/WHEEL).exists():
        args += ["--build-arg", "WHEEL_SHA256="+sha(context/"wheel"/WHEEL), "--build-arg", "SOURCE_SHA256="+identity["source_sha256"], "--build-arg", "LOCK_SHA256="+sha(context/"locks/runtime.lock")]
    return args

def builder(root, suffix):
    return "dimple-" + root.name.rsplit("-",1)[-1] + "-" + suffix

def image_tag(identity, context, test=False):
    profile = "current-test" if test else "current"
    return "dimple-gwas:3.0.0rc1-"+identity["source_sha256"][:12]+"-"+sha(context/"locks/runtime.lock")[:12]+"-"+profile+"-amd64"

def assert_new_tag(tag):
    check = subprocess.run(["docker","image","inspect",tag],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    if check.returncode == 0:
        raise RuntimeError("immutable tag already exists: " + tag)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["prepare-wheel","prepare-current","create-builder","build-wheel","build-current-test","build-current","inspect-current","export-current","rebuild-current","publication-dry-run"])
    p.add_argument("--run-root",required=True,type=Path)
    p.add_argument("--builder-suffix",default="a",choices=["a","b"])
    a=p.parse_args()
    root=a.run_root.resolve()
    if root.parent.name != "runs" or root.parent.parent.name != "docker_validation":
        p.error("run-root must be an existing task run under docker_validation/runs")
    identity=json.loads((root/"inventory/source_identity.json").read_text())
    if a.action.startswith("prepare-"):
        prepare(root,identity,a.action.split("-",1)[1]);return
    if a.action == "create-builder":
        run(root,"create-builder-"+a.builder_suffix,["docker","buildx","create","--name",builder(root,a.builder_suffix),"--driver","docker-container","--driver-opt","image="+BUILDKIT]);return
    if a.action == "publication-dry-run":
        context=root/"contexts/current";tag=image_tag(identity,context)
        image_file=root/"manifests/current-image.json"
        manifest_file=root/"manifests/release-manifest.json"
        inspection=json.loads(image_file.read_text())[0] if image_file.exists() else {}
        release=json.loads(manifest_file.read_text()) if manifest_file.exists() else {}
        print(json.dumps({"local_tag":tag,"local_image_id":inspection.get("Id"),
            "proposed_remote_tag":"zymlam/"+tag,"platform":"linux/amd64",
            "validation_status":release.get("overall_status","UNASSESSED"),
            "publication_allowed":False,
            "validation_report":str(root/"reports/10_release_readiness_report.md"),
            "sbom_available":(root/"sbom/current-verified/sbom.spdx.json").exists(),
            "local_unsigned_provenance_available":(root/"manifests/local-unsigned-provenance.json").exists(),
            "provenance_limit":"Minimal BuildKit statement has empty subject; local supplement unsigned; no registry attestation",
            "action":"DRY_RUN_ONLY; commands for later approved release after blockers are resolved",
            "commands":[["docker","tag",tag,"zymlam/"+tag],["docker","push","zymlam/"+tag]],
            "signing":"NOT_RUN; requires verified registry digest and separately configured signing identity"},indent=2));return
    if a.action == "inspect-current":
        context=root/"contexts/current";tag=image_tag(identity,context)
        content=subprocess.check_output(["docker","image","inspect",tag])
        write_json(root/"manifests/current-image.json",json.loads(content))
        run(root,"current-history",["docker","history","--no-trunc",tag]);return
    if a.action == "export-current":
        context=root/"contexts/current";tag=image_tag(identity,context)
        archive=root/"oci/current.docker.tar"
        if archive.exists():raise RuntimeError("archive exists")
        run(root,"export-current-docker",["docker","image","save","--output",archive,tag])
        with tarfile.open(archive) as tar:
            meta=json.load(tar.extractfile("manifest.json"))
            if len(meta)!=1 or tag not in meta[0]["RepoTags"]:raise RuntimeError("unexpected archive references")
        write_json(root/"oci/current.docker.tar.manifest.json",{"format":"docker-archive","sha256":sha(archive),"bytes":archive.stat().st_size,"tag":tag,"archive_metadata":meta})
        return
    kind="wheel" if a.action=="build-wheel" else "current"
    context=root/"contexts"/kind
    verify_context(root, context)
    cmd=["docker","buildx","build","--builder",builder(root,a.builder_suffix),"--platform","linux/amd64","--progress","plain","--network","none",*build_args(identity,context)]
    if kind=="wheel":
        output=root/"wheel"
        if any(output.iterdir()):raise RuntimeError("wheel output not empty")
        cmd += ["--target","wheel-export","--output","type=local,dest="+str(output),str(context)]
        run(root,"build-wheel",cmd)
        wheel=output/WHEEL
        if sorted(x.name for x in output.iterdir()) != [WHEEL]:raise RuntimeError("unexpected wheel outputs")
        with zipfile.ZipFile(wheel) as z:
            names=z.namelist()
            if any(n.startswith("/") or ".." in Path(n).parts or not(n.startswith("dimple_gwas/") or n.startswith("dimple_gwas-3.0.0rc1.dist-info/")) for n in names):raise RuntimeError("unexpected wheel contents")
            for entry in identity["files"]:
                if entry["path"].startswith("dimple_gwas/"):
                    if hashlib.sha256(z.read(entry["path"])).hexdigest()!=entry["sha256"]:raise RuntimeError("wheel source mismatch")
        write_json(output/"wheel-manifest.json",{"filename":WHEEL,"sha256":sha(wheel),"source_sha256":identity["source_sha256"],"members":names})
        return
    test=a.action=="build-current-test"
    tag=image_tag(identity,context,test)
    target="freeze3-current-test" if test else "freeze3-current-runtime"
    metadata=root/"builds"/(a.action+"-metadata.json")
    cmd += ["--target",target,"--metadata-file",str(metadata)]
    if a.action=="rebuild-current":
        output=root/"oci/current-independent.oci.tar"
        if output.exists():raise RuntimeError("independent archive exists")
        cmd += ["--no-cache","--provenance=mode=min","--output","type=oci,dest="+str(output)+",rewrite-timestamp=true",str(context)]
    else:
        assert_new_tag(tag)
        cmd += ["--provenance=false","--tag",tag,"--output","type=docker,rewrite-timestamp=true",str(context)]
    run(root,a.action,cmd)
    if a.action=="rebuild-current":
        write_json(root/"oci/current-independent.oci.tar.manifest.json",{"sha256":sha(output),"bytes":output.stat().st_size,"format":"oci-archive","provenance":"inspect archive before asserting"})
    print(tag)

if __name__=="__main__":
    main()
