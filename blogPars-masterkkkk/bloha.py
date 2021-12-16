import requests
from bs4 import BeautifulSoup
import pymysql
import time
import time
from googletrans import Translator
import json
import pyodbc

# con =  pyodbc.connect('Driver={SQL Server};'
#                       'Server=DONIYOR;'
#                       'Database=database_name;'
#                       'Trusted_Connection=yes;')
con = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='kattabozor',charset='utf8')
cur = con.cursor()

def bloha(con):
    req = requests.get("https://bloha.ru")
    soup = BeautifulSoup(req.text, features="lxml")
    href = soup.select_one(".post-thumbnail").a["href"]
    ru_title = soup.select_one(".post-thumbnail").a["title"]
    time.sleep(5)

    article_request = requests.get(href)
    article_soup = BeautifulSoup(article_request.text, features="lxml")
    article = article_soup.select_one(".entry-inner")

    # images_dict = {}
    # images_soup = article.find_all('img', class_="size-full")
    # for image in images_soup:
    #     images_dict[images_soup.index(image)] = image['data-src']
    # images_dict = json.dumps(images_dict)
    images_dict = {}
    images_soup = article.find_all("img", class_="size-full")

    for image in images_soup:
        images_dict[images_soup.index(image)] = image["data-src"]

    if len(images_soup) == 1:
        for txt in article.findAll("img"):
            # txt.replace_with("<br>{{image}}<br>")
            txt.replace_with("")
    else:
        for txt in article.findAll("img"):
            #     # txt.replace_with("<br>{{image}}<br>")
            txt.replace_with("{{image}}")

    main_image = images_dict[0]
    images_dict.pop(0, "https://olcha.uz/dist/images/logo.svg")
    images_dict = json.dumps(images_dict)

    russian_text = (
        article.get_text(strip=True)
        .split("Источник:", 1)[0]
        .split("Читаем еще:", 1)[0]
        .split("Читайте также:", 1)[0]
        .replace(" '", " `")
        .replace('"', "`")
        .replace("'", "`")
        .replace(' "', " `")
    )
    russian_text.replace(
        "(adsbygoogle = window.adsbygoogle || []).push({});(adsbygoogle = window.adsbygoogle || []).push({});",
        "",
    )
    description_ru = (
        article_soup.find(attrs={"itemprop": "description"})["content"]
        .replace("'", "`")
        .replace('"', "`")
    )

    sql = "INSERT INTO articles (title, url, images, text_rus, parsed, description_ru, main_image) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = [(
        ru_title, href, images_dict, russian_text, 0, description_ru, main_image,
    )]
    # print(val)
    cur.executemany(sql, val)
    con.commit()
    print(cur.rowcount, "was inserted.")
bloha(con)



# bloha(con)
# print(con)
#  print(images_dict)
# with open('text.txt',"w") as f:
#    f.write(text)
#    f.close()
