#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOKS_DIR="$ROOT_DIR/.githooks"

if [ ! -d "$HOOKS_DIR" ]; then
  echo "Missing hooks directory: $HOOKS_DIR" >&2
  exit 1
fi

git config --local core.hooksPath .githooks

if [ -x "$HOOKS_DIR/pre-commit" ]; then
  chmod +x "$HOOKS_DIR/pre-commit"
fi

echo "Configured git hooks to use: $(git config --local --get core.hooksPath)"
echo "Hook available at: $HOOKS_DIR/pre-commit"
