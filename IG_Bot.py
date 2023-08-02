from playwright.sync_api import sync_playwright
import os
from pathlib import Path
import json
import time

width = 375
height = 812

USERNAME = os.getenv('MY_USERNAME')  # replace with your environment variable for username
PASSWORD = os.getenv('MY_PASSWORD')  # replace with your environment variable for password

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        viewport={'width': width, 'height': height},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
    )

    page = browser.new_page()

    if Path("cookies.json").exists():
        page.context.add_cookies(json.loads(Path("cookies.json").read_text()))  # load cookies if they exist

    page.goto("https://www.instagram.com/accounts/login/")

    if "accounts/login" in page.url:
        page.fill("input[name='username']", USERNAME)
        page.fill("input[name='password']", PASSWORD)

        if page.query_selector("button:has-text('Allow essential and optional cookies')"):
            page.click("button:has-text('Allow essential and optional cookies')")
        
        page.click("button[type='submit']")

        try:
            page.wait_for_selector('div:text("Not Now")').click()
        except:
            print("login failed")

        cookies = page.context.cookies() 
        Path("cookies.json").write_text(json.dumps(cookies)) # save cookies to file if login was successful
    else:
        page.wait_for_selector('button:text("Not Now")').click()



    time.sleep(500)