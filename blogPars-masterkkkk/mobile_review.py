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
    con = pymysql.connect(host='127.0.0.1', user='root', password='', db='kattabozor', charset='utf8')
    cur = con.cursor()
    req = requests.get('https://mobile-review.com/news/tag/samsung')
    soup = BeautifulSoup(req.text, features="lxml")
    post_cards = soup.find_all('div', class_='grid-item')
    time.sleep(5)

    for i in range(0,6) :
        title_ru = post_cards[i].find('div', class_='title').text.strip()
        href = post_cards[i].find('a').get('href')
        req_post = requests.get(post_cards[i].a["href"])
        soup_post = BeautifulSoup(req_post.text, features="lxml")
        article = soup_post.find('div', class_='newsSingle').select_one('section')
        article_ru = article.select_one("p").get_text(strip=True)
        images_dict = {}
        images_soup = article.find_all('img')
        try:
            for image in images_soup:
                images_dict[images_soup.index(image)] = image['src']
            main_image = images_dict[0]
        except:
            images_dict = {}
            main_image = 'no image'


        if len(images_soup) == 1:
            for txt in article.findAll('img'):
                txt.replace_with("")
        else:
            for txt in article.findAll('img'):
                txt.replace_with("{{image}}")

        images_dict = json.dumps(images_dict)
        description_ru = title_ru

        #Translation

        # translator = Translator()
        # uz_title = translator.translate(title_ru, dest="uz", src="ru").text.replace("'", '`').replace('"', '`')
        # time.sleep(3)
        # uz_description = uz_title
        # time.sleep(3)
        # uz_text = translator.translate(article_ru, dest="uz", src='ru').text.replace("'", '`').replace('"', '`')
        # time.sleep(3)

        # oz_title = transliterate(uz_title).replace("'", '`').replace('"', '`')
        # time.sleep(3)
        # oz_description = oz_title
        # time.sleep(3)
        # oz_text= transliterate(uz_text).replace('имаге', 'image').replace("'", '`').replace('"', '`')
        # time.sleep(3)

        # cur.execute(
        #     f" INSERT INTO kattabozor.articles (title, url, images, text_rus, text_uz, text_uz_cyrillic,parsed,description_ru,title_uz,title_oz,description_uz,description_oz,main_image) VALUES ('{title_ru}', '{href}', '{images_dict}', '{article_ru}', '{uz_text}', '{oz_text}',0,'{description_ru}','{uz_title}','{oz_title}','{uz_description}','{oz_description}','{main_image}') ON DUPLICATE KEY UPDATE url = '{href}'")
        # con.commit()
        
    sql = "INSERT INTO articles (title, url, images, text_rus, parsed, description_ru, main_image) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = [(
         title_ru, href, images_dict, article_ru, 0, description_ru, main_image,
    )]
    # print(val)
    cur.executemany(sql, val)
    con.commit()
    print(cur.rowcount, "was inserted.")

nano()
