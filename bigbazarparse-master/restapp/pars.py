# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pymysql
import time
from selenium import webdriver
import time
import argparse
from webdriver_manager.chrome import ChromeDriverManager

con = pymysql.connect(host='127.0.0.1', user='root', passwd='84SvEE71Pq', db='kattabozor',charset='utf8')
start_time = time.time()

def barcode(code,con):
	binary = '/usr/bin/firefox' 
	options = webdriver.Options()
	options.binary = binary 
	options.add_argument('start-maximized') 
	options.add_argument('--headless')
	options.add_argument('--disable-gpu')
	options.add_argument('--disable-extensions')
	path_to_driver = "usr/local/bin"
	driver = webdriver.Chrome(ChromeDriverManager().install(), options=options,executable_path = path_to_driver)
	try:
		driver.get(f"https://www.barcodelookup.com/{code}")
		html = driver.page_source
		soup = BeautifulSoup(html, features="lxml")
		name = soup.select(".product-details > h4")
		driver.quit()

		return name
	except:
		driver.quit()
	finally:
		driver.quit()


print("--- %s seconds ---" % (time.time() - start_time))
