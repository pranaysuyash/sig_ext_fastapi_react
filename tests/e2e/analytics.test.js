const puppeteer = require('puppeteer');

(async () => {
  const baseUrl = 'http://localhost:8080';
  const browser = await puppeteer.launch({ headless: true });
  try {
    const page = await browser.newPage();

    // Make the environment look less like headless/automation (simulate a normal browser)
    await page.evaluateOnNewDocument(() => {
      try { Object.defineProperty(navigator, 'webdriver', { get: () => undefined }); } catch (ex) {}
      try { Object.defineProperty(navigator, 'plugins', { get: () => [1] }); } catch (ex) {}
      window.gtagCalls = [];
    });

    // Visit the purchase variant
    await page.goto(`${baseUrl}/purchase`, { waitUntil: 'domcontentloaded' });

    // Wrap/override any real gtag with a collector and preserve original
    await page.evaluate(() => {
      const orig = window.gtag || function () {};
      window.gtagCalls = window.gtagCalls || [];
      window.gtag = function (...args) {
        try { window.gtagCalls.push(args); } catch (e) {}
        if (typeof orig === 'function') orig.apply(this, args);
      };
    });

    // Ensure hero CTA points to a Gumroad test URL to trigger purchase intent
    await page.evaluate(() => {
      const el = document.getElementById('heroCTA');
      if (el) el.setAttribute('data-href', 'https://gum.new/gum/test-product');
    });

    // Simulate a few interactions to trigger real_user_detected
    await page.mouse.move(200, 200);
    await page.mouse.move(250, 220);
    await page.mouse.down();
    await page.mouse.up();

    // Scroll to bottom to trigger scroll depth
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await new Promise((resolve) => setTimeout(resolve, 600));

    // Click the CTA that now goes to Gumroad
    const hero = await page.$('#heroCTA');
    if (hero) await hero.click();
    await new Promise((resolve) => setTimeout(resolve, 800));

    // Capture gtag calls
    const calls = await page.evaluate(() => window.gtagCalls || []);
    console.log('Captured gtag calls:', JSON.stringify(calls, null, 2));

    const events = (calls || []).filter((c) => c[0] === 'event');
    const eventNames = events.map((ev) => ev[1]);
    console.log('Events found:', eventNames);

    // Bot check: new page with a bot user-agent
    const pageBot = await browser.newPage();
    await pageBot.setUserAgent('Googlebot/2.1 (+http://www.google.com/bot.html)');
    await pageBot.evaluateOnNewDocument(() => { try { Object.defineProperty(navigator, 'webdriver', { get: () => true }); } catch (ex) {} });
    await pageBot.goto(`${baseUrl}/purchase`, { waitUntil: 'domcontentloaded' });
    // Wrap gtag for bot page too
    await pageBot.evaluate(() => {
      const orig = window.gtag || function () {};
      window.gtagCalls = window.gtagCalls || [];
      window.gtag = function (...args) { try { window.gtagCalls.push(args); } catch (e) {} if (typeof orig === 'function') orig.apply(this, args); };
    });
    await new Promise((resolve) => setTimeout(resolve, 300));
    const botCalls = await pageBot.evaluate(() => window.gtagCalls || []);
    console.log('Bot gtag calls', JSON.stringify(botCalls, null, 2));

    // Analyze events
    const containsReal = eventNames.includes('real_user_detected');
    const containsCTA = eventNames.includes('cta_click');
    const containsPurchaseIntent = eventNames.includes('purchase_intent');
    const containsScrollDepth = eventNames.includes('scroll_depth');

    console.log({ containsReal, containsCTA, containsPurchaseIntent, containsScrollDepth });

    // Expect that human scenario triggers 'real_user_detected', 'cta_click', 'purchase_intent', 'scroll_depth'
    const ok = containsReal && containsCTA && containsPurchaseIntent && containsScrollDepth;
    process.exit(ok ? 0 : 2);
  } catch (err) {
    console.error(err);
    process.exit(3);
  } finally {
    await browser.close();
  }
})();
const puppeteer = require('puppeteer');

