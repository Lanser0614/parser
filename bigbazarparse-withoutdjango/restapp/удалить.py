import requests
from bs4 import BeautifulSoup
import time

# import argparse
# from webdriver_manager.firefox import GeckoDriverManager
# from selenium.webdriver.common.proxy import Proxy, ProxyType
header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0', }
req = requests.get(f'https://openshop.uz/shop/subcategory/phones?page=1', headers=header)
soup = BeautifulSoup(req.text, features="lxml")
print(soup)
last_page = int(soup.select('.products-pagination>nav>ul>li:nth-child(6)')[0].get_text(strip=True))
print(last_page)
