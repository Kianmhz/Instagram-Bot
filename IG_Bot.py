from playwright.sync_api import sync_playwright
import os
from time import sleep, time
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

    page.goto("https://www.instagram.com/accounts/login")

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
        try:
            # Click on the 'Create' button
            page.query_selector("span:has-text('Create')").click()
            sleep(uniform(10, 15))
        except Exception as e:
            print(f"Error clicking the 'Create' button: {e}")
            return  # Return early to stop the function here

        try:
            # Set the file path for photo upload
            page.set_input_files('xpath=//input[@class="_ac69" and @type="file" and @accept="image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime"]', file_path)
        except Exception as e:
            print(f"Error uploading the photo: {e}")


    def fetchPost():
        # Number of attempts to fetch a post
        max_attempts = 3
        attempts = 0

        while attempts < max_attempts:
            try:
                # Will pick random posts from the source and downloads it
                page.goto(f'https://t.me/shitpost/{randint(45000,60000)}?embed=1&mode=tme')  # replace with your own source
                sleep(uniform(2, 5))

                # Check for image
                picElement = page.query_selector('a.tgme_widget_message_photo_wrap')
                if picElement:
                    imageStyle = picElement.get_attribute('style')  
                    regexPattern = r"background-image:url\('(.*)'\)"  # Regex pattern to extract the image URL
                    match = re.search(regexPattern, imageStyle)

                    if match:
                        # Download the image
                        response = requests.get(match.group(1))
                        if response.status_code == 200:
                            with open('image.jpg', 'wb') as file:
                                file.write(response.content)
                            return  # Successfully downloaded the image, exit function
                        else:
                            print('Failed to download the image')
                            return

                # If no image, check for a video
                videoElement = page.query_selector('video.tgme_widget_message_video.js-message_video')
                if videoElement:
                    videoURL = videoElement.get_attribute('src')
                    if videoURL:
                        # Download the video
                        response = requests.get(videoURL)
                        if response.status_code == 200:
                            with open('video.mp4', 'wb') as file:
                                file.write(response.content)
                            return  # Successfully downloaded the video, exit function
                        else:
                            print('Failed to download the video')
                            return

                attempts += 1  # Increment the attempt counter

            except Exception as e:
                # Handle any exception and print its message
                print(f"Attempt {attempts + 1} failed with error: {e}")
                attempts += 1  # Increment the attempt counter

        print("Failed to fetch a post after 3 attempts.")  # If reached here, all attempts were unsuccessful

    
    def follow():
        follow_id_list = ["username"]  # Replace with your list of usernames

        try:
            random_number = choice(range(len(follow_id_list)))
            page.goto(f'https://www.instagram.com/{follow_id_list[random_number]}/followers/')
            sleep(uniform(10, 15))
        except Exception as e:
            print(f"Error navigating to the followers page: {e}")
            return

        try:
            # Locate the follow buttons
            follow_buttons = page.query_selector_all("div[role='dialog'] button div:text-is('Follow')")
            num_to_follow = randint(1, 9)
        except Exception as e:
            print(f"Error locating the follow buttons: {e}")
            return

        followed_count = 0  # Track the actual number of successful follows

        # Follow a random number of accounts
        for button in range(num_to_follow):
            try:
                follow_buttons[button].click()
                sleep(uniform(2, 5))
                followed_count += 1
            except Exception as e:
                print(f"Error following account number {button + 1}: {e}")

        print(f"Followed {followed_count} accounts.")

    
    def unfollow():
        try:
            # Navigate to the following page
            page.goto(f'https://www.instagram.com/username/following')
            sleep(uniform(10, 15))
        except Exception as e:
            print(f"Error navigating to the following page: {e}")
            return  # Return early to stop the function here

        try:
            # Locate the unfollow buttons
            unfollow_buttons = page.query_selector_all("div[role='dialog'] button div:text-is('Following')")
            num_to_unfollow = randint(10, 30)
        except Exception as e:
            print(f"Error locating the unfollow buttons or determining the number of accounts to unfollow: {e}")
            return  # Return early if there's an error

        unfollowed_count = 0  # To keep track of the number of successful unfollows

        # Unfollow a random number of accounts
        for button in range(num_to_unfollow):
            try:
                unfollow_buttons[button].click()
                page.wait_for_selector('button:has-text("Unfollow")').click()
                sleep(uniform(2, 5))
                unfollowed_count += 1
            except Exception as e:
                print(f"Error unfollowing account number {button + 1}: {e}")

        print(f"Unfollowed {unfollowed_count} accounts.")
            

