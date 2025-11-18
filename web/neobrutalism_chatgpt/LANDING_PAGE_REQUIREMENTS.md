# Landing Page Completion Requirements

**File:** `web/neobrutalism_chatgpt/index.html`

**Status:** Functionally complete for launch. Items below are enhancements for better discoverability and user trust.

---

## 🔴 Critical Additions

### 1. Add Support/Contact Information

Add a footer section with support email for pre-purchase questions.

**Where:** Before closing `</div>` of `.shell` div

```html
<div
  class="footer"
  style="text-align: center; margin-top: 32px; padding-top: 24px; border-top: 3px solid #111827; font-size: 0.85rem; color: #4b5563;"
>
  <p>
    © 2025 SignKit •
    <a
      href="mailto:support@signkit.work"
      style="color: #4f46e5; text-decoration: none;"
      >support@signkit.work</a
    >
    •
    <a
      href="https://signkit.work"
      style="color: #4f46e5; text-decoration: none;"
      >signkit.work</a
    >
  </p>
</div>
```

---

### 2. Add Open Graph Meta Tags

Enables rich previews when shared on social media (Twitter, LinkedIn, Facebook, etc.)

**Where:** In `<head>` section, after existing meta tags

```html
<!-- Open Graph / Social Media -->
<meta property="og:title" content="SignKit - Extract & Sign PDFs Offline" />
<meta
  property="og:description"
  content="Desktop app to extract signatures and sign PDFs offline. No cloud upload. $29 lifetime license."
/>
<meta property="og:url" content="https://signkit.work" />
<meta property="og:type" content="website" />
<meta property="og:image" content="https://signkit.work/og-image.png" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="SignKit - Extract & Sign PDFs Offline" />
<meta
  name="twitter:description"
  content="Desktop app to extract signatures and sign PDFs offline. No cloud upload. $29 lifetime license."
/>
<meta name="twitter:image" content="https://signkit.work/og-image.png" />
```

**Note:** You'll need to create an `og-image.png` (1200x630px recommended) showing the app interface or key value prop.

---

### 3. Add Favicon Links

Uses your existing icon assets from `assets/files/`

**Where:** In `<head>` section, after title

```html
<!-- Favicons -->
<link rel="icon" type="image/png" sizes="32x32" href="/assets/icon-32x32.png" />
<link rel="icon" type="image/png" sizes="16x16" href="/assets/icon-16x16.png" />
<link rel="apple-touch-icon" sizes="180x180" href="/assets/icon-180x180.png" />
```

**Action required:** Copy icon files from `assets/files/` to `web/neobrutalism_chatgpt/assets/`

---

## 🟡 Recommended Additions

### 4. Add Screenshots Section

Show actual product interface (once your 5-7 professional screenshots are ready)

**Where:** After the main grid, before footer

```html
<div class="screenshots-section" style="margin-top: 48px;">
  <h2 style="text-align: center; font-size: 2rem; margin-bottom: 24px;">
    See SignKit in action
  </h2>
  <div
    class="screenshot-grid"
    style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;"
  >
    <img
      src="/screenshots/main-interface.png"
      alt="SignKit main interface"
      style="width: 100%; border-radius: 16px; border: 3px solid #111827; box-shadow: 6px 6px 0 #111827;"
    />
    <img
      src="/screenshots/signature-extraction.png"
      alt="Signature extraction"
      style="width: 100%; border-radius: 16px; border: 3px solid #111827; box-shadow: 6px 6px 0 #111827;"
    />
    <img
      src="/screenshots/pdf-signing.png"
      alt="PDF signing workflow"
      style="width: 100%; border-radius: 16px; border: 3px solid #111827; box-shadow: 6px 6px 0 #111827;"
    />
  </div>
</div>
```

---

### 5. Add FAQ Section

Address common pre-purchase questions

**Where:** After screenshots section, before footer

