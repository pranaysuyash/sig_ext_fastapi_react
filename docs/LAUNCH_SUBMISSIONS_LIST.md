# Launch Submissions Plan — BFCM (Black Friday & Cyber Monday) + Ongoing directories

This document is a prioritized list of launch and product directories, marketplaces, and community channels to submit SignKit to, plus the assets and templates to prepare. It factors in prior marketing planning in the repo and new channels discovered during research.

## Goals
- Drive revenue and purchases during Black Friday / Cyber Monday week and test variants to identify top-converting flows.
- Acquire users with low support friction and high likelihood to convert to paid.
- Keep analytics clean, track revenue reliably, and attribute correctly through server-side tracking.

## Priority matrix
- Priority A (High-impact, curated): Product Hunt, Hacker News (Show HN), BetaList, Indie Hackers.
- Priority B (Good reach, consistent): Launching Next, BetaPage, Product directories (AlternativeTo), App discovery (MacUpdate, Softpedia), newsletters.
- Priority C (Optional or niche): AppSumo (deal), Flathub / Snapcraft / Homebrew (Linux/mac packaging), directories for downloads, and specific community posts.

---

## Recommended directories & submission notes (Top to lower priority)

### 1) Product Hunt (High priority)
- Best for curated launch day visibility; high traffic and multiple triggers.
- Requirements: Product images, tagline, short description (2-3 sentences), longer description, video (optional), presale link or signup.
- Usually happens on a specific "day" — plan a launch day, gather community support and pre-committers.
- Assets:
  - 1 Hero image (880 x 440 at least), PNG
  - 3 screenshots + 1 short video or GIF (MP4/GIF)
  - Logo / favicon
  - Tagline & short pitch (one-liner), long pitch (2-3 paragraphs)
- Checklist for launch day:
  - Coordinate Makers/Supporters to upvote and comment on the first hour
  - Use PH Ship for private early support
  - Track using GA4 DebugView and Realtime; ensure `variant_view` and `checkout_intent` are logged

### 2) BetaList
- Great place for early adopters and testers; good for pre-launch and beta.
- Requirements: product description, sign-up URL, screenshots, landing page.
- Our signup (Gumroad purchase page or mailing list) is fine; ensure that a beta link is visible.
- Submission tips: BetaListers prefer early access and direct product involvement.

### 3) Hacker News (Show HN)
- Very high attention, but the community is tough; best for technical and thoughtful posts (Show HN style). Launch day recommendations:
  - Post a short write-up with key features and reasons you built SignKit.
  - Accept that traffic is unpredictable — be available to respond to comments quickly.

### 4) Indie Hackers
- Good place to ask for feedback and gather early adopters.
- Post product updates and a short launch post.

### 5) Launching Next & BetaPage
- Launching Next: everyday feature for new startups — good additional visibility after Product Hunt.
- BetaPage: great for collecting early adopters.

### 6) Reddit (r/SideProject, r/ProductHunt, r/Software, r/MacApps)
- Specific subreddits: r/SideProject, r/IndieDev, r/ProductHunt, r/MacApps, r/linux4noobs (for linux?), etc.
- Follow subreddit rules, don’t spam, keep to one well-crafted post.

### 7) Designer News, Lobsters, and relevant community forums
- Designer News (design-centric), Lobsters (tech audience).

### 8) App directories and downloads
- AlternativeTo — helpful for discovery for people who are switching (it’s an important discovery channel).
- MacUpdate, Softpedia, FileHippo — As downloadable packages are available, include listings.
- Flathub / Snapcraft / Homebrew Cask — if packaging for Linux/macOS; consider later depending on packaging status.

### 9) App deals / marketplaces (Optional)
- AppSumo — if you plan a promotion deal; requires planning and usually an editorial/approval process.
- StackSocial — marketplace listing.

### 10) PR & tech press
- TechCrunch, TheNextWeb, independent bloggers and newsletters (Hacker Newsletter, Maker-specific newsletters).
- Requires a press PR pitch, embargos, or personal relationship with writers.

