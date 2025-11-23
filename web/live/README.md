# SignKit Landing Page V2 - Production Ready

## 🎯 What's New in V2

This version improves upon the original Claude landing page with:

- ✅ **Font Awesome icons** instead of emojis (professional look)
- ✅ **Screenshot placeholders** ready for your actual app screenshots
- ✅ **YouTube video embed** option for hero demo
- ✅ **Responsive image handling** with proper captions
- ✅ **Updated branding** to "SignKit" (change to your final name)

---

## 📂 Project Structure

```
claude_landing_page_v2/
├── index.html                 # Main HTML file with Font Awesome
├── css/
│   ├── style.css             # Main styles (Font Awesome compatible)
│   └── animations.css        # [Copy from original]
├── js/
│   ├── main.js               # [Copy from original]
│   └── animations.js         # [Copy from original]
└── assets/
    └── screenshots/          # 👈 PUT YOUR SCREENSHOTS HERE
        ├── step1-upload.png  # Upload document interface
        ├── step2-select.png  # Selection + zoom tool
        ├── step3-clean.png   # Cleaned signature
        └── step4-sign.png    # PDF signing interface
```

---

## 🚀 Quick Setup (5 Steps)

### Step 1: Copy Missing Files

You need to copy these from the original landing page:

```bash
# From project root
cd web/claude_landing_page_v2

# Copy animations CSS
cp ../claude_landing_page/css/animations.css ./css/

# Copy JavaScript files
cp ../claude_landing_page/js/main.js ./js/
cp ../claude_landing_page/js/animations.js ./js/
```

### Step 2: Add Your Screenshots

Take 4 screenshots of your app and save them as:

- `assets/screenshots/step1-upload.png` - Upload document screen
- `assets/screenshots/step2-select.png` - Signature selection with zoom
- `assets/screenshots/step3-clean.png` - Cleaned extracted signature
- `assets/screenshots/step4-sign.png` - PDF signing interface
  Note: Some common pages (`index.html`, `root.html`, `purchase.html`) reference the repo root `screenshots/` folder. Even if you add per-variant screenshots, keep the root `screenshots/screenshot-*.png` files in the repo or copy them during build so those variants continue to work.

**Screenshot specs:**

- Format: PNG
- Dimensions: 800x600px (or similar 4:3 ratio)
- File size: < 500KB each (compress if needed)
- Show actual UI, not placeholders

### Step 3: Add YouTube Demo (Optional)

If you upload a demo video to YouTube:

1. Upload your 45-60 second demo to YouTube
2. Get the video ID (the part after `v=` in the URL)
3. Open `index.html`
4. Find line ~134: `src="https://www.youtube.com/embed/YOUR_VIDEO_ID"`
5. Replace `YOUR_VIDEO_ID` with your actual video ID
6. Change `style="display: none;"` to `style="display: block;"`
7. Change the carousel div style to `style="display: none;"`

### Step 4: Update Gumroad Link

Find all instances of button click handlers and update with your Gumroad product URL:

```javascript
// In js/main.js, add at the top:
const GUMROAD_URL = 'https://gumroad.com/l/your-product-id';

// Then update all CTA buttons to use this URL
```

Or manually update in HTML - search for all button IDs:

- `#heroCTA`
- `#navCTA`
- `#pricingCTA`
- `#finalCTA`
- `#demoBtn` (for video modal)

### Step 5: Test Locally

```bash
# Using Python
python3 -m http.server 8000

# OR using Node
npx serve

# OR using VS Code Live Server extension
```

Open http://localhost:8000 in your browser

---

## 🖼 Image Optimization & Cloudflare Upload (Local-only)

We provide a small set of local helper scripts for generating responsive WebP screenshots and optionally uploading them to Cloudflare Images. These helper scripts are intentionally local-only (ignored by git) so you can use them to optimize and publish assets from your development machine.

1. Convert PNG screenshots to WebP (lossy) variants using Pillow:

```bash
# create a local venv (recommended)
python3 -m venv .venv
source .venv/bin/activate
pip install pillow
python3 tools/convert_images.py
```

This script writes `-1200.webp`, `-768.webp`, and `-380.webp` variants next to your existing PNGs in `web/live/assets/screenshots/`.

2. Optionally push the generated WebP images to Cloudflare Images from your local machine (requires a Cloudflare account, an API token scoped to `Images:Edit`, and your `ACCOUNT_ID`):

```bash
pip install requests

# Set env vars (macOS / Linux)
export CLOUDFLARE_ACCOUNT_ID=your_account_id
export CLOUDFLARE_API_TOKEN=your_token

# And run the local uploader (this file is ignored by git and kept locally)
python3 tools/upload_to_cloudflare.py
```

3. After conversion, the `web/live/index.html` file is already set up to prefer WebP variants (via `<picture>` sources and responsive `srcset`), so the static assets will be automatically used when served. Cloudflare Pages (or Netlify/Vercel) will serve images from your repo; Cloudflare Images will serve directly from the CDN when uploaded via the script.

