const { test, expect } = require('@playwright/test');

const BASE = 'http://localhost:8080';

test.describe('Purchase page visual checks', () => {
  test('purchase page desktop visual (snapshot)', async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 900 });
    await page.goto(BASE + '/purchase');
    // Wait for main content to be visible
    await page.locator('.demo-carousel').waitFor({ state: 'visible' });
    const screenshot = await page.screenshot({ fullPage: true });
    expect(screenshot).toMatchSnapshot('purchase-desktop.png');
  });

  test('purchase page mobile visual (snapshot)', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 900 });
    await page.goto(BASE + '/purchase');
    await page.locator('.demo-carousel').waitFor({ state: 'visible' });
    const screenshot = await page.screenshot({ fullPage: true });
    expect(screenshot).toMatchSnapshot('purchase-mobile.png');
  });
});
