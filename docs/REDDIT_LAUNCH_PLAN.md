# Reddit & Indie Launch Plan — SignKit

This document contains the launch plan, post templates, assets checklist, posting timing, follow-up plan, and KPIs for launching SignKit on Reddit and Indie communities.

---

## TL;DR Checklist

- Verify live deploy (signkit.work, `web/live`) and demo pages working.
- Create assets: hero, 3 feature screenshots, demo GIF, short video.
- UTM-tag demo and landing links for tracking (e.g., `?utm_source=reddit&utm_medium=post&utm_campaign=launch`).
- Draft 3 copies for r/SideProject, r/IndieHackers, and Product Hunt.
- Post at recommended timings; answer comments for first several hours.
- Gather feedback and post update after 24–48 hours.

---

## Goals & Messaging

- Product: SignKit — a privacy-first, local macOS tool to extract signatures from PDFs and place them onto PDF pages.
- Target audience: indie devs, small teams, professionals who handle PDFs & signatures and care about privacy.
- Key message: local processing (no uploads), fast extraction, simple workflow (upload → crop → place), and a small friction-free UX.

---

## Image & Media Assets Checklist

- [ ] Hero screenshot: `hero-1200x675.png` (16:9)
- [ ] Feature screenshot 1: `step-upload-1200x675.png` (upload UI)
- [ ] Feature screenshot 2: `step-select-1200x675.png` (select & crop signature)
- [ ] Feature screenshot 3: `step-place-1200x675.png` (place signature on target PDF)
- [ ] Demo GIF: `demo-8s.webm` or `demo-8s.gif` (upload → select → place) — under 5MB if GIF
- [ ] Short video: `demo-20s.mp4` (20–30s for a clearer flow)
- [ ] Optional: before/after side-by-side, product badge icons

### ALT TEXT / Naming

- Always include alt text for images (e.g., "SignKit: upload PDF and the app detects signatures; crop and place on another PDF").
- Preferred formats: WebP or PNG for images; WebM/MP4 for video.

### Compression & File Size

- Aim for <200–300 KB per screenshot where possible.
- Use modern formats (WebP) when supported; keep GIFs small.
- Tools: `pngquant`, `cwebp`, `ffmpeg` for video/gif encoding.

---

## Post Copy Templates

### r/SideProject — short and friendly

**Title ideas:**

- "SignKit — extract & reuse signatures locally (macOS) — feedback welcome"
- "Launched SignKit: offline signatures from PDFs — try & comment"

**Body:**

> Hi everyone — I built SignKit, a macOS app that extracts signatures from scanned or image-based PDFs locally and lets you place the signature in other PDFs quickly.
>
> - Why: I needed a privacy-first tool that doesn't upload my documents.
> - How: drag & drop → select signature → crop/clean → place on PDF.
> - Try it (demo + landing): https://signkit.work/purchase?utm_source=reddit&utm_medium=post&utm_campaign=sideproject-launch
>   Screenshots + demo GIF attached — feedback would be much appreciated!
>   Note: I’m specifically looking for: integration suggestions, pricing feedback, and use cases.

### r/IndieHackers — traction & pricing focused

**Title ideas:**

- "SignKit — privacy-first, offline PDF signature extraction (macOS) — pricing + distribution feedback"

**Body:**

> Hi IH — I'm Pranay, and I launched SignKit — a local macOS app for extracting & placing signatures on PDFs. No uploads.
>
> - Problem/market: businesses with forms & signatures want a private, efficient tool for routine PDF work.
> - Basic model: free trial + $X one-time / $Y yearly / or tiered business pricing.
> - Demo: https://signkit.work/purchase?utm_source=indiehackers&utm_medium=post&utm_campaign=launch
>   I’d love pricing and distribution feedback: one-time vs subscription vs enterprise? Thank you!

### Product Hunt / Launch day copy (if launching there)

- Make sure to read Product Hunt rules; they are more formalized and require a dedicated product page with assets.
- Keep a short tagline & a friendly voice, ask hunters to upvote and give feedback.

---

## Example Social Post Structure

- Title (short, attention-grabbing)
- One short paragraph: problem & what SignKit does
- One line: CTA (try, demo, or sign up)
- Attach hero image + 1–3 screenshots + GIF/video
- Ask for feedback and a single question (e.g., pricing preference)
- Pin answer & link to site and a schedule for follow-up

---

## Posting Timing & Strategy

- r/SideProject: Sunday evening or Monday morning local time works well.
- r/IndieHackers: Weekdays 09:00–11:00 local time (preferably Tue/Fri).
- Product Hunt: schedule a “launch day”; coordinate with social announcements.
- Best practice: schedule posts to go live within 30 minutes of peak times and be online to answer comments for first 4 hours.

---

## Follow-up Plan

- T+0: Monitor & respond to comments for 1–2 hours intensively.
- T+24: Post update summary (metrics, top feedback, actions planned).
- T+48: Revisit feature requests and bug reports; triage and plan backlog.
- Use upvotes & comments as early validation and track download/visit metrics.

---

## Analytics & Tracking

- Add UTM parameters to all shared links (reddit, indiehackers, PH, tweets): `?utm_source=reddit&utm_medium=post&utm_campaign=sideproject-launch`
- Watch: landing page visits, trial signups, clicks on demo, conversion to paid, retention.
- Use GA & Clarity (we already added these, verify the event for CTA clicks).

---

## KPIs to Track (30-day window)

- Unique visitors from Reddit posts
- Trial signups & downloads originating from UTM tag
- CTR of demo video and clicks to download
- Conversion rate (trial → paid)
- Feedback comments & requests count

---

## Release Day War Room Checklist (Copy/paste)

- [ ] Start server locally and test the demo flow quickly: `python serve.py`
- [ ] Verify landing page is working: `https://signkit.work` and UTM parameters are correct.
- [ ] Upload images, video, and GIFs; verify previews.
- [ ] Prepare a pinned comment draft that invites feedback and lists what you want to learn.
- [ ] Post to r/SideProject (fast reply cadence first two hours).
- [ ] Post to r/IndieHackers 1–3 hours later to stagger engagement.
- [ ] Monitor crashes, console logs, or site performance issues.
- [ ] Respond in the comments first, then move to private messages only on request.

---

## Avoid These Mistakes

- Don’t post as a pure sales post — phrase asking for feedback first.
- Don’t cross-post identical content to multiple subreddits simultaneously.
- Don’t post heavy GIFs or video that take long to load (limit to <5MB as GIF).
- Don’t post to a subreddit that forbids self-promotion without community engagement.

---

## Optional: Visual Snapshot Approach for Reddit

- Attach a lightweight GIF for immediate context; add full video link in first comment.
- Use a hero image of the app with minimal UI elements visible.
- Never include personally identifiable data in screenshots.

---

## Final Notes & Suggested Workflow

1. Prepare assets and add them to `web/live/assets/screenshots/` — ensure consistent filenames.
2. Add UTM parameters to your shared link and make sure analytics capture the event.
3. Schedule posts for r/SideProject and r/IndieHackers according to the timing above.
4. Reply to comments quickly and use the
