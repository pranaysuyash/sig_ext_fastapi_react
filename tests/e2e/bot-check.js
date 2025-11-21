const puppeteer = require('puppeteer');
(async () => {
  const headless = process.env.HEADLESS === 'false' ? false : true;
  const browser = await puppeteer.launch({
    headless: headless,
    args: ['--no-sandbox', '--disable-blink-features=AutomationControlled'],
  });
  try {
    const page = await browser.newPage();
    await page.setUserAgent('Googlebot/2.1 (+http://www.google.com/bot.html)');
    await page.evaluateOnNewDocument(() => {
      window._dl = [];
      window.dataLayer = window.dataLayer || [];
      const origPush = window.dataLayer.push.bind(window.dataLayer);
      window.dataLayer.push = (...args) => {
        try {
          window._dl.push(args);
        } catch {}
        return origPush(...args);
      };
    });
    await page.goto('https://d96d3e5a.signkit-landing.pages.dev/purchase', {
      waitUntil: 'domcontentloaded',
    });
    await new Promise((resolve) => setTimeout(resolve, 500));
    const calls = await page.evaluate(() => window._dl || []);
    console.log(
      'Bot environment dataLayer calls:',
      JSON.stringify(calls, null, 2)
    );
    const events = (calls || [])
      .map((f) => {
        const arg0 = f[0];
        if (Array.isArray(arg0) && arg0[0] === 'event') return arg0[1];
        // If the array is converted to an object during JSON transport it may look like { '0': 'event', '1': 'bot_detected' }
        if (arg0 && (arg0[0] === 'event' || arg0['0'] === 'event'))
          return arg0[1] || arg0['1'];
        if (arg0?.event) return arg0.event;
        return null;
      })
      .filter(Boolean);
    console.log('Events found (bot):', events);
    process.exit(0);
  } catch (e) {
    console.error(e);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
