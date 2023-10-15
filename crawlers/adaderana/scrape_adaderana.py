from urllib.request import urlopen as uReq

import re
from bs4 import BeautifulSoup as soup
import time
import json

movies = {'movies': []}
base_url = 'https://sinhala.adaderana.lk/news.php?nid='

with open("status.json", "r") as jsonFile:
    status = json.load(jsonFile)

for i in range(status['last_working_nid'], 187750, 1):
    news_model = {
        "Source": None,
        "Timestamp": None,
        "Headline": None,
        "News Content": None,
        "URL": None,
        "Category": None,
        "Parent URL": None
    }

    current_url = 'https://sinhala.adaderana.lk/news.php?nid='+str(i)

    currentClient = uReq(current_url)
    current_raw_html = currentClient.read()
    currentClient.close()

    current_soup = soup(current_raw_html, "html.parser")
    news_item = current_soup.find("article", {"class": "news"})

    if news_item is not None:
        source = 'Adaderana'
        headline = news_item.find("h1", {"class": "news-heading"}).get_text()
        ts = " ".join(news_item.find("p", {"class": "news-datestamp english-font"}).get_text().strip().split())
        news = " ".join(news_item.find("div", {"class": "news-content"}).get_text().strip().split())

        if bool(headline) and bool(news):
            news_model['Source'] = source
            news_model['Timestamp'] = ts
            news_model['Headline'] = headline
            news_model['News Content'] = news
            news_model['URL'] = current_url

            with open("../../data/adaderana/"+str(i)+".json", 'w', encoding='utf8') as file:
                json.dump(news_model, file, ensure_ascii=False)

            with open("status.json", "r") as jsonFile:
                status = json.load(jsonFile)

            status["last_working_nid"] = i

            with open("status.json", "w") as jsonFile:
                json.dump(status, jsonFile)

            print(i)

    time.sleep(3)

# print(len(movies['movies']))
# with open('movie_list_5000.json', 'w') as file:
#     # indented_data=json.dumps(movies, indent=2)
#     json.dump(movies, file)
# print('***********END***********')