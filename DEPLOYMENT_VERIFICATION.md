# Deployment Verification - November 26, 2025

## Deployment Details

**Deployment URL:** https://2665c089.signkit-landing.pages.dev  
**Project:** signkit-landing  
**Branch:** landing-page  
**Status:** ✅ Deployed

## Files Deployed

### HTML Pages (5 variants + 1 test page)
- ✅ index.html (A/B router)
- ✅ root.html (neo-brutalist control)
- ✅ buy.html (embedded checkout)
- ✅ purchase.html (SaaS landing)
- ✅ gum.html (direct redirect)
- ✅ new.html (modern dark theme) **NEW**
- ✅ test-variants.html

### Assets
- ✅ assets/files/ (8 icon files)
- ✅ screenshots/ (3 screenshots)

### Dependencies
- ✅ web/claude_landing_page_v2/css/style.css
- ✅ web/claude_landing_page_v2/css/animations.css
- ✅ web/claude_landing_page_v2/js/main.js
- ✅ web/claude_landing_page_v2/js/animations.js
- ✅ web/claude_landing_page_v2/js/analytics.js
- ✅ web/new_landing_page/css/style.css **NEW**
- ✅ web/new_landing_page/js/main.js **NEW**

### Configuration
- ✅ _redirects
- ✅ wrangler.toml

## Verification Checklist

### URLs to Test

1. **Root (A/B Router)**
   - URL: https://2665c089.signkit-landing.pages.dev/
   - Expected: Redirects to one of 5 variants (20% each)
   - Status: ⏳ NEEDS MANUAL TEST

2. **Neo-Brutalist Control**
   - URL: https://2665c089.signkit-landing.pages.dev/root
   - Expected: Shows neo-brutalist design
   - Dependencies: web/claude_landing_page_v2/js/analytics.js
   - Status: ⏳ NEEDS MANUAL TEST

3. **Embedded Checkout**
   - URL: https://2665c089.signkit-landing.pages.dev/buy
   - Expected: Shows full-page Gumroad iframe
   - Dependencies: web/claude_landing_page_v2/js/analytics.js
   - Status: ⏳ NEEDS MANUAL TEST

4. **SaaS Landing**
   - URL: https://2665c089.signkit-landing.pages.dev/purchase
   - Expected: Shows Claude v2 design with animations
   - Dependencies:
     - web/claude_landing_page_v2/css/style.css
     - web/claude_landing_page_v2/css/animations.css
     - web/claude_landing_page_v2/js/main.js
     - web/claude_landing_page_v2/js/animations.js
     - web/claude_landing_page_v2/js/analytics.js
   - Status: ⏳ NEEDS MANUAL TEST

5. **Direct Redirect**
   - URL: https://2665c089.signkit-landing.pages.dev/gum
   - Expected: Immediate redirect to Gumroad
   - Status: ⏳ NEEDS MANUAL TEST

6. **Modern Dark Theme (NEW)**
   - URL: https://2665c089.signkit-landing.pages.dev/new
   - Expected: Shows modern dark theme with gradients
   - Dependencies:
     - web/new_landing_page/css/style.css
     - web/new_landing_page/js/main.js
   - Status: ⏳ NEEDS MANUAL TEST

### Analytics Verification

For each variant, verify in browser console:
```javascript
// Check if gtag is loaded
typeof gtag === 'function'

// Check dataLayer
window.dataLayer

// Should see variant_view event with correct variant parameter
```

### Asset Loading Verification

Check browser Network tab for:
- ✅ All CSS files load (200 status)
- ✅ All JS files load (200 status)
- ✅ All images load (200 status)
- ✅ No 404 errors

## Known Issues

### Issue: Large Build Files Excluded
The following directories were NOT deployed (too large for Cloudflare Pages):
- SignKit-Linux/ (228 MiB)
- SignKit-Windows/
- SignKit-macOS-ARM64/
- SignKit-macOS-Intel/
- build/
- build-artifacts/
- dist/

**Resolution:** These are desktop app build artifacts and should NOT be deployed to the landing page. They are correctly excluded.

## A/B Test Configuration

### Current Setup
- AUTO_SPLIT: `true` in index.html
- Traffic distribution: 20% to each of 5 variants
- Variants: root, buy, purchase, gum, **new**

### Analytics Tracking
- GA4 Property: G-PCJDGBMRRN
- Microsoft Clarity: u8zyh41jr0
- Event: `variant_view` with variant parameter

## Next Steps

1. ✅ Deployment complete
2. ⏳ Manual testing of all 6 URLs
3. ⏳ Verify analytics tracking in GA4
4. ⏳ Check for console errors
5. ⏳ Verify all assets load correctly
6. ⏳ Test A/B routing from root URL
7. ⏳ Confirm custom domain (signkit.work) points to deployment

## Production Deployment

Once verified, this deployment can be promoted to production:
```bash
# In Cloudflare Dashboard:
# 1. Go to Pages > signkit-landing
# 2. Find deployment: 2665c089
# 3. Click "..." > "Promote to production"
```

Or set up custom domain to point to this deployment.

---

**Deployed by:** Automated script  
**Deployment Time:** November 26, 2025  
**Commit:** 694ca70 (landing-page branch)
