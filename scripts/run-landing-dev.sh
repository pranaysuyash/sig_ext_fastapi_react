#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-8080}"
echo "Serving landing pages at http://127.0.0.1:${PORT}/"
echo "Tip: open http://127.0.0.1:${PORT}/test-variants.html"
exec python3 -m http.server "${PORT}" --bind 127.0.0.1

