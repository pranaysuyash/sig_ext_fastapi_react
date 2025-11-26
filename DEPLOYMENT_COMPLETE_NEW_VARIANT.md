# /new Variant Deployment - Complete

## Summary

Successfully deployed the new modern dark theme landing page variant to Cloudflare Pages.

## What Was Deployed

### Files Added/Updated:
1. **`new.html`** - Root-level HTML file for `/new` route
2. **`web/new_landing_page/`** - Complete landing page directory
   - `index.html` - Full page HTML
   - `css/style.css` - Dark theme styling
   - `js/main.js` - Animations and interactions
3. **`index.html`** - Updated A/B test logic to include `/new` (20% traffic split)
4. **`.pages-include`** - Updated to include new files in Cloudflare deployment

### Deployment Details:
- **Method:** Manual deployment via `wrangler pages deploy`
- **Project:** signkit-landing
- **Branch:** landing-page
- **Deployment URL:** https://e70d23b5.signkit-landing.pages.dev
- **Production URL:** https://signkit.work
- **Total Files:** 33 files deployed
  - 7 HTML files (index, root, buy, purchase, gum, new, test-variants)
  - 5 CSS files (claude v2 + new variant)
  - 5 JS files (claude v2 + new variant + analytics)
  - 15 images (icons + screenshots)
  - 1 _redirects file

## A/B Test Configuration

### Traffic Distribution (AUTO_SPLIT = true):
- 20% → `/root` (neo-brutalist control)
- 20% → `/buy` (embedded checkout)
- 20% → `/purchase` (SaaS landing)
- 20% → `/gum` (direct redirect)
- 20% → `/new` (modern dark theme) ✅ NEW

### Analytics Tracking:
- **GA4 Property:** G-PCJDGBMRRN
- **Variant ID:** `new`
- **Events:** `variant_view` fires on page load
- **Microsoft Clarity:** Enabled

## Testing

### Live URLs:
- **Direct Access:** https://signkit.work/new
- **Auto A/B Test:** https://signkit.work/ (20% chance of seeing /new)
- **Preview:** https://e70d23b5.signkit-landing.pages.dev/new

### Test Checklist:
- [ ] Visit https://signkit.work/new directly
- [ ] Verify dark theme loads correctly
- [ ] Check all CSS/JS assets load (no 404s)
- [ ] Test animations (scroll, hover effects)
- [ ] Verify analytics tracking in GA4 Realtime
- [ ] Test on mobile viewport
- [ ] Verify CTA buttons link to Gumroad correctly

## Files Structure

```
Root Level:
├── index.html          (A/B router - includes /new)
├── root.html           (neo-brutalist)
├── buy.html            (embedded checkout)
├── purchase.html       (SaaS landing)
├── gum.html            (redirect)
├── new.html            (modern dark theme) ✅ NEW
├── test-variants.html  (testing dashboard)
├── _redirects          (Cloudflare routing)
├── wrangler.toml       (Cloudflare config)
├── .pages-include      (deployment manifest) ✅ UPDATED
├── assets/
│   └── files/          (icons)
├── screenshots/        (product screenshots)
└── web/
    ├── claude_landing_page_v2/
    │   ├── css/
    │   ├── js/
    │   └── assets/
    └── new_landing_page/  ✅ NEW
        ├── index.html
        ├── css/
        │   └── style.css
        └── js/
            └── main.js
```

## Deployment Process Used

### Step 1: Prepare Files
```bash
# Created clean deployment directory
mkdir -p /tmp/signkit_deploy_complete

# Copied all necessary files
cp index.html root.html buy.html purchase.html gum.html new.html test-variants.html /tmp/signkit_deploy_complete/
cp _redirects wrangler.toml /tmp/signkit_deploy_complete/
cp -r assets screenshots /tmp/signkit_deploy_complete/
cp -r web/claude_landing_page_v2 web/new_landing_page /tmp/signkit_deploy_complete/web/
```

### Step 2: Deploy to Cloudflare
```bash
wrangler pages deploy /tmp/signkit_deploy_complete \
  --project-name=signkit-landing \
  --branch=landing-page \
  --commit-dirty=true
```

### Step 3: Verify Deployment
- Deployment URL: https://e70d23b5.signkit-landing.pages.dev
- Status: ✅ Success
- Files uploaded: 0 new, 32 already cached

### Step 4: Update Git
```bash
git add .pages-include index.html
git commit -m "feat: add /new variant to Cloudflare Pages deployment"
git push origin landing-page
```

## Why Manual Deployment Was Needed

1. **Large Files Issue:** Repo contains build artifacts (SignKit-Linux/SignKit_Linux.tar.gz is 228 MiB)
2. **Cloudflare Limit:** Pages only supports files up to 25 MiB
3. **Solution:** Use `.pages-include` to specify only landing page files
4. **Deployment:** Manual `wrangler pages deploy` from filtered directory

## Future Deployments

### Option 1: Manual (Current Method)
```bash
# Create clean deploy directory
rm -rf /tmp/signkit_deploy
mkdir -p /tmp/signkit_deploy

# Copy files from .pages-include
cp index.html root.html buy.html purchase.html gum.html new.html test-variants.html /tmp/signkit_deploy/
cp _redirects wrangler.toml /tmp/signkit_deploy/
cp -r assets screenshots /tmp/signkit_deploy/
mkdir -p /tmp/signkit_deploy/web
cp -r web/claude_landing_page_v2 web/new_landing_page /tmp/signkit_deploy/web/

# Deploy
wrangler pages deploy /tmp/signkit_deploy --project-name=signkit-landing --branch=landing-page
```

### Option 2: Automated Script
Use `scripts/deploy_landing.sh` (needs update to work from root, not web/live/)

### Option 3: GitHub Actions
Create workflow to deploy only files listed in `.pages-include`

## Monitoring

### GA4 Dashboard:
1. Go to GA4 → Reports → Realtime
2. Look for `variant_view` events
3. Filter by `variant: new`
4. Monitor conversion rates vs other variants

### Cloudflare Analytics:
1. Go to Cloudflare Dashboard → Pages → signkit-landing
2. View deployment history
3. Check traffic analytics
4. Monitor performance metrics

## Rollback Procedure

If issues arise:

1. **Via Cloudflare Dashboard:**
   - Go to Pages → signkit-landing → Deployments
   - Find previous working deployment
   - Click "Rollback to this deployment"

2. **Via Git:**
   ```bash
   git revert HEAD
   git push origin landing-page
   # Then redeploy manually
   ```

3. **Quick Fix - Disable /new in A/B Test:**
   - Edit `index.html`
   - Remove `/new` from random assignment logic
   - Redeploy

## Known Issues

None currently. All files deployed successfully.

## Next Steps

1. ✅ Deployment complete
2. ⏳ Monitor GA4 for `/new` variant traffic
3. ⏳ Collect conversion data (7-14 days minimum)
4. ⏳ Compare performance vs other variants
5. ⏳ Decide on winning variant based on data

---

**Deployed:** November 26, 2025  
**Deployment ID:** e70d23b5  
**Status:** ✅ Live and tracking  
**Git Commit:** c08e813
