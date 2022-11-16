from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


import pathlib
script_directory = pathlib.Path().absolute()


options = Options()
#options.binary_location = '/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe' 
options.binary_location = '/usr/bin/google-chrome' 

#options.add_argument("user-data-dir=/home/jonas/git/boardgame-vision/selenium")
options.add_argument(f"user-data-dir={script_directory}/selenium-data")
print(script_directory)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options = options)
driver.get('http://www.boardgamegeek.com/')
print("Chrome Browser Invoked")
driver.quit()