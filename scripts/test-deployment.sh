#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-https://signkit.work}"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

check_200() {
  local path="$1"
  local url="${BASE_URL}${path}"
  local code
  code="$(curl -sS -o /dev/null -L -w "%{http_code}" "$url")"
  if [[ "$code" != "200" ]]; then
    fail "$url expected 200, got $code"
  fi
  echo "OK 200 $url"
}

content_type() {
  local path="$1"
  curl -sS -I -L "${BASE_URL}${path}" | awk -F': ' 'tolower($1)=="content-type"{print tolower($2)}' | tr -d '\r' | head -n 1
}

check_robots() {
  local ct
  ct="$(content_type "/robots.txt")"
  if [[ "$ct" != text/plain* ]]; then
    fail "${BASE_URL}/robots.txt expected text/plain, got ${ct:-<empty>}"
  fi
  echo "OK content-type robots.txt $ct"
}

check_sitemap() {
  local ct
  ct="$(content_type "/sitemap.xml")"
  if [[ "$ct" != *xml* ]]; then
    fail "${BASE_URL}/sitemap.xml expected *xml*, got ${ct:-<empty>}"
  fi
  if ! curl -sS -L "${BASE_URL}/sitemap.xml" | head -n 2 | grep -q '^<?xml'; then
    fail "${BASE_URL}/sitemap.xml does not look like XML"
  fi
  echo "OK sitemap.xml content-type $ct"
}

check_200 "/"
check_200 "/root"
check_200 "/buy"
check_200 "/purchase"
check_200 "/gum"
check_200 "/test-variants"
check_robots
check_sitemap

echo "All checks passed for ${BASE_URL}"
