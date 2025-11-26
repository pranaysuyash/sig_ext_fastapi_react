#!/bin/bash
# Clean Cloudflare Pages Deployment Script
# Deploys only necessary files, excluding build artifacts

set -e

echo "🚀 SignKit Landing Page - Cloudflare Deployment"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if we're in the right directory
if [ ! -f "index.html" ] || [ ! -f "wrangler.toml" ]; then
    echo -e "${RED}Error: Must run from repository root${NC}"
    exit 1
fi

# Create temp deployment directory
DEPLOY_DIR=$(mktemp -d)
echo -e "${GREEN}Created temp directory: $DEPLOY_DIR${NC}"
echo ""

# Copy HTML files
echo "📄 Copying HTML files..."
for file in index.html root.html buy.html purchase.html gum.html new.html test-variants.html; do
    if [ -f "$file" ]; then
        cp "$file" "$DEPLOY_DIR/"
        echo "  ✓ $file"
    else
        echo -e "  ${YELLOW}⚠ $file not found${NC}"
    fi
done
echo ""

# Copy configuration files
echo "⚙️  Copying configuration..."
for file in _redirects wrangler.toml; do
    if [ -f "$file" ]; then
        cp "$file" "$DEPLOY_DIR/"
        echo "  ✓ $file"
    fi
done
echo ""

# Copy assets
echo "🖼️  Copying assets..."
if [ -d "assets" ]; then
    cp -r assets "$DEPLOY_DIR/"
    echo "  ✓ assets/"
fi

if [ -d "screenshots" ]; then
    cp -r screenshots "$DEPLOY_DIR/"
    echo "  ✓ screenshots/"
fi
echo ""

# Copy web dependencies
echo "📦 Copying web dependencies..."
mkdir -p "$DEPLOY_DIR/web"

if [ -d "web/claude_landing_page_v2" ]; then
    cp -r web/claude_landing_page_v2 "$DEPLOY_DIR/web/"
    echo "  ✓ web/claude_landing_page_v2/"
fi

if [ -d "web/new_landing_page" ]; then
    cp -r web/new_landing_page "$DEPLOY_DIR/web/"
    echo "  ✓ web/new_landing_page/"
fi
echo ""

# Show what will be deployed
echo "📊 Deployment Summary:"
echo "  HTML files: $(find "$DEPLOY_DIR" -maxdepth 1 -name "*.html" | wc -l | tr -d ' ')"
echo "  Total files: $(find "$DEPLOY_DIR" -type f | wc -l | tr -d ' ')"
echo "  Total size: $(du -sh "$DEPLOY_DIR" | cut -f1)"
echo ""

# Confirm deployment
echo -e "${YELLOW}Ready to deploy to Cloudflare Pages${NC}"
read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled"
    rm -rf "$DEPLOY_DIR"
    exit 0
fi
echo ""

# Deploy
echo "🌐 Deploying to Cloudflare..."
wrangler pages deploy "$DEPLOY_DIR" \
    --project-name=signkit-landing \
    --branch=landing-page \
    --commit-dirty=true

# Cleanup
echo ""
echo "🧹 Cleaning up..."
rm -rf "$DEPLOY_DIR"

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Test deployment URL"
echo "  2. Verify all variants load correctly"
echo "  3. Check analytics tracking"
echo "  4. Promote to production if successful"
echo ""
