const { test, expect } = require('@playwright/test');

test.describe('Index page visual checks', () => {
  test('index page desktop visual (snapshot)', async ({ page }) => {
    await page.goto('https://signkit.work');
    await page.waitForLoadState('networkidle');
    
    // Take full page screenshot
    await expect(page).toHaveScreenshot('index-desktop.png', {
      fullPage: true,
      animations: 'disabled',
    });
  });

  test('index page footer layout', async ({ page }) => {
    await page.goto('https://signkit.work');
    await page.waitForLoadState('networkidle');
    
    // Scroll to footer
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(500);
    
    // Check footer grid layout
    const footerContent = page.locator('.footer-content');
    await expect(footerContent).toBeVisible();
    
    // Get computed style
    const gridColumns = await footerContent.evaluate(el => 
      window.getComputedStyle(el).gridTemplateColumns
    );
    
    console.log('Footer grid-template-columns:', gridColumns);
    
    // Take screenshot of footer
    await expect(page.locator('.footer')).toHaveScreenshot('footer-section.png');
  });

  test('index page hero carousel', async ({ page }) => {
    await page.goto('https://signkit.work');
    await page.waitForLoadState('networkidle');
    
    // Check for text overflow in preview card
    const previewCard = page.locator('.preview-card');
    await expect(previewCard).toBeVisible();
    
    // Take screenshot of hero section
    await expect(page.locator('.grid').first()).toHaveScreenshot('hero-section.png');
  });
});
