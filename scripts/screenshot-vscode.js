const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  
  // 1. Odoo データベース管理画面
  console.log('Accessing Odoo database manager...');
  await page.goto('http://localhost:18069/web/database/manager', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(3000);
  
  const screenshotDir = '/home/ratty/.openclaw/workspace/workspace/odoo-docker-compose/docs/vscode-debug-setup/images';
  if (!fs.existsSync(screenshotDir)) {
    fs.mkdirSync(screenshotDir, { recursive: true });
  }
  
  await page.screenshot({ 
    path: path.join(screenshotDir, 'odoo-database-manager.png'),
    fullPage: true 
  });
  console.log('✓ Screenshot saved: odoo-database-manager.png');
  
  // ページタイトル確認
  const title = await page.title();
  console.log('Page title:', title);
  
  await browser.close();
  console.log('VSCode setup screenshots completed!');
})();
