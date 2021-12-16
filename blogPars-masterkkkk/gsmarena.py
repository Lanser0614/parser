import requests
from bs4 import BeautifulSoup
# import pymysql
import time
# from selenium import webdriver
import time
import googletrans
from googletrans import Translator
# import argparse
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.proxy import Proxy, ProxyType
# news-column-index review-body
def gsm_pars():

    proxies = {'http':'54.238.176.83:3128'}
    req = requests.get('https://www.gsmarena.com/',proxies = proxies)
    soup = BeautifulSoup(req.text, features="lxml")
    news = soup.select(".news-item>a")
    print(news)
    hrefs = []
    texts = []
    time.sleep(30)
    translator = Translator()
    for new in news:
        hrefs.append(new["href"])
        req = requests.get(f'https://www.gsmarena.com/{new["href"]}')
        soup = BeautifulSoup(req.text, features="lxml")
        head = soup.select(".article-info-name")[0].get_text()
        text = soup.select(".review-body")[0].get_text()
        texts.append((head,text))
        time.sleep(30)
    translated_object=[]
    for text in texts:
        translated_object.append(translator.translate(text=text,dest='ru',src='en'))
    with open('text.txt') as f:
        for translate in translated_object:
            f.write(translate)
        f.close()
gsm_pars()
