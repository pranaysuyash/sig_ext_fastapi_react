# Missing Assets for Landing Page

**Status:** Landing page HTML is 95% complete. Only need optimized images.

---

## ✅ Already Implemented in HTML

1. **Favicons** - ✅ Linked to `../../assets/files/` icons
2. **Open Graph meta tags** - ✅ Complete (need og-image.png)
3. **Footer with support** - ✅ support@signkit.work + signkit.work
4. **Platform badges** - ✅ macOS, Windows, Linux
5. **Screenshots section** - ✅ HTML structure ready
6. **FAQ section** - ✅ 4 questions answered
7. **Testimonials placeholder** - ✅ Post-launch section
8. **Analytics** - ✅ Plausible tracking configured

---

## 🔴 CRITICAL: Missing Images

### 1. Open Graph Image (og-image.png)

**Purpose:** Shows when page is shared on Twitter, LinkedIn, Facebook, etc.

**Specs:**

- Size: 1200x630px
- Format: PNG or JPG
- Max file size: <500KB
- Location: `web/neobrutalism_chatgpt/og-image.png`

**Content suggestion:**

- Take one of your best screenshots (e.g., `13_14_library_20251114_233442.png` showing signature library)
- Add text overlay: "SignKit - Extract & Sign PDFs Offline"
- Add pricing: "$29 - Lifetime License"
- Use neobrutalism style (black borders, bold colors)

---

### 2. Screenshot Images for Product Page

**Current issue:** Screenshots in `screenshots_final/` are 20MB each (too large for web!)

**Required images** (optimized for web):

1. `main-interface.png` - Main app window with signature library
   - Suggested source: `13_14_library_20251114_233442.png`
   - Specs: 1200x800px, <300KB
2. `signature-extraction.png` - Before/after signature extraction
   - Suggested source: `10_11_result_20251114_233437.png`
   - Specs: 1200x800px, <300KB
3. `pdf-signing.png` - PDF signing workflow
   - Suggested source: `17_18_pdf_workflow_20251114_233448.png`
   - Specs: 1200x800px, <300KB

**Location:** `web/neobrutalism_chatgpt/screenshots/`

---

## 📋 Action Items

### Step 1: Optimize Screenshots (REQUIRED)

```bash
# Create screenshots directory
mkdir -p web/neobrutalism_chatgpt/screenshots

# Use ImageMagick or Python PIL to resize and compress:
# Target: 1200x800px, quality 85%, <300KB each

# Example with ImageMagick:
magick screenshots_final/13_14_library_20251114_233442.png \
  -resize 1200x800 \
  -quality 85 \
  web/neobrutalism_chatgpt/screenshots/main-interface.png

magick screenshots_final/10_11_result_20251114_233437.png \
  -resize 1200x800 \
  -quality 85 \
  web/neobrutalism_chatgpt/screenshots/signature-extraction.png

magick screenshots_final/17_18_pdf_workflow_20251114_233448.png \
  -resize 1200x800 \
  -quality 85 \
  web/neobrutalism_chatgpt/screenshots/pdf-signing.png
```

**Alternative (Python script):**

```python
from PIL import Image
import os

screenshots = [
    ("screenshots_final/13_14_library_20251114_233442.png", "main-interface.png"),
    ("screenshots_final/10_11_result_20251114_233437.png", "signature-extraction.png"),
    ("screenshots_final/17_18_pdf_workflow_20251114_233448.png", "pdf-signing.png"),
]

os.makedirs("web/neobrutalism_chatgpt/screenshots", exist_ok=True)

for src, dest in screenshots:
    img = Image.open(src)
    img.thumbnail((1200, 800), Image.Resampling.LANCZOS)
    img.save(f"web/neobrutalism_chatgpt/screenshots/{dest}", "PNG", optimize=True, quality=85)
    print(f"✓ Created {dest}")
```

---

### Step 2: Create OG Image (REQUIRED)

Use Canva, Figma, or Photoshop to create 1200x630px social card:

**Template:**

1. Background: #f5f5f5 (match landing page)
2. Add screenshot of app (signature library view)
3. Text overlay:
   - "SignKit" (bold, 72pt)
   - "Extract & Sign PDFs Offline" (48pt)
   - "$29 - Lifetime License" (36pt)
4. Add neobrutalism elements: black borders (3px), shadow effects
5. Save as `web/neobrutalism_chatgpt/og-image.png`

**Quick option:** Use your app icon + text:

```python
from PIL import Image, ImageDraw, ImageFont

# Create 1200x630 canvas
img = Image.new('RGB', (1200, 630), color='#f5f5f5')
draw = ImageDraw.Draw(img)

# Add app icon
icon = Image.open('assets/files/signkit_icon_256x256.png')
icon = icon.resize((200, 200))
img.paste(icon, (100, 215), icon if icon.mode == 'RGBA' else None)

# Add text (you'll need to load fonts or use default)
# draw.text((350, 250), "SignKit", fill='#111827', font=...)
# draw.text((350, 320), "Extract & Sign PDFs Offline", fill='#4b5563', font=...)

img.save('web/neobrutalism_chatgpt/og-image.png', quality=90)
```

---

### Step 3: Update Image Paths in HTML (if needed)

Once images are created, verify paths in index.html:

- Line ~769: `src="screenshots/main-interface.png"`
- Line ~789: `src="screenshots/signature-extraction.png"`
- Line ~809 (approx): Check if PDF signing screenshot is referenced

---

## 🎯 Priority

**CRITICAL (blocks launch):**

1. ❌ Optimize 3 screenshots (20MB → <300KB each)
2. ❌ Create OG image (1200x630px)

**OPTIONAL (post-launch):**

- Add more screenshots to gallery
- Create animated GIF demo
- Add customer testimonials section

---

## 📊 Current Status

| Asset                   | Status      | Priority     | Time Est. |
| ----------------------- | ----------- | ------------ | --------- |
| Favicons                | ✅ Complete | High         | 0 min     |
| Open Graph tags         | ✅ Complete | High         | 0 min     |
| OG Image                | ❌ Missing  | **CRITICAL** | 15 min    |
| Screenshots (optimized) | ❌ Missing  | **CRITICAL** | 10 min    |
| Footer                  | ✅ Complete | High         | 0 min     |
| Platform badges         | ✅ Complete | Medium       | 0 min     |
| FAQ section             | ✅ Complete | Medium       | 0 min     |
| Analytics               | ✅ Complete | Low          | 0 min     |

**Total remaining work:** ~25 minutes (just image optimization)

---

## 🚀 Launch Readiness

**Without optimized images:** Can launch with placeholder/no screenshots  
**With optimized images:** 100% ready for production

**Recommendation:** Spend 25 minutes on image optimization before public launch for maximum conversion rate.
