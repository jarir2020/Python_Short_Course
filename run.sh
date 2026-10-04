#!/usr/bin/env bash

# PowerTrack local runner
# ----------------------
# This script starts the three small services in the same order as the real
# request path:
#
#   Django -> FastAPI -> Flask
#
# It is intended for local learning and manual testing, not production use.

set -Eeuo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [[ -n "${PYTHON_BIN:-}" ]]; then
    : "${PYTHON_BIN}"
elif [[ -x "$ROOT_DIR/.venv/bin/python" ]]; then
    PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
else
    PYTHON_BIN="$(command -v python3 || command -v python)"
fi

HOST="${POWERTRACK_HOST:-127.0.0.1}"
DJANGO_PORT="${POWERTRACK_DJANGO_PORT:-8000}"
FASTAPI_PORT="${POWERTRACK_FASTAPI_PORT:-8001}"
FLASK_PORT="${POWERTRACK_FLASK_PORT:-8002}"
MODE="${1:-up}"

RUN_DIR=""
PIDS=()

log() {
    printf '[run] %s\n' "$*"
}

fail() {
    printf '[run] ERROR: %s\n' "$*" >&2
    exit 1
}

require_command() {
    command -v "$1" >/dev/null 2>&1 || fail "Required command not found: $1"
}

cleanup() {
    local exit_code=$?

    # Stop only processes started by this script. We do not kill services that
    # were already running before run.sh was called.
    for pid in "${PIDS[@]}"; do
        kill "$pid" 2>/dev/null || true
    done
    for pid in "${PIDS[@]}"; do
        wait "$pid" 2>/dev/null || true
    done

    if [[ -n "$RUN_DIR" && -d "$RUN_DIR" ]]; then
        if [[ "${KEEP_POWERTRACK_LOGS:-0}" == "1" ]]; then
            log "Service logs kept in $RUN_DIR"
        else
            # RUN_DIR is created by mktemp immediately before this cleanup;
            # remove only its known log files, then remove the empty directory.
            rm -f "$RUN_DIR"/*.log
            rmdir "$RUN_DIR" 2>/dev/null || true
        fi
    fi

    exit "$exit_code"
}

start_process() {
    local name="$1"
    shift

    "$@" >"$RUN_DIR/$name.log" 2>&1 &
    PIDS+=("$!")
    log "$name started (PID ${PIDS[-1]})"
}

http_status() {
    local url="$1"
    curl -sS --max-time 3 -o /dev/null -w '%{http_code}' "$url" 2>/dev/null || true
}

wait_for_http() {
    local name="$1"
    local url="$2"
    local attempts=40
    local code=""

    while (( attempts > 0 )); do
        code="$(http_status "$url")"
        if [[ "$code" =~ ^2[0-9][0-9]$|^3[0-9][0-9]$ ]]; then
            log "$name is ready ($code)"
            return 0
        fi
        sleep 0.25
        ((attempts--))
    done

    log "$name did not become ready. Recent log:"
    tail -n 30 "$RUN_DIR/$name.log" 2>/dev/null || true
    return 1
}

check_endpoint() {
    local name="$1"
    local expected="$2"
    local url="$3"
    local actual

    actual="$(http_status "$url")"
    if [[ "$actual" == "$expected" ]]; then
        log "$name: HTTP $actual"
    else
        log "$name: expected HTTP $expected, received ${actual:-no response}"
        return 1
    fi
}

run_tests() {
    log "Running pytest"
    "$PYTHON_BIN" -m pytest -q

    log "Running Django tests"
    "$PYTHON_BIN" power_outage_project/manage.py test

    log "Compiling project packages"
    "$PYTHON_BIN" -m compileall -q \
        python_core web_backend django_project fastapi_project flask_project \
        capstone_api power_outage_project powertrack_operations \
        powertrack_dashboard tests
}

start_stack() {
    require_command curl
    RUN_DIR="$(mktemp -d "${TMPDIR:-/tmp}/powertrack-run.XXXXXX")"

    log "Applying Django migrations"
    "$PYTHON_BIN" power_outage_project/manage.py migrate --noinput

    if [[ -z "${POWERTRACK_DJANGO_TOKEN:-}" ]]; then
        log "WARNING: POWERTRACK_DJANGO_TOKEN is not set."
        log "FastAPI and Flask will start, but public outage data will return HTTP 503."
    else
        log "Django operations token detected in the environment."
    fi

    start_process django \
        "$PYTHON_BIN" power_outage_project/manage.py runserver \
        "$HOST:$DJANGO_PORT" --noreload
    start_process fastapi \
        "$PYTHON_BIN" -m uvicorn powertrack_operations.main:app \
        --host "$HOST" --port "$FASTAPI_PORT"
    start_process flask \
        "$PYTHON_BIN" -m flask --app powertrack_dashboard.wsgi:app run \
        --host "$HOST" --port "$FLASK_PORT"

    wait_for_http django "http://$HOST:$DJANGO_PORT/admin/login/"
    wait_for_http fastapi "http://$HOST:$FASTAPI_PORT/api/health"
    wait_for_http flask "http://$HOST:$FLASK_PORT/api/health"

    log "Django:  http://$HOST:$DJANGO_PORT/admin/"
    log "FastAPI: http://$HOST:$FASTAPI_PORT/docs"
    log "Flask:   http://$HOST:$FLASK_PORT/"
}

run_smoke_test() {
    start_stack

    check_endpoint "Django admin" "200" "http://$HOST:$DJANGO_PORT/admin/login/"
    check_endpoint "FastAPI health" "200" "http://$HOST:$FASTAPI_PORT/api/health"
    check_endpoint "Flask health" "200" "http://$HOST:$FLASK_PORT/api/health"

    # Without a configured Django token, 503 is the expected safe response.
    # With a token, the same endpoint should return the public outage list.
    local public_status
    public_status="$(http_status "http://$HOST:$FLASK_PORT/api/status")"
    if [[ "$public_status" == "200" || "$public_status" == "503" ]]; then
        log "Flask public status endpoint: HTTP $public_status"
    else
        log "Flask public status endpoint: unexpected HTTP ${public_status:-no response}"
        return 1
    fi

    log "Smoke test passed. Services will now stop."
}

case "$MODE" in
    test)
        run_tests
        ;;
    smoke)
        trap cleanup EXIT INT TERM
        run_smoke_test
        ;;
    up)
        trap cleanup EXIT INT TERM
        start_stack
        log "Press Ctrl+C to stop all three services."
        while :; do
            for pid in "${PIDS[@]}"; do
                if ! kill -0 "$pid" 2>/dev/null; then
                    log "A service stopped unexpectedly. Check logs with KEEP_POWERTRACK_LOGS=1."
                    exit 1
                fi
            done
            sleep 1
        done
        ;;
    help|-h|--help)
        cat <<'USAGE'
Usage: ./run.sh [up|smoke|test]

  up       Start Django, FastAPI, and Flask; keep them running until Ctrl+C.
  smoke    Start all services, check health/status endpoints, then stop.
  test     Run pytest, Django tests, and compileall.

Optional environment variables:
  POWERTRACK_DJANGO_TOKEN       Token used by FastAPI to read Django reports.
  POWERTRACK_DJANGO_PORT        Django port (default: 8000).
  POWERTRACK_FASTAPI_PORT       FastAPI port (default: 8001).
  POWERTRACK_FLASK_PORT         Flask port (default: 8002).
  KEEP_POWERTRACK_LOGS=1        Keep temporary service logs after stopping.
USAGE
        ;;
    *)
        fail "Unknown mode '$MODE'. Use ./run.sh help."
        ;;
esac
