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

test_header_contains() {
    local path=$1
    local name=$2
    local header=$3
    local expected=$4

    echo -n "Checking header $header contains '$expected' on $name ($path)... "
    value=$(curl -sI "$BASE_URL$path" | tr -d '\r' | awk -F': ' -v h="$header" 'tolower($1)==tolower(h){print $2}' | head -n 1)
    if echo "$value" | grep -qi "$expected"; then
        echo "✅ OK"
        return 0
    else
        echo "❌ FAILED ($header: $value)"
        return 1
    fi
}

check_contains() {
    local path=$1
    local name=$2
    local substring=$3

    echo -n "Checking for '$substring' on $name ($path)... "
    html=$(curl -s "$BASE_URL$path")
    if echo "$html" | grep -q "$substring"; then
        echo "✅ Found"
        return 0
    else
        echo "❌ Missing"
        return 1
    fi
}

# Test all variants
test_page "/" "Root/Index"
test_page "/root" "Control Variant (clean URL)"
test_page "/buy" "Buy Variant (clean URL)"
test_page "/purchase" "Purchase Variant (clean URL)"
test_page "/gum" "Gum Variant (clean URL)"
test_page "/test-variants" "Test Dashboard (clean URL)"
test_page "/root.html" "Control Variant"
test_page "/buy.html" "Buy Variant (Iframe)"
test_page "/purchase.html" "Purchase Variant (Claude v2)"
test_page "/gum.html" "Gum Variant (Redirect)"
test_page "/test-variants.html" "Test Dashboard"
test_page "/robots.txt" "robots.txt"
test_page "/sitemap.xml" "sitemap.xml"
test_header_contains "/robots.txt" "robots.txt" "content-type" "text/plain"
test_header_contains "/sitemap.xml" "sitemap.xml" "content-type" "xml"

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
echo "Checking analytics presence on pages:" 
check_contains "/" "Root/Index" "G-PCJDGBMRRN"
check_contains "/" "Root/Index" "web/claude_landing_page_v2/js/analytics.js"
check_contains "/" "Root/Index" "footer-content"
check_contains "/root.html" "Control Variant" "G-PCJDGBMRRN"
check_contains "/root.html" "Control Variant" "web/claude_landing_page_v2/js/analytics.js"
check_contains "/root.html" "Control Variant" "footer-content"
check_contains "/purchase.html" "Purchase Variant (Claude v2)" "G-PCJDGBMRRN"
check_contains "/purchase.html" "Purchase Variant (Claude v2)" "web/claude_landing_page_v2/js/analytics.js"
check_contains "/purchase.html" "Purchase Variant (Claude v2)" "u8zyh41jr0"
check_contains "/purchase.html" "Purchase Variant (Claude v2)" "demo-dot"

echo ""
echo "=========================================="
echo "✨ Testing complete!"
echo ""
echo "Open http://localhost:8080/test-variants.html to manually test all variants"
