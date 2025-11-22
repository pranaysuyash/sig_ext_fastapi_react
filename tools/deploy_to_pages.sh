#!/usr/bin/env bash
set -euo pipefail

# Deploy `web/live` to Cloudflare Pages using Wrangler
# Usage (local):
#   export CLOUDFLARE_ACCOUNT_ID=your_account_id
#   export CLOUDFLARE_API_TOKEN=your_api_token
#   ./tools/deploy_to_pages.sh

ROOT_DIR=$(dirname "$0")/..
PUBLISH_DIR="$ROOT_DIR/web/live"
# Allow overriding the branch via first arg
BRANCH="${1:-landing-page}"

if ! command -v wrangler >/dev/null 2>&1; then
  echo "Wrangler not found. Please install @cloudflare/wrangler (npm i -g @cloudflare/wrangler)"
  exit 1
fi

if [[ -z "${CLOUDFLARE_ACCOUNT_ID:-}" || -z "${CLOUDFLARE_API_TOKEN:-}" ]]; then
  echo "Please set CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN environment variables."
  exit 1
fi

echo "Publishing $PUBLISH_DIR to Cloudflare Pages (project: signkit-pages-landing, branch: $BRANCH)"
wrangler pages publish "$PUBLISH_DIR" --project-name signkit-pages-landing --branch "$BRANCH"

echo "Publish finished. Check Cloudflare Pages dashboard for status or visit the site (https://signkit-landing.pages.dev)."
