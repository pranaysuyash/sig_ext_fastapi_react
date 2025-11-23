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
    expect(gridTemplate).toMatch(/2fr/);

    // Verify that social icons exist
    const social = await footerContent.locator('.social-icons');
    await expect(social).toBeVisible();
  });
});
