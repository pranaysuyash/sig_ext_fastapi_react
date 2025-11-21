const puppeteer = require('puppeteer');

(async () => {
  const baseUrl = 'https://d96d3e5a.signkit-landing.pages.dev';
  const headless = process.env.HEADLESS === 'false' ? false : true;
  const browser = await puppeteer.launch({
    headless: headless,
    args: ['--no-sandbox', '--disable-blink-features=AutomationControlled'],
  });
  try {
    const page = await browser.newPage();
    // Override dataLayer push to capture gtag events (dataLayer used by gtag)
    await page.evaluateOnNewDocument(() => {
      try {
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
      } catch {}
      try {
        Object.defineProperty(navigator, 'plugins', { get: () => [1] });
      } catch {}
      window._dl = window._dl || [];
      window.dataLayer = window.dataLayer || [];
      // wrap push to capture events
      const origPush = window.dataLayer.push.bind(window.dataLayer);
      window.dataLayer.push = (...args) => {
        try {
          window._dl.push(args);
        } catch {}
        return origPush(...args);
      };
    });

    await page.setUserAgent(
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    );
    await page.goto(`${baseUrl}/purchase`, { waitUntil: 'domcontentloaded' });
    const heights = await page.evaluate(() => {
      return {
        scrollHeight: document.documentElement.scrollHeight,
        bodyScrollHeight: document.body.scrollHeight,
        innerHeight: window.innerHeight,
      };
    });
    console.log('Page heights:', heights);
    const scrollable = await page.evaluate(() => {
      const nodes = Array.from(document.querySelectorAll('*'));
      let candidate = null;
      nodes.forEach((n) => {
        try {
          const style = window.getComputedStyle(n);
          if (style.overflowY === 'auto' || style.overflowY === 'scroll') {
            if (!candidate || n.scrollHeight > candidate.scrollHeight)
              candidate = n;
          }
        } catch {}
      });
      if (!candidate) return null;
      return {
        selector: candidate.tagName,
        scrollHeight: candidate.scrollHeight,
        scrollTop: candidate.scrollTop,
      };
    });
    console.log('Largest scrollable element (if any):', scrollable);

    // Wrap gtag to capture calls
    await page.evaluate(() => {
      const orig = window.gtag || (() => {});
      window.gtagCalls = window.gtagCalls || [];
      window.gtag = (...args) => {
        try {
          window.gtagCalls.push(args);
        } catch {}
        if (typeof orig === 'function') orig.apply(this, args);
      };
    });

    // Interact for real-user events
    await page.mouse.move(200, 200);
    await page.mouse.move(250, 220);
    await page.mouse.down();
    await page.mouse.up();
    // Scroll in increments to trigger scroll depth events (25%, 50%, 75%, 100%)
    // Simulate natural scrolling in viewport-sized steps to ensure scroll events fire reliably
    await page
      .evaluate(() => {
        const max = document.documentElement.scrollHeight - window.innerHeight;
        const steps = Math.ceil(max / window.innerHeight) || 1;
        for (let i = 0; i <= steps; i++) {
          window.scrollBy(0, window.innerHeight);
          window.dispatchEvent(new Event('scroll'));
        }
        return Math.round((window.scrollY / max) * 100);
      })
      .then((p) => console.log('scrolled via steps ->', p));
    await new Promise((resolve) => setTimeout(resolve, 300));
    // Use mouse wheel to simulate actual user scrolling
    try {
      await page.mouse.wheel({ deltaY: 800 });
      await new Promise((resolve) => setTimeout(resolve, 200));
      await page.mouse.wheel({ deltaY: 800 });
    } catch {}
    await page.evaluate(() => {
      const height = document.body.scrollHeight - window.innerHeight;
      window.scrollTo(0, Math.floor(height * 0.5));
      window.dispatchEvent(new Event('scroll'));
    });
    await page
      .evaluate(() => {
        const height = document.body.scrollHeight - window.innerHeight;
        window.scrollTo(0, Math.floor(height * 0.25));
        window.dispatchEvent(new Event('scroll'));
        return {
          scrollY: window.scrollY,
          innerHeight: window.innerHeight,
          scrollHeight: document.documentElement.scrollHeight,
          percent: Math.round(
            (window.scrollY /
              (document.documentElement.scrollHeight - window.innerHeight)) *
              100
          ),
        };
      })
      .then((p) => console.log('scrolled to 25% ->', p));
    await new Promise((resolve) => setTimeout(resolve, 300));
    await page.evaluate(() => {
      const height = document.body.scrollHeight - window.innerHeight;
      window.scrollTo(0, Math.floor(height * 0.75));
      window.dispatchEvent(new Event('scroll'));
    });
    // Additional smooth scrolls to simulate slow reading behavior
    await page
      .evaluate(() => {
        const max = document.documentElement.scrollHeight - window.innerHeight;
        window.scrollBy(0, Math.floor(max * 0.25));
        window.dispatchEvent(new Event('scroll'));
        return Math.round((window.scrollY / max) * 100);
      })
      .then((p) => console.log('scrolled additional to ->', p));
    await page
      .evaluate(() => {
        const height = document.body.scrollHeight - window.innerHeight;
        window.scrollTo(0, Math.floor(height * 0.75));
        window.dispatchEvent(new Event('scroll'));
        return {
          scrollY: window.scrollY,
          innerHeight: window.innerHeight,
          scrollHeight: document.documentElement.scrollHeight,
          percent: Math.round(
            (window.scrollY /
              (document.documentElement.scrollHeight - window.innerHeight)) *
              100
          ),
        };
      })
      .then((p) => console.log('scrolled to 75% ->', p));
    await new Promise((resolve) => setTimeout(resolve, 300));
    await page.evaluate(() => {
      const height = document.body.scrollHeight - window.innerHeight;
      window.scrollTo(0, height);
      window.dispatchEvent(new Event('scroll'));
    });
    await page
      .evaluate(() => {
        const height = document.body.scrollHeight - window.innerHeight;
        window.scrollTo(0, height);
        window.dispatchEvent(new Event('scroll'));
        return {
          scrollY: window.scrollY,
          innerHeight: window.innerHeight,
          scrollHeight: document.documentElement.scrollHeight,
          percent: Math.round(
            (window.scrollY /
              (document.documentElement.scrollHeight - window.innerHeight)) *
              100
          ),
        };
      })
      .then((p) => console.log('scrolled to bottom ->', p));
    await new Promise((resolve) => setTimeout(resolve, 800));

    // Ensure CTA points to Gumroad and click
    await page.evaluate(() => {
      const el = document.getElementById('heroCTA');
      if (el) el.setAttribute('data-href', 'https://gum.new/gum/test-product');
    });
    const hero = await page.$('#heroCTA');
    if (hero) await hero.click();
    await new Promise((resolve) => setTimeout(resolve, 1000));

    const calls = await page.evaluate(() => window._dl || []);
    console.log(
      'Deployed site - captured gtag calls:',
      JSON.stringify(calls, null, 2)
    );
    const events = (calls || [])
      .map((frame) => frame?.[0] || frame)
      .map((obj) => {
        // obj may be an object with numeric keys (0,1,2) or have event property
        if (!obj) return null;
        if (obj[0] === 'event') return { name: obj[1], payload: obj[2] };
        if (obj.event) return { name: obj.event, payload: obj };
        return null;
      })
      .filter(Boolean);
    const eventNames = events.map((ev) => ev.name);
    console.log('Events found on deployed site:', eventNames);
    const containsReal = eventNames.includes('real_user_detected');
    const containsCTA = eventNames.includes('cta_click');
    const containsPurchaseIntent = eventNames.includes('purchase_intent');
    const containsScrollDepth = eventNames.includes('scroll_depth');
    console.log({
      containsReal,
      containsCTA,
      containsPurchaseIntent,
      containsScrollDepth,
    });
    process.exit(0);
  } catch (err) {
    console.error(err);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
