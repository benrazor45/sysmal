import sys
import fitz
import time
import pandas as pd
from selenium.webdriver.common.by import By
from utils import get_chrome_driver
from hash_mal import hash_groups

def get_malware_data():

    driver = get_chrome_driver()

    for malware_family, hash in hash_groups.items() :
        for i, md5 in enumerate(hash) :

            url = f'https://www.virustotal.com/gui/file/{md5}/behavior'
            print(f"[{malware_family}] {i+1}. Scraping {md5}")

            driver.get(url)
            time.sleep(10)

#cari shadowroot dari paling atas sampai ke elemen yang ingin di scrap.
            


        
