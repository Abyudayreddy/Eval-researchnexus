import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            headless=True
        )
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()

        # Set auth and dark theme
        await page.goto('http://localhost:5173/login')
        await page.evaluate("""() => {
            localStorage.setItem('researchnexus_token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3OTE3Mjk0MDAsInN1YiI6ImRlZmF1bHRfdXNlciJ9.BXSe24841JFVnnjw5ec1ZxkfNPOvNxRm9KpmojZzJ30');
            localStorage.setItem('rn_theme', 'dark');
            document.documentElement.className = 'theme-dark';
        }""")

        # 1. Capture Settings Page (Default General tab with prominent Toolkit entry card)
        await page.goto('http://localhost:5173/settings')
        await page.wait_for_timeout(1500)
        await page.screenshot(path='scratch/qa_settings_landing_dark.png')
        print('Captured qa_settings_landing_dark.png')

        # 2. Click OPEN TOOLKIT
        btn = page.locator('button:has-text("OPEN TOOLKIT")')
        if await btn.count() > 0:
            await btn.first.click()
            await page.wait_for_timeout(1500)
            await page.screenshot(path='scratch/qa_settings_toolkit_dark.png')
            print('Captured qa_settings_toolkit_dark.png')

        # 3. Capture Literature Review Step 1 & Step 2
        await page.goto('http://localhost:5173/literature-review')
        await page.wait_for_timeout(1500)
        await page.screenshot(path='scratch/qa_litreview_step1_dark.png')
        print('Captured qa_litreview_step1_dark.png')

        # Select first 2 papers if available
        cards = page.locator('.space-y-3 > div')
        count = await cards.count()
        if count >= 2:
            await cards.nth(0).click()
            await cards.nth(1).click()
            await page.wait_for_timeout(500)

        # Click Next Step to view Step 2 (Requirements & Topics)
        next_btn = page.locator('button:has-text("Next Step")')
        if await next_btn.count() > 0 and await next_btn.is_enabled():
            await next_btn.click()
            await page.wait_for_timeout(1500)
            await page.screenshot(path='scratch/qa_litreview_step2_dark.png')
            print('Captured qa_litreview_step2_dark.png')

        await browser.close()
        print('Visual inspection complete')

asyncio.run(run())
