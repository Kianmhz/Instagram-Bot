from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time

username = os.getenv('MY_USERNAME')  # replace with your environment variable for username
password = os.getenv('MY_PASSWORD')  # replace with your environment variable for password

options = Options()
options.add_argument("user-data-dir=C:\\Users\\kianm\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 4") # Replace the path below with the path to your Chrome profile

driver = webdriver.Chrome(options=options)

driver.get("https://www.instagram.com/accounts/login/")

# Checking if we are on the login page by examining the URL
if "accounts/login" in driver.current_url:

    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')))
    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')))
    login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div')))

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

time.sleep(600)