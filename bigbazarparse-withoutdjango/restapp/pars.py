# -*- coding: utf-8 -*-
import  json
import requests
from bs4 import BeautifulSoup
import pymysql
import time
from selenium import webdriver
import time
import argparse
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.proxy import Proxy, ProxyType
import re




HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
            'accept': '*/*'}
con = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='kattabozor',charset='utf8')
start_time = time.time()

def selenka(con,code):
	binary = '/usr/bin/firefox' 
	options = webdriver.FirefoxOptions() 
	options.binary = binary
	options.add_argument('start-maximized')
	options.add_argument('--headless')
	options.add_argument('--disable-gpu')
	options.add_argument('--disable-extensions')
	path_to_driver = "usr/local/bin"

	# prox = Proxy()
	# prox.proxy_type = ProxyType.MANUAL
	# prox.http_proxy = "94.180.133.31:4145"
	# prox.add_to_capabilities(capabilities)
	# capabilities = webdriver.DesiredCapabilities.CHROME

	driver = webdriver.Firefox(options=options,executable_path = GeckoDriverManager().install())
	# driver = webdriver.Firefox(options=options,desired_capabilities=capabilities,executable_path = GeckoDriverManager().install())
	try:
		try:
			for j in range(13000):
				cur = con.cursor()
				cur.execute("SELECT name FROM products where parsed = 0;")
				row = cur.fetchone()
				print(row)
				driver.get(f"https://www.google.com/search?q=  olcha.uz {row[0]}")
				html = driver.page_source
				soup = BeautifulSoup(html, features="lxml")
				try:
					rows = soup.find_all('div', {'class': "g"})
					for i in range(0, 5):
						href = rows[i].select("div>div>a")
						href = href[0]['href']
						if 'olcha.uz/product' in href:
							href = href.replace('https://www.olcha.uz/product/view/', '').replace('https://olcha.uz/product/view/', '')
							print(row[0])
							cur.execute(f"UPDATE products SET olcha_url='{href}', parsed=1 WHERE name='{row[0]}';")
							print("The query affected {} rows".format(cur.rowcount))
							con.commit()
							break
						else:
							cur.execute(f"UPDATE products SET olcha_url='Не найден', parsed=1 WHERE name='{row[0]}';")
							print("The query affected {} rows".format(cur.rowcount))
							con.commit()
							break
				except IndexError:
					print('ErroringASDsadas' ,row[0])
					cur.execute(f"UPDATE products SET olcha_url='Не найден', parsed=1 WHERE name='{row[0]}';")
					con.commit()
		except TypeError:
			driver.quit()
			cur = con.cursor()
			print('s')
			cur.execute("UPDATE products SET parsed=0")
			con.commit()
			driver.close()
	except:
		driver.quit()
	finally:
		driver.quit()

def get_category(con,code):
	url = 'https://www.kattabozor.uz/'
	homeUrl = 'https://www.kattabozor.uz'
	cur = con.cursor()
	req = requests.get(url, headers=HEADERS)
	soup = BeautifulSoup(req.text, features="lxml")
	tables = soup.find_all('div', {'class': "col-6 col-md-auto mb-3 mb-md-0"})
	other = soup.find_all('div', {'class': "col-6 col-md-auto mb-3"})
	array = tables + other

	
	array.pop()
	# print(array)
	sql = "INSERT INTO category (href, name, parsed) VALUES (%s, %s, %s)"
	for child in array:	
		# print(child.find('a')['href'], child.find('a').get_text(strip=True))
		# print(child['href'], child.get_text(strip=True))
		val = (child.find('a')['href'], child.find('a').get_text(strip=True), 0)
		cur.execute(sql, val)
		con.commit()
		print(cur.rowcount, "record inserted.")	
http_proxy  = "http://172.67.182.113:80"
https_proxy = "https://10.10.1.11:1080"
ftp_proxy   = "ftp://10.10.1.10:3128"

proxyDict = {
              "http"  : http_proxy,
            }


