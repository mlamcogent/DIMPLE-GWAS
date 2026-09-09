#!/usr/bin/env bash
# One fresh, hardened container; no registry write or scientific source edits.
set -euo pipefail
if [[ $# -lt 4 ]]; then
  echo 'Usage: run_smoke_tests.sh IMAGE ABS_INPUT ABS_EMPTY_OUTPUT MODE [HARNESS_ARGS...]' >&2
  exit 64
fi
image_ref=$1
input_root=$2
output_root=$3
validation_mode=$4
shift 4
case "$input_root:$output_root" in /*:/*) ;; *) echo 'Input and output paths must be absolute.' >&2; exit 64;; esac
[[ "$output_root" != / && "$input_root" != "$output_root" && -d "$input_root" && ! -L "$input_root" && ! -L "$output_root" ]] || exit 64
[[ -f "$input_root/harness.py" && -f "$input_root/preregistered_acceptance_criteria.json" ]] || {
  echo 'Shared input requires harness.py and the sealed acceptance JSON.' >&2; exit 66;
}
if [[ -e "$output_root" ]]; then
  [[ -d "$output_root" && -z "$(find "$output_root" -mindepth 1 -maxdepth 1 -print -quit)" ]] || {
    echo 'Refusing a nonempty output directory.' >&2; exit 73;
  }
else
  mkdir -p -- "$output_root"
fi

if [[ ${DIMPLE_VOLUME_TRANSPORT:-0} == 1 ]]; then
  # Docker Desktop may stall when starting bind-mounted containers. Transfer
  # through stopped helper containers so no host path reaches the scientific
  # container. Every invocation has its own volumes, never a reused cache.
  transport_token=$(python3 -c 'import uuid; print(uuid.uuid4().hex[:16])')
  transport_prefix="dimple-validation-$transport_token"
  input_volume="$transport_prefix-input"
  output_volume="$transport_prefix-output"
  helper_container="$transport_prefix-transfer"
  science_container="$transport_prefix-science"
  diagnostic_dir="$output_root/volume_transport"
  mkdir -- "$diagnostic_dir"
  transport_started=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  science_exit=UNAVAILABLE
  retrieved=0
  cleanup_complete=0
  ownership_initialized=0
  helper_created=0
  science_created=0
  printf 'utc\tevent\n' > "$diagnostic_dir/events.tsv"
  transport_event() {
    printf '%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$1" >> "$diagnostic_dir/events.tsv"
  }
  transport_finish() {
    local wrapper_exit=$?
    trap - EXIT INT TERM
    set +e
    if [[ $science_created == 1 ]]; then
      docker inspect "$science_container" > "$diagnostic_dir/science_container.inspect.json" \
        2> "$diagnostic_dir/science_container.inspect.stderr.log"
      docker logs "$science_container" > "$diagnostic_dir/container.stdout.log" \
        2> "$diagnostic_dir/container.stderr.log"
    fi
    if [[ $helper_created == 1 ]]; then
      docker inspect "$helper_container" > "$diagnostic_dir/transfer_container.inspect.json" \
        2> "$diagnostic_dir/transfer_container.inspect.stderr.log"
    fi
    docker volume inspect "$input_volume" "$output_volume" > "$diagnostic_dir/volumes.inspect.json" \
      2> "$diagnostic_dir/volumes.inspect.stderr.log"
    # Preserve by default, including failed scientific runs. Explicit cleanup
    # is accepted only after the stopped output volume has been exported.
    if [[ $retrieved == 1 && ${DIMPLE_CLEAN_TRANSPORT_AFTER_EXPORT:-0} == 1 ]]; then
      if docker rm "$science_container" "$helper_container" >> "$diagnostic_dir/cleanup.log" 2>&1 \
        && docker volume rm "$input_volume" "$output_volume" >> "$diagnostic_dir/cleanup.log" 2>&1; then
        cleanup_complete=1
      fi
    fi
    python3 - "$diagnostic_dir/transport_manifest.json" "$transport_started" "$image_ref" \
      "$input_root" "$output_root" "$input_volume" "$output_volume" "$helper_container" \
      "$science_container" "$validation_mode" "$science_exit" "$wrapper_exit" "$retrieved" \
      "$ownership_initialized" "$cleanup_complete" <<'PY'
import datetime,json,pathlib,sys
keys=['manifest','started_utc','image_ref','host_input','host_output','input_volume','output_volume',
      'transfer_container','science_container','harness_mode','container_exit_code','wrapper_exit_code',
      'output_retrieved','root_ownership_initialization_used','cleanup_complete']
record=dict(zip(keys,sys.argv[1:]))
destination=pathlib.Path(record.pop('manifest'))
for key in ('container_exit_code','wrapper_exit_code'):
    if record[key].isdigit(): record[key]=int(record[key])
for key in ('output_retrieved','root_ownership_initialization_used','cleanup_complete'):
    record[key]=record[key]=='1'
record.update(transport='docker_named_volumes_via_stopped_helper_and_docker_cp',
              finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
              scientific_uid=10001,scientific_gid=10001,
              host_bind_mounts=False,network='none',root_filesystem='read_only',
              input_mount='read_only',output_mount='writable',capabilities='ALL dropped',
              no_new_privileges=True,tmpfs='rw,nosuid,nodev,noexec',
              preservation='Volumes and containers retained unless successful retrieval and explicit cleanup requested')
with destination.open('x') as stream: json.dump(record,stream,indent=2);stream.write('\n')
PY
    exit "$wrapper_exit"
  }
  trap transport_finish EXIT
  trap 'exit 130' INT
  trap 'exit 143' TERM
  docker volume create --label dimple.validation.transport=true --label "dimple.validation.task=$transport_token" \
    "$input_volume" > "$diagnostic_dir/input_volume.id"
  docker volume create --label dimple.validation.transport=true --label "dimple.validation.task=$transport_token" \
    "$output_volume" > "$diagnostic_dir/output_volume.id"
  transport_event volumes_created
  docker create --name "$helper_container" --platform linux/amd64 --network none --read-only \
    --user 10001:10001 --cap-drop ALL --security-opt no-new-privileges:true \
    --mount "type=volume,src=$input_volume,dst=/data/input" \
    --mount "type=volume,src=$output_volume,dst=/data/output" \
    --entrypoint /bin/true "$image_ref" > "$diagnostic_dir/transfer_container.id"
  helper_created=1
  docker cp "$input_root/." "$helper_container:/data/input" \
    > "$diagnostic_dir/input_copy.stdout.log" 2> "$diagnostic_dir/input_copy.stderr.log"
  transport_event input_copied
  # New named volumes normally inherit the image directory owner (10001).
  # Probe it without root. Only if necessary, chown this empty output root.
  if ! docker run --rm --platform linux/amd64 --network none --read-only --user 10001:10001 \
    --cap-drop ALL --security-opt no-new-privileges:true \
    --mount "type=volume,src=$output_volume,dst=/data/output" \
    --entrypoint /bin/sh "$image_ref" -c 'test -w /data/output' \
    > "$diagnostic_dir/output_ownership_probe.stdout.log" 2> "$diagnostic_dir/output_ownership_probe.stderr.log"; then
    docker run --rm --platform linux/amd64 --network none --read-only --user 0:0 \
      --cap-drop ALL --cap-add CHOWN --security-opt no-new-privileges:true \
      --mount "type=volume,src=$output_volume,dst=/data/output" \
      --entrypoint /bin/chown "$image_ref" 10001:10001 /data/output \
      > "$diagnostic_dir/output_ownership_init.stdout.log" 2> "$diagnostic_dir/output_ownership_init.stderr.log"
    ownership_initialized=1
    transport_event empty_output_volume_owner_initialized
  fi
  science_command=(docker create --name "$science_container" --platform linux/amd64 --network none --read-only
    --cap-drop ALL --security-opt no-new-privileges:true
    --pids-limit 256 --cpus "${DIMPLE_VALIDATION_CPUS:-2}" --memory "${DIMPLE_VALIDATION_MEMORY:-6g}"
    --user 10001:10001
    --mount "type=volume,src=$input_volume,dst=/data/input,readonly"
    --mount "type=volume,src=$output_volume,dst=/data/output"
    --tmpfs /tmp:rw,nosuid,nodev,noexec,size=2147483648,mode=1777
    --workdir /tmp --env HOME=/tmp --env MPLCONFIGDIR=/tmp/matplotlib
    --env NUMBA_CACHE_DIR=/tmp/numba --env PYTHONDONTWRITEBYTECODE=1
    --env OMP_NUM_THREADS=1 --env OPENBLAS_NUM_THREADS=1 --env MKL_NUM_THREADS=1
    --env NUMBA_NUM_THREADS=1 --env VECLIB_MAXIMUM_THREADS=1 --env NUMEXPR_NUM_THREADS=1
    --env PYTHONHASHSEED=0 --entrypoint python "$image_ref"
    /data/input/harness.py "$validation_mode" --input /data/input --output /data/output "$@")
  printf '%q ' "${science_command[@]}" > "$diagnostic_dir/science_create.command.sh"
  printf '\n' >> "$diagnostic_dir/science_create.command.sh"
  "${science_command[@]}" > "$diagnostic_dir/science_container.id"
  science_created=1
  docker start "$science_container" > "$diagnostic_dir/science_start.stdout.log" \
    2> "$diagnostic_dir/science_start.stderr.log"
  transport_event science_started
  docker wait "$science_container" > "$diagnostic_dir/container_exit_code.txt" \
    2> "$diagnostic_dir/science_wait.stderr.log"
  science_exit=$(tr -d '\r\n' < "$diagnostic_dir/container_exit_code.txt")
  [[ "$science_exit" =~ ^[0-9]+$ ]] || { echo 'Docker wait returned no usable exit code.' >&2; exit 125; }
  transport_event "science_finished_exit_$science_exit"
  docker cp "$helper_container:/data/output/." "$output_root" \
    > "$diagnostic_dir/output_copy.stdout.log" 2> "$diagnostic_dir/output_copy.stderr.log"
  retrieved=1
  transport_event output_retrieved
  docker logs "$science_container"
  exit "$science_exit"
fi

docker run --rm --platform linux/amd64 --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges:true \
  --pids-limit 256 --cpus "${DIMPLE_VALIDATION_CPUS:-2}" --memory "${DIMPLE_VALIDATION_MEMORY:-6g}" \
  --user "$(id -u):$(id -g)" \
  --mount "type=bind,src=$input_root,dst=/data/input,readonly" \
  --mount "type=bind,src=$output_root,dst=/data/output" \
  --tmpfs /tmp:rw,nosuid,nodev,noexec,size=2147483648,mode=1777 \
  --workdir /tmp --env HOME=/tmp --env MPLCONFIGDIR=/tmp/matplotlib \
  --env NUMBA_CACHE_DIR=/tmp/numba --env PYTHONDONTWRITEBYTECODE=1 \
  --env OMP_NUM_THREADS=1 --env OPENBLAS_NUM_THREADS=1 --env MKL_NUM_THREADS=1 \
  --env NUMBA_NUM_THREADS=1 --env VECLIB_MAXIMUM_THREADS=1 --env NUMEXPR_NUM_THREADS=1 \
  --env PYTHONHASHSEED=0 --entrypoint python "$image_ref" \
  /data/input/harness.py "$validation_mode" --input /data/input --output /data/output "$@"
