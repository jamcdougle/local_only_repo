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

# Set Chrome options to maximize the window
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
folder_file = 'C:/Users/mcdouglellc/Downloads/chromedriver'
driver = webdriver.Chrome(folder_file,options=chrome_options)

page=1
website =('https://opportunities.columbia.edu/jobs/search?block_index=0&block'+
    '_uid=a46a070c3096d4b4b071a92d21dc0eed&dropdown_field_1_uids%5B%5D=b51df'+
    '6df91b69c9aacda3e2dc7a20e53&dropdown_field_1_uids%5B%5D=1bca86c4aca10b6'+
    'af6810aecfef7b95d&dropdown_field_1_uids%5B%5D=f7e98b02a5976c6556c3a5f14'+
    '1e912df&dropdown_field_1_uids%5B%5D=b69197c0f29776544152c928b9bd098b&dr'+
    'opdown_field_1_uids%5B%5D=c38bcbcf1898500a12ce7e1ee257a2a4&dropdown_fie'+
    'ld_1_uids%5B%5D=68658337891e7ec1bc60a61910d10ba7&employment_type_uids%5'+
    'B%5D=874088ab1598f5fd27779504dc693093&location_uids=&page='+
    str(page)+
    '&page_row_index=1&page_row_uid=36f2ce175cad2b3e9a8dc29feef1ce84&page_ve'+
    'rsion_uid=d59bed0726d9b0a1e03ce573610a9066&query=&search_categories=&se'+
    'arch_cities=&search_departments=&search_dropdown_field_1_values=&search'+
    '_employment_types=&sort=')

driver.get(website)
time.sleep(3)

try:
    # Find the element using its ID
    element = driver.find_element(By.ID, 'consent_agree')
    # Click the element
    element.click()


    time.sleep(3.5)
except NoSuchElementException:
    print("no consent agree")

# Find the element containing the desired value
counts_element = driver.find_element(By.CLASS_NAME, 'table-counts')
# Extract the text content from the element
text_content = counts_element.text
# Parse and extract the desired value
Records = text_content.split(' of ')[-1].split(' ')[0]
Records = Records.strip()
Records = int(Records)
print(Records)  # Output: 927

page_items = driver.find_elements(By.CLASS_NAME, 'page-item')
# Extract the value from the last element
last_page_item = page_items[-2]
Pages = int(last_page_item.text)
print(Pages)
time.sleep(3.5)

all_data = []

for rec in range(0,Records):
    if (rec != 0) and (rec%30 == 0):
        page = 1 + int(rec/30)
        website =('https://opportunities.columbia.edu/jobs/search?block_index=0&block'+
            '_uid=a46a070c3096d4b4b071a92d21dc0eed&dropdown_field_1_uids%5B%5D=b51df'+
            '6df91b69c9aacda3e2dc7a20e53&dropdown_field_1_uids%5B%5D=1bca86c4aca10b6'+
            'af6810aecfef7b95d&dropdown_field_1_uids%5B%5D=f7e98b02a5976c6556c3a5f14'+
            '1e912df&dropdown_field_1_uids%5B%5D=b69197c0f29776544152c928b9bd098b&dr'+
            'opdown_field_1_uids%5B%5D=c38bcbcf1898500a12ce7e1ee257a2a4&dropdown_fie'+
            'ld_1_uids%5B%5D=68658337891e7ec1bc60a61910d10ba7&employment_type_uids%5'+
            'B%5D=874088ab1598f5fd27779504dc693093&location_uids=&page='+
            str(page)+
            '&page_row_index=1&page_row_uid=36f2ce175cad2b3e9a8dc29feef1ce84&page_ve'+
            'rsion_uid=d59bed0726d9b0a1e03ce573610a9066&query=&search_categories=&se'+
            'arch_cities=&search_departments=&search_dropdown_field_1_values=&search'+
            '_employment_types=&sort=')
        time.sleep(3.5*4)
        driver.get(website)
        time.sleep(3.5*4)
    i = rec%30
    #Don't Need This Anymore...print(rec, i, page)
    link_to_rec = 'link_job_title_1_0_' + str(i)
    element2 = driver.find_element(By.ID, link_to_rec)
    driver.execute_script("arguments[0].scrollIntoView(true);", element2)
    # Click the element
    time.sleep(3.5 + random.random()/4)
    element2.click()
    # Find the element using its ID
    the_list = []
    block1=['job_title_2_0',
            'requisition_identifier_2_0_0',
            "location_2_0_0_0",
            "department_2_0_0_0",
            "employment_type_2_0_0_0",
            "opening_on_2_0_0",
            "dropdown_field_1_2_0_0"]
    for entry in block1:
        try:
            the_list.append(driver.find_element(By.ID, entry).text.strip())
        except NoSuchElementException:
            print("Element " + entry + " not found")
            the_list.append("#")
    try:
        ul_element = driver.find_element_by_css_selector('ul.job-attributes')
        li_elements = ul_element.find_elements_by_tag_name('li')
        text_list = []
        # Iterate over the list items and extract the text
        for li_element in li_elements:
            text_list.append(li_element.text.strip())
        #print(text_list)
        the_list.append(text_list)
    except NoSuchElementException:
        print("No Second Block")
        the_list.append(["#"])
    
    #move ID to the front
    if len(the_list[1]) == 6:
        moving = the_list.pop(1)
        the_list.insert(0, moving)
    
    #move salary to the front and clean it
    if "Salary" in the_list[-1][-1]:
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
    
    if ((len(the_list[1]) >= 7)):# and 
        #(the_list[1][-4:-2] == "-1") and not 
        #(the_list[1][-2] in ['0','1','2',])):
            print(the_list)
    all_data.append(the_list)
    time.sleep(3.5 + random.random()/4)
    driver.execute_script("window.history.go(-1)")
    time.sleep(3.5 + random.random()/4)





