def get_products(con,code):
	try:
		for i in range(30000):
			c=0
			cur = con.cursor()
			cur.execute("SELECT href from kattabozor.category where parsed = 0 AND name LIKE 'Мобильные телефоны'")
			href = cur.fetchone()
			print(href[0])
			if href[0] == '/category/mobilnye-telefony?inStock=true':
				for i in range(1, 200):
					req = requests.get(f"https://www.kattabozor.uz{href[0]}&page={i}", proxies=proxyDict, headers=HEADERS )
					print(f"https://www.kattabozor.uz{href[0]}&page={i}")
					soup = BeautifulSoup(req.text, features="lxml")
					# print(soup)
					product_card = soup.select(".border-0")
					# print(product_card)
					if product_card==[]:
						break
					else:
						for el in product_card:

							name = str(el.select('.product-name >h3> a')[0].get_text(strip=True))
							name = name.replace("'", '`')
							print(name)

							try:
								
								
								price=el.select('.font-weight-bolder')[0].get_text(strip=True).replace(' сум', "").replace(" ", '')
								price = re.findall("\d+", price)[0]
								print(price)
								merchant_name = 'kattabozor'
								# anchor_key = el.select('.product-name>a')[0]['href']

								print(name)
								print('В  таблицу  products ')
								cur = con.cursor()
								sql = "INSERT INTO kattabozor.products (name, price, merchant,  parsed) VALUES (   %s, %s, %s, %s)"
								val = (name, price, merchant_name,  0)
								cur.execute(sql, val)
								con.commit()
								print(cur.rowcount, "record inserted.")	
								# cur.execute(
								# f"INSERT INTO kattabozor.products (name, price, merchant, anchor_key, parsed) VALUES ('{name}','{price}','{merchant_name}','{anchor_key}',0)ON DUPLICATE KEY UPDATE parsed=1;")
								# con.commit()

							except IndexError:
								# try:
								product_url = el.select('.product-name>h3>a')[0]['href']
								print(product_url)
								print('В  таблицу  urls ')
								cur.execute(
									f"INSERT INTO kattabozor.phone_urls (product_url,phone_name,parsed) VALUES ('{product_url}','{name}',0) ON DUPLICATE KEY UPDATE phone_name = '{name}';")
								con.commit()
								# except IndexError:
								# 	print(name)
								# 	print('Propusk')
								# 	continue
			else:
				print(href)
				for i in range(1, 300):
					req = requests.get(f'https://www.kattabozor.uz{href[0]}&page={i}')
					soup = BeautifulSoup(req.text, features="lxml")
					product_card = soup.select(".border-0")
					if not product_card:
						break
					else:
						for el in product_card:
							c+=1
							try:
								name = el.select('.product-name>a')[0].get_text(strip=True)
								name = str(name).replace("'", '`')
								price = el.select('.col-md-5>h5>b')[0].get_text(strip=True).replace(' сум', "").replace(" ", '')
								merchant_name = el.select('.merchant-name')[0].get_text(strip=True)
								unique_key = el.select('.product-name>a')[0]['href']
								# unique_key = unique_key.replace('/', '')
								cur.execute(f"INSERT INTO  kattabozor.products (price, parsed,anchor_key, name, merchant_name) VALUES ('{price}', 0, '{unique_key}', '{name}', '{merchant_name}' ON DUPLICATE KEY UPDATE price='{product_price}' ;")
								con.commit()
							except IndexError:
								continue
			cur.execute(f"UPDATE kattabozor.category SET parsed = 1 where href = '{href[0]}'")
			print(c)
			con.commit()
	except TypeError:
		cur = con.cursor()
		cur.execute("UPDATE kattabozor.category SET parsed = 0")
		con.commit()



def insert_phone(con,code):
	try:
		for i in range(300):
			cur = con.cursor()
			cur.execute("SELECT product_url FROM phone_urls where parsed = 0;")
			row = cur.fetchone()
			req = requests.get(f'https://www.kattabozor.uz{row[0]}')
			soup = BeautifulSoup(req.text, features="lxml")
			phone_block = soup.select(".border-0")
			for el in phone_block:
				try:
					product_name = el.select('.product-name>a')[0].get_text(strip=True)
					product_name = product_name.replace("'", '')
					product_price = el.select('.col-md-5>h5>b')[0].get_text(strip=True).replace(' сум', "").replace(" ", '')
					merchant_name = el.select('.merchant-name')[0].get_text(strip=True)
					unique_key = el.select('.product-name>a')[0]['href']
					cur.execute(f"INSERT INTO products (name, price, merchant, anchor_key) VALUES ('{product_name}', '{product_price}', '{merchant_name}', '{unique_key}') ON DUPLICATE KEY UPDATE price='{product_price}', anchor_key = '{unique_key}'")	  
					con.commit()
				except IndexError:
					continue
			cur.execute(f"UPDATE kattabozor.phone_urls SET parsed = 1 where product_url = '{row[0]}'")
			con.commit()
	except TypeError:
		cur = con.cursor()
		cur.execute("UPDATE kattabozor.phone_urls SET parsed = 0")
		con.commit()

def google_query(con):
	cur = con.cursor()
	cur.execute("SELECT name FROM products where parsed = 0;")
	row = cur.fetchone()
	row = row[0].replace(" ", '+')
	print(row)
	print(f'https://duckduckgo.com/?q=olcha.uz '+row)
	req = requests.get(f'https://duckduckgo.com/?q=olcha.uz '+row)
	soup = BeautifulSoup(req.text, features="lxml")
	print(soup)
	block = soup.select('.result__a')
	for i in range(0, 3):
		href = block[i]['href']
		print(href)

	print(block)

FUNCTION_MAP = {'get_category' : get_category,
				'get_products': get_products,
				'insert_phone': insert_phone,
				'selenka' : selenka,
				}

parser = argparse.ArgumentParser()
parser.add_argument('command', choices=FUNCTION_MAP.keys())
args = parser.parse_args()
func = FUNCTION_MAP[args.command]
func(code=885370239386, con=pymysql.connect(host='127.0.0.1', user='root', passwd='', db='kattabozor'))




print("--- %s seconds ---" % (time.time() - start_time))
