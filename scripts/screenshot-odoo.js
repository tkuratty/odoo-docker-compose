const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  
  // Odoo初期画面（DB作成画面）
  console.log('Accessing Odoo setup page...');
  await page.goto('http://localhost:18069', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(3000);
  
  // スクリーンショット保存先
  const screenshotDir = '/home/ratty/.openclaw/workspace/workspace/odoo-docker-compose/docs/assets';
  if (!fs.existsSync(screenshotDir)) {
    fs.mkdirSync(screenshotDir, { recursive: true });
  }
  
  // 初期画面のスクリーンショット
  await page.screenshot({ 
    path: path.join(screenshotDir, 'odoo-setup-page.png'),
    fullPage: true 
  });
  console.log('✓ Screenshot saved: odoo-setup-page.png');
  
  // タイトルを取得
  const title = await page.title();
  console.log('Page title:', title);
  
  // ページ内容を確認
  const content = await page.content();
  if (content.includes('database')) {
    console.log('✓ Database creation page detected');
  }
  
  await browser.close();
  console.log('Screenshot capture completed!');
})();
