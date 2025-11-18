# SignKit Landing Page Documentation

> Complete guide to the SignKit landing page deployment on Cloudflare Pages with A/B testing

**Branch:** `landing-page`  
**Status:** ✅ Deployed & Live  
**Last Updated:** November 18, 2025

---

## 🌐 Live URLs

### Production (Custom Domain)
- **Main:** https://signkit.work
- **Control Variant:** https://signkit.work/root
- **Buy Variant (Iframe):** https://signkit.work/buy
- **Purchase Variant (SaaS):** https://signkit.work/purchase
- **Gum Variant (Redirect):** https://signkit.work/gum
- **Test Dashboard:** https://signkit.work/test-variants.html

### Cloudflare Pages (Staging)
- **Main:** https://d5834d2a.signkit-landing.pages.dev
- **Control:** https://d5834d2a.signkit-landing.pages.dev/root
- **Buy:** https://d5834d2a.signkit-landing.pages.dev/buy
- **Purchase:** https://d5834d2a.signkit-landing.pages.dev/purchase
- **Gum:** https://d5834d2a.signkit-landing.pages.dev/gum

---

## 📁 Repository Structure

```
Branch: landing-page
├── Landing Pages (5 variants)
│   ├── index.html          # Main entry with A/B routing
│   ├── root.html           # Control (neo-brutalism)
│   ├── buy.html            # Embedded checkout
│   ├── purchase.html       # SaaS landing
│   └── gum.html            # Direct redirect
│
├── Configuration
│   ├── _redirects          # Cloudflare routing rules
│   ├── wrangler.toml       # Cloudflare Pages config
│   ├── .cfignore           # Deployment exclusions
│   └── test-pages.sh       # Automated testing
│
├── Assets
│   ├── assets/files/       # Icons (32x32, 64x64, 256x256)
│   ├── screenshots/        # Product screenshots (1, 2, 3)
│   └── web/claude_landing_page_v2/  # CSS/JS for purchase.html
│
└── Documentation
    ├── README_LANDING_PAGE.md      # Project overview
    ├── QUICK_START.md              # 5-minute deploy guide
    ├── CLOUDFLARE_DEPLOYMENT.md    # Full deployment guide
    ├── DEPLOYMENT_CHECKLIST.md     # Step-by-step checklist
    ├── AB_TEST_STRUCTURE.md        # A/B test details
    ├── DEPLOYMENT_SUMMARY.md       # Status summary
    ├── DEPLOYMENT_STATUS.md        # Current status
    └── DOMAIN_SETUP_GUIDE.md       # DNS configuration
```

---

## 🎯 A/B Testing Setup

### Current Configuration
**Mode:** Manual Testing (`AUTO_SPLIT = false`)

### 4 Variants Being Tested

#### Variant 1: Control (`/root`)
- **Design:** Neo-brutalism
- **CTA:** External Gumroad link
- **Hypothesis:** Simple, privacy-focused design converts best
- **File:** `root.html`

#### Variant 2: Embedded Checkout (`/buy`)
- **Design:** Full-page iframe
- **CTA:** Embedded Gumroad checkout
- **Hypothesis:** Keeping users on domain increases trust
- **File:** `buy.html`
- **Iframe URL:** https://gum.new/gum/cmhyha3rs001h04l7ccem2nkj

#### Variant 3: SaaS Landing (`/purchase`)
- **Design:** Traditional SaaS with animations
- **CTA:** External Gumroad link
- **Hypothesis:** Detailed features increase perceived value
- **File:** `purchase.html`

#### Variant 4: Direct Redirect (`/gum`)
- **Design:** Immediate redirect
- **CTA:** Instant redirect to Gumroad
- **Hypothesis:** Minimal friction for high-intent users
- **File:** `gum.html`
- **Redirect URL:** https://pranaysuyash.gumroad.com/l/signkit-v1

### Traffic Distribution (When AUTO_SPLIT = true)
- 25% → Control (`/root`)
- 25% → Embedded (`/buy`)
- 25% → SaaS (`/purchase`)
- 25% → Direct (`/gum`)

---

## 🚀 Deployment

### Platform
**Cloudflare Pages**
- Project: `signkit-landing`
- Branch: `landing-page`
- Build: None (static files)
- Output: `/`

### Deployment Method
```bash
# Via Wrangler CLI
wrangler pages deploy .deploy --project-name=signkit-landing --branch=landing-page
```

### Auto-Deploy
Cloudflare Pages automatically deploys on push to `landing-page` branch.

---

## 🌍 Domain Configuration

### Domain
**signkit.work** (registered via Namecheap)

### DNS Provider
**Cloudflare** (nameservers pointed to Cloudflare)

### DNS Records
```
Type    Name              Content                        Proxy
CNAME   signkit.work      signkit-landing.pages.dev      Proxied
CNAME   www               signkit-landing.pages.dev      Proxied
MX      signkit.work      smtp.google.com                DNS only
TXT     signkit.work      v=spf1 include:_spf.google.com ~all
TXT     signkit.work      google-site-verification=...
```

### SSL/TLS
- **Mode:** Full (strict)
- **Certificate:** Auto-provisioned by Cloudflare
- **Status:** Active

---

## 📊 Analytics

### Google Analytics 4
- **Property ID:** `G-PCJDGBMRRN`
- **Event:** `ab_test_impression`
- **Parameters:**
  - `variant`: control | buy | purchase | gum
  - `experiment_id`: checkout_flow_test

