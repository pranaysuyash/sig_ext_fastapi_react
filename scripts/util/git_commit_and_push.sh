#!/usr/bin/env bash
# git_commit_and_push.sh
# Helper script to stage all changes, confirm branch, commit, and push.
# Usage: ./scripts/util/git_commit_and_push.sh "Commit message"
# If no commit message is provided, script will prompt for one.
# This script will ask for confirmation before staging/committing/pushing.

set -euo pipefail

# Determine current branch
branch=$(git rev-parse --abbrev-ref HEAD || echo "(no branch)")

# Show helpful context
echo "Current branch: $branch"

git status --porcelain

echo
read -r -p "Proceed with staging all changes (git add -A), commit and push to '${branch}'? [y/N] " confirm
confirm=${confirm:-N}
if [[ ! $confirm =~ ^[Yy]$ ]]; then
  echo "Aborting. No changes staged."
  exit 0
fi

# Ask for commit message
message="${1:-}"
if [[ -z "$message" ]]; then
  echo
  read -r -p "Commit message: " message
fi

# Final confirmation
echo
echo "About to run 'git add -A' and 'git commit -m \"$message\"' and 'git push origin $branch'"
read -r -p "Are you sure? [y/N] " final_confirm
final_confirm=${final_confirm:-N}
if [[ ! $final_confirm =~ ^[Yy]$ ]]; then
  echo "Aborted by user."
  exit 0
fi

# Stage, commit, push
if git diff --quiet && git diff --staged --quiet; then
  echo "No local changes to commit."
else
  echo "Staging all changes..."
  git add -A
  echo "Committing..."
  git commit -m "$message" || echo "No commit created (maybe no diff)"
fi

# Check if there's an upstream for the branch
upstream=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || true)
if [[ -n "$upstream" ]]; then
  echo "Pushing to upstream: $upstream"
  git push
else
  echo "No upstream for branch $branch configured; pushing to origin/$branch"
  git push origin "$branch"
fi

echo "Done." 
