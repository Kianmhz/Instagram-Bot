from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time

mobile_emulation = {
    "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
}

username = os.getenv('MY_USERNAME')  # replace with your environment variable for username
password = os.getenv('MY_PASSWORD')  # replace with your environment variable for password

options = Options()
options.add_argument("user-data-dir=C:\\Users\\kianm\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 4") # Replace the path below with the path to your Chrome profile
options.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome(options=options)

driver.get("https://www.instagram.com/accounts/login/")

# Checking if we are on the login page by examining the URL
if "accounts/login" in driver.current_url:

    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]/div/label/input')))
    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div[1]/div[4]/div/label/input')))
    login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div[1]/div[6]')))

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()


# input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0_Hl"]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/section/div/div[2]/div/div/div/div[1]/button/form/input')))

# file_path = "C:\\Users\\kianm\\OneDrive\\Pictures\\IMG_0045.JPG" # Path to the file you want to upload

# input_field.send_keys(file_path)

time.sleep(600)