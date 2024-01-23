from datetime import timedelta, date
from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup
import time
import json

with open("status.json", "r") as jsonFile:
    status = json.load(jsonFile)


def crawl_ur_ls(all_urls, current_url):
    print('crawler')
    # crawl data in current_url
    news_model = {
        "Source": None,
        "Timestamp": None,
        "Headline": None,
        "News Content": None,
        "URL": None,
        "Category": None,
        "Parent URL": None
    }

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
        news_item = current_soup.find("div", {"id": "root"}).find("div", {"class": "bbc-16ubpog"}).find("div", {"class": "bbc-1ff36h2"})

        all_hrefs = news_item.findAll("a")
        if all_hrefs:
            for href in all_hrefs:
                if 'articles' in href["href"] or 'sri-lanka' in href["href"] or 'world' in href["href"]:
                    full_url = None
                    if 'https://www.bbc.com/' not in href["href"]:
                        full_url = 'https://www.bbc.com/' + href["href"]
                    if full_url and full_url not in all_urls:
                        all_urls.append(full_url)

        if news_item is not None and bool(news_item):
            source = 'bbc'
            white_path = None
            black_path = None
            world_path = None

            if news_item.find("div", {"class": "bbc-1kb1fna"}) and news_item.find("div", {"class": "bbc-1kb1fna"}).find("div", {"class": "bbc-bg8vrv"}) and news_item.find("div", {"class": "bbc-1kb1fna"}).find("div", {"class": "bbc-bg8vrv"}).find("div", {"class": "bbc-1cvxiy9"}) and news_item.find("div", {"class": "bbc-1kb1fna"}).find("div", {"class": "bbc-bg8vrv"}).find("div", {"class": "bbc-1cvxiy9"}).find("main", {"class": "bbc-fa0wmp"}):
                white_path = news_item.find("div", {"class": "bbc-1kb1fna"}).find("div", {"class": "bbc-bg8vrv"}).find("div", {"class": "bbc-1cvxiy9"}).find("main", {"class": "bbc-fa0wmp"})
            elif news_item.find("div", {"class": "bbc-1ide38"}) and news_item.find("div", {"class": "bbc-1ide38"}).find("div", {"class": "bbc-bg8vrv"}) and news_item.find("div", {"class": "bbc-1ide38"}).find("div", {"class": "bbc-bg8vrv"}).find("div", {"class": "bbc-1cvxiy9"}) and news_item.find("div", {"class": "bbc-1ide38"}).find("div", {"class": "bbc-bg8vrv"}).find("div", {"class": "bbc-1cvxiy9"}).find("main", {"class": "bbc-fa0wmp"}):
                black_path = news_item.find("div", {"class": "bbc-1ide38"}).find("div", {"class": "bbc-bg8vrv"}).find("div", {"class": "bbc-1cvxiy9"}).find("main", {"class": "bbc-fa0wmp"})
            elif news_item.find("div", {"class": "e1j2237y4 bbc-1wf62vy ebmt73l0"}) and news_item.find("div", {"class": "e1j2237y4 bbc-1wf62vy ebmt73l0"}).find("div", {"class": "e1j2237y3 bbc-irdbz7 ebmt73l0"}) and news_item.find("div", {"class": "e1j2237y4 bbc-1wf62vy ebmt73l0"}).find("div", {"class": "e1j2237y3 bbc-irdbz7 ebmt73l0"}).find("main", {"role": "main"}):
                world_path = news_item.find("div", {"class": "e1j2237y4 bbc-1wf62vy ebmt73l0"}).find("div", {"class": "e1j2237y3 bbc-irdbz7 ebmt73l0"}).find("main", {"role": "main"})

            # crawl inside data
            if white_path and white_path.find("div", {"class": "bbc-1151pbn ebmt73l0"}) and white_path.find("div", {"class": "bbc-1151pbn ebmt73l0"}).find("h1", {"class": "bbc-pdt3nl e1p3vdyi0"}):
                headline = white_path.find("div", {"class": "bbc-1151pbn ebmt73l0"}).find("h1", {"class": "bbc-pdt3nl e1p3vdyi0"}).get_text()
            elif black_path and black_path.find("div", {"class": "bbc-1151pbn ebmt73l0"}) and black_path.find("div", {"class": "bbc-1151pbn ebmt73l0"}).find("strong", {"class": "ewk8wmc0 bbc-jb1q0x eglt09e1"}):
                headline = black_path.find("div", {"class": "bbc-1151pbn ebmt73l0"}).find("strong", {"class": "ewk8wmc0 bbc-jb1q0x eglt09e1"}).get_text()
            elif world_path and world_path.find("div", {"class": "bbc-1151pbn ebmt73l0"}) and world_path.find("div", {"class": "bbc-1151pbn ebmt73l0"}).find("h1", {"class": "bbc-pdt3nl e1p3vdyi0"}):
                headline = world_path.find("div", {"class": "bbc-1151pbn ebmt73l0"}).find("h1", {"class": "bbc-pdt3nl e1p3vdyi0"}).get_text()
            else:
                headline = ""

            if white_path and white_path.find("div", {"class": "bbc-19j92fr ebmt73l0"}) and white_path.find("div", {"class": "bbc-19j92fr ebmt73l0"}).find("time", {"class": "bbc-chpnlr e1mklfmt0"}):
                ts = white_path.find("div", {"class": "bbc-19j92fr ebmt73l0"}).find("time", {"class": "bbc-chpnlr e1mklfmt0"}).get_text()
            elif black_path and black_path.find("div", {"class": "bbc-19j92fr ebmt73l0"}) and black_path.find("div", {"class": "bbc-19j92fr ebmt73l0"}).find("time", {"class": "bbc-16tewd0 e1mklfmt0"}):
                ts = black_path.find("div", {"class": "bbc-19j92fr ebmt73l0"}).find("time", {"class": "bbc-16tewd0 e1mklfmt0"}).get_text()
            elif world_path and news_item.find("div", {"class": "e1j2237y4 bbc-1wf62vy ebmt73l0"}) and news_item.find("div", {"class": "e1j2237y4 bbc-1wf62vy ebmt73l0"}).find("div", {"class": "e1j2237y3 bbc-irdbz7 ebmt73l0"}) and news_item.find("div", {"class": "e1j2237y4 bbc-1wf62vy ebmt73l0"}).find("div", {"class": "e1j2237y3 bbc-irdbz7 ebmt73l0"}).find("main", {"role": "main"}) and news_item.find("div", {"class": "e1j2237y4 bbc-1wf62vy ebmt73l0"}).find("div", {"class": "e1j2237y3 bbc-irdbz7 ebmt73l0"}).find("main", {"role": "main"}).find("div", {"class": "e1j2237y6 bbc-q4ibpr ebmt73l0"}) and news_item.find("div", {"class": "e1j2237y4 bbc-1wf62vy ebmt73l0"}).find("div", {"class": "e1j2237y3 bbc-irdbz7 ebmt73l0"}).find("main", {"role": "main"}).find("div", {"class": "e1j2237y6 bbc-q4ibpr ebmt73l0"}).find("time", {"class": "bbc-chpnlr e1mklfmt0"}):
                ts = news_item.find("div", {"class": "e1j2237y4 bbc-1wf62vy ebmt73l0"}).find("div", {"class": "e1j2237y3 bbc-irdbz7 ebmt73l0"}).find("main", {"role": "main"}).find("div", {"class": "e1j2237y6 bbc-q4ibpr ebmt73l0"}).find("time", {"class": "bbc-chpnlr e1mklfmt0"}).get_text()

            news = ""
            if white_path and len(white_path.findAll("div", {"class": "bbc-19j92fr ebmt73l0"})) > 1:
                paras = white_path.findAll("div", {"class": "bbc-19j92fr ebmt73l0"})
                for k in range(1, len(paras)):
                    if paras[k].find("p", {"class": "bbc-fgzozg e17g058b0"}):
                        news += paras[k].find("p", {"class": "bbc-fgzozg e17g058b0"}).get_text() + " "
            elif black_path and len(black_path.findAll("div", {"class": "bbc-19j92fr ebmt73l0"})) > 1:
                paras = black_path.findAll("div", {"class": "bbc-19j92fr ebmt73l0"})
                for j in range (1, len(paras)):
                    if paras[j].find("p", {"class": "bbc-1dc5iw9 e17g058b0"}):
                        news += paras[j].find("p", {"class": "bbc-1dc5iw9 e17g058b0"}).get_text() + " "
            elif world_path and len(world_path.findAll("div", {"class": "bbc-19j92fr ebmt73l0"})) > 1:
                paras = world_path.findAll("div", {"class": "bbc-19j92fr ebmt73l0"})
                for i in range(1, len(paras)):
                    if paras[i].find("p", {"class": "bbc-fgzozg e17g058b0"}):
                        news += paras[i].find("p", {"class": "bbc-fgzozg e17g058b0"}).get_text() + " "

            with open("status.json", "r") as jsonFile:
                status = json.load(jsonFile)
            nid = current_url.split('/')[len(current_url.split('/')) - 1]
            if bool(headline) and bool(news) and nid not in status['nids']:
                news_model['Source'] = source
                news_model['Timestamp'] = ts
                news_model['Headline'] = headline
                news_model['News Content'] = news
                news_model['URL'] = current_url

                with open("../../data/bbc/" + nid + ".json", 'w', encoding='utf8') as file:
                    json.dump(news_model, file, ensure_ascii=False)

                print(nid)
                status['nids'].append(nid)

                with open("status.json", "w") as jsonFile:
                    json.dump(status, jsonFile)

    except:
        print('except 2', current_url)
        pass

    time.sleep(2)
    # find all the links in the current_url and add them to the all_urls
    return all_urls


