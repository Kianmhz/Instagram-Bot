from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time

width = 375
height = 812

mobile_emulation = {
    "deviceMetrics": { "width": width, "height": height, "pixelRatio": 3.0 },
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
    login = True
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]/div/label/input')))
    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div[1]/div[4]/div/label/input')))
    login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div[1]/div[6]')))

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

    not_now_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="button" and text()="Not Now"]')))
    not_now_button.click()


# Absolute path to the file you want to upload
file_path = "C:\\Users\\kianm\\OneDrive\\Desktop\\Python\\RestaurantFinder\\static\\img\\rest_6.jpeg"

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/div[1]/nav/div/header/div/div/div[1]/div[1]/span/div/a/div'))).click()

story = driver.find_element(By.XPATH, '//input[@accept="image/jpeg,image/png"]')
story.send_keys(file_path)


time.sleep(600)