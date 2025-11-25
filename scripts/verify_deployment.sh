#!/bin/bash

# SignKit Landing Page Deployment Verification Script
# This script verifies that web/live/ contains all necessary files before deployment

set -e

echo "🔍 SignKit Landing Page Deployment Verification"
echo "================================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

# Change to web/live directory
cd "$(dirname "$0")/../web/live" || exit 1

echo "📁 Current directory: $(pwd)"
echo ""

# Check critical HTML files
echo "✓ Checking HTML files..."
REQUIRED_HTML=("index.html" "root.html" "purchase.html" "buy.html" "gum.html")
for file in "${REQUIRED_HTML[@]}"; do
    if [ -f "$file" ]; then
        echo "  ${GREEN}✓${NC} $file exists"
    else
        echo "  ${RED}✗${NC} $file MISSING"
        ((ERRORS++))
    fi
done
echo ""

# Check CSS files
echo "✓ Checking CSS files..."
if [ -d "css" ]; then
    echo "  ${GREEN}✓${NC} css/ directory exists"
    if [ -f "css/style.css" ]; then
        echo "  ${GREEN}✓${NC} css/style.css exists"
    else
        echo "  ${RED}✗${NC} css/style.css MISSING"
        ((ERRORS++))
    fi
else
    echo "  ${RED}✗${NC} css/ directory MISSING"
    ((ERRORS++))
fi
echo ""

# Check JS files
echo "✓ Checking JavaScript files..."
if [ -d "js" ]; then
    echo "  ${GREEN}✓${NC} js/ directory exists"
    REQUIRED_JS=("main.js" "analytics.js")
    for file in "${REQUIRED_JS[@]}"; do
        if [ -f "js/$file" ]; then
            echo "  ${GREEN}✓${NC} js/$file exists"
        else
            echo "  ${RED}✗${NC} js/$file MISSING"
            ((ERRORS++))
        fi
    done
else
    echo "  ${RED}✗${NC} js/ directory MISSING"
    ((ERRORS++))
fi
echo ""

# Check nested claude_landing_page_v2 structure
echo "✓ Checking nested assets (for purchase.html)..."
if [ -d "web/claude_landing_page_v2" ]; then
    echo "  ${GREEN}✓${NC} web/claude_landing_page_v2/ exists"
    
    if [ -f "web/claude_landing_page_v2/css/style.css" ]; then
        echo "  ${GREEN}✓${NC} web/claude_landing_page_v2/css/style.css exists"
    else
        echo "  ${RED}✗${NC} web/claude_landing_page_v2/css/style.css MISSING"
        ((ERRORS++))
    fi
    
    if [ -f "web/claude_landing_page_v2/js/main.js" ]; then
        echo "  ${GREEN}✓${NC} web/claude_landing_page_v2/js/main.js exists"
    else
        echo "  ${RED}✗${NC} web/claude_landing_page_v2/js/main.js MISSING"
        ((ERRORS++))
    fi
else
    echo "  ${RED}✗${NC} web/claude_landing_page_v2/ directory MISSING"
    echo "  ${YELLOW}⚠${NC}  purchase.html will not load correctly!"
    ((ERRORS++))
fi
echo ""

# Check assets
echo "✓ Checking assets..."
if [ -d "assets/files" ]; then
    echo "  ${GREEN}✓${NC} assets/files/ directory exists"
    ICON_COUNT=$(find assets/files -name "signkit_icon_*.png" 2>/dev/null | wc -l)
    if [ "$ICON_COUNT" -ge 4 ]; then
        echo "  ${GREEN}✓${NC} Found $ICON_COUNT icon files"
    else
        echo "  ${YELLOW}⚠${NC}  Only found $ICON_COUNT icon files (expected 4+)"
        ((WARNINGS++))
    fi
else
    echo "  ${YELLOW}⚠${NC}  assets/files/ directory missing"
    ((WARNINGS++))
