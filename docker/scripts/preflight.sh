#!/usr/bin/env bash
set -euo pipefail
docker version
docker buildx version
docker buildx ls
docker info --format "CPUs={{.NCPU}} Memory={{.MemTotal}} Driver={{.Driver}}"
df -h .