def crawl_articles(all_urls, starting_index):
    url_count = len(all_urls)
    for i in range(starting_index, url_count):
        print('i = ',i)
        current_url = all_urls[i]
        nid = current_url.split('/')[len(current_url.split('/')) - 1]
        if nid not in status['nids']:
            all_urls = crawl_ur_ls(all_urls, current_url)
    if len(all_urls) > url_count:
        crawl_articles(all_urls, url_count)


def crawl_topics(page_number):
    print('started')
    if page_number == 1:
        # topic_url = 'https://www.bbc.com/sinhala/topics/cg7267dz901t'
        # topic_url = 'https://www.bbc.com/sinhala/topics/c83plvepnq1t'
        topic_url = 'https://www.bbc.com/sinhala/topics/c7zp5zxk8jxt'
    else:
        # topic_url = 'https://www.bbc.com/sinhala/topics/cg7267dz901t?page='+str(page_number)
        print('page_number = ',page_number)
        # topic_url = 'https://www.bbc.com/sinhala/topics/c83plvepnq1t?page=' + str(page_number)
        topic_url = 'https://www.bbc.com/sinhala/topics/c7zp5zxk8jxt?page=' + str(page_number)
    req = Request(
        topic_url,
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
        topics = current_soup.find("div", {"id": "root"}).find("div", {"class": "bbc-16ubpog"}).find("div", {
            "class": "bbc-1ff36h2"}).find("main", {"class": "bbc-18yqr0l"}).find("div", {"class": "bbc-1tzeti0"}).find("div", {"data-testid": "curation-grid-normal"}).find("ul", {"class": "bbc-1kz5jpr"})

        all_topics = topics.findAll("li", {"class": "bbc-t44f9r"})
        print("all_topics = ", len(all_topics))
        for topic in all_topics:
            # base_url = 'https://www.bbc.com/sinhala/articles/c725y76e7zgo'
            base_url = topic.find("div", {"class": "bbc-bjn8wh e1v051r10"}).find("div", {"class": "promo-text"}).find("h2", {"class": "bbc-6e44zt e47bds20"}).find("a")["href"]
            base = [base_url]
            crawl_articles(base, 0)


    except:
        print('except 1',topic_url)
        pass

# p = page number
for p in range(1, 40):
    crawl_topics(p)
