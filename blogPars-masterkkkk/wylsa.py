import requests
from bs4 import BeautifulSoup
import pymysql
import time
from googletrans import Translator
import json
import cssutils
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def wylsa():
    options = webdriver.ChromeOptions()
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
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get('https://wylsa.com/')
    con = pymysql.connect(host='127.0.0.1', user='root', password='', db='kattabozor', charset='utf8')
    cur = con.cursor()
    soup = BeautifulSoup(driver.page_source, features="lxml")
    post_cards = soup.select('.postCard')
    print(soup)
    print(len(post_cards))
    time.sleep(5)


    for post_card in post_cards:
        ru_title = post_card.find('div', class_='postCard-title').text.strip()
        href = post_card.find('a').get('href')
        figure_style = post_card.find('figure')['style']
        style = cssutils.parseStyle(figure_style)
        image_url = style['background-image']
        image_url = image_url.replace('url(', '').replace(')', '')
        req_post = requests.get(post_card.a["href"])
        soup_post = BeautifulSoup(req_post.text, features="lxml")
        try:
            description_ru = soup_post.find(attrs={'name': "description"})['content'].replace("'", '`').replace('"', '`')
        except:
            description_ru = ''

        russian_text = soup_post.select_one("article").find('div', class_='content__inner')
        twitter = russian_text.find_all('div', class_="twitter-tweet twitter-tweet-rendered")
        images_dict = {}
        images_soup = russian_text.find_all('img')
        for image in images_soup:
            images_dict[images_soup.index(image)] = image['src']
        if len(images_soup) == 1:
            for txt in russian_text.findAll('img'):
                txt.replace_with("")
        else:
            for txt in russian_text.findAll('img'):
                txt.replace_with("{{image}}")
        images_dict = json.dumps(images_dict)
        if len(twitter) == 1:
            for txt in russian_text.findAll('div', class_='twitter-tweet twitter-tweet-rendered'):
                txt.replace_with("")
        else:
            russian_text = soup_post.select_one("article").find('div', class_='content__inner').get_text(strip=True)
        section_style = soup_post.select_one("article").find('section', class_="article__img")['style']
        style = cssutils.parseStyle(section_style)
        main_image = style['background-image']
        main_image = main_image.replace('url(', '').replace(')', '')


        # Translation part
        # translator = Translator()

        # # UZ
        # uz_title = translator.translate(ru_title, dest="uz", src="ru",)
        # time.sleep(3)

        # uz_description = translator.translate(description_ru, dest="uz", src="ru",)
        # time.sleep(3)

        # uz_text = translator.translate(russian_text, dest="uz", src="ru",)
        # time.sleep(3)


        # # UZ
        # uz_title = uz_title.text.replace("'", '`').replace('"', '`')
        # uz_description = uz_description.text.replace("'", '`').replace('"','`')
        # uz_text = uz_text.text.replace("'", '`').replace('"', '`').replace("Image", 'image')

        # # Kiril
        # oz_title = transliterate(uz_title).replace("'", '`').replace('"', '`')
        # oz_description = transliterate(uz_description).replace("'", '`').replace('"', '`')
        # oz_text = transliterate(uz_text).replace("'", '`').replace('"', '`').replace('имаге', 'image')
        # print(ru_title)
        # cur.execute(
        #     f"#  INSERT INTO kattabozor.articles (title, url, images, text_rus, text_uz, text_uz_cyrillic,parsed,description_ru,title_uz,title_oz,description_uz,description_oz,main_image) VALUES ('{ru_title}', '{href}', '{images_dict}', '{russian_text}', '{uz_text}', '{oz_text}',0,'{description_ru}','{uz_title}','{oz_title}','{uz_description}','{oz_description}','{main_image}') ON DUPLICATE KEY UPDATE url = '{href}'")
        # con.commit()
        # time.sleep(4)
        sql = "INSERT INTO articles (title, url, images, text_rus, parsed, description_ru, main_image) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = [(
        ru_title, href, images_dict, russian_text, 0, description_ru, main_image,
         )]
 
        cur.executemany(sql, val)
        con.commit()
        print(cur.rowcount, "was inserted.")
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
wylsa()

