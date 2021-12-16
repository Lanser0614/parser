import requests
from bs4 import BeautifulSoup
import pymysql
import time
from googletrans import Translator
import json


def transliterate(text):
    diction = {
        'ў': "o`",
        'ғ': "g`",
        'ш': 'sh',
        'ё': 'yo',
        'ю': 'yu',
        'я': 'ya',
        'ц': 'ts',
        'ч': 'ch',
        "Щ": "Sh",
        "щ": "sh",
        'Ў': "O`",
        'Ғ': "G`",
        'ль ': "l ",
        'Ш': 'Sh',
        'Ч': 'Ch',
        'Ё': 'Yo',
        'Ю': 'Yu',
        'Я': 'Ya',
        'Ц': 'Ts',
        "ъ": "'",
        "Ъ": "'",
        "ь": "'",
        "Ь": "'",
        'А': 'A',
        'Б': 'B',
        'Д': 'D',
        'Е': 'E',
        'Ф': 'F',
        'Г': 'G',
        'Ҳ': 'H',
        'И': 'I',
        'Ж': 'J',
        'К': 'K',
        'Л': 'L',
        'М': 'M',
        'Н': 'N',
        'О': 'O',
        'П': 'P',
        'Қ': 'Q',
        'Р': 'R',
        'С': 'S',
        'Т': 'T',
        'У': 'U',
        'В': 'V',
        'Х': 'X',
        'Й': 'Y',
        'З': 'Z',
        'а': 'a',
        'б': 'b',
        'д': 'd',
        'е': 'e',
        'ф': 'f',
        'г': 'g',
        'ҳ': 'h',
        'и': 'i',
        'ж': 'j',
        'к': 'k',
        'л': 'l',
        'м': 'm',
        'н': 'n',
        'о': 'o',
        'п': 'p',
        'қ': 'q',
        'р': 'r',
        'с': 's',
        'т': 't',
        'у': 'u',
        'в': 'v',
        'х': 'x',
        'й': 'y',
        'з': 'z',
    }
    for key in diction:
        text = text.replace(diction[key], key)
    return text


def nano():
    con = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='kattabozor', charset='utf8')
    cur = con.cursor()
    req = requests.get('https://nanoreview.net/')
    soup = BeautifulSoup(req.text, features="lxml")
    hrefs = soup.select(".mdl-card__title-text")
    time.sleep(5)

    for i in range(0,5) :

        href = hrefs[i].select_one('a')['href']
        req = requests.get(hrefs[i].a["href"])
        soup = BeautifulSoup(req.text, features="lxml")
        article = soup.select_one(".gd-fullstory-text__story")

        images_dict = {}
        images_soup = article.find_all('img')

        # Создание массива со ссылками на изображения
        for image in images_soup:
            images_dict[images_soup.index(image)] = "https://nanoreview.net" + image['src']


        if len(images_soup)==1:
            for txt in article.findAll('img'):
                txt.replace_with("")
        else:
            for txt in article.findAll('img'):
                txt.replace_with("{{image}}")

        main_image = images_dict[0]
        images_dict.pop(0,"https://olcha.uz/dist/images/logo.svg")
        images_dict = json.dumps(images_dict)

        ru_title = hrefs[i].select_one('a').get_text(strip=True).replace("'", '`').replace('"', '`')
        description_ru = soup.find(attrs={'name' : "description"})['content'].replace("'", '`').replace('"', '`')
        russian_text = article.get_text(strip=True).split("Также подписывайтесь на наши страницы", 1)[0].replace("'", '`').replace('"', '`').replace("{{image}}",'',1)

        # # translator = Translator()
        # translator = Translator()

        # # UZ
        # uz_title = translator.translate(ru_title, dest="uz", src="ru",).text.replace("'", '`').replace('"', '`')
        # time.sleep(5)

        # uz_description = translator.translate(description_ru, dest="uz", src="ru",).text.replace("'", '`').replace('"', '`')
        # time.sleep(5)

        # uz_text = translator.translate(russian_text, dest="uz", src="ru",).text.replace("'", '`').replace('"', '`')
        # time.sleep(5)

        # # Kiril
        # oz_title = transliterate(uz_title).replace("'", '`').replace('"', '`')
        # oz_description = transliterate(uz_description).replace("'", '`').replace('"', '`')
        # oz_text= transliterate(uz_text).replace('имаге', 'image').replace("'", '`').replace('"', '`')
        # # print(uz_description,uz_title)
        # cur.execute(f"INSERT INTO kattabozor.articles (title, url, images, text_rus, text_uz, text_uz_cyrillic,parsed,description_ru,title_uz,title_oz,description_uz,description_oz,main_image) VALUES ('{ru_title}', '{href}', '{images_dict}', '{russian_text}', '{uz_text}', '{oz_text}',0,'{description_ru}','{uz_title}','{oz_title}','{uz_description}','{oz_description}','{main_image}') ON DUPLICATE KEY UPDATE url = '{href}'")
        # print(cur.rowcount)
        # con.commit()

        sql = "INSERT INTO articles (title, url, images, text_rus, parsed, description_ru, main_image) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = [(
        ru_title, href, images_dict, russian_text, 0, description_ru, main_image,
        )]
    # print(val)
        cur.executemany(sql, val)
        con.commit()
        print(cur.rowcount, "was inserted.")

nano()
