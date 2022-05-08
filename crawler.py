import os

import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta

url_patten = "https://cbmc.club/posts/"


def crawler():
    # Get article count
    dir_path = "articles"
    init_count = 1
    exception_post, articles = [], {}

    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            init_count += 1

    count = init_count

    exception_post = fetch_all_empty(count)

    while True:
        if count not in exception_post:
            page = fetch_page(count)
            if page == 0:
                print("All article fetched successfully")
                break
            articles[count] = page
            print(f"Article #{count} fetched.")

        count += 1

    file_name = "articles.json"
    with open(dir_path + "/" + file_name, 'w') as json_file:
        json.dump(articles, json_file)


def fetch_page(post_number: int) -> object:
    url = url_patten + str(post_number)
    web_page = requests.get(url).text

    soup = BeautifulSoup(web_page, 'html.parser')
    tag_content_search = soup.find("meta", property="og:description")

    formatted_content = str(tag_content_search).replace('<meta content="靠北麥塊 » cbmc.club › 檢視文章 • ', '').replace(
        '" property="og:description"/>', '')

    if stop_code(formatted_content):
        return 0

    try:
        img = str(soup.find_all("img", class_="image_max_width")[1]).split(" ")[2].replace('src="', '').replace('"/>',
                                                                                                                '')
    except IndexError as e:
        img = "None"

    return {"content": formatted_content, "img": img}


def stop_code(content: str):
    if "無此文章" in content:
        return True
    else:
        return False


def fetch_all_empty(count: int):
    init, continuous_null, exception_posts = count, 0, []
    while True:
        if fetch_page(init) == 0:
            exception_posts.append(init)
            continuous_null += 1
        else:
            continuous_null = 0

        if continuous_null == 25:
            break

        init += 1

    exception_posts.append(datetime.now().strftime("%d/%m/%Y"))
    with open("exception_post.json", 'w') as json_file:
        json.dump(exception_posts, json_file)
    print("Exception List Updated.")
    return exception_posts
