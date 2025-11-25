# SignKit Landing Page Architecture

**Last Updated:** November 25, 2025  
**Branch:** `landing-page`  
**Live URL:** https://signkit.work (via Cloudflare Pages)

## Critical Information

### What Gets Deployed to Production
**ONLY the contents of `web/live/` directory are deployed to Cloudflare Pages.**

When you run:
```bash
cd web/live
wrangler pages deploy . --project-name signkit-landing --branch landing-page
```

Everything in `web/live/` becomes the root of the website.

---

## Directory Structure

### Production Files (web/live/)
```
web/live/
├── index.html                    # Main landing page (neo-brutalism design)
├── root.html                     # Alternative landing page (/root route)
├── index.root.html               # Backup/variant of root page
├── purchase.html                 # Purchase page (/purchase route)
├── buy.html                      # Buy redirect page
├── gum.html                      # Gumroad redirect page
├── test-variants.html            # A/B testing page
├── robots.txt                    # SEO robots file
├── sitemap.xml                   # SEO sitemap
├── wrangler.toml                 # Cloudflare deployment config
│
├── css/                          # Standalone CSS (for web/live pages)
│   ├── style.css                 # Main styles
│   ├── animations.css            # Animation styles
│   ├── font-awesome-additions.css
│   └── style-complete.css
│
├── js/                           # Standalone JavaScript
│   ├── main.js                   # Main JS (carousel, nav, etc.)
│   ├── animations.js             # Animation logic
│   └── analytics.js              # GA4 & Clarity tracking
│
├── assets/                       # Images and icons
│   └── files/
│       ├── signkit_icon_16x16.png
│       ├── signkit_icon_32x32.png
│       ├── signkit_icon_64x64.png
│       └── signkit_icon_256x256.png
│
├── screenshots/                  # Product screenshots
│   ├── screenshot-1.png
│   ├── screenshot-2.png
│   └── screenshot-3.png
│
└── web/                          # Nested directory for shared assets
    └── claude_landing_page_v2/   # Shared CSS/JS for purchase.html
        ├── css/
        │   ├── style.css         # Purchase page styles
        │   └── animations.css
        ├── js/
        │   ├── main.js           # Purchase page JS
        │   ├── animations.js
        │   └── analytics.js
        └── assets/
```

### Root-Level Files (NOT deployed)
```
/ (project root)
├── index.html                    # Development version (has A/B test logic)
├── root.html                     # Development version
├── purchase.html                 # Development version
├── buy.html                      # Development version
├── gum.html                      # Development version
└── test-analytics.html           # Analytics testing page
```

**⚠️ IMPORTANT:** These root-level HTML files are NOT deployed. They are development/testing versions. Only `web/live/` contents are deployed.

### Other Web Directories (NOT deployed)
```
web/
├── claude_landing_page_v2/       # Shared assets (symlinked in web/live)
├── archives/                     # Old versions (backup)
├── backups/                      # Backup copies
├── e2e/                          # Playwright tests
└── [various other landing page experiments]
```

---

## Page Variants & Routes

### Live Routes (on signkit.work)

| Route | File | Design | Purpose |
|-------|------|--------|---------|
| `/` or `/index` | `web/live/index.html` | Neo-brutalism | Main landing page (A/B test enabled) |
| `/root` | `web/live/root.html` | Neo-brutalism | Alternative landing page |
| `/purchase` | `web/live/purchase.html` | Modern gradient | Detailed purchase page with features |
| `/buy` | `web/live/buy.html` | Redirect | Redirects to Gumroad |
| `/gum` | `web/live/gum.html` | Redirect | Redirects to Gumroad |

### A/B Testing Logic
In `web/live/index.html`, there's JavaScript that controls A/B testing:
```javascript
const AUTO_SPLIT = true; // Enable auto A/B testing
```

When enabled, visitors to `/` are randomly redirected to either:
- `/root` (50% chance)
- `/buy` (25% chance)
- `/purchase` (25% chance)

Direct access to `/root`, `/buy`, `/purchase` always works regardless of AUTO_SPLIT.

---

## Design Systems