Security note: Do not commit your Cloudflare API token and keep the `tools` helpers local and secure. If you need an automation step in CI/Conventional workflows, we can discuss secure variables and token management later.

## Why are helper scripts kept local (not committed)?

We keep local helper scripts such as `tools/convert_images.py` and `tools/upload_to_cloudflare.py` untracked for the following reasons:

If you'd like the repository to contain a helper example, we commit a safe sample file: `tools/upload_to_cloudflare.sample.py` (without secrets). Use it as a starting point and copy to `tools/upload_to_cloudflare.py` locally when you're ready.

If you'd prefer automating these steps in CI/CD, we can add an action that runs the conversion (or uploads) using GitHub Actions with secrets stored in `Settings -> Secrets & variables` for the repository. This enables a secure automation route without exposing credentials in the codebase.

### Manual Publish with Wrangler (Cloudflare Pages)

If you have `wrangler` configured locally and want to deploy the landing `web/live` folder directly to Cloudflare Pages without waiting for GitHub or CI, do this from your development machine:

```bash
# Install wrangler (if not installed):
npm install -g @cloudflare/wrangler

# Export your Cloudflare credentials
export CLOUDFLARE_ACCOUNT_ID=your_account_id
export CLOUDFLARE_API_TOKEN=your_api_token

# Publish folder to Cloudflare Pages (landing branch preview)
wrangler pages deploy web/live --project-name signkit-landing --branch landing-page
```

Notes:

- This publishes the contents of `web/live` to the Pages project (signkit-landing) under the `landing-page` branch.
- If the Pages project is set to build from `landing-page`, a new build should pick up these files automatically.
- We included an optional workflow (`.github/workflows/manual_publish_landing.yml`) that can be triggered manually from the Actions tab to run the same command via GitHub Actions; you'll need to set `CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_API_TOKEN` in repository secrets for it to succeed.

### Auto Publish (Optional)

We also provide an optional, guarded auto-publish workflow (`.github/workflows/auto_publish_landing.yml`) that automatically publishes `web/live` to Cloudflare Pages when commits are pushed to the `landing-page` branch. This workflow will only publish when the push contains changes restricted to `web/live` or the root landing pages (index/buy/purchase/gum/root) — any broader changes will abort the publish to prevent accidental site updates.

---

## 🎨 Customization Guide

### Change Brand Name

Search and replace "SignKit" with your chosen name:

- In `index.html` (appears ~15 times)
- In page title, meta tags, and all text content

### Update Colors

Edit `css/style.css` CSS variables:

```css
:root {
  --navy: #1a1f36; /* Dark text color */
  --blue: #3b82f6; /* Primary brand color */
  --orange: #f59e0b; /* CTA buttons */
  /* ... change any colors you want */
}
```

### Update Pricing

In `index.html`, find the pricing section and update:

- Launch price (currently $29)
- Regular price (currently $39)
- Feature list

### Update Social Proof Numbers

Replace placeholder numbers:

- "1,200+ Happy Customers" → Use real number or "Early Access"
- "12,847 Signatures Extracted" → Remove if not accurate
- "4.8/5 Average Rating" → Add when you have reviews

---

## ✅ Pre-Launch Checklist

Before deploying to production:

### Content

- [ ] All 4 screenshots added to `assets/screenshots/`
- [ ] YouTube video ID added (or carousel kept as default)
- [ ] Brand name updated from "SignKit" to your choice
- [ ] Pricing updated ($29/$39 or your prices)
- [ ] Gumroad product URL added to all CTA buttons
- [ ] Social proof numbers updated (or marked as "Early Access")
- [ ] Meta description and title updated
- [ ] OG image created and added (`assets/og-image.jpg`)

### Technical

- [ ] All CTA buttons link to Gumroad
- [ ] Responsive design tested on mobile
- [ ] Page loads in < 3 seconds
- [ ] No console errors in browser
- [ ] All images optimized (< 500KB each)
- [ ] Analytics code added (Google Analytics, Plausible, etc.)

### Legal

- [ ] Privacy Policy link updated
- [ ] Terms of Service link updated
- [ ] Refund Policy link updated

---

## 📸 Screenshot Tips

### What to Capture

**Step 1 - Upload:**

- Show the file upload interface
- Empty state or drag-and-drop area
- Make it inviting and simple

**Step 2 - Select:**

- Show signature selection in progress
- Highlight the zoom/pan controls
- Show the precision tools

**Step 3 - Clean:**

- Show before/after comparison
- Highlight the cleaned transparent result
- Show export options

**Step 4 - Sign PDF:**

- Show PDF viewer with signature placed
- Show library of saved signatures
- Show the final signed document

### How to Capture

```bash
# macOS native screenshot
Cmd + Shift + 4    # Select area
Cmd + Shift + 5    # Screenshot UI with options

# Then use Preview to:
1. Resize to 800x600px
2. Export as PNG
3. Compress if > 500KB
```

