---
title: Landing Page Branch Strategy
---

This document summarizes options and immediate steps for keeping the landing page isolated from the main app codebase while continuing launches and development.

## Goal

Keep `main` focused on the desktop app and backend. Maintain `landing-page` branch (or separate repo) for the landing site, preview deploys, and marketing assets.

## Why

- Branches share history; landing files added on `main` will remain on other branches unless changed.

- We want to minimize accidental adds to `main` from `landing-page` work and avoid heavy artifacts getting tracked.

## Short-term recommendation (safe and reversible)
1. Add patterns to `.gitignore` on `main` to prevent future accidental additions of landing files and deploy artifacts (done with this commit).

2. If landing files are still tracked on `main` and you want them removed from `main`:

   - Untrack them without deleting the files locally:

     ```bash
     # on the `main` branch
     git checkout main
     git pull origin main
     git rm -r --cached web/claude_landing_page_v2
     git rm -r --cached deploy_dist
     git commit -m "Untrack landing site files from main (moved to landing-page branch)"
     git push origin main
     ```

3. Verify `landing-page` branch still contains the folder and history:

   ```bash
   git checkout landing-page
   git pull origin landing-page
   git log -- web/claude_landing_page_v2
   ```

4. If you have a CI/CD or `wrangler` deploy that pulls from `main`, update it to either:

   - Deploy from `landing-page` for Pages previews, or
   - Use a separate repository for the landing site (see next section).

## Mid-term recommendation (clean history & separation)
1. Create a new repo for the landing site (e.g., `signkit-landing`) and preserve history via `git subtree split`:

   ```bash
   git subtree split --prefix=web/claude_landing_page_v2 -b landing-only
   git remote add landing-repo git@github.com:pranaysuyash/signkit-landing.git
   git push landing-repo landing-only:main
   ```

2. Remove the folder from `main` and optionally add it as a submodule:

   ```bash
   git checkout main
   git rm -r --cached web/claude_landing_page_v2
   git commit -m "Remove landing site from main; use landing repo instead"
   git push origin main

   # add submodule if you want to keep the folder structure
   git submodule add git@github.com:pranaysuyash/signkit-landing.git web/claude_landing_page_v2
   git commit -m "Add signkit landing as submodule"
   git push origin main
   ```

3. Alternatively keep the `landing-page` branch if a separate repo is not desired:

   ```bash
   git subtree split --prefix=web/claude_landing_page_v2 -b landing-only
   git branch -M landing-only landing-page
   git push origin landing-page --force
   ```

## Automations / Safety

- Add a `pre-commit` or `pre-push` hook on `main` to prevent adding `web/claude_landing_page_v2` to `main` accidentally.
- Use `git add -n -A` or `git status -s` to preview changes before adding.
- To untrack a tracked file/directory you must `git rm --cached <path>` and commit; `.gitignore` does not untrack already tracked files.

### Example `pre-commit` snippet

Add a `pre-commit` file under `.git/hooks/` (not committed) that `exit 1` if landing files are being added on `main`:

```bash
# .git/hooks/pre-commit (make executable)
branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$branch" = "main" ]; then
  if git diff --cached --name-only | grep -q "web/claude_landing_page_v2"; then
    echo "Error: Landing page files should not be added to main. Use landing-page branch or landing repo."
    exit 1
  fi
fi
```

## Notes

- We're intentionally adding `web/claude_landing_page_v2` to `.gitignore` on the `main` branch; the landing files will still exist on `landing-page` and the submodule/repo (if you create one).
- If you want me to implement any of the mid-term changes (split into repo and submodule), I can do that next — but they change repo history and require careful coordination.

## Questions / next steps

- Should I untrack files from `main` now (using `git rm --cached`) or only add `.gitignore` and leave tracked files on `main` for now?
- Do we want to split to a new repo now, or keep `landing-page` as the isolated branch for now?
Additional: Test artifacts to ignore
----------------------------------

If your e2e tests or test artifacts are producing large files, add them to `.gitignore` (e.g., `tests/e2e/`) and use `git rm --cached` on main to untrack them. This prevents staging or pushing test output to `main` accidentally.

If you prefer to keep test source files in the repo but ignore the heavy test output, add patterns specifically for those outputs (logs, screenshots): `tests/e2e/screenshots/`, `tests/e2e/reports/`, etc.
-----

