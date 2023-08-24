from playwright.sync_api import sync_playwright
import os
from time import sleep
import requests
from dotenv import load_dotenv
from random import choice, randint, uniform
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

    page.goto("https://www.instagram.com")

    # checking if we are on the login page

    if "accounts/login" in page.url:
        page.fill("input[name='username']", USERNAME)
        sleep(uniform(2, 5))

        page.fill("input[name='password']", PASSWORD)
        sleep(uniform(2, 5))

        if page.query_selector("button:has-text('Allow essential and optional cookies')"):
            page.click("button:has-text('Allow essential and optional cookies')")
        
        page.click("button[type='submit']")

        # checking if we are logged in
        try:
            page.wait_for_selector('div:has-text("Not Now")').click()
        except:
            print("login failed")


    def upload_photo(file_path):
        # Will upload a photo to post
        page.query_selector("span:has-text('Create')").click()

        sleep(uniform(10, 15))

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

        page.goto(f'https://www.instagram.com/{follow_id_list[random_number]}/following/')

        sleep(uniform(10, 15))

        # dialog = page.query_selector("div[role='dialog'] div._aano")

        # # If the dialog is found, then scroll inside the dialog until a "Follow" button is found
        # if dialog:
        #     while not page.query_selector("div[role='dialog'] button div:text-is('Follow')"):
        #         # Scroll the dialog
        #         page.evaluate("arguments[0].scrollTop += 100", dialog)
        #         sleep(1)  # Allow for potential loading

        # Locate the follow buttons
        follow_buttons = page.query_selector_all("div[role='dialog'] button div:text-is('Follow')")
        num_to_follow = randint(1, 9)

        # Follow random number of accounts
        for button in range(num_to_follow):
            follow_buttons[button].click()
            sleep(uniform(2, 5))

        print(f"Followed {num_to_follow} accounts.")


    sleep(5)