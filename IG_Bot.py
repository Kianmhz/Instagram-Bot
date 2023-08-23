from playwright.sync_api import sync_playwright
import os
import time
import requests
from dotenv import load_dotenv
from random import choice

load_dotenv()

USERNAME = os.getenv('MY_USERNAME')  # replace with your environment variable for username
PASSWORD = os.getenv('MY_PASSWORD')  # replace with your environment variable for password

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir="/Users/kianmhz/Library/Application Support/Google/Chrome/Profile 2",
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
            page.wait_for_selector('div:has-text("Not Now")').click()
        except:
            print("login failed")


    def upload_photo(file_path):
        page.query_selector("span:has-text('Create')").click()

        time.sleep(5)

        page.set_input_files('xpath=//input[@class="_ac69" and @type="file" and @accept="image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime"]', file_path)

    # upload_photo("C:\\Users\\kianm\\Desktop\\test.jpg")   # replace with your file path

    def dataset():
        page.goto('https://t.me/meme/756')
        time.sleep(5)
        link_element = page.wait_for_selector('xpath=/html/body/div/div[2]/a[2]')
        print(link_element)
        image_style = link_element.get_attribute('style')
        image_url = image_style.split("url('")[1].split("')")[0]

        response = requests.get(image_url)
        if response.status_code == 200:
            with open('image.jpg', 'wb') as file:
                file.write(response.content)
        else:
            print('Failed to download the image')
    
    def follow():
         # Will randomly pick one of these below sources and then follow their n last followers
        follow_id_list = ["username1", "username2"]  # Replace with your list of usernames
        random_number = choice(range(len(follow_id_list)))

        page.goto(f'https://www.instagram.com/{follow_id_list[random_number]}/followers/')

    follow()


    time.sleep(500)