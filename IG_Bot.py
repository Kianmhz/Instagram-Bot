from playwright.sync_api import sync_playwright, BrowserType
import os
import time

width = 375
height = 812

USERNAME = os.getenv('MY_USERNAME')  # replace with your environment variable for username
PASSWORD = os.getenv('MY_PASSWORD')  # replace with your environment variable for password

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir="C:\\Users\\kianm\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 5",
        headless=False,
    )

    page = context.new_page()

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

    

    time.sleep(500)