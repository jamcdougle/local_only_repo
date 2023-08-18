# -*- coding: utf-8 -*-
"""
Created on Thu May  4 21:23:23 2023

@author: mcdouglellc
"""
import time
import pandas as pd
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup




# Replace '/path/to/chromedriver' with the actual path to your chromedriver executable
#os.environ['PATH'] = f"{os.environ['PATH']}:C:\\Users\\mcdouglellc\\Downloads\\chromedriver_win32\\chromedriver.exe"

vendor = 'empire'
bar = 'tap'
folder_file = 'C:/Users/jm3696/Downloads/chromedriver'
website = 'https://ebay.com/'
user_name = 'jamcdougle@gmail.com'
password = 'rqu*bvq0akz.RXE.dnu'

browser = webdriver.Chrome(executable_path="C:\\Users\\mcdouglellc\\Downloads\\chromedriver_win32\\chromedriver.exe")
time.sleep(1)
browser.get(website)
time.sleep(1)
browser.find_element_by_link_text('Sign in').click()
'''
find text 'sign in'
click it



searchBar = browser.find_element_by_id('ctl00_CustomerMainContent_txt_UserId')

#Sign In
browser = webdriver.Chrome(folder_file)
browser.get(website)
time.sleep(3)
searchBar = browser.find_element_by_id('ctl00_CustomerMainContent_txt_UserId')
searchBar.send_keys(user_name)
time.sleep(3)
searchBar = browser.find_element_by_id('ctl00_CustomerMainContent_txt_Password')
searchBar.send_keys(password)
time.sleep(3)
elem = browser.find_element_by_id('ctl00_CustomerMainContent_btn_ContinueLogin')
elem.send_keys(Keys.ENTER)
time.sleep(3)

#<button id="signin-continue-btn" name="signin-continue-btn" data-viewport="{&quot;trackableId&quot;:&quot;01GZMWZ0QY0KFKMZ973GMFDSQ3&quot;}" class="btn btn--fluid btn--large-truncated btn--primary" data-ebayui="" type="button">Continue</button>


'''