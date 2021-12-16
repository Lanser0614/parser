import json
import time
import cssutils
import pymysql
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from googletrans import Translator
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pychrome


def wylsa():
    options = webdriver.ChromeOptions()
    options.add_argument('--remote-debugging-port=8000')
    options.add_argument('--no-sandbox'),
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.headless = True
    options.add_argument('start-maximized')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-dev-shm-usage')
    ser = Service("C:\\Users\\Lanser\\Desktop\\blogPars-masterkkkk\\chromedriver.exe")
    op = webdriver.ChromeOptions()
    s = webdriver.Chrome(service=ser, options=op)
    time.sleep(100)
    # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    
  
translator = Translator()
wylsa()
