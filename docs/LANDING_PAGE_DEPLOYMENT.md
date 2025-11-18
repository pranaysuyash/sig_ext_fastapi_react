# Landing Page Deployment Guide

## Overview
The SignKit landing page is deployed on Cloudflare Pages at **signkit.work** from the `landing-page` branch.

## Branch Strategy

### `landing-page` Branch
- **Purpose**: Production landing page and A/B test variants
- **Domain**: https://signkit.work
- **Cloudflare Project**: signkit-landing
- **Contents**: HTML pages, assets, screenshots for marketing site
- **When to update**: Only for landing page copy, design, or A/B test changes

### `main` Branch  
- **Purpose**: Desktop application development
- **Contents**: Python app, backend, tests, build tools
- **When to update**: All feature development, bug fixes, new functionality

**The branches are independent** - you can develop new features in `main` without affecting the live landing page.

## A/B Testing Setup

### Current Configuration
Four checkout flow variants are being tested:
- **`/root`** - Control variant (neo-brutal design)
- **`/buy`** - Embedded gum.new checkout
- **`/gum`** - Direct Gumroad redirect
- **`/purchase`** - Claude v2 landing page

### How It Works
1. **Manual Testing (Current)**
   - Each variant has its own URL
   - Send different traffic sources to different URLs
   - Track conversions in Google Analytics by variant

2. **Automatic A/B Testing (Future)**
   - Set `AUTO_SPLIT = true` in `index.html`
   - Visitors to `/` are randomly assigned a variant
   - Assignment stored in localStorage
   - Subsequent visits use same variant

### Enabling Auto A/B Testing
When ready to enable automatic variant assignment:

1. Checkout `landing-page` branch
2. Edit `index.html`:
   ```javascript
   const AUTO_SPLIT = true; // Change from false
   ```
3. Commit and push
4. Cloudflare Pages will auto-deploy

## Deployment Process

### Automatic Deployment (Recommended)
Cloudflare Pages automatically deploys when you push to `landing-page`:

```bash
git checkout landing-page
# Make your changes
git add -A
git commit -m "Update landing page copy"
git push origin landing-page
```

Cloudflare detects the push and deploys automatically (usually 1-2 minutes).

### Manual Deployment via Wrangler
If automatic deployment isn't working:

```bash
# Create temp directory with only landing page files
mkdir -p /tmp/signkit-deploy
cp -r index.html root.html buy.html purchase.html gum.html test-variants.html assets screenshots web /tmp/signkit-deploy/

# Deploy
wrangler pages deploy /tmp/signkit-deploy --project-name=signkit-landing --branch=landing-page
```

## Important: No _redirects File Needed

**Do NOT create a `_redirects` file!**

Cloudflare Pages automatically handles extensionless URLs:
- `/root` → serves `root.html` (HTTP 200)
- `/buy` → serves `buy.html` (HTTP 200)  
- `/gum` → serves `gum.html` (HTTP 200)
- `/purchase` → serves `purchase.html` (HTTP 200)

Adding a `_redirects` file causes 308 redirect loops. See `CLOUDFLARE_REDIRECTS_ISSUE.md` in the `landing-page` branch for details.

## File Structure

```
landing-page branch:
├── index.html              # Main landing page
├── root.html               # Control variant
├── buy.html                # Gum.new embedded variant
├── gum.html                # Gumroad redirect variant
├── purchase.html           # Claude v2 variant
├── test-variants.html      # Testing page
├── assets/                 # Icons, logos
├── screenshots/            # Product screenshots
├── web/                    # Additional landing page assets
├── wrangler.toml           # Cloudflare Pages config
└── .pages-include          # Files to include in deployment
```

## Testing Deployment

After deployment, test all routes:

```bash
curl -I https://signkit.work/root
curl -I https://signkit.work/buy
curl -I https://signkit.work/gum
curl -I https://signkit.work/purchase
```

All should return `HTTP/2 200`.

## Google Analytics Tracking

### Event Tracking
Each variant tracks impressions:
- Event: `ab_test_impression`
- Experiment ID: `checkout_flow_test`
- Variants: `control`, `root`, `buy`, `gum`, `purchase`

View results in Google Analytics:
- Property ID: G-PCJDGBMRRN
- Events → ab_test_impression
- Filter by variant dimension

### Analytics Fix (Nov 18, 2025)
**Issue**: The `/gum` variant was redirecting immediately before GA4 could fire tracking events.

**Solution**: Updated `gum.html` to use GA4's `event_callback` feature:
- Tracks the `ab_test_impression` event
- Waits for callback confirmation (~100-500ms)
- Then redirects to Gumroad
- Includes fallback timeout to ensure redirect happens

**Testing**: Use `test-analytics.html` (in landing-page branch) to verify all variants track correctly:
```bash
# Start local server
python3 -m http.server 8001

# Open test suite
open http://localhost:8001/test-analytics.html
```

**Verification**: 
- Open DevTools Network tab
- Filter by "collect"
- Each variant should send `collect?v=2&...&en=ab_test_impression`
- One request may show "(canceled)" - this is normal, the 204 response is what matters

See `ANALYTICS_FIX_SUMMARY.md` (in landing-page branch) for complete details.

## Troubleshooting

### 308 Redirect Loops
**Cause**: A `_redirects` file exists  
**Solution**: Delete the `_redirects` file

### Changes Not Appearing
**Cause**: Browser cache or Cloudflare cache  
**Solution**: 
- Hard refresh (Cmd+Shift+R on Mac)
- Check preview URL from Cloudflare dashboard
- Wait 2-3 minutes for cache to clear

### Deployment Not Triggering
**Cause**: GitHub webhook not configured  
**Solution**: 
- Check Cloudflare Pages dashboard → Settings → Builds
- Ensure "Automatic deployments" is enabled
- Or use manual deployment via Wrangler

## When to Update Each Branch

### Update `landing-page` when:
- Changing landing page copy or messaging
- Updating pricing information
- Adding/removing A/B test variants
- Changing screenshots or assets
- Enabling/disabling AUTO_SPLIT

### Update `main` when:
- Adding new desktop app features
- Fixing bugs in the application
- Updating dependencies
- Changing build process
- Adding tests

## Related Documentation
- `CLOUDFLARE_REDIRECTS_ISSUE.md` (in landing-page branch) - Details on the 308 redirect issue
- `AB_TEST_STRUCTURE.md` (in landing-page branch) - A/B testing implementation details
- `DEPLOYMENT_CHECKLIST.md` (in landing-page branch) - Pre-deployment checklist
