from playwright.sync_api import sync_playwright
import os
from time import sleep, time
import requests
from dotenv import load_dotenv
from random import choice, randint, uniform
import re
import logging

load_dotenv()

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler("my_app.log")])

USERNAME = os.getenv('MY_USERNAME')  # replace with your environment variable for username
PASSWORD = os.getenv('MY_PASSWORD')  # replace with your environment variable for password
PROFILE_PATH = os.getenv('MY_PROFILE_PATH')  # replace with your environment variable for profile path
CHROME_PATH = os.getenv('MY_CHROME_PATH')  # replace with your environment variable for chrome path

with sync_playwright() as p:
    browser_type = p.chromium

    # Path to your Google Chrome installation. Modify this to point to the Chrome executable on your system.
    chrome_executable_path = CHROME_PATH

    context = browser_type.launch_persistent_context(
        executable_path=chrome_executable_path,
        user_data_dir=PROFILE_PATH,
        headless=False,
    )

    page = context.new_page()

    def post(file_path):
        try:
            # Navigate to the tweet composition page
            page.goto("https://www.instagram.com")
            sleep(uniform(5, 10))
            
        except Exception as e:
            # This will catch exceptions related to navigation
            logging.error(f"An error occurred while navigating to the tweet page: {e}")
            return  # Exit the function
        
        try:
            # Click on the 'Create' button
            page.query_selector("span:has-text('Create')").click()
            sleep(uniform(5, 10))
        except Exception as e:
            logging.error(f"Error clicking the 'Create' button: {e}")
            return  # Return early to stop the function here

        try:
            # Set the file path for photo upload
            page.set_input_files('xpath=//input[@class="_ac69" and @type="file" and @accept="image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime"]', file_path)
            sleep(uniform(15, 20))
            page.click("div[role='button']:has-text('Next')")
            sleep(uniform(2, 5))
            page.click("div[role='button']:has-text('Next')")
            sleep(uniform(2, 5))
            page.click("div[role='button']:has-text('Share')")
        except Exception as e:
            logging.error(f"Error uploading the photo: {e}")


    def fetchPost():
        # Number of attempts to fetch a post
        max_attempts = 10
        attempts = 0

        # List of sources to fetch posts from, replace with your list of sources
        sources = [
            ("https://t.me/Radicalshitposting/", (44000, 47000)),
            ("https://t.me/BictorsShitpost/", (39000, 42000)),
            ("https://t.me/shitpost/", (53000, 56000))
        ]


        while attempts < max_attempts:
            try:
                source, randint_range = choice(sources)
                url = f"{source}{randint(*randint_range)}?embed=1&mode=tme"

                page.goto(url)
                sleep(uniform(5, 10))

                # Check for image
                picElement = page.query_selector('a.tgme_widget_message_photo_wrap')
                if picElement:
                    imageStyle = picElement.get_attribute('style')  
                    regexPattern = r"background-image:url\('(.*)'\)"
                    match = re.search(regexPattern, imageStyle)

                    if match:
                        response = requests.get(match.group(1))
                        if response.status_code == 200:
                            with open('image.jpg', 'wb') as file:
                                file.write(response.content)
                            return 'image'
                        else:
                            logging.error('Failed to download the image')
                            return None

                # Check for video
                videoElement = page.query_selector('video.tgme_widget_message_video.js-message_video')
                if videoElement:
                    videoURL = videoElement.get_attribute('src')
                    if videoURL:
                        response = requests.get(videoURL)
                        if response.status_code == 200:
                            with open('video.mp4', 'wb') as file:
                                file.write(response.content)
                            return 'video'
                        else:
                            logging.error('Failed to download the video')
                            return None

                attempts += 1

            except Exception as e:
                logging.error(f"Attempt {attempts + 1} failed with error: {e}")
                attempts += 1

        logging.error("Failed to fetch a post after 3 attempts.") 
        return None

    
    def follow():
         # Will randomly pick one of these below sources and then follow their n last followers
        follow_id_list = ["6.memes.9"]  # Replace with your list of usernames

        try:
            random_number = choice(range(len(follow_id_list)))
            page.goto(f'https://www.instagram.com/{follow_id_list[random_number]}/followers/')
            sleep(uniform(5, 10))
        except Exception as e:
            logging.error(f"Error navigating to the followers page: {e}")
            return

        try:
            # Locate the follow buttons
            unfollow_buttons = page.query_selector_all("div[role='dialog'] button div:text-is('Following')")
            follow_buttons = page.query_selector_all("div[role='dialog'] button div:text-is('Follow')")
            unfollow_buttons.extend(follow_buttons)
            follow_buttons = unfollow_buttons
            num_to_follow = randint(1, 9)
        except Exception as e:
            logging.error(f"Error locating the follow buttons: {e}")
            return

        followed_count = 0  # Track the actual number of successful follows
        button = 0  # Keep track of the current button index

        # Follow a random number of accounts
        while followed_count < num_to_follow:
            print(button)
            try:
                if follow_buttons[button].inner_html() == "Following":
                    button += 1
                    follow_buttons[button].scroll_into_view_if_needed()
                    sleep(uniform(1, 2))
                    try:
                        # Locate the follow buttons
                        unfollow_buttons = page.query_selector_all("div[role='dialog'] button div:text-is('Following')")
                        follow_buttons = page.query_selector_all("div[role='dialog'] button div:text-is('Follow')")
                        unfollow_buttons.extend(follow_buttons)
                        follow_buttons = unfollow_buttons
                    except Exception as e:
                        logging.error(f"Error locating the follow buttons: {e}")
                        return
                    continue
                follow_buttons[button].click()
                button += 1
                sleep(uniform(1, 2))
                followed_count += 1
            except Exception as e:
                button += 1
                logging.error(f"Error following account number {button}: {e}")
                return

        logging.info(f"Followed {followed_count} accounts.")

    
    def unfollow():
        try:
            # Navigate to the following page
            page.goto(f'https://www.instagram.com/{USERNAME}/following')
            sleep(uniform(5, 10))
        except Exception as e:
            logging.error(f"Error navigating to the following page: {e}")
            return  # Return early to stop the function here

        try:
            # Locate the unfollow buttons
            unfollow_buttons = page.query_selector_all("div[role='dialog'] button div:text-is('Following')")
            num_to_unfollow = randint(10, 30)
        except Exception as e:
            logging.error(f"Error locating the unfollow buttons or determining the number of accounts to unfollow: {e}")
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
                logging.error(f"Error unfollowing account number {button + 1}: {e}")

        logging.info(f"Unfollowed {unfollowed_count} accounts.")



    # Start the script
    script_start_time = time()  # To keep track of when the script started running
    MAX_LOGIN_ATTEMPTS = 3

    while True:  # Infinite loop to ensure the script runs indefinitely

        login_attempts = 0
        while login_attempts < MAX_LOGIN_ATTEMPTS:
            page.goto("https://www.instagram.com/accounts/login/")
            sleep(uniform(5, 10))  # Give some time for the page to load

            # checking if we are on the login page
            if "accounts/login" in page.url:
                try:
                    page.fill("input[name='username']", USERNAME)
                    sleep(uniform(2, 5))
                    
                    page.fill("input[name='password']", PASSWORD)
                    sleep(uniform(2, 5))

                    # Handling cookies pop-up
                    if page.query_selector("button:has-text('Allow essential and optional cookies')"):
                        page.click("button:has-text('Allow essential and optional cookies')")
                    
                    page.click("button[type='submit']")
                    sleep(uniform(5, 10))
                    
                    # Check if login was successful by verifying if we are out of the login page
                    if "accounts/login" not in page.url:
                        # You might want to add any post-login steps here, like dismissing pop-ups
                        break  # Exit the login_attempts loop

                except Exception as e:
                    logging.error(f"Login attempt {login_attempts + 1} failed due to: {e}")
                    login_attempts += 1
                    if login_attempts < MAX_LOGIN_ATTEMPTS:
                        logging.info("Reloading page for next login attempt...")
                        sleep(uniform(2, 5))   # Adding a short sleep before reloading
                        page.goto("https://www.instagram.com/accounts/login/")
                        sleep(uniform(5, 10))  # Sleep again after reloading

        # If reached max attempts and still not logged in
        if login_attempts == MAX_LOGIN_ATTEMPTS:
            logging.error("Reached max login attempts. Please check your credentials or the page structure.")
            break  # Exit the main loop

        # Define the total number of posts to make in the day
        num_of_posts_today = randint(4, 6)

        # Define the number of times to run the follow() function
        follow_times_today = randint(0, 3)
        follow_intervals = sorted([randint(0, 86400) for _ in range(follow_times_today)])
        next_follow_index = 0  # To keep track of which follow_interval to check next

        # Calculate the average interval
        avg_interval = 86400 / num_of_posts_today

        # Define the time we start the loop, to make sure we don't cross into the next day
        start_time = time()

        while num_of_posts_today > 0 and (time() - start_time) < 86400:

            media_type = fetchPost()
            if media_type == 'image':
                post('image.jpg')
                os.remove('image.jpg')  # Delete the image after posting
            elif media_type == 'video':
                post('video.mp4')
                os.remove('video.mp4')  # Delete the video after posting

            # Check if it's time for the next follow action
            if next_follow_index < len(follow_intervals) and (time() - start_time) > follow_intervals[next_follow_index]:
                follow()
                next_follow_index += 1

            # Randomize the sleep time based on the average interval with ±20% variation
            sleep_time = randint(int(0.8 * avg_interval), int(1.2 * avg_interval))
            sleep(sleep_time)

            num_of_posts_today -= 1

        # Check if a week has passed to unfollow
        if time() - script_start_time >= 7 * 86400:
            unfollow()
            script_start_time = time()  # Reset the timer after unfollowing

        # Sleep until the next day starts
        while (time() - start_time) < 86400:
            sleep(600)  # Sleep for 10 minutes and then check again
