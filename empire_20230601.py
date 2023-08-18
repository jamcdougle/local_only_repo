# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 13:09:25 2023

@author: mcdouglellc
"""

# -*- coding: utf-8 -*-
#Taphouse, Empire, NEED TO DEFINE one_summary = [] at some point
import time
import pandas as pd
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import os



def detail_stats(browser,temp_soup):
    stats_temp = []
    tbl2 = temp_soup.find('table',{"id":"ctl00_CustomerMainContent_Datagrid2"})   
    inv_num_det = '#' + tbl2.find_all('td',{'align':"left"})[0].get_text()
    tbl1 = temp_soup.find('table',{"id":"ctl00_CustomerMainContent_DataGrid1"})
    true_count = len(tbl1.find_all('tr'))
    if true_count == 12:
        stat_pages = int(tbl1.find_all('tr')[-1].find_all('a')[-1].get_text())
    else:
        stat_pages = 1
    for stat_i in range(1, stat_pages + 1):
        if stat_i > 1:
            browser.find_element_by_link_text(str(stat_i)).click() 
            html = browser.page_source
            temp_soup = BeautifulSoup(html,'html.parser')       
            tbl1 = temp_soup.find(
                'table',{"id":"ctl00_CustomerMainContent_DataGrid1"})
            true_count = len(tbl1.find_all('tr'))
        row_count = min(true_count - 1, 10)
        #This is to deal with the last page having 2 extra tr's, not 1
        if (stat_pages > 1) and (stat_i == stat_pages) and (true_count != 12):
            row_count = row_count - 1
        for row in range(1, row_count + 1):
            item_num = tbl1.find_all('td')[10 * row + 2].get_text()
            item_descr = tbl1.find_all('td')[10 * row + 3].get_text()
            size = tbl1.find_all('td')[10 * row + 4].get_text()
            status = tbl1.find_all('td')[10 * row + 5].get_text()
            q = tbl1.find_all('td')[10 * row + 6].get_text()
            uom = tbl1.find_all('td')[10 * row + 7].get_text()
            p = tbl1.find_all('td')[10 * row + 8].get_text()
            pq = tbl1.find_all('td')[10 * row + 9].get_text()
            stats_temp = stats_temp + [(inv_num_det, item_num, item_descr, size, status, q, uom, p, pq)]
    return stats_temp

def summary_stats(temp_soup):
    tbl2 = temp_soup.find('table',{"id":"ctl00_CustomerMainContent_Datagrid2"})    
    ord_num = '#' + temp_soup.find('span',{'id':'ctl00_CustomerMainContent_lblJDEOrderNo'}).get_text()[0:7]
    ord_type =      temp_soup.find('span',{'id':'ctl00_CustomerMainContent_lblJDEOrderNo'}).get_text()[7:]    
    inv_num = '#' +  tbl2.find_all('td',{'align':"left"})[0].get_text()
    inv_date = tbl2.find_all('td',{'align':"left"})[1].get_text()
    due_date = tbl2.find_all('td',{'align':"left"})[2].get_text()
    amt_total = tbl2.find_all('td',{'align':"left"})[3].get_text()
    amt_open = tbl2.find_all('td',{'align':"left"})[4].get_text()
    return [(ord_num, ord_type, inv_num, inv_date, due_date, amt_total, amt_open)]

def radio_cycle(browser,count):
    #goes through up to 10 invoices
    one_summary = []
    one_detail = []
    for i in range(0,len(count)):  
        count[i].click()
        html = browser.page_source
        soup = BeautifulSoup(html,'html.parser')
        #the only invoice types which have details are RM and RI I think
        if  (soup.find('table',{"id":"ctl00_CustomerMainContent_DataGrid1"}).find_all('td')[13 + i * 11].get_text() =='RM') or (soup.find('table',{"id":"ctl00_CustomerMainContent_DataGrid1"}).find_all('td')[13 + i * 11].get_text() =='RI'):
            browser.find_element_by_id('ctl00_CustomerMainContent_btn_ShowDetails').click()
            time.sleep(1)
            html = browser.page_source
            soup = BeautifulSoup(html,'html.parser')
            one_summary = one_summary + summary_stats(soup)
            one_detail = one_detail + detail_stats(browser, soup)
            browser.find_element_by_id('ctl00_CustomerMainContent_btn_Back').click()    
            time.sleep(1)
        count = browser.find_elements_by_name('Radio1')
        time.sleep(1)
    return [one_summary, one_detail]





desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")





#define variables
vendor = 'empire'
bar = 'tap'
folder_file = desktop_path + '\\chromedriver_win32\\chromedriver'
website = 'https://ecommerce.empiremerchants.com/e2wLogin.aspx'
user_name = 'info@districttaphouse.com'
password = '246West38'









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

#Setup
browser.get("https://ecommerce.empiremerchants.com/e2wCustomerShipSelection.aspx?type=invoice")
time.sleep(3)
elem = browser.find_element_by_id('ctl00_CustomerMainContent_TBDateFrom')
elem.clear()
elem.send_keys('05/01/2014')
time.sleep(3)
elem.send_keys(Keys.ENTER)
time.sleep(3)

final_summary = []
final_detail = []




#Find how many pages of orders there are
html = browser.page_source
soup = BeautifulSoup(html,'html.parser')
ellipses = '...'
while ellipses == '...':
    ellipses = soup.find('table',{"id":"ctl00_CustomerMainContent_DataGrid1"}).find_all('tr')[-1].find_all('a')[-1].get_text()
    if ellipses == '...':
        browser.find_elements_by_link_text('...')[-1].click()
        time.sleep(1)
        html = browser.page_source
        soup = BeautifulSoup(html,'html.parser')
        ellipses = soup.find('table',{"id":"ctl00_CustomerMainContent_DataGrid1"}).find_all('tr')[-1].find_all('a')[-1].get_text()
pages = int(ellipses)









#Go back to the first element of the first page of data
for i in range(0, int((pages - 0.5)/10)):
    browser.find_elements_by_link_text('...')[0].click()
    time.sleep(1)
browser.find_element_by_link_text('1').click()













#Click to the next page and grab the data
for i in range(1, pages + 1):
    if i > 1:
        #if i = 1, then don't click through to 11 because 1 not done yet 
        if i % 10 == 1:
            #click through to next set of ten pages of data
            browser.find_elements_by_link_text('...')[-1].click()
            time.sleep(1)
        else:
            browser.find_element_by_link_text(str(i)).click()
    html = browser.page_source
    soup = BeautifulSoup(html,'html.parser')
    count = browser.find_elements_by_name('Radio1')
    #radio cycle is the main function called, radio_cycle will go through up to 10 invoices
    cycle_output = radio_cycle(browser, count)
    final_summary = final_summary + cycle_output[0]
    final_detail = final_detail + cycle_output[1]





'''












df_sum = pd.DataFrame(final_summary, 
    columns = ['ord_num', 'ord_type', 'inv_num', 'inv_date', 'due_date', 'amt_total', 'amt_open'])
df_det = pd.DataFrame(final_detail, 
    columns = ['inv_num', 'item_num', 'item_descr', 'size', 'status', 'q', 'uom', 'p', 'pq'])

df_sum['amt_total'] = df_sum['amt_total'].str.replace(',','').astype(float)
df_sum['amt_open'] = df_sum['amt_open'].str.replace(',','').astype(float)
df_det['p'] = df_det['p'].str.replace(',','').astype(float)
df_det['q'] = df_det['q'].str.replace(',','').astype(float)
df_det['pq'] = df_det['pq'].str.replace(',','').astype(float)

sum_dup = df_sum[df_sum.duplicated(subset=['inv_num'],keep=False)]

'''