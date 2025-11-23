# SignKit Landing Page - Incident & Fix Summary

Date: 2025-11-23

TL;DR

- The `web/live` folder (Cloudflare Pages deploy source) drifted out of sync with the canonical root files. Several pages were missing the Google Analytics snippet and the centralized analytics helper, and the `test-variants.html` dashboard was not present in the deployed site.

- We performed a controlled sync, backup, and redeploy of `web/live`, then added automated verification and cleanup steps to reduce the chance of future drift.

## What went wrong

- `web/live` had older or partial snapshots for `index.html`, `root.html`, and other files; some did not include the `gtag` inline snippet or the `web/claude_landing_page_v2/js/analytics.js` helper.

- `web/live` had older or partial snapshots for `index.html`, `root.html`, and other files; some did not include the `gtag` inline snippet or the `web/claude_landing_page_v2/js/analytics.js` helper.

- `test-variants.html` was missing from `web/live` and thus inaccessible on the deployed preview.

- Temporary local backup files were left inside `web/live` (e.g., `_backup_pre_sync/` and `index.claude-backup.html`) — these are safe but must be kept out of the repository.

Why it happened (probable causes)

- Manual syncing and ad-hoc deployment operations resulted in inconsistent copies of pages under `web/live`.

- A missing guard/check in the deployment process allowed the site to go live without verifying essential snippets (GA, Clarity, analytics helper).

How we handled it (step-by-step)

1.  Backed up current `web/live` pages into `web/backups/landing-page-sync-20251123/`

    - This preserves a local snapshot for any rollback or analysis; we did not commit these to git.

2.  Reconciled `web/live` with authoritative pages in the repository root.

    - Copied canonical `index.html`, `root.html`, `purchase.html`, `buy.html`, `gum.html` and `test-variants.html` into `web/live`.

3.  Validated analytics presence locally.

    - Confirmed inline GA snippet, Clarity and analytics helper are included on `index`, `root`, `purchase`, `buy`, and `gum` files.

4.  Committed changes to the `landing-page` branch with a descriptive commit message.

5.  Deployed `web/live` to Cloudflare Pages (preview) and validated the public site at `https://signkit-landing.pages.dev`.

6.  Added automated local smoke tests and CI workflow to prevent repeat issues:

    - `test-pages.sh`: now asserts 200 responses and checks for `G-PCJDGBMRRN`, `u8zyh41jr0` and the analytics helper `web/claude_landing_page_v2/js/analytics.js` in pages.

    - `.github/workflows/landing-page-smoke.yml`: runs `test-pages.sh` on pushes and PRs to `landing-page`.

7.  Moved ad-hoc backups from `web/live/_backup_pre_sync` and `web/live/index.claude-backup.html` to `web/backups/landing-page-sync-20251123/` and added `.gitignore` entries to ignore these backups going forward.

Files changed/created

- Updated: `.gitignore` — ignore `web/live/_backup_pre_sync/`, `web/live/index.claude-backup.html`, and `web/backups/*` (keep README)

- Updated: `test-pages.sh` — added `check_contains` to verify analytics presence

- New: `.github/workflows/landing-page-smoke.yml` — simple smoke-tests CI workflow

- New: `web/backups/landing-page-sync-20251123/` — local backup files (untracked)

- New: `web/backups/README.md` — explains backup policy

Smoke-test outputs (local checks)

- Ran `serve.py` locally and executed `./test-pages.sh`. The script verifies:

- Page accessibility (HTTP 200) for `/`, `/root`, `/buy`, `/purchase`, `/gum`, and `test-variants.html`.

- The presence of Google Analytics (G-PCJDGBMRRN), `web/claude_landing_page_v2/js/analytics.js`, and Clarity ID `u8zyh41jr0` on key pages.

- All tests passed locally.

Deployed checks (Cloudflare)

- Confirmed Cloudflare Pages site reachable: <https://signkit-landing.pages.dev>
- Verified these pages contain the GA property ID, Clarity ID, and the analytics helper by downloading page HTML and `grep`-ing for strings.
- All relevant pages on deployed site showed GA + analytics helper + Clarity present:
- `<https://signkit-landing.pages.dev/>` contains `G-PCJDGBMRRN` and `web/claude_landing_page_v2/js/analytics.js`.
- `<https://signkit-landing.pages.dev/purchase>` contains `G-PCJDGBMRRN`, `u8zyh41jr0`, and `web/claude_landing_page_v2/js/analytics.js`.

Manual verification checklist (what you can manually verify quickly)

- Re-deploy verification: Confirm <https://signkit-landing.pages.dev> loads and shows the root version. Use `curl` to inspect HTML at a glance:
  - Root: `curl -s <https://signkit-landing.pages.dev> | grep "G-PCJDGBMRRN"` (should show snippet)
  - Purchase: `curl -s <https://signkit-landing.pages.dev/purchase> | grep -E "G-PCJDGBMRRN|u8zyh41jr0|analytics.js"`
  - Root and buy variant: same approach as above.
- Browser-level checks:
  - In your browser dev tools, open Console and check for `dataLayer` pushes while interacting (scroll, click CTA).
  - For Playwright-like verification, run a script capturing `window.dataLayer` pushes — we used such a script during verification.
- Cloudflare Pages check:

  - Confirm the site shows a 200 status: `curl -I <https://signkit-landing.pages.dev>`.

- Roll-back & emergency restore

- If you find errors, copy the corresponding backup file from `web/backups/landing-page-sync-YYYYMMDD/` into `web/live/` and run the `wrangler pages publish web/live --project-name signkit-pages-landing --branch landing-page` command (or equivalent `wrangler pages deploy web/live --project-name signkit-pages-landing --branch landing-page` depending on your workflow).
- Alternatively, revert via git by checking out the previous commit and redeploying.

Follow-up recommendations

1. Add Playwright E2E tests in CI to verify `dataLayer` event pushes and precise event names (e.g., `real_user_detected`, `cta_click`, `purchase`) to prevent subtle functional regressions.
2. Add a pre-deploy check (script or CI step) to assert that every page in `web/live` contains `G-PCJDGBMRRN` and `web/claude_landing_page_v2/js/analytics.js`. Block deploy if checks fail.
3. Consider a regression diff-check that ensures `web/live` and canonical root HTML are in parity, or enforce `web/live` to be generated from canonical root sources programmatically.
4. Remove or standardize any inline GA/analytics movement and rely on centralized `analytics.js` to minimize duplication and lower the chance of an accidental removal somewhere.

Notes & caveats

- Cloudflare Pages may insert its own analytics beacon; that is expected behavior from the Pages platform and is not an issue to block.

- Confirm ingestion into GA servers using GA's Realtime/DebugView; we only check the `dataLayer` pushes client-side and presence of `gtag.js` on HTML.

If you want me to proceed while you manually verify:

- Add Playwright E2E test that asserts event names on manual interactions and push it behind a CI job.
- Create a pre-deploy script and add it to your deployment pipeline (e.g., `wrangler` command wrapper) for enforced checks.

If anything is missing or you want me to re-run a set of validations/Playwright scenario(s) while you confirm changes, say the word and I’ll run it now.

— End of report —
