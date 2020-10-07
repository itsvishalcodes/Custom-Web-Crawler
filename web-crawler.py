from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as soup
import time
import wget
from getpass import getpass
import os

username = input("Enter Your Instagram username: ")
try:
    password = getpass(prompt="Enter your Instagram Password: ")
except Exception as error:
    print('ERROR: ', error)
    os.exit(1)
toCrawl = input("Enter Target Username: ")
url = f'https://www.instagram.com/{toCrawl}/'
login_url = 'https://www.instagram.com/accounts/login/'

chrome_driver_path = '/Users/Vishal/Desktop/Custom-Web-Crawler/chromedriver'

chrome_options = Options()
# chrome_options.add_argument('--headless')
webdriver = webdriver.Chrome(
  executable_path=chrome_driver_path, options=chrome_options
)



with webdriver as driver:
    driver.get(login_url)

    element = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'L3NKy'))
    )

    # print('Submit button found')
    # page_soup = soup(driver.page_source, "html.parser")
    username_container = driver.find_element_by_name('username')
    password_container = driver.find_element_by_name("password")
    # username_container = page_soup.find("input", {"name": "username" })
    # password_container = page_soup.find("input", {"name": "password"})
    username_container.send_keys(username)
    password_container.send_keys(password)
    time.sleep(2)
    driver.find_element_by_class_name('L3NKy').click()
    element = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'ABCxa'))
    )

    driver.get(url)

    element = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'ySN3v'))
    )

    page_soup = soup(driver.page_source, "html.parser")

    total_posts = page_soup.find("span", {"class": "g47SY"}).text

    image_containers = page_soup.findAll("div", {"class": "KL4Bh"})

    # while len(image_containers) != int(total_posts):
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     image_containers = page_soup.findAll("div", {"class": "KL4Bh"})
    #     print('Still Scrolling...')

    path = f'C:\\{toCrawl}\\'
    try:
        os.mkdir(path)
        os.chdir(path)
    except OSError as error:
        print(error)
        os.exit(0)

    for image_container in image_containers:
        image = image_container.find("img", {"class": "FFVAD"})
        # file_name = image['alt']+'.jpg'
        image_url = image['src']

        # Use wget download method to download specified image url.
        image_filename = wget.download(image_url)

        print('Image Successfully Downloaded: ', image_filename)