### Tracking Implementation
All variants include GA4 tracking script that fires on page load.

### View Results
1. Go to [GA4 Dashboard](https://analytics.google.com/)
2. Navigate to **Reports** → **Events**
3. Look for `ab_test_impression` event
4. Filter by `variant` parameter

---

## 🔧 Configuration

### Enable A/B Testing
To enable automatic traffic splitting:

1. Edit `index.html` in `landing-page` branch
2. Change: `const AUTO_SPLIT = false;` → `const AUTO_SPLIT = true;`
3. Commit and push
4. Cloudflare auto-deploys

### Disable A/B Testing
Set `AUTO_SPLIT = false` to show control page to all visitors.

---

## 🧪 Testing

### Local Testing
```bash
# Start local server
python3 -m http.server 8080

# Run automated tests
chmod +x test-pages.sh
./test-pages.sh

# Open test dashboard
open http://localhost:8080/test-variants.html
```

### Production Testing
Visit each variant URL and verify:
- ✅ Page loads correctly
- ✅ Assets load (images, CSS, JS)
- ✅ CTA buttons work
- ✅ GA4 tracking fires
- ✅ Mobile responsive

---

## 📝 Maintenance

### Update Landing Page
```bash
# Switch to landing-page branch
git checkout landing-page

# Make changes
# ... edit files ...

# Commit and push
git add .
git commit -m "Update landing page"
git push origin landing-page

# Cloudflare auto-deploys
```

### Redeploy Manually
```bash
# Prepare deployment directory
rm -rf .deploy
mkdir -p .deploy
cp -r index.html root.html buy.html purchase.html gum.html \
      test-variants.html _redirects assets screenshots web .deploy/

# Deploy
wrangler pages deploy .deploy --project-name=signkit-landing --branch=landing-page
```

---

## 🎯 Success Metrics

### Primary Metric
**Conversion Rate:** Purchases / Unique Visitors

### Secondary Metrics
- Click-through Rate (CTA clicks / Page views)
- Bounce Rate
- Time on Page
- Exit Rate

### Target Sample Size
- **Minimum:** 100 conversions per variant
- **Total Visitors:** ~4,000+ (assuming 1% conversion rate)
- **Duration:** 14-30 days
- **Confidence Level:** 95%

---

## 🐛 Troubleshooting

### Issue: Domain not resolving
**Solution:** Wait 24-48 hours for DNS propagation, check nameservers

### Issue: Assets not loading
**Solution:** Verify paths are relative, check `.cfignore` exclusions

### Issue: Iframe not loading on /buy
**Solution:** Check browser console for CSP errors, verify Gumroad URL

### Issue: A/B routing not working
**Solution:** Verify `AUTO_SPLIT` setting, clear localStorage

---

## 📞 Support & Resources

### Cloudflare
- **Dashboard:** https://dash.cloudflare.com/pages/signkit-landing
- **Docs:** https://developers.cloudflare.com/pages/
- **Community:** https://community.cloudflare.com/

### Repository
- **GitHub:** https://github.com/pranaysuyash/sig_ext_fastapi_react
- **Branch:** `landing-page`
- **Issues:** Report via GitHub Issues

### Documentation
All documentation is in the `landing-page` branch:
- `QUICK_START.md` - Quick deployment guide
- `CLOUDFLARE_DEPLOYMENT.md` - Comprehensive guide
- `AB_TEST_STRUCTURE.md` - A/B test details
- `DOMAIN_SETUP_GUIDE.md` - DNS configuration

---

## 🔄 Workflow

### Development → Staging → Production

```
1. Local Development
   ├── Edit files in landing-page branch
   ├── Test locally (python -m http.server)
   └── Commit changes

2. Staging (Cloudflare Pages)
   ├── Push to landing-page branch
   ├── Auto-deploy to *.pages.dev
   └── Test on staging URL

3. Production (Custom Domain)
   ├── Verify staging works
   ├── DNS propagates to signkit.work
   └── Monitor analytics
```

---

## 📈 Roadmap

### Phase 1: Testing (Current)
- ✅ Deploy all variants
- ✅ Configure DNS
- ⬜ Test all variants
- ⬜ Verify GA4 tracking

### Phase 2: Soft Launch
- ⬜ Enable AUTO_SPLIT
- ⬜ Drive initial traffic
- ⬜ Monitor for bugs

### Phase 3: Full A/B Test
- ⬜ Run for 14-30 days
- ⬜ Collect 100+ conversions per variant
- ⬜ Analyze results

### Phase 4: Optimization
- ⬜ Identify winning variant
- ⬜ Implement winner as default
- ⬜ Iterate and optimize

---

## 🎉 Quick Reference

### Key URLs
- **Production:** https://signkit.work
- **Staging:** https://d5834d2a.signkit-landing.pages.dev
- **Dashboard:** https://dash.cloudflare.com/pages/signkit-landing
- **Analytics:** https://analytics.google.com/ (G-PCJDGBMRRN)

### Key Files
- `index.html` - Main entry (A/B routing)
- `_redirects` - Cloudflare routing
- `wrangler.toml` - Deployment config

### Key Commands
```bash
# Deploy
wrangler pages deploy .deploy --project-name=signkit-landing

# Test locally
python3 -m http.server 8080

# Check DNS
dig signkit.work
```

---

**Deployed:** November 18, 2025  
**Status:** ✅ Live  
**Branch:** `landing-page`  
**Platform:** Cloudflare Pages  
**Domain:** signkit.work
