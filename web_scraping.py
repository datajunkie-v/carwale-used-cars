import time
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urljoin

##### Web scrapper for infinite scrolling page #####
driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.carwale.com/used/cars-for-sale/?pn=1&kms=0-&year=0-&budget=0-&city=244&state=-1&so=-1&sc=-1")
time.sleep(2)  # Allow 2 seconds for the web page to open
scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break 

##### Extract Reddit URLs #####

soup = BeautifulSoup(driver.page_source, "html.parser")
links = soup.find_all("h3",attrs={'class':'o-bqHweY o-bVSleT o-bwCunT o-bfyaNx o-bNxxEB o-eZTujG o-byFsZJ o-fzoTzs o-bkmzIL'})

kms = soup.find_all("span",attrs={'class':'o-eemiLE o-cpNAVm'})

prices = soup.find_all("span",attrs={'class':'o-Hyyko o-eZTujG o-eqqVmt o-fzpibr'})


titles = []
kms_lst = []
prices_lst = []

for link,km,price in zip(links,kms,prices):
    titles.append(link.text)
    kms_lst.append(km.text.strip())
    prices_lst.append(price.text)

print(titles, kms_lst, prices_lst)

d = {'title':titles,'distance':kms_lst, 'prices':prices_lst}

cars_df = pd.DataFrame.from_dict(d)
print(cars_df)

cars_df.to_csv(r"C:\Users\P.Victor\OneDrive\Desktop\Project\cars10.csv",header=True, index=False)
