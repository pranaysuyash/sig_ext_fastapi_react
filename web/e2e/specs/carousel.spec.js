const { test, expect } = require('@playwright/test');

const BASE = 'http://localhost:8080';

test.describe('Carousel demo', () => {
  test('carousel dots should change active slide on click', async ({ page }) => {
    await page.goto(BASE + '/purchase.html');

    const dots = page.locator('.demo-dot');
    await expect(dots.first()).toBeVisible();

    // Get number of dots
    const dotCount = await dots.count();
    expect(dotCount).toBeGreaterThan(1);

    // Click second dot
    await dots.nth(1).click();

    // The second step should be active
    const steps = page.locator('.demo-step');
    const activeIndex = await steps.evaluateAll(nodes => nodes.findIndex(n => n.classList.contains('active')));
    expect(activeIndex).toBeGreaterThanOrEqual(0);

    const activeStep = steps.nth(activeIndex);
    await expect(activeStep).toBeVisible();

    // Ensure analytics snippet exists on the page
    const html = await page.content();
    expect(html).toContain('G-PCJDGBMRRN');
    expect(html).toContain('web/claude_landing_page_v2/js/analytics.js');
    expect(html).toContain('u8zyh41jr0');
  });
});
