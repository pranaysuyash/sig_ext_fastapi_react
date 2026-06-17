# Playwright E2E tests

Run tests:

```bash
cd web/e2e
npm install --no-audit --no-fund
npx playwright install --with-deps
npm test
```

Visual snapshot tests
---------------------

To generate/update visual baseline snapshots for Playwright tests:

```bash
cd web/e2e
npm install --no-audit --no-fund
npx playwright install --with-deps
npx playwright test --update-snapshots
```

Commit generated snapshots to the repo so CI comparisons use the baseline snapshots.