```html
<div class="faq-section" style="margin-top: 48px;">
  <h2 style="text-align: center; font-size: 2rem; margin-bottom: 24px;">
    Frequently Asked Questions
  </h2>
  <div style="max-width: 700px; margin: 0 auto;">
    <div
      class="faq-item"
      style="margin-bottom: 20px; padding: 16px; background: #fff; border-radius: 16px; border: 3px solid #111827; box-shadow: 4px 4px 0 #111827;"
    >
      <h3 style="font-size: 1.1rem; margin-bottom: 8px;">
        What platforms does SignKit support?
      </h3>
      <p style="color: #4b5563; font-size: 0.9rem;">
        SignKit runs on macOS (Intel & ARM64), Windows, and Linux. Download the
        version for your platform from Gumroad after purchase.
      </p>
    </div>

    <div
      class="faq-item"
      style="margin-bottom: 20px; padding: 16px; background: #fff; border-radius: 16px; border: 3px solid #111827; box-shadow: 4px 4px 0 #111827;"
    >
      <h3 style="font-size: 1.1rem; margin-bottom: 8px;">
        Is there a subscription or is it really one-time?
      </h3>
      <p style="color: #4b5563; font-size: 0.9rem;">
        It's truly one-time payment. $29 gets you lifetime access with future
        minor updates included. No recurring charges.
      </p>
    </div>

    <div
      class="faq-item"
      style="margin-bottom: 20px; padding: 16px; background: #fff; border-radius: 16px; border: 3px solid #111827; box-shadow: 4px 4px 0 #111827;"
    >
      <h3 style="font-size: 1.1rem; margin-bottom: 8px;">
        Does it work completely offline?
      </h3>
      <p style="color: #4b5563; font-size: 0.9rem;">
        Yes! SignKit is a desktop app that runs 100% offline. Your PDFs and
        signatures never leave your machine. No internet connection required
        after installation.
      </p>
    </div>

    <div
      class="faq-item"
      style="margin-bottom: 20px; padding: 16px; background: #fff; border-radius: 16px; border: 3px solid #111827; box-shadow: 4px 4px 0 #111827;"
    >
      <h3 style="font-size: 1.1rem; margin-bottom: 8px;">
        What if I need a refund?
      </h3>
      <p style="color: #4b5563; font-size: 0.9rem;">
        All purchases are processed through Gumroad which offers buyer
        protection. Contact
        <a href="mailto:support@signkit.work" style="color: #4f46e5;"
          >support@signkit.work</a
        >
        if you have issues.
      </p>
    </div>
  </div>
</div>
```

---

### 6. Add Analytics Tracking (Optional but recommended)

Track page views and conversion metrics

**Where:** Before closing `</body>` tag

**Option A: Plausible (privacy-friendly, recommended)**

```html
<script
  defer
  data-domain="signkit.work"
  src="https://plausible.io/js/script.js"
></script>
```

**Option B: Google Analytics**

```html
<!-- Google tag (gtag.js) -->
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

---

## 🟢 Nice-to-Have (Post-Launch)

### 7. Testimonials Section

Add after you get initial customers

```html
<div class="testimonials-section" style="margin-top: 48px; text-align: center;">
  <h2 style="font-size: 2rem; margin-bottom: 24px;">What users are saying</h2>
  <!-- Add customer testimonials here -->
</div>
```

---

### 8. Platform Download Badges

Show clear platform support

**Where:** Below hero actions

```html
<div style="margin-top: 12px; display: flex; gap: 8px; align-items: center;">
  <span style="font-size: 0.8rem; color: #4b5563;">Available for:</span>
  <div style="display: flex; gap: 6px;">
    <span
      class="badge"
      style="font-size: 0.7rem; padding: 4px 8px; border-radius: 999px; border: 2px solid #111827; background: #ffffff;"
      >🍎 macOS</span
    >
    <span
      class="badge"
      style="font-size: 0.7rem; padding: 4px 8px; border-radius: 999px; border: 2px solid #111827; background: #ffffff;"
      >🪟 Windows</span
    >
    <span
      class="badge"
      style="font-size: 0.7rem; padding: 4px 8px; border-radius: 999px; border: 2px solid #111827; background: #ffffff;"
      >🐧 Linux</span
    >
  </div>
</div>
```

---

## 📝 Assets Still Needed

1. **Screenshots** (5-7 images at 1200x800px minimum)

   - Main interface with signature library
   - Before/after signature extraction
   - PDF signing workflow
   - Export options screen
   - License activation screen

2. **Open Graph image** (`og-image.png` at 1200x630px)

   - Should show app interface or key value proposition
   - Will be displayed when page is shared on social media

3. **Favicon files** (copy from `assets/files/` to `web/neobrutalism_chatgpt/assets/`)
   - icon-16x16.png
   - icon-32x32.png
   - icon-180x180.png

---

## 🚀 Launch Readiness

**Current status:** Page is **functionally complete** and ready for soft launch.

**Priority order for enhancements:**

1. Add footer with support email (5 minutes) ← **Do this first**
2. Add Open Graph meta tags (5 minutes)
3. Add favicon links + copy icon files (10 minutes)
4. Add screenshots section once screenshots are ready (15 minutes)
5. Add FAQ section (20 minutes)
6. Add analytics tracking (10 minutes)
7. Everything else post-launch

**Total time to make page production-ready:** ~30-40 minutes (excluding screenshot creation)
