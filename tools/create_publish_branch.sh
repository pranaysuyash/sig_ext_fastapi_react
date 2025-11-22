#!/usr/bin/env bash
set -euo pipefail

# Create a temporary branch from origin/main and copy only web/live and root landing pages into it
# Usage:
#   ./tools/create_publish_branch.sh
# This must be run from a branch with the desired web/live changes (e.g., 'landing-page').

ROOT_DIR=$(dirname "$0")/..
cd "$ROOT_DIR"

if [ "$(git rev-parse --abbrev-ref HEAD)" != "landing-page" ]; then
  echo "Warning: Not currently on 'landing-page' branch. Run this script from the branch that contains the landing changes (usually 'landing-page')";
fi

UNIQUE_BRANCH="landing-publish-$(date +%Y%m%d%H%M%S)"

echo "Saving current web/live and root landing files from the current branch to a temp folder"
TMP_DIR=$(mktemp -d -t signkit-landing-XXXX)
echo "Temp dir: $TMP_DIR"
if [ -d "$ROOT_DIR/web/live" ]; then
  rsync -a --delete "$ROOT_DIR/web/live/" "$TMP_DIR/web_live/"
fi
for f in index.html buy.html purchase.html gum.html root.html; do
  if [ -f "$ROOT_DIR/$f" ]; then
    mkdir -p "$TMP_DIR/root_pages"
    cp "$ROOT_DIR/$f" "$TMP_DIR/root_pages/"
  fi
done

echo "Creating branch $UNIQUE_BRANCH from origin/main"
git fetch origin main:refs/remotes/origin/main
git checkout -b "$UNIQUE_BRANCH" origin/main

echo "Restoring web/live and root pages from temp dir into $UNIQUE_BRANCH"
rm -rf web/live || true
mkdir -p web/live
if [ -d "$TMP_DIR/web_live" ]; then
  rsync -a --delete "$TMP_DIR/web_live/" web/live/
fi
if [ -d "$TMP_DIR/root_pages" ]; then
  for f in "$TMP_DIR/root_pages"/*; do
    base=$(basename "$f")
    cp "$f" "$base"
  done
fi

git add -A web/live index.html buy.html purchase.html gum.html root.html || true

if git diff --cached --quiet; then
  echo "No changes to commit in $UNIQUE_BRANCH; inspecting web/live only";
else
  git commit -m "chore: publish web/live (landing) to $UNIQUE_BRANCH"
fi

echo "Pushing branch $UNIQUE_BRANCH to origin"
git push -u origin "$UNIQUE_BRANCH"

echo "Branch created and pushed: $UNIQUE_BRANCH"
echo "You can use the manual GitHub Action with the 'branch' input set to '$UNIQUE_BRANCH' to publish web/live to Cloudflare Pages, or you can run wrangler locally by switching to the branch and running ./tools/deploy_to_pages.sh"

exit 0
