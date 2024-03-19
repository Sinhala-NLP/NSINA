# Created by Hansi on 22/09/2023
import json
import os.path

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

source = 'hirunews'
category = 'Local News'
origin_url = 'https://www.hirunews.lk/local-news.php?'
# url = 'https://www.hirunews.lk/local-news.php?pageID=1'

output_folder = '../data/hirunews/local-news'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for page_id in range(4001, 6001):
    print(f'processing page {page_id}')
    url = f'{origin_url}pageID={page_id}'
    json_path = os.path.join(output_folder, f'{page_id}.json')

    # crawling logic
    response = requests.get(url)
    if response.status_code != 200:
        for i in range(1, 10):
            print(f'load url: attempt {i+1}')
            response = requests.get(url)
            if response.status_code == 200:
                break

    if response.status_code != 200:
        continue

    soup = BeautifulSoup(response.content, "lxml")
    news_stories = soup.find_all('div', {'class': 'row', 'style':'margin-bottom:10px'})

    for idx, story in tqdm(enumerate(news_stories)):
        try:
            story_url = story.a['href']

            story_response =requests.get(story_url)
            story_soup = BeautifulSoup(story_response.content, "lxml")

            title = story_soup.select('h1.main-tittle')[0].get_text(strip=True)
            content = story_soup.select('div[id*="article-phara"]')[0].get_text(separator='\n', strip=True)
            timestamp = story_soup.select('p')[0].get_text(strip=True)

            dict = {'Source': source, 'Timestamp': timestamp, 'Headline': title, 'News Content': content, 'URL': story_url, 'Category': category, 'Parent URL': url}
            json_object = json.dumps(dict, ensure_ascii=False, indent=7)

            json_path = os.path.join(output_folder, f'{page_id}_{idx}.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                f.write(json_object)

        except:
            print(f'Encountered a processing error at interation {idx}')
