const { test, expect } = require('@playwright/test');

const BASE = 'http://localhost:8080';

test.describe('Purchase page layout and carousel behavior', () => {
  test('footer should render as one-row grid on desktop', async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(BASE + '/purchase.html');

    const footerContent = await page.locator('.footer-content');
    await expect(footerContent).toBeVisible();

    const gridTemplate = await footerContent.evaluate(el => getComputedStyle(el).gridTemplateColumns);
    const columnCount = gridTemplate.split(' ').filter(c => c.trim().length > 0).length;
    expect(columnCount).toBeGreaterThanOrEqual(4);
  });

  test('carousel caption visible, only active slide is shown', async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(BASE + '/purchase.html');

    const steps = page.locator('.demo-step');
    const count = await steps.count();
    expect(count).toBeGreaterThan(1);

    // Find active step
    const activeSteps = await steps.evaluateAll(nodes => nodes.map(n => ({
      dataset: n.getAttribute('data-step'),
      opacity: getComputedStyle(n).opacity,
      display: getComputedStyle(n).display
    })).filter(s => parseFloat(s.opacity) > 0.5));
    expect(activeSteps.length).toBe(1);

    // Ensure caption is visible and has text
    const activeStep = page.locator('.demo-step.active');
    const caption = activeStep.locator('.demo-caption');
    await expect(caption).toBeVisible();
    const captionText = (await caption.innerText()).trim();
    expect(captionText.length).toBeGreaterThan(0);
  });

  test('carousel caption not overflowing on small viewport', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 800 });
    await page.goto(BASE + '/purchase.html');

    const activeStep = page.locator('.demo-step.active');
    const caption = activeStep.locator('.demo-caption');
    await expect(caption).toBeVisible();

    // Ensure caption bounding box height within a reasonable fraction of viewport (not covering whole view)
    const rect = await caption.boundingBox();
    expect(rect.height).toBeLessThan(200);
    expect(rect.width).toBeLessThanOrEqual(375);
    // Ensure caption does not overlap footer by checking its bottom is above footer top
    const footerTop = await page.locator('footer').evaluate(el => el.getBoundingClientRect().top);
    expect(rect.y + rect.height).toBeLessThanOrEqual(footerTop);
  });
});
