from playwright.sync_api import sync_playwright
import time
import os

USER_DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".whatsapp_session")
os.makedirs(USER_DATA_DIR, exist_ok=True)

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-setuid-sandbox",
        ],
        ignore_default_args=["--enable-automation"],
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
    page = context.pages[0] if context.pages else context.new_page()
    print("Navigating to web.whatsapp.com...")
    page.goto("https://web.whatsapp.com", timeout=60000)
    print("Page title:", page.title())
    
    for i in range(15):
        time.sleep(2)
        print(f"[{i*2}s] URL:", page.url)
        print("Canvas count:", page.locator('canvas').count())
        print("Data-ref count:", page.locator('div[data-ref]').count())
        print("Data-testid qrcode count:", page.locator('div[data-testid="qrcode"]').count())
        print("Logged in selectors count (#pane-side):", page.locator('#pane-side').count())
        if page.locator('canvas').count() > 0:
            print("FOUND CANVAS! Screenshotting...")
            page.locator('canvas').first.screenshot(path="test_qr_out.png")
            print("Screenshot saved to test_qr_out.png")
            break
        if page.locator('#pane-side').count() > 0:
            print("ALREADY LOGGED IN!")
            break
    context.close()