---

## 🌐 Deployment Options

### Option 1: Netlify (Recommended)

1. Drag and drop the `claude_landing_page_v2` folder
2. Done! You get a URL like `signkit-app.netlify.app`
3. Add custom domain in settings

### Option 2: Vercel

1. Push to GitHub repository
2. Import to Vercel
3. Deploy (auto-builds on every push)

### Option 3: Cloudflare Pages

1. Connect GitHub repo
2. Set build directory to `web/claude_landing_page_v2`
3. Deploy

Note: We expect most production deploys to use Cloudflare Pages (fast global CDN).

To avoid confusion and ensure assets are included in the Pages build, add your screenshots and images under this variant's assets folder prior to publishing:

- `web/claude_landing_page_v2/assets/screenshots/step1-upload.png`
- `web/claude_landing_page_v2/assets/screenshots/step2-select.png`
- `web/claude_landing_page_v2/assets/screenshots/step3-clean.png`

Security note: The `uploads/` folder is a runtime-only folder and should never be committed. If uploads are tracked accidentally, remove them with:

```bash
git rm -r --cached uploads
git commit -m "chore: remove runtime uploads from repository"
```

### Option 4: Cloudflare Pages via wrangler (CLI)

If you prefer using the `wrangler` CLI to deploy your static site, follow the steps below:

1. Install `wrangler` (if not installed):

```bash
npm install -g @cloudflare/wrangler
# or
brew install cloudflare/cloudflare/wrangler
```

2. Ensure `wrangler.toml` in this directory is populated with your `account_id` and `project` name.

3. Run pages publish:

```bash
cd web/claude_landing_page_v2
wrangler pages deploy . --project-name signkit-landing --branch landing-page
```

Note: `wrangler pages publish` can also accept a directory `dist` created by a build step. For simple static pages the site root `.` works fine.

### Option 4: GitHub Pages

1. Create `docs` folder in repo root
2. Copy all files from `claude_landing_page_v2` to `docs`
3. Enable GitHub Pages in repo settings
4. Set source to `docs` folder

---

## 🔧 Common Issues & Fixes

### Icons not showing

**Problem:** Font Awesome CDN blocked  
**Fix:** Download Font Awesome and host locally

```bash
# Download Font Awesome
npm install @fortawesome/fontawesome-free

# Copy to assets
cp -r node_modules/@fortawesome/fontawesome-free/css assets/
cp -r node_modules/@fortawesome/fontawesome-free/webfonts assets/

# Update HTML link to local path
<link rel="stylesheet" href="./assets/css/all.min.css">
```

### Screenshots not loading

**Problem:** Wrong file paths or names  
**Fix:** Check that files are exactly named:

- `step1-upload.png` (not `Step1-Upload.PNG`)
- Located in `assets/screenshots/` folder
- File extensions match (png not jpg)

### Video not playing

**Problem:** YouTube embed blocked or wrong video ID  
**Fix:**

- Check video is not private
- Verify video ID is correct
- Ensure embeds are allowed for the video

### Mobile layout broken

**Problem:** CSS not loading properly  
**Fix:**

- Ensure `style.css` and `animations.css` are both in `css/` folder
- Check browser console for 404 errors
- Verify file paths are correct

---

## 📊 Analytics Setup

Add your analytics code before closing `</body>` tag:

### Google Analytics

```html
<script
  async
  src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"
></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag() {
    dataLayer.push(arguments);
  }
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### Plausible (Privacy-friendly)

```html
<script
  defer
  data-domain="yourdomain.com"
  src="https://plausible.io/js/script.js"
></script>
```

---

## 🎯 Next Steps After Launch

1. **Week 1:** Monitor analytics daily
2. **Week 1:** Collect first 10 customer testimonials
3. **Week 2:** A/B test headline variations
4. **Week 2:** Add testimonials section
5. **Month 1:** Update social proof numbers with real data
6. **Month 1:** Create case studies from power users

---

## 💡 Tips for Success

1. **Screenshots are critical** - They sell more than text. Make them beautiful.
2. **Demo video is gold** - 45 seconds showing the workflow convinces buyers.
3. **Update social proof weekly** - Fresh numbers build credibility.
4. **Test on real devices** - Emulators lie. Test on actual phones/tablets.
5. **Monitor page speed** - Keep load time under 3 seconds.

---

## 📞 Support

If you run into issues:

1. Check browser console for errors (F12 → Console)
2. Verify all files are in correct locations
3. Test with a simple Python server first
4. Check responsive design in browser DevTools

---

## 🚀 Ready to Launch?

Final checklist:

- ✅ Screenshots added
- ✅ Gumroad URL updated
- ✅ Brand name updated
- ✅ Tested on mobile
- ✅ All buttons work
- ✅ Analytics added

**Then deploy and GO LIVE!** 🎉

---

**Version:** 2.0  
**Last Updated:** November 2025  
**Based on:** Claude landing page strategy  
**Optimized for:** Conversion and mobile performance
