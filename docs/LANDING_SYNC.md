# Landing Page Workflow: Keep landing-page branch as Dev, sync to main

This document explains the recommended process to keep the `landing-page` branch as the working branch for marketing and A/B testing while ensuring the `main` branch contains a canonical `web/live` copy used for production staging and audits.


## Goals
 
- Keep `landing-page` as the active development branch for landing and analytics work.
- Keep `main` clean, with landing content stored under `web/live` and essential root pages (index, buy, purchase, gum, root).
- Make it easy to update `main` from `landing-page` without merging the entire branch.


## Recommended Sync Process

1. On a clean working tree, switch to `main`:
   
   ```bash
   git checkout main
   git fetch origin
   git reset --hard origin/main
   ```

2. Pull `web/live` and root pages from the `landing-page` branch (or whichever feature branch you're working on):
   
   ```bash
   # Bring the latest landing output into main
   git checkout landing-page -- web/live
   # Root-level pages that are variants
   git checkout landing-page -- index.html buy.html purchase.html gum.html root.html
   ```

3. Review the changes, adjust asset paths if necessary (e.g., ensure references to `web/live/...` are used), then commit and push:
   
   ```bash
   git add web/live index.html buy.html purchase.html gum.html root.html
   git commit -m "chore(main): sync landing-page (web/live and root pages)"
   git push origin main
   ```

4. If you use any deployment scripts or CI (e.g., Cloudflare pages), update them to use `web/live` or use `main` as the production branch as appropriate.



## Notes and Best Practices
 
- Prefer `git checkout branch -- <path>` to avoid merge conflicts arising from rename/rename (e.g., `web/claude_landing_page_v2` vs `web/live`).
- Avoid merging the entire `landing-page` into `main` unless you want to bring non-website code changes.
- Document updates to `web/live` in the `web/live/README.md` file so future editors know where to find the canonical content in `main`.
- If you expect frequent syncs, consider setting up a small automation (CI) that automatically updates `web/live/` in `main` on demand (e.g., a GitHub Action triggered by a label or a schedule).


## Example automation (optional)

Add a GitHub Action that runs on a repository dispatch event (or branch push) to sync `web/live` from `landing-page` into `main` automatically.

By following this approach you maintain `landing-page` as the dev/test zone while keeping `main` up-to-date with the canonical live site (`web/live`) and root pages.