---

## Assets & content checklist (standard)
- Headline / tagline (1-sentence clear positioning)
- Long description (2-3 paragraphs)
- Short pitch (1-2 lines)
- Screen shots (3+): hero, signature extraction screen, signed PDF preview
- Video/GIF: 30–60s demo (optional but recommended for Product Hunt & PH thumbnails)
- Branding: Logo (SVG / PNG), favicon
- Pricing details & CTA links: Gumroad links or coupon codes
- Contact info: support@signkit.work + social handles
- FAQs and help links: link to privacy and refund policy

---

## Submission templates

### Product Hunt Post Template (example)

Title: SignKit — Extract signatures and sign PDFs offline (privacy-first)
Tagline: Extract clean signatures from images and place them on PDFs — entirely offline, $29 one-time.

Long description:
SignKit is a small desktop app that extracts signature images and places them on PDFs — completely local, fast, and privacy-oriented. Our goal is to give professionals a low-cost, privacy-first way to sign documents without subscribing to cloud services.

Key features:
- Precision signature extraction with zoom controls
- Clean transparent PNG export
- Interactive PDF viewer and simple signing
- 30-day money-back guarantee

CTA: Try SignKit for $29 — [Gumroad link]

### BetaList & BetaPage Template
- Short pitch (1–2 lines)
- Link for signup or demo + email
- 2–3 screenshots and brief notes on what to look for

---

## Tracking & analytics notes for promotion
- Make sure `variant` is included in all events (we added cookie + variant setup in index/variants and analytics tracking centralization). This enables A/B analysis per variant.
- Use server-side webhook for purchase tracking (Gumroad webhook -> backend -> Measurement Protocol) to ensure purchases are captured even if a buyer doesn't return to the site.
- Add a UTM scheme and ensure our analytics properly maps source/medium/campaign to checkout intent/purchase events.

UTM example:
- utm_source=producthunt&utm_medium=launch&utm_campaign=bfcm2025 or utm_source=betal ist etc.

---

## Assets staging & hosting
- Place final assets in `assets/`, `screenshots/`, and `docs/` as needed. Use public preview site for screenshot links.
- Prepare a folder `assets/marketing/` with high-res screenshots, GIFs, and preview images.

## Suggested immediate tasks (next 24–48 hours)
1. Finalize the Product Hunt launch post + PH Ship plan and identify 6–10 supporters to upvote in the critical first hour.
2. Sign up and prepare a BetaList entry (pre-launch to gain early adopters).
3. Prepare Reddit / Hacker News posting texts and set owners for moderation responses.
4. Prepare server-side webhook capture and testing for purchases (Measurement Protocol) — optional but recommended.
5. Create a landing page variant that focuses on BFCM savings and provide a coupon to the Gumroad checkout.

## Tentative timeline
- Nov 21–22: Finalize assets, write launch copy, prepare Product Hunt and BetaList entries.
- Nov 23–27: Internal testing and bug fixes; finalize analytics checklists + webhooks.
- Launch window: Nov 29 – Dec 2 (Black Friday to Cyber Monday week) — staggered communications across channels.
- Post-launch analysis & scaling: Dec 3 onwards.

---

## Helpful sources & further research
- Product Hunt Checklist: (various expert guides) — we should prepare an internal checklist and identify supporters.
- BetaList submission guidelines: https://betalist.com/criteria + BetaList submit page.
- LaunchingNext: https://www.launchingnext.com/submit/
- Betapage: https://betapage.co/
- Big list of directories: Indie Hackers article listing 261 free launch platforms — review and pick the most relevant 20.

---

If you'd like, I can now:
- Create an actionable timeline & calendar with owners for each submission (who posts and when), 
- Implement a production webhook to capture Gumroad purchases and record them in GA4 server-side (Measurement Protocol) with tests,
- Draft & finalize Product Hunt & BetaList copy and social posts.

Tell me which of these you want next and I’ll start executing (create a branch and PR with docs and scripts as needed).