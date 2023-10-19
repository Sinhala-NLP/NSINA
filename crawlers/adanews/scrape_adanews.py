from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup
from bs4 import Comment
import time
import json

base_url = 'https://www.ada.lk/0/0/0-'

with open("status.json", "r") as jsonFile:
    status = json.load(jsonFile)

pause_counter = 0

for i in range(status['last_working_nid'], 1, -1):

    if i % 500 == 0:
        time.sleep(50)

    news_model = {
        "Source": None,
        "Timestamp": None,
        "Headline": None,
        "News Content": None,
        "URL": None,
        "Category": None,
        "Parent URL": None
    }

    current_url = base_url + str(i)
    req = Request(
        current_url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.181 Safari/537.36 '
        }
    )
    try:
        currentClient = uReq(req)
        current_raw_html = currentClient.read()
        currentClient.close()

        current_soup = soup(current_raw_html, "html.parser")
        root_news_item = current_soup.find("section", {"id": "main"})
        news_item = current_soup.find("div", {"class": "row mainrow"})
        # news_meta = current_soup.find_all("script", {"type": "application/ld+json"})

        if news_item is not None and bool(news_item):
            source = 'Ada News'
            headline = news_item.find("h1", {"class": "single-head"}).get_text()
            ts = news_item.find("span", {"class": "sr-date"}).get_text()
            ts = ts.replace("- ", "").strip()
            news_body = ""
            category = root_news_item.find("nav", {"aria-label": "breadcrumb"}).find_all("li", {"class": "breadcrumb-item"})

            # category_json = json.loads(news_meta[1].get_text())
            category = category[1].get_text()

            # remove commented tags
            for element in news_item(text=lambda text: isinstance(text, Comment)):
                element.extract()

            new_body_paras = news_item.find("div", {"class": "single-body-wrap"}).find_all('p')

            for para in new_body_paras:
                news_body = news_body + para.get_text() + ' '

            if bool(headline) and bool(news_body):
                news_model['Source'] = source
                news_model['Timestamp'] = ts
                news_model['Headline'] = headline
                news_model['News Content'] = news_body
                news_model['URL'] = current_url
                news_model['Category'] = category

                with open("../../data/adanews/" + str(i) + ".json", 'w', encoding='utf8') as file:
                    json.dump(news_model, file, ensure_ascii=False)

                with open("status.json", "r") as jsonFile:
                    status = json.load(jsonFile)

                status["last_working_nid"] = i

                with open("status.json", "w") as jsonFile:
                    json.dump(status, jsonFile)

                print(i)

    except:
        continue

    time.sleep(2)
