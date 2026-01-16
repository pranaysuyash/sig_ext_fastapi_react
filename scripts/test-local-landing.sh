#!/usr/bin/env bash
set -euo pipefail

# Local smoke test for landing pages without Cloudflare "pretty URL" routing.
# Validates that all expected files exist and can be served by a static server.

PORT="${PORT:-8099}"

cleanup() {
  if [[ -n "${SERVER_PID:-}" ]]; then
    kill "${SERVER_PID}" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

python3 -m http.server "${PORT}" >/dev/null 2>&1 &
SERVER_PID="$!"

BASE="http://127.0.0.1:${PORT}"

wait_ready() {
  for _ in $(seq 1 30); do
    if curl -s -o /dev/null "${BASE}/"; then
      return 0
    fi
    sleep 0.1
  done
  return 1
}

wait_ready

check_200() {
  local path="$1"
  local code
  code="$(curl -sS -o /dev/null -L -w "%{http_code}" "${BASE}${path}")"
  if [[ "$code" != "200" ]]; then
    echo "FAIL: ${BASE}${path} expected 200, got $code" >&2
    exit 1
  fi
  echo "OK 200 ${path}"
}

check_200 "/index.html"
check_200 "/root.html"
check_200 "/buy.html"
check_200 "/purchase.html"
check_200 "/gum.html"
check_200 "/test-variants.html"
check_200 "/robots.txt"
check_200 "/sitemap.xml"

echo "Local landing smoke test passed (${BASE})"
