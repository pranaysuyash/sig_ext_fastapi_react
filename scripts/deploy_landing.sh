#!/bin/bash

# SignKit Landing Page Safe Deployment Script
# This script verifies files before deploying to Cloudflare Pages

set -e

echo "🚀 SignKit Landing Page Deployment"
echo "===================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Step 1: Verify we're on the right branch
echo "${BLUE}Step 1: Checking git branch...${NC}"
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "landing-page" ]; then
    echo "${YELLOW}⚠ Warning: You're on branch '$CURRENT_BRANCH', not 'landing-page'${NC}"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Deployment cancelled."
        exit 1
    fi
else
    echo "${GREEN}✓ On landing-page branch${NC}"
fi
echo ""

# Step 2: Check for uncommitted changes
echo "${BLUE}Step 2: Checking for uncommitted changes...${NC}"
if ! git diff-index --quiet HEAD -- web/live/; then
    echo "${YELLOW}⚠ You have uncommitted changes in web/live/${NC}"
    echo ""
    git status --short web/live/
    echo ""
    read -p "Commit changes before deploying? (Y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        echo ""
        read -p "Enter commit message: " COMMIT_MSG
        git add web/live/
        git commit -m "$COMMIT_MSG"
        echo "${GREEN}✓ Changes committed${NC}"
    fi
else
    echo "${GREEN}✓ No uncommitted changes${NC}"
fi
echo ""

# Step 3: Run verification
echo "${BLUE}Step 3: Running pre-deployment verification...${NC}"
echo ""
if ! "$SCRIPT_DIR/verify_deployment.sh"; then
    echo ""
    echo "${RED}❌ Verification failed!${NC}"
    echo "Fix the errors above before deploying."
    exit 1
fi
echo ""

# Step 4: Show what will be deployed
echo "${BLUE}Step 4: Files to be deployed:${NC}"
cd "$PROJECT_ROOT/web/live"
echo "  Directory: $(pwd)"
echo "  File count: $(find . -type f ! -path '*/\.*' | wc -l) files"
echo ""

# Step 5: Confirm deployment
echo "${YELLOW}⚠ This will deploy to Cloudflare Pages (signkit-landing)${NC}"
echo ""
read -p "Proceed with deployment? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 0
fi
echo ""

# Step 6: Deploy
echo "${BLUE}Step 6: Deploying to Cloudflare Pages...${NC}"
echo ""
wrangler pages deploy . --project-name signkit-landing --branch landing-page

# Step 7: Show deployment info
echo ""
echo "${GREEN}✓ Deployment complete!${NC}"
echo ""
echo "View deployments:"
echo "  wrangler pages deployment list --project-name signkit-landing"
echo ""
echo "Check live site:"
echo "  https://signkit.work"
echo ""
