# Landing Page Deployment Guide

## Quick Start

### Safe Deployment (Recommended)
```bash
# From project root
./scripts/deploy_landing.sh
```

This script will:
1. Check you're on the right branch
2. Check for uncommitted changes
3. Run verification checks
4. Show what will be deployed
5. Ask for confirmation
6. Deploy to Cloudflare

### Manual Deployment
```bash
# 1. Verify files first
./scripts/verify_deployment.sh

# 2. If verification passes, deploy
cd web/live
wrangler pages deploy . --project-name signkit-landing --branch landing-page
```

## What Gets Deployed

**ONLY files in `web/live/` directory are deployed.**

### Critical Files
- `index.html` - Main landing page (neo-brutalism)
- `root.html` - Alternative landing page
- `purchase.html` - Purchase page (modern gradient)
- `buy.html`, `gum.html` - Redirect pages
- `robots.txt`, `sitemap.xml` - SEO files
- `wrangler.toml` - Deployment config

### Assets
- `css/` - Standalone CSS for index/root pages
- `js/` - Standalone JavaScript
- `assets/files/` - Icons and logos
- `screenshots/` - Product screenshots
- `web/claude_landing_page_v2/` - CSS/JS for purchase.html

## Verification Checklist

Before deploying, the verification script checks:

✓ All HTML files exist  
✓ CSS and JS files exist  
✓ Nested assets for purchase.html exist  
✓ Icons and screenshots present  
✓ SEO files present  
✓ Wrangler config exists  
✓ root.html has neo-brutalism footer (inline styles)  
✓ purchase.html references correct CSS path  
✓ Carousel timing is set correctly  

## Common Issues

### Issue: Changes not appearing on live site
**Cause:** You edited root-level files instead of `web/live/` files  
**Fix:** Edit files in `web/live/` directory, then deploy

### Issue: purchase.html looks broken
**Cause:** Missing `web/live/web/claude_landing_page_v2/` directory  
**Fix:** Ensure nested directory structure exists with CSS/JS files

### Issue: Footer styling wrong on /root
**Cause:** Footer using external CSS classes instead of inline styles  
**Fix:** Footer must have inline `style=""` attributes for neo-brutalism design

### Issue: Carousel too fast
**Cause:** Timing set to 3000ms instead of 5000ms  
**Fix:** Edit `web/live/web/claude_landing_page_v2/js/main.js`:
```javascript
autoPlayInterval = setInterval(nextStep, 5000); // 5 seconds
```

## Deployment Workflow

1. **Make changes** in `web/live/` directory
2. **Test locally**:
   ```bash
   cd web/live
   python -m http.server 8000
   # Visit http://localhost:8000
   ```
3. **Run verification**:
   ```bash
   ./scripts/verify_deployment.sh
   ```
4. **Commit changes**:
   ```bash
   git add web/live/
   git commit -m "fix: description"
   git push origin landing-page
   ```
5. **Deploy**:
   ```bash
   ./scripts/deploy_landing.sh
   ```
6. **Verify deployment**:
   ```bash
   wrangler pages deployment list --project-name signkit-landing
   ```

## View Deployments

```bash
# List all deployments
wrangler pages deployment list --project-name signkit-landing

# View specific deployment
# Check the URL from the deployment output
```

## Rollback

If you need to rollback to a previous deployment:

1. Go to Cloudflare Dashboard
2. Navigate to Pages > signkit-landing
3. Find the previous deployment
4. Click "Rollback to this deployment"

Or redeploy from a previous git commit:
```bash
git checkout <previous-commit-hash>
cd web/live
wrangler pages deploy . --project-name signkit-landing --branch landing-page
git checkout landing-page  # Return to latest
```

## Testing

### E2E Tests
```bash
cd web/e2e
npm test
```

### Manual Testing
See `web/live/TEST_CHECKLIST.md`

## Important Notes

- Always work on `landing-page` branch
- Never edit root-level HTML files (they don't get deployed)
- Run verification before every deployment
- Test locally before deploying
- Keep `web/live/` directory clean and organized

## Help

For detailed architecture documentation, see:
- `docs/LANDING_PAGE_ARCHITECTURE.md`

For issues or questions:
- Check verification script output
- Review deployment logs in Cloudflare dashboard
- Test locally to reproduce issues
