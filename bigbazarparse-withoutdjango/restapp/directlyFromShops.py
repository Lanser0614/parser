import requests
from bs4 import BeautifulSoup
import pymysql
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.firefox.options import Options
#import argparse
#from webdriver_manager.firefox import GeckoDriverManager
#from selenium.webdriver.common.proxy import Proxy, ProxyType

con = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='kattabozor', charset='utf8')
# start_time = time.time()
PATH = r"C:\Работа\Парсинг\geckodriver.exe"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
            'accept': '*/*'}

def asaxiy(con):
    cur = con.cursor()
    for i in range(1, 4):
        url = 'https://asaxiy.uz/product/telefony-i-gadzhety/telefony?per-page=60&size=60&page={i}'
        req = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(req.text, features="lxml")
        cards = soup.select('.product__item-wrapper')
        
        for card in cards:
            href = "https://asaxiy.uz"+card.select_one(".product__item-img")['href']
            price = card.select_one('.product__item-price').get_text(strip=True).replace(' сум', '')
            name = card.select_one('.product__item__info-title').get_text(strip=True).replace("'","")
            # print(name)
            cur.execute(
                f"INSERT INTO kattabozor.phones (name, price, merchant, parsed,href) VALUES ('{name}', '{price}', 'asaxiy', '0','{href}') ON DUPLICATE KEY UPDATE price='{price}', href = '{href}'")
            con.commit()
#
#
def openshop(con):
    cur = con.cursor()
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    print(chrome_options.binary_location)
    # firefox_options = Options()
    # firefox_options.add_argument("--headless")
    # driver = webdriver.Firefox()
    # driver = webdriver.Firefox(options=firefox_options, executable_path="/usr/bin/geckodriver",firefox_binary="/usr/bin/firefox")

    # req = requests.get(f'https://openshop.uz/shop/subcategory/phones?page=1', headers=header)
    driver.get("https://openshop.uz/shop/subcategory/phones?page=1")
    soup = BeautifulSoup(driver.page_source, features="lxml")
    prod_pagin = soup.select('.products-pagination')[0]
    lll = prod_pagin.select(".d-xl-block")[1]
    last_page = int(lll.select('a')[0].get_text(strip=True))
   
    for i in range(1, last_page+1):
        driver.get(f'https://openshop.uz/shop/subcategory/phones?page={i}',)
        soup = BeautifulSoup(driver.page_source, features="lxml")
        cards = soup.select('.products-box-bar')[0].select('.product-details')
        for card in cards:
            href = card.select_one("a")['href']
            name = card.select('.product-title')[0]
            name = name.select('a')[0].get_text(strip=True).replace("'","")
            price = card.select('.product-price')[0]
            price = price.select('strong')[0].get_text(strip=True).replace(',', ' ').replace('UZS', '')
            cur.execute(
                f"INSERT INTO kattabozor.phones (name, price, merchant, parsed, href) VALUES ('{name}', '{price}', 'openshop', '0','{href}') ON DUPLICATE KEY UPDATE price='{price}', href = '{href}'")
            con.commit()
            print(href)
            print("The query affected {} rows".format(cur.rowcount))

        # driver.quit()



def mediapark(con):
    cur = con.cursor()
    for i in range(1, 26):
        url = "https://mediapark.uz/products/category/40?page={i}"
        req = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(req.text, features="lxml")
        cards = soup.select(".product_list_text")
        # print(cards)
        for card in cards:
            href = "https://mediapark.uz"+card.select_one(".product_list_name")['href']
            name = card.select(".product_list_name")[0].get_text(strip=True).replace("'", '')
            price = card.select(".product_list_price")[0].get_text(strip=True).replace('сум', '')
            # print(price)
            merchant = 'mediapark'
            sql = "INSERT INTO kattabozor.phones (name, price, merchant, parsed, href)  VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE  price = VALUES(price), href = VALUES(href)"
            vars = (
                name, price, merchant, 0, href
            )
            cur.execute(sql, vars)
            con.commit()
            print(cur.rowcount, "record inserted.")	



