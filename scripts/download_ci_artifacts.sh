#!/bin/bash
set -euo pipefail

# Download CI artifacts from GitHub Actions
RUN_ID="${1:-19420175173}"
REPO="pranaysuyash/sig_ext_fastapi_react"
TODAY=$(date +%Y-%m-%d)
OUTDIR="$HOME/Downloads/SignKit-CI-$TODAY"

echo "🔍 Checking build status for run $RUN_ID..."

# Wait for build to complete (max 30 minutes)
MAX_WAIT=1800
ELAPSED=0
INTERVAL=30

while [ $ELAPSED -lt $MAX_WAIT ]; do
  STATUS=$(curl -s -H "Accept: application/vnd.github+json" \
    "https://api.github.com/repos/$REPO/actions/runs/$RUN_ID" | \
    jq -r '.status')
  
  CONCLUSION=$(curl -s -H "Accept: application/vnd.github+json" \
    "https://api.github.com/repos/$REPO/actions/runs/$RUN_ID" | \
    jq -r '.conclusion // "running"')
  
  echo "[$(date +%H:%M:%S)] Status: $STATUS | Conclusion: $CONCLUSION"
  
  if [ "$STATUS" = "completed" ]; then
    echo ""
    if [ "$CONCLUSION" = "success" ]; then
      echo "✅ Build completed successfully!"
      break
    else
      echo "❌ Build failed with conclusion: $CONCLUSION"
      echo "Check: https://github.com/$REPO/actions/runs/$RUN_ID"
      exit 1
    fi
  fi
  
  sleep $INTERVAL
  ELAPSED=$((ELAPSED + INTERVAL))
  
  if [ $ELAPSED -ge $MAX_WAIT ]; then
    echo "⏱️  Timeout waiting for build to complete"
    echo "Check manually: https://github.com/$REPO/actions/runs/$RUN_ID"
    exit 1
  fi
done

echo ""
echo "📦 Downloading artifacts..."
mkdir -p "$OUTDIR"

# Download all artifacts using GitHub CLI
cd "$OUTDIR"

echo "Using gh CLI to download artifacts..."
gh run download $RUN_ID -R $REPO

echo ""
echo "📁 Downloaded to: $OUTDIR"
ls -lh "$OUTDIR"

# List all downloaded files recursively
echo ""
echo "📋 All downloaded files:"
find "$OUTDIR" -type f -exec ls -lh {} \; | awk '{printf "%-10s %s\n", $5, $NF}'

echo ""
echo "✅ Done! Artifacts downloaded to:"
echo "   $OUTDIR"
echo ""
echo "Files ready for distribution:"
find "$OUTDIR" -type f \( -name "*.dmg" -o -name "*.zip" -o -name "*.tar.gz" \) -exec ls -lh {} \;
