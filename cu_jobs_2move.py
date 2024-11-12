#from bs4 import BeautifulSoup  #import pandas as pd  #import xlsxwriter
#from selenium.webdriver import ActionChains  #from selenium.webdriver.common.keys import Keys
import os
import random
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
chrome_options = Options() #Maximize the window
chrome_options.add_argument("--start-maximized")
# Define path to chromedriver
driver_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'chromedriver.exe')
# Set up the Service object
service = Service(executable_path=driver_path, options=chrome_options)
# Initialize Chrome with service and options
driver = webdriver.Chrome(service=service, options=chrome_options)
page=1
website_1 = "https://opportunities.columbia.edu/jobs/search?block_index=0&block_uid=a46a070c3096d4b4b071a92d21dc0eed&location_uids=&page_row_index=1&page_row_uid=36f2ce175cad2b3e9a8dc29feef1ce84&page_version_uid=d59bed0726d9b0a1e03ce573610a9066&query=&search_categories=&search_cities=&search_departments=&search_dropdown_field_1_values=&search_employment_types=&sort=&page="
website = website_1 + str(page)
driver.get(website)
time.sleep(7)           #SLEEP ADDED SO A CAPTCHA ISNT THROWN
try:
    element = driver.find_element(By.ID, 'consent_agree') #Find element by ID
    element.click() # Click the element
    time.sleep(3.5)
except NoSuchElementException:
    print("no consent agree")
#total positions to iterate through
counts_element = driver.find_element(By.CLASS_NAME, 'table-counts') #Webelement
text_content = counts_element.text #extract text str
Records = text_content.split(' of ')[-1].split(' ')[0] 
Records = Records.strip()
Records = int(Records)
print(Records)  # Output: usually around 185
page_items = driver.find_elements(By.CLASS_NAME, 'page-item') #total pages
last_page_item = page_items[-2]
Pages = int(last_page_item.text)
print(Pages)
time.sleep(3.5)
all_data = []
for rec in range(0,Records):            #go thru all records; 30 recs/page
    if (rec != 0) and (rec%30 == 0):
        page = 1 + int(rec/30)
        website = website_1 + str(page) 
        time.sleep(3.5*4)
        driver.get(website)
        time.sleep(3.5*4)
    i = rec%30
    link_to_rec = 'link_job_title_1_0_' + str(i)
    element2 = driver.find_element(By.ID, link_to_rec)
    driver.execute_script("arguments[0].scrollIntoView(true);", element2)
    time.sleep(3.5 + random.random()/4)        #randomize wait or it catches on
    element2.click()
    the_list = []  #these are all IDs we are pulling
    block1=['job_title_2_0',           'requisition_identifier_2_0_0',
            "location_2_0_0_0",        "department_2_0_0_0",
            "employment_type_2_0_0_0", "opening_on_2_0_0",
            "dropdown_field_1_2_0_0"]
    for entry in block1:
        try:
            the_list.append(driver.find_element(By.ID, entry).text.strip())
        except NoSuchElementException:
            print("Element " + entry + " not found")
            the_list.append("#")
    try:
        ul_element = driver.find_element(By.CSS_SELECTOR, 'ul.job-attributes')
        li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
        text_list = []
        for li_element in li_elements: #Iterate over list items, extract text
            text_list.append(li_element.text.strip())
        the_list.append(text_list)
    except NoSuchElementException:
        print("No Second Block")
        the_list.append(["#"])
    if len(the_list[1]) == 6: #move ID to the front
        moving = the_list.pop(1)
        the_list.insert(0, moving)
    if "Salary" in the_list[-1][-1]: #move salary to the front & clean
        moving = the_list[-1].pop(-1)
        moving = moving.replace('.00','')
        moving = moving.replace('000','')
        moving = re.sub(r',\d\d\d','',moving)
        moving = moving.replace('-','797979')
        moving = moving.replace('to','797979')
        moving = re.sub(r'\D','', moving)
        moving = moving.replace('797979','-')
        the_list.insert(1, moving)
    the_list.pop(-1)
    for index, item in enumerate(the_list):
        if item == "Full Time":
            the_list.pop(index)
    for index, item in enumerate(the_list):
        the_list[index] = the_list[index].replace('Opening on: ','')
        the_list[index] = the_list[index].replace('Medical Center','CUMC')
        the_list[index] = the_list[index].replace('Manhattanville','Mville')
        the_list[index] = the_list[index].replace('Morningside','MS')
    if ((len(the_list[1]) >= 7)): #filtering out for bottom salary <100k
            print(the_list)
    all_data.append(the_list)
    time.sleep(3.5 + random.random()/4)
    driver.execute_script("window.history.go(-1)")
    time.sleep(3.5 + random.random()/4)