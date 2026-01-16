# Landing Deployment Process (Static Multi-Page)

## Goal
Deploy a **static multi-page** marketing site with clean URLs and 4 A/B variants:

- `/root` → `root.html` (control)
- `/buy` → `buy.html` (embedded checkout)
- `/purchase` → `purchase.html` (SaaS landing)
- `/gum` → `gum.html` (redirect)

Supporting pages:

- `/` → `index.html` (entry + optional traffic split via `AUTO_SPLIT`)
- `/test-variants` → `test-variants.html` (QA dashboard)
- `/robots.txt` and `/sitemap.xml` must be real files at the site root.

## Source Of Truth
The deployable landing site is the **repo root**:

- `index.html`, `root.html`, `buy.html`, `purchase.html`, `gum.html`, `test-variants.html`
- `robots.txt`, `sitemap.xml`, `404.html`
- assets referenced by the HTML (notably `assets/` and `web/live/`)

## Cloudflare Pages Settings (Required)
In Cloudflare Pages project settings:

- **Framework preset:** None
- **Build command:** (empty)
- **Build output directory:** `/` (root)
- **Single-page application (SPA) fallback:** **OFF**
  - If SPA fallback is ON, unknown paths (and sometimes `sitemap.xml`) can incorrectly return HTML instead of proper file content.

Cloudflare handles extensionless URLs natively:

- `/purchase.html` → `/purchase` (canonical)
- `/test-variants.html` → `/test-variants` (canonical)

## Local QA
Run a local smoke test (serves files and checks the expected pages exist):

```bash
chmod +x scripts/test-local-landing.sh
./scripts/test-local-landing.sh
```

## Production QA
Smoke-test the deployed site:

```bash
chmod +x scripts/test-deployment.sh
./scripts/test-deployment.sh https://signkit.work
```

This validates:

- All variant routes return HTTP 200
- `robots.txt` is `text/plain`
- `sitemap.xml` is XML and starts with `<?xml`

## CI
GitHub Actions runs landing smoke tests via `.github/workflows/landing-smoke.yml`.

