# Landing Sync Checklist (post sync verification)

When a PR or commit syncs `web/live` and root pages into `main`, please verify the following items before merging or accepting the update.

Purpose: The landing branch remains the working branch for landing pages and analytics; this checklist ensures the main branch receives the right content and everything that matters for deployment is validated.

Files to check (high priority):

- `web/live/` (entire directory) — check that `index.html`, `css/`, `js/`, `assets/` exist and match the variant deployed.

- `index.html`, `buy.html`, `purchase.html`, `root.html`, `gum.html` — root-level landing pages should reference `web/live/*` where applicable.

- `web/live/js/analytics.js` — confirm analytics helper updated and contains central logic (gtag fallback, event names, UTM appenders).

- `web/live/js/main.js` — confirm interactive behavior (A/B routing, CTA handlers, demo carousel, iframe embed for buy variant).

- `web/live/css/style.css` and `web/live/css/animations.css` — CSS files should be present and match the expected variant design.

Docs & deploy to check (medium priority):

- `deploy_dist/` files (if included) — make sure deploy_dist references web/live correctly; if you keep deploy_dist in git, update references.

- `web/live/wrangler.toml` — verify project name and settings when using wrangler/Cloudflare deploys.

- `docs/LANDING_SYNC.md` and `docs/LANDING_SYNC_CHECKLIST.md` — keep docs updated if the sync process changes.

Tests & QA (optional but recommended):

- Run a static smoke test: `python3 -m http.server 8000` and visit `http://localhost:8000/index.html` and `purchase.html`.

- Verify GA4 events via browser console (Network tab collect requests) — `ab_test_impression`, `variant_view`, `purchase` events.

- Verify the `buy` iframe loads and that the CTA appends utm tags when clicking Gumroad links.

Notes for reviewers and agents:

- The landing branch (`landing-page`) remains the single source of truth for day-to-day edits and analytics work.

- Use the GitHub Action `.github/workflows/landing_sync.yml` to create PRs that update `main`. This PR is intended as an auditable review step.

- If `deploy_dist/` files are tracked and cause noise in PRs, discuss with the team whether to add them to `.gitignore` and remove them from the repo.

If you find issues, revert the PR or apply fixes in a new PR to `landing-page` and re-run the sync.