def texnomart(con):
    cur = con.cursor()
    url = "https://texnomart.uz/ru/katalog/smartfony?page=1"
    req = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(req.text, features="lxml")
    pagination = soup.select_one(".pagination")
    last_page = int(pagination.select_one("li:nth-of-type(9)").get_text(strip=True))
    print(last_page)

    for i in range(1,last_page+1):
        req = requests.get('https://texnomart.uz/ru/katalog/smartfony?page='+str(i))
        soup = BeautifulSoup(req.text,features="lxml")
        phones_container = soup.select_one("#product-group-sort-wrapper")
        products = phones_container.select(".products-cards__item")
        for phone_card in products:
            content = phone_card.select_one(".content")
            href = "https://texnomart.uz"+content.select_one(".name")['href']
            name = content.select_one('.name').get_text(strip=True).replace("'","")
            price = content.select_one('.price').get_text(strip=True).replace("Цена:","").replace("cум","").replace(" ","")
            merchant = 'texnomart'
            print(price)
            sql = "INSERT INTO kattabozor.phones (name, price, merchant, parsed, href) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE price = VALUES(price), href = VALUES(href)"
            vars = (  name, price, merchant, 0, href)
            cur.execute(sql, vars)
            con.commit()
            print(cur.rowcount, "record inserted.")	

def all(con):
    # asaxiy(con)
    openshop(con)
    # mediapark(con)
    # texnomart(con)


#
all(con)


def parsFromGoogle(con):
    # prox = Proxy()
    # prox.proxy_type = ProxyType.MANUAL
    # prox.http_proxy = "154.16.202.22:8080"
    # capabilities = webdriver.DesiredCapabilities.FIREFOX
    # prox.add_to_capabilities(capabilities)

    driver = webdriver.Chrome("/usr/bin/chromedriver")
    # driver = webdriver.Firefox(executable_path=PATH, desired_capabilities=capabilities)
    cur = con.cursor()
    cur.execute("SELECT name FROM phones where parsed = 0;")
    rows = cur.fetchall()

    if rows == []:
        print("NONE")
        return
        # cur.execute(f"UPDATE phones SET  parsed=0")
        # con.commit()
    for row in rows:
        driver.get(f"https://www.google.com/search?q=  olcha.uz {row[0]}")
        soup = BeautifulSoup(driver.page_source, features="lxml")
        try:
            results = soup.find_all('div', {'class': "g"})
            for i in range(0, 4):
                href = results[i].select("div>div>a")[0]['href']
                if (
                        'olcha.uz/product' in href or 'https://olcha.uz/index.php/product/' in href or 'https://olcha.uz/oz/product/view/' in href
                        or 'https://olcha.uz/uz/product/view/' in href):
                    href = href.replace(
                        'https://www.olcha.uz/product/view/', '').replace(
                        'https://olcha.uz/product/view/', '').replace(
                        'https://olcha.uz/index.php/product/view', '').replace(
                        'https://olcha.uz/oz/product/view/', '').replace(
                        'https://olcha.uz/uz/product/view/', '').replace(
                        'https://olcha.uz/ru/product/view/', '').replace("http://olcha.uz/product/view/",'').replace("https://api.olcha.uz/product/view/",'')
                    print(href)
                    cur.execute(f"UPDATE phones SET olcha_url='{href}', parsed=1 WHERE name='{row[0]}';")
                    con.commit()
                    break
                else:
                    cur.execute(f"UPDATE phones SET olcha_url='undefined' WHERE name='{row[0]}';")
                    con.commit()
                    continue
            time.sleep(60)
        except Exception as error:
            print(error)
            quit()
            cur.execute(f"UPDATE phones SET olcha_url='{error}', parsed=0 WHERE name='{row[0]}';")
            con.commit()


# > nav > ul: nth - child(6) > a
