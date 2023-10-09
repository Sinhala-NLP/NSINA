from urllib.request import urlopen as uReq

import re
from bs4 import BeautifulSoup as soup
import time
import json

base_url = 'https://lankatruth.com/si/?p='

with open("status.json", "r") as jsonFile:
    status = json.load(jsonFile)

for i in range(status['last_working_pid'], 153100, 1):
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
    try:
        currentClient = uReq(current_url)
        current_raw_html = currentClient.read()
        currentClient.close()

        current_soup = soup(current_raw_html, "html.parser")
        news_item = current_soup.find_all("div", {"class": "elementor-widget-wrap elementor-element-populated"})

        if news_item is not None and bool(news_item):
            source = 'Lankatruth'
            headline = news_item[0].find("h1", {"class": "elementor-heading-title elementor-size-default"}).get_text()
            ts = news_item[0].find("div", {"class": "jeg_meta_date"}).get_text().strip()
            news_body = ""
            category = news_item[0].find("a", {"rel": "category"}).get_text()

            new_body_paras = news_item[0].find("div", {"data-widget_type": "theme-post-content.default"}).find("div", {"class": "elementor-widget-container"})
            for data in new_body_paras(['div', 'figure']):
                # Remove tags
                data.decompose()

            for para in new_body_paras.find_all('p'):
                for span in para.find_all('span'):
                    news_body = news_body+' '+span.get_text()
                news_body = news_body + ' ' + para.get_text()

            news_body = re.sub("[<].*?[>]", "", news_body)
            news_body = ''.join(news_body.splitlines())
            news_body = news_body.replace(" ", "")
            news_body = news_body.strip()

            if bool(headline) and bool(news_body):
                news_model['Source'] = source
                news_model['Timestamp'] = ts
                news_model['Headline'] = headline
                news_model['News Content'] = news_body
                news_model['URL'] = current_url
                news_model['Category'] = category

                with open("../../data/lankatruth/" + str(i) + ".json", 'w', encoding='utf8') as file:
                    json.dump(news_model, file, ensure_ascii=False)

                with open("status.json", "r") as jsonFile:
                    status = json.load(jsonFile)

                status["last_working_pid"] = i

                with open("status.json", "w") as jsonFile:
                    json.dump(status, jsonFile)

                print(i)
    except:
        continue

    time.sleep(2)