### Neo-Brutalism Design (index.html, root.html)
**Characteristics:**
- Inline styles (no external CSS dependencies)
- Bold black borders (3px solid #111827)
- Strong shadows (8px 8px 0 #111827)
- Bright accent colors (#ffb800, #4f46e5, #00c2a8)
- Space Grotesk font
- Card-based layout with strong visual hierarchy

**Key Elements:**
- `.shell` - Main container with border and shadow
- `.hero-highlight` - Rotated accent badges
- `.btn-primary` - Buttons with hover lift effect
- `.preview-card` - Product preview with mock window
- Footer with grid layout (1.5fr 1fr 1fr 1fr)

### Modern Gradient Design (purchase.html)
**Characteristics:**
- External CSS from `web/claude_landing_page_v2/css/style.css`
- Gradient backgrounds
- Smooth animations
- Inter + Space Grotesk fonts
- Mesh gradient hero section
- Carousel with 5-second transitions

**Key Elements:**
- `.hero` with mesh gradient background
- `.demo-carousel` with auto-rotating screenshots
- `.tabs` for feature showcase
- `.pricing-card` with comparison table
- Footer with dark background (uses external CSS classes)

---

## CSS & JavaScript Dependencies

### For index.html and root.html (Neo-brutalism)
- **CSS:** All inline styles (self-contained)
- **JS:** Inline JavaScript for A/B testing
- **Fonts:** Google Fonts (Space Grotesk)
- **Icons:** Font Awesome CDN
- **Analytics:** Google Analytics (G-PCJDGBMRRN), Microsoft Clarity

### For purchase.html (Modern gradient)
- **CSS:** 
  - `web/claude_landing_page_v2/css/style.css`
  - `web/claude_landing_page_v2/css/animations.css`
- **JS:**
  - `web/claude_landing_page_v2/js/main.js` (carousel, nav, FAQ)
  - `web/claude_landing_page_v2/js/animations.js`
  - `web/claude_landing_page_v2/js/analytics.js`
- **Fonts:** Google Fonts (Inter, Space Grotesk)
- **Icons:** Font Awesome CDN
- **Analytics:** Same as above

---

## Key Configuration Files

### wrangler.toml (web/live/wrangler.toml)
```toml
name = "signkit-landing"
type = "javascript"
account_id = "9af41d56d8210eaef657aa2635ab5d73"
compatibility_date = "2025-11-20"

[build]
command = ""
upload = "./"

[site]
bucket = "./"
entry-point = "."
```

### Analytics Configuration
- **Google Analytics ID:** G-PCJDGBMRRN
- **Microsoft Clarity ID:** u8zyh41jr0
- **Internal traffic exclusion:** Cookie-based (`ga_internal=true`)
- **Variant tracking:** Each page tracks its variant name

---

## Common Issues & Solutions

### Issue 1: Changes not appearing on live site
**Problem:** You edited root-level files (e.g., `/root.html`) but changes don't show on signkit.work  
**Solution:** Edit `web/live/root.html` instead, then deploy:
```bash
cd web/live
wrangler pages deploy . --project-name signkit-landing --branch landing-page
```

### Issue 2: CSS not loading on purchase.html
**Problem:** Purchase page looks broken  
**Solution:** Ensure `web/live/web/claude_landing_page_v2/` directory exists with CSS/JS files

### Issue 3: Footer styling inconsistent
**Problem:** Footer on /root has dark background instead of neo-brutalism  
**Solution:** The footer must use inline styles, not external CSS classes. Check `web/live/root.html` for inline `style=""` attributes.

### Issue 4: Carousel too fast
**Problem:** Screenshots change too quickly  
**Solution:** Edit `web/live/web/claude_landing_page_v2/js/main.js`:
```javascript
autoPlayInterval = setInterval(nextStep, 5000); // 5 seconds
```

### Issue 5: Images showing UI chrome/sidebars
**Problem:** Screenshots show too much app UI  
**Solution:** Use `object-fit: cover` in CSS:
```css
.demo-step img {
    object-fit: cover;
    object-position: center;
}
```

---

## Deployment Workflow

### 1. Make Changes
Edit files in `web/live/` directory:
```bash
# For neo-brutalism pages
vim web/live/index.html
vim web/live/root.html

# For purchase page
vim web/live/purchase.html
vim web/live/web/claude_landing_page_v2/css/style.css
vim web/live/web/claude_landing_page_v2/js/main.js
```

### 2. Test Locally
```bash
cd web/live
python -m http.server 8000
# Visit http://localhost:8000
```

### 3. Commit Changes
```bash
git add web/live/
git commit -m "fix: description of changes"
git push origin landing-page
```

### 4. Deploy to Cloudflare
```bash
cd web/live
wrangler pages deploy . --project-name signkit-landing --branch landing-page
```

### 5. Verify Deployment
```bash
wrangler pages deployment list --project-name signkit-landing
```

Check the latest deployment URL (e.g., `https://abc123.signkit-landing.pages.dev`)

---

## Asset Locations

### Screenshots
- **Source:** `screenshots_final/` (high-quality originals)
- **Deployed:** `web/live/screenshots/` (optimized for web)
- **Used by:** purchase.html carousel, index.html preview

### Icons/Logos
- **Source:** `assets/files/`
- **Deployed:** `web/live/assets/files/`
- **Sizes:** 16x16, 32x32, 64x64, 256x256 PNG

### Promotional Materials
- **Location:** `promotional_material/`
- **Contents:**
  - `product_hunt/` - PH gallery images
  - `reddit/` - Reddit post images
  - `social_media/` - Social media assets
- **NOT deployed** (used for marketing only)

---

## Testing

### E2E Tests
Location: `web/e2e/`

Run tests:
```bash
cd web/e2e
npm test
```

Test files:
- `specs/carousel.spec.js` - Carousel functionality
- `specs/footer.spec.js` - Footer layout
- `specs/purchase_layout.spec.js` - Purchase page layout

### Manual Testing Checklist
See: `web/live/TEST_CHECKLIST.md`

---

## Branch Strategy

- **main:** Desktop app development
- **landing-page:** Landing page development and deployment
- **landing-publish-*:** Automated deployment branches

Always work on `landing-page` branch for landing page changes.

---

## Quick Reference Commands

```bash
# Switch to landing page branch
git checkout landing-page

# Deploy to Cloudflare
cd web/live && wrangler pages deploy . --project-name signkit-landing --branch landing-page

# List deployments
wrangler pages deployment list --project-name signkit-landing

# Run E2E tests
cd web/e2e && npm test

# Start local server
cd web/live && python -m http.server 8000
```

---

## Contact & Support

For landing page issues:
- Check this document first
- Review `web/live/README.md`
- Check deployment logs in Cloudflare dashboard
- Test locally before deploying

**Remember:** Only `web/live/` contents are deployed. Always edit files there, not in the project root.
