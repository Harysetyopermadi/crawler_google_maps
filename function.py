from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import time
import datetime
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


def opened_link_chroome(url_search):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1300, 800)
    driver.get(url_search)
    #time.sleep(5)
    return driver
def Scrap_data(driver):

    action=ActionChains(driver)
    a= driver.find_elements(By.CLASS_NAME,'ecceSd')
    while True:
        #print(len(a))
        content = driver.page_source
        var= len(a)
        Scroll_origin=ScrollOrigin.from_element(a[len(a)-1])
        action.scroll_from_origin(Scroll_origin,0,1000).perform()
        #time.sleep(2)

        data = BeautifulSoup(content, 'html.parser')
        print("---Proccessing---")
        if data.find('div',class_="PbZDve"):
            print("Parsing selesai")
            break
    data = BeautifulSoup(content, 'html.parser')
    lens = 1
    res = []
    for area in data.find_all('div', class_="Nv2PK Q2HXcd THOPZb"):
        #print('proses data ke-' + str(lens))
        current_datetime = datetime.datetime.now()
        merge_date = current_datetime.strftime("%Y%m%d%H%M%S%f")
        id=str(lens)
            #Nama
        try:
            a_nama = area.find('div', class_="qBF1Pd fontHeadlineSmall").get_text()
            nama = a_nama
        except:
            nama="Nama Not Found"
            #Rating
        try:
            a_rating = area.find('span', class_="MW4etd").get_text()
            rating = a_rating
        except:
            rating="Rating Not Found"
                
            #link
        try:
            a_link = area.find('a', class_='hfpxzc')
            link = a_link.get('href')
        except:
            link="Link Not Found"

            # Append the values to the list res as a dictionary
        res.append({'id':merge_date+id, 'nama': nama, 'rating': rating, 'link': link})
            
        lens += 1

    df=pd.DataFrame(res)
    #driver.quit()
    return df