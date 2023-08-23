from playwright.sync_api import sync_playwright
import os
import time
import requests
from dotenv import load_dotenv
from random import choice, randint
import re

load_dotenv()

USERNAME = os.getenv('MY_USERNAME')  # replace with your environment variable for username
PASSWORD = os.getenv('MY_PASSWORD')  # replace with your environment variable for password

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir="C:\\Users\\kianm\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 5",  # replace with your own Chrome profile
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

        # checking if we are logged in
        try:
            page.wait_for_selector('div:has-text("Not Now")').click()
        except:
            print("login failed")


    def upload_photo(file_path):
        page.query_selector("span:has-text('Create')").click()

        time.sleep(5)

        page.set_input_files('xpath=//input[@class="_ac69" and @type="file" and @accept="image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime"]', file_path)


    def fetchPost():
        # Will pick random posts from the source and downloads it
        page.goto(f'https://t.me/meme/{randint(200, 800)}?embed=1&mode=tme')  # replace with your own source
        linkElement = page.wait_for_selector('a.tgme_widget_message_photo_wrap')  
        imageStyle = linkElement.get_attribute('style')  
        regexPattern = r"background-image:url\('(.*)'\)"  # regex pattern to extract the image url
        match = re.search(regexPattern, imageStyle)

        # Download the image
        response = requests.get(match.group(1))
        if response.status_code == 200:
            with open('image.jpg', 'wb') as file:  
                file.write(response.content)
        else:
            print('Failed to download the image')
    
    def follow():
        # Will randomly pick one of these below sources and then follow their n last followers
        follow_id_list = ["username1"]  # Replace with your list of usernames
        random_number = choice(range(len(follow_id_list)))

        page.goto(f'https://www.instagram.com/{follow_id_list[random_number]}/followers/')

        num_to_follow = randint(1, 20)

        # Locate the follow buttons and click on them
        for i in range(num_to_follow):
            follow_button = page.locator("div:has-text('Follow')")
            if follow_button:
                follow_button.click()
                time.sleep(2)  # Wait 2 seconds to avoid too quick actions

        print(f"Followed {num_to_follow} followers.")

    time.sleep(500)