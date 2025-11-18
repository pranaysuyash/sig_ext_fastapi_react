#!/bin/bash

# Test script to verify all landing page variants are working

echo "🧪 Testing SignKit Landing Page Variants"
echo "=========================================="
echo ""

BASE_URL="http://localhost:8080"

# Function to test a page
test_page() {
    local path=$1
    local name=$2
    
    echo -n "Testing $name ($path)... "
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL$path")
    
    if [ "$response" = "200" ]; then
        echo "✅ OK"
        return 0
    else
        echo "❌ FAILED (HTTP $response)"
        return 1
    fi
}

# Test all variants
test_page "/" "Root/Index"
test_page "/root.html" "Control Variant"
test_page "/buy.html" "Buy Variant (Iframe)"
test_page "/purchase.html" "Purchase Variant (Claude v2)"
test_page "/gum.html" "Gum Variant (Redirect)"
test_page "/test-variants.html" "Test Dashboard"

echo ""
echo "Testing Assets:"
test_page "/assets/files/signkit_icon_32x32.png" "Favicon 32x32"
test_page "/assets/files/signkit_icon_64x64.png" "Logo 64x64"
test_page "/screenshots/screenshot-1.png" "Screenshot 1"
test_page "/screenshots/screenshot-2.png" "Screenshot 2"
test_page "/screenshots/screenshot-3.png" "Screenshot 3"

echo ""
echo "Testing CSS/JS for purchase.html:"
test_page "/web/claude_landing_page_v2/css/style.css" "Style CSS"
test_page "/web/claude_landing_page_v2/css/animations.css" "Animations CSS"
test_page "/web/claude_landing_page_v2/js/main.js" "Main JS"
test_page "/web/claude_landing_page_v2/js/animations.js" "Animations JS"

echo ""
echo "=========================================="
echo "✨ Testing complete!"
echo ""
echo "Open http://localhost:8080/test-variants.html to manually test all variants"