fi
echo ""

# Check screenshots
echo "✓ Checking screenshots..."
if [ -d "screenshots" ]; then
    SCREENSHOT_COUNT=$(find screenshots -name "screenshot-*.png" 2>/dev/null | wc -l)
    if [ "$SCREENSHOT_COUNT" -ge 3 ]; then
        echo "  ${GREEN}✓${NC} Found $SCREENSHOT_COUNT screenshot files"
    else
        echo "  ${YELLOW}⚠${NC}  Only found $SCREENSHOT_COUNT screenshots (expected 3+)"
        ((WARNINGS++))
    fi
else
    echo "  ${YELLOW}⚠${NC}  screenshots/ directory missing"
    ((WARNINGS++))
fi
echo ""

# Check SEO files
echo "✓ Checking SEO files..."
if [ -f "robots.txt" ]; then
    echo "  ${GREEN}✓${NC} robots.txt exists"
else
    echo "  ${YELLOW}⚠${NC}  robots.txt missing"
    ((WARNINGS++))
fi

if [ -f "sitemap.xml" ]; then
    echo "  ${GREEN}✓${NC} sitemap.xml exists"
else
    echo "  ${YELLOW}⚠${NC}  sitemap.xml missing"
    ((WARNINGS++))
fi
echo ""

# Check wrangler config
echo "✓ Checking deployment config..."
if [ -f "wrangler.toml" ]; then
    echo "  ${GREEN}✓${NC} wrangler.toml exists"
else
    echo "  ${RED}✗${NC} wrangler.toml MISSING"
    ((ERRORS++))
fi
echo ""

# Verify file contents
echo "✓ Verifying file contents..."

# Check if root.html has neo-brutalism footer (inline styles)
if grep -q "border: 3px solid #111827" root.html 2>/dev/null; then
    echo "  ${GREEN}✓${NC} root.html has neo-brutalism footer (inline styles)"
else
    echo "  ${YELLOW}⚠${NC}  root.html may not have correct footer styling"
    ((WARNINGS++))
fi

# Check if purchase.html references correct CSS path
if grep -q "web/claude_landing_page_v2/css/style.css" purchase.html 2>/dev/null; then
    echo "  ${GREEN}✓${NC} purchase.html references correct CSS path"
else
    echo "  ${RED}✗${NC} purchase.html has incorrect CSS path"
    ((ERRORS++))
fi

# Check carousel timing in main.js
if grep -q "setInterval(nextStep, 5000)" web/claude_landing_page_v2/js/main.js 2>/dev/null; then
    echo "  ${GREEN}✓${NC} Carousel timing set to 5 seconds"
elif grep -q "setInterval(nextStep, 3000)" web/claude_landing_page_v2/js/main.js 2>/dev/null; then
    echo "  ${YELLOW}⚠${NC}  Carousel timing is 3 seconds (might be too fast)"
    ((WARNINGS++))
fi

echo ""
echo "================================================"
echo "📊 Verification Summary"
echo "================================================"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "${GREEN}✓ All checks passed!${NC}"
    echo ""
    echo "Ready to deploy with:"
    echo "  cd web/live"
    echo "  wrangler pages deploy . --project-name signkit-landing --branch landing-page"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo "${YELLOW}⚠ $WARNINGS warning(s) found${NC}"
    echo ""
    echo "You can proceed with deployment, but review warnings above."
    echo ""
    echo "Deploy with:"
    echo "  cd web/live"
    echo "  wrangler pages deploy . --project-name signkit-landing --branch landing-page"
    exit 0
else
    echo "${RED}✗ $ERRORS error(s) found${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo "${YELLOW}⚠ $WARNINGS warning(s) found${NC}"
    fi
    echo ""
    echo "❌ DO NOT DEPLOY until errors are fixed!"
    echo ""
    echo "Review the errors above and fix them before deploying."
    exit 1
fi
