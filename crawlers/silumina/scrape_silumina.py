from datetime import timedelta, date
from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup
import time
import json


with open("status.json", "r") as jsonFile:
    status = json.load(jsonFile)

print('started')


def daterange(start_date, end_date):
    for single_date in (start_date - timedelta(n) for n in range(10000)):
        print(single_date)
        yield single_date;
    # for n in range(int((end_date - start_date).days)):
    #     yield start_date + timedelta(n)


end_date = date(2023, 1, 1)
start_date = date(2023, 12, 29)
for single_date in daterange(start_date, end_date):
    if start_date < end_date:
        break
    dateStr = single_date.strftime("%Y/%m/%d")
    dateStrFileName = single_date.strftime("%Y-%m-%d")
    base_url = 'https://www.silumina.lk/' + dateStr + '/news-features/'
    print(base_url)

    for i in range(status['last_working_nid'], 1, -1):
        if i == 3000:
            break

        news_model = {
            "Source": None,
            "Timestamp": None,
            "Headline": None,
            "News Content": None,
            "URL": None,
            "Category": None,
            "Parent URL": None
        }

        current_url = base_url + str(i) + '/'
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
            news_item = current_soup.find("div", {"id": "soledad_wrapper"})

            if news_item is not None and bool(news_item):
                source = 'Silumina'
                headline = news_item.find("h1", {"class": "post-title single-post-title entry-title"}).get_text()
                ts = " ".join(
                    news_item.find("div", {"class": "post-box-meta-single"}).find('span').text.strip().split())
                news = " ".join(
                    news_item.find("div", {"class": "inner-post-entry entry-content"}).get_text().strip().split())

                if bool(headline) and bool(news):
                    news_model['Source'] = source
                    news_model['Timestamp'] = ts
                    news_model['Headline'] = headline
                    news_model['News Content'] = news
                    news_model['URL'] = current_url

                    with open("../../data/silumina/" + dateStrFileName + str(i) + ".json", 'w', encoding='utf8') as file:
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

    status["last_working_nid"] = 9800
