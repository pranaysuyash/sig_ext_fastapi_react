/** @type {import('@playwright/test').PlaywrightTestConfig} */
const config = {
  testDir: './tests',
  timeout: 30 * 1000,
  use: {
    headless: true,
    baseURL: 'http://localhost:8080',
  },
  reporter: [['list'], ['html', { open: 'never' }]],
};
module.exports = config;
