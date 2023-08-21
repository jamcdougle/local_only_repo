import time
import pandas as pd
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import random
import re

#Maximize the window
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

#Chromedriver location
folder_file = 'C:/Users/mcdouglellc/Downloads/chromedriver'
driver = webdriver.Chrome(folder_file,options=chrome_options)

website = 'https://prioritypass.com/airport-lounges'
driver.get(website)
time.sleep(3)           #SLEEP ADDED SO A CAPTCHA ISNT THROWN

try:
    #Pop-up Accept... Find the element using its ID
    element = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
    element.click()
    time.sleep(3.5)
except NoSuchElementException:
    print("no consent agree") #help find issue if this is it

time.sleep(3)           #SLEEP ADDED SO A CAPTCHA ISNT THROWN

anchors = driver.find_elements_by_css_selector('.items a')

# Extract the href attributes from these anchor tags and store them in a list
hrefs = [anchor.get_attribute('href') for anchor in anchors]

#print(hrefs)








#Immediate next steps:
#For a given location, cycle through each terminal
#For each Lounge, click into it and take all the information I need
#Once these are set up, bring everything into a df with:
#Country/Location/Abbr./Terminal/Lounge/Columns for all the data



full_list=[]
for site in hrefs:
    website = site
    driver.get(website)
    time.sleep(3)           #SLEEP ADDED SO A CAPTCHA ISNT THROWN
    anchors = driver.find_elements_by_css_selector('a.item-link')
    sub_hrefs = [anchor.get_attribute('href') for anchor in anchors]
    print(sub_hrefs)






























