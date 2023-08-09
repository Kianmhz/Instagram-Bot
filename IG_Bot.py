from playwright.sync_api import sync_playwright
import os
import time


USERNAME = os.getenv('MY_USERNAME')  # replace with your environment variable for username
PASSWORD = os.getenv('MY_PASSWORD')  # replace with your environment variable for password

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir="C:\\Users\\kianm\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 5",
        headless=False,
    )

    page = context.new_page()

    page.goto("https://www.instagram.com/accounts/login/")

    # checking if we are on the login page

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


    def upload_photo(file_path):
        page.query_selector("span:has-text('Create')").click()

        time.sleep(5)

        page.set_input_files('xpath=//input[@class="_ac69" and @type="file" and @accept="image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime"]', file_path)

    upload_photo("C:\\Users\\kianm\\Desktop\\test.jpg")   # replace with your file path


    time.sleep(500)