(async () => {
  const baseUrl = 'http://localhost:8080';
  const browser = await puppeteer.launch({ headless: true });
  try {
    const page = await browser.newPage();

    // Install a gtag stub before any script runs
    await page.evaluateOnNewDocument(() => {
      window.gtagCalls = [];
      window.gtag = function () {
        try {
          window.gtagCalls.push(Array.from(arguments));
        } catch (e) {
          // ignore
        }
      };
    });

            // Make the environment look less like headless/automation
            await page.evaluateOnNewDocument(() => {
              try {
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
              } catch (ex) {}
              try {
                Object.defineProperty(navigator, 'plugins', { get: () => [1] });
              } catch (ex) {}
              window.gtagCalls = [];
            });
    await page.evaluate(() => {
      const el = document.getElementById('heroCTA');
      if (el) el.setAttribute('data-href', 'https://gum.new/gum/test-product');
    });

    // Scroll the page a bit to get scroll events
    await page.evaluate(() =>
      const browser = await puppeteer.launch({ headless: true });
    );
    // Wait for JS to settle; use a safe fallback for older Puppeteer
        // Make the environment look less like headless/automation
        await page.evaluateOnNewDocument(() => {
          window.gtagCalls = [];
          window.gtag = function () {
            try {
              window.gtagCalls.push(Array.from(arguments));
            } catch (e) {
              // ignore
            }
          };
        });
        await page.evaluateOnNewDocument(() => {
          try {
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
          } catch (ex) {}
          try {
            Object.defineProperty(navigator, 'plugins', { get: () => [1] });
          } catch (ex) {}
        });

    const calls = await page.evaluate(() => window.gtagCalls);
    console.log('Captured gtag calls\n', JSON.stringify(calls, null, 2));

    // Check for events we expect
    const events = calls.filter((c) => c[0] === 'event');
    const eventNames = events.map((e) => e[1]);

    console.log('Events found:', eventNames);

    // Bot check (simulate a bot user-agent)
    const pageBot = await browser.newPage();
    await pageBot.setUserAgent(
      'Googlebot/2.1 (+http://www.google.com/bot.html)'
    );
    await pageBot.evaluateOnNewDocument(() => {
      window.gtagCalls = [];
      window.gtag = function () {
        window.gtagCalls.push(Array.from(arguments));
      };
    });
    await pageBot.goto(`${baseUrl}/purchase`, {
        const calls = await page.evaluate(() => window.gtagCalls || []);
    });
            // Prevent bot environment masking - keep navigator.webdriver true to simulate bot
            await pageBot.evaluateOnNewDocument(() => {
              try {
                Object.defineProperty(navigator, 'webdriver', { get: () => true });
              } catch (ex) {}
              window.gtagCalls = [];
            });
    // Return results via process exit
    const containsReal = eventNames.includes('real_user_detected');
    const containsCTA = eventNames.includes('cta_click');
    const containsPurchaseIntent = eventNames.includes('purchase_intent');
            await new Promise((resolve) => setTimeout(resolve, 200));
        await pageBot.evaluateOnNewDocument(() => {
          window.gtagCalls = [];
          window.gtag = function () {
            try {
              window.gtagCalls.push(Array.from(arguments));
            } catch (e) {}
          };
        });
      ', purchaseIntent:',
      containsPurchaseIntent,
      ', scrollDepth:',
                // Prevent bot environment masking - keep navigator.webdriver true to simulate bot
                await pageBot.evaluateOnNewDocument(() => {
                  try {
                    Object.defineProperty(navigator, 'webdriver', { get: () => true });
                  } catch (ex) {}
                  window.gtagCalls = [];
                });
      containsCTA &&
      containsPurchaseIntent &&
      containsScrollDepth;
    process.exit(ok ? 0 : 2);
  } catch (err) {
    console.error(err);
    process.exit(3);
  } finally {
    await browser.close();
  }
})();
