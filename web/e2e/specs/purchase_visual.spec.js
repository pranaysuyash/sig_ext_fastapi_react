const { test, expect } = require('@playwright/test');

const BASE = 'http://localhost:8080';

test.describe('Purchase page visual checks', () => {
  test('purchase page desktop visual (snapshot)', async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 900 });
    await page.goto(BASE + '/purchase');
    // Wait for page network activity to finish
    await page.waitForLoadState('networkidle');
    const screenshot = await page.screenshot({ fullPage: true });
    expect(screenshot).toMatchSnapshot('purchase-desktop.png', { maxDiffPixelRatio: 0.02 });
  });

  test('purchase page mobile visual (snapshot)', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 900 });
    await page.goto(BASE + '/purchase');
      await page.waitForLoadState('networkidle');
    const screenshot = await page.screenshot({ fullPage: true });
    expect(screenshot).toMatchSnapshot('purchase-mobile.png', { maxDiffPixelRatio: 0.02 });
  });
});
