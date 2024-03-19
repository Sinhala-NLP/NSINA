# Created by Hansi on 10/10/2023

import json
import os.path

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


source = 'dinamina'
category = 'entertainment'
origin_url = 'https://www.dinamina.lk/category/entertainment/'

output_folder = f'../data/{source}/{category}'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for page_id in range(1, 450):
    print(f'processing page {page_id}')
    url = f'{origin_url}/page/{page_id}/'
    print(url)
    json_path = os.path.join(output_folder, f'{page_id}.json')

    # crawling logic
    response = requests.get(url)
    print(response)
    if response.status_code == 404:
        break

    if response.status_code != 200:
        for i in range(1, 10):
            print(f'load url: attempt {i+1}')
            response = requests.get(url)
            if response.status_code == 200:
                break

    if response.status_code != 200:
        continue

    soup = BeautifulSoup(response.content, "lxml")
    news_stories = soup.select('h2[class*="penci-entry-title entry-title"]')

    for idx, story in tqdm(enumerate(news_stories)):
        try:
            story_url = story.a['href']

            story_response = requests.get(story_url)
            story_soup = BeautifulSoup(story_response.content, "lxml")

            title = story_soup.select('h1[class="post-title single-post-title entry-title"]')[0].get_text(strip=True)

            content_div = story_soup.select('div[class="inner-post-entry entry-content"]')
            paragraphs = content_div[0].select('p')
            content_list = [paragraph.get_text(separator='\n', strip=True) for paragraph in paragraphs]
            content = '\n\n'.join(content_list)

            time_div = story_soup.select('div[class="post-box-meta-single"]')
            timestamp = time_div[0].select('span')[0].get_text(strip=True)

            dict = {'Source': source, 'Timestamp': timestamp, 'Headline': title, 'News Content': content, 'URL': story_url, 'Category': category, 'Parent URL': url}
            json_object = json.dumps(dict, ensure_ascii=False, indent=7)

            json_path = os.path.join(output_folder, f'{page_id}_{idx}.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                f.write(json_object)

        except:
            print(f'Encountered a processing error at interation {idx}')



