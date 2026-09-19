import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=".test_session",
        headless=True,
        channel="chrome",
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-infobars"
        ],
        ignore_default_args=["--enable-automation"],
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    browser.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
    page = browser.new_page()
    page.goto("https://web.whatsapp.com")
    print("Aguardando carregamento da página...")
    time.sleep(8)
    
    # Check if QR code canvas exists
    canvas = page.locator('canvas')
    print("Encontrou canvas QR Code?:", canvas.count() > 0)
    
    # Let's take a screenshot of the login screen to verify
    page.screenshot(path="login_screenshot.png")
    print("Screenshot salvo em login_screenshot.png")
    
    browser.close()
