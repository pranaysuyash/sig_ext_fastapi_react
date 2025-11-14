#!/bin/bash
# Monitor GitHub Actions build progress

echo "Monitoring GitHub Actions build..."
echo ""

# Get the latest run
RUN_ID=$(gh run list --workflow=build-all-platforms.yml --limit 1 --json databaseId --jq '.[0].databaseId')

echo "Run ID: $RUN_ID"
echo "URL: https://github.com/pranaysuyash/sig_ext_fastapi_react/actions/runs/$RUN_ID"
echo ""

# Watch the run
gh run watch $RUN_ID

# Once complete, show summary
echo ""
echo "========================================="
echo "Build Complete! Checking results..."
echo "========================================="
echo ""

# Show job statuses
gh run view $RUN_ID --json jobs --jq '.jobs[] | "\(.name): \(.conclusion)"'

echo ""
echo "========================================="
echo "Download artifacts:"
echo "========================================="
echo "gh run download $RUN_ID"
echo ""
