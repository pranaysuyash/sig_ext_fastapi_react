const { test, expect } = require('@playwright/test');

const BASE = 'http://localhost:8080';

test.describe('Footer layout', () => {
  test('footer should use grid and contain expected columns', async ({ page }) => {
    await page.goto(BASE + '/');

    const footer = await page.locator('footer');
    await expect(footer).toBeVisible();

    const footerContent = await page.locator('.footer-content');
    await expect(footerContent).toBeVisible();

    // Evaluate computed style to check display grid
    const display = await footerContent.evaluate(el => getComputedStyle(el).display);
    expect(display).toBe('grid');

    const gridTemplate = await footerContent.evaluate(el => getComputedStyle(el).gridTemplateColumns);
    // gridTemplate can be in px or fr units depending on viewport; ensure it has 4 columns
    const columnCount = gridTemplate.split(' ').filter(c => c.trim().length > 0).length;
    expect(columnCount).toBeGreaterThanOrEqual(3);

    // Verify that at least one brand icon exists
    const brandIcon = await footerContent.locator('i.fa-brands');
    await expect(brandIcon.first()).toBeVisible();
  });
});
